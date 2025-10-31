from fastapi import APIRouter, HTTPException, status, BackgroundTasks, File, UploadFile
from typing import Optional, List

# Import schemas and service logic
from .schemas import TextQueryRequest, TextQueryResponse, VoiceQueryResponse, ConversationHistory
from .service_logic import process_text_query, process_voice_query, get_conversation_history

# Create router
router = APIRouter()

# Test route
@router.get("/test")
async def test_assistant_service():
    return {"status": "ok", "service": "assistant_service"}

# Text-based Q&A endpoint
@router.post("/query/text", response_model=TextQueryResponse)
async def text_query(request: TextQueryRequest):
    # Process the text query
    response = await process_text_query(
        query=request.query,
        user_id=request.user_id,
        conversation_id=request.conversation_id,
        location=request.location,
        language=request.language
    )
    
    return response

# Voice-based Q&A endpoint
@router.post("/query/voice", response_model=VoiceQueryResponse)
async def voice_query(
    audio: UploadFile = File(...),
    user_id: Optional[str] = None,
    conversation_id: Optional[str] = None,
    language: Optional[str] = "en",
    latitude: Optional[float] = None,
    longitude: Optional[float] = None
):
    # Validate file type
    if not audio.content_type.startswith('audio/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an audio file"
        )
    
    # Read audio content
    audio_content = await audio.read()
    
    # Process the voice query
    response = await process_voice_query(
        audio_content=audio_content,
        user_id=user_id,
        conversation_id=conversation_id,
        language=language,
        location={"latitude": latitude, "longitude": longitude} if latitude and longitude else None
    )
    
    return response

# Get conversation history
@router.get("/conversation/{conversation_id}", response_model=ConversationHistory)
async def get_conversation(
    conversation_id: str,
    limit: Optional[int] = 10
):
    history = await get_conversation_history(conversation_id, limit)
    
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return history
