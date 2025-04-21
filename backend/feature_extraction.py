import re
import ssl
import socket
import whois
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests

class FeatureExtractor:
    def __init__(self):
        self.features = {}
        # Known suspicious TLDs
        self.suspicious_tlds = {'finance', 'in', 'tk', 'ml', 'ga', 'cf', 'xyz', 'top', 'club', 'work', 'info', 'online', 'site'}
        
        # Known suspicious keywords
        self.suspicious_keywords = {
            'login', 'signin', 'verify', 'secure', 'account', 'password', 'credential',
            'reward', 'bonus', 'lucky', 'winner', 'payment', 'wallet', 'crypto',
            'update', 'confirm', 'verify', 'authenticate', 'recover', 'unlock',
            'access', 'restricted', 'security', 'important'
        }
        
        # Common brand names that might be impersonated
        self.brand_names = {
            'google', 'facebook', 'apple', 'microsoft', 'amazon', 'paypal',
            'netflix', 'linkedin', 'twitter', 'instagram', 'whatsapp', 'telegram'
        }
    
    def extract_all_features(self, url, html_content=None):
        """Extract all features from URL and content"""
        self.features.update(self.extract_url_features(url))
        self.features.update(self.extract_domain_features(url))
        
        if html_content:
            self.features.update(self.extract_content_features(html_content))
            
        return self.features
    
    def extract_url_features(self, url):
        try:
            parsed_url = urlparse(url)
            path = parsed_url.path
            query = parsed_url.query
            domain = parsed_url.netloc.lower()
            
            # Basic features
            features = {
                'url_length': len(url),
                'num_dots': url.count('.'),
                'num_hyphens': url.count('-'),
                'num_underscores': url.count('_'),
                'num_slashes': url.count('/'),
                'num_digits': sum(c.isdigit() for c in url),
                'num_special_chars': len(re.findall(r'[^a-zA-Z0-9]', url)),
                'domain_length': len(domain),
                'path_length': len(path),
                'has_https': 1 if url.startswith('https://') else 0
            }
            
            # Check for suspicious TLD
            tld_match = re.search(r'\.([a-zA-Z]+)$', domain)
            if tld_match and tld_match.group(1).lower() in self.suspicious_tlds:
                features['has_suspicious_tld'] = 1
            else:
                features['has_suspicious_tld'] = 0
            
            # Check for suspicious keywords in URL
            url_lower = url.lower()
            features['has_suspicious_keywords'] = 1 if any(keyword in url_lower for keyword in self.suspicious_keywords) else 0
            
            # Check for brand names
            features['has_brand_name'] = 1 if any(brand in domain for brand in self.brand_names) else 0
            
            # Check for mixed numbers and characters in domain
            domain_without_tld = domain.split('.')[0]
            has_letters = any(c.isalpha() for c in domain_without_tld)
            has_numbers = any(c.isdigit() for c in domain_without_tld)
            features['has_mixed_nums_chars'] = 1 if has_letters and has_numbers else 0
            
            # Count subdomains
            features['num_subdomains'] = len(domain.split('.')) - 1
            
            # Check for suspicious URL encoding
            features['has_suspicious_encoding'] = 1 if '%' in url or any(c in url for c in ['\\x', '\\u']) else 0
            
            # Check for data URI scheme
            features['has_data_uri'] = 1 if url.startswith('data:') else 0
            
            # Check for javascript URI scheme
            features['has_javascript_uri'] = 1 if url.startswith('javascript:') else 0
            
            # Check for empty or invalid hostname
            features['has_empty_hostname'] = 1 if not domain or domain.startswith('.') else 0
            
            # Check for port number
            features['has_port_number'] = 1 if ':' in domain else 0
            
            # Check for IP address
            features['has_ip_address'] = 1 if re.match(r'\d+\.\d+\.\d+\.\d+', domain) else 0
            
            # Check for random-looking strings
            features['has_random_strings'] = 1 if any(len(part) >= 6 and re.match(r'^[a-zA-Z0-9]+$', part) and 
                                                    not any(brand in part.lower() for brand in self.brand_names)
                                                    for part in re.split(r'[/._-]', url)) else 0
            
            # Check for excessive query parameters
            features['has_complex_query'] = 1 if len(query) > 20 or query.count('=') > 2 else 0
            
            # Check for hexadecimal or base64-like strings
            features['has_encoded_strings'] = 1 if re.search(r'[a-fA-F0-9]{16,}|[A-Za-z0-9+/]{20,}=*', url) else 0
            
            # Check for short domain segments
            features['has_short_domain'] = 1 if any(len(segment) <= 3 for segment in domain.split('.')[:-1]) else 0
            
            return features
            
        except Exception as e:
            print(f"Error extracting features: {str(e)}")
            return {}
    
    def extract_domain_features(self, url):
        """Extract domain-based features"""
        features = {}
        parsed = urlparse(url)
        domain = parsed.netloc
        
        try:
            # Domain age and registration
            w = whois.whois(domain)
            features['domain_age'] = 1 if w.creation_date else 0
            features['domain_registered'] = 1 if w.registrar else 0
        except:
            features['domain_age'] = 0
            features['domain_registered'] = 0
        
        try:
            # SSL certificate check
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    features['has_valid_ssl'] = 1
        except:
            features['has_valid_ssl'] = 0
            
        return features
    
    def extract_content_features(self, html_content):
        """Extract features from webpage content"""
        features = {}
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Form analysis
        forms = soup.find_all('form')
        features['num_forms'] = len(forms)
        features['has_password_field'] = int(bool(soup.find('input', {'type': 'password'})))
        features['num_input_fields'] = len(soup.find_all('input'))
        
        # Link analysis
        links = soup.find_all('a')
        external_links = 0
        for link in links:
            href = link.get('href', '')
            if href.startswith('http') and urlparse(url).netloc not in href:
                external_links += 1
        features['num_external_links'] = external_links
        
        # Script analysis
        features['num_scripts'] = len(soup.find_all('script'))
        
        # iFrame presence
        features['has_iframe'] = int(bool(soup.find('iframe')))
        
        return features 