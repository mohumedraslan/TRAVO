from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class BusinessCategory(str, Enum):
    RESTAURANT = "restaurant"
    HOTEL = "hotel"
    ATTRACTION = "attraction"
    SHOPPING = "shopping"
    ENTERTAINMENT = "entertainment"
    TRANSPORTATION = "transportation"
    OTHER = "other"

class PriceLevel(str, Enum):
    BUDGET = "$"
    MODERATE = "$$"
    EXPENSIVE = "$$$"
    LUXURY = "$$$$"

class BusinessHours(BaseModel):
    monday: Optional[str] = None
    tuesday: Optional[str] = None
    wednesday: Optional[str] = None
    thursday: Optional[str] = None
    friday: Optional[str] = None
    saturday: Optional[str] = None
    sunday: Optional[str] = None

class Location(BaseModel):
    address: str
    city: str
    state: Optional[str] = None
    country: str
    postal_code: Optional[str] = None
    latitude: float
    longitude: float

class BusinessListingResponse(BaseModel):
    id: str
    name: str
    category: BusinessCategory
    rating: float
    review_count: int
    price_level: Optional[PriceLevel] = None
    image_url: Optional[HttpUrl] = None
    location: Location
    distance_km: float

class BusinessDetailResponse(BaseModel):
    id: str
    name: str
    category: BusinessCategory
    description: Optional[str] = None
    rating: float
    review_count: int
    price_level: Optional[PriceLevel] = None
    phone: Optional[str] = None
    website: Optional[HttpUrl] = None
    email: Optional[str] = None
    hours: Optional[BusinessHours] = None
    location: Location
    images: List[HttpUrl] = Field(default=[])
    amenities: List[str] = Field(default=[])
    tags: List[str] = Field(default=[])
    created_at: datetime
    updated_at: datetime

class ReviewCreate(BaseModel):
    user_id: str
    rating: float = Field(ge=1.0, le=5.0)
    content: str
    images: List[HttpUrl] = Field(default=[])

class ReviewResponse(BaseModel):
    id: str
    business_id: str
    user_id: str
    user_name: str
    rating: float
    content: str
    images: List[HttpUrl] = Field(default=[])
    created_at: datetime
    updated_at: datetime
