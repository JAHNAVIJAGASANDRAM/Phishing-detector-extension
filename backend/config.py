import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
GOOGLE_SAFE_BROWSING_API_KEY = os.getenv('GOOGLE_SAFE_BROWSING_API_KEY')

# PhishTank settings
PHISHTANK_API_KEY = os.getenv('PHISHTANK_API_KEY')  # Optional
PHISHTANK_USER_AGENT = "phishing-detector-extension/1.0"

# API Configuration
API_TIMEOUT = 5  # seconds
CACHE_DURATION = 3600  # 1 hour in seconds

# Feature Extraction Settings
MAX_URL_LENGTH = 200
MAX_DOMAIN_LENGTH = 50
SUSPICIOUS_TLDS = ['.xyz', '.top', '.work', '.live', '.loan', '.click', '.tk', '.ml', '.ga', '.cf']
SUSPICIOUS_KEYWORDS = [
    'login', 'signin', 'verify', 'secure', 'account', 'update', 'confirm',
    'banking', 'payment', 'security', 'password', 'credential'
]
BRAND_NAMES = [
    'paypal', 'apple', 'microsoft', 'amazon', 'google', 'facebook',
    'netflix', 'bank', 'wellsfargo', 'chase', 'citibank', 'hsbc'
] 