import uuid
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), nullable=True)

    author: Mapped["User"] = relationship("User", back_populates="posts")
    events: Mapped[List["PostEvent"]] = relationship(
        "PostEvent",
        back_populates="post",
        lazy="selectin",
        cascade="all, delete-orphan",
        order_by="PostEvent.created_at.desc()"
    )
    comments: Mapped[List["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        lazy="selectin",
        cascade="all, delete-orphan"
    )