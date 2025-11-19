from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from .common import TimestampMixin


class UserCreate(BaseModel):
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


class UserUpdate(BaseModel):
    display_name: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"display_name": "Johnny"}
            ]
        }
    }


class UserResponse(TimestampMixin):
    id: UUID
    username: str
    display_name: Optional[str] = None

    model_config = {"from_attributes": True}