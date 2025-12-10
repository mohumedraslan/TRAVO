from fastapi import APIRouter, UploadFile, File, HTTPException, status
from typing import Optional
import os
import tempfile
import shutil

# Import schemas and service logic
from .schemas import MonumentDetectionResponse, MonumentInfo, MonumentIdentificationResponse
from .deep_scan import deep_analyze_image

# Create router
router = APIRouter()

@router.get("/test")
async def test_vision_service():
    return {"status": "ok", "service": "vision_service"}

@router.post("/identify")
async def identify_monument_in_image(image: UploadFile = File(...)):
    """
    Primary monument identification endpoint.
    Uses Gemini 2.0 Flash for accurate identification.
    """
    if not image.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    try:
        # Read image bytes
        image_bytes = await image.read()
        
        # Call Gemini-powered vision analysis
        result = await deep_analyze_image(image_bytes)
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Vision analysis failed: {str(e)}"
        )

@router.post("/deep_scan")
async def deep_scan_endpoint(image: UploadFile = File(...)):
    """
    Deep analysis with more detailed response.
    Same as /identify but explicit for UI clarity.
    """
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    content = await image.read()
    result = await deep_analyze_image(content)
    return result

# Get information about a specific monument (legacy)
@router.get("/monument/{monument_id}")
async def get_monument_details(monument_id: str):
    # This would query a database in production
    return {"monument_id": monument_id, "status": "not_implemented"}
