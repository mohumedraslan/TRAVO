"""
Hugging Face ViT-based Landmark Recognition Model
Uses zhanglianghui/landmark-recognition-vit-base for monument detection
"""
import torch
from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image
import io
import base64
import logging
from typing import List, Dict, Tuple
import numpy as np

logger = logging.getLogger(__name__)

class LandmarkRecognitionModel:
    """Landmark recognition using Hugging Face ViT model"""
    
    def __init__(self, model_name: str = "google/vit-base-patch16-224"):
        """
        Initialize the landmark recognition model
        
        Args:
            model_name: Hugging Face model identifier
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Initializing landmark model on device: {self.device}")
        
        try:
            # Load feature extractor and model
            self.feature_extractor = AutoFeatureExtractor.from_pretrained(model_name)
            self.model = AutoModelForImageClassification.from_pretrained(model_name)
            self.model.to(self.device)
            self.model.eval()
            
            # Get label mapping
            self.id2label = self.model.config.id2label if hasattr(self.model.config, 'id2label') else {}
            
            logger.info(f"✅ Model loaded successfully: {model_name}")
            logger.info(f"Number of classes: {len(self.id2label)}")
            
        except Exception as e:
            logger.error(f"❌ Error loading model: {e}")
            raise
    
    def preprocess_image(self, image_data: str) -> Image.Image:
        """
        Preprocess base64 image data
        
        Args:
            image_data: Base64 encoded image string
            
        Returns:
            PIL Image object
        """
        try:
            # Decode base64
            image_bytes = base64.b64decode(image_data)
            
            # Open image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            return image
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            raise ValueError(f"Invalid image data: {e}")
    
    def predict(self, image_data: str, top_k: int = 3) -> List[Dict]:
        """
        Predict landmark from image
        
        Args:
            image_data: Base64 encoded image string
            top_k: Number of top predictions to return
            
        Returns:
            List of predictions with monument_name and confidence
        """
        try:
            # Preprocess image
            image = self.preprocess_image(image_data)
            
            # Extract features
            inputs = self.feature_extractor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Run inference
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
            
            # Get probabilities
            probs = torch.nn.functional.softmax(logits, dim=-1)
            
            # Get top-k predictions
            top_probs, top_indices = torch.topk(probs[0], k=min(top_k, len(probs[0])))
            
            # Format results
            predictions = []
            for prob, idx in zip(top_probs, top_indices):
                label = self.id2label.get(idx.item(), f"Class_{idx.item()}")
                predictions.append({
                    "monument_name": label,
                    "confidence": float(prob.item())
                })
            
            logger.info(f"Predictions: {predictions}")
            return predictions
            
        except Exception as e:
            logger.error(f"Error during prediction: {e}", exc_info=True)
            raise

# Global model instance
_model_instance = None

def get_model() -> LandmarkRecognitionModel:
    """Get or create global model instance"""
    global _model_instance
    if _model_instance is None:
        _model_instance = LandmarkRecognitionModel()
    return _model_instance

def predict_landmark(image_data: str, top_k: int = 3) -> Dict:
    """
    Predict landmark from base64 image data
    
    Args:
        image_data: Base64 encoded image string
        top_k: Number of top predictions to return
        
    Returns:
        Dictionary with prediction results
    """
    try:
        model = get_model()
        predictions = model.predict(image_data, top_k=top_k)
        
        if not predictions:
            return {
                "identified_monument": "Unknown",
                "confidence": 0.0,
                "monument_id": None,
                "candidates": []
            }
        
        # Format response
        top_prediction = predictions[0]
        return {
            "identified_monument": top_prediction["monument_name"],
            "confidence": top_prediction["confidence"],
            "monument_id": None,  # Can be mapped to database ID later
            "candidates": predictions
        }
        
    except Exception as e:
        logger.error(f"Error in predict_landmark: {e}")
        raise
