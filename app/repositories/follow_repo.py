from sqlalchemy.orm import Session
from app.db.models.follows import Follow
import uuid

class FollowRepo:
    def follow_user(self, db: Session, follower_id: str, following_id: str) -> Follow:
        follow = Follow(
            follower_id=uuid.UUID(follower_id),
            following_id=uuid.UUID(following_id)
        )
        db.add(follow)
        db.commit()
        db.refresh(follow)
        return follow

    def unfollow_user(self, db: Session, follower_id: str, following_id: str) -> bool:
        follow = db.query(Follow).filter(
            Follow.follower_id == uuid.UUID(follower_id),
            Follow.following_id == uuid.UUID(following_id)
        ).first()
        if not follow:
            return False
        db.delete(follow)
        db.commit()
        return True

    def list_followed_users(self, db: Session, follower_id: str) -> list[uuid.UUID]:
        rows = db.query(Follow.following_id).filter(
            Follow.follower_id == uuid.UUID(follower_id)
        ).all()
        return [row.following_id for row in rows]

    def is_followed_by_user(self, db: Session, me_id: str, user_id: str) -> bool:
        return db.query(Follow).filter(
            Follow.follower_id == uuid.UUID(user_id),
            Follow.following_id == uuid.UUID(me_id)
        ).first() is not None

    def has_followed_user(self, db: Session, me_id: str, user_id: str) -> bool:
        return db.query(Follow).filter(
            Follow.follower_id == uuid.UUID(me_id),
            Follow.following_id == uuid.UUID(user_id)
        ).first() is not None

follow_repo = FollowRepo()