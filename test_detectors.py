import requests
import json
import os
from datetime import datetime

def test_email_detector():
    print("\n=== Testing Email Detector ===")
    
    test_cases = [
        {
            "name": "Obvious Phishing Email",
            "data": {
                "subject": "URGENT: Account Suspended - Verify Now",
                "body": "Dear user, your account has been suspended. Click here to verify your identity and update your information immediately.",
                "sender": "security@fakebank.com",
                "attachments": []
            }
        },
        {
            "name": "Legitimate Email",
            "data": {
                "subject": "Welcome to Our Newsletter",
                "body": "Thank you for subscribing to our monthly newsletter. Here are the latest updates from our team.",
                "sender": "newsletter@company.com",
                "attachments": []
            }
        },
        {
            "name": "Sophisticated Phishing Attempt",
            "data": {
                "subject": "Important: Security Update Required",
                "body": "We've detected unusual activity in your account. Please verify your identity by confirming your details through our secure portal.",
                "sender": "support@securityteam.net",
                "attachments": []
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        try:
            response = requests.post(
                "http://127.0.0.1:8000/detect/email",
                json=test_case['data']
            )
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"Error: {str(e)}")

def test_voice_detector():
    print("\n=== Testing Voice Detector ===")
    
    # Test cases with different audio files
    test_files = [
        "test_files/human_voice.wav",
        "test_files/ai_generated_voice.wav",
        "test_files/mixed_voice.wav"
    ]
    
    for file_path in test_files:
        print(f"\nTesting file: {file_path}")
        try:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    response = requests.post(
                        "http://127.0.0.1:8000/detect/voice",
                        files={"audio_file": f}
                    )
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            else:
                print(f"Test file not found: {file_path}")
        except Exception as e:
            print(f"Error: {str(e)}")

def test_video_detector():
    print("\n=== Testing Video Detector ===")
    
    # Test cases with different video files
    test_files = [
        "test_files/real_video.mp4",
        "test_files/deepfake_video.mp4",
        "test_files/mixed_video.mp4"
    ]
    
    for file_path in test_files:
        print(f"\nTesting file: {file_path}")
        try:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    response = requests.post(
                        "http://127.0.0.1:8000/detect/video",
                        files={"video_file": f}
                    )
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            else:
                print(f"Test file not found: {file_path}")
        except Exception as e:
            print(f"Error: {str(e)}")

def save_test_results(results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nTest results saved to: {filename}")

if __name__ == "__main__":
    print("Starting detector tests...")
    
    # Create test_files directory if it doesn't exist
    os.makedirs("test_files", exist_ok=True)
    
    # Run tests
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "results": {}
    }
    
    try:
        # Test email detector
        test_email_detector()
        
        # Note about voice and video tests
        print("\nNote: Voice and video tests require test files.")
        print("Please place test files in the 'test_files' directory with appropriate names.")
        
        # Test voice detector
        test_voice_detector()
        
        # Test video detector
        test_video_detector()
        
    except Exception as e:
        print(f"\nError during testing: {str(e)}")
    
    print("\nTests completed.") 