# Phishing URL Detector

A machine learning-based system for detecting phishing URLs in real-time. This project includes both a backend API service and a browser extension for protecting users against phishing attacks.

## Features

- Real-time URL analysis
- Machine learning-based detection using Random Forest and Decision Tree models
- Comprehensive feature extraction from URLs
- Browser extension for instant protection
- RESTful API service

## Project Structure

```
phishing_detector/
├── backend/             # Flask API server
│   ├── app.py          # Main server application
│   ├── feature_extraction.py  # URL feature extraction
│   └── models/         # ML model files
└── extension/          # Browser extension files
```

## Setup

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Start the server:
```bash
python app.py
```

The server will start on `http://localhost:5000`.

## API Endpoints

### POST /analyze
Analyzes a URL for phishing characteristics.

Request body:
```json
{
    "url": "https://example.com"
}
```

Response:
```json
{
    "is_phishing": false,
    "confidence": 0.1,
    "risk_factors": [],
    "model_votes": {
        "random_forest": false,
        "decision_tree": false
    }
}
```

## Browser Extension

The browser extension can be loaded as an unpacked extension in Chrome/Edge. It provides real-time protection by analyzing URLs as you browse.

## Security Notes

- The system uses multiple detection methods including:
  - Machine learning models
  - Pattern recognition
  - Domain analysis
  - URL structure analysis
  - Risk factor assessment

## License

MIT License
