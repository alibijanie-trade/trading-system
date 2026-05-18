# -*- coding: utf-8 -*-
"""
مدل ExchangeAPIKey — سند ۵.۴
================================================================
کلید API صرافی متعلق به یک کاربر.
🔒 api_key_encrypted و secret_key_encrypted با Fernet رمزنگاری می‌شوند
   (در service layer، با ENCRYPTION_KEY از .env). هرگز plaintext.

ستون‌ها (سند ۵.۴):
  id, user_id (FK→Users), exchange_id (FK→Exchanges),
  label, api_key_encrypted, secret_key_encrypted, permissions(JSON),
  is_active, is_deleted, created_at, updated_at
================================================================
"""

from app.infrastructure.database import Base, SoftDeleteMixin, TimestampMixin
from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ExchangeAPIKey(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "ExchangeAPIKeys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    exchange_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Exchanges.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    label: Mapped[str | None] = mapped_column(String, nullable=True)
    api_key_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    secret_key_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    permissions: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON: ["read","trade"]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # ===================================================
    # Relationships
    # ===================================================
    user: Mapped["User"] = relationship("User", back_populates="api_keys")
    exchange: Mapped["Exchange"] = relationship("Exchange", back_populates="api_keys")

    def __repr__(self) -> str:
        return (
            f"<ExchangeAPIKey id={self.id} user_id={self.user_id} "
            f"exchange_id={self.exchange_id} label={self.label!r}>"
        )
