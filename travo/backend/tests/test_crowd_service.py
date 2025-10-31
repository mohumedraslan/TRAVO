import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from ..services.crowd_service.service_logic import predict_crowd_level
from ..services.crowd_service.schemas import CrowdPredictionRequest, CrowdLevel


def test_predict_crowd_level():
    """Test the crowd prediction logic."""
    # Test case 1: Pyramids of Giza at peak time
    request = CrowdPredictionRequest(
        monument_id="pyr_giza",
        month=7,  # July (peak tourist season)
        day=15,
        time="10:30"  # Morning, typically busy
    )
    result = predict_crowd_level(request)
    assert result is not None
    assert hasattr(result, 'crowd_level')
    assert isinstance(result.crowd_level, CrowdLevel)
    
    # Test case 2: Off-peak time
    request = CrowdPredictionRequest(
        monument_id="luxor",
        month=1,  # January (off-peak)
        day=10,
        time="16:30"  # Late afternoon
    )
    result = predict_crowd_level(request)
    assert result is not None
    assert hasattr(result, 'crowd_level')
    assert isinstance(result.crowd_level, CrowdLevel)


@pytest.fixture
def client():
    """Create a test client for the API."""
    from ..main import app
    return TestClient(app)


def test_predict_crowd_endpoint(client):
    """Test the predict crowd endpoint."""
    with patch('travo.backend.services.crowd_service.routes.predict_crowd_level') as mock_predict:
        # Mock the prediction function
        mock_predict.return_value = MagicMock(
            monument_id="pyr_giza",
            crowd_level=CrowdLevel.HIGH,
            factors={
                "time_of_day": "Peak hours",
                "season": "High season",
                "day_of_week": "Weekend"
            },
            wait_time_minutes=45
        )
        
        # Test the endpoint
        response = client.post(
            "/api/crowds/predict",
            json={
                "monument_id": "pyr_giza",
                "month": 7,
                "day": 15,
                "time": "10:30"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["monument_id"] == "pyr_giza"
        assert data["crowd_level"] == "HIGH"
        assert "factors" in data
        assert "wait_time_minutes" in data


def test_invalid_input(client):
    """Test the endpoint with invalid input."""
    # Test with invalid month
    response = client.post(
        "/api/crowds/predict",
        json={
            "monument_id": "pyr_giza",
            "month": 13,  # Invalid month
            "day": 15,
            "time": "10:30"
        }
    )
    assert response.status_code == 400
    
    # Test with invalid time format
    response = client.post(
        "/api/crowds/predict",
        json={
            "monument_id": "pyr_giza",
            "month": 7,
            "day": 15,
            "time": "25:30"  # Invalid time
        }
    )
    assert response.status_code == 400
