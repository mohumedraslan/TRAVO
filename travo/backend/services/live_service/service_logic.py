import logging
import base64
from typing import Optional
from .ollama_client import analyze_with_ollama

logger = logging.getLogger(__name__)

async def analyze_pulse(image_bytes: bytes, lat: Optional[float], lon: Optional[float]) -> dict:
    """
    Fast visual analysis using LOCAL AI (Ollama).
    """
    # Macro-location context (simplified for MVP)
    location_context = "Unknown location (Rely on visual only)"
    # DISABLE GPS for remote testing:
    # if lat and lon:
    #     location_context = f"Coordinates {lat:.4f}, {lon:.4f}"

    prompt = (
        "Look at the image. Provide ONE short, helpful, proactive travel tip. "
        "Start your answer with 'TIP: '. "
        "Example: 'TIP: Visit at sunrise.' "
        "Do not explain. Do not reason. Keep it under 20 words."
    )

    # Call Local Ollama
    content = await analyze_with_ollama(image_bytes, prompt)

    if content == "CONNECTION_ERROR":
        return {"tip": "Please start Ollama App!", "context": "Error"}
    
    if not content:
        return {"tip": "AI is distracted...", "context": "Error"}

    # Cleaning (Ollama is usually cleaner, but just in case)
    if "TIP:" in content:
        content = content.split("TIP:")[-1].strip()
    
    content = content.replace('"', '').replace("'", "").strip()

    logger.info(f"Live Pulse Success (Local): {content}")
    return {"tip": content, "context": location_context}
