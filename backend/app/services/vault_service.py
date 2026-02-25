import json
from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import VaultEntry, PasswordHistory
from app.schemas.vault import VaultCreateRequest, VaultUpdateRequest
from app.utils.crypto import encrypt_value, decrypt_value


class VaultService:
    @staticmethod
    def list_entries(db: Session, user_id: int, search: str | None = None, tag: str | None = None):
        query = db.query(VaultEntry).filter(VaultEntry.user_id == user_id)
        if search:
            pattern = f'%{search}%'
            query = query.filter(or_(VaultEntry.site.ilike(pattern), VaultEntry.username.ilike(pattern), VaultEntry.notes.ilike(pattern)))
        if tag:
            query = query.filter(VaultEntry.tags.ilike(f'%{tag}%'))
        return query.order_by(VaultEntry.updated_at.desc()).all()

    @staticmethod
    def create_entry(db: Session, user_id: int, user_salt: str, payload: VaultCreateRequest):
        entry = VaultEntry(
            user_id=user_id,
            site=payload.site,
            username=payload.username,
            encrypted_password=encrypt_value(payload.password, user_salt),
            notes=payload.notes,
            tags=json.dumps(payload.tags),
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    @staticmethod
    def update_entry(db: Session, user_id: int, user_salt: str, entry_id: int, payload: VaultUpdateRequest):
        entry = db.query(VaultEntry).filter(VaultEntry.user_id == user_id, VaultEntry.id == entry_id).first()
        if not entry:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Entry not found')

        if payload.password is not None:
            db.add(PasswordHistory(vault_entry_id=entry.id, encrypted_password=entry.encrypted_password))
            entry.encrypted_password = encrypt_value(payload.password, user_salt)
        if payload.site is not None:
            entry.site = payload.site
        if payload.username is not None:
            entry.username = payload.username
        if payload.notes is not None:
            entry.notes = payload.notes
        if payload.tags is not None:
            entry.tags = json.dumps(payload.tags)

        db.commit()
        db.refresh(entry)
        return entry

    @staticmethod
    def delete_entry(db: Session, user_id: int, entry_id: int):
        deleted = db.query(VaultEntry).filter(VaultEntry.user_id == user_id, VaultEntry.id == entry_id).delete()
        db.commit()
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Entry not found')

    @staticmethod
    def serialize_entry(entry: VaultEntry, user_salt: str) -> dict:
        return {
            'id': entry.id,
            'site': entry.site,
            'username': entry.username,
            'password': decrypt_value(entry.encrypted_password, user_salt),
            'notes': entry.notes,
            'tags': json.loads(entry.tags or '[]'),
            'updated_at': entry.updated_at,
        }
