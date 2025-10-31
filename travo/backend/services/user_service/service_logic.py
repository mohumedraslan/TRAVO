from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import json

from .models import User, UserPreferences
from .schemas import UserCreate, UserPreferencesCreate, UserPreferencesUpdate

# Password hashing
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash a password for storing."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a stored password against a provided password."""
    return pwd_context.verify(plain_password, hashed_password)


def create_user(db: Session, user_data: UserCreate) -> User:
    """Create a new user in the database."""
    # Check if user with this email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user with hashed password
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_password
    )
    
    try:
        # Add user to database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Create default preferences for the user
        create_default_preferences(db, db_user.id)
        
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating user"
        )


def create_default_preferences(db: Session, user_id: int) -> UserPreferences:
    """Create default preferences for a new user."""
    default_preferences = UserPreferences(
        user_id=user_id,
        interests=json.dumps([]),
        preferred_cities=json.dumps([]),
        saved_itineraries=json.dumps([]),
        notification_settings=json.dumps({
            "email_notifications": True,
            "push_notifications": True,
            "crowd_alerts": False
        }),
        additional_settings=json.dumps({})
    )
    
    db.add(default_preferences)
    db.commit()
    db.refresh(default_preferences)
    return default_preferences


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password."""
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        return None
    
    if not verify_password(password, user.password_hash):
        return None
    
    return user


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get a user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a user by email."""
    return db.query(User).filter(User.email == email).first()


def get_user_preferences(db: Session, user_id: int) -> Optional[UserPreferences]:
    """Get preferences for a user."""
    return db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()


def update_user_preferences(db: Session, user_id: int, preferences: UserPreferencesUpdate) -> UserPreferences:
    """Update preferences for a user."""
    db_preferences = get_user_preferences(db, user_id)
    
    if not db_preferences:
        # Create preferences if they don't exist
        db_preferences = UserPreferences(user_id=user_id)
        db.add(db_preferences)
    
    # Update fields
    if preferences.interests is not None:
        db_preferences.interests = json.dumps([interest.value for interest in preferences.interests])
    
    if preferences.preferred_cities is not None:
        db_preferences.preferred_cities = json.dumps(preferences.preferred_cities)
    
    if preferences.saved_itineraries is not None:
        db_preferences.saved_itineraries = json.dumps(preferences.saved_itineraries)
    
    if preferences.preferred_language is not None:
        db_preferences.preferred_language = preferences.preferred_language
    
    if preferences.notification_settings is not None:
        # Merge with existing settings
        current_settings = json.loads(db_preferences.notification_settings) \
            if isinstance(db_preferences.notification_settings, str) \
            else db_preferences.notification_settings or {}
        
        merged_settings = {**current_settings, **preferences.notification_settings}
        db_preferences.notification_settings = json.dumps(merged_settings)
    
    if preferences.additional_settings is not None:
        # Merge with existing settings
        current_settings = json.loads(db_preferences.additional_settings) \
            if isinstance(db_preferences.additional_settings, str) \
            else db_preferences.additional_settings or {}
        
        merged_settings = {**current_settings, **preferences.additional_settings}
        db_preferences.additional_settings = json.dumps(merged_settings)
    
    # Update timestamp
    db_preferences.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_preferences)
    return db_preferences
