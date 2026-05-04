from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user_schema import MeResponse, UserResponse
from app.core.security import verify_access_token
from app.services.user_service import user_service

router = APIRouter(tags=["users"])

@router.get("/me", response_model=MeResponse)
def get_me(
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_access_token),
):
    return user_service.get_me(db, payload["sub"])

@router.get("/user/{user_id}", response_model=UserResponse)
def get_details_user(
    user_id: str,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_access_token),
):
    return user_service.get_details_user(db, user_id, payload["sub"])