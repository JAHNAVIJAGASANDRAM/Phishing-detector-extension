# Phishing URL Detector

A legitimate security research project for detecting and preventing phishing attacks. This machine learning-based system helps identify malicious URLs using multiple detection methods and risk analysis.

## Purpose
This project is developed for legitimate security research and protection purposes only. It is designed to:
- Help identify and prevent phishing attacks
- Provide educational resources for cybersecurity
- Contribute to the security research community
- Protect users from malicious websites

## Features

- URL feature extraction for security analysis
- Machine learning models (Random Forest and Decision Tree) for legitimate threat detection
- Risk score calculation for security assessment
- Multiple validation methods for accurate detection
- REST API endpoint for secure URL analysis

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd phishing_detector
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Train the models:
```bash
python retrain_models.py
```

## Usage

1. Start the server:
```bash
python app.py
```

2. Send POST requests to `/analyze` endpoint with URL:
```bash
curl -X POST http://localhost:5000/analyze -H "Content-Type: application/json" -d '{"url": "https://example.com"}'
```

## Project Structure

- `app.py` - Main Flask application
- `models.py` - Model loading and prediction
- `feature_extraction.py` - URL feature extraction
- `retrain_models.py` - Model training script
- `models/` - Directory for saved models
- `phishing_urls.csv` - Sample phishing URLs for research purposes
- `legitimate_urls.csv` - Sample legitimate URLs for research purposes

## Security and Ethics

This project is intended for legitimate security research and protection purposes only. The code and models should not be used for any malicious activities. Please refer to our [Security Policy](SECURITY.md) for more information.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
