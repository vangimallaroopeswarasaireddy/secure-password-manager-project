import base64
import hashlib
from cryptography.fernet import Fernet

from app.config import get_settings

settings = get_settings()


def _derive_key(user_salt: str) -> bytes:
    digest = hashlib.sha256(f'{settings.FERNET_KEY}:{user_salt}'.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(digest)


def encrypt_value(value: str, user_salt: str) -> str:
    return Fernet(_derive_key(user_salt)).encrypt(value.encode('utf-8')).decode('utf-8')


def decrypt_value(encrypted_value: str, user_salt: str) -> str:
    return Fernet(_derive_key(user_salt)).decrypt(encrypted_value.encode('utf-8')).decode('utf-8')
