from sqlalchemy.orm import Session
from app.db.models.users import User
import uuid

class UserRepository:
    def get_by_id(self, db: Session, user_id: uuid.UUID) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, **kwargs) -> User:
        user = User(**kwargs)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

user_repo = UserRepository()