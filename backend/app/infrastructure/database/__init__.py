# -*- coding: utf-8 -*-
"""
Database Infrastructure — export سطح بالا
================================================================
این پکیج زیرساخت دیتابیس را در اختیار سایر لایه‌ها می‌گذارد.

استفاده:
    from app.infrastructure.database import Base, engine, get_db
    from app.infrastructure.database import TimestampMixin, SoftDeleteMixin
================================================================
"""

from app.infrastructure.database.base import (
    Base,
    SoftDeleteMixin,
    TimestampMixin,
)
from app.infrastructure.database.engine import dispose_engine, engine
from app.infrastructure.database.session import AsyncSessionLocal, get_db

__all__ = [
    # Base + Mixins
    "Base",
    "TimestampMixin",
    "SoftDeleteMixin",
    # Engine
    "engine",
    "dispose_engine",
    # Session
    "AsyncSessionLocal",
    "get_db",
]
