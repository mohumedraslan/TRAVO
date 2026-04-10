"""
Test script for landmark recognition model
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import base64
import logging
from models.landmark_hf import predict_landmark

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_with_sample_image():
    """Test with a sample image"""
    try:
        # Create a simple test image (1x1 red pixel)
        from PIL import Image
        import io
        
        # Create a small test image
        img = Image.new('RGB', (224, 224), color='red')
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        image_bytes = buffer.getvalue()
        
        # Encode to base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        logger.info("Testing landmark prediction...")
        result = predict_landmark(image_base64, top_k=3)
        
        logger.info("✅ Prediction successful!")
        logger.info(f"Top prediction: {result['identified_monument']}")
        logger.info(f"Confidence: {result['confidence']:.4f}")
        logger.info(f"\nTop 3 candidates:")
        for i, candidate in enumerate(result['candidates'], 1):
            logger.info(f"  {i}. {candidate['monument_name']}: {candidate['confidence']:.4f}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}", exc_info=True)
        return False

if __name__ == "__main__":
    success = test_with_sample_image()
    sys.exit(0 if success else 1)
