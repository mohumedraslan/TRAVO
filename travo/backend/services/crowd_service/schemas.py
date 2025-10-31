from pydantic import BaseModel, Field
from typing import List, Optional, Tuple, Dict
from enum import Enum
from datetime import date, datetime

class CrowdLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"

class LocationRequest(BaseModel):
    location: str
    date: Optional[date] = None
    time_range: Optional[Tuple[int, int]] = None  # (hour_from, hour_to)

class HourlyPrediction(BaseModel):
    hour: int
    crowd_level: CrowdLevel
    wait_time_minutes: Optional[int] = None

class PredictionFactor(BaseModel):
    name: str
    impact: float  # -1.0 to 1.0 where positive means increases crowds
    description: str

class CrowdPredictionResponse(BaseModel):
    location: str
    date: date
    overall_crowd_level: CrowdLevel
    hourly_predictions: List[HourlyPrediction]
    factors: List[PredictionFactor]
    last_updated: datetime

class HistoricalDataPoint(BaseModel):
    date: date
    average_crowd_level: CrowdLevel
    peak_hours: List[int]
    total_visitors: Optional[int] = None

class CrowdHistoryResponse(BaseModel):
    location: str
    from_date: date
    to_date: date
    data_points: List[HistoricalDataPoint]
    trends: Optional[Dict[str, float]] = None  # e.g., {"weekday_avg": 0.7, "weekend_avg": 0.9}
