import requests
import json
import os
from urllib.parse import quote_plus
import hashlib
import base64

class ExternalAPIsChecker:
    def __init__(self, google_api_key=None):
        self.phishtank_api_url = "https://checkurl.phishtank.com/checkurl/"
        self.google_safe_browsing_api_url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
        self.google_api_key = google_api_key or os.getenv('GOOGLE_SAFE_BROWSING_API_KEY')
        self.phishtank_api_key = os.getenv('PHISHTANK_API_KEY')
        
    def check_phishtank(self, url):
        """Check if URL is in PhishTank database"""
        if not self.phishtank_api_key:
            return {'error': 'PhishTank API key not configured', 'is_phishing': False}
            
        try:
            headers = {
                'User-Agent': 'phishing-detector-extension/1.0',
                'Api-Key': self.phishtank_api_key
            }
            
            data = {
                'url': url,
                'format': 'json',
            }
            
            response = requests.post(
                self.phishtank_api_url,
                headers=headers,
                data=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'is_phishing': result.get('results', {}).get('in_database', False),
                    'verified': result.get('results', {}).get('verified', False),
                    'details_url': result.get('results', {}).get('phish_detail_page', '')
                }
            elif response.status_code == 403:
                print(f"PhishTank API authentication failed. Status: {response.status_code}")
                return {'error': 'PhishTank API authentication failed', 'is_phishing': False}
            else:
                print(f"PhishTank API error. Status: {response.status_code}, Response: {response.text}")
                return {'error': f'PhishTank API error: {response.status_code}', 'is_phishing': False}
        except Exception as e:
            print(f"PhishTank API exception: {str(e)}")
            return {'error': f'PhishTank API error: {str(e)}', 'is_phishing': False}
    
    def check_google_safe_browsing(self, url):
        """Check URL against Google Safe Browsing API"""
        if not self.google_api_key:
            return {'error': 'Google Safe Browsing API key not configured', 'is_dangerous': False}
            
        try:
            data = {
                'client': {
                    'clientId': 'phishing-detector-extension',
                    'clientVersion': '1.0.0'
                },
                'threatInfo': {
                    'threatTypes': [
                        'MALWARE', 'SOCIAL_ENGINEERING', 'UNWANTED_SOFTWARE', 
                        'POTENTIALLY_HARMFUL_APPLICATION'
                    ],
                    'platformTypes': ['ANY_PLATFORM'],
                    'threatEntryTypes': ['URL'],
                    'threatEntries': [{'url': url}]
                }
            }
            
            params = {'key': self.google_api_key}
            response = requests.post(
                self.google_safe_browsing_api_url,
                params=params,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                matches = result.get('matches', [])
                
                if matches:
                    return {
                        'is_dangerous': True,
                        'threat_types': list(set(match['threatType'] for match in matches))
                    }
                return {'is_dangerous': False}
            elif response.status_code == 400:
                print(f"Google Safe Browsing API error. Status: {response.status_code}, Response: {response.text}")
                return {'error': 'Invalid API request', 'is_dangerous': False}
            else:
                print(f"Google Safe Browsing API error. Status: {response.status_code}, Response: {response.text}")
                return {'error': f'Google Safe Browsing API error: {response.status_code}', 'is_dangerous': False}
        except Exception as e:
            print(f"Google Safe Browsing API exception: {str(e)}")
            return {'error': f'Google Safe Browsing API error: {str(e)}', 'is_dangerous': False}
    
    def check_url(self, url):
        """Check URL against both PhishTank and Google Safe Browsing"""
        results = {
            'phishtank': self.check_phishtank(url),
            'google_safe_browsing': self.check_google_safe_browsing(url)
        }
        
        # Determine overall threat assessment
        is_threat = (
            results['phishtank'].get('is_phishing', False) or
            results['google_safe_browsing'].get('is_dangerous', False)
        )
        
        results['is_threat'] = is_threat
        return results 