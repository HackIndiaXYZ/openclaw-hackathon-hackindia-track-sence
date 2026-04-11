from flask import Flask, request, render_template, jsonify
import base64
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_cracks(image_bytes):
    try:
        dark_pixels = sum(1 for b in image_bytes if b < 50)
        dark_ratio = dark_pixels / len(image_bytes)
        crack_percentage = round(dark_ratio * 100, 2)
        crack_count = int(dark_pixels / 500)

        if crack_percentage < 1:
            severity = "No Crack / Safe"
        elif crack_percentage < 3:
            severity = "Minor Crack - Monitor"
        elif crack_percentage < 6:
            severity = "Moderate Crack - Inspection Needed"
        else:
            severity = "Severe Crack - Immediate Action Required"

        result_base64 = base64.b64encode(image_bytes).decode('utf-8')

        return {
            'result_image': result_base64,
            'edge_image': result_base64,
            'crack_percentage': crack_percentage,
            'crack_count': crack_count,
            'severity': severity,
            'status': 'crack_detected' if crack_percentage > 1 else 'safe'
        }
    except Exception as e:
        return None

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
        image_bytes = file.read()
        result = detect_cracks(image_bytes)
        if result is None:
            return jsonify({'error': 'Could not process image'}), 500
        result['location'] = location
        result['track_id'] = track_id
        return jsonify(result)
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, threaded=True)
