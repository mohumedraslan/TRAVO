import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import math
import re

# Generate a unique business ID
def generate_business_id() -> str:
    """Generate a unique business ID."""
    return f"bus_{uuid.uuid4().hex[:8]}"

# Generate a unique review ID
def generate_review_id() -> str:
    """Generate a unique review ID."""
    return f"rev_{uuid.uuid4().hex[:8]}"

# Format business hours for display
def format_business_hours(hours: Dict[str, str]) -> str:
    """Format business hours for display."""
    if not hours:
        return "Hours not available"
    
    formatted_hours = []
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    
    for day in days:
        if day in hours and hours[day]:
            day_name = day.capitalize()
            formatted_hours.append(f"{day_name}: {hours[day]}")
        else:
            day_name = day.capitalize()
            formatted_hours.append(f"{day_name}: Closed")
    
    return "\n".join(formatted_hours)

# Calculate business rating statistics
def calculate_rating_stats(reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate rating statistics from a list of reviews."""
    if not reviews:
        return {
            "average": 0.0,
            "count": 0,
            "distribution": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
        }
    
    total = 0
    distribution = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
    
    for review in reviews:
        rating = review.get("rating", 0)
        total += rating
        
        # Round to nearest integer for distribution
        rating_key = str(round(rating))
        if rating_key in distribution:
            distribution[rating_key] += 1
    
    average = total / len(reviews)
    
    return {
        "average": round(average, 1),
        "count": len(reviews),
        "distribution": distribution
    }

# Sanitize and validate business data
def sanitize_business_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize and validate business data."""
    # Make a copy to avoid modifying the original
    sanitized = dict(data)
    
    # Sanitize text fields
    for field in ["name", "description", "phone", "email", "address", "city", "state", "country", "postal_code"]:
        if field in sanitized and sanitized[field]:
            # Remove any HTML tags
            sanitized[field] = re.sub(r'<[^>]*>', '', str(sanitized[field]))
            # Trim whitespace
            sanitized[field] = sanitized[field].strip()
    
    # Validate coordinates
    if "latitude" in sanitized:
        try:
            lat = float(sanitized["latitude"])
            if lat < -90 or lat > 90:
                sanitized["latitude"] = 0.0
        except (ValueError, TypeError):
            sanitized["latitude"] = 0.0
    
    if "longitude" in sanitized:
        try:
            lon = float(sanitized["longitude"])
            if lon < -180 or lon > 180:
                sanitized["longitude"] = 0.0
        except (ValueError, TypeError):
            sanitized["longitude"] = 0.0
    
    # Validate rating
    if "rating" in sanitized:
        try:
            rating = float(sanitized["rating"])
            if rating < 0 or rating > 5:
                sanitized["rating"] = 0.0
            else:
                sanitized["rating"] = round(rating, 1)
        except (ValueError, TypeError):
            sanitized["rating"] = 0.0
    
    return sanitized

# Check if a business is open at a specific time
def is_business_open(hours: Dict[str, str], check_time: Optional[datetime] = None) -> bool:
    """Check if a business is open at a specific time."""
    if not hours:
        return False
    
    if check_time is None:
        check_time = datetime.utcnow()
    
    # Get day of week (0 = Monday, 6 = Sunday)
    day_idx = check_time.weekday()
    day_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    day_name = day_names[day_idx]
    
    # Check if hours exist for this day
    if day_name not in hours or not hours[day_name]:
        return False
    
    # Parse hours string (format: "HH:MM-HH:MM")
    hours_str = hours[day_name]
    
    # Handle 24-hour businesses
    if hours_str == "00:00-24:00":
        return True
    
    # Parse regular hours
    try:
        open_close = hours_str.split("-")
        if len(open_close) != 2:
            return False
        
        open_time = datetime.strptime(open_close[0], "%H:%M").time()
        close_time = datetime.strptime(open_close[1], "%H:%M").time()
        current_time = check_time.time()
        
        # Handle overnight hours (close time is earlier than open time)
        if close_time < open_time:
            return current_time >= open_time or current_time <= close_time
        else:
            return open_time <= current_time <= close_time
    except ValueError:
        return False
