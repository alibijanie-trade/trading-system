# -*- coding: utf-8 -*-
"""
UserSessionRepository — Repository نشست‌های احراز هویت
================================================================
هر رکورد UserSession یک refresh token را نگه می‌دارد.
- login : ایجاد رکورد جدید
- logout: is_revoked=True
- refresh: فقط چک معتبر بودن (revoke نمی‌کنیم)

نکته: UserSession ستون is_deleted ندارد — BaseRepository این را
خودش از طریق hasattr تشخیص می‌دهد و filter سافت-دیلیت اعمال نمی‌شود.
================================================================
"""

from app.models.user_session import UserSession
from app.repositories.base import BaseRepository
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserSessionRepository(BaseRepository[UserSession]):
    """Repository نشست‌های کاربر (refresh token)."""

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, UserSession)

    async def get_by_token(self, token: str) -> UserSession | None:
        """پیدا کردن نشست با مقدار token."""
        stmt = select(UserSession).where(UserSession.token == token)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
