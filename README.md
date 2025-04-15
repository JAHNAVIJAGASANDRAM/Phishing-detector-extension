<<<<<<< HEAD
# Phishing Detector Browser Extension

A browser extension that uses Machine Learning (Random Forest) to detect potential phishing websites in real-time.

## Features

- Real-time website analysis
- Machine learning-based detection using Random Forest
- Visual alerts for suspicious websites
- Detailed analysis of website features
- Browser popup with comprehensive information
- Top banner warning for potentially dangerous sites

## Setup Instructions

### 1. Backend Setup

1. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Run the backend server:
```bash
cd backend
python app.py
```

The server will run on http://localhost:5000

### 2. Extension Setup

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" in the top right
3. Click "Load unpacked" and select the `extension` folder

## Usage

1. Make sure the backend server is running
2. Visit any website
3. The extension will automatically analyze the website
4. If a potential phishing site is detected:
   - A red banner will appear at the top of the page
   - The extension icon will change to a warning icon
5. Click the extension icon to see detailed analysis

## Features Analyzed

- Domain length
- Path length
- Subdomain count
- HTTPS usage
- Form count
- Input field count
- External links
- Password field presence
- Submit button presence

## Technical Details

The extension uses a Random Forest classifier trained on various website features. The model analyzes both URL structure and page content to make predictions. The current implementation uses synthetic data for demonstration, but can be easily modified to use real phishing datasets for production use.

## Security Notes

- The extension requires permission to access website content for analysis
- All analysis is done locally through your backend server
- No data is sent to external servers
- The model can be retrained with custom datasets

## Development

To modify the extension:
1. Edit the files in the `extension` folder
2. Reload the extension in Chrome
3. For backend changes, modify `app.py` and restart the server

## License

MIT License 
=======
# Phishing-Detection
phishing is the most common treat
we are building it using java
It is an google extension
>>>>>>> ff9885b410f2d1ed67b1e149faeefc59cac6fd53
