import requests
from feature_extraction import FeatureExtractor
from models import PhishingDetector
import traceback

def debug_url(url):
    print(f"\nTesting URL: {url}")
    print("-" * 50)
    
    try:
        # Test feature extraction
        print("1. Testing feature extraction...")
        fe = FeatureExtractor()
        features = fe.extract_url_features(url)
        print(f"Features extracted successfully: {features}")
        
        # Test model prediction
        print("\n2. Testing model prediction...")
        pd = PhishingDetector()
        base_features = [
            features['url_length'], 
            features['num_dots'],
            features['num_hyphens'],
            features['num_underscores'],
            features['num_slashes'],
            features['num_digits'],
            features['num_special_chars'],
            features['domain_length'],
            features['path_length'],
            features['has_https']
        ]
        result = pd.predict(base_features)
        print(f"Prediction result: {result}")
        
        # Test API endpoint
        print("\n3. Testing API endpoint...")
        response = requests.post(
            'http://localhost:5000/analyze',
            json={'url': url},
            headers={'Content-Type': 'application/json'}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        print("\nFull traceback:")
        print(traceback.format_exc())

if __name__ == "__main__":
    test_url = "https://io-start-trezorus-cdn.webflow.io/"
    debug_url(test_url) 