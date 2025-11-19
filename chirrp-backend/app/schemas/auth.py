from uuid import UUID
from pydantic import BaseModel


class TokenRequest(BaseModel):
    user_id: UUID


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"