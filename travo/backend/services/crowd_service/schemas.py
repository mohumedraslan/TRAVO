from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, time


class CrowdLevel(str, Enum):
    """Enum for crowd level prediction."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class CrowdPredictionRequest(BaseModel):
    """Request model for crowd prediction."""
    monument_id: str = Field(..., description="ID of the monument")
    month: int = Field(..., ge=1, le=12, description="Month (1-12)")
    day: int = Field(..., ge=1, le=31, description="Day of month (1-31)")
    time: str = Field(..., description="Time of day in HH:MM format")
    
    class Config:
        json_schema_extra = {
            "example": {
                "monument_id": "pyr_giza",
                "month": 7,
                "day": 15,
                "time": "14:30"
            }
        }


class CrowdPredictionResponse(BaseModel):
    """Response model for crowd prediction."""
    monument_id: str
    prediction_time: datetime
    crowd_level: CrowdLevel
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score of prediction")
    wait_time_minutes: Optional[int] = Field(None, description="Estimated wait time in minutes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "monument_id": "pyr_giza",
                "prediction_time": "2023-07-15T14:30:00",
                "crowd_level": "High",
                "confidence": 0.85,
                "wait_time_minutes": 45
            }
        }


class CrowdHistoricalRequest(BaseModel):
    """Request model for historical crowd data."""
    monument_id: str
    start_date: datetime
    end_date: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "monument_id": "pyr_giza",
                "start_date": "2023-01-01T00:00:00",
                "end_date": "2023-01-31T23:59:59"
            }
        }


class CrowdHistoricalDataPoint(BaseModel):
    """Data point for historical crowd data."""
    timestamp: datetime
    crowd_level: CrowdLevel


class CrowdHistoricalResponse(BaseModel):
    """Response model for historical crowd data."""
    monument_id: str
    data_points: list[CrowdHistoricalDataPoint]
