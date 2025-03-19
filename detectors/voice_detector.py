import librosa
import numpy as np
from typing import Dict, Any
import torch
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor

class VoiceDetector:
    def __init__(self):
        # Initialize the Wav2Vec2 model for audio classification
        self.model = Wav2Vec2ForSequenceClassification.from_pretrained("superb/wav2vec2-base-superb-sid")
        self.feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained("superb/wav2vec2-base-superb-sid")
        
        # Audio processing parameters
        self.sample_rate = 16000
        self.max_duration = 30  # seconds
        
    def preprocess_audio(self, audio_path: str) -> np.ndarray:
        """
        Preprocess the audio file for analysis
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Preprocessed audio array
        """
        # Load audio file
        audio, sr = librosa.load(audio_path, sr=self.sample_rate)
        
        # Trim to max duration if necessary
        if len(audio) > self.max_duration * sr:
            audio = audio[:self.max_duration * sr]
        
        # Normalize audio
        audio = librosa.util.normalize(audio)
        
        return audio
    
    def extract_features(self, audio: np.ndarray) -> torch.Tensor:
        """
        Extract features from the audio using Wav2Vec2
        
        Args:
            audio: Preprocessed audio array
            
        Returns:
            Feature tensor
        """
        inputs = self.feature_extractor(
            audio,
            sampling_rate=self.sample_rate,
            return_tensors="pt"
        )
        
        return inputs
    
    def analyze(self, audio_path: str) -> Dict[str, Any]:
        """
        Analyze an audio file for potential AI-generated voice
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Dictionary containing detection results
        """
        try:
            # Preprocess audio
            audio = self.preprocess_audio(audio_path)
            
            # Extract features
            inputs = self.extract_features(audio)
            
            # Get model predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Calculate confidence scores
            confidence = predictions[0].numpy()
            
            # Determine if it's AI-generated
            is_threat = confidence[1] > 0.5  # Assuming index 1 represents AI-generated
            
            return {
                "is_threat": is_threat,
                "confidence": float(confidence[1]),
                "threat_type": "ai_voice" if is_threat else "human_voice",
                "details": {
                    "audio_duration": len(audio) / self.sample_rate,
                    "confidence_scores": {
                        "human": float(confidence[0]),
                        "ai": float(confidence[1])
                    }
                }
            }
            
        except Exception as e:
            raise Exception(f"Error analyzing audio file: {str(e)}") 