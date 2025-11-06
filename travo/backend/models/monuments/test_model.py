#!/usr/bin/env python3
"""
Test the monument detection model with a sample image.
"""

import sys
import os
from pathlib import Path
import numpy as np
import logging

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from models.monuments.model import MonumentDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_image():
    """Create a simple test image (3x3 RGB)"""
    # Create a simple test image - random noise
    image_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    return image_array.tobytes()

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
        logger.info("Testing with sample image...")
        test_image = create_test_image()
        result = detector.identify_monument(test_image)
        
        logger.info(f"Test result: {result}")
        
        # Test with different confidence thresholds
        logger.info("\nTesting with different confidence thresholds:")
        for threshold in [0.5, 0.7, 0.9]:
            detector.confidence_threshold = threshold
            result = detector.identify_monument(test_image)
            logger.info(f"Threshold {threshold}: {result['identified_monument'] or 'None'}")
        
        logger.info("\nModel test completed successfully!")
        
    except Exception as e:
        logger.error(f"Failed to test monument detector: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()