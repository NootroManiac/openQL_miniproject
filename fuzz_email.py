from pythonfuzz.main import PythonFuzz
from detectors.email_detector import EmailDetector
detector = EmailDetector()

@PythonFuzz
def fuzz_email(buf):
    try:
        # Convert bytes to string
        string = buf.decode('utf-8')
        # Create email data dictionary
        email_data = {
            "subject": string[:50],  # Use first 50 chars as subject
            "body": string,          # Use full string as body
            "sender": "test@example.com"  # Default sender
        }
        result = detector.analyze(email_data)

    except UnicodeDecodeError:
        pass
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    print("Starting email fuzzing...")
    fuzz_email() 