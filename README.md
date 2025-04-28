# Phishing URL Detector

A machine learning-based system for detecting phishing URLs using multiple detection methods and risk analysis.

## Features

- URL feature extraction
- Machine learning models (Random Forest and Decision Tree)
- Risk score calculation
- Multiple validation methods
- REST API endpoint for URL analysis

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
- `phishing_urls.csv` - Sample phishing URLs
- `legitimate_urls.csv` - Sample legitimate URLs

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
