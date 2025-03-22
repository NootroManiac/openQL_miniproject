import requests
import json
from datetime import datetime
import os
from colorama import init, Fore, Style

# Initialize colorama for Windows support
init()

def print_result(result, detector_type):
    print(f"\n{Fore.CYAN}=== {detector_type.upper()} DETECTION RESULT ==={Style.RESET_ALL}")
    
    # Print threat status with color
    threat_status = "THREAT DETECTED" if result.get("is_threat", False) else "NO THREAT DETECTED"
    color = Fore.RED if result.get("is_threat", False) else Fore.GREEN
    print(f"\n{color}Status: {threat_status}{Style.RESET_ALL}")
    
    # Print confidence score
    confidence = result.get("confidence", 0) * 100
    print(f"{Fore.YELLOW}Confidence: {confidence:.2f}%{Style.RESET_ALL}")
    
    # Print threat type
    threat_type = result.get("threat_type", "unknown")
    print(f"{Fore.YELLOW}Threat Type: {threat_type}{Style.RESET_ALL}")
    
    # Print detailed analysis
    print(f"\n{Fore.CYAN}Detailed Analysis:{Style.RESET_ALL}")
    details = result.get("details", {})
    
    if detector_type == "email":
        # Email specific details
        pattern_matches = details.get("pattern_matches", [])
        if pattern_matches:
            print(f"\n{Fore.YELLOW}Suspicious Patterns Found:{Style.RESET_ALL}")
            for pattern in pattern_matches:
                print(f"- {pattern}")
        
        sentiment = details.get("sentiment_analysis", {})
        if sentiment:
            print(f"\n{Fore.YELLOW}Sentiment Analysis:{Style.RESET_ALL}")
            print(f"Label: {sentiment.get('label', 'N/A')}")
            print(f"Score: {sentiment.get('score', 0):.2f}")
    
    elif detector_type == "voice":
        # Voice specific details
        audio_features = details.get("audio_features", {})
        if audio_features:
            print(f"\n{Fore.YELLOW}Audio Features:{Style.RESET_ALL}")
            for key, value in audio_features.items():
                print(f"{key}: {value}")
    
    elif detector_type == "video":
        # Video specific details
        video_features = details.get("video_features", {})
        if video_features:
            print(f"\n{Fore.YELLOW}Video Features:{Style.RESET_ALL}")
            for key, value in video_features.items():
                print(f"{key}: {value}")
    
    print("\n" + "="*50)

def save_detection_result(result, detector_type):
    # Create timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"detection_results_{detector_type}_{timestamp}.json"
    
    # Save results to file
    with open(filename, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"{Fore.GREEN}Results saved to {filename}{Style.RESET_ALL}")

def test_email_detection():
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
        result = response.json()
        print_result(result, "email")
        save_detection_result(result, "email")
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

def test_voice_detection():
    try:
        with open("test_files/human_voice.wav", "rb") as f:
            response = requests.post(
                "http://127.0.0.1:8000/detect/voice",
                files={"audio_file": f}
            )
        result = response.json()
        print_result(result, "voice")
        save_detection_result(result, "voice")
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

def test_video_detection():
    try:
        with open("test_files/real_video.mp4", "rb") as f:
            response = requests.post(
                "http://127.0.0.1:8000/detect/video",
                files={"video_file": f}
            )
        result = response.json()
        print_result(result, "video")
        save_detection_result(result, "video")
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    print(f"{Fore.CYAN}=== AI Threat Detection System ==={Style.RESET_ALL}")
    
    # Test email detection
    test_email_detection()
    
    # Test voice detection (requires test file)
    print(f"\n{Fore.YELLOW}Note: Voice detection requires test files in the test_files directory{Style.RESET_ALL}")
    test_voice_detection()
    
    # Test video detection (requires test file)
    print(f"\n{Fore.YELLOW}Note: Video detection requires test files in the test_files directory{Style.RESET_ALL}")
    test_video_detection() 