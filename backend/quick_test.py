import requests
import json
import time

def test_url(url):
    print(f"\nAnalyzing URL: {url}")
    print("-" * 60)
    
    # Wait for server to be ready
    time.sleep(2)
    
    try:
        response = requests.post(
            'http://127.0.0.1:5000/analyze',
            json={'url': url},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\nAnalysis Results:")
            print(f"Is Phishing: {result.get('is_phishing', False)}")
            print(f"Confidence: {result.get('confidence', 0.0) * 100:.1f}%")
            
            if result.get('risk_factors'):
                print("\nRisk Factors Detected:")
                for factor in result['risk_factors']:
                    print(f"- {factor}")
            
            if result.get('features'):
                print("\nURL Features:")
                features = result['features']
                print(f"- URL Length: {features.get('url_length')}")
                print(f"- Domain Length: {features.get('domain_length')}")
                print(f"- Number of Dots: {features.get('num_dots')}")
                print(f"- Number of Hyphens: {features.get('num_hyphens')}")
                print(f"- Number of Underscores: {features.get('num_underscores')}")
                print(f"- Special Characters: {features.get('num_special_chars')}")
                print(f"- Has HTTPS: {'Yes' if features.get('has_https') else 'No'}")
                print(f"- Suspicious TLD: {'Yes' if features.get('has_suspicious_tld') else 'No'}")
                print(f"- Suspicious Keywords: {'Yes' if features.get('has_suspicious_keywords') else 'No'}")
                print(f"- Mixed Numbers and Characters: {'Yes' if features.get('has_mixed_nums_chars') else 'No'}")
                
            print("\nModel Votes:")
            if result.get('model_votes'):
                votes = result['model_votes']
                print(f"- Random Forest: {votes.get('random_forest', False)}")
                print(f"- Decision Tree: {votes.get('decision_tree', False)}")
            
        else:
            print(f"Error: Server returned status code {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure the Flask server is running on port 5000")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    suspicious_url = "https://maldeep.e8dc.in/GDsU_JX?afM_di=a4BwmG5ncWKclYF5xXBpaHZ4YJ2Xs2Z"
    test_url(suspicious_url) 