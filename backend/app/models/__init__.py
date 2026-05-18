# -*- coding: utf-8 -*-
"""
SQLAlchemy Models — export سطح بالا
================================================================
این پکیج تمام ۱۵ مدل ORM پروژه را export می‌کند.

نکته مهم برای Alembic:
  Alembic برای autogenerate نیاز دارد همه مدل‌ها در این پکیج
  ایمپورت شده باشند تا Base.metadata را کشف کند.

وضعیت کامل:
  ✅ Part 1 — 8 مدل (User, UserSession, Exchange, ExchangeAPIKey,
                     Symbol, Watchlist, RiskSettings, AppSettings)
  ✅ Part 2 — 7 مدل (OhlcvData, Strategy, Signal, Trade,
                     Portfolio, Alert, AuditLog)
================================================================
"""

from app.models.alert import Alert
from app.models.app_settings import AppSettings
from app.models.audit_log import AuditLog
from app.models.exchange import Exchange
from app.models.exchange_api_key import ExchangeAPIKey

# Part 2 — 7 مدل
from app.models.ohlcv_data import OhlcvData
from app.models.portfolio import Portfolio
from app.models.risk_settings import RiskSettings
from app.models.signal import Signal
from app.models.strategy import Strategy
from app.models.symbol import Symbol
from app.models.trade import Trade

# Part 1 — 8 مدل
from app.models.user import User
from app.models.user_session import UserSession
from app.models.watchlist import Watchlist

__all__ = [
    # Part 1
    "User",
    "UserSession",
    "Exchange",
    "ExchangeAPIKey",
    "Symbol",
    "Watchlist",
    "RiskSettings",
    "AppSettings",
    # Part 2
    "OhlcvData",
    "Strategy",
    "Signal",
    "Trade",
    "Portfolio",
    "Alert",
    "AuditLog",
]
