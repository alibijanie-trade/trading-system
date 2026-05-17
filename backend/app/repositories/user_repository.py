# -*- coding: utf-8 -*-
"""
UserRepository — Query های اختصاصی User
================================================================
متدهای CRUD از BaseRepository ارث می‌رسد + متدهای اختصاصی برای
احراز هویت.
================================================================
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository کاربر."""

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, User)

    async def get_by_username(self, username: str) -> User | None:
        """
        پیدا کردن کاربر فعال با username (soft-delete رعایت می‌شود).

        Returns:
            User یا None در صورت نبود
        """
        stmt = select(User).where(
            User.username == username,
            User.is_deleted.is_(False),
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
