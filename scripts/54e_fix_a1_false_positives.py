# -*- coding: utf-8 -*-
"""
54e_fix_a1_false_positives.py -- رفع false positive های A1 در check_anti_patterns

A1 الگوی فعلی هر #hexcolor را در .jsx فلگ می‌کند، حتی اگر در
readVar(..., "#fallback") باشد که خود theme system است (نه hardcoded).

اصلاح:
  - افزودن exclude_context برای 'readVar('
  - افزودن exclude_context برای ' = "#' (فقط در default values)
  - افزودن exclude برای کامنت `// theme-fallback`
"""

from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAP = ROOT / "scripts" / "check_anti_patterns.py"


OLD_A1 = '''    "A1": {
        "name": "hex color hardcoded in JSX",
        "pattern": r"#[0-9a-fA-F]{3,6}\\\\b",
        "files": [".jsx"],
        "exclude_paths": ["frontend/src/themes/", "frontend/src/index.css"],
        "exclude_context": ["// theme-tokens-allowed"],
    },'''

NEW_A1 = '''    "A1": {
        "name": "hex color hardcoded in JSX",
        "pattern": r"#[0-9a-fA-F]{3,6}\\\\b",
        "files": [".jsx"],
        "exclude_paths": ["frontend/src/themes/", "frontend/src/index.css"],
        "exclude_context": [
            "// theme-tokens-allowed",
            "readVar(",  # fallback default in readVar(varName, "#default")
            "theme-fallback",  # // theme-fallback comment marker
        ],
    },'''


def main() -> int:
    if not CAP.exists():
        print("[ERR] check_anti_patterns.py پیدا نشد")
        return 1
    text = CAP.read_text(encoding="utf-8")
    # Idempotent
    if 'readVar(' in text and 'exclude_context' in text and '"readVar("' in text:
        print("[SKIP] قبلاً اصلاح شده")
        return 0
    if OLD_A1 not in text:
        # Try a more flexible match - check_anti_patterns may have been formatted by black
        print("[WARN] OLD_A1 exact match نشد - تلاش با regex...")
        import re
        pattern = re.compile(
            r'"A1":\s*\{[^}]*"exclude_context":\s*\[\s*"//\s*theme-tokens-allowed"\s*,?\s*\]\s*,?\s*\}',
            re.DOTALL,
        )
        m = pattern.search(text)
        if not m:
            print("[ERR] ساختار A1 پیدا نشد - اصلاح دستی لازم")
            print("[INFO] لطفاً در check_anti_patterns.py در dict CRITICAL کلید A1،")
            print("       به exclude_context این موارد را اضافه کنید:")
            print('         "readVar(",')
            print('         "theme-fallback",')
            return 1
        # Replace
        new_text = text[:m.start()] + NEW_A1.lstrip() + text[m.end():]
        CAP.write_text(new_text, encoding="utf-8", newline="\n")
        print("[OK] A1 با regex اصلاح شد")
        return 0

    text = text.replace(OLD_A1, NEW_A1, 1)
    CAP.write_text(text, encoding="utf-8", newline="\n")
    print("[OK] A1 exclude_context گسترش یافت (readVar + theme-fallback)")
    print()
    print("Next:")
    print("  pre-commit run --all-files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
