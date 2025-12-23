import logging
import json
from ..live_service.ollama_client import analyze_with_ollama

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

IDENTIFY_PROMPT = """
Look at the image. Identify the monument, landmark, or location.
Output a valid JSON object with these exact keys:
{
  "identified_monument": "Name of the place",
  "confidence": 0.9,
  "description": "A brief 1-sentence description.",
  "fun_fact": "One interesting short fact.",
  "location": "City, Country"
}
Do not write any text outside the JSON.
"""

async def deep_analyze_image(image_bytes: bytes) -> dict:
    """Vision analysis using LOCAL AI (Ollama)."""
    
    logger.info("=" * 40)
    logger.info(f"VISION (Local) - Processing {len(image_bytes)} bytes")
    
    try:
        # Call Local Ollama
        content = await analyze_with_ollama(image_bytes, IDENTIFY_PROMPT)
        
        if not content or content == "CONNECTION_ERROR":
             return {
                "identified_monument": "Service Unavailable",
                "confidence": 0.0,
                "description": "Ensure Ollama is running.",
                "fun_fact": "N/A",
                "location": "Localhost"
            }

        logger.info(f"Ollama Raw: {content[:100]}...")

        # Robust JSON Parsing
        content = content.replace('```json', '').replace('```', '').strip()
        
        # Sometimes Ollama adds chatter "Here is the JSON:"
        if "{" in content:
            content = content[content.find("{"):content.rfind("}")+1]
        
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            # Fallback if JSON is malformed
            import re
            m = re.search(r'\{.*\}', content, re.DOTALL)
            if m:
                result = json.loads(m.group())
            else:
                logger.error("Could not parse JSON from Ollama response")
                raise ValueError("Invalid JSON")

        logger.info(f"✅ Identified: {result.get('identified_monument')}")
        return result

    except Exception as e:
        logger.error(f"Deep Scan Error: {e}")
        return {
            "identified_monument": "Unknown",
            "confidence": 0.0,
            "description": "Could not identify. Try a clearer angle.",
            "fun_fact": "N/A",
            "location": "Unknown"
        }
