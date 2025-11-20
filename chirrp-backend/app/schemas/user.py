from uuid import UUID
from typing import Optional
from pydantic import Field, EmailStr
from .base import ResponseBaseModel, RequestBaseModel


class UserCreate(RequestBaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    display_name: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "john_doe",
                    "display_name": "John Doe"
                }
            ]
        }
    }


class UserUpdate(RequestBaseModel):
    display_name: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"display_name": "Johnny"}
            ]
        }
    }


class UserResponse(ResponseBaseModel):
    id: UUID
    username: str
    display_name: Optional[str] = None

    model_config = {"from_attributes": True}