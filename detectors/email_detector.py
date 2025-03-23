import re
from typing import Dict, Any

class EmailDetector:
    def __init__(self):
        # Common phishing patterns
        self.phishing_patterns = [
            r'urgent action required',
            r'account suspended',
            r'verify your account',
            r'click here to confirm',
            r'password expired',
            r'security alert',
            r'verify your identity',
            r'account compromised',
            r'confirm your details',
            r'update your information'
        ]
        
    def analyze(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze an email for potential AI-generated phishing threats
        
        Args:
            email_data: Dictionary containing email subject, body, and sender
            
        Returns:
            Dictionary containing detection results
        """
        # Combine subject and body for analysis
        full_text = f"{email_data['subject']} {email_data['body']}"
        
        # Check for phishing patterns
        pattern_matches = []
        for pattern in self.phishing_patterns:
            if re.search(pattern, full_text.lower()):
                pattern_matches.append(pattern)
        
        # Calculate threat score based on pattern matches
        threat_score = 0.0
        if pattern_matches:
            threat_score = len(pattern_matches) / len(self.phishing_patterns)
        
        # Determine if it's a threat
        is_threat = threat_score > 0.5
        
        return {
            "is_threat": is_threat,
            "confidence": threat_score,
            "threat_type": "phishing" if is_threat else "legitimate",
            "details": {
                "pattern_matches": pattern_matches,
                "sender": email_data['sender']
            }
        }
