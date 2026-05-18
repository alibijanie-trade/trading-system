# -*- coding: utf-8 -*-
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
from app.core.config import settings
from app.core.exceptions import AuthenticationError
from jose import JWTError, jwt

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
    data.update(
        {
            "iat": now,
            "exp": now + expires_delta,
            "type": token_type,
        }
    )
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
