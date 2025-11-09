from fastapi import APIRouter, UploadFile, File, HTTPException, status, Body
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict
from pydantic import BaseModel
import os
import tempfile
import shutil
import logging
import base64

# Import the new landmark model
from models.landmark_hf import predict_landmark

# Create router
router = APIRouter()

logger = logging.getLogger(__name__)

class ImageIdentificationRequest(BaseModel):
    """Request model for image identification"""
    image: str  # Base64 encoded image

# Test route
@router.get("/test")
async def test_vision_service():
    return {"status": "ok", "service": "vision_service"}

# Identify monument in an uploaded image (multipart/form-data)
@router.post("/identify_upload")
async def identify_monument_upload(image: UploadFile = File(...)):
    """Identify monument from uploaded file"""
    logger.info(f"Received file upload: {image.filename}")
    try:
        if not image.content_type.startswith("image/"):
            logger.warning(f"Invalid file type: {image.content_type}")
            return JSONResponse(
                status_code=400,
                content={
                    "identified_monument": "Unknown",
                    "confidence": 0.0,
                    "monument_id": None,
                    "candidates": [],
                    "message": "Invalid file type. Please upload an image."
                }
            )

        # Read and encode image
        image_bytes = await image.read()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # Predict using the model
        result = predict_landmark(image_base64, top_k=3)
        logger.info(f"Prediction result: {result}")

        return JSONResponse(status_code=200, content=result)

    except Exception as e:
        logger.error(f"Error in identify_monument_upload: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "identified_monument": "Unknown",
                "confidence": 0.0,
                "monument_id": None,
                "candidates": [],
                "message": f"Error: {str(e)}"
            }
        )

# Identify monument from base64 image (JSON)
@router.post("/identify")
async def identify_monument(request: ImageIdentificationRequest):
    """Identify monument from base64 encoded image"""
    logger.info(f"Received base64 image identification request")
    try:
        # Predict using the model
        result = predict_landmark(request.image, top_k=3)
        logger.info(f"Prediction result: {result}")

        return JSONResponse(status_code=200, content=result)

    except Exception as e:
        logger.error(f"Error in identify_monument: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "identified_monument": "Unknown",
                "confidence": 0.0,
                "monument_id": None,
                "candidates": [],
                "message": f"Error: {str(e)}"
            }
        )
