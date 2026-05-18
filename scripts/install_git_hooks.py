# -*- coding: utf-8 -*-
"""
install_git_hooks.py — نصب pre-commit hooks

این اسکریپت:
  ۱. تأیید نصب pre-commit framework
  ۲. اجرای `pre-commit install` در ریشه پروژه
  ۳. تست با `pre-commit run --all-files` (اختیاری)

نکته: نصب pre-commit framework قبلاً در requirements.txt آمده.
ابتدا: pip install -r backend/requirements.txt

استفاده:
  python scripts\install_git_hooks.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    # تأیید pre-commit
    if shutil.which("pre-commit") is None:
        print("❌ pre-commit نصب نیست.")
        print("📌 ابتدا اجرا کنید:")
        print("   🟦 tab «1 backend»")
        print("     cd backend")
        print("     venv\\Scripts\\activate")
        print(
            "     pip install pre-commit==3.7.1 black==24.4.2 isort==5.13.2 -i https://mirrors.aliyun.com/pypi/simple/"
        )
        return 1

    # تأیید .pre-commit-config.yaml
    config = ROOT / ".pre-commit-config.yaml"
    if not config.exists():
        print(f"❌ {config} پیدا نشد. اول اسکریپت 54 را اجرا کنید.")
        return 1

    # نصب
    print("📦 نصب pre-commit hook در .git/hooks/...")
    r = subprocess.run(["pre-commit", "install"], cwd=ROOT)
    if r.returncode != 0:
        print("❌ نصب ناموفق")
        return r.returncode

    print()
    print("✅ Pre-commit hooks نصب شد.")
    print()
    print("📌 تست:")
    print("   pre-commit run --all-files")
    print()
    print("📌 bypass در اضطرار:")
    print('   git commit --no-verify -m "[skip-hooks: REASON] ..."')
    return 0


if __name__ == "__main__":
    sys.exit(main())
