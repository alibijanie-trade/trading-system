# -*- coding: utf-8 -*-
"""
================================================================
اسکریپت ۱۴ — Seed Data (پایان زیرگام ۴.۲)
================================================================
این اسکریپت داده‌های اولیه پروژه را در trading.db درج می‌کند:

  1. Exchange مجازی → name="Excel", ccxt_id="excel"
     (برای استفاده در فاز ۶ — Excel Reader، طبق گزینه «ب» تأییدشده)

  2. کاربر admin → username="admin", password="1" (bcrypt-hashed)
     طبق تصمیم #11 Session 2

  3. RiskSettings پیش‌فرض برای admin (سند ۵.۱۱)
  4. AppSettings پیش‌فرض برای admin (سند ۵.۱۱)

ویژگی‌ها:
  - idempotent — اجرای دوم چیزی duplicate نمی‌کند
  - async — با AsyncSession (همان pattern کد production)
  - استفاده از BaseRepository (تست عملی repository که در ۴.۱ ساختیم)
  - bcrypt برای hash پسورد (طبق سند ۹.۱)

نحوه اجرا (در CMD 3):
    cd /d D:\\Projects\\trading-system
    backend\\venv\\Scripts\\activate
    python scripts\\14_seed_data.py

⚠ این اسکریپت برخلاف بقیه، در venv اجرا می‌شود (نه CMD3 پایه)
   چون نیاز به ایمپورت‌های backend دارد.
================================================================
"""

import asyncio
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
# تنظیم مسیر برای ایمپورت backend
# ============================================================
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


# ============================================================
# توابع کمکی نمایش
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


# ============================================================
# پسورد hashing با bcrypt (طبق سند ۹.۱)
# ============================================================
def hash_password(password: str) -> str:
    """هش پسورد با bcrypt."""
    import bcrypt

    salt = bcrypt.gensalt(rounds=12)  # rounds=12 توصیه‌شده برای امنیت/سرعت
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


# ============================================================
# توابع seed
# ============================================================
async def seed_exchange(session) -> int:
    """درج Exchange مجازی 'Excel'. خروجی: id رکورد (موجود یا تازه)."""
    from app.models import Exchange
    from sqlalchemy import select

    # چک کن از قبل وجود ندارد
    stmt = select(Exchange).where(Exchange.name == "Excel")
    result = await session.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing is not None:
        info(f"Exchange 'Excel' از قبل موجود است (id={existing.id})")
        return existing.id

    # ساخت جدید
    excel = Exchange(
        name="Excel",
        ccxt_id="excel",
        is_active=True,
        supports_futures=False,
    )
    session.add(excel)
    await session.flush()
    await session.refresh(excel)
    success(f"Exchange 'Excel' درج شد (id={excel.id})")
    return excel.id


async def seed_admin_user(session) -> int:
    """درج کاربر admin/1. خروجی: id کاربر."""
    from app.models import User
    from sqlalchemy import select

    # چک کن از قبل وجود ندارد
    stmt = select(User).where(User.username == "admin")
    result = await session.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing is not None:
        info(f"کاربر 'admin' از قبل موجود است (id={existing.id})")
        return existing.id

    # ساخت جدید
    info("در حال hash پسورد با bcrypt (rounds=12)...")
    pwd_hash = hash_password("1")
    info(f"hash تولید شد: {pwd_hash[:30]}...")

    admin = User(
        username="admin",
        password_hash=pwd_hash,
        role="admin",
        is_active=True,
    )
    session.add(admin)
    await session.flush()
    await session.refresh(admin)
    success(f"کاربر 'admin' درج شد (id={admin.id})")
    return admin.id


async def seed_risk_settings(session, user_id: int) -> None:
    """درج RiskSettings پیش‌فرض برای کاربر."""
    from app.models import RiskSettings
    from sqlalchemy import select

    # چک کن از قبل وجود ندارد (یک‌به‌یک با user)
    stmt = select(RiskSettings).where(RiskSettings.user_id == user_id)
    result = await session.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing is not None:
        info(f"RiskSettings برای user_id={user_id} از قبل موجود است")
        return

    rs = RiskSettings(
        user_id=user_id,
        # مقادیر پیش‌فرض همان‌هایی است که در مدل تعریف شده
    )
    session.add(rs)
    await session.flush()
    success(f"RiskSettings برای admin درج شد")


async def seed_app_settings(session, user_id: int) -> None:
    """درج AppSettings پیش‌فرض برای کاربر."""
    from app.models import AppSettings
    from sqlalchemy import select

    stmt = select(AppSettings).where(AppSettings.user_id == user_id)
    result = await session.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing is not None:
        info(f"AppSettings برای user_id={user_id} از قبل موجود است")
        return

    aps = AppSettings(
        user_id=user_id,
        # مقادیر پیش‌فرض همان‌هایی است که در مدل تعریف شده
    )
    session.add(aps)
    await session.flush()
    success(f"AppSettings برای admin درج شد")


# ============================================================
# main async
# ============================================================
async def main_async() -> int:
    header("اسکریپت ۱۴ — Seed Data")

    # ایمپورت dependencies (بعد از تنظیم sys.path)
    try:
        from app.infrastructure.database import AsyncSessionLocal, engine
    except ImportError as e:
        err(f"خطا در ایمپورت backend: {e}")
        err("مطمئن شوید که در venv هستید:")
        err("  D:")
        err("  cd /d D:\\Projects\\trading-system")
        err("  backend\\venv\\Scripts\\activate")
        err("  python scripts\\14_seed_data.py")
        return 1

    info(f"ریشه پروژه : {PROJECT_ROOT}")
    info(f"DB Path    : {BACKEND_DIR}/trading.db")
    print()

    # بررسی وجود فایل DB
    db_file = BACKEND_DIR / "trading.db"
    if not db_file.exists():
        err(f"فایل trading.db یافت نشد: {db_file}")
        err("ابتدا 'alembic upgrade head' را اجرا کنید.")
        return 1

    success("trading.db موجود است")
    print()

    # شروع seed
    info("شروع seed داده‌های اولیه...\n")

    async with AsyncSessionLocal() as session:
        try:
            # 1. Exchange "Excel"
            info("[1/4] Exchange 'Excel'")
            exchange_id = await seed_exchange(session)
            print()

            # 2. کاربر admin
            info("[2/4] User 'admin'")
            user_id = await seed_admin_user(session)
            print()

            # 3. RiskSettings
            info("[3/4] RiskSettings برای admin")
            await seed_risk_settings(session, user_id)
            print()

            # 4. AppSettings
            info("[4/4] AppSettings برای admin")
            await seed_app_settings(session, user_id)
            print()

            # commit نهایی
            await session.commit()
            success("Transaction commit شد")

        except Exception as e:
            await session.rollback()
            err(f"خطا در seed — rollback انجام شد: {e}")
            import traceback

            traceback.print_exc()
            return 1

    # آزاد کردن engine
    await engine.dispose()

    # ===== خلاصه نهایی =====
    header("خلاصه")

    # نمایش داده‌های درج‌شده
    from app.core.config import settings
    from app.models import AppSettings, Exchange, RiskSettings, User
    from sqlalchemy import select
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

    eng = create_async_engine(settings.DATABASE_URL)
    async with AsyncSession(eng) as session:
        # Exchanges
        result = await session.execute(select(Exchange))
        exchanges = result.scalars().all()
        info(f"Exchanges در DB: {len(exchanges)}")
        for ex in exchanges:
            print(
                f"    {GREEN}•{RESET} id={ex.id}  name={ex.name!r}  ccxt={ex.ccxt_id!r}  active={ex.is_active}"
            )

        # Users
        result = await session.execute(select(User))
        users = result.scalars().all()
        info(f"Users در DB: {len(users)}")
        for u in users:
            print(
                f"    {GREEN}•{RESET} id={u.id}  username={u.username!r}  role={u.role!r}  active={u.is_active}"
            )

        # RiskSettings
        result = await session.execute(select(RiskSettings))
        rss = result.scalars().all()
        info(f"RiskSettings در DB: {len(rss)}")
        for rs in rss:
            print(
                f"    {GREEN}•{RESET} user_id={rs.user_id}  max_risk={rs.max_risk_per_trade}  rr={rs.default_rr_ratio}"
            )

        # AppSettings
        result = await session.execute(select(AppSettings))
        apss = result.scalars().all()
        info(f"AppSettings در DB: {len(apss)}")
        for aps in apss:
            print(
                f"    {GREEN}•{RESET} user_id={aps.user_id}  theme={aps.theme!r}  tf={aps.default_timeframe!r}"
            )

    await eng.dispose()

    print()
    success("🎉 Seed با موفقیت انجام شد!")
    print()

    header("گام بعدی — زیرگام ۴.۲ کاملاً انجام شد!")
    info("می‌توانیم برویم سراغ زیرگام ۶ — DataSource Abstraction + Excel Reader")
    print()

    return 0


# ============================================================
# entry point
# ============================================================
def main() -> int:
    try:
        return asyncio.run(main_async())
    except KeyboardInterrupt:
        warn("لغو شد توسط کاربر")
        return 130


if __name__ == "__main__":
    sys.exit(main())
