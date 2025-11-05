from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from .schemas import (
    UserCreate, 
    UserResponse, 
    TokenResponse,
    UserPreferencesResponse,
    UserPreferencesUpdate
)
from .service_logic import (
    create_user, 
    authenticate_user, 
    get_user_preferences,
    update_user_preferences
)
from .database import get_db

# Import JWT utilities
from utils.auth import create_access_token, get_current_user

# Create router
router = APIRouter(prefix="/user", tags=["user"])

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    return create_user(db, user_data)


@router.post("/login", response_model=TokenResponse)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at
        )
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    """Get information about the currently authenticated user."""
    return current_user


@router.get("/preferences", response_model=UserPreferencesResponse)
async def get_preferences(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Get preferences for the current user."""
    preferences = get_user_preferences(db, current_user.id)
    
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferences not found"
        )
    
    # Convert JSON strings to Python objects
    return UserPreferencesResponse(
        user_id=preferences.user_id,
        interests=preferences.get_interests(),
        preferred_cities=preferences.get_preferred_cities(),
        saved_itineraries=preferences.get_saved_itineraries(),
        preferred_language=preferences.preferred_language,
        notification_settings=preferences.get_notification_settings(),
        additional_settings=preferences.get_additional_settings(),
        updated_at=preferences.updated_at or preferences.created_at
    )


@router.put("/preferences", response_model=UserPreferencesResponse)
async def update_preferences(
    preferences_data: UserPreferencesUpdate,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """Update preferences for the current user."""
    updated_preferences = update_user_preferences(db, current_user.id, preferences_data)
    
    # Convert JSON strings to Python objects
    return UserPreferencesResponse(
        user_id=updated_preferences.user_id,
        interests=updated_preferences.get_interests(),
        preferred_cities=updated_preferences.get_preferred_cities(),
        saved_itineraries=updated_preferences.get_saved_itineraries(),
        preferred_language=updated_preferences.preferred_language,
        notification_settings=updated_preferences.get_notification_settings(),
        additional_settings=updated_preferences.get_additional_settings(),
        updated_at=updated_preferences.updated_at or updated_preferences.created_at
    )