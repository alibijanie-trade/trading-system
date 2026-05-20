"""
63_backup_project.py — backup کامل پروژه به‌صورت zip

طبق قانون #۶۶ (در PENDING/Z2.9 برای v2.12):
در پایان هر چت، یک backup کامل از پروژه ساخته می‌شود.

فرمت نام: trading-system-chat{NN}-YYYY-MM-DD.zip (مثلاً trading-system-chat10-2026-05-20.zip)
محل: claude_workspace/backups/

پوشه‌های exclude:
- venv/، node_modules/ (reproducible از deps)
- __pycache__/، .pytest_cache/، dist/، build/، .vite/
- .git/ (در GitHub backup می‌شود)
- claude_workspace/backups/ (جلوگیری از recursive)
- *.pyc، *.pyo، *.log

شامل backup:
- کد backend + frontend + scripts + docs
- backend/trading.db
- claude_workspace/incoming_permanent/
- .env (local secrets)

استفاده:
    python scripts/63_backup_project.py --chat 10
    python scripts/63_backup_project.py --chat 11 --label "after-discovery"
"""

import argparse
import sys
import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKUPS_DIR = ROOT / "claude_workspace" / "backups"

# Directory names that match anywhere in the path → exclude
EXCLUDED_DIR_NAMES = {
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".git",
    "dist",
    "build",
    ".vite",
    ".turbo",
    ".coverage",
    "coverage",
    "backups",  # claude_workspace/backups recursive نشه
}

EXCLUDED_EXTS = {".pyc", ".pyo", ".log"}


def should_skip(path: Path) -> bool:
    """آیا این فایل از backup حذف شود؟"""
    rel_parts = path.relative_to(ROOT).parts
    for part in rel_parts:
        if part in EXCLUDED_DIR_NAMES:
            return True
    if path.suffix in EXCLUDED_EXTS:
        return True
    return False


def format_size(num_bytes: int) -> str:
    """تبدیل bytes به MB قابل‌خواندن."""
    return f"{num_bytes / (1024 * 1024):.1f} MB"


def main() -> int:
    parser = argparse.ArgumentParser(description="Backup کامل پروژه به‌صورت zip (طبق قانون #66)")
    parser.add_argument("--chat", type=int, required=True, help="شماره چت (مثلاً 10)")
    parser.add_argument(
        "--label", type=str, default="", help="برچسب اختیاری به انتهای نام (مثلاً 'after-discovery')"
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="overwrite اگر backup همان نام موجود است"
    )
    args = parser.parse_args()

    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    label_part = f"-{args.label}" if args.label else ""
    zip_name = f"trading-system-chat{args.chat:02d}-{date_str}{label_part}.zip"
    zip_path = BACKUPS_DIR / zip_name

    if zip_path.exists() and not args.overwrite:
        print(f"[WARN] backup already exists: {zip_name}")
        print("       برای overwrite از --overwrite یا --label برای نام دیگر استفاده کنید")
        return 1

    if zip_path.exists():
        print(f"[INFO] overwriting existing: {zip_name}")

    print(f"[INFO] ساخت backup: {zip_name}")
    print(f"[INFO] جمع‌آوری فایل‌ها از: {ROOT}")
    print()

    files_added = 0
    files_skipped = 0
    total_uncompressed = 0
    largest_files: list[tuple[int, str]] = []

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path in ROOT.rglob("*"):
            if not path.is_file():
                continue
            if should_skip(path):
                files_skipped += 1
                continue

            rel_path = path.relative_to(ROOT)
            try:
                size = path.stat().st_size
                zf.write(path, str(rel_path))
                files_added += 1
                total_uncompressed += size
                # track largest files
                largest_files.append((size, str(rel_path)))
                largest_files.sort(reverse=True)
                largest_files = largest_files[:5]
            except (PermissionError, OSError) as e:
                print(f"[WARN] skipped (error): {rel_path} — {e}")
                files_skipped += 1

    zip_size = zip_path.stat().st_size
    ratio = (1 - zip_size / total_uncompressed) * 100 if total_uncompressed > 0 else 0

    print(f"[OK] backup ساخته شد")
    print(f"     مسیر: {zip_path}")
    print(f"     فایل‌های اضافه شده: {files_added}")
    print(f"     فایل‌های skip شده: {files_skipped}")
    print(f"     اندازه قبل از فشرده‌سازی: {format_size(total_uncompressed)}")
    print(f"     اندازه zip: {format_size(zip_size)}")
    print(f"     نسبت فشرده‌سازی: {ratio:.1f}%")
    print()
    print(f"     ۵ فایل بزرگ‌ترین در backup:")
    for size, name in largest_files:
        print(f"       {format_size(size):>10}  {name}")
    print()
    print(
        f"     بعدی: python scripts/63b_test_backup.py --chat {args.chat}{' --label ' + args.label if args.label else ''}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
