import uuid
import random
from datetime import datetime, time
from typing import List, Dict, Any, Optional
import re
from urllib.parse import quote

# Constants
SHARE_BASE_URL = "https://travo.app/share/"

def generate_itinerary_id() -> str:
    """Generate a unique ID for an itinerary."""
    return f"itin_{uuid.uuid4().hex[:8]}"

def generate_activity_id() -> str:
    """Generate a unique ID for an activity."""
    return f"act_{uuid.uuid4().hex[:8]}"

def generate_share_id() -> str:
    """Generate a unique ID for a share link."""
    return f"share_{uuid.uuid4().hex[:8]}"

def generate_share_url(share_id: str) -> str:
    """Generate a shareable URL for an itinerary."""
    return f"{SHARE_BASE_URL}{share_id}"

def calculate_itinerary_stats(activities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate statistics for an itinerary based on its activities."""
    if not activities:
        return {
            "total_activities": 0,
            "total_cost": 0.0,
            "currency": "USD",
            "activity_types": {},
            "daily_costs": {},
            "avg_cost_per_day": 0.0
        }
    
    # Initialize stats
    stats = {
        "total_activities": len(activities),
        "total_cost": 0.0,
        "currency": "USD",  # Default currency
        "activity_types": {},
        "daily_costs": {},
        "avg_cost_per_day": 0.0
    }
    
    # Determine the most common currency
    currency_counts = {}
    for activity in activities:
        if "currency" in activity and activity["currency"]:
            currency = activity["currency"]
            currency_counts[currency] = currency_counts.get(currency, 0) + 1
    
    if currency_counts:
        stats["currency"] = max(currency_counts.items(), key=lambda x: x[1])[0]
    
    # Calculate stats
    for activity in activities:
        # Count activity types
        activity_type = activity.get("activity_type", "other")
        stats["activity_types"][activity_type] = stats["activity_types"].get(activity_type, 0) + 1
        
        # Sum costs (assuming same currency for simplicity)
        if "cost" in activity and activity["cost"]:
            if activity.get("currency") == stats["currency"]:
                stats["total_cost"] += activity["cost"]
            # In a real implementation, we would convert currencies
        
        # Track daily costs
        day_index = activity.get("day_index", 0)
        if "cost" in activity and activity["cost"]:
            if activity.get("currency") == stats["currency"]:
                stats["daily_costs"][day_index] = stats["daily_costs"].get(day_index, 0.0) + activity["cost"]
    
    # Calculate average cost per day
    if stats["daily_costs"]:
        stats["avg_cost_per_day"] = stats["total_cost"] / len(stats["daily_costs"])
    
    return stats

def format_time_range(start_time: time, end_time: time) -> str:
    """Format a time range for display."""
    start_format = start_time.strftime("%I:%M %p")
    end_format = end_time.strftime("%I:%M %p")
    return f"{start_format} - {end_format}"

def validate_date_range(start_date: datetime, end_date: datetime) -> bool:
    """Validate that end_date is not before start_date."""
    return end_date >= start_date

def sanitize_itinerary_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize user input for itinerary data to prevent injection attacks."""
    sanitized = {}
    
    for key, value in data.items():
        if isinstance(value, str):
            # Remove potentially dangerous HTML/script tags
            value = re.sub(r'<script.*?>.*?</script>', '', value, flags=re.DOTALL)
            value = re.sub(r'<.*?>', '', value)
            sanitized[key] = value
        elif isinstance(value, dict):
            sanitized[key] = sanitize_itinerary_data(value)
        elif isinstance(value, list):
            if all(isinstance(item, dict) for item in value):
                sanitized[key] = [sanitize_itinerary_data(item) for item in value]
            else:
                sanitized[key] = value
        else:
            sanitized[key] = value
    
    return sanitized

def is_activity_overlapping(new_start: time, new_end: time, existing_activities: List[Dict[str, Any]]) -> bool:
    """Check if a new activity's time overlaps with existing activities."""
    for activity in existing_activities:
        existing_start = activity.get("start_time")
        existing_end = activity.get("end_time")
        
        if not existing_start or not existing_end:
            continue
        
        # Check for overlap
        if (new_start < existing_end and new_end > existing_start):
            return True
    
    return False

def get_activity_duration_minutes(start_time: time, end_time: time) -> int:
    """Calculate the duration of an activity in minutes."""
    start_minutes = start_time.hour * 60 + start_time.minute
    end_minutes = end_time.hour * 60 + end_time.minute
    
    # Handle activities that span midnight
    if end_minutes < start_minutes:
        end_minutes += 24 * 60
    
    return end_minutes - start_minutes

def format_itinerary_for_sharing(itinerary: Dict[str, Any]) -> Dict[str, Any]:
    """Format an itinerary for sharing, removing sensitive information."""
    # Create a copy to avoid modifying the original
    shared_itinerary = dict(itinerary)
    
    # Remove user-specific information
    if "user_id" in shared_itinerary:
        del shared_itinerary["user_id"]
    
    # Add a shared flag
    shared_itinerary["is_shared"] = True
    
    return shared_itinerary

def encode_itinerary_for_url(itinerary_id: str) -> str:
    """Encode an itinerary ID for use in a URL."""
    return quote(itinerary_id)

def suggest_nearby_activities(location: Dict[str, Any], radius_km: float = 5.0) -> List[Dict[str, Any]]:
    """Suggest nearby activities based on a location (mock implementation)."""
    # In a real implementation, this would query a database or external API
    # for attractions, restaurants, etc. near the given coordinates
    
    # Mock data for demonstration
    nearby = [
        {
            "title": "Local Restaurant",
            "description": "Popular local dining spot",
            "activity_type": "RESTAURANT",
            "distance_km": round(random.uniform(0.1, radius_km), 1),
            "rating": round(random.uniform(3.5, 5.0), 1)
        },
        {
            "title": "Tourist Attraction",
            "description": "Must-see local landmark",
            "activity_type": "ATTRACTION",
            "distance_km": round(random.uniform(0.1, radius_km), 1),
            "rating": round(random.uniform(3.5, 5.0), 1)
        },
        {
            "title": "Shopping Center",
            "description": "Local shopping mall with various stores",
            "activity_type": "SHOPPING",
            "distance_km": round(random.uniform(0.1, radius_km), 1),
            "rating": round(random.uniform(3.5, 5.0), 1)
        }
    ]
    
    return nearby

def optimize_itinerary_route(activities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Optimize the route between activities to minimize travel time (mock implementation)."""
    # In a real implementation, this would use a routing algorithm
    # to optimize the order of activities based on their locations
    
    # For this mock implementation, we'll just sort by start_time
    return sorted(activities, key=lambda x: x.get("start_time", time(0, 0)))

def calculate_travel_time(origin: Dict[str, Any], destination: Dict[str, Any]) -> int:
    """Calculate estimated travel time in minutes between two locations (mock implementation)."""
    # In a real implementation, this would use a routing API
    # to get the actual travel time based on mode of transportation
    
    # Mock implementation - random time between 10 and 60 minutes
    return random.randint(10, 60)

def generate_itinerary_summary(itinerary: Dict[str, Any]) -> str:
    """Generate a text summary of an itinerary."""
    summary = f"Trip to {itinerary.get('destination', 'Unknown')}\n"
    summary += f"Dates: {itinerary.get('start_date').strftime('%b %d')} - {itinerary.get('end_date').strftime('%b %d, %Y')}\n"
    summary += f"Duration: {(itinerary.get('end_date') - itinerary.get('start_date')).days + 1} days\n"
    
    if itinerary.get('total_activities'):
        summary += f"Activities: {itinerary.get('total_activities')}\n"
    
    if itinerary.get('total_cost'):
        summary += f"Estimated cost: {itinerary.get('total_cost')} {itinerary.get('currency', 'USD')}\n"
    
    return summary
