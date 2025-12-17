import os
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Supabase settings
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL") or "https://mvqljubjlufjyyktsljn.supabase.co"
# Prefer Service Role Key for backend operations (to bypass RLS)
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

BUCKET_NAME = "trip_photos"

_supabase_client = None

def get_supabase_client():
    """Get Supabase client instance."""
    global _supabase_client
    
    if _supabase_client:
        return _supabase_client
    
    if not SUPABASE_KEY:
        logger.error("No Supabase key found! processing will fail.")
        # Fallback to the hardcoded anon key if absolutely necessary, but warn
        # (This section is effectively removed/replaced by the env var logic)
    
    try:
        from supabase import create_client
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Log which key type we are using (safely)
        key_type = "SERVICE_ROLE (Admin)" if "service_role" in str(os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")) else "ANON (Public)"
        logger.info(f"Supabase connected: {SUPABASE_URL} using {key_type} key")
        
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
        base_path = f"{user_id}/{trip_id}" if trip_id else user_id
        
        # 1. List items in the base path
        response = client.storage.from_(BUCKET_NAME).list(base_path)
        
        photos = []
        
        # Helper to process a list of items and add to photos
        def process_items(items, current_path):
            for item in items:
                # If it has an ID, it's a file
                if item.get('id'):
                    file_path = f"{current_path}/{item['name']}"
                    public_url = client.storage.from_(BUCKET_NAME).get_public_url(file_path)
                    photos.append({
                        "name": item['name'],
                        "path": file_path,
                        "url": public_url,
                        "created_at": item.get('created_at')
                    })
        
        process_items(response, base_path)

        # 2. If we are at the root (no trip_id), also check "general" folder specifically
        # (This is where untripped photos go)
        if not trip_id:
            try:
                general_path = f"{user_id}/general"
                gen_response = client.storage.from_(BUCKET_NAME).list(general_path)
                process_items(gen_response, general_path)
            except Exception as e:
                # Ignore if general folder doesn't exist
                logger.warning(f"Could not list general folder: {e}")

        # 3. Handle strict recursion if needed later, but this covers the current structure
        
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
