from fastapi import APIRouter
from .posts import router as posts_router
from .comments import router as comments_router
from .health import router as health_router

router = APIRouter()

router.include_router(health_router)
router.include_router(posts_router)
router.include_router(comments_router)