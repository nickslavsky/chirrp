from fastapi import APIRouter

router = APIRouter(prefix="/healthz", tags=["health"])

@router.get("", response_model=dict)
def health_check():
    return {"status": "ok"}