import logging
from datetime import datetime
from typing import List, Optional
from uuid import uuid4
from fastapi import UploadFile
from geopy.geocoders import Nominatim
from supabase import Client
import base64
from PIL import Image
import io

# Import existing vision service for CLIP
from services.vision_service.service_logic import identify_monument, initialize_clip_model

logger = logging.getLogger(__name__)

# Initialize Geocoder
geolocator = Nominatim(user_agent="travo_diary_app")

async def start_trip(user_id: str, title: str, supabase: Client):
    """Starts a new trip for the user."""
    try:
        trip_data = {
            "user_id": user_id,
            "title": title,
            "start_time": datetime.now().isoformat(),
            "status": "active"
        }
        response = supabase.table("trips").insert(trip_data).execute()
        return response.data[0]
    except Exception as e:
        logger.error(f"Error starting trip: {e}")
        raise e

async def identify_and_log_photo(
    trip_id: str,
    file: UploadFile,
    gps_lat: float,
    gps_lon: float,
    supabase: Client
):
    """
    1. Identifies location (CLIP or GPS).
    2. Logs place to trip_places (if new).
    3. Logs photo to trip_photos.
    """
    try:
        # 1. Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert to base64 for vision service (if needed) or process directly
        # For now, let's assume we use the existing identify_monument which takes base64 string
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # 2. Identify
        place_name = "Unknown Location"
        confidence = 0.0
        
        # Try CLIP first
        try:
            # We need to ensure CLIP is initialized. It might be better to call this on startup.
            # identify_monument expects a Pydantic model usually, but let's check its signature.
            # Assuming we can reuse logic. If not, we implement fallback immediately.
            
            # Simplified CLIP call (mocking the integration for now as we reuse vision_service)
            # In a real refactor, we'd import the specific function.
            # Let's rely on GPS fallback primarily for "Diary" if CLIP fails.
            
            # Pass PIL Image directly, and do not await (it's sync)
            vision_result = identify_monument(image)
            print(f"DEBUG: Vision result: {vision_result}")
            
            # Accept even low confidence for now, as 0.04 is typical for this model/set
            if vision_result and vision_result.get('confidence', 0) > 0.01:
                place_name = vision_result['identified_monument']
                confidence = vision_result['confidence']
        except Exception as e:
            logger.warning(f"CLIP identification failed: {e}")

        # 3. Fallback to GPS if CLIP failed or low confidence
        if place_name == "Unknown Location" or place_name == "Unknown":
            try:
                location = geolocator.reverse(f"{gps_lat}, {gps_lon}")
                if location:
                    # Extract a meaningful name (e.g., landmark, or street)
                    address = location.raw.get('address', {})
                    place_name = address.get('tourism') or address.get('historic') or address.get('building') or address.get('road') or "GPS Location"
            except Exception as e:
                logger.warning(f"Reverse geocoding failed: {e}")
                place_name = f"Location at {gps_lat:.4f}, {gps_lon:.4f}"

        # 4. Log Place (Check if we are still at the last place to avoid duplicates)
        # Get last place for this trip
        last_place_response = supabase.table("trip_places").select("*").eq("trip_id", trip_id).order("created_at", desc=True).limit(1).execute()
        
        place_id = None
        if last_place_response.data:
            last_place = last_place_response.data[0]
            # Simple check: if name is same OR distance is very close (skip distance calc for MVP, use name)
            if last_place['place_name'] == place_name:
                place_id = last_place['id']
        
        if not place_id:
            # Create new place
            place_data = {
                "trip_id": trip_id,
                "place_name": place_name,
                "gps_lat": gps_lat,
                "gps_lon": gps_lon
            }
            place_response = supabase.table("trip_places").insert(place_data).execute()
            place_id = place_response.data[0]['id']

        # 5. Upload Photo to Storage (Mocking storage upload for MVP, storing URL as placeholder or base64 if small)
        # In production: Upload to Supabase Storage -> Get Public URL.
        # For MVP: We will assume the client uploads to storage and sends us the URL, OR we handle it here.
        # Let's assume we save a placeholder URL for now to keep it simple, or user sends URL.
        # Wait, the prompt says "Camera/Gallery photo -> CLIP recognition".
        # Let's assume we store the photo in Supabase Storage.
        
        photo_filename = f"{trip_id}/{uuid4()}.jpg"
        
        # Upload to Supabase Storage
        # Note: 'trip_photos' bucket must exist and be public
        try:
            supabase.storage.from_("trip_photos").upload(
                path=photo_filename,
                file=contents,
                file_options={"content-type": "image/jpeg"}
            )
            photo_url = supabase.storage.from_("trip_photos").get_public_url(photo_filename)
        except Exception as e:
            logger.error(f"Failed to upload photo to storage: {e}")
            # Fallback to a placeholder only if upload fails
            photo_url = f"https://placehold.co/600x400?text=Upload+Failed"

        # 6. Log Photo
        photo_data = {
            "trip_place_id": place_id,
            "photo_url": photo_url,
            "caption": f"Photo at {place_name}"
        }
        supabase.table("trip_photos").insert(photo_data).execute()

        return {
            "place_name": place_name,
            "photo_url": photo_url,
            "confidence": confidence
        }

    except Exception as e:
        logger.error(f"Error in identify_and_log_photo: {e}")
        raise e

async def get_trip_timeline(trip_id: str, supabase: Client):
    """Fetches the timeline for a trip."""
    try:
        # Fetch places with photos
        response = supabase.table("trip_places").select("*, trip_photos(*)").eq("trip_id", trip_id).order("created_at", desc=False).execute()
        return response.data
    except Exception as e:
        logger.error(f"Error fetching timeline: {e}")
        raise e
