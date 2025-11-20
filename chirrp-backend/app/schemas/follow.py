from datetime import datetime
from uuid import UUID
from app.schemas.base import ResponseBaseModel


class FollowResponse(ResponseBaseModel):
    follower_id: UUID
    followee_id: UUID
    created_at: datetime

    model_config = {"from_attributes": True}