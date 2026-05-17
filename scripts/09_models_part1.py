# -*- coding: utf-8 -*-
"""
================================================================
اسکریپت ۰۹ — ۸ مدل ساده (Models Part 1)
================================================================
این اسکریپت ۸ مدل اول SQLAlchemy را در `backend/app/models/`
می‌سازد به همراه به‌روزرسانی `app/models/__init__.py`.

مدل‌های این Part (طبق سند ۵.۱ تا ۵.۶ و ۵.۱۱):
  1. User             → سند ۵.۱   → جدول Users
  2. UserSession 💡   → سند ۵.۲   → جدول Sessions  (نام کلاس Python: UserSession)
  3. Exchange         → سند ۵.۳   → جدول Exchanges
  4. ExchangeAPIKey   → سند ۵.۴   → جدول ExchangeAPIKeys
  5. Symbol           → سند ۵.۵   → جدول Symbols (+ ایندکس composite)
  6. Watchlist        → سند ۵.۶   → جدول Watchlist
  7. RiskSettings     → سند ۵.۱۱  → جدول RiskSettings (یک‌به‌یک با User)
  8. AppSettings      → سند ۵.۱۱  → جدول AppSettings (یک‌به‌یک با User)

نکات معماری:
  - تمام relationship ها با string forward refs (به‌جای import واقعی)
    تا با مدل‌های part2 (که هنوز ساخته نشده‌اند) سازگار باشد.
  - relationship های مربوط به part2 (Strategy/Trade/...) به‌صورت
    string-only تعریف می‌شوند و در زمان configure_mappers (part2)
    resolve می‌شوند.
  - timezone-aware datetime با UTC + default = datetime.now(timezone.utc)
  - PascalCase برای نام جداول (سند ۴.۵) - مثلاً "Users", "OhlcvData"

نحوه اجرا (در CMD 3):
    cd D:\\Projects\\trading-system
    python scripts\\09_models_part1.py
================================================================
"""

import sys
from pathlib import Path

try:
    from colorama import init as _colorama_init
    from colorama import Fore, Style
    _colorama_init(autoreset=True)
    GREEN, RED, YELLOW, CYAN, BOLD, RESET = (
        Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.CYAN, Style.BRIGHT, Style.RESET_ALL,
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

USER_PY = '''# -*- coding: utf-8 -*-
"""
مدل User — سند ۵.۱
================================================================
کاربر سیستم. هر کاربر یک یا چند Session، چندین API Key صرافی،
Watchlist، Strategy، Trade، و تنظیمات شخصی دارد.

ستون‌ها (سند ۵.۱):
  id, username (UNIQUE), password_hash, role, is_active,
  last_login, is_deleted, created_at, updated_at

نقش‌ها (role): admin | trader | viewer

رمز عبور:
  - password_hash با bcrypt در service layer ساخته می‌شود
  - هرگز plaintext ذخیره نشود
================================================================
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base, SoftDeleteMixin, TimestampMixin


class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True,
    )
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)  # admin/trader/viewer
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
    )

    # ===================================================
    # Relationships — Part 1 (مدل‌های ساخته‌شده در همین اسکریپت)
    # ===================================================
    sessions: Mapped[list["UserSession"]] = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    api_keys: Mapped[list["ExchangeAPIKey"]] = relationship(
        "ExchangeAPIKey",
        back_populates="user",
    )
    watchlist: Mapped[list["Watchlist"]] = relationship(
        "Watchlist",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    risk_settings: Mapped["RiskSettings | None"] = relationship(
        "RiskSettings",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    app_settings: Mapped["AppSettings | None"] = relationship(
        "AppSettings",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # ===================================================
    # Relationships — Part 2 (مدل‌های اسکریپت بعدی)
    # تا configure_mappers صدا زده نشود، string-form OK است.
    # ===================================================
    strategies: Mapped[list["Strategy"]] = relationship(
        "Strategy",
        back_populates="user",
    )
    trades: Mapped[list["Trade"]] = relationship(
        "Trade",
        back_populates="user",
    )
    portfolio: Mapped[list["Portfolio"]] = relationship(
        "Portfolio",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    alerts: Mapped[list["Alert"]] = relationship(
        "Alert",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(
        "AuditLog",
        back_populates="user",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r} role={self.role!r}>"
'''


USER_SESSION_PY = '''# -*- coding: utf-8 -*-
"""
مدل UserSession — سند ۵.۲
================================================================
Session احراز هویت کاربر (JWT token + متادیتای ورود).
نام جدول طبق سند ۵.۲ → "Sessions"
نام کلاس Python → `UserSession` (برای جلوگیری از تداخل با
sqlalchemy.orm.Session)

ستون‌ها (سند ۵.۲):
  id, user_id (FK→Users), token (UNIQUE), ip_address,
  expires_at, is_revoked, created_at

نکته: UserSession مشمول soft delete نیست — هنگام logout/expire
رکوردهای فیزیکی حذف می‌شوند یا is_revoked=True می‌گیرند.
================================================================
"""

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class UserSession(Base):
    __tablename__ = "Sessions"  # نام جدول طبق سند ۵.۲

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True,
    )
    ip_address: Mapped[str | None] = mapped_column(String, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
    )
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="sessions")

    def __repr__(self) -> str:
        return f"<UserSession id={self.id} user_id={self.user_id} revoked={self.is_revoked}>"
'''


EXCHANGE_PY = '''# -*- coding: utf-8 -*-
"""
مدل Exchange — سند ۵.۳
================================================================
صرافی — مثلاً Binance، Kraken، Bybit.
ccxt_id برای پیوست با کتابخانه ccxt در فاز ۱.

ستون‌ها (سند ۵.۳):
  id, name (UNIQUE), ccxt_id, is_active, supports_futures,
  is_deleted, created_at, updated_at
================================================================
"""

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base, SoftDeleteMixin, TimestampMixin


class Exchange(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "Exchanges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True,
    )
    ccxt_id: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    supports_futures: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False,
    )

    # ===================================================
    # Relationships
    # ===================================================
    api_keys: Mapped[list["ExchangeAPIKey"]] = relationship(
        "ExchangeAPIKey",
        back_populates="exchange",
    )
    symbols: Mapped[list["Symbol"]] = relationship(
        "Symbol",
        back_populates="exchange",
    )
    # Part 2
    trades: Mapped[list["Trade"]] = relationship(
        "Trade",
        back_populates="exchange",
    )
    portfolio: Mapped[list["Portfolio"]] = relationship(
        "Portfolio",
        back_populates="exchange",
    )

    def __repr__(self) -> str:
        return f"<Exchange id={self.id} name={self.name!r} ccxt_id={self.ccxt_id!r}>"
'''


EXCHANGE_API_KEY_PY = '''# -*- coding: utf-8 -*-
"""
مدل ExchangeAPIKey — سند ۵.۴
================================================================
کلید API صرافی متعلق به یک کاربر.
🔒 api_key_encrypted و secret_key_encrypted با Fernet رمزنگاری می‌شوند
   (در service layer، با ENCRYPTION_KEY از .env). هرگز plaintext.

ستون‌ها (سند ۵.۴):
  id, user_id (FK→Users), exchange_id (FK→Exchanges),
  label, api_key_encrypted, secret_key_encrypted, permissions(JSON),
  is_active, is_deleted, created_at, updated_at
================================================================
"""

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base, SoftDeleteMixin, TimestampMixin


class ExchangeAPIKey(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "ExchangeAPIKeys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    exchange_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Exchanges.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    label: Mapped[str | None] = mapped_column(String, nullable=True)
    api_key_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    secret_key_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    permissions: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON: ["read","trade"]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # ===================================================
    # Relationships
    # ===================================================
    user: Mapped["User"] = relationship("User", back_populates="api_keys")
    exchange: Mapped["Exchange"] = relationship("Exchange", back_populates="api_keys")

    def __repr__(self) -> str:
        return (
            f"<ExchangeAPIKey id={self.id} user_id={self.user_id} "
            f"exchange_id={self.exchange_id} label={self.label!r}>"
        )
'''


SYMBOL_PY = '''# -*- coding: utf-8 -*-
"""
مدل Symbol — سند ۵.۵
================================================================
نماد معاملاتی — مثلاً BTC/USDT در Binance spot.

ستون‌ها (سند ۵.۵):
  id, exchange_id (FK→Exchanges), symbol, base_asset, quote_asset,
  market_type (spot/futures), is_active, is_deleted

ایندکس Composite (سند ۵.۵):
  idx_symbols_exchange_symbol روی (exchange_id, symbol)

نکته: TimestampMixin اضافه شد طبق سند ۵.۰ (created_at/updated_at
       در همه جداول اصلی).
================================================================
"""

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base, SoftDeleteMixin, TimestampMixin


class Symbol(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "Symbols"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exchange_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Exchanges.id", ondelete="CASCADE"),
        nullable=False,
    )
    symbol: Mapped[str] = mapped_column(String, nullable=False)        # BTC/USDT
    base_asset: Mapped[str] = mapped_column(String, nullable=False)    # BTC
    quote_asset: Mapped[str] = mapped_column(String, nullable=False)   # USDT
    market_type: Mapped[str] = mapped_column(String, nullable=False)   # spot/futures
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # ===================================================
    # Relationships
    # ===================================================
    exchange: Mapped["Exchange"] = relationship("Exchange", back_populates="symbols")
    watchlist_entries: Mapped[list["Watchlist"]] = relationship(
        "Watchlist",
        back_populates="symbol",
    )
    # Part 2
    ohlcv_data: Mapped[list["OhlcvData"]] = relationship(
        "OhlcvData",
        back_populates="symbol",
    )
    signals: Mapped[list["Signal"]] = relationship(
        "Signal",
        back_populates="symbol",
    )
    trades: Mapped[list["Trade"]] = relationship(
        "Trade",
        back_populates="symbol",
    )
    alerts: Mapped[list["Alert"]] = relationship(
        "Alert",
        back_populates="symbol",
    )

    # ===================================================
    # Indexes
    # ===================================================
    __table_args__ = (
        Index("idx_symbols_exchange_symbol", "exchange_id", "symbol"),
    )

    def __repr__(self) -> str:
        return (
            f"<Symbol id={self.id} symbol={self.symbol!r} "
            f"exchange_id={self.exchange_id} market={self.market_type!r}>"
        )
'''


WATCHLIST_PY = '''# -*- coding: utf-8 -*-
"""
مدل Watchlist — سند ۵.۶
================================================================
لیست نمادهای مورد علاقه کاربر با ترتیب نمایش.

ستون‌ها (سند ۵.۶):
  id, user_id (FK→Users), symbol_id (FK→Symbols),
  sort_order, created_at

نکته: Watchlist مشمول soft delete نیست — حذف می‌شود به‌صورت
       فیزیکی (cascade از User).
================================================================
"""

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Watchlist(Base):
    __tablename__ = "Watchlist"

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
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=_utcnow,
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="watchlist")
    symbol: Mapped["Symbol"] = relationship("Symbol", back_populates="watchlist_entries")

    def __repr__(self) -> str:
        return f"<Watchlist id={self.id} user_id={self.user_id} symbol_id={self.symbol_id}>"
'''


RISK_SETTINGS_PY = '''# -*- coding: utf-8 -*-
"""
مدل RiskSettings — سند ۵.۱۱
================================================================
تنظیمات ریسک شخصی کاربر — رابطه یک‌به‌یک با User.

ستون‌ها (سند ۵.۱۱):
  user_id, max_risk_per_trade, max_daily_drawdown,
  max_open_trades, default_rr_ratio, auto_stop_on_loss

مقادیر پیش‌فرض (بهترین‌رویه‌های ترید):
  - max_risk_per_trade = 0.02   (2% سرمایه در هر معامله)
  - max_daily_drawdown = 0.05   (5% افت روزانه ماکزیمم)
  - max_open_trades    = 5
  - default_rr_ratio   = 2.0    (Risk/Reward ratio)
  - auto_stop_on_loss  = True

یک‌به‌یک بودن: user_id با UNIQUE تضمین می‌شود.
================================================================
"""

from sqlalchemy import Boolean, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base, TimestampMixin


class RiskSettings(Base, TimestampMixin):
    __tablename__ = "RiskSettings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # یک‌به‌یک
    )
    max_risk_per_trade: Mapped[float] = mapped_column(
        Float, default=0.02, nullable=False,
    )
    max_daily_drawdown: Mapped[float] = mapped_column(
        Float, default=0.05, nullable=False,
    )
    max_open_trades: Mapped[int] = mapped_column(
        Integer, default=5, nullable=False,
    )
    default_rr_ratio: Mapped[float] = mapped_column(
        Float, default=2.0, nullable=False,
    )
    auto_stop_on_loss: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="risk_settings")

    def __repr__(self) -> str:
        return f"<RiskSettings user_id={self.user_id} max_risk={self.max_risk_per_trade}>"
'''


APP_SETTINGS_PY = '''# -*- coding: utf-8 -*-
"""
مدل AppSettings — سند ۵.۱۱
================================================================
تنظیمات شخصی UI و سیستم — رابطه یک‌به‌یک با User.

ستون‌ها (سند ۵.۱۱):
  user_id, theme, calendar_type, font_size, default_timeframe,
  active_exchanges (JSON), telegram_chat_id

پیش‌فرض‌ها (طبق Session 2 - تصمیم #12):
  - theme = "light"
  - calendar_type = "gregorian"  (تصمیم #12: تقویم پیش‌فرض میلادی)
  - font_size = 14
  - default_timeframe = "1h"
================================================================
"""

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base, TimestampMixin


class AppSettings(Base, TimestampMixin):
    __tablename__ = "AppSettings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # یک‌به‌یک
    )
    theme: Mapped[str] = mapped_column(String, default="light", nullable=False)
    calendar_type: Mapped[str] = mapped_column(
        String, default="gregorian", nullable=False,
    )
    font_size: Mapped[int] = mapped_column(Integer, default=14, nullable=False)
    default_timeframe: Mapped[str] = mapped_column(
        String, default="1h", nullable=False,
    )
    active_exchanges: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON list
    telegram_chat_id: Mapped[str | None] = mapped_column(String, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="app_settings")

    def __repr__(self) -> str:
        return f"<AppSettings user_id={self.user_id} theme={self.theme!r}>"
'''


# ============================================================
# __init__.py پکیج models
# ============================================================

INIT_PY = '''# -*- coding: utf-8 -*-
"""
SQLAlchemy Models — export سطح بالا
================================================================
این پکیج تمام مدل‌های ORM پروژه را export می‌کند.

نکته مهم برای Alembic:
  Alembic برای autogenerate نیاز دارد همه مدل‌ها در این پکیج
  ایمپورت شده باشند تا Base.metadata را کشف کند.

وضعیت فعلی:
  ✅ Part 1 — 8 مدل (User, UserSession, Exchange, ExchangeAPIKey,
                     Symbol, Watchlist, RiskSettings, AppSettings)
  ⏳ Part 2 — 7 مدل (OhlcvData, Strategy, Signal, Trade,
                     Portfolio, Alert, AuditLog) — اسکریپت ۱۰
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

# Part 2 — به‌زودی در اسکریپت ۱۰ اضافه می‌شود

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
    header("اسکریپت ۰۹ — ۸ مدل ساده (Models Part 1)")

    info(f"ریشه پروژه : {PROJECT_ROOT}")
    info(f"پوشه مدل‌ها: {MODELS_DIR}")

    # بررسی پیش‌نیازها
    if not BACKEND_DIR.exists():
        err(f"پوشه backend پیدا نشد: {BACKEND_DIR}")
        return 1

    db_init = BACKEND_DIR / "app" / "infrastructure" / "database" / "__init__.py"
    if not db_init.exists():
        err("زیرساخت دیتابیس آماده نیست.")
        err("ابتدا اسکریپت ۰۸ را اجرا کنید.")
        return 1

    success("پیش‌نیازها OK (اسکریپت ۰۸ قبلاً اجرا شده)")
    print()

    info("شروع ساخت مدل‌ها...\n")

    files = [
        ("user.py",             USER_PY),
        ("user_session.py",     USER_SESSION_PY),
        ("exchange.py",         EXCHANGE_PY),
        ("exchange_api_key.py", EXCHANGE_API_KEY_PY),
        ("symbol.py",           SYMBOL_PY),
        ("watchlist.py",        WATCHLIST_PY),
        ("risk_settings.py",    RISK_SETTINGS_PY),
        ("app_settings.py",     APP_SETTINGS_PY),
        ("__init__.py",         INIT_PY),
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

    info("گام بعدی — تست ایمپورت در CMD 1 (با venv فعال):")
    print()
    print(f"  {BOLD}python -c \"from app.models import User, UserSession, Exchange, ExchangeAPIKey, Symbol, Watchlist, RiskSettings, AppSettings; print('OK - 8 models imported')\"{RESET}")
    print()
    info("اگر پیام «OK - 8 models imported» دیدید، گام بعدی (۷ مدل Part 2) آغاز می‌شود.")
    print()
    warn("⚠ تا اسکریپت ۱۰ (Part 2) و اسکریپت ۱۱ (Repository) و سپس")
    warn("  زیرگام ۴.۲ (Alembic migration) اجرا نشده، هنوز جدولی در DB ساخته نشده است.")
    warn("  این کاملاً طبیعی است — این مرحله فقط تعریف مدل‌ها است.")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
