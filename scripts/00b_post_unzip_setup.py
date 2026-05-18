# -*- coding: utf-8 -*-
"""
اسکریپت 00b — Post-Unzip Auto-Setup (راه‌اندازی خودکار بعد از باز کردن zip)
================================================================
این اسکریپت idempotent است — اجرای مجدد بدون عوارض جانبی.

🎯 هدف: بعد از باز کردن zip در سیستم جدید، یک دستور کل پروژه را آماده کند.

🔄 ترتیب اجرا (طبق درس‌های Session 6):
  1) چک backend\venv\ → اگر نبود: ساخت venv + pip install
     - اگر pip timeout داد → سوییچ به mirror ایرانی
  2) چک backend\trading.db → اگر نبود: alembic + seed (14 → 17 → 19)
  3) چک frontend\node_modules\ → اگر نبود: npm install
     - اگر npm timeout داد → سوییچ به registry.npmmirror.com

📋 پیش‌نیاز:
  - Python 3.11+ نصب شده
  - Node.js 22 LTS نصب شده
  - این اسکریپت در tab بدون venv فعال اجرا شود

استفاده:
    cd /d D:\\Projects\\trading-system
    python scripts\\00b_post_unzip_setup.py
================================================================
"""

import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
DATA_DIR = PROJECT_ROOT / "data" / "excel_imports"

# Paths مهم
VENV_DIR = BACKEND_DIR / "venv"
VENV_PYTHON = VENV_DIR / "Scripts" / "python.exe"  # Windows
VENV_PIP = VENV_DIR / "Scripts" / "pip.exe"
VENV_ACTIVATE = VENV_DIR / "Scripts" / "activate.bat"
DB_FILE = BACKEND_DIR / "trading.db"
NODE_MODULES = FRONTEND_DIR / "node_modules"
REQUIREMENTS = BACKEND_DIR / "requirements.txt"
EXCEL_FILE = DATA_DIR / "btcusdt-daily-20220426.xlsx"

# Mirror های جایگزین ایران
PIP_MIRROR_IRAN = "https://mirror-pypi.runflare.com/simple"
NPM_MIRROR_CHINA = "https://registry.npmmirror.com/"


def header(msg: str):
    print()
    print("=" * 68)
    print(f" {msg}")
    print("=" * 68)


def step(num: str, msg: str):
    print()
    print(f"━━━ [{num}] {msg} ━━━")


def run(cmd, cwd=None, env=None, check=True, capture=False):
    """اجرای دستور با shell=True (Windows-friendly)."""
    if isinstance(cmd, list):
        cmd_str = " ".join(cmd)
    else:
        cmd_str = cmd
    print(f"  > {cmd_str}")
    result = subprocess.run(
        cmd_str,
        cwd=str(cwd) if cwd else None,
        env=env,
        shell=True,
        capture_output=capture,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if check and result.returncode != 0:
        print(f"  ❌ exit code: {result.returncode}")
        if capture and result.stderr:
            print(result.stderr[-1000:])
        return False
    return True if not capture else result


def check_url(url: str, timeout: int = 5) -> bool:
    """چک می‌کند آیا URL در دسترس است."""
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout):
            return True
    except (urllib.error.URLError, OSError, TimeoutError):
        return False


# ============================================================
# مرحله ۱: Backend venv + pip install
# ============================================================
def setup_backend_venv() -> bool:
    if VENV_PYTHON.exists():
        print(f"  ✓ venv موجود است: {VENV_DIR}")
        return True

    step("1.1", "ساخت Python venv")
    if not run(f'python -m venv "{VENV_DIR}"'):
        print("  ❌ ساخت venv شکست خورد. آیا Python 3.11+ نصب است؟")
        return False
    print(f"  ✓ venv ساخته شد: {VENV_DIR}")

    step("1.2", "upgrade pip")
    run(f'"{VENV_PYTHON}" -m pip install --upgrade pip', check=False)

    step("1.3", "نصب requirements (تست با pypi رسمی)")
    pip_ok = run(
        f'"{VENV_PYTHON}" -m pip install -r "{REQUIREMENTS}" --timeout=30',
        check=False,
    )

    if not pip_ok:
        print()
        print("  ⚠ نصب از pypi.org شکست خورد (احتمالاً فیلتر در ایران)")
        print(f"  ↻ سوییچ به mirror: {PIP_MIRROR_IRAN}")
        step("1.3.bis", f"نصب از {PIP_MIRROR_IRAN}")
        if not run(
            f'"{VENV_PYTHON}" -m pip install -r "{REQUIREMENTS}" '
            f"--index-url {PIP_MIRROR_IRAN} --timeout=60"
        ):
            print("  ❌ نصب pip حتی با mirror هم شکست خورد.")
            return False

    print(f"  ✓ پکیج‌های Python نصب شدند.")
    return True


# ============================================================
# مرحله ۲: Backend DB + Seed
# ============================================================
def setup_backend_db() -> bool:
    if DB_FILE.exists():
        print(f"  ✓ trading.db موجود است")
        return True

    step("2.1", "alembic upgrade head — ساخت schema")
    if not run(
        f'"{VENV_PYTHON}" -m alembic upgrade head',
        cwd=BACKEND_DIR,
    ):
        print("  ❌ alembic شکست خورد.")
        return False

    step("2.2", "seed admin + Exchange (اسکریپت ۱۴)")
    if not run(
        f'"{VENV_PYTHON}" "{SCRIPT_DIR / "14_seed_data.py"}"',
    ):
        print("  ❌ seed 14 شکست خورد.")
        return False

    step("2.3", "seed نماد BTC/USDT (اسکریپت ۱۷)")
    if not run(
        f'"{VENV_PYTHON}" "{SCRIPT_DIR / "17_seed_btc_mapping.py"}"',
    ):
        print("  ❌ seed 17 شکست خورد.")
        return False

    step("2.4", "import OHLCV از Excel (اسکریپت ۱۹)")
    if not EXCEL_FILE.exists():
        print(f"  ❌ فایل Excel نیست: {EXCEL_FILE}")
        return False
    if not run(
        f'"{VENV_PYTHON}" "{SCRIPT_DIR / "19_test_excel_reader.py"}" "{EXCEL_FILE}"',
    ):
        print("  ❌ import OHLCV شکست خورد.")
        return False

    print(f"  ✓ DB کاملاً seed شد (admin + Excel + BTC/USDT + 1714 کندل)")
    return True


# ============================================================
# مرحله ۳: Frontend node_modules
# ============================================================
def setup_frontend() -> bool:
    if NODE_MODULES.exists() and (NODE_MODULES / ".bin").exists():
        print(f"  ✓ node_modules موجود است")
        return True

    step("3.1", "تست connectivity registry.npmjs.org")
    npm_official_ok = check_url("https://registry.npmjs.org/", timeout=5)
    if npm_official_ok:
        print("  ✓ registry.npmjs.org پاسخ می‌دهد")
    else:
        print(f"  ⚠ registry.npmjs.org پاسخ نداد → سوییچ به {NPM_MIRROR_CHINA}")
        if not run(f"npm config set registry {NPM_MIRROR_CHINA}"):
            print("  ❌ تنظیم mirror شکست خورد.")
            return False

    step("3.2", "npm install (~۲-۵ دقیقه با mirror)")
    if not run(
        "npm install --no-audit --no-fund --loglevel=http",
        cwd=FRONTEND_DIR,
    ):
        # اگر با mirror هم شکست خورد و قبلاً به mirror نرفته بودیم، الان برو
        if npm_official_ok:
            print()
            print(f"  ⚠ npm install با pypi رسمی شکست → تست با {NPM_MIRROR_CHINA}")
            run(f"npm config set registry {NPM_MIRROR_CHINA}")
            if not run(
                "npm install --no-audit --no-fund --loglevel=http",
                cwd=FRONTEND_DIR,
            ):
                return False
        else:
            return False

    print(f"  ✓ node_modules نصب شد")
    return True


# ============================================================
# main
# ============================================================
def main() -> int:
    header("00b — Post-Unzip Auto-Setup")
    print(f"  ریشه پروژه: {PROJECT_ROOT}")
    print()

    # تشخیص اولیه
    print("  وضعیت اولیه:")
    print(f"    backend/venv         : {'✅' if VENV_PYTHON.exists() else '❌ غایب'}")
    print(f"    backend/trading.db   : {'✅' if DB_FILE.exists() else '❌ غایب'}")
    print(f"    frontend/node_modules: {'✅' if NODE_MODULES.exists() else '❌ غایب'}")

    if not REQUIREMENTS.exists():
        print(f"\n  ❌ requirements.txt پیدا نشد: {REQUIREMENTS}")
        return 1

    # مرحله ۱
    header("مرحله ۱/۳ — Backend Python venv")
    if not setup_backend_venv():
        return 1

    # مرحله ۲
    header("مرحله ۲/۳ — Backend DB + Seed (admin + Excel + BTC + 1714 کندل)")
    if not setup_backend_db():
        return 1

    # مرحله ۳
    header("مرحله ۳/۳ — Frontend node_modules")
    if not setup_frontend():
        return 1

    # خلاصه نهایی
    header("✅ Post-Unzip Setup کاملاً موفق")
    print()
    print("  حالا می‌توانی سه tab را راه‌اندازی کنی:")
    print()
    print("  🟦 tab «1 backend»:")
    print(f"     cd /d {BACKEND_DIR}")
    print(f"     venv\\Scripts\\activate")
    print(f"     uvicorn main:app --reload")
    print()
    print("  🟧 tab «3 frontend»:")
    print(f"     cd /d {FRONTEND_DIR}")
    print(f"     npm run dev")
    print()
    print("  🌐 مرورگر:")
    print(f"     http://localhost:5173/  →  admin/1")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
