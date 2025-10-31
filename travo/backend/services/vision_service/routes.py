from fastapi import APIRouter, UploadFile, File, HTTPException, status
from typing import List, Optional

# Import schemas and service logic
from .schemas import MonumentDetectionResponse, MonumentInfo
from .service_logic import detect_monuments, get_monument_info

# Create router
router = APIRouter()

# Test route
@router.get("/test")
async def test_vision_service():
    return {"status": "ok", "service": "vision_service"}

# Upload image and detect monuments
@router.post("/detect", response_model=MonumentDetectionResponse)
async def detect_monuments_in_image(
    image: UploadFile = File(...),
    confidence_threshold: Optional[float] = 0.5
):
    # Validate file type
    if not image.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Read image content
    image_content = await image.read()
    
    # Call monument detection function
    detection_result = await detect_monuments(image_content, confidence_threshold)
    
    return detection_result

# Get information about a specific monument
@router.get("/monument/{monument_id}", response_model=MonumentInfo)
async def get_monument_details(monument_id: str):
    monument = await get_monument_info(monument_id)
    
    if not monument:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monument not found"
        )
    
    return monument
