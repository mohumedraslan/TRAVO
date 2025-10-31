from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from .schemas import (
    DestinationRecommendationResponse, AttractionRecommendationResponse,
    RecommendationCategory, Season, BudgetLevel, Location,
    RecommendationRequest, PersonalizedRecommendationResponse
)
from .service_logic import (
    get_destination_recommendations, get_trending_destinations,
    get_similar_destinations, get_attraction_recommendations,
    get_personalized_recommendations, create_rule_based_recommendation
)

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/test")
async def test_route():
    """Test route to verify the recommendation service is working."""
    return {"message": "Recommendation service is working!"}


@router.get("/destinations", response_model=List[DestinationRecommendationResponse])
async def get_destinations(
    categories: Optional[List[RecommendationCategory]] = Query(None),
    budget_level: Optional[BudgetLevel] = None,
    season: Optional[Season] = None,
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0)
):
    """Get destination recommendations based on filters."""
    destinations, total = await get_destination_recommendations(
        categories=categories,
        budget_level=budget_level,
        season=season,
        limit=limit,
        offset=offset
    )
    
    return destinations


@router.get("/destinations/trending", response_model=List[DestinationRecommendationResponse])
async def get_trending(
    limit: int = Query(5, ge=1, le=20),
    offset: int = Query(0, ge=0)
):
    """Get trending destinations based on popularity score."""
    destinations, total = await get_trending_destinations(
        limit=limit,
        offset=offset
    )
    
    return destinations


@router.get("/destinations/{destination_id}/similar", response_model=List[DestinationRecommendationResponse])
async def get_similar(
    destination_id: str,
    limit: int = Query(5, ge=1, le=20)
):
    """Get destinations similar to the specified destination."""
    similar_destinations = await get_similar_destinations(
        destination_id=destination_id,
        limit=limit
    )
    
    if not similar_destinations:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    return similar_destinations


@router.get("/destinations/{destination_id}/attractions", response_model=List[AttractionRecommendationResponse])
async def get_attractions(
    destination_id: str,
    categories: Optional[List[RecommendationCategory]] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0)
):
    """Get attraction recommendations for a specific destination."""
    attractions, total = await get_attraction_recommendations(
        destination_id=destination_id,
        categories=categories,
        limit=limit,
        offset=offset
    )
    
    if not attractions:
        raise HTTPException(status_code=404, detail="Destination not found or no attractions available")
    
    return attractions


@router.post("/personalized", response_model=PersonalizedRecommendationResponse)
async def get_personalized(
    request: RecommendationRequest
):
    """Get personalized recommendations based on user preferences and history."""
    recommendations = await get_personalized_recommendations(request)
    
    if not recommendations.destinations:
        raise HTTPException(
            status_code=404,
            detail="Could not generate personalized recommendations with the provided parameters"
        )
    
    return recommendations


class RecommendationBody(BaseModel):
    interests: List[str]
    days: int = Field(2, ge=1, le=14)


@router.post("/recommend")
async def recommend_itinerary(
    request: RecommendationBody
):
    """Create a rule-based recommendation based on user interests and available time.
    
    Args:
        interests: List of user interests (e.g., "history", "culture", "nature")
        days: Number of days available for the trip (default: 2)
        
    Returns:
        JSON with recommended itinerary
    """
    if not request.interests:
        raise HTTPException(status_code=400, detail="At least one interest must be provided")
        
    if request.days < 1:
        raise HTTPException(status_code=400, detail="Days must be at least 1")
        
    itinerary = await create_rule_based_recommendation(request.interests, request.days)
    return itinerary
