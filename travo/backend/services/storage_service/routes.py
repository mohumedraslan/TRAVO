from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional

from .service_logic import upload_photo, list_user_photos, delete_photo

router = APIRouter()

@router.get("/test")
async def test_storage():
    return {"status": "ok", "service": "storage_service"}

@router.post("/upload")
async def upload_photo_endpoint(
    image: UploadFile = File(...),
    user_id: str = Form("anonymous"),
    trip_id: Optional[str] = Form(None)
):
    """Upload a photo to storage."""
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    content = await image.read()
    
    # Determine file extension
    ext = image.filename.split('.')[-1] if image.filename else 'jpg'
    
    result = await upload_photo(content, user_id, trip_id, ext)
    return result

@router.get("/photos/{user_id}")
async def get_user_photos(user_id: str, trip_id: Optional[str] = None):
    """Get all photos for a user."""
    photos = await list_user_photos(user_id, trip_id)
    return {"photos": photos, "count": len(photos)}

@router.delete("/photos")
async def delete_photo_endpoint(path: str):
    """Delete a photo."""
    success = await delete_photo(path)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete photo")
    return {"deleted": True, "path": path}
