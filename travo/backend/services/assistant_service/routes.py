from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Body
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel
import base64
import logging

from .schemas import (
    AssistantQuery, 
    AssistantResponse,
    VoiceToTextRequest,
    VoiceToTextResponse,
    TextToVoiceRequest,
    TextToVoiceResponse,
    QueryType
)
from .service_logic import get_ai_response, voice_to_text, text_to_voice
from services.ai_integration import (
    ask_simple_question,
    ask_complex_question,
    detect_landmark_from_base64
)

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
    """Process a text or image query to the AI assistant.
    
    Accepts:
    - TEXT queries: Uses DeepSeek API for conversational responses
    - IMAGE queries: Uses Google Vision for landmark detection, then DeepSeek for details
    
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
            # Handle text query with DeepSeek
            context = f"Location: {request.location}" if request.location else None
            
            # Use simple model for straightforward questions
            response_text = ask_simple_question(request.query, context)
            
            return JSONResponse(
                status_code=200,
                content={
                    "type": "TEXT",
                    "original_query": request.query,
                    "deepseek_response": response_text,
                    "location": request.location
                }
            )
            
        elif request.query_type.upper() == "IMAGE":
            # Handle image query with Google Vision + DeepSeek
            if not request.image:
                return JSONResponse(
                    status_code=400,
                    content={
                        "error": "Image data required for IMAGE query type"
                    }
                )
            
            # Detect landmark using Google Vision
            logger.info("Detecting landmark with Google Vision...")
            vision_result = detect_landmark_from_base64(request.image)
            
            if not vision_result["success"]:
                return JSONResponse(
                    status_code=500,
                    content={
                        "type": "IMAGE",
                        "original_query": request.query,
                        "error": vision_result.get("error", "Landmark detection failed")
                    }
                )
            
            # Build context for DeepSeek
            if vision_result.get("landmark_detected"):
                landmark_name = vision_result["name"]
                confidence = vision_result["confidence"]
                
                # Ask DeepSeek for details about the landmark
                deepseek_query = f"Tell me about {landmark_name}. {request.query}"
                context = f"Landmark detected: {landmark_name} (confidence: {confidence:.2f})"
                if request.location:
                    context += f"\nLocation: {request.location}"
                
                response_text = ask_complex_question(deepseek_query, context)
                
                return JSONResponse(
                    status_code=200,
                    content={
                        "type": "IMAGE",
                        "original_query": request.query,
                        "landmark_detected": landmark_name,
                        "confidence": confidence,
                        "deepseek_response": response_text,
                        "location": request.location
                    }
                )
            else:
                # No landmark detected, use labels
                description = vision_result.get("description", "Unknown object")
                
                deepseek_query = f"I see {description} in an image. {request.query}"
                response_text = ask_simple_question(deepseek_query)
                
                return JSONResponse(
                    status_code=200,
                    content={
                        "type": "IMAGE",
                        "original_query": request.query,
                        "landmark_detected": None,
                        "description": description,
                        "deepseek_response": response_text,
                        "location": request.location
                    }
                )
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
