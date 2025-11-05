import os
import sys
import pytest
import pytest_asyncio
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
import asyncio
from io import BytesIO

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

# Use httpx for async testing
@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def mock_image_file():
    """Create a mock image file for testing."""
    return {"image": ("test_image.jpg", BytesIO(b"test image content"), "image/jpeg")}

@pytest.mark.asyncio
async def test_identify_endpoint(async_client, mock_image_file):
    """Test the /identify endpoint."""
    with patch('services.vision_service.service_logic.identify_monument', new_callable=AsyncMock) as mock_identify:
        mock_identify.return_value = {
            "identified_monument": "Pyramids of Giza",
            "confidence": 0.95,
            "monument_id": "pyramids-giza"
        }

        response = await async_client.post(
            "/api/vision/identify",
            files=mock_image_file
        )
        assert response.status_code == 200
        data = response.json()
        assert data["identified_monument"] == "Pyramids of Giza"
        assert data["confidence"] == 0.95

@pytest.mark.asyncio
async def test_detect_endpoint(async_client, mock_image_file):
    """Test the /detect endpoint."""
    with patch('services.vision_service.service_logic.detect_monuments', new_callable=AsyncMock) as mock_detect:
        mock_detect.return_value = {
            "image_id": "test-id",
            "detected_monuments": [{
                "monument_id": "pyramids-giza",
                "name": "Pyramids of Giza",
                "confidence": 0.95,
                "bounding_box": {"x_min": 0.1, "y_min": 0.1, "x_max": 0.5, "y_max": 0.5}
            }],
            "processing_time_ms": 100,
            "timestamp": "2023-10-27T10:00:00Z"
        }

        response = await async_client.post(
            "/api/vision/detect",
            files=mock_image_file
        )
        assert response.status_code == 200
        data = response.json()
        assert "detected_monuments" in data
        assert len(data["detected_monuments"]) == 1
        assert data["detected_monuments"][0]["name"] == "Pyramids of Giza"

@pytest.mark.asyncio
async def test_monument_info_endpoint(async_client):
    """Test the /monument/{monument_id} endpoint."""
    with patch('services.vision_service.service_logic.get_monument_info', new_callable=AsyncMock) as mock_get_info:
        mock_get_info.return_value = {
            "monument_id": "eiffel-tower-paris",
            "name": "Eiffel Tower"
        }

        response = await async_client.get("/api/vision/monument/eiffel-tower-paris")
        assert response.status_code == 200
        data = response.json()
        assert data["monument_id"] == "eiffel-tower-paris"
        assert data["name"] == "Eiffel Tower"

        # Test with an invalid ID
        mock_get_info.return_value = None
        response = await async_client.get("/api/vision/monument/non-existent-id")
        assert response.status_code == 404
