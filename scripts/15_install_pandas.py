# -*- coding: utf-8 -*-
"""
اسکریپت ۱۵ — نصب pandas و openpyxl (شروع زیرگام ۶)
"""

import sys
from pathlib import Path

try:
    from colorama import init as _colorama_init
    from colorama import Fore, Style
    _colorama_init(autoreset=True)
    GREEN, RED, YELLOW, CYAN, BOLD, RESET = (
        Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.CYAN, Style.BRIGHT, Style.RESET_ALL,
    )
except ImportError:
    GREEN = RED = YELLOW = CYAN = BOLD = RESET = ""


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
REQUIREMENTS = BACKEND_DIR / "requirements.txt"


NEW_REQUIREMENTS = """# ============================================================
# requirements.txt — سامانه هوشمند ترید
# نسخه: v0.1.3 (گام ۶ فاز ۰ - افزودن pandas/openpyxl)
# ============================================================

# --- Web Framework ---
fastapi==0.111.0
uvicorn[standard]==0.29.0

# --- Database & ORM ---
sqlalchemy==2.0.30
aiosqlite==0.20.0
alembic==1.13.1

# --- Validation & Settings ---
pydantic==2.7.1
pydantic-settings==2.2.1

# --- Authentication & Security ---
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
cryptography==42.0.7

# --- Environment ---
python-dotenv==1.0.1
colorama==0.4.6    # Windows ANSI colors support

# --- HTTP Client ---
httpx==0.27.0

# --- Data Processing (فاز ۶ - Excel Reader) ---
pandas==2.2.2
openpyxl==3.1.2

# ============================================================
# نکته: ccxt، websockets، python-telegram-bot
# در فازهای آینده طبق نیاز اضافه خواهند شد.
# ============================================================
"""


def info(msg): print(f"{CYAN}ℹ {msg}{RESET}")
def success(msg): print(f"{GREEN}✅ {msg}{RESET}")
def warn(msg): print(f"{YELLOW}⚠ {msg}{RESET}")
def err(msg): print(f"{RED}❌ {msg}{RESET}")

def header(msg):
    line = "=" * 60
    print(f"\n{BOLD}{CYAN}{line}{RESET}")
    print(f"{BOLD}{CYAN}{msg}{RESET}")
    print(f"{BOLD}{CYAN}{line}{RESET}\n")


def main() -> int:
    header("اسکریپت ۱۵ — نصب pandas و openpyxl")

    if not REQUIREMENTS.exists():
        err(f"requirements.txt پیدا نشد: {REQUIREMENTS}")
        return 1

    current = REQUIREMENTS.read_text(encoding="utf-8")

    if current == NEW_REQUIREMENTS:
        info("requirements.txt از قبل به‌روز است.")
    else:
        backup = REQUIREMENTS.with_suffix(".txt.bak")
        backup.write_text(current, encoding="utf-8")
        REQUIREMENTS.write_text(NEW_REQUIREMENTS, encoding="utf-8")
        success("requirements.txt به‌روز شد")
        info(f"بک‌آپ: {backup.name}")

    print()
    header("گام بعدی")

    print(f"{BOLD}📍 Tab: 2 scripts{RESET}\n")
    print(f"  {BOLD}pip install pandas==2.2.2 openpyxl==3.1.2{RESET}\n")
    info("خروجی: 'Successfully installed pandas-2.2.2 openpyxl-3.1.2 ...'")
    print()

    print(f"{BOLD}📍 Tab: 2 scripts{RESET} — تست ایمپورت\n")
    print(f"  {BOLD}python -c \"import pandas; import openpyxl; print('OK', pandas.__version__, openpyxl.__version__)\"{RESET}\n")
    info("خروجی: 'OK 2.2.2 3.1.2'")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
