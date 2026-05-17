# -*- coding: utf-8 -*-
"""
اسکریپت ۱۶b — اصلاح Migration row_index
بازنویسی فایل add_row_index_to_ohlcv با محتوای صحیح
(حذف تغییرات اشتباه روی ایندکس‌های AuditLog)
"""

import re
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
VERSIONS_DIR = BACKEND_DIR / "migrations" / "versions"


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
    header("اسکریپت ۱۶b — اصلاح Migration row_index")

    # پیدا کردن فایل migration
    candidates = list(VERSIONS_DIR.glob("*_add_row_index_to_ohlcv.py"))
    if not candidates:
        err("فایل migration add_row_index_to_ohlcv پیدا نشد.")
        return 1

    migration_file = max(candidates, key=lambda p: p.stat().st_mtime)
    info(f"فایل: {migration_file.name}")

    content = migration_file.read_text(encoding="utf-8")

    # استخراج revision id ها
    rev_match = re.search(r"revision:\s*str\s*=\s*['\"]([^'\"]+)['\"]", content)
    down_match = re.search(r"down_revision:[^=]*=\s*['\"]([^'\"]+)['\"]", content)
    date_match = re.search(r"Create Date:\s*(.+)", content)

    if not rev_match or not down_match:
        err("نتوانست revision id ها را از فایل استخراج کند.")
        return 1

    revision = rev_match.group(1)
    down_revision = down_match.group(1)
    create_date = date_match.group(1).strip() if date_match else "auto"

    info(f"revision      = {revision}")
    info(f"down_revision = {down_revision}")
    print()

    # backup
    backup = migration_file.with_suffix(".py.bak")
    backup.write_text(content, encoding="utf-8")
    info(f"بک‌آپ: {backup.name}")

    # محتوای جدید فقط با row_index
    new_content = f'''"""add_row_index_to_ohlcv

Revision ID: {revision}
Revises: {down_revision}
Create Date: {create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '{revision}'
down_revision: Union[str, None] = '{down_revision}'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema — only add row_index to OhlcvData."""
    with op.batch_alter_table('OhlcvData', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('row_index', sa.Integer(), nullable=False, server_default='0')
        )


def downgrade() -> None:
    """Downgrade schema — remove row_index from OhlcvData."""
    with op.batch_alter_table('OhlcvData', schema=None) as batch_op:
        batch_op.drop_column('row_index')
'''

    migration_file.write_text(new_content, encoding="utf-8")
    success(f"فایل migration بازنویسی شد")
    print()

    header("گام بعدی")

    print(f"{BOLD}📍 Tab: 2 scripts{RESET}\n")
    print(f"  {BOLD}alembic upgrade head{RESET}\n")
    info("خروجی: 'Running upgrade {} -> {}, add_row_index_to_ohlcv'".format(down_revision, revision))
    print()

    print(f"{BOLD}📍 Tab: 2 scripts{RESET} — تأیید ستون row_index\n")
    print(f"  {BOLD}python -c \"import sqlite3; c=sqlite3.connect('trading.db'); [print(r) for r in c.execute('PRAGMA table_info(OhlcvData)')]\"{RESET}\n")
    info("باید یک ردیف row_index در خروجی دیده شود")
    print()

    print(f"{BOLD}📍 Tab: 2 scripts{RESET} — تأیید ایندکس‌های DESC سالم هستند\n")
    print(f"  {BOLD}python -c \"import sqlite3; c=sqlite3.connect('trading.db'); [print(n,'->',s) for n,s in c.execute(\\\"SELECT name,sql FROM sqlite_master WHERE name LIKE 'idx_audit%'\\\")]\"{RESET}\n")
    info("باید هر دو ایندکس همچنان شامل 'created_at DESC' باشند")
    print()

    print(f"{BOLD}📍 Tab: 1 backend{RESET}\n")
    print(f"  {BOLD}cd /d D:\\Projects\\trading-system\\backend{RESET}")
    print(f"  {BOLD}venv\\Scripts\\activate{RESET}")
    print(f"  {BOLD}uvicorn main:app --reload{RESET}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
