from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

security_scheme = HTTPBearer()

def require_bearer_token(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
):
    if credentials.credentials != settings.CHIRRP_BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": {"code": "UNAUTHORIZED", "message": "Invalid token"}},
        )
    return True