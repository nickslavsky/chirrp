from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import insert, delete, exists, select

from app.api.deps import get_db, get_current_user_id_dep
from app.api.errors import create_error_response
from app.models.follow import Follow, SocialGraphEvent
from app.models.user import User
from app.schemas.follow import FollowResponse

router = APIRouter(prefix="/users/me/following", tags=["follows"])


@router.post("/{followee_id}", response_model=FollowResponse, status_code=status.HTTP_201_CREATED)
def follow_user(
    followee_id: UUID,
    db: Session = Depends(get_db),
    follower_id: UUID = Depends(get_current_user_id_dep),
):
    if follower_id == followee_id:
        raise create_error_response(
            "BAD_REQUEST", "You cannot follow yourself", status.HTTP_400_BAD_REQUEST
        )

    # Check that followee exists
    followee = db.get(User, followee_id)
    if not followee:
        raise create_error_response("NOT_FOUND", "User not found", status.HTTP_404_NOT_FOUND)

    # Check if already following

    already_following = db.scalar(
        select(1).where(
            Follow.follower_id==follower_id,
            Follow.followee_id==followee_id
        )
    ) is not None
    if already_following:
        raise create_error_response(
            "CONFLICT", "You are already following this user", status.HTTP_409_CONFLICT
        )

    # Atomically create follow relationship + event log
    follow = Follow(follower_id=follower_id, followee_id=followee_id)
    event = SocialGraphEvent(
        follower_id=follower_id,
        followee_id=followee_id,
        event_type="followed",
    )

    db.add(follow)
    db.add(event)
    db.commit()
    db.refresh(follow)

    return follow


@router.delete("/{followee_id}", status_code=status.HTTP_204_NO_CONTENT)
def unfollow_user(
    followee_id: UUID,
    db: Session = Depends(get_db),
    follower_id: UUID = Depends(get_current_user_id_dep),
):
    if follower_id == followee_id:
        raise create_error_response(
            "BAD_REQUEST", "You cannot unfollow yourself", status.HTTP_400_BAD_REQUEST
        )

    # Delete the relationship (if exists)
    result = db.execute(
        delete(Follow).where(
            Follow.follower_id == follower_id,
            Follow.followee_id == followee_id,
        )
    )

    if result.rowcount == 0:
        raise create_error_response(
            "NOT_FOUND", "You are not following this user", status.HTTP_404_NOT_FOUND
        )

    # Append unfollow event
    event = SocialGraphEvent(
        follower_id=follower_id,
        followee_id=followee_id,
        event_type="unfollowed",
    )
    db.add(event)
    db.commit()

    return None