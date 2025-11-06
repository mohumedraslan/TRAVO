#!/usr/bin/env python3
"""
Test the monument detection model with a real image file.
"""

import sys
import os
from pathlib import Path
import logging
import requests
from PIL import Image
import io

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from models.monuments.model import MonumentDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_test_image():
    """Download a test image of a monument"""
    try:
        # Use a simple placeholder image
        url = "https://via.placeholder.com/224x224/0066cc/ffffff?text=Monument+Test"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception as e:
        logger.warning(f"Failed to download image: {e}")
        # Create a simple colored image
        img = Image.new('RGB', (224, 224), color=(0, 102, 204))
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        return img_buffer.getvalue()

def main():
    """Test the monument detector"""
    try:
        # Initialize detector
        logger.info("Initializing monument detector...")
        detector = MonumentDetector()
        
        # Load model
        logger.info("Loading CLIP model...")
        detector.load_model()
        
        # Load labels
        labels_path = Path(__file__).parent / "labels.json"
        logger.info(f"Loading labels from {labels_path}")
        detector.load_labels(str(labels_path))
        
        # Load embeddings
        embeddings_path = Path(__file__).parent / "embeddings.pkl"
        if embeddings_path.exists():
            logger.info(f"Loading embeddings from {embeddings_path}")
            detector.load_embeddings(str(embeddings_path))
        else:
            logger.info("Computing embeddings...")
            detector.compute_embeddings(str(embeddings_path))
        
        # Test with sample image
        logger.info("Getting test image...")
        test_image = download_test_image()
        
        logger.info("Testing monument identification...")
        result = detector.identify_monument(test_image)
        
        logger.info(f"Test result: {result}")
        
        # Show top 3 matches
        logger.info("\nTesting top 3 matches...")
        top_matches = detector.get_top_matches(test_image, top_k=3)
        for i, match in enumerate(top_matches):
            logger.info(f"{i+1}. {match['name']} (confidence: {match['confidence']:.3f})")
        
        logger.info("\nModel test completed successfully!")
        
    except Exception as e:
        logger.error(f"Failed to test monument detector: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()