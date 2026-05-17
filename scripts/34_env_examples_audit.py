# -*- coding: utf-8 -*-
"""
اسکریپت ۳۴ — Audit و تکمیل فایل‌های .env.example
================================================================
Task: T2.03 (Tier 2 — Quality Hardening)

این اسکریپت idempotent است — قابل اجرا چندبار بدون شکست.

محتوای کار:
  ۱) backend/.env.example — به‌روزرسانی کامل:
     - APP_VERSION: 0.1.1 → 0.4.0  (همگام با CHANGELOG)
     - افزودن API_PREFIX (که در config.py هست ولی در .env.example نبود)
     - افزودن دستورالعمل تولید SECRET_KEY و ENCRYPTION_KEY
     - افزودن کامنت برای هر کلید
     - حفظ بخش Exchange API Keys (commented out)

  ۲) frontend/.env.example — ساخت از صفر:
     - VITE_API_URL با کامنت و راهنما
     - توضیح prefix VITE_ و قرارداد امنیتی Vite

نکات معماری:
  - backend/.env (state کاربر) دست‌نخورده می‌ماند
  - فقط .env.example (قابل commit) به‌روز می‌شود
  - الگوی write_if_changed برای idempotency
  - منبع رسمی keys: backend/app/core/config.py (کلاس Settings)
                    + frontend/src grep "import.meta.env"

نحوه اجرا (tab «2 scripts»):
    python scripts\\34_env_examples_audit.py

سپس برای تست:
    python scripts\\34b_test_env_examples.py
================================================================
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
BACKEND_ENV_EXAMPLE = PROJECT_ROOT / "backend" / ".env.example"
FRONTEND_ENV_EXAMPLE = PROJECT_ROOT / "frontend" / ".env.example"


# ────────────────────────────────────────────────────────────────
# محتوای جدید backend/.env.example
# ────────────────────────────────────────────────────────────────
# همگام با backend/app/core/config.py (کلاس Settings)
# و CHANGELOG.md (نسخه فعلی)
BACKEND_ENV_EXAMPLE_CONTENT = """\
# ============================================================
# .env.example — نمونه تنظیمات محیطی backend
# ============================================================
# این فایل قابل commit به Git است — هیچ مقدار حساسی ندارد.
#
# نحوه استفاده:
#   ۱) این فایل را به .env کپی کنید:
#        cp backend/.env.example backend/.env
#   ۲) SECRET_KEY و ENCRYPTION_KEY را با مقادیر تصادفی واقعی
#      پر کنید (راهنمای تولید زیر هر کلید آمده).
#   ۳) سایر مقادیر را به دلخواه تنظیم کنید.
#
# تولید خودکار:
#   اسکریپت scripts/03_setup_backend_base.py در صورت نبود .env
#   آن را با کلیدهای تصادفی واقعی می‌سازد.
#
# منبع رسمی keys: app/core/config.py (کلاس Settings)
# ============================================================

# === Application ===
# APP_ENV: محیط اجرا — "development" یا "production"
APP_ENV=development
APP_NAME=Trading System
# APP_VERSION: نسخه جاری برنامه (همگام با CHANGELOG.md)
APP_VERSION=0.5.0

# === API ===
# API_HOST: آدرس bind شدن uvicorn
API_HOST=127.0.0.1
# API_PORT: پورت backend
API_PORT=8000
# API_PREFIX: prefix همه endpointها (مثلاً /api/v1/auth/login)
API_PREFIX=/api/v1

# === Security (اجباری — placeholder در این فایل) ===
# SECRET_KEY: کلید امضای JWT — حداقل ۶۴ کاراکتر تصادفی.
# تولید با Python:
#   python -c "import secrets; print(secrets.token_urlsafe(48))"
SECRET_KEY=replace_with_random_64_chars_string
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# === Encryption — Fernet key ۴۴ کاراکتر (اجباری — placeholder) ===
# ENCRYPTION_KEY: برای رمزنگاری API Keyهای صرافی در DB.
# تولید با Python:
#   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
ENCRYPTION_KEY=replace_with_fernet_key_44_chars

# === Database ===
# DB_PATH: مسیر فایل SQLite — relative نسبت به پوشه backend/
DB_PATH=./trading.db

# === CORS ===
# FRONTEND_URL: آدرس frontend برای CORS whitelist
FRONTEND_URL=http://localhost:5173

# === Timezone ===
# TIMEZONE: timezone ذخیره‌سازی داده‌ها (همیشه UTC پیشنهاد می‌شود)
TIMEZONE=UTC
# DISPLAY_TIMEZONE: timezone نمایش به کاربر
DISPLAY_TIMEZONE=Asia/Tehran

# === Exchange API Keys (در فاز ۱+ پر می‌شوند — اختیاری) ===
# BINANCE_API_KEY=
# BINANCE_SECRET_KEY=
"""


# ────────────────────────────────────────────────────────────────
# محتوای frontend/.env.example
# ────────────────────────────────────────────────────────────────
# همگام با: grep -r "import.meta.env" frontend/src/
FRONTEND_ENV_EXAMPLE_CONTENT = """\
# ============================================================
# .env.example — نمونه تنظیمات محیطی frontend (Vite)
# ============================================================
# این فایل قابل commit به Git است — هیچ مقدار حساسی ندارد.
#
# نحوه استفاده:
#   ۱) این فایل را به .env کپی کنید:
#        cp frontend/.env.example frontend/.env
#   ۲) مقادیر را برای محیط خود تنظیم کنید.
#
# ⚠️  نکته امنیتی Vite:
#   فقط متغیرهای با prefix VITE_ به کد frontend expose می‌شوند
#   (طبق قرارداد Vite). همه‌ی این متغیرها در bundle نهایی
#   به صورت plain-text به مرورگر فرستاده می‌شوند.
#   → برای SECRETها هرگز از VITE_ استفاده نکنید.
#
# منبع رسمی keys: grep -r "import.meta.env" frontend/src/
# ============================================================

# === API ===
# VITE_API_URL: آدرس پایه backend API (شامل prefix)
# باید با FRONTEND_URL در backend/.env همخوان باشد (از طرف backend)
# و با مسیر واقعی mount endpointها (API_PREFIX).
VITE_API_URL=http://localhost:8000/api/v1
"""


# ────────────────────────────────────────────────────────────────
# الگوی write_if_changed برای idempotency
# ────────────────────────────────────────────────────────────────
def write_if_changed(path: Path, content: str) -> str:
    """
    اگر محتوای فایل با content فرق دارد، فایل را به‌روز می‌کند.
    Returns:
      "created"   — فایل وجود نداشت، ساخته شد
      "updated"   — فایل وجود داشت، محتوا تغییر کرد
      "unchanged" — فایل از قبل صحیح بود
    """
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        return "created"

    try:
        current = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        current = path.read_text(encoding="cp1252")

    if current == content:
        return "unchanged"

    path.write_text(content, encoding="utf-8", newline="\n")
    return "updated"


def main() -> int:
    print("=" * 64)
    print("اسکریپت ۳۴ — Audit و تکمیل فایل‌های .env.example")
    print("=" * 64)
    print()

    # === backend ===
    print("📝 backend/.env.example")
    status = write_if_changed(BACKEND_ENV_EXAMPLE, BACKEND_ENV_EXAMPLE_CONTENT)
    icon = {"created": "🆕", "updated": "✏️", "unchanged": "✓"}[status]
    print(f"   {icon} {status}  → {BACKEND_ENV_EXAMPLE.relative_to(PROJECT_ROOT)}")
    print()

    # === frontend ===
    print("📝 frontend/.env.example")
    status = write_if_changed(FRONTEND_ENV_EXAMPLE, FRONTEND_ENV_EXAMPLE_CONTENT)
    icon = {"created": "🆕", "updated": "✏️", "unchanged": "✓"}[status]
    print(f"   {icon} {status}  → {FRONTEND_ENV_EXAMPLE.relative_to(PROJECT_ROOT)}")
    print()

    # === خلاصه ===
    print("-" * 64)
    print("✅ پایان. حالا برای تست اجرا کنید:")
    print("   python scripts/34b_test_env_examples.py")
    print()
    print("📌 یادآوری:")
    print("   - این تغییرات فقط روی .env.example اعمال شد (قابل commit).")
    print("   - فایل‌های واقعی .env دست‌نخورده باقی ماندند.")
    print("   - اگر همکار جدید پروژه را clone کند، اسکریپت")
    print("     03_setup_backend_base.py یا 00b_post_unzip_setup.py")
    print("     .env واقعی را با کلیدهای تصادفی می‌سازد.")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
