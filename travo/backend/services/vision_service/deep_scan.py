
import os
import logging
import base64
import json

logger = logging.getLogger(__name__)

# Third-party libraries
try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from openai import AsyncOpenAI
except ImportError:
    AsyncOpenAI = None

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Prompt for monument identification
IDENTIFY_PROMPT = """
Analyze this image and identify if it contains a monument, landmark, or famous building.
Be SPECIFIC - identify the exact monument (e.g., "Pyramids of Giza" not just "pyramid", "Eiffel Tower" not "tower").

Return a JSON object with this exact structure:
{
    "identified_monument": "Exact name of the monument or 'Unknown'",
    "confidence": 0.0 to 1.0,
    "description": "2-3 sentence description",
    "fun_fact": "One interesting fact",
    "location": "City, Country"
}

Do not include markdown code blocks.
"""

# Gemini models to try in order (main + fallbacks)
GEMINI_MODELS = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-exp",
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
]

async def deep_analyze_image(image_bytes: bytes) -> dict:
    """
    Primary vision analysis using Gemini with multiple fallbacks.
    Returns standardized identification result.
    """
    
    # 1. Try Gemini (Google) with fallbacks
    if GEMINI_API_KEY and genai:
        genai.configure(api_key=GEMINI_API_KEY)
        
        for model_name in GEMINI_MODELS:
            try:
                logger.info(f"Vision: Trying {model_name}...")
                model = genai.GenerativeModel(model_name)
                
                response = await model.generate_content_async([
                    {'mime_type': 'image/jpeg', 'data': image_bytes},
                    IDENTIFY_PROMPT
                ])
                
                text_resp = response.text.replace('```json', '').replace('```', '').strip()
                result = json.loads(text_resp)
                logger.info(f"✅ {model_name} identified: {result.get('identified_monument')}")
                return result
                
            except Exception as e:
                logger.warning(f"❌ {model_name} failed: {e}")
                continue
        
        logger.error("All Gemini models failed")

    # 2. Try OpenAI (GPT-4o) as final fallback
    if OPENAI_API_KEY and AsyncOpenAI:
        try:
            logger.info("Vision: Falling back to OpenAI GPT-4o...")
            client = AsyncOpenAI(api_key=OPENAI_API_KEY)
            
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a travel expert. Identify monuments precisely."
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": IDENTIFY_PROMPT},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ],
                max_tokens=300,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"OpenAI failed: {e}")

    # 3. No API available
    logger.warning("No vision API available")
    return {
        "identified_monument": "Unknown",
        "confidence": 0.0,
        "description": "Vision API not configured. Set GEMINI_API_KEY in environment.",
        "fun_fact": "N/A",
        "location": "Unknown"
    }
