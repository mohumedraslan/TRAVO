from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class QueryType(str, Enum):
    """Type of query input."""
    TEXT = "text"
    VOICE = "voice"


class AssistantQuery(BaseModel):
    """Model for assistant query."""
    query: str = Field(..., description="The user's question or query")
    location: Optional[str] = Field(None, description="Optional location context for the query")
    query_type: QueryType = Field(default=QueryType.TEXT, description="Type of query input")


class AssistantResponse(BaseModel):
    """Model for assistant response."""
    answer: str = Field(..., description="The assistant's answer to the query")
    related_monuments: List[str] = Field(default=[], description="Related monuments to the query")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the answer")


class VoiceToTextRequest(BaseModel):
    """Model for voice-to-text conversion request."""
    audio_data: str = Field(..., description="Base64 encoded audio data")
    language: str = Field(default="en-US", description="Language code for speech recognition")


class VoiceToTextResponse(BaseModel):
    """Model for voice-to-text conversion response."""
    text: str = Field(..., description="Transcribed text from voice input")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score of transcription")


class TextToVoiceRequest(BaseModel):
    """Model for text-to-voice conversion request."""
    text: str = Field(..., description="Text to convert to speech")
    language: str = Field(default="en", description="Language code for text-to-speech")
    voice: Optional[str] = Field(None, description="Voice ID or name for text-to-speech")


class TextToVoiceResponse(BaseModel):
    """Model for text-to-voice conversion response."""
    audio_data: str = Field(..., description="Base64 encoded audio data")
    format: str = Field(default="mp3", description="Audio format")
