import logging
import base64
import httpx
import os
from typing import Optional

logger = logging.getLogger(__name__)

# Lightweight VLM for fast response (Free alternative to Gemini)
LIVE_MODEL = "meta-llama/llama-3.2-11b-vision-instruct:free"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Load API Key (reusing from env)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def analyze_pulse(image_bytes: bytes, lat: Optional[float], lon: Optional[float]) -> dict:
    """
    Fast visual analysis for live assistance.
    Uses a minimal prompt and small model to reduce latency.
    """
    if not OPENROUTER_API_KEY:
        return {"tip": "API Key missing", "context": "Error"}

    # Macro-location context (simplified for MVP)
    location_context = "Unknown location (Rely on visual only)"
    # DISABLE GPS for remote testing:
    # if lat and lon:
    #     location_context = f"Coordinates {lat:.4f}, {lon:.4f}"
    #     # In a real app, reverse geocode here to get "Paris, Eiffel Tower"

    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    prompt = f"""
    You are a travel assistant. 
    User Location: {location_context}.
    Task: Look at the image. Provide ONE short, helpful, proactive tip for the user.
    If it's just a street, say what kind of street. If it's a menu, suggest checking specials. 
    Keep it under 15 words.
    IMPORTANT: Provide ONLY the tip. Do NOT explain your reasoning.
    """

    # List of models to try in order
    MODELS = [
        "google/gemini-2.0-flash-exp:free",             # Primary: Fast & Smart
        # "mistralai/mistral-small-24b-instruct-2501:free", # 404s often
        "google/gemma-3-12b-it:free",                   # Tertiary: Google's new open model
        "nvidia/nemotron-nano-12b-v2-vl:free",          # Fallback: Reliable
    ]

    async with httpx.AsyncClient(timeout=15.0) as client:
        for model in MODELS:
            try:
                # Adjust prompt based on model (Nemotron needs strict instructions)
                current_prompt = prompt
                if "nemotron" in model:
                    current_prompt = (
                        "Look at the image. Provide ONE short, helpful, proactive travel tip. "
                        "Output ONLY the tip. Do not explain. Do not say 'I think' or 'The user'. "
                        "Start directly with the tip."
                    )
                
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
                                {"type": "text", "text": current_prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]
                        }],
                        "max_tokens": 150, 
                        "temperature": 0.4 # Lower temp for less rambling
                    }
                )

                if resp.status_code == 200:
                    data = resp.json()
                    choice = data.get("choices", [{}])[0]
                    content = choice.get("message", {}).get("content", "").strip()
                    
                    # Fallback logic for empty content
                    if not content:
                        reasoning = choice.get("message", {}).get("reasoning", "")
                        if reasoning:
                            # Heuristic: Nemotron often ends reasoning with "So, [Tip]."
                            if "So," in reasoning:
                                content = reasoning.split("So,")[-1].strip()
                            else:
                                content = reasoning.split('.')[-2] + "." if '.' in reasoning else reasoning[:50]
                    
                    # CLEANING: Remove artifacts like "Also good", "So...", quotes
                    if content:
                        content = content.replace('"', '').replace("'", "").strip()
                        
                        # Fix common Nemotron prefixes
                        if "So, " in content:
                            content = content.split("So, ")[-1]
                        if "Tiip:" in content or "Tip:" in content:
                            content = content.split(":")[-1].strip()

                        # If multiple lines, take the last one (often the real answer)
                        if "\n" in content:
                            lines = [l.strip() for l in content.split("\n") if l.strip()]
                            if lines:
                                content = lines[-1]

                        # Filter out weak/internal-monologue responses
                        bad_prefixes = ["Let me", "I need to", "The user", "Possible tips", "The image", "Also ", "Okay"]
                        if any(content.strip().startswith(p) for p in bad_prefixes):
                            # Last ditch effort: Try to find a sentence that DOESN'T start with these
                            sentences = content.split('.')
                            valid_sents = [s.strip() for s in sentences if s.strip() and not any(s.strip().startswith(p) for p in bad_prefixes)]
                            if valid_sents:
                                content = valid_sents[-1]
                            else:
                                logger.warning(f"Model {model} returned monologue: {content}")
                                content = None # Force fallback

                    if content and content != "SILENT":
                        logger.info(f"Live Pulse Success ({model}): {content}")
                        return {"tip": content, "context": location_context}
                
                logger.warning(f"Model {model} failed with {resp.status_code}: {resp.text}")

            except Exception as e:
                logger.warning(f"Model {model} exception: {e}")
                continue

    return {"tip": "Service unavailable", "context": "Error"}
