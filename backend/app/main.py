from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.config import get_settings
from app.database import Base, engine
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.routes.auth import router as auth_router
from app.routes.vault import router as vault_router
from app.routes.backup import router as backup_router

settings = get_settings()
from app.rate_limit import limiter

app = FastAPI(title=settings.APP_NAME)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(',')],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(vault_router)
app.include_router(backup_router)


@app.get('/health')
def health_check():
    return {'status': 'ok'}
