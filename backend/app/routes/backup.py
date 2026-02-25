from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.models import User
from app.schemas.vault import BackupPayload, VaultCreateRequest
from app.services.vault_service import VaultService
from app.services.backup_service import BackupService

router = APIRouter(prefix='/backup', tags=['backup'])


@router.post('/export')
def export_backup(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    entries = VaultService.list_entries(db, current_user.id)
    serial = [VaultService.serialize_entry(entry, current_user.password_salt) for entry in entries]
    encrypted_blob = BackupService.export_entries(serial, current_user.password_salt)
    return {'encrypted_blob': encrypted_blob}


@router.post('/import')
def import_backup(payload: BackupPayload, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    entries = BackupService.import_entries(payload.encrypted_blob, current_user.password_salt)
    for item in entries:
        VaultService.create_entry(db, current_user.id, current_user.password_salt, VaultCreateRequest(**item))
    return {'message': f'Imported {len(entries)} entries'}
