from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import User, RefreshToken
from app.schemas.auth import RegisterRequest, LoginRequest
from app.utils.security import (
    create_access_token,
    create_refresh_token,
    generate_salt,
    hash_password,
    verify_password,
    token_fingerprint,
    validate_password_strength,
    safe_decode,
)
from app.utils.totp import generate_totp_secret, verify_totp


class AuthService:
    @staticmethod
    def register(db: Session, payload: RegisterRequest) -> tuple[User, str | None]:
        existing = db.query(User).filter(User.email == payload.email.lower()).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already registered')
        if not validate_password_strength(payload.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Weak password')

        salt = generate_salt()
        user = User(
            email=payload.email.lower(),
            password_hash=hash_password(payload.password, salt),
            password_salt=salt,
            is_2fa_enabled=payload.enable_2fa,
            totp_secret=generate_totp_secret() if payload.enable_2fa else None,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user, user.totp_secret

    @staticmethod
    def login(db: Session, payload: LoginRequest) -> tuple[str, str]:
        user = db.query(User).filter(User.email == payload.email.lower()).first()
        if not user or not verify_password(payload.password, user.password_salt, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
        if user.is_2fa_enabled and not verify_totp(user.totp_secret or '', payload.totp_code or ''):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid 2FA code')

        access_token = create_access_token(str(user.id))
        refresh_token, expires_at = create_refresh_token(str(user.id))
        db.add(RefreshToken(user_id=user.id, token_hash=token_fingerprint(refresh_token), expires_at=expires_at))
        db.commit()
        return access_token, refresh_token

    @staticmethod
    def refresh(db: Session, refresh_token: str) -> tuple[str, str]:
        token_data = safe_decode(refresh_token, refresh=True)
        if not token_data or token_data.get('type') != 'refresh':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')
        token_row = db.query(RefreshToken).filter(RefreshToken.token_hash == token_fingerprint(refresh_token)).first()
        if not token_row:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Refresh token revoked')
        access_token = create_access_token(token_data['sub'])
        new_refresh_token, expires_at = create_refresh_token(token_data['sub'])
        token_row.token_hash = token_fingerprint(new_refresh_token)
        token_row.expires_at = expires_at
        db.commit()
        return access_token, new_refresh_token

    @staticmethod
    def logout(db: Session, refresh_token: str) -> None:
        db.query(RefreshToken).filter(RefreshToken.token_hash == token_fingerprint(refresh_token)).delete()
        db.commit()
