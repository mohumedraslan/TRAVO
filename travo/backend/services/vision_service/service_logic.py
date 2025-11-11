import uuid
import random
import json
import os
import time
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple, ByteString

# CLIP and image processing imports
try:
    import torch
    import torch.nn.functional as F
    from transformers import CLIPProcessor, CLIPModel
    CLIP_AVAILABLE = True
except ImportError:
    CLIP_AVAILABLE = False
    logging.warning("CLIP dependencies not available. Monument identification will use fallback method.")

import cv2
import numpy as np
from PIL import Image
import io

# CLIP model and processor initialization
model = None
processor = None
text_embeddings = None
monument_labels = None

# Configuration
CONFIDENCE_THRESHOLD = 0.45

# Initialize logging
logger = logging.getLogger(__name__)

def initialize_clip_model():
    """Initialize CLIP if available; always load monument labels.
    Returns True if CLIP was initialized successfully, else False.
    """
    global model, processor, text_embeddings, monument_labels

    # Always load labels for both CLIP and fallback paths
    monuments_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'monuments.json'))
    try:
        with open(monuments_path, "r") as f:
            monument_labels = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load monument labels from {monuments_path}: {e}")
        monument_labels = []

    if not CLIP_AVAILABLE:
        logger.warning("CLIP not available; using fallback identification.")
        return False

    try:
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        monument_texts = [f"A photo of {m['name']}" for m in monument_labels]
        text_inputs = processor(text=monument_texts, return_tensors="pt", padding=True)
        with torch.no_grad():
            text_features = model.get_text_features(**text_inputs)
        text_embeddings = text_features / text_features.norm(dim=-1, keepdim=True)
        return True
    except Exception as e:
        logger.error(f"Failed to initialize CLIP model: {e}", exc_info=True)
        model = None
        processor = None
        text_embeddings = None
        return False

# Initialize CLIP model on module import
clip_initialized = initialize_clip_model()

# Mock database of monuments
MONUMENTS_DB = [
    {
        "monument_id": "eiffel-tower-paris",
        "name": "Eiffel Tower",
        "description": "Iconic iron lattice tower in Paris, France, built in 1889",
        "location": {"latitude": 48.8584, "longitude": 2.2945},
        "country": "France",
        "city": "Paris"
    },
    {
        "monument_id": "colosseum-rome",
        "name": "Colosseum",
        "description": "Ancient Roman amphitheatre in Rome, Italy, largest ever built",
        "location": {"latitude": 41.8902, "longitude": 12.4922},
        "country": "Italy",
        "city": "Rome"
    },
    {
        "monument_id": "taj-mahal-agra",
        "name": "Taj Mahal",
        "description": "Ivory-white marble mausoleum in Agra, India, built by Mughal emperor Shah Jahan",
        "location": {"latitude": 27.1751, "longitude": 78.0421},
        "country": "India",
        "city": "Agra"
    },
    {
        "monument_id": "temple-of-luxor-luxor",
        "name": "Temple of Luxor",
        "description": "Ancient Egyptian temple complex on the east bank of the Nile River in Luxor",
        "location": {"latitude": 25.6995, "longitude": 32.6396},
        "country": "Egypt",
        "city": "Luxor"
    },
    {
        "monument_id": "pyramids-of-giza-giza",
        "name": "Pyramids of Giza",
        "description": "Ancient pyramid complex in Egypt, including the Great Pyramid, one of the Seven Wonders",
        "location": {"latitude": 29.9792, "longitude": 31.1342},
        "country": "Egypt",
        "city": "Giza"
    },
    {
        "monument_id": "parthenon-athens",
        "name": "Parthenon",
        "description": "Ancient Greek temple on the Acropolis of Athens, dedicated to goddess Athena",
        "location": {"latitude": 37.9715, "longitude": 23.7267},
        "country": "Greece",
        "city": "Athens"
    },
    {
        "monument_id": "great-wall-of-china-china",
        "name": "Great Wall of China",
        "description": "Series of fortifications across northern China, built to protect against invasions",
        "location": {"latitude": 40.4319, "longitude": 116.5704},
        "country": "China",
        "city": "Various"
    },
    {
        "monument_id": "machu-picchu-peru",
        "name": "Machu Picchu",
        "description": "Ancient Incan citadel set high in the Andes Mountains of Peru",
        "location": {"latitude": -13.1631, "longitude": -72.5450},
        "country": "Peru",
        "city": "Cusco Region"
    },
    {
        "monument_id": "stonehenge-wiltshire",
        "name": "Stonehenge",
        "description": "Prehistoric monument in Wiltshire, England consisting of a ring of standing stones",
        "location": {"latitude": 51.1789, "longitude": -1.8262},
        "country": "United Kingdom",
        "city": "Wiltshire"
    },
    {
        "monument_id": "angkor-wat-cambodia",
        "name": "Angkor Wat",
        "description": "Temple complex in Cambodia and the largest religious monument in the world",
        "location": {"latitude": 13.4125, "longitude": 103.8667},
        "country": "Cambodia",
        "city": "Siem Reap"
    },
    {
        "monument_id": "statue-of-liberty-new-york",
        "name": "Statue of Liberty",
        "description": "Neoclassical sculpture on Liberty Island in New York Harbor",
        "location": {"latitude": 40.6892, "longitude": -74.0445},
        "country": "United States",
        "city": "New York"
    },
    {
        "monument_id": "christ-the-redeemer-rio-de-janeiro",
        "name": "Christ the Redeemer",
        "description": "Art Deco statue of Jesus Christ in Rio de Janeiro, Brazil",
        "location": {"latitude": -22.9519, "longitude": -43.2105},
        "country": "Brazil",
        "city": "Rio de Janeiro"
    },
    {
        "monument_id": "petra-jordan",
        "name": "Petra",
        "description": "Archaeological site in Jordan famous for its rock-cut architecture",
        "location": {"latitude": 30.3285, "longitude": 35.4444},
        "country": "Jordan",
        "city": "Ma'an Governorate"
    },
    {
        "monument_id": "chichen-itza-mexico",
        "name": "Chichen Itza",
        "description": "Large pre-Columbian archaeological site built by the Maya civilization",
        "location": {"latitude": 20.6843, "longitude": -88.5678},
        "country": "Mexico",
        "city": "Yucatán"
    },
    {
        "monument_id": "big-ben-london",
        "name": "Big Ben",
        "description": "Famous clock tower at the Palace of Westminster in London, England",
        "location": {"latitude": 51.5007, "longitude": -0.1246},
        "country": "United Kingdom",
        "city": "London"
    },
    {
        "monument_id": "sydney-opera-house-sydney",
        "name": "Sydney Opera House",
        "description": "Multi-venue performing arts centre in Sydney, Australia with distinctive shell design",
        "location": {"latitude": -33.8568, "longitude": 151.2153},
        "country": "Australia",
        "city": "Sydney"
    },
    {
        "monument_id": "golden-gate-bridge-san-francisco",
        "name": "Golden Gate Bridge",
        "description": "Suspension bridge spanning the Golden Gate strait in San Francisco, California",
        "location": {"latitude": 37.8199, "longitude": -122.4783},
        "country": "United States",
        "city": "San Francisco"
    },
    {
        "monument_id": "sagrada-familia-barcelona",
        "name": "Sagrada Familia",
        "description": "Large unfinished Roman Catholic basilica in Barcelona, Spain, designed by Gaudí",
        "location": {"latitude": 41.4036, "longitude": 2.1744},
        "country": "Spain",
        "city": "Barcelona"
    },
    {
        "monument_id": "notre-dame-cathedral-paris",
        "name": "Notre-Dame Cathedral",
        "description": "Medieval Catholic cathedral in Paris, France, famous for French Gothic architecture",
        "location": {"latitude": 48.8530, "longitude": 2.3499},
        "country": "France",
        "city": "Paris"
    },
    {
        "monument_id": "neuschwanstein-castle-bavaria",
        "name": "Neuschwanstein Castle",
        "description": "19th-century Romanesque Revival palace in Bavaria, Germany",
        "location": {"latitude": 47.5576, "longitude": 10.7498},
        "country": "Germany",
        "city": "Bavaria"
    }
]

def get_monument_details_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Retrieve full monument details from MONUMENTS_DB by name."""
    logger.debug(f"Searching for monument details for: {name}")
    for monument in MONUMENTS_DB:
        if monument["name"] == name:
            logger.debug(f"Found monument details for: {name}")
            return monument
    logger.warning(f"No monument details found for: {name}")
    return None

def identify_monument(image: Image.Image):
    """Identify monument using CLIP when available, else fallback.
    Returns a dict with keys: identified_monument, confidence, monument_id, candidates.
    """
    try:
        if not CLIP_AVAILABLE or not clip_initialized or model is None or processor is None or text_embeddings is None:
            # Fallback
            return fallback_identification()

        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            image_features = model.get_image_features(**inputs)
        image_features /= image_features.norm(dim=-1, keepdim=True)

        similarity = (image_features @ text_embeddings.T).softmax(dim=-1)
        best_idx = similarity.argmax().item()
        best_match = monument_labels[best_idx]
        confidence = float(similarity[0][best_idx].item())

        # Top-3 candidates
        topk_idx = similarity[0].topk(3).indices.tolist()
        candidates = [
            {"monument_name": monument_labels[i]["name"], "confidence": float(similarity[0][i])}
            for i in topk_idx
        ]

        return {
            "identified_monument": best_match.get("name"),
            "confidence": confidence,
            "monument_id": best_match.get("id"),
            "candidates": candidates
        }
    except Exception as e:
        logger.error(f"Error during CLIP identification, using fallback: {e}", exc_info=True)
        return fallback_identification()
def fallback_identification() -> Dict[str, Any]:
    """Fallback monument identification: pick a random label and build a consistent response."""
    logger.info("Using fallback identification method")
    try:
        if monument_labels:
            selected = random.choice(monument_labels)
            name = selected.get("name")
            mid = selected.get("id")
            confidence = round(random.uniform(0.3, 0.6), 4)
            candidates = [{"monument_name": name, "confidence": confidence}]
            return {
                "identified_monument": name,
                "confidence": confidence,
                "monument_id": mid,
                "candidates": candidates,
            }
        else:
            logger.warning("No monument labels loaded for fallback.")
            return {
                "identified_monument": "Unknown",
                "confidence": 0.0,
                "monument_id": None,
                "candidates": [],
            }
    except Exception as e:
        logger.error(f"Error in fallback identification: {e}", exc_info=True)
        return {
            "identified_monument": "Unknown",
            "confidence": 0.0,
            "monument_id": None,
            "candidates": [],
        }
