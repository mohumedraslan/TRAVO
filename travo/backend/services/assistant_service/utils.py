import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import re

def generate_conversation_id() -> str:
    """Generate a unique conversation ID"""
    return str(uuid.uuid4())

def generate_message_id() -> str:
    """Generate a unique message ID"""
    return str(uuid.uuid4())

def extract_entities(text: str) -> List[str]:
    """Extract named entities from text
    
    In a real implementation, this would use an NLP model for named entity recognition.
    Here we use a simple regex-based approach for demonstration.
    """
    # Simple pattern matching for common travel entities
    patterns = {
        "cities": ["Paris", "Rome", "Barcelona", "London", "New York", "Tokyo", "Sydney"],
        "landmarks": ["Eiffel Tower", "Louvre", "Colosseum", "Sagrada Familia", "Big Ben", "Statue of Liberty"]
    }
    
    found_entities = []
    
    # Check for each entity in the text
    for category, entities in patterns.items():
        for entity in entities:
            if re.search(r'\b' + re.escape(entity) + r'\b', text, re.IGNORECASE):
                found_entities.append(entity)
    
    return found_entities

def detect_language(text: str) -> str:
    """Detect the language of the text
    
    In a real implementation, this would use a language detection model.
    Here we default to English for demonstration.
    """
    # Default to English
    return "en"

def format_conversation_history(messages: List[Dict]) -> str:
    """Format conversation history for context in AI prompts"""
    formatted_history = ""
    
    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "")
        
        if role and content:
            formatted_history += f"{role.capitalize()}: {content}\n\n"
    
    return formatted_history

def calculate_response_metrics(query: str, response: str) -> Dict:
    """Calculate metrics about the query and response"""
    return {
        "query_length": len(query),
        "response_length": len(response),
        "query_word_count": len(query.split()),
        "response_word_count": len(response.split()),
        "timestamp": datetime.utcnow()
    }

def sanitize_user_input(text: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    # Remove any potential HTML/script tags
    text = re.sub(r'<[^>]*>', '', text)
    
    # Limit length
    max_length = 500
    if len(text) > max_length:
        text = text[:max_length]
    
    return text.strip()
