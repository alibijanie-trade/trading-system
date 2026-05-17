# -*- coding: utf-8 -*-
"""
اسکریپت ۲۳ — تست Auth + OHLCV محافظت‌شده از ترمینال
================================================================
این اسکریپت ۷ تست انجام می‌دهد:

  ۱) POST /auth/login (admin/1)         → 200 + tokens
  ۲) GET  /auth/me با access            → 200 + اطلاعات admin
  ۳) GET  /ohlcv/1 بدون token           → 401
  ۴) GET  /ohlcv/1 با access            → 200 + کندل‌ها
  ۵) POST /auth/refresh با refresh      → 200 + access جدید
  ۶) POST /auth/logout با refresh       → 200
  ۷) POST /auth/refresh با refresh لغو شده → 401

نکته: OAuth2PasswordRequestForm با multipart/form-data ارسال می‌شود
       (نه JSON). در httpx از پارامتر data= استفاده می‌کنیم.

پیش‌نیاز:
  - Backend در 🟦 tab «1 backend» در حال اجرا

اجرا (🟩 tab «2 scripts»):
    python scripts\\23_test_auth.py
================================================================
"""

import json
import sys

import httpx

BASE_URL = "http://127.0.0.1:8000"
API = f"{BASE_URL}/api/v1"


# ============================================================
# توابع کمکی
# ============================================================
def hr(num: int, title: str) -> None:
    print()
    print("=" * 72)
    print(f"  تست {num}: {title}")
    print("=" * 72)


def show(resp: httpx.Response, expected: int) -> dict | None:
    ok = resp.status_code == expected
    print(f"  انتظار: {expected}    دریافت: {resp.status_code}    {'✓' if ok else '✗'}")
    try:
        data = resp.json()
    except json.JSONDecodeError:
        print(f"  پاسخ غیر JSON: {resp.text[:200]}")
        return None

    if isinstance(data, dict):
        print(f"  success: {data.get('success')}")
        msg = data.get("message") or data.get("detail")
        if msg:
            print(f"  message: {msg}")
        d = data.get("data")
        if isinstance(d, dict):
            # خلاصه‌سازی tokens
            preview = {}
            for k, v in d.items():
                if isinstance(v, str) and len(v) > 40:
                    preview[k] = v[:35] + "…"
                else:
                    preview[k] = v
            print(f"  data   : {preview}")
        errors = data.get("errors")
        if errors:
            print(f"  errors : {errors}")
    return data


def fatal(msg: str, code: int = 1) -> None:
    print()
    print("=" * 72)
    print(f"  ✗ {msg}")
    print("=" * 72)
    sys.exit(code)


# ============================================================
# اجرا
# ============================================================
def main() -> None:
    print("=" * 72)
    print("  اسکریپت ۲۳ — تست Auth + OHLCV محافظت‌شده")
    print("=" * 72)
    print(f"  Base: {BASE_URL}")

    try:
        client = httpx.Client(timeout=10.0)
    except httpx.HTTPError as e:
        fatal(f"خطای client httpx: {e}")

    # ============================================================
    # تست ۱ — login
    # ============================================================
    hr(1, "POST /auth/login (username=admin, password=1)")
    try:
        resp = client.post(
            f"{API}/auth/login",
            data={"username": "admin", "password": "1"},
        )
    except httpx.ConnectError:
        fatal("اتصال برقرار نشد. آیا backend در 🟦 tab «1 backend» روشن است؟", 2)

    body = show(resp, expected=200)
    if not body or not body.get("data"):
        fatal("Login ناموفق — ادامه تست ممکن نیست")

    access = body["data"]["access_token"]
    refresh = body["data"]["refresh_token"]
    print(f"  access_token  (40 char اول): {access[:40]}…")
    print(f"  refresh_token (40 char اول): {refresh[:40]}…")

    auth_header = {"Authorization": f"Bearer {access}"}

    # ============================================================
    # تست ۲ — /auth/me
    # ============================================================
    hr(2, "GET /auth/me (با access token)")
    resp = client.get(f"{API}/auth/me", headers=auth_header)
    show(resp, expected=200)

    # ============================================================
    # تست ۳ — OHLCV بدون token
    # ============================================================
    hr(3, "GET /ohlcv/1 بدون token (انتظار 401)")
    resp = client.get(f"{API}/ohlcv/1?timeframe=1d&limit=3")
    show(resp, expected=401)

    # ============================================================
    # تست ۴ — OHLCV با access
    # ============================================================
    hr(4, "GET /ohlcv/1 با access token (انتظار 200)")
    resp = client.get(
        f"{API}/ohlcv/1?timeframe=1d&limit=3",
        headers=auth_header,
    )
    body = show(resp, expected=200)
    if body and body.get("data"):
        candles = body["data"].get("candles") or []
        print(f"  تعداد کندل: {len(candles)}")
        if candles:
            print(f"  اولین کندل: {json.dumps(candles[0], ensure_ascii=False)}")

    # ============================================================
    # تست ۵ — refresh
    # ============================================================
    hr(5, "POST /auth/refresh (با refresh token معتبر)")
    resp = client.post(
        f"{API}/auth/refresh",
        json={"refresh_token": refresh},
    )
    body = show(resp, expected=200)
    if body and body.get("data"):
        new_access = body["data"]["access_token"]
        print(f"  access جدید (40 char اول): {new_access[:40]}…")
        same = new_access == access
        print(f"  access جدید == access قبلی ؟ {same}")

    # ============================================================
    # تست ۶ — logout
    # ============================================================
    hr(6, "POST /auth/logout (revoke refresh token)")
    resp = client.post(
        f"{API}/auth/logout",
        headers=auth_header,
        json={"refresh_token": refresh},
    )
    show(resp, expected=200)

    # ============================================================
    # تست ۷ — refresh پس از logout
    # ============================================================
    hr(7, "POST /auth/refresh با refresh لغو شده (انتظار 401)")
    resp = client.post(
        f"{API}/auth/refresh",
        json={"refresh_token": refresh},
    )
    show(resp, expected=401)

    client.close()

    print()
    print("=" * 72)
    print("  ✅ پایان تست‌ها — Auth flow کامل")
    print("=" * 72)


if __name__ == "__main__":
    main()
