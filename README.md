# 🛤️ RailScan AI — Railway Track Crack Detection

> AI-powered crack detection system for Indian Railways — built for Hack India 2025

---

## 🚨 Problem Statement

India has **67,000 km of railway tracks**. Manual crack detection using trolleys is:
- Slow and labor-intensive
- Cannot cover all remote sections
- Prone to human error
- Reactive, not proactive

**Result:** Undetected cracks cause derailments, accidents, and loss of life.

---

## 💡 Solution

**RailScan AI** uses Computer Vision (OpenCV) to instantly detect cracks in railway track images with:

- 📷 Simple image upload interface
- 🤖 Automatic crack detection using edge detection + contour analysis
- 📊 Severity classification (Safe / Minor / Moderate / Severe)
- 📍 Location tagging for record-keeping
- ⚡ Actionable recommendations for maintenance teams

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python + Flask |
| Computer Vision | OpenCV |
| Frontend | HTML + CSS + JavaScript |
| Image Processing | Canny Edge Detection + Contour Analysis |

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/railway-crack-detection.git
cd railway-crack-detection
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
```
http://localhost:5000
```

---

## 🔍 How It Works

1. User uploads a railway track image
2. Image is converted to grayscale
3. Gaussian blur reduces noise
4. Canny Edge Detection identifies edges
5. Morphological operations enhance crack features
6. Contour analysis finds and measures crack regions
7. Severity is calculated based on crack area % and count
8. Annotated result image is returned with recommendations

---

## 📊 Severity Levels

| Level | Crack Area | Action |
|-------|-----------|--------|
| ✅ Safe | < 0.5% | Regular inspection |
| ⚠️ Minor | 0.5% - 2% | Inspect within 7 days |
| 🔶 Moderate | 2% - 5% | Inspect within 24 hours |
| 🚨 Severe | > 5% | Suspend operations immediately |

---

## 🌐 Future Scope

- [ ] Drone integration for automated scanning
- [ ] Real-time video stream analysis
- [ ] GPS auto-tagging via mobile
- [ ] ML model trained on railway-specific dataset
- [ ] SMS/Email alerts to section engineers
- [ ] Historical scan dashboard

---

## 👩‍💻 Built By

Made with ❤️ for **Hack India 2025 — Open Claw Hackathon**

*Protecting 1.4 billion lives on 67,000 km of Indian Railways.*
