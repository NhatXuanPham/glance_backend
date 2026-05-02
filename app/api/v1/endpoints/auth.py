from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth_schema import (
    TokenResponse,
    RefreshTokenRequest,
    RegisterRequest,
    AccessTokenResponse,
    GoogleExchangeRequest,
)
from app.services.auth_service import auth_service
from app.core.config import settings
router = APIRouter()

@router.post("/register", status_code=201)
def register_customer(data: RegisterRequest, db: Session = Depends(get_db)):
    user = auth_service.register(db, data)
    return {"message": "Registration successful", "user_id": user.id}

@router.post("/login", response_model=TokenResponse)
def login_customer(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return auth_service.login(db, form_data)

@router.post("/refreshtoken", response_model=AccessTokenResponse)
def refresh_token(
    refresh_token_data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    return auth_service.refresh_access_token(db, refresh_token_data)

@router.get("/google/login")
def google_login():
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        "&response_type=code"
        "&scope=openid email profile"
    )
    return RedirectResponse(google_auth_url)

@router.post("/google/exchange")
def google_exchange( data: GoogleExchangeRequest, db: Session = Depends(get_db ),
):
    return auth_service.google_exchange(db, data.code)
