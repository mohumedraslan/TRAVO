from pydantic import BaseModel, Field, HttpUrl, confloat
from typing import List, Optional, Dict
from datetime import datetime

class BoundingBox(BaseModel):
    x_min: float
    y_min: float
    x_max: float
    y_max: float

class DetectedMonument(BaseModel):
    monument_id: str
    name: str
    confidence: float
    bounding_box: BoundingBox

class MonumentDetectionResponse(BaseModel):
    image_id: str
    detected_monuments: List[DetectedMonument]
    processing_time_ms: float
    timestamp: datetime

class HistoricalPeriod(BaseModel):
    name: str
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    description: str

class MonumentInfo(BaseModel):
    monument_id: str
    name: str
    description: str
    location: Dict[str, float]  # {"latitude": 48.8584, "longitude": 2.2945}
    country: str
    city: str
    year_built: Optional[int] = None
    historical_period: Optional[HistoricalPeriod] = None
    architect: Optional[str] = None
    style: Optional[str] = None
    height_meters: Optional[float] = None
    fun_facts: List[str] = Field(default=[])
    image_urls: List[HttpUrl] = Field(default=[])
    wikipedia_url: Optional[HttpUrl] = None
    last_updated: datetime


class MonumentIdentificationResponse(BaseModel):
    identified_monument: str
    confidence: confloat(ge=0.0, le=1.0) = Field(..., description="Confidence score between 0 and 1")
