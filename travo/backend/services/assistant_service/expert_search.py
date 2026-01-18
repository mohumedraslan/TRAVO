import logging
import json
from ..storage_service.service_logic import get_supabase_client
from ..live_service.ollama_client import analyze_with_ollama

logger = logging.getLogger(__name__)

async def search_user_memories(query: str, user_id: str = None) -> dict:
    """
    Search User's Photos and Trips using SQL (ILIKE) and return structured results.
    """
    client = get_supabase_client()
    results = []
    
    # 1. Search Photos (Match AI Label or Location)
    # Note: local_uri often contains the filename which might have clues, but ai_label is best.
    try:
        photo_res = client.table("photos").select("*").eq("user_id", user_id).or_(f"ai_label.ilike.%{query}%,status.ilike.%{query}%").execute()
        for p in photo_res.data:
            results.append({
                "id": p.get("id"),
                "type": "photo",
                "title": p.get("ai_label") or "Untitled Photo",
                "subtitle": p.get("timestamp", "").split("T")[0],
                "image_url": p.get("remote_url")
            })
    except Exception as e:
        logger.warning(f"Photo search failed: {e}")

    # 2. Search Trips (Match Title)
    try:
        trip_res = client.table("trips").select("*").eq("user_id", user_id).ilike("title", f"%{query}%").execute()
        for t in trip_res.data:
            results.append({
                "id": t.get("id"),
                "type": "trip",
                "title": t.get("title"),
                "subtitle": f"Trip from {t.get('start_time', '').split('T')[0]}",
                # "image_url": "..." # Could fetch first photo of trip
            })
    except Exception as e:
        logger.warning(f"Trip search failed: {e}")

    # 3. (Optional) Local AI Summary / filtering
    # For now, just return raw results to be fast.
    
    return {
        "query": query,
        "results": results,
        "count": len(results)
    }
