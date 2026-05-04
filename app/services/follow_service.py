from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.follow_repo import follow_repo
from app.schemas.follow_schema import FollowResponse, FollowListResponse

class FollowService:
    def follow_user(self, db: Session, me_id: str, user_id: str) -> FollowResponse:
        if me_id == user_id:
            raise HTTPException(status_code=400, detail="Cannot follow yourself")
        if follow_repo.has_followed_user(db, me_id, user_id):
            raise HTTPException(status_code=400, detail="Already following")
        follow = follow_repo.follow_user(db, me_id, user_id)
        return FollowResponse.model_validate(follow)

    def unfollow_user(self, db: Session, me_id: str, user_id: str):
        if me_id == user_id:
            raise HTTPException(status_code=400, detail="Cannot unfollow yourself")
        success = follow_repo.unfollow_user(db, me_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Follow not found")

        return {"success": True}

    def list_followed_users(self, db: Session, me_id: str) -> FollowListResponse:
        users = follow_repo.list_followed_users(db, me_id)
        return FollowListResponse(followed_users=users)

    def is_followed_by_user(self, db: Session, me_id: str, user_id: str) -> bool:
        return follow_repo.is_followed_by_user(db, me_id, user_id)

    def has_followed_user(self, db: Session, me_id: str, user_id: str) -> bool:
        return follow_repo.has_followed_user(db, me_id, user_id)

follow_service = FollowService()