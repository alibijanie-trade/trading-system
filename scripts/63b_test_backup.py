"""
63b_test_backup.py — تست backup zip ساخته‌شده توسط script 63

۵ تست:
1. فایل zip موجود است
2. zipfile.testzip() integrity check
3. فایل‌های کلیدی در zip موجودند (sample 5 فایل)
4. هیچ پوشه excluded (venv، node_modules، .git) در zip نیست
5. حجم zip منطقی است (1MB < size < 200MB)
"""

import argparse
import sys
import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKUPS_DIR = ROOT / "claude_workspace" / "backups"

KEY_FILES_TO_VERIFY = [
    "README.md",
    "backend/requirements.txt",
    "backend/app/infrastructure/data_sources/base.py",
    "backend/app/infrastructure/data_sources/ccxt_source.py",
    "docs/CHAT_LOG.md",
    "docs/SESSION_STATUS.md",
    "claude_workspace/incoming_permanent/CHAT11_HANDOFF.txt",
    "scripts/62_create_ccxt_source.py",
]

EXCLUDED_DIR_NAMES = {
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".git",
    "dist",
    "build",
    ".vite",
}

MIN_SIZE = 1 * 1024 * 1024  # 1 MB
MAX_SIZE = 200 * 1024 * 1024  # 200 MB


def get_zip_path(chat: int, label: str = "") -> Path:
    date_str = datetime.now().strftime("%Y-%m-%d")
    label_part = f"-{label}" if label else ""
    name = f"trading-system-chat{chat:02d}-{date_str}{label_part}.zip"
    return BACKUPS_DIR / name


def t_file_exists(zip_path: Path) -> bool:
    if zip_path.exists():
        print(f"[OK] zip exists: {zip_path.name}")
        return True
    print(f"[FAIL] zip not found: {zip_path}")
    return False


def t_integrity(zip_path: Path) -> bool:
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            bad = zf.testzip()
            if bad is not None:
                print(f"[FAIL] corrupted member: {bad}")
                return False
        print("[OK] integrity check passed (testzip)")
        return True
    except Exception as e:
        print(f"[FAIL] integrity exception: {e}")
        return False


def t_key_files_present(zip_path: Path) -> bool:
    with zipfile.ZipFile(zip_path, "r") as zf:
        members = set(zf.namelist())
        # zip uses forward slashes regardless of OS
        normalized = set(m.replace("\\", "/") for m in members)
        missing = []
        for kf in KEY_FILES_TO_VERIFY:
            if kf not in normalized:
                missing.append(kf)
        if missing:
            print(f"[FAIL] missing key files: {missing}")
            return False
        print(f"[OK] all {len(KEY_FILES_TO_VERIFY)} key files present in zip")
        return True


def t_no_excluded_dirs(zip_path: Path) -> bool:
    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.namelist():
            parts = member.replace("\\", "/").split("/")
            for ex in EXCLUDED_DIR_NAMES:
                if ex in parts:
                    print(f"[FAIL] excluded dir found in zip: {member}")
                    return False
    print("[OK] no excluded directories (venv, node_modules, .git, ...) in zip")
    return True


def t_size_reasonable(zip_path: Path) -> bool:
    size = zip_path.stat().st_size
    size_mb = size / (1024 * 1024)
    if size < MIN_SIZE:
        print(f"[FAIL] zip too small: {size_mb:.2f} MB (min: {MIN_SIZE / 1024 / 1024:.0f} MB)")
        return False
    if size > MAX_SIZE:
        print(f"[FAIL] zip too large: {size_mb:.2f} MB (max: {MAX_SIZE / 1024 / 1024:.0f} MB)")
        return False
    print(f"[OK] size reasonable: {size_mb:.2f} MB")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="تست backup zip (script 63)")
    parser.add_argument("--chat", type=int, required=True, help="شماره چت")
    parser.add_argument("--label", type=str, default="", help="label اختیاری")
    args = parser.parse_args()

    zip_path = get_zip_path(args.chat, args.label)
    print(f"=== تست backup: {zip_path.name} ===")
    print()

    tests = [
        ("file_exists", lambda: t_file_exists(zip_path)),
        ("integrity", lambda: t_integrity(zip_path)),
        ("key_files", lambda: t_key_files_present(zip_path)),
        ("no_excluded", lambda: t_no_excluded_dirs(zip_path)),
        ("size_reasonable", lambda: t_size_reasonable(zip_path)),
    ]

    results = []
    for name, test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"[ERROR] {name}: {type(e).__name__}: {e}")
            results.append(False)
        print()

    passed = sum(results)
    total = len(results)
    print(f"=== {passed}/{total} pass ===")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
