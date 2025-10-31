from fastapi import APIRouter, UploadFile, File, HTTPException, status
from typing import List, Optional
import os
import tempfile
import shutil

# Import schemas and service logic
from .schemas import MonumentDetectionResponse, MonumentInfo, MonumentIdentificationResponse
from .service_logic import detect_monuments, get_monument_info, identify_monument

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


# Identify monument in an uploaded image
@router.post("/identify", response_model=MonumentIdentificationResponse)
async def identify_monument_in_image(image: UploadFile = File(...)):
    # Validate file type
    if not image.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Create a temporary file to store the uploaded image
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        # Copy the uploaded file to the temporary file
        shutil.copyfileobj(image.file, temp_file)
        temp_file_path = temp_file.name
    
    try:
        # Call the identify_monument function
        result = identify_monument(temp_file_path)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error identifying monument: {str(e)}"
        )
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
