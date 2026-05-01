import uuid

from sqlalchemy import Boolean, Column, Date, DateTime, String, Text, CheckConstraint
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
    refresh_tokens = relationship("RefreshToken", back_populates="user")