import requests
import json

def test_email_detection():
    # Example phishing email
    email_data = {
        "subject": "URGENT: Account Security Alert",
        "body": "Dear user, we've detected unusual activity in your account. Please verify your identity immediately.",
        "sender": "security@example.com",
        "attachments": []
    }
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/detect/email",
            json=email_data
        )
        print("Email Detection Result:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")

def test_voice_detection():
    # Example voice file test
    try:
        with open("test_files/human_voice.wav", "rb") as f:
            response = requests.post(
                "http://127.0.0.1:8000/detect/voice",
                files={"audio_file": f}
            )
        print("\nVoice Detection Result:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")

def test_video_detection():
    # Example video file test
    try:
        with open("test_files/real_video.mp4", "rb") as f:
            response = requests.post(
                "http://127.0.0.1:8000/detect/video",
                files={"video_file": f}
            )
        print("\nVideo Detection Result:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Testing AI Threat Detection System...")
    
    # Test email detection
    test_email_detection()
    
    # Test voice detection (requires test file)
    print("\nNote: Voice detection requires test files in the test_files directory")
    test_voice_detection()
    
    # Test video detection (requires test file)
    print("\nNote: Video detection requires test files in the test_files directory")
    test_video_detection() 