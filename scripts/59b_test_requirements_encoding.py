"""
59b_test_requirements_encoding.py — تست BOM در requirements.txt

۴ تست:
1. وجود فایل
2. وجود BOM در ابتدای فایل (3 بایت EF BB BF)
3. parseable بودن با utf-8-sig
4. حفظ شدن ccxt و websockets بعد از BOM fix
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQ_FILE = ROOT / "backend" / "requirements.txt"

BOM = b"\xef\xbb\xbf"


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
        print(f"[OK] BOM present (bytes: {first3.hex()})")
        return True
    print(f"[FAIL] BOM missing. First 3 bytes: {first3.hex()}")
    return False


def t_parseable_as_utf8() -> bool:
    try:
        content = REQ_FILE.read_text(encoding="utf-8-sig")
        if len(content) > 0:
            print(f"[OK] parseable as utf-8-sig ({len(content)} chars)")
            return True
        print("[FAIL] file is empty after BOM strip")
        return False
    except UnicodeDecodeError as e:
        print(f"[FAIL] decode error: {e}")
        return False


def t_deps_still_present() -> bool:
    content = REQ_FILE.read_text(encoding="utf-8-sig")
    has_ccxt = "ccxt==4.3.0" in content
    has_ws = "websockets==12.0" in content
    if has_ccxt and has_ws:
        print("[OK] ccxt==4.3.0 and websockets==12.0 still present")
        return True
    print(f"[FAIL] missing — ccxt={has_ccxt}, websockets={has_ws}")
    return False


def main() -> int:
    tests = [t_file_exists, t_bom_present, t_parseable_as_utf8, t_deps_still_present]
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
