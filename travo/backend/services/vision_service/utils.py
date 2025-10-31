import hashlib
from typing import Dict, List, ByteString, Tuple
from datetime import datetime
import base64

def generate_image_hash(image_content: ByteString) -> str:
    """Generate a hash for an image to use as a unique identifier"""
    return hashlib.sha256(image_content).hexdigest()

def format_bounding_box(box: Dict[str, float], image_width: int, image_height: int) -> Dict[str, int]:
    """Convert normalized bounding box coordinates to pixel coordinates"""
    return {
        "x_min": int(box["x_min"] * image_width),
        "y_min": int(box["y_min"] * image_height),
        "x_max": int(box["x_max"] * image_width),
        "y_max": int(box["y_max"] * image_height)
    }

def encode_image_base64(image_content: ByteString) -> str:
    """Encode image as base64 string for API responses"""
    return base64.b64encode(image_content).decode('utf-8')

def calculate_detection_metrics(detections: List[Dict]) -> Dict:
    """Calculate metrics about the detection results"""
    if not detections:
        return {
            "count": 0,
            "avg_confidence": 0,
            "timestamp": datetime.utcnow()
        }
    
    # Calculate average confidence
    confidences = [d["confidence"] for d in detections]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
    
    return {
        "count": len(detections),
        "avg_confidence": round(avg_confidence, 2),
        "timestamp": datetime.utcnow()
    }

def get_monument_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the approximate distance between two points in kilometers
    
    This is a simplified implementation using the Haversine formula.
    In a production system, this would use a more sophisticated geospatial library.
    """
    from math import radians, cos, sin, asin, sqrt
    
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    
    return c * r
