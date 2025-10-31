from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

# Import schemas and service logic
from .schemas import UserCreate, UserResponse
from .service_logic import get_user, create_user, get_all_users

# Create router
router = APIRouter()

# Test route
@router.get("/test")
async def test_user_service():
    return {"status": "ok", "service": "user_service"}

# Get all users
@router.get("/", response_model=List[UserResponse])
async def read_users():
    return await get_all_users()

# Get user by ID
@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: str):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Create new user
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreate):
    return await create_user(user)
