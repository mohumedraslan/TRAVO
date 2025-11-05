import os
import sys
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import json
from io import BytesIO

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.vision_service.service_logic import identify_monument, detect_monuments, get_monument_info
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


@patch('services.vision_service.service_logic.identify_monument')
def test_identify_endpoint(mock_identify, mock_image_file):
    """Test the /identify endpoint."""
    # Mock the identify_monument function
    mock_identify.return_value = {
        "identified_monument": "Pyramids of Giza",
        "confidence": 0.95
    }
    
    # Make a request to the endpoint
    response = client.post(
        "/vision/identify",
        files={"file": mock_image_file}
    )
    
    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert data["identified_monument"] == "Pyramids of Giza"
    assert data["confidence"] == 0.95


def test_detect_monuments():
    """Test the detect_monuments function."""
    # Call the function
    result = detect_monuments("test_image.jpg")
    
    # Check the result structure
    assert isinstance(result, list)
    if result:  # If any monuments were detected
        assert "id" in result[0]
        assert "name" in result[0]
        assert "bounding_box" in result[0]
        assert "confidence" in result[0]


def test_get_monument_info():
    """Test the get_monument_info function."""
    # Call the function with a valid ID
    result = get_monument_info("taj-mahal")
    
    # Check the result
    assert result is not None
    assert result["id"] == "taj-mahal"
    assert result["name"] == "Taj Mahal"
    
    # Test with an invalid ID
    result = get_monument_info("non-existent-id")
    assert result is None


@patch('services.vision_service.service_logic.detect_monuments')
def test_detect_endpoint(mock_detect, mock_image_file):
    """Test the /detect endpoint."""
    # Mock the detect_monuments function
    mock_detect.return_value = [{
        "id": "pyramids-giza",
        "name": "Pyramids of Giza",
        "bounding_box": {
            "x": 100,
            "y": 100,
            "width": 200,
            "height": 200
        },
        "confidence": 0.95
    }]
    
    # Make a request to the endpoint
    response = client.post(
        "/vision/detect",
        files={"file": mock_image_file}
    )
    
    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert "detected_monuments" in data
    assert len(data["detected_monuments"]) == 1
    assert data["detected_monuments"][0]["name"] == "Pyramids of Giza"


def test_monument_info_endpoint():
    """Test the /monument/{monument_id} endpoint."""
    # Make a request to the endpoint with a valid ID
    response = client.get("/vision/monument/taj-mahal")
    
    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "taj-mahal"
    assert data["name"] == "Taj Mahal"
    
    # Test with an invalid ID
    response = client.get("/vision/monument/non-existent-id")
    assert response.status_code == 404