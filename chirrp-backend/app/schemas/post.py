from uuid import UUID
from pydantic import Field
from .base import ResponseBaseModel, RequestBaseModel

class PostCreate(RequestBaseModel):
    title: str | None = None
    body: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "My Post",
                    "body": "This is the content."
                }
            ]
        }
    }

class PostUpdate(RequestBaseModel):
    title: str | None = None
    body: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Updated Title",
                    "body": "Updated content."
                }
            ]
        }
    }

class PostResponse(ResponseBaseModel):
    id: UUID
    author_id: UUID
    title: str | None
    body: str
    deleted_at: str | None = None

    model_config = {"from_attributes": True}