# Chirrp Backend v0.1

A backend for a "Reddit meets X" service with nested comments.

## Prerequisites

- Docker
- Docker Compose

## Quickstart

1. Copy `.env.example` to `.env` and adjust if needed.

2. Build and start the services: `docker compose up --build`
3. Run the migrations inside the container: `docker exec -it chirrp-api alembic upgrade head`
4. Access the API at http://localhost:8001/api/v1/healthz (should return {"status": "ok"}). 
5. OpenAPI docs at http://localhost:8001/docs. 
6. Seed sample data: `docker compose exec api python -m scripts.seed`
7. List posts: `curl http://localhost:8001/api/v1/posts`
