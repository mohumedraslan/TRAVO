"""
New monument detection service logic using the improved MonumentDetector model.
This replaces the old CLIP-based implementation with a more robust architecture.
"""

import os
import logging
from typing import Dict, Optional
from pathlib import Path

# Add backend directory to path for imports
backend_dir = Path(__file__).parent.parent.parent
import sys
sys.path.insert(0, str(backend_dir))

from models.monuments.model import MonumentDetector

logger = logging.getLogger(__name__)

class MonumentDetectionService:
    """Service class for monument detection operations"""
    
    def __init__(self):
        self.detector = MonumentDetector()
        self.initialized = False
        
    def initialize(self) -> bool:
        """Initialize the monument detection service"""
        try:
            logger.info("Initializing monument detection service...")
            
            # Get the vision service directory
            service_dir = Path(__file__).parent
            
            # Load model
            self.detector.load_model()
            
            # Load labels
            labels_path = service_dir / "labels.json"
            if not labels_path.exists():
                logger.error(f"Labels file not found: {labels_path}")
                return False
                
            self.detector.load_labels(str(labels_path))
            
            # Load embeddings
            embeddings_path = backend_dir / "models" / "monuments" / "embeddings.pkl"
            if embeddings_path.exists():
                logger.info(f"Loading pre-computed embeddings from {embeddings_path}")
                self.detector.load_embeddings(str(embeddings_path))
            else:
                logger.info("Computing embeddings...")
                self.detector.compute_embeddings(str(embeddings_path))
            
            self.initialized = True
            logger.info("Monument detection service initialized successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize monument detection service: {e}", exc_info=True)
            return False
    
    def identify_monument(self, image_bytes: bytes) -> Dict:
        """Identify monument from image bytes"""
        if not self.initialized:
            return {
                "identified_monument": None,
                "confidence": 0.0,
                "monument_id": None,
                "message": "Service not initialized"
            }
        
        try:
            result = self.detector.identify_monument(image_bytes)
            return result
            
        except Exception as e:
            logger.error(f"Error identifying monument: {e}", exc_info=True)
            return {
                "identified_monument": None,
                "confidence": 0.0,
                "monument_id": None,
                "message": f"Error during identification: {str(e)}"
            }
    
    def get_monument_info(self, monument_id: str) -> Optional[Dict]:
        """Get detailed information about a monument"""
        if not self.initialized:
            return None
            
        try:
            return self.detector.get_monument_info(monument_id)
        except Exception as e:
            logger.error(f"Error getting monument info: {e}")
            return None
    
    def get_top_matches(self, image_bytes: bytes, top_k: int = 3) -> list:
        """Get top K matches for an image"""
        if not self.initialized:
            return []
            
        try:
            return self.detector.get_top_matches(image_bytes, top_k)
        except Exception as e:
            logger.error(f"Error getting top matches: {e}")
            return []

# Global service instance
monument_service = MonumentDetectionService()

# Initialize the service
service_initialized = monument_service.initialize()

# Legacy function for backward compatibility
def identify_monument(image_bytes: bytes) -> Dict:
    """Legacy function for monument identification"""
    return monument_service.identify_monument(image_bytes)

def get_monument_details_by_name(monument_name: str) -> Optional[Dict]:
    """Get monument details by name"""
    if not service_initialized:
        return None
        
    # Find monument by name in the detector's labels
    for monument in monument_service.detector.monuments:
        if monument["name"] == monument_name:
            return {
                "monument_id": monument["id"],
                "name": monument["name"],
                "description": monument["description"],
                "location": {
                    "latitude": monument.get("latitude", 0.0),
                    "longitude": monument.get("longitude", 0.0)
                },
                "country": monument.get("country", "Unknown"),
                "city": monument.get("city", "Unknown")
            }
    return None