from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime

# This would be imported from a database module in a real application
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Monument(Base):
    __tablename__ = "monuments"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    country = Column(String)
    city = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    year_built = Column(Integer, nullable=True)
    historical_period = Column(String, nullable=True)
    architect = Column(String, nullable=True)
    style = Column(String, nullable=True)
    height_meters = Column(Float, nullable=True)
    fun_facts = Column(JSON, default=[])
    image_urls = Column(JSON, default=[])
    wikipedia_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DetectionLog(Base):
    __tablename__ = "detection_logs"
    
    id = Column(String, primary_key=True)
    image_hash = Column(String, nullable=False)
    detected_monuments = Column(JSON, default=[])
    processing_time_ms = Column(Float)
    user_id = Column(String, nullable=True)  # If the user is authenticated
    device_info = Column(JSON, nullable=True)  # Optional device information
    created_at = Column(DateTime, default=datetime.utcnow)
