# -*- coding: utf-8 -*-
"""
================================================================
اسکریپت ۱۰ — ۷ مدل پیچیده‌تر (Models Part 2)
================================================================
این اسکریپت ۷ مدل پایانی + بازنویسی `app/models/__init__.py`
را به ۱۵ مدل کامل می‌رساند.

مدل‌های این Part:
  1. OhlcvData ⭐  → سند ۵.۷    → جدول OhlcvData (+ ایندکس critical)
  2. Strategy     → سند ۵.۸    → جدول Strategies (با parent_id خود-ارجاع)
  3. Signal       → سند ۵.۹    → جدول Signals
  4. Trade        → سند ۵.۱۰   → جدول Trades
  5. Portfolio    → سند ۵.۱۱   → جدول Portfolio
  6. Alert        → سند ۵.۱۱   → جدول Alerts
  7. AuditLog ⭐  → سند ۵.۱۲   → جدول AuditLog (+ ۲ ایندکس)

نکات معماری مهم:
  - ایندکس critical: idx_ohlcv_symbol_tf_ts روی (symbol_id, timeframe, timestamp)
  - Strategy.parent_id با self-reference + remote_side
  - AuditLog با دو ایندکس DESC روی created_at
  - Signal/AuditLog فقط created_at دارند (immutable log records)
  - Portfolio با snapshot_at به‌جای created_at (تاکید بر معنا)
  - Trade دارای TimestampMixin + opened_at/closed_at مستقل

نحوه اجرا (در CMD 3):
    cd D:\\Projects\\trading-system
    python scripts\\10_models_part2.py
================================================================
"""

import sys
from pathlib import Path

try:
    from colorama import Fore, Style
    from colorama import init as _colorama_init

    _colorama_init(autoreset=True)
    GREEN, RED, YELLOW, CYAN, BOLD, RESET = (
        Fore.GREEN,
        Fore.RED,
        Fore.YELLOW,
        Fore.CYAN,
        Style.BRIGHT,
        Style.RESET_ALL,
    )
except ImportError:
    GREEN = RED = YELLOW = CYAN = BOLD = RESET = ""


# ============================================================
# مسیرها
# ============================================================
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
MODELS_DIR = BACKEND_DIR / "app" / "models"


# ============================================================
# محتوای فایل‌های مدل
# ============================================================

OHLCV_DATA_PY = '''# -*- coding: utf-8 -*-
"""
مدل OhlcvData — سند ۵.۷ ⭐
================================================================
داده‌های کندل (Open/High/Low/Close/Volume) برای یک نماد در یک
تایم‌فریم خاص. این بزرگ‌ترین جدول دیتابیس خواهد بود.

ستون‌ها (سند ۵.۷):
  id, symbol_id (FK→Symbols), timeframe, timestamp (UTC),
  open, high, low, close, volume, is_closed, created_at

ایندکس Critical (سند ۵.۷ — قطعی):
  idx_ohlcv_symbol_tf_ts روی (symbol_id, timeframe, timestamp)
  → برای جستجوی محدوده زمانی یک نماد در یک TF — الزامی

نکته‌ها:
  - timestamp = زمان شروع کندل (UTC)
  - is_closed = True یعنی کندل به پایان رسیده (نه candle جاری live)
  - بدون updated_at، بدون is_deleted (داده غیرقابل تغییر)
================================================================
"""

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class OhlcvData(Base):
    __tablename__ = "OhlcvData"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Symbols.id", ondelete="CASCADE"),
        nullable=False,
    )
    timeframe: Mapped[str] = mapped_column(String, nullable=False)  # 1m/5m/15m/1h/4h/1d/...
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
    )
    open: Mapped[float] = mapped_column(Float, nullable=False)
    high: Mapped[float] = mapped_column(Float, nullable=False)
    low: Mapped[float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[float] = mapped_column(Float, nullable=False)
    is_closed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        nullable=False,
    )

    symbol: Mapped["Symbol"] = relationship("Symbol", back_populates="ohlcv_data")

    __table_args__ = (
        # ⭐ ایندکس critical — الزامی طبق سند ۵.۷
        Index("idx_ohlcv_symbol_tf_ts", "symbol_id", "timeframe", "timestamp"),
    )

    def __repr__(self) -> str:
        return (
            f"<OhlcvData symbol_id={self.symbol_id} tf={self.timeframe!r} "
            f"ts={self.timestamp.isoformat()} close={self.close}>"
        )
'''


STRATEGY_PY = '''# -*- coding: utf-8 -*-
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
'''


SIGNAL_PY = '''# -*- coding: utf-8 -*-
"""
مدل Signal — سند ۵.۹
================================================================
سیگنال تولیدشده از یک استراتژی برای یک نماد.

ستون‌ها (سند ۵.۹):
  id, strategy_id (FK), symbol_id (FK), signal_type (buy/sell),
  strength (strong/medium/weak), timeframe, price_at_signal,
  suggested_entry, suggested_tp, suggested_sl, notes,
  is_executed, created_at

نکته: signals immutable هستند — بدون updated_at و is_deleted.
       اگر باطل شد، فقط is_executed=False باقی می‌ماند و سیگنال
       جدید ایجاد می‌شود.
================================================================
"""

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Signal(Base):
    __tablename__ = "Signals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    strategy_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Strategies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    symbol_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Symbols.id", ondelete="CASCADE"),
        nullable=False,
    )
    signal_type: Mapped[str] = mapped_column(String, nullable=False)  # buy/sell
    strength: Mapped[str] = mapped_column(String, nullable=False)     # strong/medium/weak
    timeframe: Mapped[str] = mapped_column(String, nullable=False)
    price_at_signal: Mapped[float] = mapped_column(Float, nullable=False)
    suggested_entry: Mapped[float | None] = mapped_column(Float, nullable=True)
    suggested_tp: Mapped[float | None] = mapped_column(Float, nullable=True)   # Take Profit
    suggested_sl: Mapped[float | None] = mapped_column(Float, nullable=True)   # Stop Loss
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_executed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        nullable=False,
    )

    # ===================================================
    # Relationships
    # ===================================================
    strategy: Mapped["Strategy"] = relationship("Strategy", back_populates="signals")
    symbol: Mapped["Symbol"] = relationship("Symbol", back_populates="signals")
    trades: Mapped[list["Trade"]] = relationship("Trade", back_populates="signal")

    def __repr__(self) -> str:
        return (
            f"<Signal id={self.id} {self.signal_type!r}/{self.strength!r} "
            f"strategy_id={self.strategy_id} symbol_id={self.symbol_id}>"
        )
'''


TRADE_PY = '''# -*- coding: utf-8 -*-
"""
مدل Trade — سند ۵.۱۰
================================================================
معامله واقعی یا paper trade کاربر.

ستون‌ها (سند ۵.۱۰):
  id, user_id (FK), strategy_id (FK, nullable), signal_id (FK, nullable),
  symbol_id (FK), exchange_id (FK), order_type, side, status,
  entry_price, exit_price, quantity, take_profit, stop_loss,
  pnl, pnl_percent, commission, is_paper, is_deleted,
  opened_at, closed_at

مقادیر مجاز:
  - order_type : market | limit | stop-limit
  - side       : buy | sell
  - status     : open | closed | cancelled

تصمیم پیاده‌سازی:
  - TimestampMixin اضافه شد (created_at/updated_at — audit trail رکورد)
  - opened_at/closed_at = زمان معاملاتی واقعی (متمایز از created_at)
  - SoftDeleteMixin برای is_deleted
================================================================
"""

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base, SoftDeleteMixin, TimestampMixin


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Trade(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "Trades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    strategy_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("Strategies.id", ondelete="SET NULL"),
        nullable=True,
    )
    signal_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("Signals.id", ondelete="SET NULL"),
        nullable=True,
    )
    symbol_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Symbols.id", ondelete="RESTRICT"),
        nullable=False,
    )
    exchange_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Exchanges.id", ondelete="RESTRICT"),
        nullable=False,
    )

    order_type: Mapped[str] = mapped_column(String, nullable=False)  # market/limit/stop-limit
    side: Mapped[str] = mapped_column(String, nullable=False)        # buy/sell
    status: Mapped[str] = mapped_column(
        String, default="open", nullable=False,
    )  # open/closed/cancelled

    entry_price: Mapped[float] = mapped_column(Float, nullable=False)
    exit_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    take_profit: Mapped[float | None] = mapped_column(Float, nullable=True)
    stop_loss: Mapped[float | None] = mapped_column(Float, nullable=True)
    pnl: Mapped[float | None] = mapped_column(Float, nullable=True)
    pnl_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    commission: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_paper: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    opened_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        nullable=False,
    )
    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
    )

    # ===================================================
    # Relationships
    # ===================================================
    user: Mapped["User"] = relationship("User", back_populates="trades")
    strategy: Mapped["Strategy | None"] = relationship(
        "Strategy", back_populates="trades",
    )
    signal: Mapped["Signal | None"] = relationship(
        "Signal", back_populates="trades",
    )
    symbol: Mapped["Symbol"] = relationship("Symbol", back_populates="trades")
    exchange: Mapped["Exchange"] = relationship("Exchange", back_populates="trades")

    def __repr__(self) -> str:
        return (
            f"<Trade id={self.id} {self.side!r} {self.status!r} "
            f"qty={self.quantity} entry={self.entry_price} pnl={self.pnl}>"
        )
'''


PORTFOLIO_PY = '''# -*- coding: utf-8 -*-
"""
مدل Portfolio — سند ۵.۱۱
================================================================
Snapshot موجودی کاربر در یک صرافی برای یک دارایی، در زمان معین.
هر رکورد یک snapshot تاریخی است (نه وضعیت زنده).

ستون‌ها (سند ۵.۱۱):
  user_id (FK), exchange_id (FK), asset, balance_total,
  balance_free, balance_locked, snapshot_at

نکته: Portfolio به‌صورت time-series است:
  - یک snapshot روزانه/ساعتی برای هر (user, exchange, asset)
  - تاریخچه نگه‌داشته می‌شود برای نمودار equity
================================================================
"""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Portfolio(Base):
    __tablename__ = "Portfolio"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    exchange_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Exchanges.id", ondelete="CASCADE"),
        nullable=False,
    )
    asset: Mapped[str] = mapped_column(String, nullable=False)  # BTC, USDT, ...
    balance_total: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    balance_free: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    balance_locked: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    snapshot_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="portfolio")
    exchange: Mapped["Exchange"] = relationship("Exchange", back_populates="portfolio")

    def __repr__(self) -> str:
        return (
            f"<Portfolio user_id={self.user_id} {self.asset!r} "
            f"total={self.balance_total} at={self.snapshot_at.isoformat()}>"
        )
'''


ALERT_PY = '''# -*- coding: utf-8 -*-
"""
مدل Alert — سند ۵.۱۱
================================================================
هشدار قابل تنظیم برای یک نماد (مثلاً قیمت بالاتر از X).

ستون‌ها (سند ۵.۱۱):
  user_id (FK), symbol_id (FK), alert_type, condition (JSON),
  is_triggered, triggered_at, is_active

نمونه condition (JSON):
  {"operator": ">", "value": 70000}              ← price_above
  {"indicator": "RSI", "operator": "<", "value": 30}  ← oversold
================================================================
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base, TimestampMixin


class Alert(Base, TimestampMixin):
    __tablename__ = "Alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    symbol_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Symbols.id", ondelete="CASCADE"),
        nullable=False,
    )
    alert_type: Mapped[str] = mapped_column(String, nullable=False)  # price_above, indicator_cross, ...
    condition: Mapped[str] = mapped_column(Text, nullable=False)     # JSON
    is_triggered: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    triggered_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="alerts")
    symbol: Mapped["Symbol"] = relationship("Symbol", back_populates="alerts")

    def __repr__(self) -> str:
        return (
            f"<Alert id={self.id} type={self.alert_type!r} "
            f"triggered={self.is_triggered} active={self.is_active}>"
        )
'''


AUDIT_LOG_PY = '''# -*- coding: utf-8 -*-
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

from sqlalchemy import (
    DateTime, ForeignKey, Index, Integer, String, Text, text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base


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
'''


# ============================================================
# __init__.py به‌روزشده — ۱۵ مدل کامل
# ============================================================

INIT_PY = '''# -*- coding: utf-8 -*-
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

# Part 1 — 8 مدل
from app.models.user import User
from app.models.user_session import UserSession
from app.models.exchange import Exchange
from app.models.exchange_api_key import ExchangeAPIKey
from app.models.symbol import Symbol
from app.models.watchlist import Watchlist
from app.models.risk_settings import RiskSettings
from app.models.app_settings import AppSettings

# Part 2 — 7 مدل
from app.models.ohlcv_data import OhlcvData
from app.models.strategy import Strategy
from app.models.signal import Signal
from app.models.trade import Trade
from app.models.portfolio import Portfolio
from app.models.alert import Alert
from app.models.audit_log import AuditLog

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
'''


# ============================================================
# توابع کمکی
# ============================================================


def info(msg: str) -> None:
    print(f"{CYAN}ℹ {msg}{RESET}")


def success(msg: str) -> None:
    print(f"{GREEN}✅ {msg}{RESET}")


def warn(msg: str) -> None:
    print(f"{YELLOW}⚠ {msg}{RESET}")


def err(msg: str) -> None:
    print(f"{RED}❌ {msg}{RESET}")


def header(msg: str) -> None:
    line = "=" * 60
    print(f"\n{BOLD}{CYAN}{line}{RESET}")
    print(f"{BOLD}{CYAN}{msg}{RESET}")
    print(f"{BOLD}{CYAN}{line}{RESET}\n")


def write_file(path: Path, content: str) -> str:
    """نوشتن idempotent. خروجی: 'created' | 'updated' | 'unchanged'"""
    path.parent.mkdir(parents=True, exist_ok=True)
    rel = path.relative_to(PROJECT_ROOT)

    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing == content:
            info(f"بدون تغییر:  {rel}")
            return "unchanged"
        path.write_text(content, encoding="utf-8")
        warn(f"بازنویسی:    {rel}")
        return "updated"

    path.write_text(content, encoding="utf-8")
    success(f"ساخت جدید:   {rel}")
    return "created"


# ============================================================
# main
# ============================================================
def main() -> int:
    header("اسکریپت ۱۰ — ۷ مدل پیچیده (Models Part 2)")

    info(f"ریشه پروژه : {PROJECT_ROOT}")
    info(f"پوشه مدل‌ها: {MODELS_DIR}")

    # بررسی پیش‌نیاز — اسکریپت ۰۹ باید قبلاً اجرا شده باشد
    user_py = MODELS_DIR / "user.py"
    if not user_py.exists():
        err("مدل‌های Part 1 ساخته نشده‌اند.")
        err("ابتدا اسکریپت ۰۹ را اجرا کنید.")
        return 1

    success("پیش‌نیازها OK (اسکریپت ۰۹ قبلاً اجرا شده)")
    print()
    info("شروع ساخت مدل‌های Part 2...\n")

    files = [
        ("ohlcv_data.py", OHLCV_DATA_PY),
        ("strategy.py", STRATEGY_PY),
        ("signal.py", SIGNAL_PY),
        ("trade.py", TRADE_PY),
        ("portfolio.py", PORTFOLIO_PY),
        ("alert.py", ALERT_PY),
        ("audit_log.py", AUDIT_LOG_PY),
        ("__init__.py", INIT_PY),
    ]

    results = {}
    for filename, content in files:
        results[filename] = write_file(MODELS_DIR / filename, content)

    # خلاصه
    header("خلاصه")
    created = sum(1 for v in results.values() if v == "created")
    updated = sum(1 for v in results.values() if v == "updated")
    unchanged = sum(1 for v in results.values() if v == "unchanged")
    print(f"  {GREEN}ساخت جدید :{RESET} {created}")
    print(f"  {YELLOW}بازنویسی  :{RESET} {updated}")
    print(f"  {CYAN}بدون تغییر:{RESET} {unchanged}")
    print()

    info("گام بعدی — دو تست در CMD 1 (با venv فعال):")
    print()
    print(f"  {BOLD}# تست ۱ — ایمپورت همه ۱۵ مدل:{RESET}")
    print(
        f"  {BOLD}python -c \"from app.models import User, UserSession, Exchange, ExchangeAPIKey, Symbol, Watchlist, RiskSettings, AppSettings, OhlcvData, Strategy, Signal, Trade, Portfolio, Alert, AuditLog; print('OK - 15 models imported')\"{RESET}"
    )
    print()
    print(f"  {BOLD}# تست ۲ — اعتبارسنجی relationship ها (configure_mappers):{RESET}")
    print(
        f"  {BOLD}python -c \"from app.models import User; from sqlalchemy.orm import configure_mappers; configure_mappers(); print('OK - all relationships valid')\"{RESET}"
    )
    print()
    info("اگر هر دو تست OK دادند، گام بعدی (اسکریپت ۱۱ - BaseRepository) آغاز می‌شود.")
    print()
    warn("⚠ هنوز هیچ جدولی در DB ساخته نشده — این مرحله فقط تعریف ORM است.")
    warn("  جدول‌ها در زیرگام ۴.۲ با Alembic ساخته می‌شوند.")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
