# -*- coding: utf-8 -*-
"""
SymbolRepository — Repository نماد
================================================================
این Repository ساده — فقط ارث از BaseRepository — برای دسترسی
به Symbol استفاده می‌شود. متدهای CRUD از Base می‌آیند:
  - get(id) / get_or_404(id)
  - list / count / exists
  - create / update / delete (soft)

در فازهای بعد متدهای اختصاصی اضافه خواهد شد (مثلاً
get_by_exchange_and_symbol).
================================================================
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.symbol import Symbol
from app.repositories.base import BaseRepository


class SymbolRepository(BaseRepository[Symbol]):
    """Repository نماد — متدهای CRUD از BaseRepository."""

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, Symbol)
