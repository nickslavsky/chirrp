from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

def get_auth_headers():
    return {"Authorization": f"Bearer {settings.CHIRRP_BEARER_TOKEN}"}