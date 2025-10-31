from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Body
from typing import Optional
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

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("/ask", response_model=AssistantResponse)
async def ask_assistant(query: AssistantQuery):
    """Process a text query to the AI assistant.
    
    This endpoint accepts a text query and optional location context,
    and returns a conversational response about monuments, their history,
    or visiting tips.
    """
    try:
        # Log the incoming query
        logger.info(f"Received query: {query.query} (type: {query.query_type}, location: {query.location})")
        
        # Process the query based on its type
        if query.query_type == QueryType.TEXT:
            # Get AI response for text query
            response_data = get_ai_response(query.query, query.location)
            
            # Create response object
            response = AssistantResponse(
                answer=response_data["answer"],
                related_monuments=response_data["related_monuments"],
                confidence=response_data["confidence"]
            )
            
            return response
        else:
            # Voice queries should be sent to the voice_to_text endpoint first
            raise HTTPException(
                status_code=400,
                detail="Voice queries should be sent to the /voice_to_text endpoint first"
            )
    
    except Exception as e:
        logger.error(f"Error processing assistant query: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
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
