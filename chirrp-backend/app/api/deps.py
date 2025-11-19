from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import SessionLocal
from app.core.security import get_current_user_id

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user_id_dep(user_id: str = Depends(get_current_user_id)):
    return user_id