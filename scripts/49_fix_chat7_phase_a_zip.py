# -*- coding: utf-8 -*-
"""
49_fix_chat7_phase_a_zip.py — رفع mis-placement اسکریپت ۴۳ برای zip چت ۷

این اسکریپت ۳ کار را انجام می‌دهد:
  ۱. ۵ فایل .md misplaced را از root به docs/ منتقل می‌کند
  ۲. اسکریپت‌های 47, 47b, 48, 48b, 48c را از zip به scripts/ استخراج می‌کند
  ۳. سند_جامع_v2_8.md (که در zip نام Persian دارد) را با fix encoding به docs/ منتقل می‌کند

استفاده (از ریشه پروژه):
  python scripts\\49_fix_chat7_phase_a_zip.py
"""
from __future__ import annotations

import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path.cwd()
ZIP = ROOT / "CHAT7_PHASE_A_atomic_update.zip"
SCRIPTS = ROOT / "scripts"
DOCS = ROOT / "docs"


def main() -> int:
    if not ZIP.exists():
        print(f"❌ zip پیدا نشد: {ZIP}")
        return 1

    SCRIPTS.mkdir(exist_ok=True)
    DOCS.mkdir(exist_ok=True)

    # 1) Move misplaced .md files: root → docs/
    misplaced = [
        "CHAT_LOG.md",
        "CLAUDE_CHECKLIST.md",
        "PROJECT_GOVERNANCE.md",
        "SESSION_STATUS.md",
        "TASK_BACKLOG.md",
    ]
    for fname in misplaced:
        src = ROOT / fname
        dst = DOCS / fname
        if src.exists():
            if dst.exists():
                dst.unlink()
            shutil.move(str(src), str(dst))
            print(f"  ✓ moved: ./{fname} → docs/{fname}")

    # 2) Extract scripts/ and Persian-named docs/ file from zip
    with zipfile.ZipFile(ZIP) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue

            # Fix encoding: CP437 → UTF-8 if no UTF-8 flag
            if info.flag_bits & 0x800:
                name = info.filename
            else:
                try:
                    name = info.filename.encode("cp437").decode("utf-8")
                except (UnicodeDecodeError, UnicodeEncodeError):
                    name = info.filename

            # Decide target
            if name.startswith("scripts/"):
                target = SCRIPTS / Path(name).name
            elif name.startswith("docs/") and ("v2_8" in name or "2_8" in name):
                target = DOCS / "سند_جامع_v2_8.md"
            else:
                continue

            with zf.open(info) as s, open(target, "wb") as d:
                shutil.copyfileobj(s, d)
            print(f"  ✓ extracted: {target.relative_to(ROOT)}")

    print()
    print("✅ Recovery تمام شد.")
    print()
    print("📌 گام بعدی:")
    print("   python scripts\\47b_test_doc_v28.py")
    print("   python scripts\\48b_test_governance_update.py")
    print("   del CHAT7_PHASE_A_atomic_update.zip")
    print("   git add docs/ scripts/")
    print('   git commit -m "docs(governance): integrate rules #23-#32 + bump سند_جامع to v2.8"')
    return 0


if __name__ == "__main__":
    sys.exit(main())
