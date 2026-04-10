import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import json
import pickle
import logging
import io
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import os

logger = logging.getLogger(__name__)

class MonumentDetector:
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = model_name
        self.model = None
        self.processor = None
        self.monument_embeddings = None
        self.monument_labels = []
        self.confidence_threshold = 0.45
        
    def load_model(self):
        """Load the CLIP model and processor"""
        try:
            logger.info(f"Loading CLIP model: {self.model_name}")
            self.model = CLIPModel.from_pretrained(self.model_name)
            self.processor = CLIPProcessor.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.model.eval()
            logger.info(f"CLIP model loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load CLIP model: {e}")
            raise
    
    def load_labels(self, labels_path: str):
        """Load monument labels from JSON file"""
        try:
            with open(labels_path, 'r') as f:
                labels_data = json.load(f)
            
            # Handle both formats: dict with 'monuments' key or direct array
            if isinstance(labels_data, dict):
                self.monument_labels = labels_data.get('monuments', [])
            elif isinstance(labels_data, list):
                # Convert list format to expected dict format
                self.monument_labels = [
                    {
                        'id': str(i+1),
                        'name': item.get('label', item.get('name', '')),
                        'description': item.get('description', '')
                    }
                    for i, item in enumerate(labels_data)
                ]
            else:
                raise ValueError("Invalid labels format")
            
            logger.info(f"Loaded {len(self.monument_labels)} monument labels")
        except Exception as e:
            logger.error(f"Failed to load labels: {e}")
            raise
    
    def load_embeddings(self, embeddings_path: str):
        """Load precomputed embeddings from pickle file"""
        try:
            if os.path.exists(embeddings_path):
                with open(embeddings_path, 'rb') as f:
                    self.monument_embeddings = pickle.load(f)
                logger.info(f"Loaded {len(self.monument_embeddings)} precomputed embeddings")
                return True
            else:
                logger.warning(f"Embeddings file not found: {embeddings_path}")
                return False
        except Exception as e:
            logger.error(f"Failed to load embeddings: {e}")
            return False
    
    def compute_embeddings(self, save_path: str = None):
        """Compute embeddings for all monument labels"""
        if not self.model or not self.processor:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        if not self.monument_labels:
            raise RuntimeError("No labels loaded. Call load_labels() first.")
        
        logger.info("Computing text embeddings for monuments...")
        embeddings = []
        
        with torch.no_grad():
            for monument in self.monument_labels:
                name = monument.get('name', '')
                description = monument.get('description', '')
                
                # Create a descriptive text for the monument
                text = f"a photo of {name}, {description}"
                
                inputs = self.processor(text=text, return_tensors="pt", padding=True, truncation=True)
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
                
                text_features = self.model.get_text_features(**inputs)
                text_features = F.normalize(text_features, dim=-1)
                
                embeddings.append(text_features.cpu().numpy())
        
        self.monument_embeddings = np.vstack(embeddings)
        logger.info(f"Computed embeddings for {len(embeddings)} monuments")
        
        # Save embeddings if path provided
        if save_path:
            self.save_embeddings(save_path)
    
    def save_embeddings(self, save_path: str):
        """Save computed embeddings to pickle file"""
        try:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as f:
                pickle.dump(self.monument_embeddings, f)
            logger.info(f"Saved embeddings to {save_path}")
        except Exception as e:
            logger.error(f"Failed to save embeddings: {e}")
            raise
    
    def preprocess_image(self, image_data: bytes) -> Image.Image:
        """Preprocess image data"""
        try:
            image = Image.open(io.BytesIO(image_data))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            return image
        except Exception as e:
            logger.error(f"Failed to preprocess image: {e}")
            raise
    
    def extract_image_features(self, image: Image.Image) -> np.ndarray:
        """Extract features from an image using CLIP"""
        if not self.model or not self.processor:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        with torch.no_grad():
            inputs = self.processor(images=image, return_tensors="pt", padding=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            image_features = self.model.get_image_features(**inputs)
            image_features = F.normalize(image_features, dim=-1)
            
            return image_features.cpu().numpy()
    
    def compute_similarity(self, image_features: np.ndarray) -> Tuple[float, int, str]:
        """Compute cosine similarity between image and monument embeddings"""
        if self.monument_embeddings is None:
            raise RuntimeError("No monument embeddings available")
        
        # Compute cosine similarity
        similarities = np.dot(image_features, self.monument_embeddings.T).flatten()
        
        # Get top match
        top_index = np.argmax(similarities)
        top_score = similarities[top_index]
        top_monument = self.monument_labels[top_index]
        
        return top_score, top_index, top_monument
    
    def identify_monument(self, image_data: bytes) -> Dict:
        """Identify monument in the given image"""
        try:
            # Preprocess image
            image = self.preprocess_image(image_data)
            
            # Extract image features
            image_features = self.extract_image_features(image)
            
            # Compute similarity with monument embeddings
            top_score, top_index, top_monument = self.compute_similarity(image_features)
            
            # Check confidence threshold
            if top_score < self.confidence_threshold:
                return {
                    "identified_monument": None,
                    "confidence": float(top_score),
                    "monument_id": None,
                    "message": "No confident match found"
                }
            
            # Return successful identification
            return {
                "identified_monument": top_monument.get('name', ''),
                "confidence": float(top_score),
                "monument_id": top_monument.get('id', ''),
                "monument_data": top_monument
            }
            
        except Exception as e:
            logger.error(f"Error identifying monument: {e}")
            return {
                "identified_monument": None,
                "confidence": 0.0,
                "monument_id": None,
                "message": f"Error during identification: {str(e)}"
            }
    
    def get_top_matches(self, image_data: bytes, top_k: int = 3) -> List[Dict]:
        """Get top K matches for an image"""
        try:
            if self.monument_embeddings is None:
                return []
            
            # Preprocess image
            image = self.preprocess_image(image_data)
            
            # Extract image features
            image_features = self.extract_image_features(image)
            
            # Compute similarities
            similarities = np.dot(image_features, self.monument_embeddings.T).flatten()
            
            # Get top K matches
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            top_scores = similarities[top_indices]
            
            results = []
            for idx, score in zip(top_indices, top_scores):
                monument = self.monument_labels[idx]
                results.append({
                    "name": monument.get('name', ''),
                    "confidence": float(score),
                    "id": monument.get('id', ''),
                    "description": monument.get('description', '')
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error getting top matches: {e}")
            return []
    
    def get_monument_info(self, monument_id: str) -> Optional[Dict]:
        """Get detailed information about a specific monument"""
        for monument in self.monument_labels:
            if monument.get('id') == monument_id:
                return monument
        return None

# Initialize the detector
monument_detector = MonumentDetector()

def initialize_detector(labels_path: str = None, embeddings_path: str = None):
    """Initialize the monument detector with model and data"""
    try:
        # Load model
        monument_detector.load_model()
        
        # Load labels
        if labels_path and os.path.exists(labels_path):
            monument_detector.load_labels(labels_path)
        else:
            # Use default labels if none provided
            default_labels = {
                "monuments": [
                    {"id": "1", "name": "Eiffel Tower", "description": "iconic iron tower in Paris, France"},
                    {"id": "2", "name": "Statue of Liberty", "description": "famous statue in New York, USA"},
                    {"id": "3", "name": "Colosseum", "description": "ancient amphitheater in Rome, Italy"},
                    {"id": "4", "name": "Great Wall of China", "description": "ancient fortification in China"},
                    {"id": "5", "name": "Machu Picchu", "description": "ancient Incan city in Peru"},
                    {"id": "6", "name": "Christ the Redeemer", "description": "famous statue in Rio de Janeiro, Brazil"},
                    {"id": "7", "name": "Taj Mahal", "description": "beautiful mausoleum in Agra, India"},
                    {"id": "8", "name": "Pyramids of Giza", "description": "ancient pyramids in Egypt"},
                    {"id": "9", "name": "Big Ben", "description": "famous clock tower in London, UK"},
                    {"id": "10", "name": "Sydney Opera House", "description": "iconic opera house in Sydney, Australia"}
                ]
            }
            monument_detector.monument_labels = default_labels["monuments"]
            logger.info("Using default monument labels")
        
        # Try to load existing embeddings
        if embeddings_path:
            loaded = monument_detector.load_embeddings(embeddings_path)
            if not loaded:
                # Compute embeddings if not found
                logger.info("Computing new embeddings...")
                monument_detector.compute_embeddings(embeddings_path)
        
        logger.info("Monument detector initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize monument detector: {e}")
        return False