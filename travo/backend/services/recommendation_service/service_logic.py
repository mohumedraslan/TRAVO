from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timedelta
import random
import math

from .schemas import (
    DestinationRecommendationResponse, AttractionRecommendationResponse,
    RecommendationCategory, Season, BudgetLevel, Location, WeatherInfo,
    TravelHistoryItem, UserPreference, RecommendationRequest,
    PersonalizedRecommendationResponse, RecommendedItinerary
)
from .utils import (
    generate_destination_id, generate_attraction_id, generate_itinerary_id,
    calculate_similarity, filter_by_budget, filter_by_season,
    calculate_personalization_score
)

# Mock data for destinations
mock_destinations = [
    {
        "id": "dest-001",
        "name": "Paris",
        "description": "The City of Light, known for its art, fashion, gastronomy, and culture.",
        "location": {"city": "Paris", "country": "France", "latitude": 48.8566, "longitude": 2.3522},
        "categories": [RecommendationCategory.CITY, RecommendationCategory.CULTURAL, RecommendationCategory.ROMANTIC],
        "image_url": "https://example.com/images/paris.jpg",
        "rating": 4.7,
        "budget_level": BudgetLevel.MODERATE,
        "best_time_to_visit": [Season.SPRING, Season.FALL],
        "popularity_score": 95.0,
        "weather_info": {
            "avg_temperature": 15.0,
            "precipitation": 637.0,
            "best_season": Season.SPRING,
            "current_weather": "Partly cloudy"
        },
        "tags": ["eiffel tower", "louvre", "seine", "notre dame", "art"],
        "highlights": ["Eiffel Tower", "Louvre Museum", "Notre Dame Cathedral", "Seine River Cruise", "Montmartre"]
    },
    {
        "id": "dest-002",
        "name": "Bali",
        "description": "A tropical paradise with beautiful beaches, lush rice terraces, and vibrant culture.",
        "location": {"city": "Denpasar", "country": "Indonesia", "latitude": -8.6705, "longitude": 115.2126},
        "categories": [RecommendationCategory.BEACH, RecommendationCategory.CULTURAL, RecommendationCategory.RELAXATION],
        "image_url": "https://example.com/images/bali.jpg",
        "rating": 4.5,
        "budget_level": BudgetLevel.BUDGET,
        "best_time_to_visit": [Season.SPRING, Season.SUMMER],
        "popularity_score": 88.0,
        "weather_info": {
            "avg_temperature": 27.0,
            "precipitation": 1700.0,
            "best_season": Season.SUMMER,
            "current_weather": "Sunny"
        },
        "tags": ["beach", "temples", "rice terraces", "yoga", "surfing"],
        "highlights": ["Ubud Monkey Forest", "Tanah Lot Temple", "Tegallalang Rice Terraces", "Kuta Beach", "Mount Batur"]
    },
    {
        "id": "dest-003",
        "name": "New York City",
        "description": "The Big Apple, a global center for art, fashion, finance, and culture.",
        "location": {"city": "New York", "country": "USA", "latitude": 40.7128, "longitude": -74.0060},
        "categories": [RecommendationCategory.CITY, RecommendationCategory.SHOPPING, RecommendationCategory.NIGHTLIFE],
        "image_url": "https://example.com/images/nyc.jpg",
        "rating": 4.6,
        "budget_level": BudgetLevel.LUXURY,
        "best_time_to_visit": [Season.SPRING, Season.FALL],
        "popularity_score": 92.0,
        "weather_info": {
            "avg_temperature": 12.0,
            "precipitation": 1174.0,
            "best_season": Season.FALL,
            "current_weather": "Clear"
        },
        "tags": ["times square", "central park", "broadway", "statue of liberty", "museums"],
        "highlights": ["Times Square", "Central Park", "Empire State Building", "Statue of Liberty", "Broadway Shows"]
    },
    {
        "id": "dest-004",
        "name": "Kyoto",
        "description": "Japan's cultural capital with thousands of classical Buddhist temples and gardens.",
        "location": {"city": "Kyoto", "country": "Japan", "latitude": 35.0116, "longitude": 135.7681},
        "categories": [RecommendationCategory.CULTURAL, RecommendationCategory.CITY],
        "image_url": "https://example.com/images/kyoto.jpg",
        "rating": 4.8,
        "budget_level": BudgetLevel.MODERATE,
        "best_time_to_visit": [Season.SPRING, Season.FALL],
        "popularity_score": 85.0,
        "weather_info": {
            "avg_temperature": 15.0,
            "precipitation": 1500.0,
            "best_season": Season.SPRING,
            "current_weather": "Rainy"
        },
        "tags": ["temples", "shrines", "gardens", "geisha", "traditional"],
        "highlights": ["Fushimi Inari Shrine", "Kinkaku-ji (Golden Pavilion)", "Arashiyama Bamboo Grove", "Gion District", "Kiyomizu-dera Temple"]
    },
    {
        "id": "dest-005",
        "name": "Santorini",
        "description": "A stunning Greek island with white-washed buildings and blue domes overlooking the sea.",
        "location": {"city": "Thira", "country": "Greece", "latitude": 36.3932, "longitude": 25.4615},
        "categories": [RecommendationCategory.BEACH, RecommendationCategory.ROMANTIC, RecommendationCategory.RELAXATION],
        "image_url": "https://example.com/images/santorini.jpg",
        "rating": 4.9,
        "budget_level": BudgetLevel.LUXURY,
        "best_time_to_visit": [Season.SPRING, Season.FALL],
        "popularity_score": 90.0,
        "weather_info": {
            "avg_temperature": 23.0,
            "precipitation": 371.0,
            "best_season": Season.SUMMER,
            "current_weather": "Sunny"
        },
        "tags": ["caldera", "sunset", "blue domes", "beaches", "wine"],
        "highlights": ["Oia Sunset", "Fira Town", "Red Beach", "Akrotiri Archaeological Site", "Santorini Wineries"]
    }
]

# Mock data for attractions
mock_attractions = [
    # Paris attractions
    {
        "id": "attr-001",
        "name": "Eiffel Tower",
        "description": "Iconic iron tower that has become a global cultural icon of France.",
        "destination_id": "dest-001",
        "location": {"city": "Paris", "country": "France", "latitude": 48.8584, "longitude": 2.2945},
        "categories": [RecommendationCategory.CULTURAL, RecommendationCategory.ROMANTIC],
        "image_url": "https://example.com/images/eiffel.jpg",
        "rating": 4.7,
        "price_level": 3,
        "estimated_duration_minutes": 180,
        "tags": ["landmark", "view", "architecture", "iconic"],
        "best_time_to_visit": [Season.SPRING, Season.SUMMER, Season.FALL]
    },
    {
        "id": "attr-002",
        "name": "Louvre Museum",
        "description": "World's largest art museum and a historic monument housing the Mona Lisa.",
        "destination_id": "dest-001",
        "location": {"city": "Paris", "country": "France", "latitude": 48.8606, "longitude": 2.3376},
        "categories": [RecommendationCategory.CULTURAL],
        "image_url": "https://example.com/images/louvre.jpg",
        "rating": 4.8,
        "price_level": 2,
        "estimated_duration_minutes": 240,
        "tags": ["art", "museum", "history", "mona lisa"],
        "best_time_to_visit": [Season.FALL, Season.WINTER]
    },
    # Bali attractions
    {
        "id": "attr-003",
        "name": "Ubud Monkey Forest",
        "description": "Natural sanctuary home to over 700 Balinese long-tailed monkeys.",
        "destination_id": "dest-002",
        "location": {"city": "Ubud", "country": "Indonesia", "latitude": -8.5188, "longitude": 115.2582},
        "categories": [RecommendationCategory.ADVENTURE, RecommendationCategory.FAMILY],
        "image_url": "https://example.com/images/monkey-forest.jpg",
        "rating": 4.5,
        "price_level": 1,
        "estimated_duration_minutes": 120,
        "tags": ["nature", "wildlife", "monkeys", "forest"],
        "best_time_to_visit": [Season.SPRING, Season.FALL]
    },
    {
        "id": "attr-004",
        "name": "Tegallalang Rice Terraces",
        "description": "Stunning terraced rice fields offering a picturesque view of greenery.",
        "destination_id": "dest-002",
        "location": {"city": "Ubud", "country": "Indonesia", "latitude": -8.4312, "longitude": 115.2777},
        "categories": [RecommendationCategory.CULTURAL, RecommendationCategory.RELAXATION],
        "image_url": "https://example.com/images/rice-terraces.jpg",
        "rating": 4.6,
        "price_level": 1,
        "estimated_duration_minutes": 90,
        "tags": ["nature", "agriculture", "scenery", "photography"],
        "best_time_to_visit": [Season.SPRING, Season.SUMMER]
    },
    # New York attractions
    {
        "id": "attr-005",
        "name": "Central Park",
        "description": "Urban park spanning 843 acres in the heart of Manhattan.",
        "destination_id": "dest-003",
        "location": {"city": "New York", "country": "USA", "latitude": 40.7812, "longitude": -73.9665},
        "categories": [RecommendationCategory.RELAXATION, RecommendationCategory.FAMILY],
        "image_url": "https://example.com/images/central-park.jpg",
        "rating": 4.8,
        "price_level": 1,
        "estimated_duration_minutes": 180,
        "tags": ["park", "nature", "recreation", "walking"],
        "best_time_to_visit": [Season.SPRING, Season.FALL]
    },
    {
        "id": "attr-006",
        "name": "Empire State Building",
        "description": "Iconic 102-story skyscraper offering panoramic views of NYC.",
        "destination_id": "dest-003",
        "location": {"city": "New York", "country": "USA", "latitude": 40.7484, "longitude": -73.9857},
        "categories": [RecommendationCategory.CULTURAL, RecommendationCategory.ROMANTIC],
        "image_url": "https://example.com/images/empire-state.jpg",
        "rating": 4.7,
        "price_level": 3,
        "estimated_duration_minutes": 120,
        "tags": ["skyscraper", "view", "architecture", "landmark"],
        "best_time_to_visit": [Season.SPRING, Season.FALL, Season.SUMMER]
    }
]

# Mock data for recommended itineraries
mock_itineraries = [
    {
        "id": "itin-001",
        "title": "Romantic Paris Weekend",
        "description": "A perfect weekend getaway for couples in the City of Love.",
        "destination_id": "dest-001",
        "duration_days": 3,
        "activities_count": 8,
        "estimated_cost": 1200.0,
        "currency": "EUR",
        "image_url": "https://example.com/images/paris-romantic.jpg",
        "tags": ["romantic", "weekend", "couples", "sightseeing"]
    },
    {
        "id": "itin-002",
        "title": "Bali Wellness Retreat",
        "description": "A week of relaxation, yoga, and natural beauty in Bali.",
        "destination_id": "dest-002",
        "duration_days": 7,
        "activities_count": 15,
        "estimated_cost": 1500.0,
        "currency": "USD",
        "image_url": "https://example.com/images/bali-wellness.jpg",
        "tags": ["wellness", "yoga", "relaxation", "nature"]
    },
    {
        "id": "itin-003",
        "title": "New York City Explorer",
        "description": "Experience the best of NYC in 5 action-packed days.",
        "destination_id": "dest-003",
        "duration_days": 5,
        "activities_count": 12,
        "estimated_cost": 2500.0,
        "currency": "USD",
        "image_url": "https://example.com/images/nyc-explorer.jpg",
        "tags": ["city", "sightseeing", "shopping", "entertainment"]
    }
]


async def get_destination_recommendations(
    categories: Optional[List[RecommendationCategory]] = None,
    budget_level: Optional[BudgetLevel] = None,
    season: Optional[Season] = None,
    limit: int = 10,
    offset: int = 0
) -> Tuple[List[DestinationRecommendationResponse], int]:
    """Get destination recommendations based on filters."""
    filtered_destinations = mock_destinations.copy()
    
    # Apply category filter
    if categories:
        filtered_destinations = [
            dest for dest in filtered_destinations
            if any(category in dest["categories"] for category in categories)
        ]
    
    # Apply budget filter
    if budget_level:
        filtered_destinations = [
            dest for dest in filtered_destinations
            if dest["budget_level"] == budget_level
        ]
    
    # Apply season filter
    if season:
        filtered_destinations = [
            dest for dest in filtered_destinations
            if season in dest["best_time_to_visit"]
        ]
    
    # Get total count before pagination
    total_count = len(filtered_destinations)
    
    # Apply pagination
    paginated_destinations = filtered_destinations[offset:offset + limit]
    
    # Convert to response model
    result = [DestinationRecommendationResponse(**dest) for dest in paginated_destinations]
    
    return result, total_count


async def get_trending_destinations(
    limit: int = 5,
    offset: int = 0
) -> Tuple[List[DestinationRecommendationResponse], int]:
    """Get trending destinations based on popularity score."""
    # Sort destinations by popularity score in descending order
    sorted_destinations = sorted(
        mock_destinations,
        key=lambda x: x["popularity_score"],
        reverse=True
    )
    
    # Get total count before pagination
    total_count = len(sorted_destinations)
    
    # Apply pagination
    paginated_destinations = sorted_destinations[offset:offset + limit]
    
    # Convert to response model
    result = [DestinationRecommendationResponse(**dest) for dest in paginated_destinations]
    
    return result, total_count


async def get_similar_destinations(
    destination_id: str,
    limit: int = 5
) -> List[DestinationRecommendationResponse]:
    """Get destinations similar to the specified destination."""
    # Find the reference destination
    reference_destination = next((dest for dest in mock_destinations if dest["id"] == destination_id), None)
    
    if not reference_destination:
        return []
    
    # Calculate similarity scores for all other destinations
    similarity_scores = []
    for dest in mock_destinations:
        if dest["id"] != destination_id:
            # Calculate similarity based on categories, budget level, and best time to visit
            category_similarity = len(set(dest["categories"]) & set(reference_destination["categories"])) / \
                                 len(set(dest["categories"]) | set(reference_destination["categories"]))
            
            season_similarity = len(set(dest["best_time_to_visit"]) & set(reference_destination["best_time_to_visit"])) / \
                               len(set(dest["best_time_to_visit"]) | set(reference_destination["best_time_to_visit"]))
            
            budget_similarity = 1.0 if dest["budget_level"] == reference_destination["budget_level"] else 0.0
            
            # Weighted similarity score
            similarity = (0.5 * category_similarity) + (0.3 * season_similarity) + (0.2 * budget_similarity)
            
            similarity_scores.append((dest, similarity))
    
    # Sort by similarity score in descending order
    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Take top 'limit' destinations
    similar_destinations = [dest for dest, _ in similarity_scores[:limit]]
    
    # Convert to response model
    result = [DestinationRecommendationResponse(**dest) for dest in similar_destinations]
    
    return result


async def get_attraction_recommendations(
    destination_id: str,
    categories: Optional[List[RecommendationCategory]] = None,
    limit: int = 10,
    offset: int = 0
) -> Tuple[List[AttractionRecommendationResponse], int]:
    """Get attraction recommendations for a specific destination."""
    # Filter attractions by destination_id
    filtered_attractions = [attr for attr in mock_attractions if attr["destination_id"] == destination_id]
    
    # Apply category filter if provided
    if categories:
        filtered_attractions = [
            attr for attr in filtered_attractions
            if any(category in attr["categories"] for category in categories)
        ]
    
    # Get total count before pagination
    total_count = len(filtered_attractions)
    
    # Apply pagination
    paginated_attractions = filtered_attractions[offset:offset + limit]
    
    # Convert to response model
    result = [AttractionRecommendationResponse(**attr) for attr in paginated_attractions]
    
    return result, total_count


async def get_personalized_recommendations(
    request: RecommendationRequest
) -> PersonalizedRecommendationResponse:
    """Get personalized recommendations based on user preferences and history."""
    # Initialize weights for personalization
    destination_scores = {dest["id"]: 0.0 for dest in mock_destinations}
    
    # Factor 1: User preferences
    personalization_factors = []
    if request.preferences:
        personalization_factors.append("User preferences")
        for preference in request.preferences:
            for dest in mock_destinations:
                if preference.category in dest["categories"]:
                    destination_scores[dest["id"]] += preference.weight
    
    # Factor 2: Travel history
    if request.travel_history:
        personalization_factors.append("Travel history")
        for history_item in request.travel_history:
            # Find the historical destination
            historical_dest = next((dest for dest in mock_destinations if dest["id"] == history_item.destination_id), None)
            if historical_dest:
                # Boost similar destinations
                for dest in mock_destinations:
                    if dest["id"] != history_item.destination_id:
                        # Calculate similarity
                        category_similarity = len(set(dest["categories"]) & set(historical_dest["categories"])) / \
                                             max(1, len(set(dest["categories"]) | set(historical_dest["categories"])))
                        
                        # Apply rating boost if available
                        rating_factor = history_item.rating / 5.0 if history_item.rating else 0.8
                        
                        # Add to score
                        destination_scores[dest["id"]] += category_similarity * rating_factor * 2.0
    
    # Factor 3: Budget level
    if request.budget_level:
        personalization_factors.append("Budget level")
        for dest in mock_destinations:
            if dest["budget_level"] == request.budget_level:
                destination_scores[dest["id"]] += 3.0
            elif (
                (request.budget_level == BudgetLevel.LUXURY and dest["budget_level"] == BudgetLevel.MODERATE) or
                (request.budget_level == BudgetLevel.MODERATE and dest["budget_level"] in [BudgetLevel.BUDGET, BudgetLevel.LUXURY])
            ):
                destination_scores[dest["id"]] += 1.0
    
    # Factor 4: Travel dates and seasons
    if request.travel_dates:
        personalization_factors.append("Travel dates")
        travel_month = request.travel_dates["start_date"].month
        season = None
        
        # Determine season based on month (Northern Hemisphere)
        if 3 <= travel_month <= 5:
            season = Season.SPRING
        elif 6 <= travel_month <= 8:
            season = Season.SUMMER
        elif 9 <= travel_month <= 11:
            season = Season.FALL
        else:
            season = Season.WINTER
        
        for dest in mock_destinations:
            if season in dest["best_time_to_visit"]:
                destination_scores[dest["id"]] += 2.5
    
    # Sort destinations by score
    sorted_destinations = sorted(
        [(dest_id, score) for dest_id, score in destination_scores.items()],
        key=lambda x: x[1],
        reverse=True
    )
    
    # Get top destinations
    top_destination_ids = [dest_id for dest_id, _ in sorted_destinations[:5]]
    recommended_destinations = [
        DestinationRecommendationResponse(**dest)
        for dest in mock_destinations
        if dest["id"] in top_destination_ids
    ]
    
    # Add recommendation reason to each destination
    for dest in recommended_destinations:
        if request.preferences and any(pref.category in dest.categories for pref in request.preferences):
            dest.recommendation_reason = "Matches your preferred travel categories"
        elif request.budget_level and dest.budget_level == request.budget_level:
            dest.recommendation_reason = f"Fits your {dest.budget_level.value} budget preference"
        elif request.travel_dates and any(season in dest.best_time_to_visit for season in [Season.SPRING, Season.SUMMER, Season.FALL, Season.WINTER]):
            dest.recommendation_reason = "Great destination for your travel dates"
        else:
            dest.recommendation_reason = "Popular destination you might enjoy"
    
    # Get attractions for the top destinations
    recommended_attractions = []
    for dest_id in top_destination_ids[:2]:  # Only get attractions for top 2 destinations
        dest_attractions = [attr for attr in mock_attractions if attr["destination_id"] == dest_id]
        for attr in dest_attractions[:3]:  # Limit to 3 attractions per destination
            attraction = AttractionRecommendationResponse(**attr)
            attraction.recommendation_reason = "Popular attraction at your recommended destination"
            recommended_attractions.append(attraction)
    
    # Get recommended itineraries
    recommended_itineraries = []
    for dest_id in top_destination_ids[:2]:  # Only get itineraries for top 2 destinations
        dest_itineraries = [itin for itin in mock_itineraries if itin["destination_id"] == dest_id]
        recommended_itineraries.extend([RecommendedItinerary(**itin) for itin in dest_itineraries])
    
    # Create response
    response = PersonalizedRecommendationResponse(
        destinations=recommended_destinations,
        attractions=recommended_attractions,
        itineraries=recommended_itineraries,
        recommendation_date=datetime.utcnow(),
        expiry_date=datetime.utcnow() + timedelta(days=7),
        personalization_factors=personalization_factors
    )
    
    return response
