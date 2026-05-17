# -*- coding: utf-8 -*-
"""
Session Maker + Dependency Injection برای FastAPI
================================================================
این فایل دو چیز را تعریف می‌کند:
  1. AsyncSessionLocal → کارخانه ساخت AsyncSession
  2. get_db()          → Dependency برای injection در API routes

نحوه استفاده در API route ها:

    from fastapi import Depends
    from sqlalchemy.ext.asyncio import AsyncSession
    from app.infrastructure.database import get_db

    @router.get("/users/{user_id}")
    async def get_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
    ):
        ...

قانون قفل‌شده (سند ۳.۳):
  - هیچ Query مستقیمی در api/ یا services/ نباشد
  - Query فقط در repositories/ — با دریافت session از get_db
================================================================
"""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.logging import get_logger
from app.infrastructure.database.engine import engine

logger = get_logger(__name__)


# ============================================================
# Session Factory
# ============================================================
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # رکوردها پس از commit قابل خواندن می‌مانند
    autoflush=False,
    autocommit=False,
)


# ============================================================
# Dependency: get_db
# ============================================================
async def get_db() -> AsyncIterator[AsyncSession]:
    """
    Dependency Injection برای دریافت یک AsyncSession در route ها.

    رفتار:
      - یک session جدید ساخته می‌شود
      - در صورت بروز هر Exception، rollback خودکار انجام می‌شود
      - در پایان (چه موفق چه ناموفق)، session بسته می‌شود (async with)
      - commit مسئولیت لایه service است (نه این تابع)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            logger.exception("خطا در session — rollback انجام شد")
            raise
