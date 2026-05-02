import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.users import User
from app.repositories.user_repo import user_repo

class UserService:
    def get_me(self, db: Session, user_id: str) -> User:
        user = user_repo.get_by_id(db, uuid.UUID(user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

user_service = UserService()