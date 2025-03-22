from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from typing import Optional
import os
<<<<<<< HEAD
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import detectors
=======
from dotenv import load_dotenv

# Import our detection modules
>>>>>>> 21b402bb860a5f49bd0d560b67f3922910a37724
from detectors.email_detector import EmailDetector
from detectors.voice_detector import VoiceDetector
from detectors.video_detector import VideoDetector

<<<<<<< HEAD
# Initialize detectors
email_detector = EmailDetector()
voice_detector = VoiceDetector()
video_detector = VideoDetector()

# Create FastAPI app
app = FastAPI(
    title="AI Threat Detection System",
    description="A comprehensive system for detecting AI-generated threats",
=======
# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Threat Detection System",
    description="A comprehensive system for detecting AI-generated threats including deepfakes and phishing",
>>>>>>> 21b402bb860a5f49bd0d560b67f3922910a37724
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

<<<<<<< HEAD
=======
# Initialize detectors
email_detector = EmailDetector()
voice_detector = VoiceDetector()
video_detector = VideoDetector()

>>>>>>> 21b402bb860a5f49bd0d560b67f3922910a37724
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

<<<<<<< HEAD
@app.get("/")
async def root():
    """
    Root endpoint to check if the server is running
    """
    return {"status": "ok", "message": "AI Threat Detection System is running"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

=======
>>>>>>> 21b402bb860a5f49bd0d560b67f3922910a37724
@app.post("/detect/email", response_model=DetectionResponse)
async def detect_email_threat(email: EmailRequest):
    """
    Detect AI-generated phishing emails
    """
    try:
        result = email_detector.analyze(email.dict())
        return DetectionResponse(**result)
    except Exception as e:
<<<<<<< HEAD
        logger.error(f"Error in email detection: {str(e)}")
=======
>>>>>>> 21b402bb860a5f49bd0d560b67f3922910a37724
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
<<<<<<< HEAD
        logger.error(f"Error in voice detection: {str(e)}")
=======
>>>>>>> 21b402bb860a5f49bd0d560b67f3922910a37724
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
<<<<<<< HEAD
        logger.error(f"Error in video detection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    try:
        print("\n" + "="*50)
        print("Starting AI Threat Detection System...")
        print("Server will be available at: http://127.0.0.1:8000")
        print("API Documentation at: http://127.0.0.1:8000/docs")
        print("Health check at: http://127.0.0.1:8000/health")
        print("="*50 + "\n")
        
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Make sure port 8000 is not in use")
        print("2. Try running with administrator privileges")
        print("3. Check your firewall settings")
        print("4. Try using 'localhost' instead of '127.0.0.1'")
=======
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
>>>>>>> 21b402bb860a5f49bd0d560b67f3922910a37724
