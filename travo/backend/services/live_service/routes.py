from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from .schemas import PulseResponse
from .service_logic import analyze_pulse

router = APIRouter()

@router.post("/pulse", response_model=PulseResponse)
async def live_pulse(
    image: UploadFile = File(...),
    lat: Optional[float] = Form(None),
    lon: Optional[float] = Form(None)
):
    """
    Receive a live camera pulse (frame) and return immediate context/tips.
    Intentionally lightweight.
    """
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Invalid image")
    
    content = await image.read()
    
    # Process
    result = await analyze_pulse(content, lat, lon)
    
    return result
