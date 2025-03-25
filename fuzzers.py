from pythonfuzz.main import PythonFuzz
from detectors.email_detector import EmailDetector

@PythonFuzz
def fuzz_email_detector(buf):
    fuzzer = EmailDetector()

    try:
        string = buf.decode("ascii")
        email_data = {
            "subject": string[:12],  
            "body": string,         
            "sender": "test@example.com"  
        }
        fuzzer.analyze(email_data)
    except UnicodeDecodeError:
        print("UnicodeDecodeError")
        pass


if __name__ == '__main__':
    print("Starting email fuzzing...")
    fuzz_email_detector() 