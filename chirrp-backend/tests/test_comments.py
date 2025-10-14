from uuid import uuid4
from .conftest import client, get_auth_headers

def test_comments_crud():
    # Create post first
    post_payload = {"title": "Comment Test Post", "body": "Content"}
    post_res = client.post("/api/v1/posts", json=post_payload, headers=get_auth_headers())
    post_id = post_res.json()["id"]

    # Create top-level comment
    comment_payload = {"post_id": post_id, "body": "Top comment"}
    response = client.post("/api/v1/comments", json=comment_payload, headers=get_auth_headers())
    assert response.status_code == 201
    comment = response.json()
    comment_id = comment["id"]

    # Create reply
    reply_payload = {"post_id": post_id, "parent_comment_id": comment_id, "body": "Reply"}
    reply_res = client.post("/api/v1/comments", json=reply_payload, headers=get_auth_headers())
    assert reply_res.status_code == 201
    reply_id = reply_res.json()["id"]

    # Get tree
    response = client.get(f"/api/v1/posts/{post_id}/comments")
    assert response.status_code == 200
    tree = response.json()
    assert len(tree) == 1
    assert tree[0]["id"] == str(comment_id)
    assert len(tree[0]["children"]) == 1
    assert tree[0]["children"][0]["id"] == str(reply_id)

    # Get single
    response = client.get(f"/api/v1/comments/{comment_id}")
    assert response.status_code == 200

    # Update
    update_payload = {"body": "Updated top comment"}
    response = client.patch(f"/api/v1/comments/{comment_id}", json=update_payload, headers=get_auth_headers())
    assert response.status_code == 200
    assert response.json()["body"] == "Updated top comment"

    # Delete
    response = client.delete(f"/api/v1/comments/{comment_id}", headers=get_auth_headers())
    assert response.status_code == 204

    # Tree excludes deleted
    response = client.get(f"/api/v1/posts/{post_id}/comments")
    assert response.status_code == 200
    assert len(response.json()) == 0  # Reply should still be there but since top-level is deleted, and replies are descendants, but deleted top-level hides it? Wait, actually, since delete is soft and query excludes deleted, reply's parent is deleted but reply isn't, but in tree, top-level excludes deleted, so reply won't appear as top-level.