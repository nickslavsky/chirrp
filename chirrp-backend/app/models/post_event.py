import uuid
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, DateTime, JSON, String, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from .post import Post
    from .user import User


class PostEvent(Base):
    __tablename__ = "post_events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    post_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    event_version: Mapped[str] = mapped_column(String(16), nullable=False, server_default="v1", default="v1")
    snapshot: Mapped[dict] = mapped_column(JSON, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    post: Mapped["Post"] = relationship("Post", back_populates="events")
    author: Mapped["User"] = relationship("User", back_populates="post_events")

    __table_args__ = (
        Index("ix_post_events_author_created", "author_id", "created_at"),
        Index("ix_post_events_type_created", "event_type", "created_at"),
    )