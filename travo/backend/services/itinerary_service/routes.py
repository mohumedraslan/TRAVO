from fastapi import APIRouter, HTTPException, Query, Depends, Body
from typing import List, Optional
from datetime import datetime

# Import service logic and schemas
from .schemas import (
    ItineraryCreate,
    ItineraryResponse,
    ItineraryUpdate,
    ItineraryDayResponse,
    ItineraryActivityCreate,
    ItineraryActivityResponse,
    ItineraryActivityUpdate,
    ItineraryShareResponse
)
from .service_logic import (
    create_itinerary,
    get_itineraries,
    get_itinerary_by_id,
    update_itinerary,
    delete_itinerary,
    add_activity_to_itinerary,
    update_activity,
    delete_activity,
    reorder_activities,
    share_itinerary,
    get_shared_itinerary,
    generate_itinerary
)

# Create router
router = APIRouter(prefix="/itinerary", tags=["itinerary"])


@router.get("/test")
async def test_route():
    """Test route to verify the itinerary service is working."""
    return {"message": "Itinerary service is working!"}


@router.post("/", response_model=ItineraryResponse)
async def create_new_itinerary(itinerary: ItineraryCreate):
    """Create a new travel itinerary."""
    try:
        result = await create_itinerary(itinerary)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[ItineraryResponse])
async def list_itineraries(
    user_id: str,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sort_by: Optional[str] = Query(None, enum=["created_at", "start_date", "title"]),
    sort_order: Optional[str] = Query("desc", enum=["asc", "desc"])
):
    """Get all itineraries for a user with pagination and sorting."""
    try:
        itineraries = await get_itineraries(
            user_id=user_id,
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            sort_order=sort_order
        )
        return itineraries
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{itinerary_id}", response_model=ItineraryResponse)
async def get_itinerary(itinerary_id: str):
    """Get a specific itinerary by ID."""
    itinerary = await get_itinerary_by_id(itinerary_id)
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return itinerary


@router.put("/{itinerary_id}", response_model=ItineraryResponse)
async def update_itinerary_details(itinerary_id: str, itinerary_update: ItineraryUpdate):
    """Update an existing itinerary."""
    updated_itinerary = await update_itinerary(itinerary_id, itinerary_update)
    if not updated_itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return updated_itinerary


@router.delete("/{itinerary_id}")
async def remove_itinerary(itinerary_id: str):
    """Delete an itinerary."""
    success = await delete_itinerary(itinerary_id)
    if not success:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return {"message": "Itinerary deleted successfully"}


@router.post("/{itinerary_id}/activities", response_model=ItineraryActivityResponse)
async def add_activity(itinerary_id: str, activity: ItineraryActivityCreate):
    """Add a new activity to an itinerary."""
    try:
        result = await add_activity_to_itinerary(itinerary_id, activity)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{itinerary_id}/activities/{activity_id}", response_model=ItineraryActivityResponse)
async def update_activity_details(itinerary_id: str, activity_id: str, activity_update: ItineraryActivityUpdate):
    """Update an existing activity in an itinerary."""
    updated_activity = await update_activity(itinerary_id, activity_id, activity_update)
    if not updated_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return updated_activity


@router.delete("/{itinerary_id}/activities/{activity_id}")
async def remove_activity(itinerary_id: str, activity_id: str):
    """Delete an activity from an itinerary."""
    success = await delete_activity(itinerary_id, activity_id)
    if not success:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"message": "Activity deleted successfully"}


@router.post("/{itinerary_id}/activities/reorder")
async def reorder_itinerary_activities(
    itinerary_id: str, 
    activity_ids: List[str] = Body(..., embed=True)
):
    """Reorder activities within an itinerary."""
    success = await reorder_activities(itinerary_id, activity_ids)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to reorder activities")
    return {"message": "Activities reordered successfully"}


@router.post("/{itinerary_id}/share", response_model=ItineraryShareResponse)
async def share_itinerary_with_others(itinerary_id: str):
    """Generate a shareable link for an itinerary."""
    share_info = await share_itinerary(itinerary_id)
    if not share_info:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return share_info


@router.get("/shared/{share_id}", response_model=ItineraryResponse)
async def get_shared_itinerary_by_id(share_id: str):
    """Get a shared itinerary using a share ID."""
    itinerary = await get_shared_itinerary(share_id)
    if not itinerary:
        raise HTTPException(status_code=404, detail="Shared itinerary not found or expired")
    return itinerary


@router.post("/generate", response_model=ItineraryResponse)
async def generate_ai_itinerary(
    destination: str = Body(...),
    start_date: datetime = Body(...),
    end_date: datetime = Body(...),
    preferences: List[str] = Body(default=[]),
    budget_level: Optional[str] = Body(None, enum=["budget", "moderate", "luxury"]),
    user_id: str = Body(...)
):
    """Generate an AI-powered itinerary based on user preferences."""
    try:
        itinerary = await generate_itinerary(
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            preferences=preferences,
            budget_level=budget_level,
            user_id=user_id
        )
        return itinerary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
