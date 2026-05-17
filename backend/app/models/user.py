# -*- coding: utf-8 -*-
"""
مدل User — سند ۵.۱
================================================================
کاربر سیستم. هر کاربر یک یا چند Session، چندین API Key صرافی،
Watchlist، Strategy، Trade، و تنظیمات شخصی دارد.

ستون‌ها (سند ۵.۱):
  id, username (UNIQUE), password_hash, role, is_active,
  last_login, is_deleted, created_at, updated_at

نقش‌ها (role): admin | trader | viewer

رمز عبور:
  - password_hash با bcrypt در service layer ساخته می‌شود
  - هرگز plaintext ذخیره نشود
================================================================
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base, SoftDeleteMixin, TimestampMixin


class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True,
    )
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)  # admin/trader/viewer
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
    )

    # ===================================================
    # Relationships — Part 1 (مدل‌های ساخته‌شده در همین اسکریپت)
    # ===================================================
    sessions: Mapped[list["UserSession"]] = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    api_keys: Mapped[list["ExchangeAPIKey"]] = relationship(
        "ExchangeAPIKey",
        back_populates="user",
    )
    watchlist: Mapped[list["Watchlist"]] = relationship(
        "Watchlist",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    risk_settings: Mapped["RiskSettings | None"] = relationship(
        "RiskSettings",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    app_settings: Mapped["AppSettings | None"] = relationship(
        "AppSettings",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # ===================================================
    # Relationships — Part 2 (مدل‌های اسکریپت بعدی)
    # تا configure_mappers صدا زده نشود، string-form OK است.
    # ===================================================
    strategies: Mapped[list["Strategy"]] = relationship(
        "Strategy",
        back_populates="user",
    )
    trades: Mapped[list["Trade"]] = relationship(
        "Trade",
        back_populates="user",
    )
    portfolio: Mapped[list["Portfolio"]] = relationship(
        "Portfolio",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    alerts: Mapped[list["Alert"]] = relationship(
        "Alert",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="user",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r} role={self.role!r}>"
