from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.deps import get_db
from app.models.user import User
from app.schemas.auth import TokenRequest, TokenResponse
from app.core.security import create_access_token
from app.api.errors import create_error_response

router = APIRouter(tags=["auth"])


@router.post("/token", response_model=TokenResponse)
def get_token(request: TokenRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.id == request.user_id))
    if not user:
        raise create_error_response("NOT_FOUND", "User not found", status.HTTP_404_NOT_FOUND)

    access_token = create_access_token(user.id)
    return TokenResponse(access_token=access_token)