
# ai-security-mini-project
# AI Threat Detection System
Coded using LLM's.

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

  Fuzzing is supported with the email phishing dectection function
  

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-threat-detection
```

2. Install dependencies:
```bash
pip install -r requirements.txt
#you may want to install requirements after making a virtual environment by following the instructions on the fuzzer installation instructions below
```
## Fuzzing 

1) Follow install steps

Download Python 3.9.18 

Install Python 3.9.18 using pyenv
```bash 
sudo apt update && sudo apt install -y build-essential curl git libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncursesw5-dev xz-utils tk-dev \
  libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```


Install pyenv
```bash
curl https://pyenv.run | bash
```
Add it to your bash/terminal
```bash
nano ~/.bashrc # or use ~/.zshrc
# put this at the end of the script/settings
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)" 
```

Reload your shell
```bash 
exec "$SHELL"
```
Install python versions
```bash 
pyenv install 3.9.18
pyenv install 3.12.2
```
Set local python verion to 3.9.18
```bash
pyenv local 3.9.18
```
Make virtual environment
```bash
python3 -m venv myenv
```
Activate virtual environment
```bash
source myenv/bin/activate
#when your done you can just type deactivate in the terminal
```
Download requirements
```bash 
pip install -r requirements.txt

```
Download atheris
```bash
pip3 install atheris
```
Run fuzzing script located at test_files.py

(optional)Download coverage
```bash
python3 -m pip install coverage

#run the script by running 
python3 -m coverage run test_files.py -atheris_runs=100
```

## Usage

1. Start the server:
```bash
python main.py
```

2. The API will be available at `http://localhost:8000`
3. Run the test_detectors.py file in a different terminal and modify the requests. Alternatively, go and send your own JSON requests.
3. Add .wav and .mov files to the test files folder and rename your files to the correct keywords. Alternatively, go and send your own JSON requests. (it works without files as well)
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
Additionally, the responses are saved into a JSON file and printed into the terminal.
## Requirements

- Python 3.8+
- CUDA-capable GPU (recommended for better performance)
- See requirements.txt for Python package dependencies

## License

MIT License

