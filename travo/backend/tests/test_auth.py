import pytest
from fastapi import HTTPException
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from ..utils.auth import create_access_token, get_current_user


def test_create_access_token():
    """Test JWT token creation."""
    # Test with default expiration
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    assert token is not None
    assert isinstance(token, str)
    
    # Test with custom expiration
    expires = timedelta(minutes=60)
    token = create_access_token(data, expires_delta=expires)
    assert token is not None
    assert isinstance(token, str)


@pytest.mark.asyncio
async def test_get_current_user():
    """Test current user extraction from JWT token."""
    # Mock dependencies
    mock_db = MagicMock()
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.name = "Test User"
    mock_user.email = "test@example.com"
    mock_user.created_at = datetime.utcnow()
    
    # Create a real token for testing
    token_data = {"sub": "test@example.com"}
    token = create_access_token(token_data)
    
    # Test successful token validation
    with patch('travo.backend.utils.auth.get_user_by_email') as mock_get_user:
        mock_get_user.return_value = mock_user
        
        user = await get_current_user(token, mock_db)
        
        assert user is not None
        assert user.email == "test@example.com"
        assert user.id == 1
        assert user.name == "Test User"


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    """Test error handling for invalid JWT token."""
    # Mock dependencies
    mock_db = MagicMock()
    
    # Test with invalid token
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user("invalid_token", mock_db)
    
    assert exc_info.value.status_code == 401
    assert "Could not validate credentials" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_current_user_nonexistent_user():
    """Test error handling for valid token but nonexistent user."""
    # Mock dependencies
    mock_db = MagicMock()
    
    # Create a real token for testing
    token_data = {"sub": "nonexistent@example.com"}
    token = create_access_token(token_data)
    
    # Test with nonexistent user
    with patch('travo.backend.utils.auth.get_user_by_email') as mock_get_user:
        mock_get_user.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(token, mock_db)
        
        assert exc_info.value.status_code == 401
        assert "Could not validate credentials" in exc_info.value.detail
