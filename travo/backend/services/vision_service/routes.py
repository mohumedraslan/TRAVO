from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List, Optional
import os
import tempfile
import shutil
import logging

# Import schemas and new service logic
from .schemas import MonumentIdentificationResponse
from .new_service_logic import monument_service

# Create router
router = APIRouter()

logger = logging.getLogger(__name__)

# Test route
@router.get("/test")
async def test_vision_service():
    return {"status": "ok", "service": "vision_service"}

# Identify monument in an uploaded image
@router.post("/identify", response_model=MonumentIdentificationResponse)
async def identify_monument_in_image(image: UploadFile = File(...)):
    logger.info(f"Received request to identify monument in image: {image.filename}")
    try:
        if not image.content_type.startswith("image/"):
            logger.warning(f"Invalid file type uploaded: {image.content_type}")
            return JSONResponse(
                status_code=400,
                content={
                    "identified_monument": None,
                    "confidence": 0.0,
                    "monument_id": None,
                    "message": "Invalid file type. Please upload an image."
                }
            )

        # Read image data
        image_bytes = await image.read()
        
        # Identify the monument
        result = monument_service.identify_monument(image_bytes)
        logger.info(f"identify_monument returned: {result}")

        # Check if we have a valid identification
        if result.get("identified_monument") is None:
            return JSONResponse(
                status_code=404,
                content=result
            )

        return JSONResponse(
            status_code=200,
            content=result
        )

    except Exception as e:
        logger.error(f"An unexpected error occurred in identify_monument_in_image: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "identified_monument": None,
                "confidence": 0.0,
                "monument_id": None,
                "message": "Internal server error occurred"
            }
        )
