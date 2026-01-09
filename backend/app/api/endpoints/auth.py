"""
Authentication Endpoints
Simple auth for demo purposes - in production, replace with proper user DB.
"""

from datetime import timedelta
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.core.security import create_access_token, get_password_hash, verify_password
from app.core.config import settings


router = APIRouter()


# Simple in-memory user store for demo
# In production, use a proper database
# Pre-hashed password for "student123" to avoid runtime issues
demo_users = {}


def get_demo_users():
    """Lazy load demo users."""
    if not demo_users:
        demo_users["student@lab.edu"] = {
            "email": "student@lab.edu",
            "hashed_password": get_password_hash("student123"),
            "name": "Demo Student",
            "role": "student"
        }
    return demo_users


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Login with email and password."""
    users = get_demo_users()
    user = users.get(request.email)
    
    if not user or not verify_password(request.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    access_token = create_access_token(
        data={"sub": user["email"], "name": user["name"], "role": user["role"]},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
    )
    
    return TokenResponse(
        access_token=access_token,
        user={"email": user["email"], "name": user["name"], "role": user["role"]}
    )


@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest):
    """Register a new user."""
    users = get_demo_users()
    if request.email in users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    users[request.email] = {
        "email": request.email,
        "hashed_password": get_password_hash(request.password),
        "name": request.name,
        "role": "student"
    }
    
    access_token = create_access_token(
        data={"sub": request.email, "name": request.name, "role": "student"},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
    )
    
    return TokenResponse(
        access_token=access_token,
        user={"email": request.email, "name": request.name, "role": "student"}
    )


@router.get("/me")
async def get_me():
    """Get current user info - placeholder."""
    return {"message": "Use /api/auth/login to get a token"}
