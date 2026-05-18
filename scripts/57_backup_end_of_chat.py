# -*- coding: utf-8 -*-
"""
57_backup_end_of_chat.py -- Backup با نام نسخه‌دار طبق قانون #۴۸

این اسکریپت در پایان هر چت اجرا می‌شود و کل پروژه (به‌جز venv و node_modules)
را در یک فایل zip در پوشه `backups/` با نام نسخه‌دار ذخیره می‌کند.

فرمت نام:
  backup_chat-{N}_{YYYYMMDD}_{commit-hash}.zip

مثال:
  backup_chat-7_20260518_24235aa.zip

استفاده:
  python scripts\\57_backup_end_of_chat.py 7

اگر شماره چت ندهید، از CHAT_LOG.md استخراج می‌کند.

excluded:
  - .git/
  - backend/venv/
  - frontend/node_modules/
  - frontend/dist/
  - **/__pycache__/
  - **/*.pyc
  - **/.pytest_cache/
  - **/htmlcov/
  - **/.coverage
  - backend/trading.db (داده تست)
  - backend/logs/*.log
  - backups/  (خود این پوشه)
"""

from __future__ import annotations

import io
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

ROOT = Path(__file__).resolve().parent.parent
BACKUPS_DIR = ROOT / "backups"

# Patterns to exclude (rglob-style)
EXCLUDE_DIRS = {
    ".git",
    "venv",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    ".pytest_cache",
    ".cache",
    "htmlcov",
    ".sync-backup",
    "backups",
    "logs",
    ".pre-commit-cache",
}

EXCLUDE_FILE_PATTERNS = {
    ".pyc",
    ".pyo",
    ".coverage",
    ".db",
    ".sqlite",
    ".sqlite3",
    ".log",
}


def get_git_hash_short() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short=7", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "nogit"


def get_chat_number(arg: str | None) -> int:
    if arg:
        try:
            return int(arg)
        except ValueError:
            pass

    # Try to detect from CHAT_LOG.md
    chat_log = ROOT / "docs" / "CHAT_LOG.md"
    if chat_log.exists():
        text = chat_log.read_text(encoding="utf-8")
        # Find latest "## چت N" heading
        import re

        # Find Persian digits ۰-۹
        persian_to_ascii = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
        matches = re.findall(r"## چت ([۰-۹0-9]+)", text)
        if matches:
            numbers = [int(m.translate(persian_to_ascii)) for m in matches]
            return max(numbers)

    # Default
    return 0


def should_exclude(rel_path: Path) -> bool:
    """Check if a file/dir should be excluded from backup."""
    parts = rel_path.parts

    # Exclude any path with excluded dir name
    for excl in EXCLUDE_DIRS:
        if excl in parts:
            return True

    # Exclude by suffix
    if rel_path.suffix in EXCLUDE_FILE_PATTERNS:
        return True

    return False


def main() -> int:
    print("=" * 64)
    print("  57_backup_end_of_chat -- Backup با نام نسخه‌دار")
    print("=" * 64)
    print()

    # Detect chat number
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    chat_num = get_chat_number(arg)
    if chat_num == 0:
        print("[ERR] شماره چت نامشخص. مثال:")
        print("   python scripts\\57_backup_end_of_chat.py 7")
        return 1

    # Generate filename
    date_str = datetime.now().strftime("%Y%m%d")
    git_hash = get_git_hash_short()
    filename = f"backup_chat-{chat_num}_{date_str}_{git_hash}.zip"

    BACKUPS_DIR.mkdir(exist_ok=True)
    output_path = BACKUPS_DIR / filename

    if output_path.exists():
        print(f"[SKIP] {filename} از قبل موجود است")
        size_mb = output_path.stat().st_size / 1024 / 1024
        print(f"       Size: {size_mb:.2f} MB")
        return 0

    print(f"  Chat number: {chat_num}")
    print(f"  Git hash: {git_hash}")
    print(f"  Output: backups/{filename}")
    print()

    # Collect files
    files_to_zip: list[tuple[Path, str]] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if should_exclude(rel):
            continue
        # Skip the backup itself
        if path == output_path:
            continue
        files_to_zip.append((path, str(rel).replace("\\", "/")))

    if not files_to_zip:
        print("[ERR] هیچ فایلی برای backup پیدا نشد")
        return 1

    # Create zip
    print(f"  Compressing {len(files_to_zip)} files...")
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for src, arcname in files_to_zip:
            try:
                zf.write(src, arcname)
            except (OSError, PermissionError) as e:
                print(f"  [WARN] skip {arcname}: {e}")

    size_mb = output_path.stat().st_size / 1024 / 1024
    print()
    print("=" * 64)
    print(f"  [OK] backup ساخته شد")
    print(f"       Path:  backups/{filename}")
    print(f"       Files: {len(files_to_zip)}")
    print(f"       Size:  {size_mb:.2f} MB")
    print("=" * 64)
    print()
    print("نکته: این فایل در backups/ ذخیره می‌شود.")
    print("توصیه: backups/ را در .gitignore اضافه کنید (اگر هنوز نیست).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
