import httpx
import logging
import base64
import json

logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2-vision"

async def analyze_with_ollama(image_bytes: bytes, prompt: str) -> str:
    """
    Sends image and prompt to local Ollama instance.
    """
    try:
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                    "images": [base64_image]
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.6,
                "num_predict": 100
            }
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(OLLAMA_URL, json=payload)
            
            if resp.status_code == 200:
                data = resp.json()
                content = data.get("message", {}).get("content", "")
                logger.info(f"Ollama Response: {content[:50]}...")
                return content
            else:
                logger.error(f"Ollama Error {resp.status_code}: {resp.text}")
                return None

    except httpx.ConnectError:
        logger.error("Could not connect to Ollama. Is it running on port 11434?")
        return "CONNECTION_ERROR"
    except Exception as e:
        logger.error(f"Ollama Exception: {e}")
        return None
