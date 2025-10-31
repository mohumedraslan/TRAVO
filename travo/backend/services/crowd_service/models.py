from sqlalchemy import Column, String, Integer, Float, DateTime, Date, JSON, Enum
from datetime import datetime, date
import uuid

# This would typically import from a shared database configuration
# For now, we'll define a Base class placeholder
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class CrowdPrediction(Base):
    __tablename__ = "crowd_predictions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    location = Column(String, index=True)
    prediction_date = Column(Date, index=True)
    overall_crowd_level = Column(Enum("low", "moderate", "high", "very_high", name="crowd_level"))
    hourly_predictions = Column(JSON)  # List of hourly predictions
    factors = Column(JSON)  # List of factors affecting the prediction
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CrowdHistory(Base):
    __tablename__ = "crowd_history"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    location = Column(String, index=True)
    record_date = Column(Date, index=True)
    average_crowd_level = Column(Enum("low", "moderate", "high", "very_high", name="crowd_level"))
    peak_hours = Column(JSON)  # List of peak hours
    total_visitors = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
