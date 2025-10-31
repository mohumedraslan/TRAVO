from typing import Dict, List, Tuple
from datetime import date, datetime, timedelta

def is_holiday(check_date: date) -> bool:
    """Check if a date is a holiday
    
    This is a simplified implementation. In a production system,
    this would use a more comprehensive holiday calendar, possibly
    from an external API or database.
    """
    # Common US holidays (simplified)
    holidays = [
        # New Year's Day
        date(check_date.year, 1, 1),
        # Independence Day
        date(check_date.year, 7, 4),
        # Thanksgiving (4th Thursday in November)
        date(check_date.year, 11, 1) + timedelta(days=(24 - date(check_date.year, 11, 1).weekday()) % 7 + 21),
        # Christmas
        date(check_date.year, 12, 25),
    ]
    
    return check_date in holidays

def calculate_crowd_trend(historical_data: List[Dict]) -> Dict:
    """Calculate crowd trends from historical data"""
    if not historical_data:
        return {}
    
    # Convert crowd levels to numeric values
    crowd_values = {"low": 0.25, "moderate": 0.5, "high": 0.75, "very_high": 1.0}
    
    # Group by day of week
    days_data = {i: [] for i in range(7)}  # 0 = Monday, 6 = Sunday
    
    for entry in historical_data:
        day_of_week = entry["date"].weekday()
        days_data[day_of_week].append(crowd_values[entry["average_crowd_level"]])
    
    # Calculate average by day of week
    day_averages = {}
    for day, values in days_data.items():
        if values:
            day_averages[day] = sum(values) / len(values)
    
    # Find busiest and quietest days
    if day_averages:
        busiest_day = max(day_averages.items(), key=lambda x: x[1])[0]
        quietest_day = min(day_averages.items(), key=lambda x: x[1])[0]
    else:
        busiest_day = quietest_day = None
    
    # Day of week names
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    return {
        "day_averages": {day_names[day]: round(avg, 2) for day, avg in day_averages.items()},
        "busiest_day": day_names[busiest_day] if busiest_day is not None else None,
        "quietest_day": day_names[quietest_day] if quietest_day is not None else None
    }

def estimate_wait_time(crowd_level: str, attraction_type: str = "general") -> int:
    """Estimate wait time in minutes based on crowd level and attraction type"""
    # Base wait times by crowd level
    base_times = {
        "low": 10,
        "moderate": 25,
        "high": 45,
        "very_high": 90
    }
    
    # Multipliers by attraction type
    multipliers = {
        "general": 1.0,
        "popular_ride": 1.5,
        "show": 0.8,
        "restaurant": 1.2,
        "museum": 0.7
    }
    
    # Get base time and apply multiplier
    base_time = base_times.get(crowd_level, 30)  # Default to 30 minutes if unknown
    multiplier = multipliers.get(attraction_type, 1.0)  # Default to general if unknown
    
    return int(base_time * multiplier)
