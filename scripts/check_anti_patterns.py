# -*- coding: utf-8 -*-
"""
check_anti_patterns.py - custom pre-commit hook for A1-A10

Hybrid mode:
  - critical (A1, A4, A8, A10): fail commit
  - minor (A6 print): warning only

Usage:
  python scripts/check_anti_patterns.py            # check all files
  python scripts/check_anti_patterns.py --staged   # check git staged files

Notes:
  - ASCII-only output for Windows cp1252 compatibility
  - No emoji, no special Unicode in print()
"""

from __future__ import annotations

import io
import re
import subprocess
import sys
from pathlib import Path

# UTF-8 stdout for Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
        except Exception:
            pass

ROOT = Path(__file__).resolve().parent.parent

# ============================================================
# Rules
# ============================================================

CRITICAL = {
    "A1": {
        "name": "hex color hardcoded in JSX",
        "pattern": r"#[0-9a-fA-F]{3,6}\b",
        "files": [".jsx"],
        "exclude_paths": ["frontend/src/themes/", "frontend/src/index.css"],
        "exclude_context": [
            "// theme-tokens-allowed",
            "readVar(",  # fallback default in readVar(varName, "#default")
            "theme-fallback",  # // theme-fallback comment marker
        ],
    },
    "A4": {
        "name": "hardcoded secret/password/api_key/token",
        "pattern": r"""(SECRET_KEY|PASSWORD|API_KEY|TOKEN)\s*=\s*["\'][^"\']{8,}["\']""",
        "files": [".py"],
        "exclude_paths": ["tests/", "scripts/"],
        "exclude_context": ["# noqa: secret-allowed", "settings.", "os.environ"],
    },
    "A8": {
        "name": "localStorage in JSX (use Zustand store instead)",
        "pattern": r"localStorage\.(get|set)Item",
        "files": [".jsx"],
        "exclude_paths": ["frontend/src/stores/", "frontend/src/utils/storage"],
        "exclude_context": [],
    },
    "A10": {
        "name": "sync I/O (open/time.sleep/requests) in async context",
        "pattern": r"^\s+(with open\(|time\.sleep|requests\.)",
        "files": [".py"],
        "exclude_paths": ["scripts/", "tests/", "migrations/"],
        "exclude_context": ["# noqa: sync-allowed"],
    },
}

MINOR = {
    "A6": {
        "name": "print() instead of logger in backend",
        "pattern": r"^\s*print\(",
        "files": [".py"],
        "exclude_paths": ["scripts/", "tests/", "migrations/", "backend/main.py"],
        "exclude_context": ["# noqa: print-allowed"],
    },
}


def normalize_path(p: Path) -> str:
    """Return relative path with forward slashes (cross-platform)."""
    return str(p.relative_to(ROOT)).replace("\\", "/")


def get_staged_files() -> list[Path]:
    """Get git staged files."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",
        )
        return [ROOT / f for f in result.stdout.splitlines() if f.strip()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def get_all_project_files() -> list[Path]:
    """Get all Python and JSX files in the project."""
    files = []
    for pattern in ["backend/**/*.py", "scripts/**/*.py", "frontend/src/**/*.jsx"]:
        files.extend(ROOT.glob(pattern))
    return [
        f
        for f in files
        if "venv" not in str(f) and "node_modules" not in str(f) and "__pycache__" not in str(f)
    ]


def check_file(path: Path, rule_id: str, rule: dict) -> list[str]:
    """Check one file against one rule. Return list of violations."""
    if not path.exists() or path.is_dir():
        return []

    if path.suffix not in rule["files"]:
        return []

    rel = normalize_path(path)
    for excl in rule["exclude_paths"]:
        if rel.startswith(excl):
            return []

    violations = []
    pattern = re.compile(rule["pattern"], re.MULTILINE)
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []

    lines = text.splitlines()
    for m in pattern.finditer(text):
        line_num = text[: m.start()].count("\n") + 1
        line = lines[line_num - 1] if line_num <= len(lines) else ""

        # Skip if excluded context found
        if any(ctx in line for ctx in rule["exclude_context"]):
            continue

        # ASCII-safe output
        snippet = line.strip()[:100]
        violations.append(f"  [{rule_id}] {rel}:{line_num} -- {snippet}")

    return violations


def main() -> int:
    # Determine file list
    if "--staged" in sys.argv:
        files = get_staged_files()
        if not files:
            print("[INFO] No staged files. Use without --staged to check all.")
            return 0
    else:
        files = get_all_project_files()

    critical_violations = []
    minor_violations = []

    for rule_id, rule in CRITICAL.items():
        for f in files:
            for v in check_file(f, rule_id, rule):
                critical_violations.append((rule_id, rule["name"], v))

    for rule_id, rule in MINOR.items():
        for f in files:
            for v in check_file(f, rule_id, rule):
                minor_violations.append((rule_id, rule["name"], v))

    # Report (ASCII-only)
    print("=" * 64)
    print(f"  Anti-Patterns check ({len(files)} files scanned)")
    print("=" * 64)

    if critical_violations:
        print()
        print("=" * 64)
        print("  [FAIL] CRITICAL Anti-Pattern Violations -- commit aborted")
        print("=" * 64)
        for rule_id, name, v in critical_violations:
            print(f"\n  [{rule_id}] {name}")
            print(v)
        print()

    if minor_violations:
        print()
        print("=" * 64)
        print("  [WARN] MINOR Anti-Pattern Warnings -- commit allowed")
        print("=" * 64)
        for rule_id, name, v in minor_violations:
            print(f"\n  [{rule_id}] {name}")
            print(v)
        print()

    if critical_violations:
        print()
        print("[INFO] For emergency bypass:")
        print('   git commit --no-verify -m "[skip-hooks: REASON] ..."')
        return 1

    if not critical_violations and not minor_violations:
        print()
        print("  [OK] No anti-patterns found.")
    else:
        print()
        print("  [OK] No critical violations. Minor warnings only.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
