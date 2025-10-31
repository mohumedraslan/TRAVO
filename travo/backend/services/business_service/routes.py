from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional

# Import schemas and service logic
from .schemas import BusinessListingResponse, BusinessDetailResponse, ReviewResponse, ReviewCreate
from .service_logic import get_businesses, get_business_by_id, get_reviews, create_review

# Create router
router = APIRouter()

# Test route
@router.get("/test")
async def test_business_service():
    return {"status": "ok", "service": "business_service"}

# Get businesses near a location
@router.get("/listings", response_model=List[BusinessListingResponse])
async def get_business_listings(
    latitude: float,
    longitude: float,
    radius: Optional[float] = 5.0,  # km
    category: Optional[str] = None,
    limit: Optional[int] = 20,
    offset: Optional[int] = 0
):
    businesses = await get_businesses(
        latitude=latitude,
        longitude=longitude,
        radius=radius,
        category=category,
        limit=limit,
        offset=offset
    )
    
    return businesses

# Get business details
@router.get("/business/{business_id}", response_model=BusinessDetailResponse)
async def get_business_detail(business_id: str):
    business = await get_business_by_id(business_id)
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    return business

# Get reviews for a business
@router.get("/business/{business_id}/reviews", response_model=List[ReviewResponse])
async def get_business_reviews(
    business_id: str,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0
):
    reviews = await get_reviews(business_id, limit, offset)
    
    return reviews

# Create a review for a business
@router.post("/business/{business_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def add_business_review(
    business_id: str,
    review: ReviewCreate
):
    # Check if business exists
    business = await get_business_by_id(business_id)
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    # Create the review
    new_review = await create_review(business_id, review)
    
    return new_review
