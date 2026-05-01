from datetime import datetime
from sqlalchemy.orm import Session
from app.db.models.refresh_tokens import RefreshToken
import uuid

class RefreshTokenRepository:
    def create(self, db: Session, user_id: uuid.UUID, token: str, expires_at: datetime) -> RefreshToken:
        rt = RefreshToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(rt)
        db.commit()
        db.refresh(rt)
        return rt

    def get_by_token(self, db: Session, token: str) -> RefreshToken | None:
        return db.query(RefreshToken).filter(RefreshToken.token == token).first()

    def revoke(self, db: Session, token: str) -> None:
        rt = self.get_by_token(db, token)
        if rt:
            rt.revoked = True
            db.commit()

    def revoke_all_by_user(self, db: Session, user_id: uuid.UUID) -> None:
        db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked == False,
        ).update({"revoked": True})
        db.commit()

refresh_token_repo = RefreshTokenRepository()