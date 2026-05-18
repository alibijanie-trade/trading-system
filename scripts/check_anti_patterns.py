# -*- coding: utf-8 -*-
"""
check_anti_patterns.py — هوک سفارشی pre-commit برای A1-A10

این اسکریپت روی فایل‌های staged Python و JSX اجرا می‌شود.
حالت Hybrid:
  - critical (A1, A4, A8, A10): fail commit
  - minor (A6 print): warning only

استفاده مستقیم: python scripts\check_anti_patterns.py
از pre-commit: خودکار
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ============================================================
# لیست anti-pattern ها (Hybrid: critical اجباری، minor warning)
# ============================================================

CRITICAL = {
    # A1 — hex color hardcoded در JSX (frontend only)
    "A1": {
        "name": "hex color hardcoded در JSX",
        "pattern": r"#[0-9a-fA-F]{3,6}",
        "files": [".jsx"],
        "exclude_paths": ["frontend/src/themes/", "frontend/src/index.css"],
        "exclude_context": ["// theme-tokens-allowed"],
    },
    # A4 — secrets hardcoded
    "A4": {
        "name": "secret hardcoded (password/key/token)",
        "pattern": r'''(SECRET_KEY|PASSWORD|API_KEY|TOKEN)\s*=\s*["\'][^"\']{8,}["\']''',
        "files": [".py"],
        "exclude_paths": ["tests/", "scripts/"],
        "exclude_context": ["# noqa: secret-allowed", "settings.", "os.environ"],
    },
    # A8 — localStorage در JSX (Claude artifacts)
    "A8": {
        "name": "localStorage در JSX (به‌جای Zustand store)",
        "pattern": r"localStorage\.(get|set)Item",
        "files": [".jsx"],
        "exclude_paths": ["frontend/src/stores/", "frontend/src/utils/storage"],
        "exclude_context": [],
    },
    # A10 — sync I/O در async function
    "A10": {
        "name": "sync I/O (open/time.sleep/requests) در async context",
        "pattern": r"^\s+(with open\(|time\.sleep|requests\.)",
        "files": [".py"],
        "exclude_paths": ["scripts/", "tests/", "migrations/"],
        "exclude_context": ["# noqa: sync-allowed"],
    },
}

MINOR = {
    # A6 — print در backend
    "A6": {
        "name": "print() به‌جای logger در backend",
        "pattern": r"^\s*print\(",
        "files": [".py"],
        "exclude_paths": ["scripts/", "tests/", "migrations/", "backend/main.py"],
        "exclude_context": ["# noqa: print-allowed"],
    },
}


def get_staged_files() -> list[Path]:
    """فایل‌های staged از git."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True, text=True, check=True,
        )
        return [ROOT / f for f in result.stdout.splitlines() if f.strip()]
    except subprocess.CalledProcessError:
        return []


def check_file(path: Path, rule_id: str, rule: dict) -> list[str]:
    """بررسی یک فایل برای یک قانون. لیست violations برمی‌گرداند."""
    if not path.exists() or path.is_dir():
        return []

    ext = path.suffix
    if ext not in rule["files"]:
        return []

    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    for excl in rule["exclude_paths"]:
        if rel.startswith(excl):
            return []

    violations = []
    pattern = re.compile(rule["pattern"], re.MULTILINE)
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []

    for m in pattern.finditer(text):
        # شماره خط
        line_num = text[:m.start()].count("\n") + 1
        line = text.splitlines()[line_num - 1] if line_num <= len(text.splitlines()) else ""

        # exclude_context
        skip = False
        for ctx in rule["exclude_context"]:
            if ctx in line:
                skip = True
                break
        if skip:
            continue

        violations.append(f"  [{rule_id}] {rel}:{line_num} — {line.strip()[:100]}")

    return violations


def main() -> int:
    files = get_staged_files()
    if not files:
        # احتمالاً اجرای دستی — همه فایل‌های پروژه را چک کن
        files = list((ROOT / "backend").rglob("*.py")) + list((ROOT / "frontend" / "src").rglob("*.jsx"))
        files = [f for f in files if "venv" not in str(f) and "node_modules" not in str(f)]

    critical_violations = []
    minor_violations = []

    for rule_id, rule in CRITICAL.items():
        for f in files:
            critical_violations.extend(
                (rule_id, rule["name"], v) for v in check_file(f, rule_id, rule)
            )

    for rule_id, rule in MINOR.items():
        for f in files:
            minor_violations.extend(
                (rule_id, rule["name"], v) for v in check_file(f, rule_id, rule)
            )

    # گزارش
    if critical_violations:
        print("=" * 64)
        print("  ❌ Anti-Pattern Violations (CRITICAL — commit aborted)")
        print("=" * 64)
        for rule_id, name, v in critical_violations:
            print(f"\n  🔴 {rule_id}: {name}")
            print(v)
        print()

    if minor_violations:
        print("=" * 64)
        print("  ⚠️  Anti-Pattern Warnings (MINOR — commit allowed)")
        print("=" * 64)
        for rule_id, name, v in minor_violations:
            print(f"\n  🟡 {rule_id}: {name}")
            print(v)
        print()

    if critical_violations:
        print("📌 برای bypass (فقط در اضطرار):")
        print('   git commit --no-verify -m "[skip-hooks: REASON] ..."')
        return 1

    if not critical_violations and not minor_violations:
        print("✓ هیچ anti-pattern یافت نشد.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
