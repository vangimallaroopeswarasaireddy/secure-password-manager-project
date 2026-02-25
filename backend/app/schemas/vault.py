from datetime import datetime
from pydantic import BaseModel, Field


class VaultCreateRequest(BaseModel):
    site: str = Field(min_length=1, max_length=255)
    username: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1)
    notes: str | None = None
    tags: list[str] = []


class VaultUpdateRequest(BaseModel):
    site: str | None = Field(default=None, min_length=1, max_length=255)
    username: str | None = Field(default=None, min_length=1, max_length=255)
    password: str | None = None
    notes: str | None = None
    tags: list[str] | None = None


class VaultResponse(BaseModel):
    id: int
    site: str
    username: str
    password: str
    notes: str | None
    tags: list[str]
    updated_at: datetime


class BackupPayload(BaseModel):
    encrypted_blob: str
