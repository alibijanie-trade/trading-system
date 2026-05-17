# -*- coding: utf-8 -*-
"""
اسکریپت ۲۲c — رفع bug passlib، استفاده مستقیم از bcrypt
================================================================
مشکل:
  passlib==1.7.4 با bcrypt>=4.1 ناسازگار است:
      ValueError: password cannot be longer than 72 bytes
  این در detect_wrap_bug() داخل passlib رخ می‌دهد.

راه‌حل:
  حذف passlib از security.py — استفاده مستقیم از bcrypt 4.x

سازگاری با seed:
  seed admin/1 با bcrypt.hashpw() ساخته شد — فرمت hash یکسان است.

فایل‌های به‌روز:
  ۱) backend/app/core/security.py    (hash/verify بدون passlib)
  ۲) backend/requirements.txt        (حذف passlib، تثبیت bcrypt==4.1.3)

پس از اجرا:
  🟩 tab «2 scripts»:
      pip uninstall passlib -y
      pip install bcrypt==4.1.3
  🟦 tab «1 backend»:
      Ctrl+C  →  uvicorn main:app --reload
================================================================
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
APP_DIR = BACKEND_DIR / "app"


# ============================================================
# ۱) app/core/security.py — bcrypt مستقیم (بدون passlib)
# ============================================================
CORE_SECURITY_PY = '''# -*- coding: utf-8 -*-
"""
Security utilities — bcrypt مستقیم + JWT
================================================================
توابع کمکی برای:
  - hash و verify رمز عبور (bcrypt مستقیم — بدون passlib)
  - encode/decode JWT (HS256 via python-jose)

🆕 v0.2.0: passlib حذف شد به دلیل ناسازگاری با bcrypt 4.x
            (تصمیم #40 — Session 4).

استفاده در service layer:
    from app.core.security import (
        hash_password, verify_password,
        create_access_token, create_refresh_token, decode_token,
    )

قانون قفل‌شده (سند ۹.۱):
  - تنها این فایل JWT/bcrypt را مستقیم استفاده می‌کند
  - service ها از این توابع استفاده می‌کنند
================================================================
"""

from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings
from app.core.exceptions import AuthenticationError

# تعداد rounds پیش‌فرض bcrypt — توازن امنیت/سرعت
BCRYPT_ROUNDS = 12


# ============================================================
# Password Hashing — bcrypt مستقیم
# ============================================================
def hash_password(plain: str) -> str:
    """
    ساخت hash bcrypt برای رمز عبور.

    نکته bcrypt: رمز عبور بیش از ۷۲ بایت silently truncate
    نمی‌شود (در bcrypt 4.x). اینجا اگر طولانی بود به ۷۲ بایت
    اول محدود می‌کنیم — سازگار با رفتار historic.
    """
    pwd_bytes = plain.encode("utf-8")[:72]
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """
    بررسی مطابقت رمز عبور با hash.

    اگر hash خراب باشد، False برمی‌گرداند (نه exception).
    """
    pwd_bytes = plain.encode("utf-8")[:72]
    try:
        return bcrypt.checkpw(pwd_bytes, hashed.encode("utf-8"))
    except (ValueError, TypeError):
        return False


# ============================================================
# JWT Tokens
# ============================================================
def _create_token(
    payload: dict[str, Any],
    expires_delta: timedelta,
    token_type: str,
) -> str:
    """ساخت JWT با iat + exp + type."""
    now = datetime.now(timezone.utc)
    data = payload.copy()
    data.update({
        "iat": now,
        "exp": now + expires_delta,
        "type": token_type,
    })
    return jwt.encode(
        data,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_access_token(user_id: int, username: str, role: str) -> str:
    """ساخت access token کوتاه‌مدت (پیش‌فرض ۳۰ دقیقه)."""
    return _create_token(
        payload={"sub": str(user_id), "username": username, "role": role},
        expires_delta=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access",
    )


def create_refresh_token(user_id: int) -> tuple[str, datetime]:
    """
    ساخت refresh token بلندمدت (پیش‌فرض ۷ روز).

    Returns:
        (token, expires_at) — expires_at برای ذخیره در DB
    """
    expires_delta = timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    token = _create_token(
        payload={"sub": str(user_id), "jti": str(uuid4())},
        expires_delta=expires_delta,
        token_type="refresh",
    )
    expires_at = datetime.now(timezone.utc) + expires_delta
    return token, expires_at


def decode_token(token: str, expected_type: str) -> dict[str, Any]:
    """
    decode + اعتبارسنجی JWT.

    Args:
        token: رشته JWT
        expected_type: "access" یا "refresh"

    Raises:
        AuthenticationError: توکن نامعتبر / منقضی / نوع اشتباه
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except JWTError as e:
        raise AuthenticationError(
            message="توکن نامعتبر یا منقضی است",
            code="INVALID_TOKEN",
        ) from e

    if payload.get("type") != expected_type:
        raise AuthenticationError(
            message=f"نوع توکن صحیح نیست (انتظار: {expected_type})",
            code="WRONG_TOKEN_TYPE",
        )
    return payload
'''


# ============================================================
# ۲) backend/requirements.txt — حذف passlib، تثبیت bcrypt==4.1.3
# ============================================================
REQUIREMENTS_TXT = '''# ============================================================
# requirements.txt — سامانه هوشمند ترید
# نسخه: v0.2.0 (Auth + JWT + رفع bug passlib/bcrypt — تصمیم #40)
# ============================================================

# --- Web Framework ---
fastapi==0.111.0
uvicorn[standard]==0.29.0
python-multipart==0.0.9    # OAuth2PasswordRequestForm (multipart/form-data)

# --- Database & ORM ---
sqlalchemy==2.0.30
aiosqlite==0.20.0
alembic==1.13.1

# --- Validation & Settings ---
pydantic==2.7.1
pydantic-settings==2.2.1

# --- Authentication & Security ---
# 🆕 v0.2.0: passlib حذف شد به دلیل ناسازگاری با bcrypt 4.x
# bcrypt مستقیم استفاده می‌شود (تصمیم #40)
python-jose[cryptography]==3.3.0
bcrypt==4.1.3
cryptography==42.0.7

# --- Environment ---
python-dotenv==1.0.1
colorama==0.4.6    # Windows ANSI colors support

# --- HTTP Client ---
httpx==0.27.0

# --- Data Processing (فاز ۶ - Excel Reader) ---
pandas==2.2.2
openpyxl==3.1.2

# ============================================================
# نکته: ccxt، websockets، python-telegram-bot
# در فازهای آینده طبق نیاز اضافه خواهند شد.
# ============================================================
'''


FILES_TO_WRITE: dict[Path, str] = {
    APP_DIR / "core" / "security.py": CORE_SECURITY_PY,
    BACKEND_DIR / "requirements.txt": REQUIREMENTS_TXT,
}


def main() -> None:
    print("=" * 64)
    print("اسکریپت ۲۲c — رفع bug passlib، bcrypt مستقیم")
    print("=" * 64)

    if not BACKEND_DIR.exists():
        print(f"[ERROR] پوشه backend پیدا نشد: {BACKEND_DIR}")
        raise SystemExit(1)

    for path, content in FILES_TO_WRITE.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"  ✓ {path.relative_to(PROJECT_ROOT)}")

    print()
    print("=" * 64)
    print(f"✅ {len(FILES_TO_WRITE)} فایل به‌روز شد.")
    print("=" * 64)
    print()
    print("مراحل بعد:")
    print()
    print("  🟩 tab «2 scripts»:")
    print("      pip uninstall passlib -y")
    print("      pip install bcrypt==4.1.3")
    print()
    print("  🟦 tab «1 backend»:")
    print("      Ctrl+C")
    print("      uvicorn main:app --reload")
    print()
    print("  🟩 tab «2 scripts»:")
    print("      python scripts\\23_test_auth.py")


if __name__ == "__main__":
    main()
