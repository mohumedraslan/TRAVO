from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Body
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel
import base64
import logging
import os
import json

from .schemas import (
    AssistantQuery, 
    AssistantResponse,
    VoiceToTextRequest,
    VoiceToTextResponse,
    TextToVoiceRequest,
    TextToVoiceResponse,
    QueryType
)
from .service_logic import voice_to_text, text_to_voice
# External AI providers disabled by configuration
from services.vision_service.service_logic import identify_monument
from PIL import Image
import io

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
# router = APIRouter(prefix="/assistant", tags=["assistant"])
router = APIRouter(tags=["assistant"])


# New request model that handles optional params
class NewAssistantQuery(BaseModel):
    query: str
    location: Optional[str] = None
    query_type: str = "TEXT"
    image: Optional[str] = None  # Base64 encoded image for IMAGE queries


@router.post("/ask")
async def ask_assistant(request: NewAssistantQuery):
    """Process a text or image query to the assistant using local logic only.
    
    Accepts:
    - TEXT queries: Returns static descriptions from local monuments.json
    - IMAGE queries: Uses CLIP (if cached) or fallback to guess a monument, then returns static description
    
    Request body:
    {
        "query": "Your question",
        "location": "Optional location context",
        "query_type": "TEXT" or "IMAGE",
        "image": "Base64 encoded image (required for IMAGE type)"
    }
    """
    try:
        logger.info(f"Received query: {request.query} (type: {request.query_type}, location: {request.location})")
        
        if request.query_type.upper() == "TEXT":
            # Always use static description based on monuments.json
            data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "monuments.json")
            try:
                with open(data_path, "r", encoding="utf-8") as f:
                    catalog = json.load(f)
            except Exception as e:
                catalog = []
                logger.error(f"Failed to load monuments.json: {e}")

            ql = (request.query or "").lower()
            locl = (request.location or "").lower()
            chosen = None
            for m in catalog:
                nm = str(m.get("name", "")).lower()
                if nm and ((nm in ql) or (ql in nm) or (nm in locl) or (locl in nm)):
                    chosen = m
                    break
            if not chosen and catalog:
                chosen = catalog[0]
            desc = (chosen or {}).get("description", "No description available.")
            facts = (chosen or {}).get("facts", [])
            extra = facts[0] if isinstance(facts, list) and facts else ""
            answer_text = (f"{(chosen or {}).get('name', 'This monument')}: {desc} " + (extra or "")).strip()
            return JSONResponse(
                status_code=200,
                content={
                    "type": "TEXT",
                    "original_query": request.query,
                    "answer": answer_text,
                    "fallback_used": True,
                    "monument": (chosen or {}).get("name"),
                    "description": desc,
                    "extra_info": extra,
                    "location": request.location,
                }
            )
            
        elif request.query_type.upper() == "IMAGE":
            if not request.image:
                return JSONResponse(
                    status_code=400,
                    content={
                        "error": "Image data required for IMAGE query type"
                    }
                )
            logger.info("Detecting landmark with CLIP...")
            # Decode base64 to PIL image
            try:
                image_bytes = base64.b64decode(request.image)
                image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            except Exception as e:
                logger.error(f"Invalid image data: {e}")
                return JSONResponse(status_code=400, content={"error": "Invalid image data"})

            # Run CLIP-based identification
            clip_result = identify_monument(image)

            # Load catalog for static descriptions
            data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "monuments.json")
            try:
                with open(data_path, "r", encoding="utf-8") as f:
                    catalog = json.load(f)
            except Exception as e:
                catalog = []
                logger.error(f"Failed to load monuments.json: {e}")

            landmark_name = clip_result.get("identified_monument") or None
            confidence = float(clip_result.get("confidence") or 0.0)

            if landmark_name and landmark_name != "Unknown":
                # Static description by matching catalog name
                matched = None
                ln = (landmark_name or "").lower()
                for m in catalog:
                    nm = str(m.get("name", "")).lower()
                    if nm and (nm in ln or ln in nm):
                        matched = m
                        break
                desc = (matched or {}).get("description", "No description available.")
                facts = (matched or {}).get("facts", [])
                extra = facts[0] if isinstance(facts, list) and facts else ""
                return JSONResponse(status_code=200, content={
                    "type": "IMAGE",
                    "original_query": request.query,
                    "landmark_detected": landmark_name,
                    "confidence": confidence,
                    "answer": (f"About {landmark_name}: {desc} " + (extra or "")).strip(),
                    "description": desc,
                    "extra_info": extra,
                    "location": request.location,
                    "fallback_used": True,
                })

            # No clear landmark name; provide a simple static response
            chosen = catalog[0] if catalog else {}
            desc = chosen.get("description", "I couldn't identify the landmark from the image.")
            extra = (chosen.get("facts", []) or [""])[0]
            return JSONResponse(status_code=200, content={
                "type": "IMAGE",
                "original_query": request.query,
                "landmark_detected": None,
                "confidence": confidence,
                "answer": (f"{desc} {extra}").strip(),
                "location": request.location,
                "fallback_used": True,
            })
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "error": f"Invalid query_type: {request.query_type}. Must be TEXT or IMAGE"
                }
            )
    
    except Exception as e:
        logger.error(f"Error processing assistant query: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": f"Error processing query: {str(e)}"
            }
        )


@router.post("/voice_to_text", response_model=VoiceToTextResponse)
async def process_voice_to_text(request: VoiceToTextRequest):
    """Convert voice audio to text.
    
    This endpoint accepts base64 encoded audio data and returns
    the transcribed text that can be used for further processing.
    """
    try:
        # Log the incoming request
        logger.info(f"Received voice-to-text request (language: {request.language})")
        
        # Process the voice data
        result = voice_to_text(request.audio_data, request.language)
        
        # Create response object
        response = VoiceToTextResponse(
            text=result["text"],
            confidence=result["confidence"]
        )
        
        return response
    
    except Exception as e:
        logger.error(f"Error processing voice to text: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing voice: {str(e)}"
        )


@router.post("/text_to_voice", response_model=TextToVoiceResponse)
async def process_text_to_voice(request: TextToVoiceRequest):
    """Convert text to voice audio.
    
    This endpoint accepts text and returns base64 encoded audio data
    that can be played on the client side.
    """
    try:
        # Log the incoming request
        logger.info(f"Received text-to-voice request (language: {request.language})")
        
        # Process the text data
        result = text_to_voice(request.text, request.language, request.voice)
        
        # Check for errors
        if "error" in result:
            raise HTTPException(
                status_code=500,
                detail=result["error"]
            )
        
        # Create response object
        response = TextToVoiceResponse(
            audio_data=result["audio_data"],
            format=result["format"]
        )
        
        return response
    
    except Exception as e:
        logger.error(f"Error processing text to voice: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing text to voice: {str(e)}"
        )


@router.post("/upload_audio", response_model=VoiceToTextResponse)
async def upload_audio_file(
    audio_file: UploadFile = File(...),
    language: str = Form("en-US")
):
    """Upload an audio file for transcription.
    
    This endpoint accepts an audio file upload and returns
    the transcribed text. This is an alternative to sending
    base64 encoded audio data.
    """
    try:
        # Read the file content
        audio_data = await audio_file.read()
        
        # Encode to base64
        audio_data_base64 = base64.b64encode(audio_data).decode("utf-8")
        
        # Process the voice data
        result = voice_to_text(audio_data_base64, language)
        
        # Create response object
        response = VoiceToTextResponse(
            text=result["text"],
            confidence=result["confidence"]
        )
        
        return response
    
    except Exception as e:
        logger.error(f"Error processing audio file: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing audio file: {str(e)}"
        )
