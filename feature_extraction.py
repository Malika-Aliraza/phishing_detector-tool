import re
from urllib.parse import urlparse

def extract_features(url):
    """
    Extracts rule-based features from a URL for phishing detection.
    Returns a dictionary of features and a rule-based risk score.
    """
    features = {}
    
    # 1. URL Length
    features['url_length'] = len(url)
    
    # 2. Presence of HTTPS
    features['has_https'] = 1 if url.startswith('https') else 0
    
    # 3. Number of dots
    features['num_dots'] = url.count('.')
    
    # 4. Presence of special characters
    features['has_at_symbol'] = 1 if '@' in url else 0
    features['has_hyphen'] = 1 if '-' in url else 0
    features['has_underscore'] = 1 if '_' in url else 0
    
    # 5. Use of IP address instead of domain
    ip_pattern = r'(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
    features['is_ip_address'] = 1 if re.search(ip_pattern, url) else 0
    
    # 6. Suspicious keywords
    suspicious_keywords = ['login', 'verify', 'bank', 'secure', 'update', 'account', 'signin', 'ebayisapi', 'webscr']
    features['num_suspicious_keywords'] = sum(1 for word in suspicious_keywords if word in url.lower())
    
    # Calculate a simple rule-based risk score (0 to 1)
    # This is a heuristic approach for the hybrid system
    risk_score = 0
    if features['url_length'] > 75: risk_score += 0.2
    if not features['has_https']: risk_score += 0.3
    if features['num_dots'] > 3: risk_score += 0.2
    if features['has_at_symbol']: risk_score += 0.3
    if features['is_ip_address']: risk_score += 0.5
    if features['num_suspicious_keywords'] > 0: risk_score += 0.2 * features['num_suspicious_keywords']
    
    # Normalize risk score to be between 0 and 1
    features['rule_risk_score'] = min(1.0, risk_score)
    
    return features

def get_feature_list(url):
    """
    Returns features as a list of values in a specific order for the ML model.
    """
    f = extract_features(url)
    return [
        f['url_length'],
        f['has_https'],
        f['num_dots'],
        f['has_at_symbol'],
        f['has_hyphen'],
        f['has_underscore'],
        f['is_ip_address'],
        f['num_suspicious_keywords']
    ]
