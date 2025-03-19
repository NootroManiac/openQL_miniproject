import cv2
import numpy as np
from typing import Dict, Any
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import os

class VideoDetector:
    def __init__(self):
        # Initialize the image classification model for deepfake detection
        self.processor = AutoImageProcessor.from_pretrained("microsoft/resnet-50")
        self.model = AutoModelForImageClassification.from_pretrained("microsoft/resnet-50")
        
        # Video processing parameters
        self.frame_interval = 30  # Process every 30th frame
        self.min_frames = 10  # Minimum number of frames to analyze
        self.max_frames = 100  # Maximum number of frames to analyze
        
    def extract_frames(self, video_path: str) -> list:
        """
        Extract frames from the video file
        
        Args:
            video_path: Path to the video file
            
        Returns:
            List of frames as PIL Images
        """
        frames = []
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise Exception("Error opening video file")
        
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            if frame_count % self.frame_interval == 0:
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Convert to PIL Image
                pil_image = Image.fromarray(frame_rgb)
                frames.append(pil_image)
                
            frame_count += 1
            
            if len(frames) >= self.max_frames:
                break
        
        cap.release()
        
        if len(frames) < self.min_frames:
            raise Exception(f"Video too short. Need at least {self.min_frames} frames.")
            
        return frames
    
    def analyze_frame(self, frame: Image.Image) -> Dict[str, float]:
        """
        Analyze a single frame for deepfake detection
        
        Args:
            frame: PIL Image to analyze
            
        Returns:
            Dictionary containing confidence scores
        """
        # Preprocess the image
        inputs = self.processor(images=frame, return_tensors="pt")
        
        # Get model predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        return {
            "real": float(predictions[0][0]),
            "fake": float(predictions[0][1])
        }
    
    def analyze(self, video_path: str) -> Dict[str, Any]:
        """
        Analyze a video file for potential deepfakes
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Dictionary containing detection results
        """
        try:
            # Extract frames
            frames = self.extract_frames(video_path)
            
            # Analyze each frame
            frame_results = []
            for frame in frames:
                result = self.analyze_frame(frame)
                frame_results.append(result)
            
            # Calculate average confidence scores
            avg_real = np.mean([r["real"] for r in frame_results])
            avg_fake = np.mean([r["fake"] for r in frame_results])
            
            # Determine if it's a deepfake
            is_threat = avg_fake > 0.5
            
            return {
                "is_threat": is_threat,
                "confidence": float(avg_fake),
                "threat_type": "deepfake" if is_threat else "real",
                "details": {
                    "num_frames_analyzed": len(frames),
                    "confidence_scores": {
                        "real": float(avg_real),
                        "fake": float(avg_fake)
                    },
                    "frame_results": frame_results
                }
            }
            
        except Exception as e:
            raise Exception(f"Error analyzing video file: {str(e)}") 