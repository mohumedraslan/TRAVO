import uuid
import random
from datetime import datetime
from typing import List, Dict, Any, Optional

# Mock data for attractions to use as sources
ATTRACTIONS = [
    {
        "id": "eiffel-tower",
        "name": "Eiffel Tower",
        "city": "Paris",
        "country": "France",
        "description": "Iconic wrought-iron lattice tower on the Champ de Mars in Paris."
    },
    {
        "id": "louvre-museum",
        "name": "Louvre Museum",
        "city": "Paris",
        "country": "France",
        "description": "World's largest art museum and a historic monument in Paris."
    },
    {
        "id": "colosseum",
        "name": "Colosseum",
        "city": "Rome",
        "country": "Italy",
        "description": "Oval amphitheatre in the centre of the city of Rome."
    },
    {
        "id": "sagrada-familia",
        "name": "Sagrada Familia",
        "city": "Barcelona",
        "country": "Spain",
        "description": "Large unfinished basilica designed by Antoni Gaudí."
    }
]

# Mock conversation data
CONVERSATIONS = {}

async def process_text_query(
    query: str,
    user_id: Optional[str] = None,
    conversation_id: Optional[str] = None,
    location: Optional[Dict] = None,
    language: str = "en"
) -> Dict:
    """Process a text query and generate a response
    
    In a real implementation, this would:
    1. Use an NLP model to understand the query
    2. Retrieve relevant information from a knowledge base
    3. Generate a natural language response
    """
    # Generate a new conversation ID if not provided
    if not conversation_id:
        conversation_id = str(uuid.uuid4())
    
    # Generate a message ID
    message_id = str(uuid.uuid4())
    
    # Store the user message in the conversation history
    if conversation_id not in CONVERSATIONS:
        CONVERSATIONS[conversation_id] = {
            "user_id": user_id,
            "messages": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    
    # Add user message to history
    CONVERSATIONS[conversation_id]["messages"].append({
        "role": "user",
        "content": query,
        "message_type": "text",
        "timestamp": datetime.utcnow()
    })
    
    # Update conversation timestamp
    CONVERSATIONS[conversation_id]["updated_at"] = datetime.utcnow()
    
    # Generate a mock response based on the query
    response_text = generate_mock_response(query, location)
    
    # Add assistant message to history
    CONVERSATIONS[conversation_id]["messages"].append({
        "role": "assistant",
        "content": response_text,
        "message_type": "text",
        "timestamp": datetime.utcnow()
    })
    
    # Get related attractions based on the query
    related_attractions = get_related_attractions(query)
    
    # Generate mock sources
    sources = generate_mock_sources(query)
    
    return {
        "response_text": response_text,
        "conversation_id": conversation_id,
        "message_id": message_id,
        "sources": sources,
        "related_attractions": related_attractions,
        "timestamp": datetime.utcnow()
    }

async def process_voice_query(
    audio_content: bytes,
    user_id: Optional[str] = None,
    conversation_id: Optional[str] = None,
    language: str = "en",
    location: Optional[Dict] = None
) -> Dict:
    """Process a voice query and generate a response
    
    In a real implementation, this would:
    1. Use a speech-to-text model to transcribe the audio
    2. Process the transcribed text using NLP
    3. Generate a text response
    4. Convert the text response to speech
    """
    # Mock transcription (in a real system, this would use a speech-to-text model)
    transcription = "Tell me about the Eiffel Tower"
    
    # Process the transcribed text
    text_response = await process_text_query(
        query=transcription,
        user_id=user_id,
        conversation_id=conversation_id,
        location=location,
        language=language
    )
    
    # In a real system, we would generate audio from the response text
    # and store it at a URL. Here we'll just use a mock URL.
    audio_url = f"https://api.travo.com/audio/{text_response['message_id']}.mp3"
    
    return {
        **text_response,
        "audio_url": audio_url,
        "transcription": transcription
    }

async def get_conversation_history(
    conversation_id: str,
    limit: int = 10
) -> Optional[Dict]:
    """Get the conversation history for a specific conversation"""
    if conversation_id not in CONVERSATIONS:
        return None
    
    conversation = CONVERSATIONS[conversation_id]
    
    # Limit the number of messages returned
    messages = conversation["messages"][-limit:] if limit > 0 else conversation["messages"]
    
    return {
        "conversation_id": conversation_id,
        "user_id": conversation["user_id"],
        "messages": messages,
        "created_at": conversation["created_at"],
        "updated_at": conversation["updated_at"]
    }

def generate_mock_response(query: str, location: Optional[Dict] = None) -> str:
    """Generate a mock response based on the query"""
    query_lower = query.lower()
    
    # Simple keyword matching for demo purposes
    if "eiffel" in query_lower or "tower" in query_lower:
        return "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel, whose company designed and built the tower. It was constructed from 1887 to 1889 as the entrance to the 1889 World's Fair and is now one of the most recognizable structures in the world."
    
    elif "louvre" in query_lower or "museum" in query_lower:
        return "The Louvre Museum is the world's largest art museum and a historic monument in Paris, France. A central landmark of the city, it is located on the Right Bank of the Seine. Approximately 38,000 objects from prehistory to the 21st century are exhibited over an area of 72,735 square meters."
    
    elif "colosseum" in query_lower or "rome" in query_lower:
        return "The Colosseum is an oval amphitheatre in the centre of the city of Rome, Italy. It is the largest ancient amphitheatre ever built, and is still the largest standing amphitheatre in the world today, despite its age. Construction began under the emperor Vespasian in AD 72 and was completed in AD 80 under his successor and heir, Titus."
    
    elif "sagrada" in query_lower or "familia" in query_lower or "barcelona" in query_lower:
        return "The Sagrada Familia is a large unfinished basilica in Barcelona, designed by Catalan architect Antoni Gaudí. Construction began in 1882 and is still ongoing, with an anticipated completion date of 2026, the centenary of Gaudí's death. The basilica is a UNESCO World Heritage Site and is known for its unique architectural style that combines Gothic and Art Nouveau elements."
    
    elif "weather" in query_lower and location:
        return f"The current weather at your location (latitude: {location.get('latitude')}, longitude: {location.get('longitude')}) is sunny with a temperature of 25°C (77°F). The forecast for the next few days shows clear skies with temperatures ranging from 20°C to 28°C (68°F to 82°F)."
    
    else:
        return "I'm your TRAVO assistant, here to help with information about travel destinations, attractions, and local tips. How can I assist you with your travel plans today?"

def get_related_attractions(query: str) -> List[Dict]:
    """Get related attractions based on the query"""
    query_lower = query.lower()
    
    # Simple keyword matching for demo purposes
    if "paris" in query_lower or "france" in query_lower or "eiffel" in query_lower:
        return [a for a in ATTRACTIONS if a["country"] == "France"]
    
    elif "rome" in query_lower or "italy" in query_lower or "colosseum" in query_lower:
        return [a for a in ATTRACTIONS if a["country"] == "Italy"]
    
    elif "barcelona" in query_lower or "spain" in query_lower or "sagrada" in query_lower:
        return [a for a in ATTRACTIONS if a["country"] == "Spain"]
    
    else:
        # Return a random selection of attractions
        return random.sample(ATTRACTIONS, min(2, len(ATTRACTIONS)))

def generate_mock_sources(query: str) -> List[Dict]:
    """Generate mock sources for the response"""
    query_lower = query.lower()
    
    sources = []
    
    # Add Wikipedia as a source
    if "eiffel" in query_lower or "tower" in query_lower:
        sources.append({
            "source_type": "website",
            "title": "Eiffel Tower - Wikipedia",
            "url": "https://en.wikipedia.org/wiki/Eiffel_Tower",
            "snippet": "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France."
        })
    
    elif "louvre" in query_lower or "museum" in query_lower:
        sources.append({
            "source_type": "website",
            "title": "Louvre Museum - Wikipedia",
            "url": "https://en.wikipedia.org/wiki/Louvre",
            "snippet": "The Louvre, or the Louvre Museum, is the world's most-visited museum and a historic monument in Paris, France."
        })
    
    elif "colosseum" in query_lower or "rome" in query_lower:
        sources.append({
            "source_type": "website",
            "title": "Colosseum - Wikipedia",
            "url": "https://en.wikipedia.org/wiki/Colosseum",
            "snippet": "The Colosseum is an oval amphitheatre in the centre of the city of Rome, Italy."
        })
    
    elif "sagrada" in query_lower or "familia" in query_lower or "barcelona" in query_lower:
        sources.append({
            "source_type": "website",
            "title": "Sagrada Família - Wikipedia",
            "url": "https://en.wikipedia.org/wiki/Sagrada_Fam%C3%ADlia",
            "snippet": "The Basílica i Temple Expiatori de la Sagrada Família is a church in Barcelona, Spain, designed by Catalan architect Antoni Gaudí."
        })
    
    # Add a travel guide as a source
    sources.append({
        "source_type": "article",
        "title": "TRAVO Travel Guide",
        "url": "https://travo.com/guides/europe",
        "snippet": "Comprehensive travel guide to the most popular destinations in Europe."
    })
    
    return sources
