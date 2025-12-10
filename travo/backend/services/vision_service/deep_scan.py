import os
import logging
import base64
import json
import httpx

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Hardcoded API key
OPENROUTER_API_KEY = "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"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Correct free vision models from OpenRouter (verified Dec 2024)
OPENROUTER_MODELS = [
    "qwen/qwen2.5-vl-32b-instruct:free",      # Qwen vision - works!
    "meta-llama/llama-3.2-11b-vision-instruct:free",  # Llama vision
    "nvidia/nemotron-nano-12b-v2-vl:free",    # NVIDIA vision
    "amazon/nova-lite-v1:free",               # Amazon Nova
    "google/gemma-3-12b-it:free",             # Google Gemma
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
