# -*- coding: utf-8 -*-
"""
مدل AuditLog — سند ۵.۱۲ ⭐ 🆕 v2.1
================================================================
لاگ امنیتی DB-level — مکمل لاگ فایلی.
هر عمل مهم در سیستم (login، تغییر API Key، اجرای trade، ...) را
ثبت می‌کند.

ستون‌ها (سند ۵.۱۲):
  id, user_id (FK→Users, nullable), action, resource_type,
  resource_id, ip_address, user_agent, details (JSON),
  status (success/failed/blocked), created_at

دو ایندکس DESC (سند ۵.۱۲):
  - idx_audit_user_created   روی (user_id, created_at DESC)
  - idx_audit_action_created روی (action, created_at DESC)

نکته: AuditLog کاملاً immutable است — بدون updated_at و is_deleted.
       user_id nullable است برای رویدادهای سیستمی (بدون کاربر فعلی).
       اگر کاربر حذف فیزیکی شود، رکوردهای audit با user_id=NULL باقی می‌مانند.
================================================================
"""

from datetime import datetime, timezone

from app.infrastructure.database import Base
from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class AuditLog(Base):
    __tablename__ = "AuditLog"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("Users.id", ondelete="SET NULL"),
        nullable=True,
    )
    action: Mapped[str] = mapped_column(String, nullable=False)  # login/logout/create/update/...
    resource_type: Mapped[str | None] = mapped_column(String, nullable=True)
    resource_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String, nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON
    status: Mapped[str] = mapped_column(String, nullable=False)  # success/failed/blocked
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        nullable=False,
    )

    user: Mapped["User | None"] = relationship("User", back_populates="audit_logs")

    __table_args__ = (
        # ایندکس‌های DESC (سند ۵.۱۲) — SQLite syntax راه‌حل
        Index("idx_audit_user_created", "user_id", text("created_at DESC")),
        Index("idx_audit_action_created", "action", text("created_at DESC")),
    )

    def __repr__(self) -> str:
        return (
            f"<AuditLog id={self.id} action={self.action!r} "
            f"status={self.status!r} user_id={self.user_id}>"
        )
