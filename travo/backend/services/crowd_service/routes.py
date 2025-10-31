from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from datetime import date, datetime

# Import schemas and service logic
from .schemas import CrowdPredictionResponse, LocationRequest
from .service_logic import get_crowd_prediction, get_crowd_history

# Create router
router = APIRouter()

# Test route
@router.get("/test")
async def test_crowd_service():
    return {"status": "ok", "service": "crowd_service"}

# Get crowd prediction for a location
@router.post("/prediction", response_model=CrowdPredictionResponse)
async def predict_crowd(request: LocationRequest):
    prediction = await get_crowd_prediction(
        location=request.location,
        date=request.date,
        time_range=request.time_range
    )
    return prediction

# Get crowd prediction for a location (GET method alternative)
@router.get("/prediction", response_model=CrowdPredictionResponse)
async def get_crowd_prediction_for_location(
    location: str,
    prediction_date: Optional[date] = Query(None),
    time_from: Optional[int] = Query(None, ge=0, le=23),
    time_to: Optional[int] = Query(None, ge=0, le=23)
):
    # Use current date if not provided
    if not prediction_date:
        prediction_date = date.today()
    
    # Default to full day if time range not provided
    time_range = None
    if time_from is not None and time_to is not None:
        time_range = (time_from, time_to)
    
    prediction = await get_crowd_prediction(
        location=location,
        date=prediction_date,
        time_range=time_range
    )
    return prediction

# Get historical crowd data
@router.get("/history")
async def get_historical_crowd_data(
    location: str,
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None)
):
    # Default to last 30 days if dates not provided
    if not to_date:
        to_date = date.today()
    
    if not from_date:
        # 30 days before to_date
        from_date = date(to_date.year, to_date.month, to_date.day)
        from_date = date.fromordinal(from_date.toordinal() - 30)
    
    history = await get_crowd_history(location, from_date, to_date)
    return history
