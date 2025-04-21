from flask import Flask, request, jsonify
from flask_cors import CORS
from feature_extraction import FeatureExtractor
import joblib
import json

app = Flask(__name__)
CORS(app)

# Load the models
rf_model = joblib.load('models/random_forest_model.pkl')
dt_model = joblib.load('models/decision_tree_model.pkl')
print("Models loaded successfully!")

def analyze_url(url):
    # Extract features
    extractor = FeatureExtractor()
    features = extractor.extract_url_features(url)
    print(f"Analyzing URL: {url}")
    print(f"Extracted features: {features}")
    
    # Convert features to list in correct order for model
    feature_list = []
    for feature in ['url_length', 'num_dots', 'num_hyphens', 'num_underscores', 
                   'num_slashes', 'num_digits', 'num_special_chars', 'domain_length',
                   'path_length', 'has_https', 'has_suspicious_tld', 
                   'has_suspicious_keywords', 'has_brand_name', 'has_mixed_nums_chars',
                   'num_subdomains']:
        feature_list.append(features.get(feature, 0))

    # Get model predictions
    rf_pred = rf_model.predict([feature_list])[0]
    dt_pred = dt_model.predict([feature_list])[0]
    
    # Calculate confidence based on risk factors
    risk_score = 0
    risk_factors = []
    
    # Check for random-looking strings (higher weight)
    if features.get('has_random_strings', 0):
        risk_score += 0.4
        risk_factors.append("Random-looking strings detected in URL")
    
    # Check for complex query parameters
    if features.get('has_complex_query', 0):
        risk_score += 0.2
        risk_factors.append("Suspicious query parameters")
    
    # Check for encoded strings (higher weight)
    if features.get('has_encoded_strings', 0):
        risk_score += 0.3
        risk_factors.append("Suspicious encoded strings")
    
    # Check for suspicious TLD (higher weight)
    if features.get('has_suspicious_tld', 0):
        risk_score += 0.3
        risk_factors.append("Suspicious top-level domain")
    
    # Check for suspicious keywords (higher weight)
    if features.get('has_suspicious_keywords', 0):
        risk_score += 0.3
        risk_factors.append("Suspicious keywords found")

    # Check for mixed numbers and characters in domain
    if features.get('has_mixed_nums_chars', 0):
        risk_score += 0.2
        risk_factors.append("Suspicious mix of numbers and letters in domain")

    # Check for excessive subdomains
    if features.get('num_subdomains', 0) > 2:
        risk_score += 0.2
        risk_factors.append("Excessive number of subdomains")

    # Check for suspicious URL encoding
    if features.get('has_suspicious_encoding', 0):
        risk_score += 0.3
        risk_factors.append("Suspicious URL encoding detected")

    # Check for IP address instead of domain
    if features.get('has_ip_address', 0):
        risk_score += 0.4
        risk_factors.append("IP address used instead of domain name")

    # Check for unusually long domain
    if features.get('domain_length', 0) > 30:
        risk_score += 0.2
        risk_factors.append("Unusually long domain name")

    # Check for short domain segments (like URL shorteners)
    if features.get('has_short_domain', 0):
        risk_score += 0.2
        risk_factors.append("Suspicious short domain segments")

    # If multiple risk factors are present, increase the risk score
    if len(risk_factors) >= 3:
        risk_score = min(1.0, risk_score * 1.5)  # Increase score but cap at 1.0

    # Determine if it's phishing based on risk score (lower threshold)
    is_phishing = risk_score >= 0.3 or rf_pred or dt_pred

    result = {
        'is_phishing': is_phishing,
        'confidence': risk_score,
        'risk_factors': risk_factors,
        'model_votes': {
            'random_forest': bool(rf_pred),
            'decision_tree': bool(dt_pred)
        }
    }
    
    print(f"ML model result: {result}")
    return result

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'No URL provided'}), 400
            
        url = data['url']
        print("Received analysis request")
        
        result = analyze_url(url)
        return jsonify(result)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(host='0.0.0.0', debug=True) 