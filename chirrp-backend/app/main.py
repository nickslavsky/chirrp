from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import logging  # Import to configure
from app.api.v1.router import router as v1_router

app = FastAPI(title="Chirrp Backend", version="0.1")

app.include_router(v1_router, prefix=settings.API_V1_PREFIX)