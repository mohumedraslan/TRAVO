from typing import List, Optional, Tuple, Dict
from datetime import date, datetime, timedelta
import random

# Crowd level probabilities for different scenarios
WEEKDAY_PROBS = {"low": 0.4, "moderate": 0.3, "high": 0.2, "very_high": 0.1}
WEEKEND_PROBS = {"low": 0.1, "moderate": 0.3, "high": 0.4, "very_high": 0.2}
HOLIDAY_PROBS = {"low": 0.05, "moderate": 0.15, "high": 0.3, "very_high": 0.5}

# Mock popular locations
POPULAR_LOCATIONS = [
    "Eiffel Tower", "Louvre Museum", "Colosseum", "Statue of Liberty",
    "Great Wall of China", "Taj Mahal", "Machu Picchu", "Pyramids of Giza"
]

async def get_crowd_prediction(
    location: str,
    date: Optional[date] = None,
    time_range: Optional[Tuple[int, int]] = None
) -> Dict:
    """Generate a simulated crowd prediction for a location
    
    This is a placeholder for a real ML-based crowd prediction model.
    In a production system, this would use historical data, current events,
    weather forecasts, and other factors to predict crowd levels.
    """
    # Use current date if not provided
    if date is None:
        date = datetime.now().date()
    
    # Default to full day if time range not provided
    if time_range is None:
        time_range = (8, 20)  # 8 AM to 8 PM
    
    # Determine if it's a weekend
    is_weekend = date.weekday() >= 5  # 5 = Saturday, 6 = Sunday
    
    # Determine if it's a holiday (simplified mock implementation)
    is_holiday = (date.month == 12 and date.day == 25) or \
                (date.month == 1 and date.day == 1) or \
                (date.month == 7 and date.day == 4)
    
    # Select probability distribution based on day type
    if is_holiday:
        probs = HOLIDAY_PROBS
    elif is_weekend:
        probs = WEEKEND_PROBS
    else:
        probs = WEEKDAY_PROBS
    
    # Adjust probabilities based on location popularity
    if location in POPULAR_LOCATIONS:
        # Shift probabilities toward higher crowd levels for popular locations
        probs = {
            "low": max(0.05, probs["low"] - 0.2),
            "moderate": probs["moderate"],
            "high": probs["high"] + 0.1,
            "very_high": probs["very_high"] + 0.1
        }
    
    # Generate hourly predictions
    hourly_predictions = []
    for hour in range(time_range[0], time_range[1] + 1):
        # Morning and evening tend to be less crowded
        time_factor = 1.0
        if hour < 10 or hour > 18:
            time_factor = 0.7
        elif 12 <= hour <= 14:  # Lunch time peak
            time_factor = 1.3
        
        # Adjust probabilities based on time of day
        hour_probs = {
            k: min(1.0, v * time_factor) for k, v in probs.items()
        }
        
        # Normalize probabilities
        total = sum(hour_probs.values())
        hour_probs = {k: v / total for k, v in hour_probs.items()}
        
        # Weighted random selection of crowd level
        crowd_level = random.choices(
            population=list(hour_probs.keys()),
            weights=list(hour_probs.values()),
            k=1
        )[0]
        
        # Estimate wait time based on crowd level
        wait_times = {
            "low": random.randint(5, 15),
            "moderate": random.randint(15, 30),
            "high": random.randint(30, 60),
            "very_high": random.randint(60, 120)
        }
        
        hourly_predictions.append({
            "hour": hour,
            "crowd_level": crowd_level,
            "wait_time_minutes": wait_times[crowd_level]
        })
    
    # Determine overall crowd level (mode of hourly predictions)
    crowd_counts = {"low": 0, "moderate": 0, "high": 0, "very_high": 0}
    for pred in hourly_predictions:
        crowd_counts[pred["crowd_level"]] += 1
    
    overall_crowd_level = max(crowd_counts.items(), key=lambda x: x[1])[0]
    
    # Generate prediction factors
    factors = []
    if is_weekend:
        factors.append({
            "name": "Weekend",
            "impact": 0.7,
            "description": "Weekend days typically see higher visitor numbers"
        })
    if is_holiday:
        factors.append({
            "name": "Holiday",
            "impact": 0.9,
            "description": "Public holiday significantly increases crowd levels"
        })
    if location in POPULAR_LOCATIONS:
        factors.append({
            "name": "Popular Attraction",
            "impact": 0.8,
            "description": "This is one of the most visited attractions in the area"
        })
    
    # Add some random factors for variety
    possible_factors = [
        {
            "name": "Local Event",
            "impact": 0.6,
            "description": "A local event is taking place nearby"
        },
        {
            "name": "Good Weather",
            "impact": 0.5,
            "description": "Pleasant weather conditions attract more visitors"
        },
        {
            "name": "School Break",
            "impact": 0.7,
            "description": "School holidays increase family visits"
        },
        {
            "name": "Off-Season",
            "impact": -0.6,
            "description": "Current travel season has fewer tourists"
        }
    ]
    
    # Add 1-2 random factors
    for _ in range(random.randint(1, 2)):
        if possible_factors:
            factor = random.choice(possible_factors)
            factors.append(factor)
            possible_factors.remove(factor)
    
    return {
        "location": location,
        "date": date,
        "overall_crowd_level": overall_crowd_level,
        "hourly_predictions": hourly_predictions,
        "factors": factors,
        "last_updated": datetime.now()
    }

async def get_crowd_history(
    location: str,
    from_date: date,
    to_date: date
) -> Dict:
    """Generate simulated historical crowd data
    
    This is a placeholder for actual historical data that would be
    retrieved from a database in a production system.
    """
    # Validate date range
    if from_date > to_date:
        from_date, to_date = to_date, from_date
    
    # Limit to 90 days of history to avoid excessive data
    days_diff = (to_date - from_date).days
    if days_diff > 90:
        from_date = date.fromordinal(to_date.toordinal() - 90)
    
    # Generate data points for each day in the range
    data_points = []
    current_date = from_date
    
    while current_date <= to_date:
        # Determine if it's a weekend
        is_weekend = current_date.weekday() >= 5
        
        # Select appropriate probability distribution
        if is_weekend:
            probs = WEEKEND_PROBS
        else:
            probs = WEEKDAY_PROBS
        
        # Weighted random selection of crowd level
        crowd_level = random.choices(
            population=list(probs.keys()),
            weights=list(probs.values()),
            k=1
        )[0]
        
        # Generate random peak hours (2-4 hours)
        num_peak_hours = random.randint(2, 4)
        peak_hours = sorted(random.sample(range(10, 19), num_peak_hours))  # 10 AM to 7 PM
        
        # Estimate total visitors based on crowd level
        visitors_base = {
            "low": random.randint(500, 1000),
            "moderate": random.randint(1000, 2500),
            "high": random.randint(2500, 5000),
            "very_high": random.randint(5000, 10000)
        }
        
        # Add some randomness to visitor numbers
        total_visitors = int(visitors_base[crowd_level] * random.uniform(0.8, 1.2))
        
        data_points.append({
            "date": current_date,
            "average_crowd_level": crowd_level,
            "peak_hours": peak_hours,
            "total_visitors": total_visitors
        })
        
        # Move to next day
        current_date = date.fromordinal(current_date.toordinal() + 1)
    
    # Calculate trends
    weekday_crowds = [p for p in data_points if p["date"].weekday() < 5]
    weekend_crowds = [p for p in data_points if p["date"].weekday() >= 5]
    
    # Convert crowd levels to numeric values for averaging
    crowd_values = {"low": 0.25, "moderate": 0.5, "high": 0.75, "very_high": 1.0}
    
    weekday_avg = sum(crowd_values[p["average_crowd_level"]] for p in weekday_crowds) / len(weekday_crowds) if weekday_crowds else 0
    weekend_avg = sum(crowd_values[p["average_crowd_level"]] for p in weekend_crowds) / len(weekend_crowds) if weekend_crowds else 0
    
    trends = {
        "weekday_avg": round(weekday_avg, 2),
        "weekend_avg": round(weekend_avg, 2),
        "busiest_day": max(data_points, key=lambda x: crowd_values[x["average_crowd_level"]])["date"].strftime("%Y-%m-%d") if data_points else None
    }
    
    return {
        "location": location,
        "from_date": from_date,
        "to_date": to_date,
        "data_points": data_points,
        "trends": trends
    }
