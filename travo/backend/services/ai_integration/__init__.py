"""AI Integration Services for TRAVO"""
from .deepseek_client import call_deepseek, ask_simple_question, ask_complex_question, MODEL_SIMPLE, MODEL_COMPLEX
from .google_vision_client import detect_landmark, detect_landmark_from_base64

__all__ = [
    'call_deepseek',
    'ask_simple_question',
    'ask_complex_question',
    'detect_landmark',
    'detect_landmark_from_base64',
    'MODEL_SIMPLE',
    'MODEL_COMPLEX'
]
