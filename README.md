# AI Threat Detection System

A comprehensive system for detecting AI-generated threats including deepfakes, voice impersonation, and phishing emails.

## Features

- Email Phishing Detection
  - Pattern matching for common phishing indicators
  - Sentiment analysis for detecting AI-generated content
  - Text classification for phishing detection

- Voice Impersonation Detection
  - Audio analysis using Wav2Vec2 model
  - Feature extraction and classification
  - Support for various audio formats

- Video Deepfake Detection
  - Frame-by-frame analysis
  - Deep learning-based classification
  - Support for various video formats

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-threat-detection
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python main.py
```

2. The API will be available at `http://localhost:8000`

3. API Endpoints:

   - Email Detection:
     ```
     POST /detect/email
     Content-Type: application/json
     
     {
         "subject": "email subject",
         "body": "email body",
         "sender": "sender@example.com",
         "attachments": []
     }
     ```

   - Voice Detection:
     ```
     POST /detect/voice
     Content-Type: multipart/form-data
     
     audio_file: <audio file>
     ```

   - Video Detection:
     ```
     POST /detect/video
     Content-Type: multipart/form-data
     
     video_file: <video file>
     ```

## API Documentation

Once the server is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Response Format

All endpoints return a JSON response in the following format:

```json
{
    "is_threat": boolean,
    "confidence": float,
    "threat_type": string,
    "details": {
        // Additional details specific to each detection type
    }
}
```

## Requirements

- Python 3.8+
- CUDA-capable GPU (recommended for better performance)
- See requirements.txt for Python package dependencies

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 