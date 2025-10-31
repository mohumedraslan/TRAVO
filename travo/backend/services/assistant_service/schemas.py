from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class MessageType(str, Enum):
    TEXT = "text"
    VOICE = "voice"

class LocationInfo(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    place_name: Optional[str] = None

class TextQueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None
    language: Optional[str] = "en"
    location: Optional[LocationInfo] = None

class Message(BaseModel):
    role: MessageRole
    content: str
    message_type: MessageType
    timestamp: datetime

class TextQueryResponse(BaseModel):
    response_text: str
    conversation_id: str
    message_id: str
    sources: List[Dict[str, Any]] = Field(default=[])
    related_attractions: List[Dict[str, Any]] = Field(default=[])
    timestamp: datetime

class VoiceQueryResponse(BaseModel):
    response_text: str
    audio_url: Optional[HttpUrl] = None
    conversation_id: str
    message_id: str
    transcription: str
    sources: List[Dict[str, Any]] = Field(default=[])
    related_attractions: List[Dict[str, Any]] = Field(default=[])
    timestamp: datetime

class ConversationHistory(BaseModel):
    conversation_id: str
    user_id: Optional[str] = None
    messages: List[Message]
    created_at: datetime
    updated_at: datetime
