from transformers import pipeline
import re
from typing import Dict, Any

class EmailDetector:
    def __init__(self):
        # Initialize the sentiment analysis pipeline for detecting AI-generated content
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        # Initialize the text classification pipeline for phishing detection using a different model
        self.text_classifier = pipeline("text-classification", model="distilbert-base-uncased")
        
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
        
        # Analyze sentiment and detect potential AI generation
        sentiment_result = self.sentiment_analyzer(full_text)
        
        # Classify text for phishing detection
        classification_result = self.text_classifier(full_text)
        
        # Calculate threat score based on multiple factors
        threat_score = 0.0
        
        # Pattern matching weight
        if pattern_matches:
            threat_score += 0.3 * len(pattern_matches) / len(self.phishing_patterns)
        
        # Sentiment analysis weight
        if sentiment_result[0]['label'] == 'POSITIVE' and sentiment_result[0]['score'] > 0.8:
            threat_score += 0.2  # High positive sentiment might indicate AI generation
        
        # Text classification weight
        if classification_result[0]['label'] == 'LABEL_1':  # Assuming LABEL_1 is phishing
            threat_score += 0.5 * classification_result[0]['score']
        
        # Determine if it's a threat
        is_threat = threat_score > 0.5
        
        return {
            "is_threat": is_threat,
            "confidence": threat_score,
            "threat_type": "phishing" if is_threat else "legitimate",
            "details": {
                "pattern_matches": pattern_matches,
                "sentiment_analysis": sentiment_result[0],
                "text_classification": classification_result[0],
                "sender": email_data['sender']
            }
        } 