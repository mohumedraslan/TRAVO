"""
DeepSeek API Client for TRAVO
Huawei Cloud DeepSeek Integration
"""
import os
import requests
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

logger = logging.getLogger(__name__)

# DeepSeek API Configuration
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_BASE_URL = "https://deepseek.huaweicloud.com/v1/chat/completions"

# Model names
MODEL_SIMPLE = "Distil-llama-8b_46e6iu"
MODEL_COMPLEX = "deepseek-r1-distil-qwen-32b_raziqt"


def call_deepseek(
    model_name: str,
    user_prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    **params
) -> Dict[str, Any]:
    """
    Call DeepSeek API for text generation
    
    Args:
        model_name: Model to use (MODEL_SIMPLE or MODEL_COMPLEX)
        user_prompt: User's question/prompt
        system_prompt: Optional system instruction
        temperature: Sampling temperature (0-1)
        max_tokens: Maximum tokens in response
        **params: Additional API parameters
        
    Returns:
        Dictionary with response text and metadata
    """
    try:
        if not DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY not found in environment")
        
        # Build messages
        messages = []
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        messages.append({
            "role": "user",
            "content": user_prompt
        })
        
        # Prepare request payload
        payload = {
            "model": model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **params
        }
        
        # Make API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
        }
        
        logger.info(f"Calling DeepSeek API with model: {model_name}")
        response = requests.post(
            DEEPSEEK_BASE_URL,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        # Check response
        if response.status_code != 200:
            logger.error(f"DeepSeek API error: {response.status_code} - {response.text}")
            return {
                "success": False,
                "error": f"API returned status {response.status_code}",
                "details": response.text
            }
        
        # Parse response
        data = response.json()
        
        if "choices" not in data or len(data["choices"]) == 0:
            logger.error(f"Invalid response format: {data}")
            return {
                "success": False,
                "error": "Invalid response format from API"
            }
        
        # Extract text
        text_response = data["choices"][0]["message"]["content"]
        
        logger.info(f"DeepSeek response received: {len(text_response)} characters")
        
        return {
            "success": True,
            "text": text_response,
            "model": model_name,
            "usage": data.get("usage", {}),
            "finish_reason": data["choices"][0].get("finish_reason")
        }
        
    except requests.exceptions.Timeout:
        logger.error("DeepSeek API timeout")
        return {
            "success": False,
            "error": "API request timed out"
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"DeepSeek API request error: {e}")
        return {
            "success": False,
            "error": f"Request failed: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error calling DeepSeek: {e}", exc_info=True)
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }


def ask_simple_question(question: str, context: Optional[str] = None) -> str:
    """
    Ask a simple question using the lightweight model
    
    Args:
        question: User's question
        context: Optional context information
        
    Returns:
        Response text or error message
    """
    system_prompt = "You are a helpful travel assistant for Egypt. Provide concise, accurate information about Egyptian landmarks, history, and culture."
    
    if context:
        user_prompt = f"Context: {context}\n\nQuestion: {question}"
    else:
        user_prompt = question
    
    result = call_deepseek(
        model_name=MODEL_SIMPLE,
        user_prompt=user_prompt,
        system_prompt=system_prompt,
        temperature=0.7,
        max_tokens=500
    )
    
    if result["success"]:
        return result["text"]
    else:
        return f"Error: {result.get('error', 'Unknown error')}"


def ask_complex_question(question: str, context: Optional[str] = None) -> str:
    """
    Ask a complex question using the advanced model
    
    Args:
        question: User's question
        context: Optional context information
        
    Returns:
        Response text or error message
    """
    system_prompt = "You are an expert Egyptologist and travel guide. Provide detailed, engaging information about Egyptian landmarks, their history, cultural significance, and visitor tips."
    
    if context:
        user_prompt = f"Context: {context}\n\nQuestion: {question}"
    else:
        user_prompt = question
    
    result = call_deepseek(
        model_name=MODEL_COMPLEX,
        user_prompt=user_prompt,
        system_prompt=system_prompt,
        temperature=0.7,
        max_tokens=1500
    )
    
    if result["success"]:
        return result["text"]
    else:
        return f"Error: {result.get('error', 'Unknown error')}"
