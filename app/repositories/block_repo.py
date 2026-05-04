from sqlalchemy.orm import Session
from app.db.models.blocks import Block
import uuid

class BlockRepo:
    def block_user(self, db: Session, blocker_id: str, blocked_id: str) -> Block:
        block = Block(
            blocker_id=uuid.UUID(blocker_id),
            blocked_id=uuid.UUID(blocked_id)
        )
        db.add(block)
        db.commit()
        db.refresh(block)
        return block

    def unblock_user(self, db: Session, blocker_id: str, blocked_id: str) -> bool:
        block = db.query(Block).filter(
            Block.blocker_id == uuid.UUID(blocker_id),
            Block.blocked_id == uuid.UUID(blocked_id)
        ).first()
        if not block:
            return False
        db.delete(block)
        db.commit()
        return True

    def list_blocked_users(self, db: Session, blocker_id: str) -> list[uuid.UUID]:
        rows = db.query(Block.blocked_id).filter(
            Block.blocker_id == uuid.UUID(blocker_id)
        ).all()
        return [row.blocked_id for row in rows]

    def is_blocked_by_user(self, db: Session, me_id: str, user_id: str) -> bool:
        return db.query(Block).filter(
            Block.blocker_id == uuid.UUID(user_id),
            Block.blocked_id == uuid.UUID(me_id)
        ).first() is not None

    def has_blocked_user(self, db: Session, me_id: str, user_id: str) -> bool:
        return db.query(Block).filter(
            Block.blocker_id == uuid.UUID(me_id),
            Block.blocked_id == uuid.UUID(user_id)
        ).first() is not None

block_repo = BlockRepo()