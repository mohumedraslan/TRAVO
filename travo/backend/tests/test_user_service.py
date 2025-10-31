import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session

from ..services.user_service.service_logic import (
    get_password_hash,
    verify_password,
    create_user,
    authenticate_user,
    get_user_preferences,
    update_user_preferences
)
from ..services.user_service.schemas import UserCreate, UserPreferencesUpdate
from ..services.user_service.models import User, UserPreferences


def test_password_hashing():
    """Test password hashing and verification."""
    password = "TestPassword123"
    hashed = get_password_hash(password)
    
    # Verify the hash is different from the original password
    assert hashed != password
    
    # Verify the password verification works
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


@pytest.fixture
def mock_db():
    """Create a mock database session."""
    return MagicMock(spec=Session)


def test_create_user(mock_db):
    """Test user creation."""
    # Mock the query to return no existing user
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # Create a test user
    user_data = UserCreate(
        name="Test User",
        email="test@example.com",
        password="TestPassword123"
    )
    
    # Mock the created user
    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.name = user_data.name
    mock_user.email = user_data.email
    
    # Set up the mock to return our mock user after commit
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = lambda x: setattr(x, 'id', 1)
    
    # Call the function
    with patch('travo.backend.services.user_service.service_logic.create_default_preferences') as mock_create_prefs:
        mock_create_prefs.return_value = MagicMock(spec=UserPreferences)
        result = create_user(mock_db, user_data)
    
    # Verify the result
    assert result is not None
    assert mock_db.add.called
    assert mock_db.commit.called
    assert mock_db.refresh.called


def test_authenticate_user(mock_db):
    """Test user authentication."""
    # Create a mock user with a known password hash
    password = "TestPassword123"
    hashed_password = get_password_hash(password)
    
    mock_user = MagicMock(spec=User)
    mock_user.email = "test@example.com"
    mock_user.password_hash = hashed_password
    
    # Set up the mock to return our mock user
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    
    # Test successful authentication
    result = authenticate_user(mock_db, "test@example.com", password)
    assert result is not None
    assert result == mock_user
    
    # Test failed authentication with wrong password
    result = authenticate_user(mock_db, "test@example.com", "WrongPassword")
    assert result is None
    
    # Test failed authentication with non-existent user
    mock_db.query.return_value.filter.return_value.first.return_value = None
    result = authenticate_user(mock_db, "nonexistent@example.com", password)
    assert result is None


def test_user_preferences(mock_db):
    """Test user preferences operations."""
    # Mock user preferences
    mock_prefs = MagicMock(spec=UserPreferences)
    mock_prefs.user_id = 1
    mock_prefs.interests = '[]'
    mock_prefs.preferred_cities = '[]'
    mock_prefs.saved_itineraries = '[]'
    mock_prefs.notification_settings = '{"email_notifications": true}'
    mock_prefs.additional_settings = '{}'
    
    # Set up the mock to return our mock preferences
    mock_db.query.return_value.filter.return_value.first.return_value = mock_prefs
    
    # Test getting preferences
    result = get_user_preferences(mock_db, 1)
    assert result is not None
    assert result == mock_prefs
    
    # Test updating preferences
    update_data = UserPreferencesUpdate(
        interests=["historical", "cultural"],
        preferred_cities=["Cairo", "Luxor"],
        notification_settings={"email_notifications": False}
    )
    
    # Mock the JSON methods
    mock_prefs.get_interests = MagicMock(return_value=[])
    mock_prefs.get_preferred_cities = MagicMock(return_value=[])
    mock_prefs.get_saved_itineraries = MagicMock(return_value=[])
    mock_prefs.get_notification_settings = MagicMock(return_value={"email_notifications": True})
    mock_prefs.get_additional_settings = MagicMock(return_value={})
    
    result = update_user_preferences(mock_db, 1, update_data)
    assert result is not None
    assert mock_db.commit.called
    assert mock_db.refresh.called


@pytest.fixture
def client():
    """Create a test client for the API."""
    from ..main import app
    return TestClient(app)


def test_register_endpoint(client):
    """Test the user registration endpoint."""
    with patch('travo.backend.services.user_service.routes.create_user') as mock_create:
        # Mock the user creation
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.name = "Test User"
        mock_user.email = "test@example.com"
        mock_user.created_at = "2023-01-01T00:00:00"
        mock_create.return_value = mock_user
        
        # Test the endpoint
        response = client.post(
            "/api/users/register",
            json={
                "name": "Test User",
                "email": "test@example.com",
                "password": "TestPassword123"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test User"
        assert data["email"] == "test@example.com"
        assert "id" in data


def test_login_endpoint(client):
    """Test the user login endpoint."""
    with patch('travo.backend.services.user_service.routes.authenticate_user') as mock_auth, \
         patch('travo.backend.services.user_service.routes.create_access_token') as mock_token:
        
        # Mock the authentication
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.name = "Test User"
        mock_user.email = "test@example.com"
        mock_user.created_at = "2023-01-01T00:00:00"
        mock_auth.return_value = mock_user
        
        # Mock the token creation
        mock_token.return_value = "test_token"
        
        # Test the endpoint
        response = client.post(
            "/api/users/login",
            data={"username": "test@example.com", "password": "TestPassword123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["access_token"] == "test_token"
        assert data["token_type"] == "bearer"
        assert "user" in data
