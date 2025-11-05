from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime

from .schemas import (
    CrowdPredictionRequest,
    CrowdPredictionResponse,
    CrowdHistoricalRequest,
    CrowdHistoricalResponse,
    CrowdHistoricalDataPoint,
    CrowdLevel
)
from .service_logic import predict_crowd_level

# Create router
router = APIRouter(prefix="/crowd", tags=["crowd"])


@router.post("/predict", response_model=CrowdPredictionResponse)
async def predict_crowd(request: CrowdPredictionRequest):
    """Predict crowd levels for a monument at a specific time."""
    try:
        # Validate day based on month
        days_in_month = {
            1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
            7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }
        
        if request.day > days_in_month.get(request.month, 31):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid day {request.day} for month {request.month}"
            )
        
        # Validate time format
        try:
            hour, minute = map(int, request.time.split(':'))
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                raise ValueError("Invalid time values")
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid time format. Use HH:MM format (e.g., 14:30)"
            )
        
        # Get prediction
        result = predict_crowd_level(request)
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error predicting crowd level: {str(e)}"
        )


@router.get("/monuments", response_model=List[str])
async def get_supported_monuments():
    """Get list of monuments supported by the crowd prediction service."""
    # This would typically come from a database
    # For now, return a static list of supported monuments
    return [
        "pyr_giza",
        "sphinx",
        "luxor",
        "karnak",
        "abu_simbel",
        "valley_kings",
        "philae",
        "hatshepsut"
    ]


@router.post("/historical", response_model=CrowdHistoricalResponse)
async def get_historical_data(request: CrowdHistoricalRequest):
    """Get historical crowd data for a monument."""
    # This would typically fetch data from a database
    # For now, generate synthetic historical data
    
    # Validate date range
    if request.end_date < request.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date must be after start date"
        )
    
    # Generate synthetic data points
    # In a real implementation, this would query a database
    import random
    from datetime import timedelta
    
    data_points = []
    current_date = request.start_date
    
    while current_date <= request.end_date:
        # Generate a data point every 3 hours between 8AM and 8PM
        for hour in range(8, 21, 3):
            # Skip some points randomly to make data look more realistic
            if random.random() < 0.2:
                continue
                
            timestamp = current_date.replace(hour=hour, minute=0, second=0)
            
            # Determine crowd level based on time of day and some randomness
            rand_val = random.random()
            if hour in (10, 11, 14, 15):  # Peak hours
                crowd_level = CrowdLevel.HIGH if rand_val < 0.7 else CrowdLevel.MEDIUM
            elif hour in (8, 9, 16, 17):  # Moderate hours
                crowd_level = CrowdLevel.MEDIUM if rand_val < 0.6 else \
                             (CrowdLevel.HIGH if rand_val < 0.8 else CrowdLevel.LOW)
            else:  # Off-peak hours
                crowd_level = CrowdLevel.LOW if rand_val < 0.6 else CrowdLevel.MEDIUM
            
            data_points.append(CrowdHistoricalDataPoint(
                timestamp=timestamp,
                crowd_level=crowd_level
            ))
        
        # Move to next day
        current_date += timedelta(days=1)
    
    return CrowdHistoricalResponse(
        monument_id=request.monument_id,
        data_points=data_points
    )
