from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserPreferences(BaseModel):
    favorite_destinations: Optional[List[str]] = Field(default=[])
    travel_interests: Optional[List[str]] = Field(default=[])
    accommodation_preferences: Optional[List[str]] = Field(default=[])
    budget_range: Optional[dict] = Field(default=None)
    notification_settings: Optional[dict] = Field(default=None)

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str
    preferences: Optional[UserPreferences] = None

class UserResponse(UserBase):
    id: str
    profile_picture: Optional[str] = None
    preferences: Optional[UserPreferences] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class SavedItinerary(BaseModel):
    id: str
    user_id: str
    name: str
    destinations: List[str]
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
