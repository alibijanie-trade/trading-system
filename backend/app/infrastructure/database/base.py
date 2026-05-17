# -*- coding: utf-8 -*-
"""
Base Classes و Mixins برای مدل‌های SQLAlchemy
================================================================
این فایل پایه‌ای‌ترین کلاس‌های ORM را تعریف می‌کند که تمام مدل‌ها
از آن‌ها ارث می‌برند.

اجزا:
  - Base            → DeclarativeBase (SQLAlchemy 2.0 style)
  - TimestampMixin  → created_at + updated_at (UTC)
  - SoftDeleteMixin → is_deleted

تصمیمات معماری مرتبط:
  - سند ۵.۰  : تمام datetime ها timezone-aware و UTC ذخیره شوند
  - سند ۴.۵  : نام جداول PascalCase (Users, OhlcvData, AuditLog, ...)
  - استفاده از datetime.now(timezone.utc) — utcnow() در Python 3.12+ deprecated است
  - استفاده از Mapped[] annotation سبک SQLAlchemy 2.0
================================================================
"""

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def _utcnow() -> datetime:
    """تابع کمکی — زمان فعلی UTC به‌صورت timezone-aware."""
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    """
    کلاس پایه برای تمام مدل‌های SQLAlchemy.
    سبک SQLAlchemy 2.0 (DeclarativeBase) — جایگزین declarative_base() قدیمی.

    قرارداد نامگذاری جدول‌ها (سند ۴.۵):
      هر مدل __tablename__ خود را به‌صراحت تعریف می‌کند (مثلاً "Users").
    """
    pass


class TimestampMixin:
    """
    Mixin برای افزودن دو ستون زمان‌بندی به مدل.

    استفاده:
        class User(Base, TimestampMixin):
            __tablename__ = "Users"
            ...

    رفتار:
      - created_at : زمان درج رکورد (INSERT)
      - updated_at : زمان آخرین تغییر — در هر UPDATE خودکار به‌روز می‌شود
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        onupdate=_utcnow,
        nullable=False,
    )


class SoftDeleteMixin:
    """
    Mixin برای پشتیبانی از حذف نرم (Soft Delete).

    استفاده:
        class User(Base, TimestampMixin, SoftDeleteMixin):
            __tablename__ = "Users"
            ...

    قرارداد سند ۵.۰:
      - هرگز رکورد به‌صورت فیزیکی حذف نشود
      - فقط is_deleted = True تنظیم شود
      - Repository ها در query پیش‌فرض رکوردهای حذف‌شده را نمی‌آورند
    """

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
