# app/schemas/base.py
from datetime import datetime, timezone
from pydantic import BaseModel as PydanticBaseModel, field_serializer


# Only response models inherit from this
class ResponseBaseModel(PydanticBaseModel):
    model_config = {"from_attributes": True}

    @field_serializer("*", when_used="json")
    def serialize_datetimes(self, value):
        if isinstance(value, datetime):
            return value.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
        return value


# Request bodies (Create/Update) stay plain BaseModel → no serialization logic
class RequestBaseModel(PydanticBaseModel):
    model_config = {"extra": "forbid"}  # optional: be strict on input