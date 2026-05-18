# -*- coding: utf-8 -*-
"""
اسکریپت گام ۲ — راه‌اندازی Backend پایه
================================================================
این اسکریپت فایل‌های پایه Backend را می‌سازد:

  • backend/requirements.txt
  • backend/.env.example
  • backend/.env                                 (یک‌بار با کلید تصادفی)
  • backend/main.py
  • backend/app/core/config.py
  • backend/app/api/v1/routes/health.py

نکته امنیتی مهم:
  فایل .env فقط در اولین اجرا ساخته می‌شود. کلیدهای رمزنگاری
  (SECRET_KEY و ENCRYPTION_KEY) به‌صورت تصادفی تولید می‌شوند.
  اگر این فایل گم شود، تمام API Keyهای رمزشده در آینده
  غیرقابل بازیابی خواهند بود.

نحوه اجرا (در CMD 3):
    cd /d D:\\Projects\\trading-system
    python scripts\\03_setup_backend_base.py

نسخه: 1.0.0
تاریخ: 2026-05-14
================================================================
"""

import base64
import os
import sys
from pathlib import Path

# ============================================================
# تنظیمات
# ============================================================
PROJECT_ROOT = Path(r"D:\Projects\trading-system")
BACKEND_DIR = PROJECT_ROOT / "backend"


# ============================================================
# توابع تولید کلیدهای تصادفی
# ============================================================
def generate_secret_key() -> str:
    """
    تولید SECRET_KEY تصادفی برای امضای JWT.

    خروجی: ۶۴ کاراکتر urlsafe base64 (بدون padding =).
    """
    return base64.urlsafe_b64encode(os.urandom(48)).decode("utf-8").rstrip("=")


def generate_fernet_key() -> str:
    """
    تولید Fernet key معتبر برای cryptography.Fernet.

    دقیقاً معادل cryptography.fernet.Fernet.generate_key():
      - ۳۲ بایت تصادفی
      - urlsafe base64 encode (شامل padding = در پایان)
      - طول نهایی: ۴۴ کاراکتر
    """
    return base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8")


# ============================================================
# محتوای فایل‌ها
# ============================================================

# --- requirements.txt ---
REQUIREMENTS_CONTENT = """\
# ============================================================
# requirements.txt — سامانه هوشمند ترید
# نسخه: v0.1.1 (گام ۲ فاز ۰)
# ============================================================

# --- Web Framework ---
fastapi==0.111.0
uvicorn[standard]==0.29.0

# --- Database & ORM ---
sqlalchemy==2.0.30
aiosqlite==0.20.0
alembic==1.13.1

# --- Validation & Settings ---
pydantic==2.7.1
pydantic-settings==2.2.1

# --- Authentication & Security ---
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
cryptography==42.0.7

# --- Environment ---
python-dotenv==1.0.1

# --- HTTP Client ---
httpx==0.27.0

# ============================================================
# نکته: ccxt، websockets، python-telegram-bot، openpyxl، pandas
# در فازهای آینده طبق نیاز اضافه خواهند شد.
# ============================================================
"""


# --- .env.example ---
ENV_EXAMPLE_CONTENT = """\
# ============================================================
# .env.example — نمونه تنظیمات محیطی
# ============================================================
# این فایل قابل commit به Git است (بدون مقادیر حساس).
# فایل واقعی .env با کلیدهای تصادفی توسط اسکریپت
# 03_setup_backend_base.py ساخته می‌شود.
# ============================================================

# === Application ===
APP_ENV=development
APP_NAME=Trading System
APP_VERSION=0.1.1

# === API ===
API_HOST=127.0.0.1
API_PORT=8000

# === Security (تولید خودکار توسط setup) ===
SECRET_KEY=replace_with_random_64_chars_string
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# === Encryption — Fernet key 44 chars (تولید خودکار توسط setup) ===
ENCRYPTION_KEY=replace_with_fernet_key_44_chars

# === Database ===
DB_PATH=./trading.db

# === CORS ===
FRONTEND_URL=http://localhost:5173

# === Timezone ===
TIMEZONE=UTC
DISPLAY_TIMEZONE=Asia/Tehran

# === Exchange API Keys (در فاز ۱+ پر می‌شوند) ===
# BINANCE_API_KEY=
# BINANCE_SECRET_KEY=
"""


# --- .env (با placeholderها) ---
ENV_CONTENT_TEMPLATE = """\
# ============================================================
# .env — فایل تنظیمات محیطی (حساس)
# ============================================================
# ⚠️  این فایل شامل کلیدهای رمزنگاری است.
# ⚠️  هرگز در Git commit نشود (در .gitignore است).
# ⚠️  از این فایل بک‌آپ امن بگیرید — اگر گم شود، تمام
#     API Keyهای رمزشده صرافی غیرقابل رمزگشایی می‌شوند.
# ============================================================

# === Application ===
APP_ENV=development
APP_NAME=Trading System
APP_VERSION=0.1.1

# === API ===
API_HOST=127.0.0.1
API_PORT=8000

# === Security ===
SECRET_KEY={secret_key}
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# === Encryption (Fernet) ===
ENCRYPTION_KEY={fernet_key}

# === Database ===
DB_PATH=./trading.db

# === CORS ===
FRONTEND_URL=http://localhost:5173

# === Timezone ===
TIMEZONE=UTC
DISPLAY_TIMEZONE=Asia/Tehran
"""


# --- backend/app/core/config.py ---
CONFIG_PY_CONTENT = '''# -*- coding: utf-8 -*-
"""
تنظیمات اپلیکیشن — بارگذاری از .env
================================================================
تمام مقادیر پیکربندی از .env خوانده می‌شوند.
هرگز مقدار Hardcode در کد قرار نمی‌گیرد (قانون قفل‌شده).

نحوه استفاده در سایر فایل‌ها:
    from app.core.config import settings
    print(settings.APP_VERSION)
================================================================
"""

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


# مسیر ریشه پوشه backend (که .env در آن قرار دارد)
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """کلاس تنظیمات اصلی — بارگذاری از .env با Pydantic v2"""

    model_config = SettingsConfigDict(
        env_file=str(BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # === Application ===
    APP_ENV: Literal["development", "production"] = "development"
    APP_NAME: str = "Trading System"
    APP_VERSION: str = "0.1.1"

    # === API ===
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"

    # === Security (اجباری از .env) ===
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # === Encryption (Fernet key — اجباری از .env) ===
    ENCRYPTION_KEY: str

    # === Database ===
    DB_PATH: str = "./trading.db"

    # === CORS ===
    FRONTEND_URL: str = "http://localhost:5173"

    # === Timezone ===
    TIMEZONE: str = "UTC"
    DISPLAY_TIMEZONE: str = "Asia/Tehran"

    # ============================================================
    # خصوصیات محاسبه‌شده
    # ============================================================

    @property
    def DATABASE_URL(self) -> str:
        """آدرس اتصال SQLAlchemy برای SQLite + aiosqlite"""
        return f"sqlite+aiosqlite:///{self.DB_PATH}"

    @property
    def IS_DEVELOPMENT(self) -> bool:
        """آیا در محیط توسعه هستیم؟"""
        return self.APP_ENV == "development"

    @property
    def CORS_ORIGINS(self) -> list[str]:
        """لیست منشأهای مجاز برای CORS"""
        return [self.FRONTEND_URL]


# نمونه singleton — در سرتاسر برنامه از این استفاده می‌شود
settings = Settings()
'''


# --- backend/app/api/v1/routes/health.py ---
HEALTH_PY_CONTENT = '''# -*- coding: utf-8 -*-
"""
Endpoint بررسی سلامت سیستم
================================================================
این endpoint برای:
  - تأیید فعال بودن API
  - بررسی نسخه و محیط در حال اجرا
  - Health check در Production Monitoring
================================================================
"""

from datetime import datetime, timezone

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check() -> dict:
    """
    بررسی سلامت API.

    خروجی: ساختار استاندارد پاسخ طبق سند ۶
        {success, message, data, errors}
    """
    return {
        "success": True,
        "message": "API سالم است",
        "data": {
            "status": "ok",
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        "errors": None,
    }
'''


# --- backend/main.py ---
MAIN_PY_CONTENT = '''# -*- coding: utf-8 -*-
"""
نقطه ورود FastAPI — سامانه هوشمند ترید
================================================================
این فایل فقط شامل: app instance + middleware + router include.

قواعد قفل‌شده:
  - Business Logic در services/ — هرگز اینجا
  - Query در repositories/ — هرگز اینجا
  - Validation در schemas/ — هرگز اینجا

نحوه اجرا (در CMD 1):
    cd backend
    venv\\\\Scripts\\\\activate
    uvicorn main:app --reload
================================================================
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import health
from app.core.config import settings


# ============================================================
# Lifecycle Events (Startup / Shutdown)
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """مدیریت چرخه عمر اپلیکیشن"""
    # ===== Startup =====
    print("=" * 60)
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"   Environment: {settings.APP_ENV}")
    print(f"   API: http://{settings.API_HOST}:{settings.API_PORT}{settings.API_PREFIX}")
    print(f"   Docs: http://{settings.API_HOST}:{settings.API_PORT}/docs")
    print("=" * 60)

    yield

    # ===== Shutdown =====
    print(f"👋 {settings.APP_NAME} shutting down...")


# ============================================================
# ساخت FastAPI app
# ============================================================
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="سامانه هوشمند ترید — کریپتو و فارکس",
    lifespan=lifespan,
)


# ============================================================
# Middleware
# ============================================================
# CORS — اجازه دسترسی Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# نکته: سایر middleware ها (Rate Limit, Auth, RBAC, Input Sanitize,
# Audit Log) طبق ترتیب سند ۶ در گام‌های بعد اضافه می‌شوند.


# ============================================================
# Router Registration
# ============================================================
app.include_router(health.router, prefix=settings.API_PREFIX)


# ============================================================
# Root Endpoint
# ============================================================
@app.get("/")
async def root() -> dict:
    """صفحه ریشه — اطلاعات کلی"""
    return {
        "success": True,
        "message": "سامانه هوشمند ترید فعال است",
        "data": {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "health": f"{settings.API_PREFIX}/health",
        },
        "errors": None,
    }
'''


# ============================================================
# توابع کمکی
# ============================================================
def write_file_full(path: Path, content: str) -> None:
    """نوشتن کامل فایل (با ساخت پوشه‌های والد در صورت نیاز)"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# ============================================================
# تابع اصلی
# ============================================================
def main() -> None:
    print("=" * 60)
    print("🛠️  گام ۲ — راه‌اندازی Backend پایه")
    print("=" * 60)
    print(f"📁 ریشه پروژه: {PROJECT_ROOT}")
    print(f"📁 ریشه Backend: {BACKEND_DIR}")
    print()

    # بررسی وجود پوشه‌های لازم
    if not PROJECT_ROOT.exists():
        print(f"❌ خطا: پوشه ریشه وجود ندارد: {PROJECT_ROOT}")
        sys.exit(1)
    if not BACKEND_DIR.exists():
        print(f"❌ خطا: پوشه backend وجود ندارد: {BACKEND_DIR}")
        print("   ابتدا scripts/01_create_structure.py را اجرا کنید.")
        sys.exit(1)

    # ============================================================
    # ۱) فایل‌های قابل بازنویسی
    # ============================================================
    files_to_overwrite = [
        ("backend/requirements.txt", REQUIREMENTS_CONTENT, "📦"),
        ("backend/.env.example", ENV_EXAMPLE_CONTENT, "📋"),
        ("backend/main.py", MAIN_PY_CONTENT, "🐍"),
        ("backend/app/core/config.py", CONFIG_PY_CONTENT, "⚙️ "),
        ("backend/app/api/v1/routes/health.py", HEALTH_PY_CONTENT, "🩺"),
    ]

    print("📝 ساخت/بازنویسی فایل‌ها:")
    print("-" * 60)
    for rel_path, content, icon in files_to_overwrite:
        full = PROJECT_ROOT / rel_path
        existed = full.exists()
        write_file_full(full, content)
        status = "بازنویسی شد" if existed else "ساخته شد   "
        print(f"   {icon} {rel_path:<48} {status}")
    print()

    # ============================================================
    # ۲) .env — فقط در اولین اجرا
    # ============================================================
    env_path = BACKEND_DIR / ".env"
    print("🔐 ساخت .env:")
    print("-" * 60)
    if env_path.exists():
        print(f"   ⚠️  backend/.env از قبل وجود دارد — حفظ شد")
        print(f"       (برای ساخت مجدد، ابتدا فایل را دستی پاک کنید)")
    else:
        secret_key = generate_secret_key()
        fernet_key = generate_fernet_key()
        env_content = ENV_CONTENT_TEMPLATE.format(secret_key=secret_key, fernet_key=fernet_key)
        write_file_full(env_path, env_content)
        print(f"   🔑 backend/.env ساخته شد (با کلیدهای تصادفی)")
        print()
        print(f"   ⚠️  ⚠️  ⚠️   هشدار مهم   ⚠️  ⚠️  ⚠️")
        print(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"   از فایل backend\\.env بک‌آپ امن بگیرید!")
        print(f"   اگر این فایل گم شود، تمام API Keyهای")
        print(f"   رمزنگاری‌شده صرافی غیرقابل بازیابی می‌شوند.")
        print(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()

    # ============================================================
    # پیام پایانی + راهنمای گام‌های دستی
    # ============================================================
    print("=" * 60)
    print("✅ ساخت فایل‌های گام ۲ کامل شد!")
    print("=" * 60)
    print()
    print("📌 گام‌های دستی بعدی در CMD:")
    print()
    print("─── ۱) ساخت Virtual Environment ───")
    print(r"      cd /d D:\Projects\trading-system\backend")
    print(r"      python -m venv venv")
    print()
    print("─── ۲) فعال‌سازی venv ───")
    print(r"      venv\Scripts\activate")
    print(r"      (در ابتدای خط باید (venv) ظاهر شود)")
    print()
    print("─── ۳) به‌روزرسانی pip ───")
    print(r"      python -m pip install --upgrade pip")
    print()
    print("─── ۴) نصب وابستگی‌ها (ممکن است ۲-۵ دقیقه طول بکشد) ───")
    print(r"      pip install -r requirements.txt")
    print()
    print("─── ۵) اجرای سرور ───")
    print(r"      uvicorn main:app --reload")
    print()
    print("─── ۶) تست در مرورگر ───")
    print(r"      http://127.0.0.1:8000/")
    print(r"      http://127.0.0.1:8000/api/v1/health")
    print(r"      http://127.0.0.1:8000/docs   (Swagger UI)")
    print()


if __name__ == "__main__":
    main()
