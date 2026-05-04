import uuid

from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, Text, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            "(email IS NOT NULL) OR (phone_number IS NOT NULL)",
            name="ck_users_email_or_phone",
        ),
    )
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    display_name = Column(String(255), nullable=False)
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    phone_number = Column(String(20), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=True)
    avatar_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    dob = Column(Date, nullable=True)
    active = Column(Boolean, default=True, nullable=False)
    is_private = Column(Boolean, default=False, nullable=False)
    refresh_tokens = relationship("RefreshToken", back_populates="user")
    total_followers = Column(Integer, default=0, nullable=False)
    total_following = Column(Integer, default=0, nullable=False)
    total_posts = Column(Integer, default=0, nullable=False)
    followers = relationship(
        "Follow",
        foreign_keys="Follow.following_id",
        back_populates="following",
        cascade="all, delete-orphan"
    )
    following = relationship(
        "Follow",
        foreign_keys="Follow.follower_id",
        back_populates="follower",
        cascade="all, delete-orphan"
    )
    sent_requests = relationship(
        "FollowRequest",
        foreign_keys="FollowRequest.requester_id",
        back_populates="requester",
        cascade="all, delete-orphan"
    )
    received_requests = relationship(
        "FollowRequest",
        foreign_keys="FollowRequest.target_id",
        back_populates="target",
        cascade="all, delete-orphan"
    )
    blocked_users = relationship(
        "Block",
        foreign_keys="Block.blocker_id",
        back_populates="blocker",
        cascade="all, delete-orphan"
    )
    blocked_by = relationship(
        "Block",
        foreign_keys="Block.blocked_id",
        back_populates="blocked",
        cascade="all, delete-orphan"
    )
    restricted_users = relationship(
        "Restrict",
        foreign_keys="Restrict.user_id",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    restricted_by = relationship(
        "Restrict",
        foreign_keys="Restrict.target_id",
        back_populates="target",
        cascade="all, delete-orphan"
    )