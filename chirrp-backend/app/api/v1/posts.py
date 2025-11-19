from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select, update, func
from app.api.deps import get_db
from app.api.errors import create_error_response
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.api.deps import get_current_user_id_dep

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id_dep),
):
    new_post = Post(author_id=user_id, **post.model_dump())
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
    user_id: UUID = Depends(get_current_user_id_dep),  # note: UUID, not str
):
    post = db.scalar(
        select(Post)
        .where(Post.id == post_id, Post.deleted_at.is_(None))
    )
    if not post:
        raise create_error_response("NOT_FOUND", "Post not found", status.HTTP_404_NOT_FOUND)

    if post.author_id != user_id:
        raise create_error_response(
            "FORBIDDEN", "You can only edit your own posts", status.HTTP_403_FORBIDDEN
        )

    update_dict = update_data.model_dump(exclude_unset=True)
    if not update_dict:
        return post  # nothing to update

    db.execute(
        update(Post)
        .where(Post.id == post_id)
        .values(**update_dict, updated_at=func.now())
    )
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: UUID,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id_dep),  # now real JWT auth + ownership check
):
    post = db.scalar(
        select(Post)
        .where(Post.id == post_id, Post.deleted_at.is_(None))
    )
    if not post:
        raise create_error_response("NOT_FOUND", "Post not found", status.HTTP_404_NOT_FOUND)

    if post.author_id != user_id:
        raise create_error_response(
            "FORBIDDEN", "You can only delete your own posts", status.HTTP_403_FORBIDDEN
        )

    db.execute(update(Post).where(Post.id == post_id).values(deleted_at=func.now()))
    db.commit()
    return None