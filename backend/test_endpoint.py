import requests
import json
import traceback

def test_url(url):
    endpoint = "http://localhost:5000/analyze"
    data = {"url": url}
    
    try:
        print(f"\nTesting URL: {url}")
        print("Sending request to:", endpoint)
        print("Request data:", json.dumps(data, indent=2))
        
        response = requests.post(endpoint, json=data)
        print(f"\nStatus Code: {response.status_code}")
        
        try:
            response_json = response.json()
            print(f"Is Phishing: {response_json['is_phishing']}")
            print(f"Confidence: {response_json['confidence']}")
            if response_json['risk_factors']:
                print("Risk Factors:")
                for factor in response_json['risk_factors']:
                    print(f"- {factor}")
            else:
                print("No risk factors detected")
            print("\nFull Response:", json.dumps(response_json, indent=2))
        except json.JSONDecodeError:
            print(f"Raw Response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    print("Testing various URLs...\n")
    
    # Test known phishing patterns
    test_url("https://reward-ondo.finance")  # Suspicious TLD and keyword
    test_url("http://paypal-secure.xyz/login")  # Brand impersonation
    test_url("https://banking.secure-login.com/@user")  # Suspicious characters and keywords
    
    # Test legitimate URLs
    test_url("https://www.google.com")  # Major brand
    test_url("https://www.microsoft.com")  # Another major brand
    test_url("https://example.com")  # Generic domain
    
    # Test edge cases
    test_url("data:text/html,<script>alert('test')</script>")  # Data URI
    test_url("javascript:alert('test')")  # JavaScript URI
    test_url("https://192.168.1.1/admin")  # IP address
    test_url("https://test.com:8080/path")  # Port number 