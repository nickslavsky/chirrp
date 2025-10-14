from uuid import uuid4
from .conftest import client, get_auth_headers

def test_posts_crud():
    # Create
    create_payload = {"title": "Test Post", "body": "Content"}
    response = client.post("/api/v1/posts", json=create_payload, headers=get_auth_headers())
    assert response.status_code == 201
    post = response.json()
    post_id = post["id"]

    # Get
    response = client.get(f"/api/v1/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["body"] == "Content"

    # List
    response = client.get("/api/v1/posts")
    assert response.status_code == 200
    assert any(p["id"] == post_id for p in response.json())

    # Update
    update_payload = {"body": "Updated Content"}
    response = client.patch(f"/api/v1/posts/{post_id}", json=update_payload, headers=get_auth_headers())
    assert response.status_code == 200
    assert response.json()["body"] == "Updated Content"

    # Delete
    response = client.delete(f"/api/v1/posts/{post_id}", headers=get_auth_headers())
    assert response.status_code == 204

    # List excludes deleted
    response = client.get("/api/v1/posts")
    assert response.status_code == 200
    assert not any(p["id"] == post_id for p in response.json())