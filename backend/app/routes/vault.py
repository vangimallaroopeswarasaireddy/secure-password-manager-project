from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.models import User
from app.schemas.vault import VaultCreateRequest, VaultUpdateRequest
from app.services.vault_service import VaultService

router = APIRouter(prefix='/vault', tags=['vault'])


@router.get('')
def list_vault(
    search: str | None = Query(default=None),
    tag: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entries = VaultService.list_entries(db, current_user.id, search=search, tag=tag)
    return [VaultService.serialize_entry(entry, current_user.password_salt) for entry in entries]


@router.post('')
def create_vault(payload: VaultCreateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    entry = VaultService.create_entry(db, current_user.id, current_user.password_salt, payload)
    return VaultService.serialize_entry(entry, current_user.password_salt)


@router.put('/{entry_id}')
def update_vault(
    entry_id: int,
    payload: VaultUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = VaultService.update_entry(db, current_user.id, current_user.password_salt, entry_id, payload)
    return VaultService.serialize_entry(entry, current_user.password_salt)


@router.delete('/{entry_id}')
def delete_vault(entry_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    VaultService.delete_entry(db, current_user.id, entry_id)
    return {'message': 'Deleted'}
