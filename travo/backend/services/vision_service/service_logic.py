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
clip_model = None
clip_processor = None
text_embeddings = None
monument_labels = None

# Configuration
CONFIDENCE_THRESHOLD = 0.45

# Initialize logging
logger = logging.getLogger(__name__)

def initialize_clip_model():
    """Initialize CLIP model and precompute text embeddings"""
    global clip_model, clip_processor, text_embeddings, monument_labels
    
    if not CLIP_AVAILABLE:
        logger.warning("CLIP not available, using fallback identification")
        return False
    
    try:
        logger.info("Loading CLIP model and processor...")
        start_time = time.time()
        
        # Load CLIP model and processor
        clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        
        # Load monument labels
        current_dir = os.path.dirname(os.path.abspath(__file__))
        labels_path = os.path.join(current_dir, 'labels.json')
        
        with open(labels_path, 'r', encoding='utf-8') as f:
            monument_labels = json.load(f)
        
        logger.info(f"Loaded {len(monument_labels)} monument labels")
        
        # Precompute text embeddings for all labels
        logger.info("Precomputing text embeddings...")
        text_inputs = []
        for monument in monument_labels:
            # Combine label and description for better context
            text = f"{monument['label']}: {monument['description']}"
            text_inputs.append(text)
        
        # Process text inputs
        text_inputs_processed = clip_processor(text=text_inputs, return_tensors="pt", padding=True)
        
        # Get text embeddings
        with torch.no_grad():
            text_embeddings = clip_model.get_text_features(**text_inputs_processed)
            # Normalize embeddings
            text_embeddings = F.normalize(text_embeddings, p=2, dim=1)
        
        load_time = time.time() - start_time
        logger.info(f"CLIP model initialized in {load_time:.2f} seconds")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize CLIP model: {e}", exc_info=True)
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
        "monument_.venv": "christ-the-redeemer-rio-de-janeiro",
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

def identify_monument(image_bytes: bytes) -> Dict[str, Any]:
    """
    Identifies a monument from an image using CLIP or a fallback method.
    """
    request_id = uuid.uuid4()
    logger.info(f"Request {request_id}: Starting monument identification")

    if not clip_initialized or not CLIP_AVAILABLE:
        logger.warning(f"Request {request_id}: CLIP not initialized, using fallback method")
        return fallback_identification(request_id)

    try:
        start_time = time.time()
        
        # Preprocess the image
        logger.info(f"Request {request_id}: Preprocessing image")
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image_input = clip_processor(images=image, return_tensors="pt")
        
        # Compute image embedding
        logger.info(f"Request {request_id}: Computing image embedding")
        with torch.no_grad():
            image_embedding = clip_model.get_image_features(**image_input)
            image_embedding = F.normalize(image_embedding, p=2, dim=1)
        
        # Compute similarity
        logger.info(f"Request {request_id}: Computing similarity with text embeddings")
        similarity_scores = torch.matmul(image_embedding, text_embeddings.T)
        
        # Get top prediction
        top_score, top_index = torch.max(similarity_scores, dim=1)
        top_score = top_score.item()
        top_index = top_index.item()
        
        processing_time = time.time() - start_time
        logger.info(f"Request {request_id}: Image processing and similarity computation finished in {processing_time:.2f}s")
        logger.info(f"Request {request_id}: Top match: {monument_labels[top_index]['label']} with score {top_score:.3f}")

        if top_score < CONFIDENCE_THRESHOLD:
            logger.warning(f"Request {request_id}: No confident match found. Score {top_score:.3f} is below threshold {CONFIDENCE_THRESHOLD}")
            return {
                "identified_monument": None,
                "confidence": 0.0,
                "monument_id": None,
                "message": "No confident match found"
            }

        # Get monument details
        monument_name = monument_labels[top_index]["label"]
        logger.info(f"Request {request_id}: Retrieving details for monument: {monument_name}")
        monument_details = get_monument_details_by_name(monument_name)

        if not monument_details:
            logger.error(f"Request {request_id}: Monument details not found for '{monument_name}'")
            return {
                "identified_monument": None,
                "confidence": 0.0,
                "monument_id": None,
                "message": "Monument details not found"
            }
        
        logger.info(f"Request {request_id}: Successfully identified monument: {monument_name}")
        return {
            "identified_monument": monument_details["name"],
            "confidence": top_score,
            "monument_id": monument_details["monument_id"]
        }

    except Exception as e:
        logger.error(f"Request {request_id}: An error occurred during monument identification: {e}", exc_info=True)
        return {
            "identified_monument": None,
            "confidence": 0.0,
            "monument_id": None,
            "message": f"Error during identification: {str(e)}"
        }
async def fallback_identify_monument(image_data: bytes) -> Dict[str, Any]:
    """
    Fallback monument identification using a simplified random choice from loaded labels.
    """
    logger.info("Using fallback identification method")
    try:
        # This fallback will just return a random monument from the loaded labels
        if monument_labels:
            selected_monument_label = random.choice(monument_labels)
            label_name = selected_monument_label["label"]
            monument_details = get_monument_details_by_name(label_name)
            confidence = round(random.uniform(0.3, 0.6), 4)  # Lower confidence for fallback

            logger.info(f"Fallback selected monument: {label_name}")
            return {
                "candidates": [{
                    "monument_id": monument_details.get("monument_id") if monument_details else None,
                    "label": label_name,
                    "score": confidence,
                    "description": selected_monument_label["description"]
                }],
                "identified": label_name,
                "confidence": confidence
            }
        else:
            # Ultimate fallback if no labels are loaded
            logger.warning("No monument labels loaded for fallback.")
            return {
                "candidates": [],
                "identified": None,
                "confidence": 0.0
            }
    except Exception as e:
        logger.error(f"Error in fallback identification: {e}", exc_info=True)
        return {
            "candidates": [],
            "identified": None,
            "confidence": 0.0
        }
