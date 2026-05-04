import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class Restrict(Base):
    __tablename__ = "restricts"
    __table_args__ = (
        UniqueConstraint("user_id", "target_id", name="uq_restrict"),
        CheckConstraint("user_id != target_id", name="no_self_restrict"),
    )
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    target_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    user = relationship("User", foreign_keys=[user_id], back_populates="restricted_users")
    target = relationship("User", foreign_keys=[target_id], back_populates="restricted_by")