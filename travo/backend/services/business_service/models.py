from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

# This would be imported from a database module in a real application
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Business(Base):
    __tablename__ = "businesses"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # Enum: restaurant, hotel, attraction, etc.
    description = Column(Text, nullable=True)
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    price_level = Column(String, nullable=True)  # Enum: $, $$, $$$, $$$$
    phone = Column(String, nullable=True)
    website = Column(String, nullable=True)
    email = Column(String, nullable=True)
    hours = Column(JSON, nullable=True)  # JSON object with days of week
    
    # Location information
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=True)
    country = Column(String, nullable=False)
    postal_code = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Additional information
    images = Column(JSON, default=[])
    amenities = Column(JSON, default=[])
    tags = Column(JSON, default=[])
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reviews = relationship("Review", back_populates="business")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(String, primary_key=True)
    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)
    user_id = Column(String, nullable=False)  # Foreign key to users table
    rating = Column(Float, nullable=False)
    content = Column(Text, nullable=False)
    images = Column(JSON, default=[])
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="reviews")
