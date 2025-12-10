from fastapi import APIRouter

router = APIRouter()

@router.get("/summary")
async def get_analytics_summary():
    """Return a mock analytics summary for the dashboard."""
    return {
        "destinations_count": 12,
        "attractions_count": 45,
        "users_count": 1024,
        "trips_logged_today": 8,
        "popular_destination": "Cairo, Egypt"
    }

@router.get("/recent-activity")
async def get_recent_activity():
    """Return mock recent activity for the dashboard."""
    return {
        "items": [
            {"type": "photo", "user": "ali", "monument": "Pyramids of Giza", "time": "2 min ago"},
            {"type": "trip", "user": "sara", "destination": "Luxor", "time": "15 min ago"},
            {"type": "photo", "user": "omar", "monument": "Karnak Temple", "time": "1 hour ago"}
        ]
    }
