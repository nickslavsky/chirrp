import uuid
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
if TYPE_CHECKING:
    from .post import Post
    from .comment import Comment
    from .post_event import PostEvent


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    display_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    posts: Mapped[List["Post"]] = relationship(
        "Post", back_populates="author", lazy="selectin", cascade="all, delete-orphan"
    )
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="author", lazy="selectin", cascade="all, delete-orphan"
    )
    post_events: Mapped[List["PostEvent"]] = relationship(
        "PostEvent", back_populates="author", lazy="selectin", cascade="all, delete-orphan"
    )
    following: Mapped[List["User"]] = relationship(
        "User",
        secondary="follows",
        primaryjoin="User.id == Follow.follower_id",
        secondaryjoin="User.id == Follow.followee_id",
        back_populates="followers",
        lazy="selectin"
    )
    followers: Mapped[List["User"]] = relationship(
        "User",
        secondary="follows",
        primaryjoin="User.id == Follow.followee_id",
        secondaryjoin="User.id == Follow.follower_id",
        back_populates="following",
        lazy="selectin"
    )