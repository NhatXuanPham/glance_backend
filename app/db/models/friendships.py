import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Enum as SQLEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
class FriendshipStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    BLOCKED = "blocked"
class Friendship(Base):
    __tablename__ = "friendships"

    __table_args__ = (
        CheckConstraint(
            "user_id_1 < user_id_2",
            name="ck_friendships_user_id_order",
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id_1 = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user_id_2 = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    status = Column(
        SQLEnum(FriendshipStatus, name="friendship_status"),
        nullable=False,
        default=FriendshipStatus.PENDING
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user_1 = relationship("User", foreign_keys=[user_id_1])
    user_2 = relationship("User", foreign_keys=[user_id_2])