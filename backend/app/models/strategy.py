# -*- coding: utf-8 -*-
"""
مدل Strategy — سند ۵.۸
================================================================
استراتژی معاملاتی کاربر — شامل شرایط ورود/خروج/ریسک به فرم JSON.
از Versioning ساده پشتیبانی می‌کند با parent_id (خود-ارجاع).

ستون‌ها (سند ۵.۸):
  id, user_id (FK→Users), name, description, version,
  parent_id (FK→Strategies — self), entry_conditions (JSON),
  exit_conditions (JSON), risk_settings (JSON), timeframes (JSON),
  is_active, is_deleted

نکته Versioning:
  هر ویرایش استراتژی، رکورد جدید می‌سازد با parent_id = id قبلی
  و version+=1. این تاریخچه را حفظ می‌کند بدون از دست دادن داده.

نکته JSON:
  در این پروژه JSON ها به‌صورت Text (string) ذخیره می‌شوند و
  serialize/deserialize در service layer انجام می‌شود — کنترل
  بیشتر، debugging راحت‌تر.
================================================================
"""

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base, SoftDeleteMixin, TimestampMixin


class Strategy(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "Strategies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("Strategies.id", ondelete="SET NULL"),
        nullable=True,
    )
    entry_conditions: Mapped[str] = mapped_column(Text, nullable=False)   # JSON
    exit_conditions: Mapped[str] = mapped_column(Text, nullable=False)    # JSON
    risk_settings: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON
    timeframes: Mapped[str] = mapped_column(Text, nullable=False)         # JSON list
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # ===================================================
    # Relationships
    # ===================================================
    user: Mapped["User"] = relationship("User", back_populates="strategies")

    # self-reference برای Versioning
    parent: Mapped["Strategy | None"] = relationship(
        "Strategy",
        remote_side="Strategy.id",
        back_populates="children",
    )
    children: Mapped[list["Strategy"]] = relationship(
        "Strategy",
        back_populates="parent",
    )

    signals: Mapped[list["Signal"]] = relationship(
        "Signal",
        back_populates="strategy",
    )
    trades: Mapped[list["Trade"]] = relationship(
        "Trade",
        back_populates="strategy",
    )

    def __repr__(self) -> str:
        return (
            f"<Strategy id={self.id} name={self.name!r} v{self.version} "
            f"user_id={self.user_id}>"
        )
