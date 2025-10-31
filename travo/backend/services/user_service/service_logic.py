from typing import List, Optional
import uuid
from datetime import datetime

# In a real application, these functions would interact with a database
# For now, we'll use an in-memory store for demonstration

# Mock database
users_db = {}

async def get_all_users():
    """Get all users from the database"""
    return list(users_db.values())

async def get_user(user_id: str):
    """Get a user by ID"""
    return users_db.get(user_id)

async def create_user(user_data):
    """Create a new user"""
    user_id = str(uuid.uuid4())
    current_time = datetime.utcnow()
    
    # In a real application, we would hash the password
    new_user = {
        "id": user_id,
        "email": user_data.email,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "profile_picture": None,
        "preferences": user_data.preferences.dict() if user_data.preferences else None,
        "created_at": current_time,
        "updated_at": current_time
    }
    
    users_db[user_id] = new_user
    return new_user

async def update_user(user_id: str, user_data):
    """Update an existing user"""
    if user_id not in users_db:
        return None
    
    user = users_db[user_id]
    
    # Update fields
    user["email"] = user_data.email
    user["first_name"] = user_data.first_name
    user["last_name"] = user_data.last_name
    if user_data.preferences:
        user["preferences"] = user_data.preferences.dict()
    
    user["updated_at"] = datetime.utcnow()
    
    return user

async def delete_user(user_id: str):
    """Delete a user"""
    if user_id in users_db:
        del users_db[user_id]
        return True
    return False
