import uuid
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment

engine = create_engine(settings.DATABASE_URL)

with Session(engine) as session:
    # Idempotent: check if users exist
    if not session.scalar(select(User).where(User.username == "user1")):
        user1 = User(id=uuid.uuid4(), username="user1", display_name="User One")
        user2 = User(id=uuid.uuid4(), username="user2", display_name="User Two")
        session.add_all([user1, user2])
        session.commit()

    user1 = session.scalar(select(User).where(User.username == "user1"))
    user2 = session.scalar(select(User).where(User.username == "user2"))

    # Check if post exists
    if not session.scalar(select(Post).where(Post.title == "Sample Post")):
        post = Post(id=uuid.uuid4(), author_id=user1.id, title="Sample Post", body="This is a sample post.")
        session.add(post)
        session.commit()

    post = session.scalar(select(Post).where(Post.title == "Sample Post"))

    # Comments
    if not session.scalar(select(Comment).where(Comment.body == "Top-level comment 1")):
        comment1 = Comment(id=uuid.uuid4(), post_id=post.id, author_id=user1.id, body="Top-level comment 1")
        comment2 = Comment(id=uuid.uuid4(), post_id=post.id, author_id=user2.id, body="Top-level comment 2")
        reply1 = Comment(id=uuid.uuid4(), post_id=post.id, parent_comment_id=comment1.id, author_id=user2.id, body="Reply to comment 1")
        session.add_all([comment1, comment2, reply1])
        session.commit()

print("Seed data inserted.")