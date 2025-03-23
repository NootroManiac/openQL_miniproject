from detectors.email_detector import EmailDetector
import random
import string
import time

def generate_random_string(length):
    """Generate a random string of fixed length"""
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def inject_pattern(text, pattern):
    """Inject a pattern at a random position in the text"""
    position = random.randint(0, len(text))
    return text[:position] + pattern + text[position:]

def run_fuzzing():
    """Run email fuzzing"""
    print("Starting email fuzzing...")
    
    detector = EmailDetector()
    iterations = 0
    threats_found = 0
    start_time = time.time()
    
    try:
        while True:
            # Generate random strings for subject and body
            subject_length = random.randint(10, 100)
            body_length = random.randint(50, 1000)
            
            subject = generate_random_string(subject_length)
            body = generate_random_string(body_length)
            
            # Sometimes inject known phishing patterns
            if random.random() < 0.3:  # 30% chance to increase likelihood of finding threats
                patterns = [
                    "urgent action required", 
                    "verify your account", 
                    "account suspended",
                    "security alert",
                    "password expired",
                    "confirm your details",
                    "click here to confirm"
                ]
                pattern = random.choice(patterns)
                if random.random() < 0.5:
                    subject = inject_pattern(subject, pattern)
                else:
                    body = inject_pattern(body, pattern)
            
            # Create email data
            email_data = {
                "subject": subject,
                "body": body,
                "sender": "test@example.com"
            }
            
            # Analyze email
            result = detector.analyze(email_data)
            iterations += 1
            
            if result["is_threat"]:
                threats_found += 1
                print(f"\nFound threat! #{threats_found}")
                print(f"Subject: {subject[:50]}...")
                print(f"Confidence: {result['confidence']:.2f}")
                print(f"Patterns: {result['details']['pattern_matches']}")
            
            # Print status every 1000 iterations
            if iterations % 1000 == 0:
                elapsed = time.time() - start_time
                print(f"\nCompleted {iterations} iterations in {elapsed:.2f} seconds")
                print(f"Threats found: {threats_found}")
                print(f"Rate: {iterations/elapsed:.2f} iterations/second")
    
    except KeyboardInterrupt:
        print("\nFuzzing stopped by user")
        elapsed = time.time() - start_time
        print(f"\nFuzzing summary:")
        print(f"Total iterations: {iterations}")
        print(f"Total threats found: {threats_found}")
        print(f"Run time: {elapsed:.2f} seconds")
        print(f"Average rate: {iterations/elapsed:.2f} iterations/second")

if __name__ == "__main__":
    run_fuzzing() 