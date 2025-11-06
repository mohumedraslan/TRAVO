import os
import sys
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
import json
import os
import asyncio
from pathlib import Path
from io import BytesIO

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.vision_service.service_logic import identify_monument
from services.vision_service.routes import router
from main import app

# Create a test client
client = TestClient(app)


@pytest.fixture
def mock_image_file():
    """Create a mock image file for testing."""
    # Create a small blank image
    return ("test_image.jpg", BytesIO(b"test image content"), "image/jpeg")


def test_identify_monument():
    """Test the identify_monument function."""
    # Create a temporary test image
    test_image_path = "test_image.jpg"
    with open(test_image_path, "wb") as f:
        f.write(b"test image content")
    
    try:
        # Call the function
        result = identify_monument(test_image_path)
        
        # Check the result structure
        assert "identified_monument" in result
        assert "confidence" in result
        assert isinstance(result["confidence"], float)
        assert 0 <= result["confidence"] <= 1
    finally:
        # Clean up the test file
        if os.path.exists(test_image_path):
            os.remove(test_image_path)


@patch('services.vision_service.routes.monument_service.identify_monument')
def test_identify_endpoint(mock_identify, mock_image_file):
    """Test the /identify endpoint."""
    # Mock the identify_monument function
    mock_identify.return_value = {
        "identified_monument": "Pyramids of Giza",
        "confidence": 0.95,
        "monument_id": "pyramids-of-giza-giza",
        "message": "Monument identified successfully"
    }
    
    # Make a request to the endpoint
    response = client.post(
        "/api/vision/identify",
        files={"image": mock_image_file}
    )
    
    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert data["identified_monument"] == "Pyramids of Giza"
    assert data["confidence"] == 0.95