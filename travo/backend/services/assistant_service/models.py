from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime

# This would be imported from a database module in a real application
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    language = Column(String, default="en")
    metadata = Column(JSON, default={})
    
    # Relationship with messages
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    message_type = Column(String, default="text")  # text, voice
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Audio metadata for voice messages
    audio_url = Column(String, nullable=True)
    audio_duration_seconds = Column(Float, nullable=True)
    transcription = Column(Text, nullable=True)
    
    # Relationship with conversation
    conversation = relationship("Conversation", back_populates="messages")
    
    # Relationship with sources
    sources = relationship("MessageSource", back_populates="message")

class MessageSource(Base):
    __tablename__ = "message_sources"
    
    id = Column(String, primary_key=True)
    message_id = Column(String, ForeignKey("messages.id"), nullable=False)
    source_type = Column(String, nullable=False)  # attraction, article, website
    source_id = Column(String, nullable=True)  # ID of the source if it's an internal entity
    title = Column(String)
    url = Column(String, nullable=True)
    snippet = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with message
    message = relationship("Message", back_populates="sources")
