import json
import os
import random
import base64
import logging
from typing import Dict, List, Optional, Tuple, Any

# For AI text processing
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

# For voice processing
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    import io
    from TTS.api import TTS
    COQUI_TTS_AVAILABLE = True
except ImportError:
    COQUI_TTS_AVAILABLE = False

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path to the monument data
MONUMENT_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "vision_service",
    "labels.json"
)

# Monument context database with additional information
MONUMENT_CONTEXT = {
    "Temple of Luxor": {
        "description": "An ancient Egyptian temple complex located on the east bank of the Nile River in Luxor (ancient Thebes). It was constructed around 1400 BCE.",
        "visiting_tips": "Best visited early morning or late afternoon to avoid the heat. Hire a guide for historical context. The sound and light show in the evening is recommended.",
        "historical_period": "New Kingdom of Egypt",
        "facts": [
            "Built mainly by Amenhotep III and Ramesses II",
            "Connected to Karnak Temple by an avenue of sphinxes",
            "Features massive statues of Ramesses II at the entrance"
        ]
    },
    "Pyramids of Giza": {
        "description": "A complex of ancient Egyptian pyramids located on the Giza plateau, including the Great Pyramid of Khufu, one of the Seven Wonders of the Ancient World.",
        "visiting_tips": "Visit early to avoid crowds and heat. Consider hiring a guide. Be prepared for persistent vendors. The sound and light show at night offers a different perspective.",
        "historical_period": "Old Kingdom of Egypt",
        "facts": [
            "The Great Pyramid was built for Pharaoh Khufu around 2560 BCE",
            "Originally covered in polished limestone casing stones",
            "The Sphinx guards the pyramid complex"
        ]
    },
    "Parthenon": {
        "description": "A former temple dedicated to the goddess Athena, located on the Acropolis of Athens, Greece. It was built in the 5th century BCE.",
        "visiting_tips": "Visit early or late in the day to avoid crowds. Wear comfortable shoes and bring water. The Acropolis Museum nearby is worth visiting to see original sculptures.",
        "historical_period": "Classical Greece",
        "facts": [
            "Designed by architects Ictinus and Callicrates",
            "Supervised by the sculptor Phidias",
            "Converted to a church in the 6th century CE"
        ]
    },
    "Colosseum": {
        "description": "An oval amphitheatre in the center of Rome, Italy. It is the largest ancient amphitheatre ever built and is still the largest standing amphitheatre in the world today.",
        "visiting_tips": "Book tickets online in advance to skip lines. Consider a guided tour to learn about the history. Visit early or late in the day to avoid crowds.",
        "historical_period": "Ancient Rome",
        "facts": [
            "Construction began under Emperor Vespasian in 72 CE",
            "Could hold between 50,000-80,000 spectators",
            "Used for gladiatorial contests and public spectacles"
        ]
    },
    "Taj Mahal": {
        "description": "An ivory-white marble mausoleum on the right bank of the river Yamuna in Agra, India. It was commissioned in 1632 by the Mughal emperor Shah Jahan to house the tomb of his favorite wife.",
        "visiting_tips": "Visit at sunrise for the best experience and fewer crowds. Wear shoe covers provided or go barefoot inside the mausoleum. Photography is not allowed inside the main structure.",
        "historical_period": "Mughal Empire",
        "facts": [
            "Built over approximately 22 years",
            "Designed by architect Ustad Ahmad Lahauri",
            "Incorporates Persian, Islamic, and Indian architectural styles"
        ]
    },
    "Great Wall of China": {
        "description": "A series of fortifications built along the northern borders of ancient Chinese states and Imperial China as protection against nomadic groups.",
        "visiting_tips": "The Mutianyu and Jinshanling sections are less crowded than Badaling. Wear comfortable shoes and bring water. Consider visiting in spring or autumn for the best weather.",
        "historical_period": "Various Chinese Dynasties",
        "facts": [
            "Construction began in the 7th century BCE",
            "The majority of the existing wall was built during the Ming Dynasty",
            "Total length is approximately 13,171 miles"
        ]
    },
    "Machu Picchu": {
        "description": "An Incan citadel set high in the Andes Mountains in Peru, above the Urubamba River valley. Built in the 15th century and later abandoned.",
        "visiting_tips": "Book tickets well in advance. Consider hiking the Inca Trail for a more immersive experience. Visit early morning for fewer crowds and better lighting for photos.",
        "historical_period": "Inca Empire",
        "facts": [
            "Built around 1450 CE",
            "Abandoned during the Spanish conquest",
            "Rediscovered by Hiram Bingham in 1911"
        ]
    },
    "Stonehenge": {
        "description": "A prehistoric monument consisting of a ring of standing stones, each around 13 feet high, seven feet wide, and weighing around 25 tons. Located in Wiltshire, England.",
        "visiting_tips": "Book tickets in advance. Visit during sunrise or sunset for a magical experience. The visitor center provides valuable context about the monument's history.",
        "historical_period": "Neolithic and Bronze Age",
        "facts": [
            "Constructed between 3000 BCE to 2000 BCE",
            "Aligned with the movements of the sun",
            "The stones were transported from over 140 miles away"
        ]
    },
    "Angkor Wat": {
        "description": "A temple complex in Cambodia and the largest religious monument in the world by land area. Originally constructed as a Hindu temple dedicated to Vishnu, it was gradually transformed into a Buddhist temple.",
        "visiting_tips": "Purchase a multi-day pass to explore the entire complex. Hire a guide for historical context. Visit at sunrise for iconic photos. Dress respectfully as it's an active religious site.",
        "historical_period": "Khmer Empire",
        "facts": [
            "Built in the early 12th century by King Suryavarman II",
            "Covers an area of 402 acres",
            "Depicted on Cambodia's national flag"
        ]
    },
    "Statue of Liberty": {
        "description": "A colossal neoclassical sculpture on Liberty Island in New York Harbor. A gift from the people of France to the people of the United States.",
        "visiting_tips": "Reserve crown access tickets months in advance. Security screening is similar to airports. The museum on Liberty Island provides historical context about the statue's creation.",
        "historical_period": "Modern Era",
        "facts": [
            "Dedicated on October 28, 1886",
            "Designed by French sculptor Frédéric Auguste Bartholdi",
            "The internal structure was designed by Gustave Eiffel"
        ]
    }
}


def load_monument_data() -> List[Dict[str, str]]:
    """Load monument data from the labels.json file."""
    try:
        with open(MONUMENT_DATA_PATH, 'r') as f:
            data = json.load(f)
            return data.get("monuments", [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error loading monument data: {e}")
        return []


def get_ai_response(query: str, location: Optional[str] = None) -> Dict[str, Any]:
    """Generate an AI response to the user's query.
    
    Args:
        query: The user's question or query
        location: Optional location context
        
    Returns:
        Dictionary containing the answer, related monuments, and confidence score
    """
    # Load monument data
    monuments = load_monument_data()
    monument_names = [m["name"] for m in monuments]
    
    # Check if we have OpenAI or Transformers available
    if OPENAI_AVAILABLE and os.environ.get("OPENAI_API_KEY"):
        return get_openai_response(query, location, monument_names)
    elif TRANSFORMERS_AVAILABLE:
        return get_transformers_response(query, location, monument_names)
    else:
        return get_rule_based_response(query, location, monument_names)


def get_openai_response(query: str, location: Optional[str], monument_names: List[str]) -> Dict[str, Any]:
    """Generate a response using OpenAI API."""
    try:
        # Set up the OpenAI client
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # Create context from monument data
        context = "Information about monuments:\n"
        for name in monument_names:
            if name in MONUMENT_CONTEXT:
                info = MONUMENT_CONTEXT[name]
                context += f"- {name}: {info['description']}\n"
        
        # Add location context if provided
        location_context = f"\nThe user is currently at or interested in: {location}" if location else ""
        
        # Create the prompt
        prompt = f"{context}{location_context}\n\nUser question: {query}\n\nProvide a concise, conversational answer about the monument, its history, or visiting tips. If the question is not about a monument, politely explain you can only answer questions about famous monuments."
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful travel assistant specializing in historical monuments."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        # Extract the answer
        answer = response.choices[0].message.content.strip()
        
        # Identify related monuments
        related_monuments = [name for name in monument_names if name.lower() in answer.lower() or name.lower() in query.lower()]
        
        return {
            "answer": answer,
            "related_monuments": related_monuments,
            "confidence": 0.95  # High confidence for OpenAI responses
        }
    
    except Exception as e:
        logger.error(f"Error with OpenAI API: {e}")
        # Fall back to rule-based response
        return get_rule_based_response(query, location, monument_names)


def get_transformers_response(query: str, location: Optional[str], monument_names: List[str]) -> Dict[str, Any]:
    """Generate a response using Hugging Face Transformers."""
    try:
        # Load question-answering pipeline
        qa_pipeline = pipeline("question-answering")
        
        # Create context from monument data
        context = "Information about monuments: "
        for name in monument_names:
            if name in MONUMENT_CONTEXT:
                info = MONUMENT_CONTEXT[name]
                context += f"{name}: {info['description']}. "
        
        # Add visiting tips for likely monuments
        for name in monument_names:
            if name.lower() in query.lower() and name in MONUMENT_CONTEXT:
                context += f"Visiting tips for {name}: {MONUMENT_CONTEXT[name]['visiting_tips']}. "
        
        # Add location context if provided
        if location:
            context += f"The user is currently at or interested in: {location}. "
        
        # Get response from model
        result = qa_pipeline(question=query, context=context)
        
        # Identify related monuments
        related_monuments = [name for name in monument_names if name.lower() in result["answer"].lower() or name.lower() in query.lower()]
        
        return {
            "answer": result["answer"],
            "related_monuments": related_monuments,
            "confidence": float(result["score"])
        }
    
    except Exception as e:
        logger.error(f"Error with Transformers: {e}")
        # Fall back to rule-based response
        return get_rule_based_response(query, location, monument_names)


def get_rule_based_response(query: str, location: Optional[str], monument_names: List[str]) -> Dict[str, Any]:
    """Generate a rule-based response when AI services are unavailable."""
    query_lower = query.lower()
    
    # Identify mentioned monuments
    mentioned_monuments = [name for name in monument_names if name.lower() in query_lower]
    
    # If location is provided, add it to potential monuments
    if location:
        location_monuments = [name for name in monument_names if location.lower() in name.lower()]
        mentioned_monuments.extend(location_monuments)
    
    # Remove duplicates
    mentioned_monuments = list(set(mentioned_monuments))
    
    # If no monuments mentioned, provide a general response
    if not mentioned_monuments:
        general_responses = [
            "I can provide information about famous monuments like the Pyramids of Giza, Taj Mahal, or Statue of Liberty. Could you specify which monument you're interested in?",
            "I specialize in information about historical monuments. Please ask about a specific monument like the Temple of Luxor or Stonehenge.",
            "I don't have information about that, but I can tell you about famous monuments such as the Colosseum, Angkor Wat, or the Great Wall of China."
        ]
        return {
            "answer": random.choice(general_responses),
            "related_monuments": [],
            "confidence": 0.5
        }
    
    # Select the first mentioned monument
    monument = mentioned_monuments[0]
    info = MONUMENT_CONTEXT.get(monument, {})
    
    # Determine what information to provide based on the query
    if "visit" in query_lower or "tips" in query_lower or "advice" in query_lower:
        if "visiting_tips" in info:
            answer = f"For visiting {monument}: {info['visiting_tips']}"
            confidence = 0.8
        else:
            answer = f"I don't have specific visiting tips for {monument}, but it's best to research opening hours and ticket information before your visit."
            confidence = 0.6
    
    elif "history" in query_lower or "built" in query_lower or "ancient" in query_lower or "old" in query_lower:
        if "historical_period" in info and "facts" in info:
            answer = f"{monument} was built during the {info['historical_period']}. {random.choice(info['facts'])}"
            confidence = 0.8
        else:
            answer = f"{monument} is a famous historical landmark. Unfortunately, I don't have detailed historical information about it."
            confidence = 0.6
    
    elif "what is" in query_lower or "tell me about" in query_lower or "describe" in query_lower:
        if "description" in info:
            answer = info["description"]
            confidence = 0.9
        else:
            answer = f"{monument} is a famous landmark, but I don't have detailed information about it."
            confidence = 0.6
    
    else:
        # General information about the monument
        if "description" in info:
            answer = f"{info['description']} {random.choice(info.get('facts', ['']))}"
            confidence = 0.7
        else:
            answer = f"{monument} is a famous landmark. I recommend researching more about its history and significance before visiting."
            confidence = 0.5
    
    return {
        "answer": answer,
        "related_monuments": mentioned_monuments,
        "confidence": confidence
    }


def voice_to_text(audio_data_base64: str, language: str = "en-US") -> Dict[str, Any]:
    """Convert voice audio to text.
    
    Args:
        audio_data_base64: Base64 encoded audio data
        language: Language code for speech recognition
        
    Returns:
        Dictionary containing transcribed text and confidence score
    """
    if not SPEECH_RECOGNITION_AVAILABLE:
        return {
            "text": "Speech recognition is not available. Please install the speech_recognition package.",
            "confidence": 0.0
        }
    
    try:
        # Decode base64 audio data
        audio_data = base64.b64decode(audio_data_base64)
        
        # Create a temporary audio file
        temp_file = "temp_audio.wav"
        with open(temp_file, "wb") as f:
            f.write(audio_data)
        
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Load audio file
        with sr.AudioFile(temp_file) as source:
            audio = recognizer.record(source)
        
        # Perform speech recognition
        text = recognizer.recognize_google(audio, language=language)
        
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        return {
            "text": text,
            "confidence": 0.8  # Approximate confidence
        }
    
    except sr.UnknownValueError:
        return {
            "text": "Could not understand audio",
            "confidence": 0.0
        }
    except sr.RequestError as e:
        logger.error(f"Speech recognition service error: {e}")
        return {
            "text": "Speech recognition service unavailable",
            "confidence": 0.0
        }
    except Exception as e:
        logger.error(f"Error in voice to text conversion: {e}")
        return {
            "text": "Error processing audio",
            "confidence": 0.0
        }
    finally:
        # Ensure temporary file is removed
        if os.path.exists(temp_file):
            os.remove(temp_file)


def text_to_voice(text: str, language: str = "en", voice: Optional[str] = None) -> Dict[str, Any]:
    """Convert text to voice audio.
    
    Args:
        text: Text to convert to speech
        language: Language code for text-to-speech
        voice: Voice ID or name for text-to-speech
        
    Returns:
        Dictionary containing base64 encoded audio data and format
    """
    # Try using Coqui TTS first (higher quality)
    if COQUI_TTS_AVAILABLE:
        try:
            # Initialize TTS with appropriate model
            tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
            
            # Create an in-memory file-like object
            audio_buffer = io.BytesIO()
            
            # Generate speech
            tts.tts_to_file(text=text, file_path=audio_buffer)
            
            # Get the audio data and encode as base64
            audio_buffer.seek(0)
            audio_data_base64 = base64.b64encode(audio_buffer.read()).decode("utf-8")
            
            return {
                "audio_data": audio_data_base64,
                "format": "wav"
            }
        
        except Exception as e:
            logger.error(f"Error with Coqui TTS: {e}")
            # Fall back to gTTS
    
    # Fall back to gTTS
    if GTTS_AVAILABLE:
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Create an in-memory file-like object
            audio_buffer = io.BytesIO()
            
            # Save the audio to the buffer
            tts.write_to_fp(audio_buffer)
            
            # Get the audio data and encode as base64
            audio_buffer.seek(0)
            audio_data_base64 = base64.b64encode(audio_buffer.read()).decode("utf-8")
            
            return {
                "audio_data": audio_data_base64,
                "format": "mp3"
            }
        
        except Exception as e:
            logger.error(f"Error with gTTS: {e}")
    
    # If both TTS options fail, return an error
    return {
        "audio_data": "",
        "format": "none",
        "error": "Text-to-speech conversion is not available. Please install gTTS or Coqui TTS."
    }
