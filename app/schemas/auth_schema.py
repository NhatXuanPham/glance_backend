from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.core.config import settings
class RegisterRequest(BaseModel):
    display_name: str
    username: str
    email: Optional[EmailStr] = None
    password: str
class LoginRequest(BaseModel):
    email: Optional[EmailStr] = None
    password: str
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    access_token_expires_at: datetime 
    refresh_token_expires_at: datetime
class RefreshTokenRequest(BaseModel):
    refresh_token: str
class AccessTokenResponse(BaseModel):
    access_token: str
    expires_at: datetime