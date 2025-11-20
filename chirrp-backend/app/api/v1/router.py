from fastapi import APIRouter
from .posts import router as posts_router
from .comments import router as comments_router
from .health import router as health_router
from .auth import router as auth_router
from .users import router as users_router
from .follows import router as follow_router

router = APIRouter()

router.include_router(health_router)
router.include_router(posts_router)
router.include_router(comments_router)
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(follow_router)
