from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import joblib
import os
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)

# Initialize the model
model = RandomForestClassifier(n_estimators=100, random_state=42)

def extract_features(url):
    features = {}
    
    try:
        # URL-based features
        parsed = urlparse(url)
        features['domain_length'] = len(parsed.netloc)
        features['path_length'] = len(parsed.path)
        features['subdomain_count'] = len(parsed.netloc.split('.')) - 1
        features['has_https'] = 1 if parsed.scheme == 'https' else 0
        
        # Content-based features
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Form features
            features['form_count'] = len(soup.find_all('form'))
            features['input_count'] = len(soup.find_all('input'))
            features['external_links'] = len([a for a in soup.find_all('a', href=True) 
                                           if urlparse(a['href']).netloc 
                                           and urlparse(a['href']).netloc != parsed.netloc])
            
            # Security indicators
            features['has_password_field'] = 1 if soup.find('input', {'type': 'password'}) else 0
            features['has_submit_button'] = 1 if soup.find('input', {'type': 'submit'}) else 0
            
        except:
            # If we can't fetch the page, set content features to -1
            features['form_count'] = -1
            features['input_count'] = -1
            features['external_links'] = -1
            features['has_password_field'] = -1
            features['has_submit_button'] = -1
    
    except:
        return None
    
    return features

def train_model():
    # For demonstration, we'll create a simple synthetic dataset
    # In production, you should use a real phishing dataset
    np.random.seed(42)
    n_samples = 1000
    
    # Generate synthetic data
    data = {
        'domain_length': np.random.randint(5, 30, n_samples),
        'path_length': np.random.randint(0, 50, n_samples),
        'subdomain_count': np.random.randint(0, 4, n_samples),
        'has_https': np.random.randint(0, 2, n_samples),
        'form_count': np.random.randint(0, 5, n_samples),
        'input_count': np.random.randint(0, 10, n_samples),
        'external_links': np.random.randint(0, 20, n_samples),
        'has_password_field': np.random.randint(0, 2, n_samples),
        'has_submit_button': np.random.randint(0, 2, n_samples)
    }
    
    # Create more sophisticated rules for labeling
    df = pd.DataFrame(data)
    df['is_phishing'] = ((df['has_password_field'] == 1) & 
                        (df['external_links'] > 10) & 
                        (df['has_https'] == 0) & 
                        (df['subdomain_count'] > 2)).astype(int)
    
    # Train the model
    X = df.drop('is_phishing', axis=1)
    y = df['is_phishing']
    model.fit(X, y)
    
    # Save the model
    joblib.dump(model, 'phishing_model.joblib')

@app.route('/analyze', methods=['POST'])
def analyze_url():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    features = extract_features(url)
    if features is None:
        return jsonify({'error': 'Could not analyze URL'}), 400
    
    # Convert features to DataFrame
    features_df = pd.DataFrame([features])
    
    # Make prediction
    prediction = model.predict_proba(features_df)[0]
    
    return jsonify({
        'url': url,
        'phishing_probability': float(prediction[1]),
        'is_phishing': bool(prediction[1] > 0.7),  # threshold at 70%
        'features': features
    })

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    if not os.path.exists('phishing_model.joblib'):
        train_model()
    else:
        model = joblib.load('phishing_model.joblib')
    app.run(port=5000, debug=True) 