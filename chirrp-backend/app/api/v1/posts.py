from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select, update, func
from app.api.deps import get_db, require_bearer_token
from app.api.errors import create_error_response
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate, PostResponse

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    auth: bool = Depends(require_bearer_token),
):
    # For simplicity, assume a fixed user for testing; in real, from auth
    user = db.scalar(select(User).limit(1))
    if not user:
        raise create_error_response("NO_USERS", "No users found for testing", status.HTTP_500_INTERNAL_SERVER_ERROR)
    new_post = Post(id=uuid4(), author_id=user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("", response_model=list[PostResponse])
def list_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    stmt = select(Post).where(Post.deleted_at.is_(None)).order_by(Post.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    return db.scalars(stmt).all()

@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: UUID,
    db: Session = Depends(get_db),
):
    post = db.scalar(select(Post).where(Post.id == post_id, Post.deleted_at.is_(None)))
    if not post:
        raise create_error_response("NOT_FOUND", "Post not found", status.HTTP_404_NOT_FOUND)
    return post

@router.patch("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: UUID,
    update_data: PostUpdate,
    db: Session = Depends(get_db),
    auth: bool = Depends(require_bearer_token),
):
    post = db.scalar(select(Post).where(Post.id == post_id, Post.deleted_at.is_(None)))
    if not post:
        raise create_error_response("NOT_FOUND", "Post not found", status.HTTP_404_NOT_FOUND)
    update_dict = update_data.model_dump(exclude_unset=True)
    if update_dict:
        db.execute(update(Post).where(Post.id == post_id).values(**update_dict, updated_at=func.now()))
        db.commit()
        db.refresh(post)
    return post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: UUID,
    db: Session = Depends(get_db),
    auth: bool = Depends(require_bearer_token),
):
    post = db.scalar(select(Post).where(Post.id == post_id, Post.deleted_at.is_(None)))
    if not post:
        raise create_error_response("NOT_FOUND", "Post not found", status.HTTP_404_NOT_FOUND)
    db.execute(update(Post).where(Post.id == post_id).values(deleted_at=func.now()))
    db.commit()