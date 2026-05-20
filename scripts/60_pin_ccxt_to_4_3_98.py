"""
60_pin_ccxt_to_4_3_98.py — تغییر نسخه ccxt در requirements.txt به 4.3.98

دلیل: ccxt==4.3.0 در PyPI وجود ندارد (احتمالاً منتشر نشده یا yank شد).
آخرین stable در همان minor version (4.3.x) که در PyPI موجود است: 4.3.98.

اعمال:
1. خط `ccxt==4.3.0` (یا هر 4.3.x دیگر) را به `ccxt==4.3.98` تغییر می‌دهد
2. BOM فایل حفظ می‌شود (read/write با utf-8-sig)
3. Idempotent: اگر قبلاً 4.3.98 است، skip
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQ_FILE = ROOT / "backend" / "requirements.txt"

TARGET_VERSION = "4.3.98"
TARGET_LINE = f"ccxt=={TARGET_VERSION}"
PATTERN = re.compile(r"^ccxt==\S+\s*$", re.MULTILINE)


def main() -> int:
    if not REQ_FILE.exists():
        print(f"[ERROR] file not found: {REQ_FILE}")
        return 1

    # Read with utf-8-sig (strips BOM if present)
    content = REQ_FILE.read_text(encoding="utf-8-sig")

    matches = PATTERN.findall(content)
    if not matches:
        print(f"[ERROR] no ccxt== line found in {REQ_FILE.name}")
        return 2

    if len(matches) > 1:
        print(f"[ERROR] {len(matches)} ccxt lines found — manual review needed")
        for m in matches:
            print(f"   {m.strip()}")
        return 3

    current = matches[0].strip()
    if current == TARGET_LINE:
        print(f"[SKIP] ccxt already pinned to {TARGET_VERSION}")
        return 0

    # Replace
    print(f"[INFO] changing: {current} → {TARGET_LINE}")
    new_content = PATTERN.sub(TARGET_LINE, content, count=1)

    # Write with utf-8-sig (re-adds BOM)
    REQ_FILE.write_text(new_content, encoding="utf-8-sig")

    # Read-back verify
    verify = REQ_FILE.read_text(encoding="utf-8-sig")
    if TARGET_LINE not in verify:
        print(f"[FAIL] read-back: {TARGET_LINE} not found")
        return 4

    # Verify BOM still present
    with open(REQ_FILE, "rb") as f:
        if f.read(3) != b"\xef\xbb\xbf":
            print("[FAIL] BOM lost after write — Bug #53 may return")
            return 5

    print(f"[OK] ccxt pinned to {TARGET_VERSION}, BOM preserved")
    print()
    print("Next step (in activated venv):")
    print("   pip install -r requirements.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
