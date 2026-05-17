# -*- coding: utf-8 -*-
"""
اسکریپت 00 — پاک‌سازی پوشه پروژه قبل از zip و انتقال به چت بعد
================================================================
این اسکریپت idempotent است — قابل اجرای چندباره بدون خطا.

🔴 پیش‌نیاز قبل از اجرا (مهم!):
  🟦 tab «1 backend»   → Ctrl+C  (توقف uvicorn — وگرنه فایل‌های log قفل می‌مانند)
  🟧 tab «3 frontend»  → Ctrl+C  (توقف vite — وگرنه node_modules قفل می‌ماند)
  🟩 tab «2 scripts»   → اگر در venv هستی، تب را ببند و یک تب جدید باز کن
                         (چون 'deactivate' در Windows همیشه در دسترس نیست)

اجرا (در tab بدون venv):
    cd /d D:\\Projects\\trading-system
    python scripts\\00_cleanup_for_zip.py

موارد حذف می‌شود:
  دایرکتوری‌ها:
    - backend\\venv\\
    - frontend\\node_modules\\
    - backend\\.pytest_cache\\
    - frontend\\dist\\
    - frontend\\.vite\\
    - تمام __pycache__\\ در کل پروژه (recursive)

  فایل‌ها:
    - backend\\trading.db
    - backend\\trading.db-wal
    - backend\\trading.db-shm
    - backend\\logs\\*.log
    - **/*.pyc (همه)

موارد حفظ:
  - backend\\app\\, backend\\main.py, backend\\migrations\\, backend\\.env
  - frontend\\src\\, frontend\\package.json, frontend\\package-lock.json, frontend\\.env
  - scripts\\, docs\\, data\\, .gitignore, CHANGELOG.md, README.md
  - .git\\ (اختیاری — اگر می‌خواهی حذف شود، خط مربوطه را uncomment کن)
================================================================
"""

import shutil
import sys
from pathlib import Path

# ============================================================
# تعیین مسیرها
# ============================================================
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent


# ============================================================
# توابع کمکی
# ============================================================
def safe_rmtree(path: Path) -> str:
    """حذف یک دایرکتوری — بدون exception اگر وجود ندارد."""
    if not path.exists():
        return "skip"
    try:
        shutil.rmtree(path)
        return "ok"
    except OSError as e:
        return f"error: {e}"


def safe_unlink(path: Path) -> str:
    """حذف یک فایل — بدون exception اگر وجود ندارد."""
    if not path.exists():
        return "skip"
    try:
        path.unlink()
        return "ok"
    except OSError as e:
        return f"error: {e}"


def remove_pycache_recursive(root: Path) -> tuple[int, int]:
    """حذف همه __pycache__ زیرمجموعه root. خروجی: (موفق, ناموفق)."""
    ok = 0
    fail = 0
    for pycache in root.rglob("__pycache__"):
        if not pycache.is_dir():
            continue
        try:
            shutil.rmtree(pycache)
            ok += 1
        except OSError:
            fail += 1
    return ok, fail


def remove_pyc_recursive(root: Path) -> int:
    """حذف همه فایل‌های .pyc منفرد."""
    count = 0
    for pyc in root.rglob("*.pyc"):
        try:
            pyc.unlink()
            count += 1
        except OSError:
            pass
    return count


def remove_logs(logs_dir: Path) -> tuple[int, int]:
    """حذف *.log در یک پوشه. خروجی: (موفق, ناموفق)."""
    if not logs_dir.exists():
        return 0, 0
    ok = 0
    fail = 0
    for log in logs_dir.glob("*.log"):
        try:
            log.unlink()
            ok += 1
        except OSError:
            fail += 1
    return ok, fail


# ============================================================
# اجرا
# ============================================================
def main() -> None:
    print("=" * 68)
    print("اسکریپت 00 — پاک‌سازی پوشه پروژه قبل از zip")
    print("=" * 68)
    print(f"  ریشه: {PROJECT_ROOT}")
    print()

    if not PROJECT_ROOT.exists():
        print(f"[ERROR] ریشه پروژه پیدا نشد: {PROJECT_ROOT}")
        sys.exit(1)

    locked_warnings: list[str] = []

    # ---- دایرکتوری‌های حذفی ----
    print("🗂  دایرکتوری‌ها:")
    dirs = [
        PROJECT_ROOT / "backend" / "venv",
        PROJECT_ROOT / "frontend" / "node_modules",
        PROJECT_ROOT / "backend" / ".pytest_cache",
        PROJECT_ROOT / "frontend" / "dist",
        PROJECT_ROOT / "frontend" / ".vite",
        # خط زیر را uncomment کن اگر می‌خواهی .git هم حذف شود (~۲۰ MB)
        # PROJECT_ROOT / ".git",
    ]
    for d in dirs:
        rel = d.relative_to(PROJECT_ROOT)
        status = safe_rmtree(d)
        if status == "ok":
            print(f"  ✓ حذف شد: {rel}")
        elif status == "skip":
            print(f"  - وجود نداشت: {rel}")
        else:
            print(f"  ✗ {rel}: {status}")
            locked_warnings.append(str(rel))

    # ---- فایل‌های DB ----
    print()
    print("🗄  فایل‌های DB:")
    db_files = [
        PROJECT_ROOT / "backend" / "trading.db",
        PROJECT_ROOT / "backend" / "trading.db-wal",
        PROJECT_ROOT / "backend" / "trading.db-shm",
    ]
    for f in db_files:
        rel = f.relative_to(PROJECT_ROOT)
        status = safe_unlink(f)
        if status == "ok":
            print(f"  ✓ حذف شد: {rel}")
        elif status == "skip":
            print(f"  - وجود نداشت: {rel}")
        else:
            print(f"  ✗ {rel}: {status}")
            locked_warnings.append(str(rel))

    # ---- لاگ‌ها ----
    print()
    print("📜 فایل‌های log:")
    log_ok, log_fail = remove_logs(PROJECT_ROOT / "backend" / "logs")
    print(f"  ✓ حذف {log_ok} فایل")
    if log_fail:
        print(f"  ✗ {log_fail} فایل قفل بود (uvicorn هنوز روشن؟)")
        locked_warnings.append(f"backend/logs/ ({log_fail} log قفل)")

    # ---- __pycache__ ----
    print()
    print("🐍 پوشه‌های __pycache__:")
    pyc_ok, pyc_fail = remove_pycache_recursive(PROJECT_ROOT)
    print(f"  ✓ حذف {pyc_ok} پوشه")
    if pyc_fail:
        print(f"  ✗ {pyc_fail} پوشه قفل بود")

    # ---- *.pyc منفرد ----
    pyc_count = remove_pyc_recursive(PROJECT_ROOT)
    if pyc_count:
        print(f"  ✓ حذف {pyc_count} فایل .pyc منفرد")

    # ---- خلاصه ----
    print()
    print("=" * 68)
    if locked_warnings:
        print("⚠ پاک‌سازی با هشدار تمام شد.")
        print("  موارد قفل (سرورها هنوز روشن؟):")
        for w in locked_warnings:
            print(f"    - {w}")
        print()
        print("  راه‌حل: 🟦 tab «1 backend» و 🟧 tab «3 frontend» → Ctrl+C")
        print("         سپس این اسکریپت را دوباره اجرا کن.")
    else:
        print("✅ پاک‌سازی کامل بدون خطا تمام شد.")
    print("=" * 68)
    print()
    print("مرحله بعد:")
    print("  راست‌کلیک روی پوشه trading-system")
    print("  → Send to → Compressed (zipped) folder")
    print("  → پیوست trading-system.zip در چت بعد")


if __name__ == "__main__":
    main()
