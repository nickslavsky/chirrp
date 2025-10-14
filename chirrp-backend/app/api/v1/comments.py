from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select, update, func
from app.api.deps import get_db, require_bearer_token
from app.api.errors import create_error_response
from app.models.comment import Comment
from app.models.user import User
from app.models.post import Post
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.services.comment_tree import build_comment_tree

router = APIRouter(tags=["comments"])

@router.post("/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    auth: bool = Depends(require_bearer_token),
):
    # Fixed user for testing
    user = db.scalar(select(User).limit(1))
    if not user:
        raise create_error_response("NO_USERS", "No users found for testing", status.HTTP_500_INTERNAL_SERVER_ERROR)
    if not db.scalar(select(Post).where(Post.id == comment.post_id)):
        raise create_error_response("NOT_FOUND", "Post not found", status.HTTP_404_NOT_FOUND)
    if comment.parent_comment_id and not db.scalar(select(Comment).where(Comment.id == comment.parent_comment_id)):
        raise create_error_response("NOT_FOUND", "Parent comment not found", status.HTTP_404_NOT_FOUND)
    new_comment = Comment(id=uuid4(), author_id=user.id, **comment.model_dump())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/posts/{post_id}/comments", response_model=list[CommentResponse])
def get_post_comments(
    post_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    if not db.scalar(select(Post).where(Post.id == post_id, Post.deleted_at.is_(None))):
        raise create_error_response("NOT_FOUND", "Post not found", status.HTTP_404_NOT_FOUND)
    # Fetch all comments for the post (non-paginated descendants)
    all_comments_stmt = select(Comment).where(Comment.post_id == post_id, Comment.deleted_at.is_(None))
    all_comments = db.scalars(all_comments_stmt).all()
    # Paginate only top-level
    top_level_stmt = select(Comment).where(Comment.post_id == post_id, Comment.parent_comment_id.is_(None), Comment.deleted_at.is_(None)).order_by(Comment.created_at.asc()).offset((page - 1) * page_size).limit(page_size)
    top_level_comments = db.scalars(top_level_stmt).all()
    tree = build_comment_tree(all_comments, top_level_comments)
    return tree

@router.get("/comments/{comment_id}", response_model=CommentResponse)
def get_comment(
    comment_id: UUID,
    db: Session = Depends(get_db),
):
    comment = db.scalar(select(Comment).where(Comment.id == comment_id, Comment.deleted_at.is_(None)))
    if not comment:
        raise create_error_response("NOT_FOUND", "Comment not found", status.HTTP_404_NOT_FOUND)
    return comment

@router.patch("/comments/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: UUID,
    update_data: CommentUpdate,
    db: Session = Depends(get_db),
    auth: bool = Depends(require_bearer_token),
):
    comment = db.scalar(select(Comment).where(Comment.id == comment_id, Comment.deleted_at.is_(None)))
    if not comment:
        raise create_error_response("NOT_FOUND", "Comment not found", status.HTTP_404_NOT_FOUND)
    update_dict = update_data.model_dump(exclude_unset=True)
    if update_dict:
        db.execute(update(Comment).where(Comment.id == comment_id).values(**update_dict, updated_at=func.now()))
        db.commit()
        db.refresh(comment)
    return comment

@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: UUID,
    db: Session = Depends(get_db),
    auth: bool = Depends(require_bearer_token),
):
    comment = db.scalar(select(Comment).where(Comment.id == comment_id, Comment.deleted_at.is_(None)))
    if not comment:
        raise create_error_response("NOT_FOUND", "Comment not found", status.HTTP_404_NOT_FOUND)
    db.execute(update(Comment).where(Comment.id == comment_id).values(deleted_at=func.now()))
    db.commit()