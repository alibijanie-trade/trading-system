# -*- coding: utf-8 -*-
"""
Repositories — export سطح بالا
================================================================
استفاده پایه:
    from app.repositories import (
        BaseRepository,
        OhlcvRepository,
        SymbolRepository,
        UserRepository,
        UserSessionRepository,
    )

قانون قفل‌شده (سند ۳.۳):
  - هرگز Query مستقیم خارج از repositories/
  - service ها از Repository استفاده می‌کنند، نه از session مستقیم
================================================================
"""

from app.repositories.base import BaseRepository
from app.repositories.ohlcv_repository import OhlcvRepository
from app.repositories.symbol_repository import SymbolRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository

__all__ = [
    "BaseRepository",
    "OhlcvRepository",
    "SymbolRepository",
    "UserRepository",
    "UserSessionRepository",
]
