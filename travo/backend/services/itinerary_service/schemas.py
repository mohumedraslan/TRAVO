from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime, time
from enum import Enum
import re


class ActivityType(str, Enum):
    ATTRACTION = "attraction"
    RESTAURANT = "restaurant"
    HOTEL = "hotel"
    TRANSPORTATION = "transportation"
    EVENT = "event"
    OTHER = "other"


class TransportationType(str, Enum):
    WALK = "walk"
    CAR = "car"
    PUBLIC_TRANSIT = "public_transit"
    TAXI = "taxi"
    FLIGHT = "flight"
    TRAIN = "train"
    BUS = "bus"
    BOAT = "boat"
    OTHER = "other"


class BudgetLevel(str, Enum):
    BUDGET = "budget"
    MODERATE = "moderate"
    LUXURY = "luxury"


class Location(BaseModel):
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class TransportationDetails(BaseModel):
    type: TransportationType
    departure_location: Optional[str] = None
    arrival_location: Optional[str] = None
    booking_reference: Optional[str] = None
    booking_url: Optional[str] = None
    notes: Optional[str] = None


class ItineraryActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    activity_type: ActivityType
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    day_index: int = Field(..., ge=0)  # 0-indexed day number in the itinerary
    location: Optional[Location] = None
    transportation: Optional[TransportationDetails] = None
    booking_info: Optional[Dict[str, Any]] = None
    cost: Optional[float] = None
    currency: Optional[str] = "USD"
    notes: Optional[str] = None
    image_url: Optional[str] = None
    external_url: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class ItineraryActivityCreate(ItineraryActivityBase):
    pass


class ItineraryActivityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    activity_type: Optional[ActivityType] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    day_index: Optional[int] = Field(None, ge=0)
    location: Optional[Location] = None
    transportation: Optional[TransportationDetails] = None
    booking_info: Optional[Dict[str, Any]] = None
    cost: Optional[float] = None
    currency: Optional[str] = None
    notes: Optional[str] = None
    image_url: Optional[str] = None
    external_url: Optional[str] = None
    tags: Optional[List[str]] = None


class ItineraryActivityResponse(ItineraryActivityBase):
    id: str
    created_at: datetime
    updated_at: datetime


class ItineraryDayResponse(BaseModel):
    day_index: int
    date: datetime
    activities: List[ItineraryActivityResponse] = Field(default_factory=list)


class ItineraryBase(BaseModel):
    title: str
    description: Optional[str] = None
    destination: str
    start_date: datetime
    end_date: datetime
    budget_level: Optional[BudgetLevel] = None
    tags: List[str] = Field(default_factory=list)
    cover_image_url: Optional[str] = None

    @validator('end_date')
    def end_date_after_start_date(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v


class ItineraryCreate(ItineraryBase):
    user_id: str


class ItineraryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    destination: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget_level: Optional[BudgetLevel] = None
    tags: Optional[List[str]] = None
    cover_image_url: Optional[str] = None

    @validator('end_date')
    def end_date_after_start_date(cls, v, values):
        if v and 'start_date' in values and values['start_date'] and v < values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v


class ItineraryResponse(ItineraryBase):
    id: str
    user_id: str
    days: List[ItineraryDayResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    total_activities: int
    total_cost: Optional[float] = None
    currency: str = "USD"


class ItineraryShareResponse(BaseModel):
    itinerary_id: str
    share_id: str
    share_url: str
    expires_at: Optional[datetime] = None
    created_at: datetime
