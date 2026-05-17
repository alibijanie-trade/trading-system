# -*- coding: utf-8 -*-
"""
اسکریپت ۴۳ v2 — Sync فایل‌های منبع از zip Claude به پروژه local
================================================================
v2 (2026-05-17): تشخیص و skip فایل‌های با نام Unicode خراب در zip

این اسکریپت idempotent و امن است:
  - zip را در پوشه موقت extract می‌کند
  - فایل‌ها را با نسخه local مقایسه می‌کند
  - گزارش دقیق می‌دهد: جدید/تغییریافته/یکسان/protected/mojibake
  - در --apply با backup خودکار، فایل‌ها را sync می‌کند
  - venv/node_modules/db/logs/.git/.env را هرگز touch نمی‌کند
  - فایل‌های با نام UTF-8 خراب را skip می‌کند

نحوه استفاده:
    python scripts\\43_sync_from_zip.py "D:\\Projects\\trading-system06.zip"
    python scripts\\43_sync_from_zip.py "D:\\Projects\\trading-system06.zip" --apply
================================================================
"""

import argparse
import hashlib
import shutil
import sys
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

PROTECTED_PATTERNS = [
    "backend/venv",
    "backend/.env",
    "backend/trading.db",
    "backend/trading.db-journal",
    "backend/logs",
    "backend/__pycache__",
    "frontend/node_modules",
    "frontend/.env.local",
    "frontend/dist",
    "frontend/coverage",
    ".git",
    ".sync-backup",
    ".pytest_cache",
    "htmlcov",
    ".vscode",
    ".idea",
    ".DS_Store",
    "Thumbs.db",
]


def is_protected(rel_path: str) -> bool:
    rel_norm = rel_path.replace("\\", "/")
    for p in PROTECTED_PATTERNS:
        if rel_norm == p or rel_norm.startswith(p + "/"):
            return True
        if "/__pycache__/" in rel_norm or rel_norm.endswith("__pycache__"):
            return True
        if rel_norm.endswith(".pyc"):
            return True
    return False


def has_mojibake(s: str) -> bool:
    """تشخیص نام فایل با Unicode خراب (mojibake)."""
    suspicious_chars = "╪┘╔╫╬╝╪╗╫╨╔╕"
    if any(c in s for c in suspicious_chars):
        return True
    box_drawing = "┌┐└┘├┤┬┴┼─│║╔╗╚╝╠╣╦╩╬═"
    if any(c in s for c in box_drawing):
        return True
    # کاراکترهای latin-1 supplement که در نام‌های فارسی corrupt دیده می‌شوند
    mojibake_indicators = "‡˧¼ºª"
    if any(c in s for c in mojibake_indicators):
        return True
    return False


def file_hash(path: Path) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def compare_files(local: Path, source: Path) -> bool:
    if not local.exists():
        return False
    if local.stat().st_size != source.stat().st_size:
        return False
    return file_hash(local) == file_hash(source)


def main():
    parser = argparse.ArgumentParser(description="Sync source files from Claude zip")
    parser.add_argument("zip_path", help="مسیر کامل zip چت Claude")
    parser.add_argument("--apply", action="store_true", help="واقعا copy کن")
    args = parser.parse_args()

    zip_path = Path(args.zip_path)
    if not zip_path.exists():
        print(f"❌ zip یافت نشد: {zip_path}")
        return 1

    apply_mode = args.apply
    mode_label = "APPLY (واقعی)" if apply_mode else "DRY-RUN (فقط گزارش)"

    print("=" * 70)
    print(f"اسکریپت ۴۳ v2 — Sync from zip — حالت: {mode_label}")
    print("=" * 70)
    print(f"📦 zip:      {zip_path}")
    print(f"📂 پروژه:    {PROJECT_ROOT}")
    print(f"💾 حجم zip:  {zip_path.stat().st_size:,} bytes")
    print()

    with tempfile.TemporaryDirectory(prefix="sync_zip_") as tmp_dir:
        tmp_path = Path(tmp_dir)
        print(f"🔓 Extract در: {tmp_path}")
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(tmp_path)

        roots = [d for d in tmp_path.iterdir() if d.is_dir()]
        if not roots:
            print("❌ zip خالی است")
            return 1
        zip_root = roots[0]
        print(f"   root داخل zip: {zip_root.name}/")
        print()

        all_files = []
        mojibake_files = []

        for f in zip_root.rglob("*"):
            if f.is_file():
                rel = f.relative_to(zip_root).as_posix()
                if has_mojibake(rel):
                    mojibake_files.append((f, rel))
                else:
                    all_files.append((f, rel))

        total = len(all_files) + len(mojibake_files)
        print(f"📊 تعداد کل فایل در zip: {total}")
        if mojibake_files:
            print(f"   ⚠️  {len(mojibake_files)} فایل با نام Unicode خراب → skip می‌شوند")
        print()

        new_files = []
        changed_files = []
        same_files = []
        protected_files = []

        for src, rel in all_files:
            if is_protected(rel):
                protected_files.append(rel)
                continue

            local = PROJECT_ROOT / rel
            if not local.exists():
                new_files.append((src, rel))
            elif compare_files(local, src):
                same_files.append(rel)
            else:
                changed_files.append((src, rel))

        print("─" * 70)
        print(f"📋 گزارش تطبیق:")
        print("─" * 70)
        print(f"  🆕 جدید:           {len(new_files):4d} فایل")
        print(f"  ✏️  تغییر یافته:    {len(changed_files):4d} فایل")
        print(f"  ✓  یکسان:         {len(same_files):4d} فایل")
        print(f"  🛡️  محافظت‌شده:     {len(protected_files):4d} فایل")
        print(f"  ⚠️  mojibake:       {len(mojibake_files):4d} فایل (skip)")
        print()

        if mojibake_files:
            print("─" * 70)
            print(f"⚠️ فایل‌های Skip شده (نام Unicode خراب در zip):")
            print("─" * 70)
            for _, rel in sorted(mojibake_files, key=lambda x: x[1]):
                print(f"   ⊘ {rel}")
            print()
            print("   💡 این فایل‌ها معمولا نسخه‌های فارسی هستند که در پروژه شما")
            print("      با نام درست از قبل موجودند.")
            print()

        if new_files:
            print("─" * 70)
            print(f"🆕 فایل‌های جدید ({len(new_files)}):")
            print("─" * 70)
            for _, rel in sorted(new_files, key=lambda x: x[1]):
                print(f"   + {rel}")
            print()

        if changed_files:
            print("─" * 70)
            print(f"✏️ فایل‌های تغییر یافته ({len(changed_files)}):")
            print("─" * 70)
            for _, rel in sorted(changed_files, key=lambda x: x[1]):
                print(f"   ~ {rel}")
            print()

        if protected_files:
            print("─" * 70)
            print(f"🛡️ فایل‌های محافظت‌شده ({len(protected_files)}):")
            print("─" * 70)
            samples = sorted(set([
                p.split("/")[0] + ("/" + p.split("/")[1] if "/" in p else "")
                for p in protected_files
            ]))[:15]
            for s in samples:
                print(f"   🛡 {s}/...")
            print()

        if not apply_mode:
            print("=" * 70)
            print("✅ Dry-run تمام شد. هیچ فایلی تغییر نکرد.")
            print("=" * 70)
            print()
            print("📌 برای اعمال واقعی، این دستور را اجرا کنید:")
            print(f'   python scripts\\43_sync_from_zip.py "{zip_path}" --apply')
            return 0

        if not new_files and not changed_files:
            print("=" * 70)
            print("✅ هیچ تغییری لازم نیست — همه فایل‌ها sync هستند.")
            print("=" * 70)
            return 0

        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        backup_dir = PROJECT_ROOT / ".sync-backup" / timestamp
        backup_dir.mkdir(parents=True, exist_ok=True)
        print("=" * 70)
        print(f"🛡️ Backup در: {backup_dir.relative_to(PROJECT_ROOT)}")
        print("=" * 70)
        print()

        for src, rel in changed_files:
            local = PROJECT_ROOT / rel
            bak_path = backup_dir / rel
            bak_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(local, bak_path)
            shutil.copy2(src, local)
            print(f"   ✏️ updated: {rel}")

        for src, rel in new_files:
            local = PROJECT_ROOT / rel
            local.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, local)
            print(f"   🆕 created: {rel}")

        print()
        print("=" * 70)
        print(f"✅ Sync تمام شد.")
        print(f"   {len(changed_files)} فایل به‌روز شد")
        print(f"   {len(new_files)} فایل جدید ساخته شد")
        if mojibake_files:
            print(f"   ⚠️  {len(mojibake_files)} فایل mojibake skip شد")
        print(f"   Backup در: .sync-backup\\{timestamp}\\")
        print("=" * 70)
        print()
        print("📌 گام بعدی:")
        print("   git status")
        print("   git diff")
        print("   git add -A")
        print('   git commit -m "feat(tier2): T2.01-T2.04 + Tier 2 docs"')

    return 0


if __name__ == "__main__":
    sys.exit(main())