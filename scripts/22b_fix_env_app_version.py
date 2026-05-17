# -*- coding: utf-8 -*-
"""
اسکریپت ۲۲b — اصلاح APP_VERSION در .env
================================================================
این اسکریپت idempotent است:
  - اگر خط APP_VERSION=... در .env باشد، آن را به 0.2.0 تغییر می‌دهد
  - اگر نباشد، اضافه می‌کند
  - اگر مقدار 0.2.0 از قبل باشد، چیزی تغییر نمی‌کند

نحوه اجرا (tab «2 scripts»):
    python scripts\\22b_fix_env_app_version.py

سپس uvicorn را Restart کنید.
================================================================
"""

import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
ENV_PATH = PROJECT_ROOT / "backend" / ".env"

TARGET_VERSION = "0.2.0"


def main() -> None:
    print("=" * 64)
    print("اسکریپت ۲۲b — اصلاح APP_VERSION در .env")
    print("=" * 64)
    print(f"  مسیر فایل: {ENV_PATH}")
    print(f"  نسخه هدف : {TARGET_VERSION}")
    print()

    if not ENV_PATH.exists():
        print(f"[ERROR] فایل .env پیدا نشد: {ENV_PATH}")
        raise SystemExit(1)

    # خواندن — utf-8 با fallback
    try:
        content = ENV_PATH.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = ENV_PATH.read_text(encoding="cp1252")

    # الگوی خط APP_VERSION (شامل کامنت و فاصله)
    pattern = re.compile(
        r"^(\s*APP_VERSION\s*=\s*)(.+?)(\s*(#.*)?)$",
        re.MULTILINE,
    )

    match = pattern.search(content)

    if match:
        current = match.group(2).strip().strip('"\'')
        if current == TARGET_VERSION:
            print(f"  ✓ APP_VERSION از قبل = {TARGET_VERSION} است (بدون تغییر)")
        else:
            new_content = pattern.sub(
                lambda m: f"{m.group(1)}{TARGET_VERSION}{m.group(3)}",
                content,
                count=1,
            )
            ENV_PATH.write_text(new_content, encoding="utf-8", newline="\n")
            print(f"  ✓ APP_VERSION از {current!r} به {TARGET_VERSION!r} تغییر یافت")
    else:
        # افزودن در پایان
        if not content.endswith("\n"):
            content += "\n"
        content += f"APP_VERSION={TARGET_VERSION}\n"
        ENV_PATH.write_text(content, encoding="utf-8", newline="\n")
        print(f"  ✓ APP_VERSION={TARGET_VERSION} به .env افزوده شد")

    print()
    print("=" * 64)
    print("✅ پایان. حالا uvicorn را در tab «1 backend» Restart کن.")
    print("=" * 64)


if __name__ == "__main__":
    main()
