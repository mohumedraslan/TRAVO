import os
import logging
import base64
import json
import httpx

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Hardcoded API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    # Try looking in settings if available, or just log warning
    from ...config import settings
    OPENROUTER_API_KEY = settings.VISION_API_KEY
    
if not OPENROUTER_API_KEY:
    logger.warning("OPENROUTER_API_KEY not found in environment variables!")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Correct free vision models from OpenRouter (verified Dec 2024)
OPENROUTER_MODELS = [
    "google/gemini-2.0-flash-exp:free",
    "mistralai/mistral-small-24b-instruct-2501:free",
    "google/gemma-3-12b-it:free",
    "nvidia/nemotron-nano-12b-v2-vl:free",
    # "amazon/nova-lite-v1:free", # User reported 404
]

IDENTIFY_PROMPT = """Identify the monument/landmark in this image.
Return JSON only: {"identified_monument": "Name", "confidence": 0.9, "description": "Brief description", "fun_fact": "One fact", "location": "City, Country"}"""

async def deep_analyze_image(image_bytes: bytes) -> dict:
    """Vision analysis using free OpenRouter models."""
    
    logger.info("=" * 40)
    logger.info(f"VISION - Processing {len(image_bytes)} bytes")
    
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    for model in OPENROUTER_MODELS:
        try:
            logger.info(f"Model: {model}")
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                resp = await client.post(
                    OPENROUTER_URL,
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://travo.app",
                    },
                    json={
                        "model": model,
                        "messages": [{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": IDENTIFY_PROMPT},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]
                        }],
                        "max_tokens": 300
                    }
                )
                
                if resp.status_code == 200:
                    data = resp.json()
                    content = data["choices"][0]["message"]["content"]
                    logger.info(f"Got: {content[:100]}")
                    
                    # Parse JSON
                    content = content.replace('```json', '').replace('```', '').strip()
                    try:
                        result = json.loads(content)
                    except:
                        import re
                        m = re.search(r'\{[^}]+\}', content, re.DOTALL)
                        if m:
                            result = json.loads(m.group())
                        else:
                            continue
                    
                    logger.info(f"✅ {result.get('identified_monument')}")
                    return result
                else:
                    logger.warning(f"❌ {resp.status_code}: {resp.text[:80]}")
                    
        except Exception as e:
            logger.error(f"Error: {str(e)[:50]}")
            continue

    return {
        "identified_monument": "Unknown",
        "confidence": 0.0,
        "description": "Could not identify. Try another image.",
        "fun_fact": "N/A",
        "location": "Unknown"
    }
