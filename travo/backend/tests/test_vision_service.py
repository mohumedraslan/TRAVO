import os
import sys
import pytest
import pytest_asyncio
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from io import BytesIO
from PIL import Image

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

# Use httpx for async testing
@pytest_asyncio.fixture
async def async_client():
    # This fixture needs to be async to be used by async tests
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def mock_image_file():
    """Create a mock image file for testing."""
    # Create a simple red image
    img = Image.new('RGB', (60, 30), color = 'red')
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return {"image": ("test_image.png", BytesIO(img_byte_arr), "image/png")}

@pytest.mark.asyncio
@patch('services.vision_service.service_logic.IDENTIFICATION_MODEL.identify', new_callable=AsyncMock)
async def test_identify_endpoint_with_real_image(mock_identify, async_client, mock_image_file):
    """Test the /identify endpoint with a mock model and a real image."""
    mock_identify.return_value = {
        "monument_id": "eiffel-tower-paris",
        "confidence": 0.9
    }

    response = await async_client.post("/api/vision/identify", files=mock_image_file)

    assert response.status_code == 200
    data = response.json()
    assert data["identified_monument"] == "Eiffel Tower"
    assert data["confidence"] == 0.9

@pytest.mark.asyncio
@patch('services.vision_service.service_logic.IDENTIFICATION_MODEL.identify', new_callable=AsyncMock)
async def test_identify_endpoint_no_match(mock_identify, async_client, mock_image_file):
    """Test the /identify endpoint when no confident match is found."""
    mock_identify.return_value = {
        "monument_id": "eiffel-tower-paris",
        "confidence": 0.3
    }

    response = await async_client.post("/api/vision/identify", files=mock_image_file)

    assert response.status_code == 200
    data = response.json()
    assert data["identified_monument"] is None
    assert data["message"] == "No confident match found"
