import uuid
import random
import math
from typing import List, Dict, Any, Optional, Set, Tuple
from datetime import datetime, timedelta
import re

from .schemas import (
    RecommendationCategory, Season, BudgetLevel, Location,
    TravelHistoryItem, UserPreference
)


def generate_destination_id() -> str:
    """Generate a unique ID for a destination."""
    return f"dest-{uuid.uuid4().hex[:8]}"


def generate_attraction_id() -> str:
    """Generate a unique ID for an attraction."""
    return f"attr-{uuid.uuid4().hex[:8]}"


def generate_itinerary_id() -> str:
    """Generate a unique ID for an itinerary."""
    return f"itin-{uuid.uuid4().hex[:8]}"


def generate_recommendation_log_id() -> str:
    """Generate a unique ID for a recommendation log."""
    return f"reclog-{uuid.uuid4().hex[:8]}"


def calculate_similarity(item1: Dict[str, Any], item2: Dict[str, Any], features: List[str]) -> float:
    """Calculate similarity between two items based on specified features.
    
    Args:
        item1: First item dictionary
        item2: Second item dictionary
        features: List of features to compare
        
    Returns:
        Similarity score between 0 and 1
    """
    similarity_score = 0.0
    feature_count = len(features)
    
    for feature in features:
        if feature not in item1 or feature not in item2:
            feature_count -= 1
            continue
            
        if isinstance(item1[feature], list) and isinstance(item2[feature], list):
            # For list features, calculate Jaccard similarity
            set1 = set(item1[feature])
            set2 = set(item2[feature])
            if set1 or set2:  # Avoid division by zero
                similarity_score += len(set1 & set2) / len(set1 | set2)
        elif item1[feature] == item2[feature]:
            # For scalar features, exact match = 1.0
            similarity_score += 1.0
    
    # Return average similarity across all features
    return similarity_score / max(1, feature_count)


def filter_by_budget(items: List[Dict[str, Any]], budget_level: BudgetLevel) -> List[Dict[str, Any]]:
    """Filter items by budget level.
    
    Args:
        items: List of items to filter
        budget_level: Budget level to filter by
        
    Returns:
        Filtered list of items
    """
    if budget_level == BudgetLevel.LUXURY:
        # Luxury travelers can see all options
        return items
    elif budget_level == BudgetLevel.MODERATE:
        # Moderate travelers see moderate and budget options
        return [item for item in items if item.get("budget_level") in [BudgetLevel.MODERATE, BudgetLevel.BUDGET]]
    else:
        # Budget travelers only see budget options
        return [item for item in items if item.get("budget_level") == BudgetLevel.BUDGET]


def filter_by_season(items: List[Dict[str, Any]], season: Season) -> List[Dict[str, Any]]:
    """Filter items by season.
    
    Args:
        items: List of items to filter
        season: Season to filter by
        
    Returns:
        Filtered list of items
    """
    return [item for item in items if "best_time_to_visit" in item and season in item["best_time_to_visit"]]


def calculate_personalization_score(
    item: Dict[str, Any],
    user_preferences: Optional[List[UserPreference]] = None,
    travel_history: Optional[List[TravelHistoryItem]] = None,
    current_season: Optional[Season] = None,
    budget_level: Optional[BudgetLevel] = None
) -> float:
    """Calculate personalization score for an item based on user data.
    
    Args:
        item: Item to calculate score for
        user_preferences: User preferences
        travel_history: User travel history
        current_season: Current season
        budget_level: User's budget level
        
    Returns:
        Personalization score
    """
    score = 0.0
    factors_applied = 0
    
    # Factor 1: User preferences
    if user_preferences and "categories" in item:
        factors_applied += 1
        preference_score = 0.0
        total_weight = sum(pref.weight for pref in user_preferences)
        
        for pref in user_preferences:
            if pref.category in item["categories"]:
                preference_score += pref.weight
        
        if total_weight > 0:
            score += (preference_score / total_weight) * 5.0  # Scale to 0-5
    
    # Factor 2: Season match
    if current_season and "best_time_to_visit" in item:
        factors_applied += 1
        if current_season in item["best_time_to_visit"]:
            score += 5.0
        elif (
            (current_season == Season.SPRING and Season.SUMMER in item["best_time_to_visit"]) or
            (current_season == Season.SUMMER and Season.SPRING in item["best_time_to_visit"]) or
            (current_season == Season.FALL and Season.SUMMER in item["best_time_to_visit"]) or
            (current_season == Season.WINTER and Season.FALL in item["best_time_to_visit"])
        ):
            # Adjacent seasons get partial score
            score += 2.5
    
    # Factor 3: Budget match
    if budget_level and "budget_level" in item:
        factors_applied += 1
        if item["budget_level"] == budget_level:
            score += 5.0
        elif (
            (budget_level == BudgetLevel.LUXURY and item["budget_level"] == BudgetLevel.MODERATE) or
            (budget_level == BudgetLevel.MODERATE and item["budget_level"] in [BudgetLevel.BUDGET, BudgetLevel.LUXURY])
        ):
            # Adjacent budget levels get partial score
            score += 2.5
    
    # Factor 4: Travel history
    if travel_history and "id" in item and "categories" in item:
        factors_applied += 1
        history_score = 0.0
        
        # Check if user has visited this exact destination
        visited_ids = [history.destination_id for history in travel_history]
        if item["id"] in visited_ids:
            # User already visited this place, slightly negative factor
            history_score -= 1.0
        else:
            # Calculate similarity to positively rated destinations
            positive_history = [history for history in travel_history if history.rating and history.rating >= 4.0]
            if positive_history:
                for history in positive_history:
                    # This is a simplified version - in a real system we would look up the historical destination
                    # and compare its categories with the current item
                    history_score += 1.0
                
                history_score = min(5.0, history_score)  # Cap at 5.0
        
        score += history_score
    
    # Calculate average score across all factors
    return score / max(1, factors_applied)


def get_current_season() -> Season:
    """Get the current season based on the current date.
    
    Returns:
        Current season
    """
    current_month = datetime.utcnow().month
    
    # Northern hemisphere seasons
    if 3 <= current_month <= 5:
        return Season.SPRING
    elif 6 <= current_month <= 8:
        return Season.SUMMER
    elif 9 <= current_month <= 11:
        return Season.FALL
    else:
        return Season.WINTER


def sanitize_recommendation_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize recommendation data to prevent injection attacks.
    
    Args:
        data: Data to sanitize
        
    Returns:
        Sanitized data
    """
    sanitized = {}
    
    for key, value in data.items():
        if isinstance(value, str):
            # Remove HTML/script tags
            sanitized[key] = re.sub(r'<[^>]*>', '', value)
        elif isinstance(value, dict):
            sanitized[key] = sanitize_recommendation_data(value)
        elif isinstance(value, list):
            sanitized[key] = [sanitize_recommendation_data(item) if isinstance(item, dict) else item for item in value]
        else:
            sanitized[key] = value
    
    return sanitized


def calculate_destination_score(destination: Dict[str, Any]) -> float:
    """Calculate an overall score for a destination based on various factors.
    
    Args:
        destination: Destination data
        
    Returns:
        Overall score
    """
    score = 0.0
    
    # Factor 1: Rating (0-5 scale, weight: 40%)
    if "rating" in destination:
        score += destination["rating"] * 0.4
    
    # Factor 2: Popularity (0-100 scale, normalized to 0-5, weight: 30%)
    if "popularity_score" in destination:
        score += (destination["popularity_score"] / 20) * 0.3
    
    # Factor 3: Season match (0 or 5 scale, weight: 20%)
    current_season = get_current_season()
    if "best_time_to_visit" in destination and current_season in destination["best_time_to_visit"]:
        score += 5.0 * 0.2
    
    # Factor 4: Number of highlights (normalized to 0-5 scale, weight: 10%)
    if "highlights" in destination and destination["highlights"]:
        highlights_score = min(5.0, len(destination["highlights"]) / 2)
        score += highlights_score * 0.1
    
    return score


def format_recommendation_reason(reason_type: str, details: Dict[str, Any]) -> str:
    """Format a recommendation reason based on type and details.
    
    Args:
        reason_type: Type of recommendation reason
        details: Details for the recommendation reason
        
    Returns:
        Formatted recommendation reason
    """
    if reason_type == "preference_match":
        categories = details.get("categories", [])
        if categories:
            category_names = [cat.value for cat in categories]
            return f"Matches your interest in {', '.join(category_names)}"
        return "Matches your preferences"
    
    elif reason_type == "season_match":
        season = details.get("season")
        if season:
            return f"Perfect for {season.value} travel"
        return "Great for your travel dates"
    
    elif reason_type == "budget_match":
        budget = details.get("budget")
        if budget:
            return f"Fits your {budget.value} budget"
        return "Matches your budget preferences"
    
    elif reason_type == "popular":
        return "Highly rated by other travelers"
    
    elif reason_type == "trending":
        return "Trending destination right now"
    
    elif reason_type == "similar":
        destination = details.get("destination")
        if destination:
            return f"Similar to {destination} which you enjoyed"
        return "Similar to places you've enjoyed"
    
    return "Recommended based on your profile"
