"""
58b_test_phase1_deps.py — تست افزودن CCXT و websockets به requirements.txt

۶ تست:
1. وجود فایل
2. وجود خط دقیق ccxt==4.3.0 (و عدم تکرار)
3. وجود خط دقیق websockets==12.0 (و عدم تکرار)
4. وجود section header "Market Data" + "فاز ۱"
5. عدم وجود comment قدیمی (ccxt + websockets به‌عنوان آینده)
6. ترتیب: ccxt قبل از Testing section باشد
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQ_FILE = ROOT / "backend" / "requirements.txt"

EXPECTED_CCXT = "ccxt==4.3.0"
EXPECTED_WS = "websockets==12.0"


def read_content() -> str:
    return REQ_FILE.read_text(encoding="utf-8")


def t_file_exists() -> bool:
    if REQ_FILE.exists():
        print("[OK] file exists")
        return True
    print(f"[FAIL] file not found: {REQ_FILE}")
    return False


def t_ccxt_present() -> bool:
    content = read_content()
    lines = [l.strip() for l in content.splitlines()]
    matches = [l for l in lines if l == EXPECTED_CCXT]
    if len(matches) == 1:
        print(f"[OK] ccxt: {matches[0]}")
        return True
    if len(matches) > 1:
        print(f"[FAIL] ccxt duplicate ({len(matches)} occurrences)")
        return False
    print(f"[FAIL] ccxt not found at expected version ({EXPECTED_CCXT})")
    return False


def t_websockets_present() -> bool:
    content = read_content()
    lines = [l.strip() for l in content.splitlines()]
    matches = [l for l in lines if l == EXPECTED_WS]
    if len(matches) == 1:
        print(f"[OK] websockets: {matches[0]}")
        return True
    if len(matches) > 1:
        print(f"[FAIL] websockets duplicate ({len(matches)} occurrences)")
        return False
    print(f"[FAIL] websockets not found at expected version ({EXPECTED_WS})")
    return False


def t_section_header_present() -> bool:
    content = read_content()
    if "Market Data" in content and "فاز ۱" in content:
        print("[OK] Market Data section header present")
        return True
    print("[FAIL] Market Data section header missing")
    return False


def t_no_stale_comment() -> bool:
    content = read_content()
    bad = "ccxt، websockets، python-telegram-bot"
    if bad in content:
        print(f"[FAIL] stale comment present: '{bad}'")
        return False
    print("[OK] no stale comment about ccxt/websockets being future")
    return True


def t_order_before_testing() -> bool:
    content = read_content()
    ccxt_pos = content.find(EXPECTED_CCXT)
    testing_pos = content.find("# --- Testing")
    if ccxt_pos < 0 or testing_pos < 0:
        print(f"[FAIL] marker missing (ccxt_pos={ccxt_pos}, testing_pos={testing_pos})")
        return False
    if ccxt_pos < testing_pos:
        print("[OK] ccxt placed before Testing section")
        return True
    print("[FAIL] ccxt placed AFTER Testing section (wrong order)")
    return False


def main() -> int:
    tests = [
        t_file_exists,
        t_ccxt_present,
        t_websockets_present,
        t_section_header_present,
        t_no_stale_comment,
        t_order_before_testing,
    ]
    print(f"=== Running {len(tests)} tests ===")
    print()
    results = []
    for t in tests:
        try:
            results.append(t())
        except Exception as e:
            print(f"[ERROR] {t.__name__}: {e}")
            results.append(False)
    print()
    passed = sum(results)
    total = len(results)
    print(f"=== {passed}/{total} pass ===")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
