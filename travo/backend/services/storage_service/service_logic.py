import os
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Hardcoded Supabase credentials (env loading broken)
SUPABASE_URL = "https://mvqljubjlufjyyktsljn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im12cWxqdWJqbHVmanl5a3RzbGpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0MTQwMjksImV4cCI6MjA3Nzk5MDAyOX0._6sCVs20oYzLUNfyYqlx54ZnuwoaamiCI_9SuSt1crA"

BUCKET_NAME = "trip_photos"

_supabase_client = None

def get_supabase_client():
    """Get Supabase client instance."""
    global _supabase_client
    
    if _supabase_client:
        return _supabase_client
    
    try:
        from supabase import create_client
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info(f"Supabase connected: {SUPABASE_URL}")
        return _supabase_client
    except ImportError:
        raise ValueError("Supabase library not installed. Run: pip install supabase")

async def upload_photo(
    image_bytes: bytes,
    user_id: str = "anonymous",
    trip_id: str = None,
    file_extension: str = "jpg"
) -> dict:
    """Upload a photo to Supabase Storage."""
    try:
        client = get_supabase_client()
        
        photo_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if trip_id:
            path = f"{user_id}/{trip_id}/{timestamp}_{photo_id}.{file_extension}"
        else:
            path = f"{user_id}/general/{timestamp}_{photo_id}.{file_extension}"
        
        response = client.storage.from_(BUCKET_NAME).upload(
            path,
            image_bytes,
            {"content-type": f"image/{file_extension}"}
        )
        
        public_url = client.storage.from_(BUCKET_NAME).get_public_url(path)
        
        logger.info(f"Photo uploaded: {path}")
        
        return {
            "photo_id": photo_id,
            "storage_path": path,
            "public_url": public_url,
            "uploaded_at": datetime.utcnow().isoformat(),
            "bucket": BUCKET_NAME
        }
        
    except Exception as e:
        logger.error(f"Photo upload failed: {e}")
        raise

async def list_user_photos(user_id: str, trip_id: str = None) -> list:
    """List photos for a user/trip."""
    try:
        client = get_supabase_client()
        path = f"{user_id}/{trip_id}" if trip_id else user_id
        
        response = client.storage.from_(BUCKET_NAME).list(path)
        
        photos = []
        for item in response:
            if not item.get('id'):
                continue
            file_path = f"{path}/{item['name']}"
            public_url = client.storage.from_(BUCKET_NAME).get_public_url(file_path)
            photos.append({
                "name": item['name'],
                "path": file_path,
                "url": public_url,
                "created_at": item.get('created_at')
            })
        
        return photos
        
    except Exception as e:
        logger.error(f"Failed to list photos: {e}")
        return []

async def delete_photo(path: str) -> bool:
    """Delete a photo from storage."""
    try:
        client = get_supabase_client()
        client.storage.from_(BUCKET_NAME).remove([path])
        logger.info(f"Photo deleted: {path}")
        return True
    except Exception as e:
        logger.error(f"Failed to delete photo: {e}")
        return False
