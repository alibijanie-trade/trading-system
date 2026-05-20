"""
60b_test_ccxt_pin.py — تست تغییر ccxt به 4.3.98 + حفظ BOM

۵ تست:
1. وجود فایل
2. BOM هنوز موجود (regression test برای M67)
3. خط ccxt==4.3.98 موجود (بدون duplicate)
4. خط قدیمی ccxt==4.3.0 موجود نیست
5. websockets==12.0 هنوز موجود (regression test)
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQ_FILE = ROOT / "backend" / "requirements.txt"

BOM = b"\xef\xbb\xbf"
EXPECTED_CCXT = "ccxt==4.3.98"
OLD_CCXT = "ccxt==4.3.0"
EXPECTED_WS = "websockets==12.0"


def read_content() -> str:
    return REQ_FILE.read_text(encoding="utf-8-sig")


def t_file_exists() -> bool:
    if REQ_FILE.exists():
        print("[OK] file exists")
        return True
    print(f"[FAIL] file not found: {REQ_FILE}")
    return False


def t_bom_present() -> bool:
    with open(REQ_FILE, "rb") as f:
        first3 = f.read(3)
    if first3 == BOM:
        print("[OK] BOM present (regression test M67 pass)")
        return True
    print(f"[FAIL] BOM missing — Bug #53 returned. First 3 bytes: {first3.hex()}")
    return False


def t_new_ccxt_present() -> bool:
    content = read_content()
    lines = [l.strip() for l in content.splitlines()]
    matches = [l for l in lines if l == EXPECTED_CCXT]
    if len(matches) == 1:
        print(f"[OK] {matches[0]}")
        return True
    if len(matches) > 1:
        print(f"[FAIL] duplicate ccxt lines ({len(matches)})")
        return False
    print(f"[FAIL] {EXPECTED_CCXT} not found")
    return False


def t_old_ccxt_absent() -> bool:
    content = read_content()
    if OLD_CCXT in content:
        print(f"[FAIL] old version still present: {OLD_CCXT}")
        return False
    print(f"[OK] old version removed ({OLD_CCXT})")
    return True


def t_websockets_intact() -> bool:
    content = read_content()
    lines = [l.strip() for l in content.splitlines()]
    matches = [l for l in lines if l == EXPECTED_WS]
    if len(matches) == 1:
        print(f"[OK] {matches[0]} intact")
        return True
    print(f"[FAIL] websockets line corrupted (found {len(matches)} matches)")
    return False


def main() -> int:
    tests = [
        t_file_exists,
        t_bom_present,
        t_new_ccxt_present,
        t_old_ccxt_absent,
        t_websockets_intact,
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
