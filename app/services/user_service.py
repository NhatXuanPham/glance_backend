import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.users import User
from app.repositories.user_repo import user_repo
from app.services.block_service import BlockService
from app.schemas.user_schema import UserResponse


class UserService:
    def __init__(self):
        self.block_service = BlockService()

    def get_me(self, db: Session, user_id: str) -> User:
        user = user_repo.get_by_id(db, uuid.UUID(user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_details_user(self, db: Session, user_id: str, requester_id: str) -> UserResponse:
        user = user_repo.get_by_id(db, uuid.UUID(user_id))
        if not user :
            raise HTTPException(status_code=404, detail="User not found")
        
        if self.block_service.is_blocked_by_user(db, requester_id, user_id):
            raise HTTPException(status_code=403, detail="something went wrong")

        return UserResponse(
            id=user.id,
            display_name=user.display_name,
            username=user.username,
            created_at=user.created_at,
            is_private=user.is_private,
            is_following=None,       # TODO: follow_service.is_following(db, requester_id, user_id)
            is_follower=None,        # TODO: follow_service.is_follower(db, requester_id, user_id)
            is_close_friend=None,    # TODO: follow_service.is_close_friend(...)
            is_restricted=None,      # TODO: follow_service.is_restricted(...)
            is_blocked_by_me=self.block_service.has_blocked_user(db, requester_id, user_id),
        )
    
user_service = UserService()