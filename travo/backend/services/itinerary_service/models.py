from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Boolean, Text, Time
from sqlalchemy.orm import relationship
from datetime import datetime

from travo.backend.database import Base


class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    destination = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    budget_level = Column(String, nullable=True)  # budget, moderate, luxury
    tags = Column(JSON, default=list)
    cover_image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    activities = relationship("ItineraryActivity", back_populates="itinerary", cascade="all, delete-orphan")
    shares = relationship("ItineraryShare", back_populates="itinerary", cascade="all, delete-orphan")


class ItineraryActivity(Base):
    __tablename__ = "itinerary_activities"

    id = Column(String, primary_key=True, index=True)
    itinerary_id = Column(String, ForeignKey("itineraries.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    activity_type = Column(String, nullable=False)  # attraction, restaurant, hotel, transportation, event, other
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    day_index = Column(Integer, nullable=False)  # 0-indexed day number in the itinerary
    location = Column(JSON, nullable=True)  # {address, city, country, latitude, longitude}
    transportation = Column(JSON, nullable=True)  # {type, departure_location, arrival_location, booking_reference, booking_url, notes}
    booking_info = Column(JSON, nullable=True)  # Any booking-related information
    cost = Column(Float, nullable=True)
    currency = Column(String, default="USD")
    notes = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    external_url = Column(String, nullable=True)
    tags = Column(JSON, default=list)
    order_index = Column(Integer, default=0)  # For ordering activities within a day
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    itinerary = relationship("Itinerary", back_populates="activities")


class ItineraryShare(Base):
    __tablename__ = "itinerary_shares"

    id = Column(String, primary_key=True, index=True)  # share_id
    itinerary_id = Column(String, ForeignKey("itineraries.id", ondelete="CASCADE"), nullable=False)
    expires_at = Column(DateTime, nullable=True)  # NULL means no expiration
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    itinerary = relationship("Itinerary", back_populates="shares")
