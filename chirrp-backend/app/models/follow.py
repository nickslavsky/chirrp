from uuid import uuid4
from sqlalchemy import Column, ForeignKey, String, DateTime, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class Follow(Base):
    __tablename__ = "follows"

    follower_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    followee_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (UniqueConstraint("follower_id", "followee_id", name="uq_follower_followee"),)


class SocialGraphEvent(Base):
    __tablename__ = "social_graph_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    follower_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    followee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    event_type = Column(String(20), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )