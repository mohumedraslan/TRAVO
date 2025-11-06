#!/usr/bin/env python3
"""
Initialize the monument detection model by computing embeddings for all monuments.
This script should be run once to create the embeddings file.
"""

import os
import sys
import logging
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from models.monuments.model import MonumentDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Initialize the monument detector and compute embeddings"""
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
        
        # Compute embeddings
        embeddings_path = Path(__file__).parent / "embeddings.pkl"
        logger.info(f"Computing embeddings and saving to {embeddings_path}")
        detector.compute_embeddings(str(embeddings_path))
        
        logger.info("Monument detector initialization completed successfully!")
        logger.info(f"Embeddings saved to: {embeddings_path}")
        
        # Test the detector
        logger.info("Testing detector with a sample query...")
        test_result = detector.identify_monument(b'')  # Empty image for testing
        logger.info(f"Test result: {test_result}")
        
    except Exception as e:
        logger.error(f"Failed to initialize monument detector: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()