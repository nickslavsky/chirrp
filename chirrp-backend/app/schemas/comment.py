from uuid import UUID
from typing import List
from pydantic import BaseModel, Field
from .common import TimestampMixin

class CommentCreate(BaseModel):
    post_id: UUID
    parent_comment_id: UUID | None = None
    body: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "post_id": "123e4567-e89b-12d3-a456-426614174000",
                    "parent_comment_id": None,
                    "body": "This is a comment."
                }
            ]
        }
    }

class CommentUpdate(BaseModel):
    body: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "body": "Updated comment."
                }
            ]
        }
    }

class CommentResponse(TimestampMixin):
    id: UUID
    post_id: UUID
    parent_comment_id: UUID | None
    author_id: UUID
    body: str
    deleted_at: str | None = None
    children: List["CommentResponse"] = Field(default_factory=list)

    model_config = {"from_attributes": True}