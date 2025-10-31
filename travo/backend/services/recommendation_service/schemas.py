from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class RecommendationCategory(str, Enum):
    """Categories for recommendations."""
    BEACH = "beach"
    MOUNTAIN = "mountain"
    CITY = "city"
    CULTURAL = "cultural"
    ADVENTURE = "adventure"
    RELAXATION = "relaxation"
    FOOD = "food"
    SHOPPING = "shopping"
    NIGHTLIFE = "nightlife"
    FAMILY = "family"
    ROMANTIC = "romantic"
    BUDGET = "budget"
    LUXURY = "luxury"


class Season(str, Enum):
    """Seasons for travel recommendations."""
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"
    WINTER = "winter"


class BudgetLevel(str, Enum):
    """Budget levels for recommendations."""
    BUDGET = "budget"
    MODERATE = "moderate"
    LUXURY = "luxury"


class Location(BaseModel):
    """Location information."""
    city: str
    country: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class WeatherInfo(BaseModel):
    """Weather information for a destination."""
    avg_temperature: float
    precipitation: float
    best_season: Season
    current_weather: Optional[str] = None


class DestinationRecommendationResponse(BaseModel):
    """Response model for destination recommendations."""
    id: str
    name: str
    description: str
    location: Location
    categories: List[RecommendationCategory]
    image_url: str
    rating: float = Field(..., ge=0, le=5)
    budget_level: BudgetLevel
    best_time_to_visit: List[Season]
    popularity_score: float = Field(..., ge=0, le=100)
    weather_info: Optional[WeatherInfo] = None
    tags: List[str] = []
    highlights: List[str] = []
    recommendation_reason: Optional[str] = None


class AttractionRecommendationResponse(BaseModel):
    """Response model for attraction recommendations."""
    id: str
    name: str
    description: str
    destination_id: str
    location: Location
    categories: List[RecommendationCategory]
    image_url: str
    rating: float = Field(..., ge=0, le=5)
    price_level: Optional[int] = Field(None, ge=1, le=4)
    estimated_duration_minutes: Optional[int] = None
    tags: List[str] = []
    best_time_to_visit: Optional[List[Season]] = None
    recommendation_reason: Optional[str] = None


class TravelHistoryItem(BaseModel):
    """Item in a user's travel history."""
    destination_id: str
    visit_date: datetime
    duration_days: int
    rating: Optional[float] = None
    activities: Optional[List[str]] = None


class UpcomingTrip(BaseModel):
    """Information about a user's upcoming trip."""
    destination_id: str
    start_date: datetime
    end_date: datetime
    purpose: Optional[str] = None


class UserPreference(BaseModel):
    """User preference for recommendations."""
    category: RecommendationCategory
    weight: float = Field(1.0, ge=0, le=10)


class RecommendationRequest(BaseModel):
    """Request model for personalized recommendations."""
    user_id: str
    preferences: Optional[List[UserPreference]] = None
    travel_history: Optional[List[TravelHistoryItem]] = None
    upcoming_trips: Optional[List[UpcomingTrip]] = None
    current_location: Optional[Location] = None
    travel_dates: Optional[Dict[str, datetime]] = None
    budget_level: Optional[BudgetLevel] = None
    group_size: Optional[int] = Field(None, ge=1)
    trip_duration_days: Optional[int] = Field(None, ge=1)

    @validator('travel_dates')
    def validate_travel_dates(cls, v):
        if v and ('start_date' not in v or 'end_date' not in v):
            raise ValueError("travel_dates must contain 'start_date' and 'end_date'")
        if v and v['end_date'] < v['start_date']:
            raise ValueError("end_date cannot be before start_date")
        return v


class RecommendedItinerary(BaseModel):
    """A recommended itinerary."""
    id: str
    title: str
    description: str
    destination_id: str
    duration_days: int
    activities_count: int
    estimated_cost: float
    currency: str
    image_url: str
    tags: List[str] = []


class PersonalizedRecommendationResponse(BaseModel):
    """Response model for personalized recommendations."""
    destinations: List[DestinationRecommendationResponse]
    attractions: List[AttractionRecommendationResponse]
    itineraries: List[RecommendedItinerary]
    recommendation_date: datetime = Field(default_factory=datetime.utcnow)
    expiry_date: Optional[datetime] = None
    personalization_factors: List[str] = []
