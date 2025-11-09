"""
Google Vision API Client for TRAVO
Landmark Detection using Google Cloud Vision
"""
import os
import logging
from typing import Dict, Any, Optional, List
from google.cloud import vision
from google.oauth2 import service_account
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

logger = logging.getLogger(__name__)

# Google Vision Configuration
CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '../../temporal-fx-455221-u3-e44db70f518a.json')


def get_vision_client():
    """Get authenticated Google Vision client"""
    try:
        # Load credentials
        credentials = service_account.Credentials.from_service_account_file(
            CREDENTIALS_PATH
        )
        
        # Create client
        client = vision.ImageAnnotatorClient(credentials=credentials)
        return client
    except Exception as e:
        logger.error(f"Error creating Vision client: {e}")
        raise


def detect_landmark(image_path: str) -> Dict[str, Any]:
    """
    Detect landmarks in an image using Google Vision API
    
    Args:
        image_path: Path to image file or base64 encoded image
        
    Returns:
        Dictionary with landmark detection results
    """
    try:
        client = get_vision_client()
        
        # Load image
        if os.path.exists(image_path):
            # From file
            with open(image_path, 'rb') as image_file:
                content = image_file.read()
        else:
            # Assume base64
            import base64
            content = base64.b64decode(image_path)
        
        image = vision.Image(content=content)
        
        # Perform landmark detection
        response = client.landmark_detection(image=image)
        landmarks = response.landmark_annotations
        
        if response.error.message:
            logger.error(f"Vision API error: {response.error.message}")
            return {
                "success": False,
                "error": response.error.message
            }
        
        if not landmarks:
            # Try label detection as fallback
            label_response = client.label_detection(image=image)
            labels = label_response.label_annotations
            
            if labels:
                top_labels = [label.description for label in labels[:3]]
                return {
                    "success": True,
                    "landmark_detected": False,
                    "description": ", ".join(top_labels),
                    "confidence": labels[0].score if labels else 0.0,
                    "labels": top_labels
                }
            else:
                return {
                    "success": True,
                    "landmark_detected": False,
                    "description": "Unable to identify landmark or objects in image",
                    "confidence": 0.0
                }
        
        # Extract landmark information
        landmark = landmarks[0]  # Get top result
        
        # Get location if available
        location_info = None
        if landmark.locations:
            lat_lng = landmark.locations[0].lat_lng
            location_info = {
                "latitude": lat_lng.latitude,
                "longitude": lat_lng.longitude
            }
        
        logger.info(f"Landmark detected: {landmark.description} (confidence: {landmark.score})")
        
        return {
            "success": True,
            "landmark_detected": True,
            "name": landmark.description,
            "confidence": landmark.score,
            "location": location_info,
            "bounding_poly": [
                {"x": vertex.x, "y": vertex.y}
                for vertex in landmark.bounding_poly.vertices
            ] if landmark.bounding_poly else None
        }
        
    except FileNotFoundError:
        logger.error(f"Image file not found: {image_path}")
        return {
            "success": False,
            "error": f"Image file not found: {image_path}"
        }
    except Exception as e:
        logger.error(f"Error detecting landmark: {e}", exc_info=True)
        return {
            "success": False,
            "error": f"Landmark detection failed: {str(e)}"
        }


def detect_landmark_from_base64(image_base64: str) -> Dict[str, Any]:
    """
    Detect landmarks from base64 encoded image
    
    Args:
        image_base64: Base64 encoded image string
        
    Returns:
        Dictionary with landmark detection results
    """
    try:
        import base64
        
        client = get_vision_client()
        
        # Decode base64
        content = base64.b64decode(image_base64)
        image = vision.Image(content=content)
        
        # Perform landmark detection
        response = client.landmark_detection(image=image)
        landmarks = response.landmark_annotations
        
        if response.error.message:
            logger.error(f"Vision API error: {response.error.message}")
            return {
                "success": False,
                "error": response.error.message
            }
        
        if not landmarks:
            # Try label detection as fallback
            label_response = client.label_detection(image=image)
            labels = label_response.label_annotations
            
            if labels:
                top_labels = [label.description for label in labels[:3]]
                return {
                    "success": True,
                    "landmark_detected": False,
                    "description": ", ".join(top_labels),
                    "confidence": labels[0].score if labels else 0.0,
                    "labels": top_labels
                }
            else:
                return {
                    "success": True,
                    "landmark_detected": False,
                    "description": "Unable to identify landmark or objects in image",
                    "confidence": 0.0
                }
        
        # Extract landmark information
        landmark = landmarks[0]
        
        # Get location if available
        location_info = None
        if landmark.locations:
            lat_lng = landmark.locations[0].lat_lng
            location_info = {
                "latitude": lat_lng.latitude,
                "longitude": lat_lng.longitude
            }
        
        logger.info(f"Landmark detected: {landmark.description} (confidence: {landmark.score})")
        
        return {
            "success": True,
            "landmark_detected": True,
            "name": landmark.description,
            "confidence": landmark.score,
            "location": location_info
        }
        
    except Exception as e:
        logger.error(f"Error detecting landmark from base64: {e}", exc_info=True)
        return {
            "success": False,
            "error": f"Landmark detection failed: {str(e)}"
        }


def get_landmark_description(landmark_name: str) -> str:
    """
    Get a description of a landmark (placeholder for now)
    
    Args:
        landmark_name: Name of the landmark
        
    Returns:
        Description string
    """
    # This could be enhanced with a database lookup
    return f"Information about {landmark_name}"
