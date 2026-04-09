from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
CORS(app)
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_cracks(image_path):
    """
    Crack detection using image processing techniques.
    Uses edge detection, thresholding, and contour analysis.
    """
    img = cv2.imread(image_path)
    if img is None:
        return None, 0, "error"

    original = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Edge detection using Canny
    edges = cv2.Canny(blurred, 50, 150)

    # Morphological operations to enhance crack features
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area and aspect ratio (cracks are usually elongated)
    crack_contours = []
    total_crack_area = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:  # Filter small noise
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = max(w, h) / (min(w, h) + 1)
            if aspect_ratio > 2 or area > 500:  # Elongated shapes or large areas
                crack_contours.append(contour)
                total_crack_area += area

    # Calculate crack percentage
    total_area = img.shape[0] * img.shape[1]
    crack_percentage = (total_crack_area / total_area) * 100

    # Draw crack contours on original image
    result_img = original.copy()
    cv2.drawContours(result_img, crack_contours, -1, (0, 0, 255), 2)

    # Add bounding boxes around major cracks
    for contour in crack_contours:
        area = cv2.contourArea(contour)
        if area > 500:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(result_img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Determine severity
    if crack_percentage < 0.5 and len(crack_contours) < 3:
        severity = "No Crack / Safe"
        color = (0, 255, 0)
    elif crack_percentage < 2 or len(crack_contours) < 8:
        severity = "Minor Crack - Monitor"
        color = (0, 165, 255)
    elif crack_percentage < 5 or len(crack_contours) < 15:
        severity = "Moderate Crack - Inspection Needed"
        color = (0, 100, 255)
    else:
        severity = "Severe Crack - Immediate Action Required"
        color = (0, 0, 255)

    # Add text overlay
    cv2.putText(result_img, severity, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.putText(result_img, f"Crack Area: {crack_percentage:.2f}%", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Convert result image to base64
    _, buffer = cv2.imencode('.jpg', result_img)
    result_base64 = base64.b64encode(buffer).decode('utf-8')

    # Convert edge detection image to base64
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    _, edge_buffer = cv2.imencode('.jpg', edges_colored)
    edge_base64 = base64.b64encode(edge_buffer).decode('utf-8')

    return {
        'result_image': result_base64,
        'edge_image': edge_base64,
        'crack_percentage': round(crack_percentage, 2),
        'crack_count': len(crack_contours),
        'severity': severity,
        'status': 'crack_detected' if len(crack_contours) > 2 else 'safe'
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    location = request.form.get('location', 'Unknown Location')
    track_id = request.form.get('track_id', 'N/A')

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        result = detect_cracks(filepath)

        if result is None:
            return jsonify({'error': 'Could not process image'}), 500

        result['location'] = location
        result['track_id'] = track_id
        result['filename'] = filename

        # Clean up uploaded file
        os.remove(filepath)

        return jsonify(result)

    return jsonify({'error': 'Invalid file type. Please upload JPG or PNG.'}), 400

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(host='0.0.0.0', port=10000)
