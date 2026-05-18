# -*- coding: utf-8 -*-
"""
54f_direct_fix_a1.py -- اصلاح مستقیم A1 با read/replace/write

این بار از template برای generation استفاده نمی‌کنیم.
به‌جای آن، خود فایل را می‌خوانیم و pattern مورد نظر را replace می‌کنیم.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAP = ROOT / "scripts" / "check_anti_patterns.py"


def main() -> int:
    if not CAP.exists():
        print("[ERR] check_anti_patterns.py not found")
        return 1

    text = CAP.read_text(encoding="utf-8")

    # Idempotent check
    if '"readVar(",  # fallback default' in text:
        print("[SKIP] A1 already fixed")
        return 0

    # The exclude_context for A1 currently is something like:
    #     "exclude_context": ["// theme-tokens-allowed"],
    # We expand it to include readVar( and theme-fallback markers

    OLD = '"exclude_context": ["// theme-tokens-allowed"],'
    NEW = '''"exclude_context": [
            "// theme-tokens-allowed",
            "readVar(",  # fallback default in readVar(varName, "#default")
            "theme-fallback",  # // theme-fallback comment marker
        ],'''

    if OLD not in text:
        # Try after black formatting - black may put each item on new line
        OLD_BLACK = '"exclude_context": ["// theme-tokens-allowed"]'
        if OLD_BLACK in text:
            text = text.replace(OLD_BLACK, NEW.rstrip(','), 1)
            CAP.write_text(text, encoding="utf-8", newline="\n")
            print("[OK] A1 fixed (black-formatted variant)")
            return 0

        print("[ERR] A1 anchor not found")
        print("[INFO] Showing first 'exclude_context' occurrence in file:")
        idx = text.find('"exclude_context"')
        if idx != -1:
            print(text[idx:idx+200])
        return 1

    text = text.replace(OLD, NEW, 1)
    CAP.write_text(text, encoding="utf-8", newline="\n")
    print("[OK] A1 exclude_context expanded")
    print()
    print("Next:")
    print("  pre-commit run --all-files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
