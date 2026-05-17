# -*- coding: utf-8 -*-
"""
مدل UserSession — سند ۵.۲
================================================================
Session احراز هویت کاربر (JWT token + متادیتای ورود).
نام جدول طبق سند ۵.۲ → "Sessions"
نام کلاس Python → `UserSession` (برای جلوگیری از تداخل با
sqlalchemy.orm.Session)

ستون‌ها (سند ۵.۲):
  id, user_id (FK→Users), token (UNIQUE), ip_address,
  expires_at, is_revoked, created_at

نکته: UserSession مشمول soft delete نیست — هنگام logout/expire
رکوردهای فیزیکی حذف می‌شوند یا is_revoked=True می‌گیرند.
================================================================
"""

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class UserSession(Base):
    __tablename__ = "Sessions"  # نام جدول طبق سند ۵.۲

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True,
    )
    ip_address: Mapped[str | None] = mapped_column(String, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
    )
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="sessions")

    def __repr__(self) -> str:
        return f"<UserSession id={self.id} user_id={self.user_id} revoked={self.is_revoked}>"
