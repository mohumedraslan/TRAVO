from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class UserBase(BaseModel):
    """Base user schema with common attributes."""
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def password_strength(cls, v):
        """Validate password strength."""
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Schema for user data returned to client."""
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class InterestCategory(str, Enum):
    """Categories of interests for user preferences."""
    HISTORICAL = "historical"
    CULTURAL = "cultural"
    NATURAL = "natural"
    ADVENTURE = "adventure"
    CULINARY = "culinary"
    RELIGIOUS = "religious"


class UserPreferencesBase(BaseModel):
    """Base schema for user preferences."""
    interests: List[InterestCategory] = Field(default=[])
    preferred_cities: List[str] = Field(default=[])
    saved_itineraries: List[int] = Field(default=[])
    preferred_language: Optional[str] = None
    notification_settings: Dict[str, bool] = Field(
        default_factory=lambda: {
            "email_notifications": True,
            "push_notifications": True,
            "crowd_alerts": False
        }
    )
    additional_settings: Dict[str, Any] = Field(default_factory=dict)


class UserPreferencesCreate(UserPreferencesBase):
    """Schema for creating user preferences."""
    pass


class UserPreferencesUpdate(UserPreferencesBase):
    """Schema for updating user preferences."""
    pass


class UserPreferencesResponse(UserPreferencesBase):
    """Schema for user preferences returned to client."""
    user_id: int
    updated_at: datetime
    
    class Config:
        orm_mode = True
