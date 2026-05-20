"""
59_fix_requirements_encoding.py — افزودن BOM به requirements.txt

هدف: حل Bug #53 — pip روی Windows فارسی-locale نمی‌تواند فایل UTF-8 بدون BOM با متن غیر-ASCII را parse کند.

اعمال:
1. خواندن requirements.txt با utf-8-sig (BOM را skip می‌کند اگر موجود باشد)
2. نوشتن مجدد با utf-8-sig (BOM را اضافه می‌کند)

Idempotent: اگر فایل قبلاً BOM دارد، read-write مجدد آن را تغییری در محتوا ایجاد نمی‌کند.
Read-back verify: byte های اول بررسی می‌شوند تا BOM (EF BB BF) وجود داشته باشد.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQ_FILE = ROOT / "backend" / "requirements.txt"

BOM = b"\xef\xbb\xbf"


def has_bom() -> bool:
    with open(REQ_FILE, "rb") as f:
        return f.read(3) == BOM


def main() -> int:
    if not REQ_FILE.exists():
        print(f"[ERROR] file not found: {REQ_FILE}")
        return 1

    before_bom = has_bom()
    print(f"[INFO] BOM status before: {'PRESENT' if before_bom else 'MISSING'}")

    if before_bom:
        print("[SKIP] BOM already present. No change needed.")
        return 0

    # Read with utf-8-sig (strips BOM if present, fine if not)
    content = REQ_FILE.read_text(encoding="utf-8-sig")

    # Write with utf-8-sig (adds BOM)
    REQ_FILE.write_text(content, encoding="utf-8-sig")

    # Read-back verify
    after_bom = has_bom()
    print(f"[INFO] BOM status after:  {'PRESENT' if after_bom else 'MISSING'}")

    if not after_bom:
        print("[FAIL] BOM was not written correctly.")
        return 2

    # Verify ccxt/websockets still present
    verify = REQ_FILE.read_text(encoding="utf-8-sig")
    if "ccxt==4.3.0" not in verify or "websockets==12.0" not in verify:
        print("[FAIL] dependencies missing after BOM fix.")
        return 3

    print("[OK] BOM added. requirements.txt is now pip-compatible on Windows locales.")
    print()
    print("Next step: re-activate venv and run pip install.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
