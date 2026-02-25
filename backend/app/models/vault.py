from datetime import datetime
from sqlalchemy import String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class VaultEntry(Base):
    __tablename__ = 'vault_entries'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    site: Mapped[str] = mapped_column(String(255), index=True)
    username: Mapped[str] = mapped_column(String(255))
    encrypted_password: Mapped[str] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship('User', back_populates='vault_entries')
    history = relationship('PasswordHistory', back_populates='vault_entry', cascade='all, delete-orphan')


class PasswordHistory(Base):
    __tablename__ = 'password_history'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vault_entry_id: Mapped[int] = mapped_column(ForeignKey('vault_entries.id', ondelete='CASCADE'), index=True)
    encrypted_password: Mapped[str] = mapped_column(Text)
    changed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    vault_entry = relationship('VaultEntry', back_populates='history')
