from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import json
from typing import List, Dict, Any

Base = declarative_base()


class User(Base):
    """SQLAlchemy model for users table."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationship with UserPreferences
    preferences = relationship("UserPreferences", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"


class UserPreferences(Base):
    """SQLAlchemy model for user_preferences table."""
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    interests = Column(JSON, default=lambda: json.dumps([]))
    preferred_cities = Column(JSON, default=lambda: json.dumps([]))
    saved_itineraries = Column(JSON, default=lambda: json.dumps([]))
    preferred_language = Column(String(10), nullable=True)
    notification_settings = Column(JSON, default=lambda: json.dumps({
        "email_notifications": True,
        "push_notifications": True,
        "crowd_alerts": False
    }))
    additional_settings = Column(JSON, default=lambda: json.dumps({}))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship with User
    user = relationship("User", back_populates="preferences")
    
    def __repr__(self):
        return f"<UserPreferences(user_id={self.user_id})>"
    
    # Helper methods for JSON fields
    def get_interests(self) -> List[str]:
        return json.loads(self.interests) if isinstance(self.interests, str) else self.interests
    
    def set_interests(self, interests: List[str]) -> None:
        self.interests = json.dumps(interests) if interests else json.dumps([])
    
    def get_preferred_cities(self) -> List[str]:
        return json.loads(self.preferred_cities) if isinstance(self.preferred_cities, str) else self.preferred_cities
    
    def set_preferred_cities(self, cities: List[str]) -> None:
        self.preferred_cities = json.dumps(cities) if cities else json.dumps([])
    
    def get_saved_itineraries(self) -> List[int]:
        return json.loads(self.saved_itineraries) if isinstance(self.saved_itineraries, str) else self.saved_itineraries
    
    def set_saved_itineraries(self, itineraries: List[int]) -> None:
        self.saved_itineraries = json.dumps(itineraries) if itineraries else json.dumps([])
    
    def get_notification_settings(self) -> Dict[str, bool]:
        return json.loads(self.notification_settings) if isinstance(self.notification_settings, str) else self.notification_settings
    
    def set_notification_settings(self, settings: Dict[str, bool]) -> None:
        default_settings = {
            "email_notifications": True,
            "push_notifications": True,
            "crowd_alerts": False
        }
        merged_settings = {**default_settings, **settings}
        self.notification_settings = json.dumps(merged_settings)
    
    def get_additional_settings(self) -> Dict[str, Any]:
        return json.loads(self.additional_settings) if isinstance(self.additional_settings, str) else self.additional_settings
    
    def set_additional_settings(self, settings: Dict[str, Any]) -> None:
        self.additional_settings = json.dumps(settings) if settings else json.dumps({})
