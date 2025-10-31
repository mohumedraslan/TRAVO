import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import random
import math

# Import schemas
from .schemas import BusinessListingResponse, BusinessDetailResponse, ReviewResponse, ReviewCreate, BusinessCategory, PriceLevel, Location, BusinessHours

# Mock data for businesses
MOCK_BUSINESSES = [
    {
        "id": "b1",
        "name": "Eiffel Tower Restaurant",
        "category": BusinessCategory.RESTAURANT,
        "description": "Elegant dining with a view of the Eiffel Tower.",
        "rating": 4.7,
        "review_count": 1250,
        "price_level": PriceLevel.EXPENSIVE,
        "phone": "+33-1-2345-6789",
        "website": "https://example.com/eiffel-restaurant",
        "email": "info@eiffelrestaurant.com",
        "hours": {
            "monday": "11:00-23:00",
            "tuesday": "11:00-23:00",
            "wednesday": "11:00-23:00",
            "thursday": "11:00-23:00",
            "friday": "11:00-00:00",
            "saturday": "10:00-00:00",
            "sunday": "10:00-22:00"
        },
        "location": {
            "address": "123 Champ de Mars",
            "city": "Paris",
            "state": "Île-de-France",
            "country": "France",
            "postal_code": "75007",
            "latitude": 48.8584,
            "longitude": 2.2945
        },
        "images": [
            "https://example.com/images/eiffel-restaurant-1.jpg",
            "https://example.com/images/eiffel-restaurant-2.jpg"
        ],
        "amenities": ["Outdoor Seating", "Reservations", "Wheelchair Accessible", "Full Bar"],
        "tags": ["French Cuisine", "Fine Dining", "Romantic", "View"],
        "created_at": datetime.utcnow() - timedelta(days=365),
        "updated_at": datetime.utcnow() - timedelta(days=30)
    },
    {
        "id": "b2",
        "name": "Colosseum Hotel",
        "category": BusinessCategory.HOTEL,
        "description": "Luxury hotel with a view of the Colosseum.",
        "rating": 4.5,
        "review_count": 875,
        "price_level": PriceLevel.LUXURY,
        "phone": "+39-06-1234-5678",
        "website": "https://example.com/colosseum-hotel",
        "email": "reservations@colosseumhotel.com",
        "hours": {
            "monday": "00:00-24:00",
            "tuesday": "00:00-24:00",
            "wednesday": "00:00-24:00",
            "thursday": "00:00-24:00",
            "friday": "00:00-24:00",
            "saturday": "00:00-24:00",
            "sunday": "00:00-24:00"
        },
        "location": {
            "address": "45 Via dei Fori Imperiali",
            "city": "Rome",
            "state": "Lazio",
            "country": "Italy",
            "postal_code": "00184",
            "latitude": 41.8902,
            "longitude": 12.4922
        },
        "images": [
            "https://example.com/images/colosseum-hotel-1.jpg",
            "https://example.com/images/colosseum-hotel-2.jpg",
            "https://example.com/images/colosseum-hotel-3.jpg"
        ],
        "amenities": ["Pool", "Spa", "Free WiFi", "Room Service", "Concierge", "Fitness Center"],
        "tags": ["Luxury", "Historic", "City Center", "Family Friendly"],
        "created_at": datetime.utcnow() - timedelta(days=730),
        "updated_at": datetime.utcnow() - timedelta(days=15)
    },
    {
        "id": "b3",
        "name": "Taj Mahal Souvenir Shop",
        "category": BusinessCategory.SHOPPING,
        "description": "Authentic souvenirs and gifts from the Taj Mahal.",
        "rating": 4.2,
        "review_count": 320,
        "price_level": PriceLevel.MODERATE,
        "phone": "+91-562-222-3333",
        "website": "https://example.com/taj-souvenirs",
        "email": "shop@tajsouvenirs.com",
        "hours": {
            "monday": "09:00-18:00",
            "tuesday": "09:00-18:00",
            "wednesday": "09:00-18:00",
            "thursday": "09:00-18:00",
            "friday": "09:00-18:00",
            "saturday": "09:00-19:00",
            "sunday": "10:00-17:00"
        },
        "location": {
            "address": "78 Taj Road",
            "city": "Agra",
            "state": "Uttar Pradesh",
            "country": "India",
            "postal_code": "282001",
            "latitude": 27.1751,
            "longitude": 78.0421
        },
        "images": [
            "https://example.com/images/taj-shop-1.jpg",
            "https://example.com/images/taj-shop-2.jpg"
        ],
        "amenities": ["Credit Cards Accepted", "Shipping Available", "Custom Orders"],
        "tags": ["Souvenirs", "Handicrafts", "Local Artisans", "Gifts"],
        "created_at": datetime.utcnow() - timedelta(days=180),
        "updated_at": datetime.utcnow() - timedelta(days=5)
    }
]

# Mock data for reviews
MOCK_REVIEWS = [
    {
        "id": "r1",
        "business_id": "b1",
        "user_id": "u1",
        "user_name": "John Doe",
        "rating": 5.0,
        "content": "Amazing view and excellent food. The service was impeccable.",
        "images": ["https://example.com/images/review-eiffel-1.jpg"],
        "created_at": datetime.utcnow() - timedelta(days=45),
        "updated_at": datetime.utcnow() - timedelta(days=45)
    },
    {
        "id": "r2",
        "business_id": "b1",
        "user_id": "u2",
        "user_name": "Jane Smith",
        "rating": 4.5,
        "content": "Great atmosphere and delicious food. A bit pricey but worth it for the experience.",
        "images": [],
        "created_at": datetime.utcnow() - timedelta(days=30),
        "updated_at": datetime.utcnow() - timedelta(days=30)
    },
    {
        "id": "r3",
        "business_id": "b2",
        "user_id": "u3",
        "user_name": "Michael Johnson",
        "rating": 4.0,
        "content": "Beautiful hotel with excellent amenities. The view of the Colosseum is breathtaking.",
        "images": ["https://example.com/images/review-colosseum-1.jpg", "https://example.com/images/review-colosseum-2.jpg"],
        "created_at": datetime.utcnow() - timedelta(days=60),
        "updated_at": datetime.utcnow() - timedelta(days=60)
    },
    {
        "id": "r4",
        "business_id": "b3",
        "user_id": "u4",
        "user_name": "Emily Wilson",
        "rating": 4.5,
        "content": "Great selection of authentic souvenirs. The staff was very helpful and knowledgeable.",
        "images": ["https://example.com/images/review-taj-1.jpg"],
        "created_at": datetime.utcnow() - timedelta(days=15),
        "updated_at": datetime.utcnow() - timedelta(days=15)
    }
]

# Helper function to calculate distance between two coordinates (Haversine formula)
def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    # Earth radius in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Differences
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    return distance

# Service functions
async def get_businesses(
    latitude: float,
    longitude: float,
    radius: float = 5.0,
    category: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
) -> List[BusinessListingResponse]:
    # Filter businesses by distance and category
    filtered_businesses = []
    
    for business in MOCK_BUSINESSES:
        # Calculate distance
        distance = calculate_distance(
            latitude, 
            longitude, 
            business["location"]["latitude"], 
            business["location"]["longitude"]
        )
        
        # Check if within radius
        if distance <= radius:
            # Check category if provided
            if category and business["category"].value != category:
                continue
            
            # Add distance to business data
            business_copy = dict(business)
            business_copy["distance_km"] = distance
            
            filtered_businesses.append(business_copy)
    
    # Sort by distance
    filtered_businesses.sort(key=lambda x: x["distance_km"])
    
    # Apply pagination
    paginated_businesses = filtered_businesses[offset:offset + limit]
    
    # Convert to response model
    result = []
    for business in paginated_businesses:
        result.append(BusinessListingResponse(
            id=business["id"],
            name=business["name"],
            category=business["category"],
            rating=business["rating"],
            review_count=business["review_count"],
            price_level=business["price_level"],
            image_url=business["images"][0] if business["images"] else None,
            location=Location(**business["location"]),
            distance_km=business["distance_km"]
        ))
    
    return result

async def get_business_by_id(business_id: str) -> Optional[BusinessDetailResponse]:
    # Find business by ID
    for business in MOCK_BUSINESSES:
        if business["id"] == business_id:
            # Convert to response model
            return BusinessDetailResponse(
                id=business["id"],
                name=business["name"],
                category=business["category"],
                description=business["description"],
                rating=business["rating"],
                review_count=business["review_count"],
                price_level=business["price_level"],
                phone=business["phone"],
                website=business["website"],
                email=business["email"],
                hours=BusinessHours(**business["hours"]),
                location=Location(**business["location"]),
                images=business["images"],
                amenities=business["amenities"],
                tags=business["tags"],
                created_at=business["created_at"],
                updated_at=business["updated_at"]
            )
    
    return None

async def get_reviews(business_id: str, limit: int = 10, offset: int = 0) -> List[ReviewResponse]:
    # Filter reviews by business ID
    filtered_reviews = [review for review in MOCK_REVIEWS if review["business_id"] == business_id]
    
    # Sort by date (newest first)
    filtered_reviews.sort(key=lambda x: x["created_at"], reverse=True)
    
    # Apply pagination
    paginated_reviews = filtered_reviews[offset:offset + limit]
    
    # Convert to response model
    result = []
    for review in paginated_reviews:
        result.append(ReviewResponse(**review))
    
    return result

async def create_review(business_id: str, review_data: ReviewCreate) -> ReviewResponse:
    # Generate a new review ID
    review_id = f"r{len(MOCK_REVIEWS) + 1}"
    
    # Get a random user name for the mock data
    user_names = ["Alex Johnson", "Sarah Williams", "David Brown", "Lisa Davis", "Robert Wilson"]
    user_name = random.choice(user_names)
    
    # Create a new review
    now = datetime.utcnow()
    new_review = {
        "id": review_id,
        "business_id": business_id,
        "user_id": review_data.user_id,
        "user_name": user_name,
        "rating": review_data.rating,
        "content": review_data.content,
        "images": review_data.images,
        "created_at": now,
        "updated_at": now
    }
    
    # Add to mock data
    MOCK_REVIEWS.append(new_review)
    
    # Update business rating and review count
    for business in MOCK_BUSINESSES:
        if business["id"] == business_id:
            # Calculate new average rating
            total_rating = business["rating"] * business["review_count"] + review_data.rating
            business["review_count"] += 1
            business["rating"] = total_rating / business["review_count"]
            business["rating"] = round(business["rating"], 1)  # Round to 1 decimal place
            business["updated_at"] = now
            break
    
    # Return the new review
    return ReviewResponse(**new_review)
