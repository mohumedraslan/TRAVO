import unittest
from unittest.mock import patch, MagicMock
import json
import base64
import sys
import os

# Add the parent directory to sys.path to import modules from the project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.assistant_service.service_logic import (
    get_ai_response,
    get_rule_based_response,
    voice_to_text,
    text_to_voice,
    load_monument_data
)
from services.assistant_service.schemas import (
    AssistantQuery,
    AssistantResponse,
    VoiceToTextRequest,
    VoiceToTextResponse,
    TextToVoiceRequest,
    TextToVoiceResponse,
    QueryType
)


class TestAssistantService(unittest.TestCase):
    
    def setUp(self):
        # Load test data
        self.monument_data = load_monument_data()
        
        # Sample audio data (base64 encoded)
        self.sample_audio = base64.b64encode(b'test audio data').decode('utf-8')
        
    def test_get_rule_based_response(self):
        # Test with a query about the Pyramids of Giza
        query = "Tell me about the Pyramids of Giza"
        location = "Egypt"
        
        response = get_rule_based_response(query, location)
        
        # Check that the response contains information about the Pyramids
        self.assertIsNotNone(response)
        self.assertIn("Pyramid", response.response)
        
        # Test with a query about an unknown monument
        query = "Tell me about the Moon Temple"
        response = get_rule_based_response(query, location)
        
        # Check that the response is a fallback response
        self.assertIsNotNone(response)
        self.assertIn("I don't have specific information", response.response)
    
    @patch('services.assistant_service.service_logic.get_openai_response')
    @patch('services.assistant_service.service_logic.get_transformers_response')
    def test_get_ai_response(self, mock_transformers, mock_openai):
        # Set up mocks
        mock_openai.return_value = None  # Simulate OpenAI not available
        mock_transformers.return_value = AssistantResponse(
            response="The Pyramids of Giza are ancient monuments in Egypt.",
            monument_info={"id": "pyr_giza", "name": "Pyramids of Giza", "country": "Egypt"},
            sources=["Test source"]
        )
        
        # Test the AI response function
        query = AssistantQuery(
            query="What are the Pyramids of Giza?",
            query_type=QueryType.text,
            location="Egypt"
        )
        
        response = get_ai_response(query)
        
        # Verify the response
        self.assertIsNotNone(response)
        self.assertEqual(response.response, "The Pyramids of Giza are ancient monuments in Egypt.")
        self.assertEqual(response.monument_info["name"], "Pyramids of Giza")
        
        # Test fallback to rule-based when all AI methods fail
        mock_transformers.return_value = None
        
        response = get_ai_response(query)
        
        # Verify fallback response
        self.assertIsNotNone(response)
        self.assertIn("Pyramid", response.response)
    
    @patch('speech_recognition.Recognizer.recognize_google')
    def test_voice_to_text(self, mock_recognize):
        # Set up mock
        mock_recognize.return_value = "What are the Pyramids of Giza?"
        
        # Test voice to text conversion
        request = VoiceToTextRequest(
            audio_data=self.sample_audio,
            language="en-US"
        )
        
        with patch('speech_recognition.AudioData'):
            response = voice_to_text(request)
            
            # Verify the response
            self.assertIsNotNone(response)
            self.assertEqual(response.text, "What are the Pyramids of Giza?")
            self.assertGreaterEqual(response.confidence, 0.0)
            self.assertLessEqual(response.confidence, 1.0)
    
    @patch('gtts.gTTS')
    def test_text_to_voice_gtts(self, mock_gtts):
        # Mock the gTTS save method
        mock_instance = MagicMock()
        mock_gtts.return_value = mock_instance
        
        # Test text to voice conversion
        request = TextToVoiceRequest(
            text="The Pyramids of Giza are ancient monuments in Egypt.",
            language="en-US"
        )
        
        # Mock the file operations
        with patch('builtins.open', unittest.mock.mock_open(read_data=b'test audio data')):
            with patch('os.remove'):
                response = text_to_voice(request)
                
                # Verify the response
                self.assertIsNotNone(response)
                self.assertTrue(hasattr(response, 'audio_data'))
                self.assertEqual(response.format, "mp3")
    
    @patch('TTS.utils.synthesizer.Synthesizer')
    def test_text_to_voice_coqui(self, mock_synthesizer):
        # Set up mock for Coqui TTS
        mock_instance = MagicMock()
        mock_instance.tts.return_value = b'test audio data'
        mock_synthesizer.return_value = mock_instance
        
        # Test text to voice conversion with Coqui TTS
        request = TextToVoiceRequest(
            text="The Pyramids of Giza are ancient monuments in Egypt.",
            language="en-US",
            voice_name="tts_models/en/ljspeech/tacotron2-DDC"
        )
        
        # Patch the import to simulate Coqui TTS being available
        with patch.dict('sys.modules', {'TTS': MagicMock()}):
            with patch('services.assistant_service.service_logic.COQUI_TTS_AVAILABLE', True):
                response = text_to_voice(request)
                
                # Verify the response
                self.assertIsNotNone(response)
                self.assertTrue(hasattr(response, 'audio_data'))
                self.assertEqual(response.format, "wav")


if __name__ == '__main__':
    unittest.main()