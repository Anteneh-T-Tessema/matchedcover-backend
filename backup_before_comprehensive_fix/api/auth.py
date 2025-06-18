""""
Authentication API endpoints for MatchedCover Insurance Platform.

This module handles user authentication, registration, and session management.
""""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
import jwt

from src.core.config import settings
from src.core.database import get_async_session


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserCreate(BaseModel):
    """User creation schema."""

    email: EmailStr
password: str
first_name: str
last_name: str
phone_number: Optional[str] = None
role: str = "customer"


class UserResponse(BaseModel):
    """User response schema."""

    id: str
email: str
first_name: Optional[str]
last_name: Optional[str]
role: str
is_verified: bool
is_active: bool
created_at: datetime


class Token(BaseModel):
    """Token response schema."""

    access_token: str
token_type: str
expires_in: int
user: UserResponse


class LoginRequest(BaseModel):
    """Login request schema."""

    email: EmailStr
password: str


# Helper functions
async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Get current user from token."""
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

    try:
        payload = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    email: str = payload.get("sub")
    user_id: str = payload.get("user_id")

        if email is None or user_id is None:
            raise credentials_exception

    except jwt.PyJWTError:
        raise credentials_exception

    # In a real implementation, this would fetch user from database
user = {
    "id": user_id,
    "email": email,
    "first_name": "John",
    "last_name": "Doe",
    "role": "customer",
    "is_verified": True,
    "is_active": True,
    "created_at": datetime.utcnow(),
}

    if user is None:
        raise credentials_exception

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
to_encode = data.copy()
if expires_delta:
        expire = datetime.utcnow() + expires_delta
else:
        expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})
encoded_jwt = jwt.encode(
    to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
)
return encoded_jwt


# API Endpoints


@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreate, db_session=Depends(get_async_session)
):
    """Register a new user."""
# Check if user already exists
# In a real implementation, this would query the database

    # Create new user
# This is a simplified implementation
new_user = {
    "id": "user-123",
    "email": user_data.email,
    "first_name": user_data.first_name,
    "last_name": user_data.last_name,
    "role": user_data.role,
    "is_verified": False,
    "is_active": True,
    "created_at": datetime.utcnow(),
}

    return UserResponse(**new_user)


@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest, db_session=Depends(get_async_session)
):
    """Authenticate user and return access token."""
# Verify user credentials
# This is a simplified implementation

    user_data = {
    "id": "user-123",
    "email": login_data.email,
    "first_name": "John",
    "last_name": "Doe",
    "role": "customer",
    "is_verified": True,
    "is_active": True,
    "created_at": datetime.utcnow(),
}

    # Generate access token
access_token = create_access_token(
    data={"sub": user_data["email"], "user_id": user_data["id"]}
)

    return Token(
    access_token=access_token,
    token_type="bearer",
    expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    user=UserResponse(**user_data),
)


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """Logout user and invalidate session."""
# Invalidate user session
# In a real implementation, this would update the database

    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
):
    """Get current user information."""
return UserResponse(**current_user)


@router.post("/refresh")
async def refresh_token(current_user: dict = Depends(get_current_user)):
    """Refresh access token."""
# Generate new access token
access_token = create_access_token(
    data={"sub": current_user["email"], "user_id": current_user["id"]}
)

    return {
    "access_token": access_token,
    "token_type": "bearer",
    "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
}


@router.post("/verify-email")
async def verify_email(token: str, db_session=Depends(get_async_session)):
    """Verify user email address."""
# Verify email token
# In a real implementation, this would validate the token and update the
# user

    return {"message": "Email verified successfully"}


@router.post("/forgot-password")
async def forgot_password(
    email: EmailStr, db_session=Depends(get_async_session)
):
    """Send password reset email."""
# Send password reset email
# In a real implementation, this would generate a reset token and send
# email

    return {"message": "Password reset email sent"}


@router.post("/reset-password")
async def reset_password(
    token: str, new_password: str, db_session=Depends(get_async_session)
):
    """Reset user password."""
# Reset password
# In a real implementation, this would validate the token and update
# password

    return {"message": "Password reset successfully"}
