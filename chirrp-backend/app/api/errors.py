from fastapi import HTTPException, status

def create_error_response(code: str, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
    return HTTPException(
        status_code=status_code,
        detail={"error": {"code": code, "message": message}},
    )