import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta, time
import random
import asyncio

# Import schemas
from .schemas import (
    ItineraryCreate,
    ItineraryResponse,
    ItineraryUpdate,
    ItineraryDayResponse,
    ItineraryActivityCreate,
    ItineraryActivityResponse,
    ItineraryActivityUpdate,
    ItineraryShareResponse,
    ActivityType,
    TransportationType,
    BudgetLevel,
    Location,
    TransportationDetails
)

# Import utils
from .utils import (
    generate_itinerary_id,
    generate_activity_id,
    generate_share_id,
    calculate_itinerary_stats,
    generate_share_url
)

# Mock data for itineraries
MOCK_ITINERARIES = [
    {
        "id": "itin_1",
        "user_id": "u1",
        "title": "Weekend in Paris",
        "description": "A romantic weekend exploring the City of Lights",
        "destination": "Paris, France",
        "start_date": datetime.utcnow() + timedelta(days=30),
        "end_date": datetime.utcnow() + timedelta(days=32),
        "budget_level": BudgetLevel.MODERATE,
        "tags": ["romantic", "city", "culture"],
        "cover_image_url": "https://example.com/images/paris.jpg",
        "created_at": datetime.utcnow() - timedelta(days=10),
        "updated_at": datetime.utcnow() - timedelta(days=5),
        "total_activities": 6,
        "total_cost": 850.00,
        "currency": "EUR"
    },
    {
        "id": "itin_2",
        "user_id": "u1",
        "title": "Rome Adventure",
        "description": "Exploring the ancient wonders of Rome",
        "destination": "Rome, Italy",
        "start_date": datetime.utcnow() + timedelta(days=60),
        "end_date": datetime.utcnow() + timedelta(days=65),
        "budget_level": BudgetLevel.LUXURY,
        "tags": ["history", "food", "architecture"],
        "cover_image_url": "https://example.com/images/rome.jpg",
        "created_at": datetime.utcnow() - timedelta(days=20),
        "updated_at": datetime.utcnow() - timedelta(days=15),
        "total_activities": 12,
        "total_cost": 1500.00,
        "currency": "EUR"
    },
    {
        "id": "itin_3",
        "user_id": "u2",
        "title": "Tokyo Exploration",
        "description": "Discovering the blend of tradition and modernity in Tokyo",
        "destination": "Tokyo, Japan",
        "start_date": datetime.utcnow() + timedelta(days=90),
        "end_date": datetime.utcnow() + timedelta(days=97),
        "budget_level": BudgetLevel.BUDGET,
        "tags": ["culture", "food", "technology"],
        "cover_image_url": "https://example.com/images/tokyo.jpg",
        "created_at": datetime.utcnow() - timedelta(days=30),
        "updated_at": datetime.utcnow() - timedelta(days=25),
        "total_activities": 15,
        "total_cost": 120000.00,
        "currency": "JPY"
    }
]

# Mock data for activities
MOCK_ACTIVITIES = [
    # Paris itinerary activities
    {
        "id": "act_1",
        "itinerary_id": "itin_1",
        "title": "Eiffel Tower Visit",
        "description": "Visit the iconic Eiffel Tower and enjoy panoramic views of Paris",
        "activity_type": ActivityType.ATTRACTION,
        "start_time": time(10, 0),
        "end_time": time(12, 0),
        "day_index": 0,
        "location": {
            "address": "Champ de Mars, 5 Avenue Anatole France",
            "city": "Paris",
            "country": "France",
            "latitude": 48.8584,
            "longitude": 2.2945
        },
        "transportation": {
            "type": TransportationType.PUBLIC_TRANSIT,
            "departure_location": "Hotel",
            "arrival_location": "Eiffel Tower",
            "notes": "Take Metro Line 6 to Bir-Hakeim station"
        },
        "booking_info": {
            "ticket_price": 25.50,
            "booking_url": "https://www.toureiffel.paris/en/rates-opening-times"
        },
        "cost": 25.50,
        "currency": "EUR",
        "notes": "Book tickets in advance to avoid long queues",
        "image_url": "https://example.com/images/eiffel_tower.jpg",
        "external_url": "https://www.toureiffel.paris/",
        "tags": ["landmark", "views", "must-see"],
        "order_index": 0,
        "created_at": datetime.utcnow() - timedelta(days=10),
        "updated_at": datetime.utcnow() - timedelta(days=10)
    },
    {
        "id": "act_2",
        "itinerary_id": "itin_1",
        "title": "Lunch at Le Jules Verne",
        "description": "Enjoy a gourmet lunch at the Eiffel Tower's renowned restaurant",
        "activity_type": ActivityType.RESTAURANT,
        "start_time": time(12, 30),
        "end_time": time(14, 30),
        "day_index": 0,
        "location": {
            "address": "Eiffel Tower, 2nd floor",
            "city": "Paris",
            "country": "France",
            "latitude": 48.8584,
            "longitude": 2.2945
        },
        "transportation": None,
        "booking_info": {
            "reservation": True,
            "booking_url": "https://www.lejulesverne-paris.com/"
        },
        "cost": 200.00,
        "currency": "EUR",
        "notes": "Dress code: Smart casual",
        "image_url": "https://example.com/images/jules_verne.jpg",
        "external_url": "https://www.lejulesverne-paris.com/",
        "tags": ["fine dining", "gourmet", "view"],
        "order_index": 1,
        "created_at": datetime.utcnow() - timedelta(days=10),
        "updated_at": datetime.utcnow() - timedelta(days=10)
    },
    # More activities for Paris...
    
    # Rome itinerary activities
    {
        "id": "act_7",
        "itinerary_id": "itin_2",
        "title": "Colosseum Tour",
        "description": "Guided tour of the ancient Roman Colosseum",
        "activity_type": ActivityType.ATTRACTION,
        "start_time": time(9, 0),
        "end_time": time(11, 0),
        "day_index": 0,
        "location": {
            "address": "Piazza del Colosseo, 1",
            "city": "Rome",
            "country": "Italy",
            "latitude": 41.8902,
            "longitude": 12.4922
        },
        "transportation": {
            "type": TransportationType.TAXI,
            "departure_location": "Hotel",
            "arrival_location": "Colosseum",
            "notes": "About 15 minutes by taxi"
        },
        "booking_info": {
            "ticket_price": 16.00,
            "booking_url": "https://www.coopculture.it/"
        },
        "cost": 16.00,
        "currency": "EUR",
        "notes": "Skip-the-line tickets recommended",
        "image_url": "https://example.com/images/colosseum.jpg",
        "external_url": "https://www.coopculture.it/",
        "tags": ["ancient", "history", "architecture"],
        "order_index": 0,
        "created_at": datetime.utcnow() - timedelta(days=20),
        "updated_at": datetime.utcnow() - timedelta(days=15)
    }
    # More activities for Rome and Tokyo...
]

# Mock data for shares
MOCK_SHARES = [
    {
        "id": "share_1",
        "itinerary_id": "itin_1",
        "expires_at": datetime.utcnow() + timedelta(days=30),
        "created_at": datetime.utcnow() - timedelta(days=5),
        "is_active": True
    }
]

# Service functions
async def create_itinerary(itinerary: ItineraryCreate) -> ItineraryResponse:
    """Create a new travel itinerary."""
    # Generate a new itinerary ID
    itinerary_id = generate_itinerary_id()
    
    # Calculate the number of days in the itinerary
    delta = itinerary.end_date - itinerary.start_date
    num_days = delta.days + 1
    
    # Create the new itinerary
    now = datetime.utcnow()
    new_itinerary = {
        "id": itinerary_id,
        "user_id": itinerary.user_id,
        "title": itinerary.title,
        "description": itinerary.description,
        "destination": itinerary.destination,
        "start_date": itinerary.start_date,
        "end_date": itinerary.end_date,
        "budget_level": itinerary.budget_level,
        "tags": itinerary.tags,
        "cover_image_url": itinerary.cover_image_url,
        "created_at": now,
        "updated_at": now,
        "total_activities": 0,
        "total_cost": 0.0,
        "currency": "USD"
    }
    
    # Add to mock data
    MOCK_ITINERARIES.append(new_itinerary)
    
    # Create empty days for the itinerary
    days = []
    for i in range(num_days):
        day_date = itinerary.start_date + timedelta(days=i)
        days.append(ItineraryDayResponse(
            day_index=i,
            date=day_date,
            activities=[]
        ))
    
    # Convert to response model
    return ItineraryResponse(
        **new_itinerary,
        days=days
    )

async def get_itineraries(
    user_id: str,
    limit: int = 10,
    offset: int = 0,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = "desc"
) -> List[ItineraryResponse]:
    """Get all itineraries for a user with pagination and sorting."""
    # Filter itineraries by user ID
    user_itineraries = [itin for itin in MOCK_ITINERARIES if itin["user_id"] == user_id]
    
    # Sort itineraries
    if sort_by:
        reverse = sort_order.lower() == "desc"
        user_itineraries.sort(key=lambda x: x[sort_by], reverse=reverse)
    
    # Apply pagination
    paginated_itineraries = user_itineraries[offset:offset + limit]
    
    # Convert to response models with days and activities
    result = []
    for itin in paginated_itineraries:
        # Get activities for this itinerary
        itin_activities = [act for act in MOCK_ACTIVITIES if act["itinerary_id"] == itin["id"]]
        
        # Group activities by day
        days_dict = {}
        for act in itin_activities:
            day_index = act["day_index"]
            if day_index not in days_dict:
                day_date = itin["start_date"] + timedelta(days=day_index)
                days_dict[day_index] = ItineraryDayResponse(
                    day_index=day_index,
                    date=day_date,
                    activities=[]
                )
            
            # Convert activity to response model
            activity_response = ItineraryActivityResponse(
                id=act["id"],
                itinerary_id=act["itinerary_id"],
                title=act["title"],
                description=act["description"],
                activity_type=act["activity_type"],
                start_time=act["start_time"],
                end_time=act["end_time"],
                day_index=act["day_index"],
                location=Location(**act["location"]) if act["location"] else None,
                transportation=TransportationDetails(**act["transportation"]) if act["transportation"] else None,
                booking_info=act["booking_info"],
                cost=act["cost"],
                currency=act["currency"],
                notes=act["notes"],
                image_url=act["image_url"],
                external_url=act["external_url"],
                tags=act["tags"],
                created_at=act["created_at"],
                updated_at=act["updated_at"]
            )
            
            # Add to day's activities
            days_dict[day_index].activities.append(activity_response)
        
        # Sort days by day_index
        days = list(days_dict.values())
        days.sort(key=lambda x: x.day_index)
        
        # Create itinerary response
        result.append(ItineraryResponse(
            **itin,
            days=days
        ))
    
    return result

async def get_itinerary_by_id(itinerary_id: str) -> Optional[ItineraryResponse]:
    """Get a specific itinerary by ID."""
    # Find the itinerary
    itinerary = None
    for itin in MOCK_ITINERARIES:
        if itin["id"] == itinerary_id:
            itinerary = itin
            break
    
    if not itinerary:
        return None
    
    # Get activities for this itinerary
    itin_activities = [act for act in MOCK_ACTIVITIES if act["itinerary_id"] == itinerary_id]
    
    # Group activities by day
    days_dict = {}
    for act in itin_activities:
        day_index = act["day_index"]
        if day_index not in days_dict:
            day_date = itinerary["start_date"] + timedelta(days=day_index)
            days_dict[day_index] = ItineraryDayResponse(
                day_index=day_index,
                date=day_date,
                activities=[]
            )
        
        # Convert activity to response model
        activity_response = ItineraryActivityResponse(
            id=act["id"],
            itinerary_id=act["itinerary_id"],
            title=act["title"],
            description=act["description"],
            activity_type=act["activity_type"],
            start_time=act["start_time"],
            end_time=act["end_time"],
            day_index=act["day_index"],
            location=Location(**act["location"]) if act["location"] else None,
            transportation=TransportationDetails(**act["transportation"]) if act["transportation"] else None,
            booking_info=act["booking_info"],
            cost=act["cost"],
            currency=act["currency"],
            notes=act["notes"],
            image_url=act["image_url"],
            external_url=act["external_url"],
            tags=act["tags"],
            created_at=act["created_at"],
            updated_at=act["updated_at"]
        )
        
        # Add to day's activities
        days_dict[day_index].activities.append(activity_response)
    
    # Create empty days for days without activities
    delta = itinerary["end_date"] - itinerary["start_date"]
    num_days = delta.days + 1
    for i in range(num_days):
        if i not in days_dict:
            day_date = itinerary["start_date"] + timedelta(days=i)
            days_dict[i] = ItineraryDayResponse(
                day_index=i,
                date=day_date,
                activities=[]
            )
    
    # Sort days by day_index
    days = list(days_dict.values())
    days.sort(key=lambda x: x.day_index)
    
    # Create itinerary response
    return ItineraryResponse(
        **itinerary,
        days=days
    )

async def update_itinerary(itinerary_id: str, itinerary_update: ItineraryUpdate) -> Optional[ItineraryResponse]:
    """Update an existing itinerary."""
    # Find the itinerary
    itinerary = None
    itinerary_index = -1
    for i, itin in enumerate(MOCK_ITINERARIES):
        if itin["id"] == itinerary_id:
            itinerary = itin
            itinerary_index = i
            break
    
    if not itinerary:
        return None
    
    # Update fields
    update_data = itinerary_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        itinerary[key] = value
    
    # Update the updated_at timestamp
    itinerary["updated_at"] = datetime.utcnow()
    
    # Update in mock data
    MOCK_ITINERARIES[itinerary_index] = itinerary
    
    # Return updated itinerary
    return await get_itinerary_by_id(itinerary_id)

async def delete_itinerary(itinerary_id: str) -> bool:
    """Delete an itinerary."""
    # Find the itinerary
    for i, itin in enumerate(MOCK_ITINERARIES):
        if itin["id"] == itinerary_id:
            # Remove from mock data
            MOCK_ITINERARIES.pop(i)
            
            # Remove associated activities
            global MOCK_ACTIVITIES
            MOCK_ACTIVITIES = [act for act in MOCK_ACTIVITIES if act["itinerary_id"] != itinerary_id]
            
            # Remove associated shares
            global MOCK_SHARES
            MOCK_SHARES = [share for share in MOCK_SHARES if share["itinerary_id"] != itinerary_id]
            
            return True
    
    return False

async def add_activity_to_itinerary(itinerary_id: str, activity: ItineraryActivityCreate) -> ItineraryActivityResponse:
    """Add a new activity to an itinerary."""
    # Check if the itinerary exists
    itinerary = None
    itinerary_index = -1
    for i, itin in enumerate(MOCK_ITINERARIES):
        if itin["id"] == itinerary_id:
            itinerary = itin
            itinerary_index = i
            break
    
    if not itinerary:
        raise ValueError("Itinerary not found")
    
    # Generate a new activity ID
    activity_id = generate_activity_id()
    
    # Get the current highest order_index for the day
    day_activities = [act for act in MOCK_ACTIVITIES if act["itinerary_id"] == itinerary_id and act["day_index"] == activity.day_index]
    order_index = 0
    if day_activities:
        order_index = max(act["order_index"] for act in day_activities) + 1
    
    # Create the new activity
    now = datetime.utcnow()
    new_activity = {
        "id": activity_id,
        "itinerary_id": itinerary_id,
        "title": activity.title,
        "description": activity.description,
        "activity_type": activity.activity_type,
        "start_time": activity.start_time,
        "end_time": activity.end_time,
        "day_index": activity.day_index,
        "location": activity.location.dict() if activity.location else None,
        "transportation": activity.transportation.dict() if activity.transportation else None,
        "booking_info": activity.booking_info,
        "cost": activity.cost,
        "currency": activity.currency,
        "notes": activity.notes,
        "image_url": activity.image_url,
        "external_url": activity.external_url,
        "tags": activity.tags,
        "order_index": order_index,
        "created_at": now,
        "updated_at": now
    }
    
    # Add to mock data
    MOCK_ACTIVITIES.append(new_activity)
    
    # Update itinerary stats
    itinerary["total_activities"] += 1
    if activity.cost:
        if activity.currency == itinerary["currency"]:
            itinerary["total_cost"] += activity.cost
        # In a real implementation, we would convert currencies
    
    itinerary["updated_at"] = now
    MOCK_ITINERARIES[itinerary_index] = itinerary
    
    # Convert to response model
    return ItineraryActivityResponse(
        id=new_activity["id"],
        itinerary_id=new_activity["itinerary_id"],
        title=new_activity["title"],
        description=new_activity["description"],
        activity_type=new_activity["activity_type"],
        start_time=new_activity["start_time"],
        end_time=new_activity["end_time"],
        day_index=new_activity["day_index"],
        location=Location(**new_activity["location"]) if new_activity["location"] else None,
        transportation=TransportationDetails(**new_activity["transportation"]) if new_activity["transportation"] else None,
        booking_info=new_activity["booking_info"],
        cost=new_activity["cost"],
        currency=new_activity["currency"],
        notes=new_activity["notes"],
        image_url=new_activity["image_url"],
        external_url=new_activity["external_url"],
        tags=new_activity["tags"],
        created_at=new_activity["created_at"],
        updated_at=new_activity["updated_at"]
    )

async def update_activity(itinerary_id: str, activity_id: str, activity_update: ItineraryActivityUpdate) -> Optional[ItineraryActivityResponse]:
    """Update an existing activity in an itinerary."""
    # Find the activity
    activity = None
    activity_index = -1
    for i, act in enumerate(MOCK_ACTIVITIES):
        if act["id"] == activity_id and act["itinerary_id"] == itinerary_id:
            activity = act
            activity_index = i
            break
    
    if not activity:
        return None
    
    # Update fields
    update_data = activity_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key in ["location", "transportation"] and value:
            activity[key] = value.dict() if value else None
        else:
            activity[key] = value
    
    # Update the updated_at timestamp
    activity["updated_at"] = datetime.utcnow()
    
    # Update in mock data
    MOCK_ACTIVITIES[activity_index] = activity
    
    # Update itinerary stats if cost changed
    if "cost" in update_data:
        # Find the itinerary
        for i, itin in enumerate(MOCK_ITINERARIES):
            if itin["id"] == itinerary_id:
                # Recalculate total cost
                total_cost = 0.0
                for act in MOCK_ACTIVITIES:
                    if act["itinerary_id"] == itinerary_id and act["cost"]:
                        if act["currency"] == itin["currency"]:
                            total_cost += act["cost"]
                        # In a real implementation, we would convert currencies
                
                itin["total_cost"] = total_cost
                itin["updated_at"] = datetime.utcnow()
                MOCK_ITINERARIES[i] = itin
                break
    
    # Convert to response model
    return ItineraryActivityResponse(
        id=activity["id"],
        itinerary_id=activity["itinerary_id"],
        title=activity["title"],
        description=activity["description"],
        activity_type=activity["activity_type"],
        start_time=activity["start_time"],
        end_time=activity["end_time"],
        day_index=activity["day_index"],
        location=Location(**activity["location"]) if activity["location"] else None,
        transportation=TransportationDetails(**activity["transportation"]) if activity["transportation"] else None,
        booking_info=activity["booking_info"],
        cost=activity["cost"],
        currency=activity["currency"],
        notes=activity["notes"],
        image_url=activity["image_url"],
        external_url=activity["external_url"],
        tags=activity["tags"],
        created_at=activity["created_at"],
        updated_at=activity["updated_at"]
    )

async def delete_activity(itinerary_id: str, activity_id: str) -> bool:
    """Delete an activity from an itinerary."""
    # Find the activity
    for i, act in enumerate(MOCK_ACTIVITIES):
        if act["id"] == activity_id and act["itinerary_id"] == itinerary_id:
            # Remove from mock data
            activity = MOCK_ACTIVITIES.pop(i)
            
            # Update itinerary stats
            for j, itin in enumerate(MOCK_ITINERARIES):
                if itin["id"] == itinerary_id:
                    itin["total_activities"] -= 1
                    if activity["cost"] and activity["currency"] == itin["currency"]:
                        itin["total_cost"] -= activity["cost"]
                    
                    itin["updated_at"] = datetime.utcnow()
                    MOCK_ITINERARIES[j] = itin
                    break
            
            return True
    
    return False

async def reorder_activities(itinerary_id: str, activity_ids: List[str]) -> bool:
    """Reorder activities within an itinerary."""
    # Check if all activities exist and belong to the itinerary
    activities = []
    for act_id in activity_ids:
        found = False
        for act in MOCK_ACTIVITIES:
            if act["id"] == act_id and act["itinerary_id"] == itinerary_id:
                activities.append(act)
                found = True
                break
        
        if not found:
            return False
    
    # Update order_index for each activity
    for i, act in enumerate(activities):
        for j, mock_act in enumerate(MOCK_ACTIVITIES):
            if mock_act["id"] == act["id"]:
                MOCK_ACTIVITIES[j]["order_index"] = i
                MOCK_ACTIVITIES[j]["updated_at"] = datetime.utcnow()
                break
    
    # Update itinerary updated_at
    for i, itin in enumerate(MOCK_ITINERARIES):
        if itin["id"] == itinerary_id:
            MOCK_ITINERARIES[i]["updated_at"] = datetime.utcnow()
            break
    
    return True

async def share_itinerary(itinerary_id: str) -> Optional[ItineraryShareResponse]:
    """Generate a shareable link for an itinerary."""
    # Check if the itinerary exists
    itinerary = None
    for itin in MOCK_ITINERARIES:
        if itin["id"] == itinerary_id:
            itinerary = itin
            break
    
    if not itinerary:
        return None
    
    # Check if a share already exists
    for share in MOCK_SHARES:
        if share["itinerary_id"] == itinerary_id and share["is_active"]:
            # Return existing share
            share_url = generate_share_url(share["id"])
            return ItineraryShareResponse(
                itinerary_id=share["itinerary_id"],
                share_id=share["id"],
                share_url=share_url,
                expires_at=share["expires_at"],
                created_at=share["created_at"]
            )
    
    # Generate a new share
    share_id = generate_share_id()
    expires_at = datetime.utcnow() + timedelta(days=30)  # Expires in 30 days
    
    new_share = {
        "id": share_id,
        "itinerary_id": itinerary_id,
        "expires_at": expires_at,
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    # Add to mock data
    MOCK_SHARES.append(new_share)
    
    # Generate share URL
    share_url = generate_share_url(share_id)
    
    return ItineraryShareResponse(
        itinerary_id=new_share["itinerary_id"],
        share_id=new_share["id"],
        share_url=share_url,
        expires_at=new_share["expires_at"],
        created_at=new_share["created_at"]
    )

async def get_shared_itinerary(share_id: str) -> Optional[ItineraryResponse]:
    """Get a shared itinerary using a share ID."""
    # Find the share
    share = None
    for s in MOCK_SHARES:
        if s["id"] == share_id:
            share = s
            break
    
    if not share:
        return None
    
    # Check if the share is active and not expired
    now = datetime.utcnow()
    if not share["is_active"] or (share["expires_at"] and share["expires_at"] < now):
        return None
    
    # Get the itinerary
    return await get_itinerary_by_id(share["itinerary_id"])

async def generate_itinerary(
    destination: str,
    start_date: datetime,
    end_date: datetime,
    preferences: List[str],
    budget_level: Optional[str],
    user_id: str
) -> ItineraryResponse:
    """Generate an AI-powered itinerary based on user preferences."""
    # Simulate AI processing delay
    await asyncio.sleep(2)
    
    # Create a new itinerary
    itinerary_create = ItineraryCreate(
        title=f"Trip to {destination}",
        description=f"AI-generated itinerary for {destination}",
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        budget_level=BudgetLevel(budget_level) if budget_level else None,
        tags=preferences,
        user_id=user_id
    )
    
    # Create the itinerary
    itinerary = await create_itinerary(itinerary_create)
    
    # Calculate the number of days
    delta = end_date - start_date
    num_days = delta.days + 1
    
    # Generate activities for each day
    for day in range(num_days):
        # Morning activity
        morning_activity = ItineraryActivityCreate(
            title=f"Morning exploration of {destination} - Day {day+1}",
            description=f"Explore the highlights of {destination}",
            activity_type=ActivityType.ATTRACTION,
            start_time=time(9, 0),
            end_time=time(12, 0),
            day_index=day,
            location=Location(
                city=destination,
                country="",
                latitude=random.uniform(-90, 90),
                longitude=random.uniform(-180, 180)
            ),
            tags=random.sample(preferences, min(len(preferences), 2)) if preferences else []
        )
        await add_activity_to_itinerary(itinerary.id, morning_activity)
        
        # Lunch activity
        lunch_activity = ItineraryActivityCreate(
            title=f"Lunch at local restaurant - Day {day+1}",
            description=f"Enjoy local cuisine in {destination}",
            activity_type=ActivityType.RESTAURANT,
            start_time=time(12, 30),
            end_time=time(14, 0),
            day_index=day,
            location=Location(
                city=destination,
                country="",
                latitude=random.uniform(-90, 90),
                longitude=random.uniform(-180, 180)
            ),
            cost=random.uniform(20, 100),
            currency="USD",
            tags=["food", "local"]
        )
        await add_activity_to_itinerary(itinerary.id, lunch_activity)
        
        # Afternoon activity
        afternoon_activity = ItineraryActivityCreate(
            title=f"Afternoon activity in {destination} - Day {day+1}",
            description=f"Discover more of {destination}",
            activity_type=ActivityType.ATTRACTION,
            start_time=time(14, 30),
            end_time=time(17, 0),
            day_index=day,
            location=Location(
                city=destination,
                country="",
                latitude=random.uniform(-90, 90),
                longitude=random.uniform(-180, 180)
            ),
            tags=random.sample(preferences, min(len(preferences), 2)) if preferences else []
        )
        await add_activity_to_itinerary(itinerary.id, afternoon_activity)
        
        # Dinner activity
        dinner_activity = ItineraryActivityCreate(
            title=f"Dinner - Day {day+1}",
            description=f"Evening dining in {destination}",
            activity_type=ActivityType.RESTAURANT,
            start_time=time(19, 0),
            end_time=time(21, 0),
            day_index=day,
            location=Location(
                city=destination,
                country="",
                latitude=random.uniform(-90, 90),
                longitude=random.uniform(-180, 180)
            ),
            cost=random.uniform(30, 150),
            currency="USD",
            tags=["food", "dinner"]
        )
        await add_activity_to_itinerary(itinerary.id, dinner_activity)
    
    # Return the generated itinerary
    return await get_itinerary_by_id(itinerary.id)
