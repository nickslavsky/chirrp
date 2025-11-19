from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select, update, func

from app.api.deps import get_db, get_current_user_id_dep
from app.api.errors import create_error_response
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    exists = db.scalar(select(User).where(User.username == user_in.username))
    if exists:
        raise create_error_response("CONFLICT", "Username already taken", status.HTTP_409_CONFLICT)

    user = User(username=user_in.username, display_name=user_in.display_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/me", response_model=UserResponse)
def read_current_user(
    user_id: str = Depends(get_current_user_id_dep),
    db: Session = Depends(get_db),
):
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise create_error_response("NOT_FOUND", "User not found", status.HTTP_404_NOT_FOUND)
    return user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise create_error_response("NOT_FOUND", "User not found", status.HTTP_404_NOT_FOUND)
    return user


@router.patch("/me", response_model=UserResponse)
def update_current_user(
    update_data: UserUpdate,
    user_id: str = Depends(get_current_user_id_dep),
    db: Session = Depends(get_db),
):
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise create_error_response("NOT_FOUND", "User not found", status.HTTP_404_NOT_FOUND)

    update_dict = update_data.model_dump(exclude_unset=True)
    if update_dict:
        db.execute(update(User).where(User.id == user_id).values(**update_dict))
        db.commit()
        db.refresh(user)
    return user