from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Table, Boolean, JSON, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from travo.backend.database import Base
from .schemas import RecommendationCategory, Season, BudgetLevel


# Association table for destination categories
destination_category = Table(
    'destination_category',
    Base.metadata,
    Column('destination_id', String, ForeignKey('destinations.id')),
    Column('category', String)
)

# Association table for destination seasons
destination_season = Table(
    'destination_season',
    Base.metadata,
    Column('destination_id', String, ForeignKey('destinations.id')),
    Column('season', String)
)

# Association table for destination tags
destination_tag = Table(
    'destination_tag',
    Base.metadata,
    Column('destination_id', String, ForeignKey('destinations.id')),
    Column('tag', String)
)

# Association table for attraction categories
attraction_category = Table(
    'attraction_category',
    Base.metadata,
    Column('attraction_id', String, ForeignKey('attractions.id')),
    Column('category', String)
)

# Association table for attraction tags
attraction_tag = Table(
    'attraction_tag',
    Base.metadata,
    Column('attraction_id', String, ForeignKey('attractions.id')),
    Column('tag', String)
)


class Destination(Base):
    """Model for travel destinations."""
    __tablename__ = "destinations"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    image_url = Column(String)
    rating = Column(Float, default=0.0)
    budget_level = Column(Enum(BudgetLevel), nullable=False)
    popularity_score = Column(Float, default=0.0)
    weather_info = Column(JSON)
    highlights = Column(JSON)  # List of highlights
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    categories = relationship("RecommendationCategory", secondary=destination_category)
    best_time_to_visit = relationship("Season", secondary=destination_season)
    tags = relationship("String", secondary=destination_tag)
    attractions = relationship("Attraction", back_populates="destination")


class Attraction(Base):
    """Model for attractions at destinations."""
    __tablename__ = "attractions"

    id = Column(String, primary_key=True, index=True)
    destination_id = Column(String, ForeignKey("destinations.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    city = Column(String)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    image_url = Column(String)
    rating = Column(Float, default=0.0)
    price_level = Column(Integer)  # 1-4, representing $ to $$$$
    estimated_duration_minutes = Column(Integer)
    best_time_to_visit = Column(JSON)  # List of seasons
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    destination = relationship("Destination", back_populates="attractions")
    categories = relationship("RecommendationCategory", secondary=attraction_category)
    tags = relationship("String", secondary=attraction_tag)


class UserPreferenceRecord(Base):
    """Model for storing user preferences for recommendations."""
    __tablename__ = "user_preferences"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    category = Column(Enum(RecommendationCategory), nullable=False)
    weight = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TravelHistoryRecord(Base):
    """Model for storing user travel history."""
    __tablename__ = "travel_history"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    destination_id = Column(String, ForeignKey("destinations.id"), nullable=False)
    visit_date = Column(DateTime, nullable=False)
    duration_days = Column(Integer, nullable=False)
    rating = Column(Float)
    activities = Column(JSON)  # List of activity IDs
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class RecommendationLog(Base):
    """Model for logging recommendations made to users."""
    __tablename__ = "recommendation_logs"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    recommendation_type = Column(String, nullable=False)  # 'destination', 'attraction', 'personalized'
    items = Column(JSON)  # List of recommended item IDs
    request_params = Column(JSON)  # The parameters used for the recommendation
    created_at = Column(DateTime, default=datetime.utcnow)
    clicked_items = Column(JSON)  # List of item IDs that were clicked by the user
    feedback_rating = Column(Float)  # User feedback on the recommendations
