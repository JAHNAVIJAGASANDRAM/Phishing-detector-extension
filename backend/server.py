# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return jsonify({'status': 'success', 'message': 'Flask is running!'})

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        url = data.get('url')
        
        # TODO: Implement your phishing detection logic here
        # For now, returning dummy response
        result = {
            'is_phishing': False,
            'phishing_probability': 0.0,
            'status': 'success'
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Changed to port 5001 to avoid conflicts 