from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.follow_schema import FollowListResponse, FollowResponse
from app.services.follow_service import follow_service
from app.core.security import verify_access_token

router = APIRouter(tags=["follows"])

@router.post("/follows/{user_id}", response_model=FollowResponse, status_code=status.HTTP_201_CREATED)
def follow_user(
    user_id: str,
    db: Session = Depends(get_db),
    payload=Depends(verify_access_token),
):
    return follow_service.follow_user(db, str(payload["sub"]), user_id)

@router.delete("/unfollows/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def unfollow_user(
    user_id: str,
    db: Session = Depends(get_db),
    payload=Depends(verify_access_token),
):
    follow_service.unfollow_user(db, str(payload["sub"]), user_id)

@router.get("/list_followed", response_model=FollowListResponse)
def list_followed_users(
    db: Session = Depends(get_db),
    payload=Depends(verify_access_token),
):
    return follow_service.list_followed_users(db, str(payload["sub"]))