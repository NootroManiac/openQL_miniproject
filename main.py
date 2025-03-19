from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from typing import Optional
import os
from dotenv import load_dotenv

# Import our detection modules
from detectors.email_detector import EmailDetector
from detectors.voice_detector import VoiceDetector
from detectors.video_detector import VideoDetector

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Threat Detection System",
    description="A comprehensive system for detecting AI-generated threats including deepfakes and phishing",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize detectors
email_detector = EmailDetector()
voice_detector = VoiceDetector()
video_detector = VideoDetector()

class EmailRequest(BaseModel):
    subject: str
    body: str
    sender: str
    attachments: Optional[list] = []

class DetectionResponse(BaseModel):
    is_threat: bool
    confidence: float
    threat_type: str
    details: dict

@app.post("/detect/email", response_model=DetectionResponse)
async def detect_email_threat(email: EmailRequest):
    """
    Detect AI-generated phishing emails
    """
    try:
        result = email_detector.analyze(email.dict())
        return DetectionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/detect/voice", response_model=DetectionResponse)
async def detect_voice_threat(audio_file: UploadFile = File(...)):
    """
    Detect AI-generated voice impersonation
    """
    try:
        # Save the uploaded file temporarily
        temp_path = f"temp_{audio_file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await audio_file.read()
            buffer.write(content)
        
        result = voice_detector.analyze(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        return DetectionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/detect/video", response_model=DetectionResponse)
async def detect_video_threat(video_file: UploadFile = File(...)):
    """
    Detect AI-generated video deepfakes
    """
    try:
        # Save the uploaded file temporarily
        temp_path = f"temp_{video_file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await video_file.read()
            buffer.write(content)
        
        result = video_detector.analyze(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        return DetectionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
