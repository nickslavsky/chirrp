from sqlalchemy.orm import Session
from app.models.post_event import PostEvent
from app.models.post import Post

EVENT_POST_CREATED = "post.created"
EVENT_POST_UPDATED = "post.updated"
EVENT_POST_DELETED = "post.deleted"


def emit_post_event(
    db: Session,
    post: Post,
    event_type: str,
    event_version: str = "v1",
    extra: dict | None = None,
):
    snapshot = {
        "id": str(post.id),
        "author_id": str(post.author_id),
        "title": post.title,
        "body": post.body,
        "created_at": post.created_at.isoformat() if post.created_at else None,
        "updated_at": post.updated_at.isoformat() if post.updated_at else None,
        "deleted_at": post.deleted_at.isoformat() if post.deleted_at else None,
    }
    if extra:
        snapshot.update(extra)

    event = PostEvent(
        post_id=post.id,
        author_id=post.author_id,
        event_type=event_type,
        event_version=event_version,
        snapshot=snapshot,
    )
    db.add(event)