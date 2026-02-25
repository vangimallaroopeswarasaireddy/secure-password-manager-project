from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.rate_limit import limiter
from app.schemas.auth import RegisterRequest, LoginRequest, RefreshRequest, AuthResponse, MessageResponse, TwoFASetupResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register')
@limiter.limit('20/hour')
def register(request: Request, payload: RegisterRequest, db: Session = Depends(get_db)):
    user, secret = AuthService.register(db, payload)
    response = {'message': 'Registration successful'}
    if secret:
        return {**response, '2fa': TwoFASetupResponse(secret=secret).model_dump()}
    return response


@router.post('/login', response_model=AuthResponse)
@limiter.limit('10/minute')
def login(request: Request, payload: LoginRequest, db: Session = Depends(get_db)):
    access_token, refresh_token = AuthService.login(db, payload)
    return AuthResponse(access_token=access_token, refresh_token=refresh_token)


@router.post('/refresh', response_model=AuthResponse)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    access_token, refresh_token = AuthService.refresh(db, payload.refresh_token)
    return AuthResponse(access_token=access_token, refresh_token=refresh_token)


@router.post('/logout', response_model=MessageResponse)
def logout(payload: RefreshRequest, db: Session = Depends(get_db)):
    AuthService.logout(db, payload.refresh_token)
    return MessageResponse(message='Logged out')
