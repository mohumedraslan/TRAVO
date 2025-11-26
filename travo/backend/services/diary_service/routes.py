from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Header
from typing import Optional
from services.diary_service import logic
from utils.supabase_client import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client, Client

router = APIRouter(prefix="/api/diary", tags=["diary"])

def get_supabase_client(authorization: Optional[str] = Header(None)) -> Client:
    """
    Creates a Supabase client authenticated with the user's token.
    This ensures RLS policies work correctly.
    """
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    if authorization:
        # Extract token from "Bearer <token>"
        token = authorization.replace("Bearer ", "")
        try:
            # Try setting the session directly. 
            # We pass a dummy refresh token because we only have the access token.
            # This is sufficient for RLS if the access token is valid.
            client.auth.set_session(access_token=token, refresh_token="dummy")
        except Exception as e:
            print(f"Error setting session: {e}")
            # Fallback to setting header directly
            client.postgrest.auth(token)
            
        # Debug logging
        print(f"DEBUG: Auth token set. Token starts with: {token[:10]}...")
    else:
        print("DEBUG: No Authorization header received.")
        
    return client

@router.post("/trips/start")
async def start_trip(
    user_id: str = Form(...), 
    title: str = Form(...),
    supabase: Client = Depends(get_supabase_client)
):
    try:
        result = await logic.start_trip(user_id, title, supabase)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/identify")
async def identify_photo(
    trip_id: str = Form(...),
    file: UploadFile = File(...),
    gps_lat: float = Form(...),
    gps_lon: float = Form(...),
    supabase: Client = Depends(get_supabase_client)
):
    try:
        result = await logic.identify_and_log_photo(trip_id, file, gps_lat, gps_lon, supabase)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trips/{trip_id}/timeline")
async def get_timeline(
    trip_id: str,
    supabase: Client = Depends(get_supabase_client)
):
    try:
        result = await logic.get_trip_timeline(trip_id, supabase)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
