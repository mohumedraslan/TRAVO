from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, Annotated
import os

# Import User model and database session
from services.user_service.database import get_db
from services.user_service.service_logic import get_user_by_email
from services.user_service.schemas import UserResponse

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-for-development-only")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a new JWT access token."""
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Create JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
) -> UserResponse:
    """Validate token and return current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    user = get_user_by_email(db, email=email)
    
    if user is None:
        raise credentials_exception
    
    # Return user data
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at
    )


async def get_current_active_user(
    current_user: Annotated[UserResponse, Depends(get_current_user)]
) -> UserResponse:
    """Check if user is active."""
    # In a real application, you would check if the user is active
    # For now, we'll just return the user
    return current_user


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a new JWT refresh token with longer expiration."""
    to_encode = data.copy()
    
    # Set expiration time (longer than access token)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default to 7 days for refresh token
        expire = datetime.utcnow() + timedelta(days=7)
    
    to_encode.update({"exp": expire, "token_type": "refresh"})
    
    # Create JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt