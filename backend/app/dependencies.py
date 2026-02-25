from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.models import User


def db_dep() -> Session:
    return Depends(get_db)


def current_user_dep() -> User:
    return Depends(get_current_user)
