from detectors.email_detector import fuzz_email_detector
from pythonfuzz.main import PythonFuzz

if __name__ == "__main__":
    print("Starting fuzzing tests...")
    fuzz_email_detector() 