from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class UserPreferencesUpdate(BaseModel):
    interests: Optional[List[str]] = None
    preferred_cities: Optional[List[str]] = None
    saved_itineraries: Optional[List[str]] = None
    preferred_language: Optional[str] = None
    notification_settings: Optional[Dict[str, Any]] = None
    additional_settings: Optional[Dict[str, Any]] = None

class UserPreferencesResponse(BaseModel):
    user_id: str
    interests: List[str]
    preferred_cities: List[str]
    saved_itineraries: List[str]
    preferred_language: str
    notification_settings: Dict[str, Any]
    additional_settings: Dict[str, Any]
    updated_at: datetime
