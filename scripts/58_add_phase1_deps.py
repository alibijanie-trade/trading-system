"""
58_add_phase1_deps.py — افزودن CCXT و websockets به requirements.txt

هدف: شروع گام G1 چت ۱۰ — فاز ۱ (CCXT + Binance WebSocket).
نسخه‌ها از سند جامع v2.11 بخش ۲.۲ (Stack).

اعمال:
1. درج بخش "Market Data (فاز ۱)" قبل از بخش Testing
2. ccxt==4.3.0
3. websockets==12.0
4. به‌روزرسانی comment block پایانی فایل

ویژگی‌ها:
- Idempotent: اگر خطوط قبلاً موجود باشند، تغییری اعمال نمی‌شود
- Read-back verify: پس از write، فایل دوباره خوانده می‌شود
- خطای صریح در صورت inconsistent state (نسخه متفاوت)
"""

import sys
from pathlib import Path

# نسخه‌ها — طبق سند جامع v2.11 بخش ۲.۲
CCXT_VERSION = "4.3.0"
WEBSOCKETS_VERSION = "12.0"

ROOT = Path(__file__).resolve().parent.parent
REQ_FILE = ROOT / "backend" / "requirements.txt"

NEW_BLOCK = (
    "# --- Market Data (فاز ۱ — CCXT + Binance WebSocket) ---\n"
    f"ccxt=={CCXT_VERSION}\n"
    f"websockets=={WEBSOCKETS_VERSION}\n"
    "\n"
)

TESTING_MARKER = "# --- Testing (T2.08 — چت ۷) ---"

OLD_COMMENT = (
    "# ============================================================\n"
    "# نکته: ccxt، websockets، python-telegram-bot\n"
    "# در فازهای آینده طبق نیاز اضافه خواهند شد.\n"
    "# ============================================================\n"
)

NEW_COMMENT = (
    "# ============================================================\n"
    "# نکته: python-telegram-bot در فازهای آینده طبق نیاز اضافه خواهد شد.\n"
    "# ccxt و websockets در چت ۱۰ (فاز ۱) افزوده شدند.\n"
    "# ============================================================\n"
)


def main() -> int:
    if not REQ_FILE.exists():
        print(f"[ERROR] file not found: {REQ_FILE}")
        return 1

    content = REQ_FILE.read_text(encoding="utf-8")

    has_ccxt_line = f"ccxt=={CCXT_VERSION}" in content
    has_ws_line = f"websockets=={WEBSOCKETS_VERSION}" in content
    has_ccxt_any = "ccxt==" in content
    has_ws_any = "websockets==" in content

    if has_ccxt_line and has_ws_line:
        print("[SKIP] Both dependencies already present at expected versions.")
        print(f"   ccxt=={CCXT_VERSION}")
        print(f"   websockets=={WEBSOCKETS_VERSION}")
        return 0

    if has_ccxt_any and not has_ccxt_line:
        print(f"[ERROR] ccxt present at different version. Expected: {CCXT_VERSION}")
        print(f"   Manual review of requirements.txt required.")
        return 2

    if has_ws_any and not has_ws_line:
        print(f"[ERROR] websockets present at different version. Expected: {WEBSOCKETS_VERSION}")
        print(f"   Manual review of requirements.txt required.")
        return 3

    if TESTING_MARKER not in content:
        print(f"[ERROR] Testing section marker not found:")
        print(f"   {TESTING_MARKER}")
        return 4

    # Insert new dependency block before Testing section
    content = content.replace(TESTING_MARKER, NEW_BLOCK + TESTING_MARKER)

    # Update comment block (if old form exists)
    comment_updated = False
    if OLD_COMMENT in content:
        content = content.replace(OLD_COMMENT, NEW_COMMENT)
        comment_updated = True

    # Write
    REQ_FILE.write_text(content, encoding="utf-8")

    # Read-back verify
    verify = REQ_FILE.read_text(encoding="utf-8")
    if f"ccxt=={CCXT_VERSION}" not in verify:
        print(f"[FAIL] read-back: ccxt=={CCXT_VERSION} not found")
        return 5
    if f"websockets=={WEBSOCKETS_VERSION}" not in verify:
        print(f"[FAIL] read-back: websockets=={WEBSOCKETS_VERSION} not found")
        return 6

    print("[OK] requirements.txt updated:")
    print(f"   + ccxt=={CCXT_VERSION}")
    print(f"   + websockets=={WEBSOCKETS_VERSION}")
    if comment_updated:
        print("   ~ comment block updated")
    print()
    print("Next step (in backend venv):")
    print("   cd backend")
    print("   venv\\Scripts\\activate")
    print("   pip install -r requirements.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
