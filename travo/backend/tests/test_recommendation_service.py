import os
import sys
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.recommendation_service.service_logic import create_rule_based_recommendation
from services.recommendation_service.routes import router
from main import app

# Create a test client
client = TestClient(app)


def test_create_rule_based_recommendation():
    """Test the create_rule_based_recommendation function."""
    # Test with valid inputs
    interests = ["history", "culture"]
    days = 3
    
    result = create_rule_based_recommendation(interests, days)
    
    # Check the result structure
    assert "destination" in result
    assert "days" in result
    assert "total_cost" in result
    assert len(result["days"]) == days
    
    # Check that each day has attractions
    for day in result["days"]:
        assert "day_number" in day
        assert "attractions" in day
        assert len(day["attractions"]) > 0


def test_recommend_endpoint():
    """Test the /recommend endpoint."""
    # Make a request to the endpoint
    response = client.post(
        "/recommendations/recommend",
        json={"interests": ["history", "culture"], "days": 2}
    )
    
    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert "destination" in data
    assert "days" in data
    assert "total_cost" in data
    assert len(data["days"]) == 2


def test_recommend_endpoint_validation():
    """Test validation in the /recommend endpoint."""
    # Test with invalid interests
    response = client.post(
        "/recommendations/recommend",
        json={"interests": ["invalid"], "days": 2}
    )
    assert response.status_code == 422
    
    # Test with days out of range
    response = client.post(
        "/recommendations/recommend",
        json={"interests": ["history"], "days": 15}
    )
    assert response.status_code == 422
    
    # Test with missing interests
    response = client.post(
        "/recommendations/recommend",
        json={"days": 2}
    )
    assert response.status_code == 422


def test_destinations_endpoint():
    """Test the /destinations endpoint."""
    # Make a request to the endpoint
    response = client.get("/recommendations/destinations")
    
    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert "destinations" in data
    assert len(data["destinations"]) > 0
    
    # Check filtering
    response = client.get("/recommendations/destinations?category=BEACH&season=SUMMER")
    assert response.status_code == 200
    data = response.json()
    assert "destinations" in data


def test_trending_destinations_endpoint():
    """Test the /destinations/trending endpoint."""
    # Make a request to the endpoint
    response = client.get("/recommendations/destinations/trending")
    
    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert "trending_destinations" in data
    assert len(data["trending_destinations"]) > 0


def test_similar_destinations_endpoint():
    """Test the /destinations/similar endpoint."""
    # Make a request to the endpoint
    response = client.get("/recommendations/destinations/similar?destination_id=paris")
    
    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert "similar_destinations" in data
    
    # Test with invalid destination_id
    response = client.get("/recommendations/destinations/similar?destination_id=invalid")
    assert response.status_code == 404


def test_attractions_endpoint():
    """Test the /destinations/{destination_id}/attractions endpoint."""
    # Make a request to the endpoint
    response = client.get("/recommendations/destinations/paris/attractions")
    
    # Check the response
    assert response.status_code == 200
    data = response.json()
    assert "attractions" in data
    assert len(data["attractions"]) > 0
    
    # Test with invalid destination_id
    response = client.get("/recommendations/destinations/invalid/attractions")
    assert response.status_code == 404