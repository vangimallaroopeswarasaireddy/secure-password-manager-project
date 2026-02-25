import hashlib
import secrets
import string
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import get_settings

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')
settings = get_settings()


def generate_salt() -> str:
    return secrets.token_hex(16)


def hash_password(password: str, salt: str) -> str:
    return pwd_context.hash(f'{password}{salt}')


def verify_password(password: str, salt: str, hashed_password: str) -> bool:
    return pwd_context.verify(f'{password}{salt}', hashed_password)


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({'sub': subject, 'exp': expire, 'type': 'access'}, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(subject: str) -> tuple[str, datetime]:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    token = jwt.encode({'sub': subject, 'exp': expire, 'type': 'refresh'}, settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token, expire


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])


def decode_refresh_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])


def token_fingerprint(token: str) -> str:
    return hashlib.sha256(token.encode('utf-8')).hexdigest()


def validate_password_strength(password: str) -> bool:
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    return len(password) >= 12 and has_upper and has_lower and has_digit and has_special


def safe_decode(token: str, refresh: bool = False) -> dict | None:
    try:
        return decode_refresh_token(token) if refresh else decode_access_token(token)
    except JWTError:
        return None
