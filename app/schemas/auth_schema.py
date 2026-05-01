from typing import Optional
from pydantic import BaseModel, EmailStr
from app.core.config import settings
class RegisterRequest(BaseModel):
    display_name: str
    username: str
    email: Optional[EmailStr] = None
    password: str
class LoginRequest(BaseModel):
    email: Optional[EmailStr] = None
    password: str
class AccessTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
class RefreshTokenRequest(BaseModel):
    refresh_token: str