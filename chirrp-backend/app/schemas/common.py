from datetime import datetime
from pydantic import BaseModel, field_serializer

class TimestampMixin(BaseModel):
    created_at: datetime
    updated_at: datetime

    @field_serializer('created_at', 'updated_at')
    def serialize_dt(self, dt: datetime) -> str:
        return dt.isoformat() + 'Z' if dt else None