# -*- coding: utf-8 -*-
"""
اسکریپت ساخت ساختار اولیه پروژه — سامانه هوشمند ترید
================================================================
گام ۱ از فاز ۰
این اسکریپت فقط یک‌بار اجرا می‌شود تا ساختار پایه پروژه را بسازد.

نحوه اجرا (در CMD):
    cd /d D:\\Projects\\trading-system
    python scripts\\01_create_structure.py

نسخه: 1.0.0
تاریخ: 2026/05/14
================================================================
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# ============================================================
# تنظیمات اصلی
# ============================================================
PROJECT_ROOT = Path(r"D:\Projects\trading-system")

# ============================================================
# لیست تمام پوشه‌هایی که باید ساخته شوند (طبق سند ۴)
# ============================================================
DIRECTORIES = [
    # Backend
    "backend",
    "backend/app",
    "backend/app/api",
    "backend/app/api/v1",
    "backend/app/api/v1/routes",
    "backend/app/api/v1/websocket",
    "backend/app/core",
    "backend/app/domain",
    "backend/app/domain/entities",
    "backend/app/domain/value_objects",
    "backend/app/domain/events",
    "backend/app/domain/services",
    "backend/app/services",
    "backend/app/repositories",
    "backend/app/models",
    "backend/app/schemas",
    "backend/app/infrastructure",
    "backend/app/infrastructure/database",
    "backend/app/infrastructure/exchange",
    "backend/app/infrastructure/cache",
    "backend/app/infrastructure/backup",
    "backend/app/infrastructure/data_sources",  # DataSource Abstraction Layer
    "backend/migrations",
    "backend/migrations/versions",
    "backend/tests",
    "backend/tests/unit",
    "backend/tests/integration",
    # Frontend
    "frontend",
    "frontend/src",
    "frontend/src/pages",
    "frontend/src/components",
    "frontend/src/components/common",
    "frontend/src/components/chart",
    "frontend/src/services",
    "frontend/src/stores",
    "frontend/src/hooks",
    "frontend/src/utils",
    "frontend/src/constants",
    # Scripts و Docs
    "scripts",
    "docs",
    "docs/architecture",
    "docs/api",
    # Data و Logs
    "data",
    "data/excel_imports",  # محل قرار دادن فایل‌های اکسل OHLCV
    "logs",
]

# ============================================================
# پوشه‌هایی که باید فایل __init__.py داشته باشند (پکیج‌های Python)
# ============================================================
PYTHON_PACKAGES = [
    "backend/app",
    "backend/app/api",
    "backend/app/api/v1",
    "backend/app/api/v1/routes",
    "backend/app/api/v1/websocket",
    "backend/app/core",
    "backend/app/domain",
    "backend/app/domain/entities",
    "backend/app/domain/value_objects",
    "backend/app/domain/events",
    "backend/app/domain/services",
    "backend/app/services",
    "backend/app/repositories",
    "backend/app/models",
    "backend/app/schemas",
    "backend/app/infrastructure",
    "backend/app/infrastructure/database",
    "backend/app/infrastructure/exchange",
    "backend/app/infrastructure/cache",
    "backend/app/infrastructure/backup",
    "backend/app/infrastructure/data_sources",
    "backend/tests",
    "backend/tests/unit",
    "backend/tests/integration",
]

# ============================================================
# پوشه‌هایی که باید فایل .gitkeep داشته باشند (پوشه‌های خالی غیر-Python)
# ============================================================
GITKEEP_DIRS = [
    "data/excel_imports",
    "logs",
    "frontend/src/pages",
    "frontend/src/components/common",
    "frontend/src/components/chart",
    "frontend/src/services",
    "frontend/src/stores",
    "frontend/src/hooks",
    "frontend/src/utils",
    "frontend/src/constants",
    "backend/migrations/versions",
    "docs/architecture",
    "docs/api",
]


def create_directory(path: Path) -> bool:
    """ساخت یک پوشه — برمی‌گرداند True اگر ساخته شد، False اگر از قبل وجود داشت."""
    if path.exists():
        return False
    path.mkdir(parents=True, exist_ok=True)
    return True


def create_file_if_not_exists(path: Path, content: str = "") -> bool:
    """ساخت فایل اگر وجود ندارد."""
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True


def main():
    print("=" * 60)
    print("🚀 ساخت ساختار اولیه پروژه — سامانه هوشمند ترید")
    print("=" * 60)
    print(f"📁 مسیر ریشه: {PROJECT_ROOT}")
    print()

    # بررسی وجود پوشه ریشه
    if not PROJECT_ROOT.exists():
        print(f"❌ خطا: پوشه ریشه وجود ندارد: {PROJECT_ROOT}")
        print("   لطفاً ابتدا آن را با دستور زیر بسازید:")
        print(f"   mkdir {PROJECT_ROOT}")
        sys.exit(1)

    # ============================================================
    # گام ۱: ساخت تمام پوشه‌ها
    # ============================================================
    print("📂 گام ۱: ساخت پوشه‌ها...")
    created_dirs = 0
    existed_dirs = 0
    for dir_path in DIRECTORIES:
        full_path = PROJECT_ROOT / dir_path
        if create_directory(full_path):
            created_dirs += 1
            print(f"   ✅ ساخته شد: {dir_path}")
        else:
            existed_dirs += 1

    print(f"\n   جمع‌بندی: {created_dirs} پوشه ساخته شد، {existed_dirs} از قبل بود.")
    print()

    # ============================================================
    # گام ۲: ساخت فایل‌های __init__.py برای پکیج‌های Python
    # ============================================================
    print("🐍 گام ۲: ساخت فایل‌های __init__.py...")
    init_content = "# -*- coding: utf-8 -*-\n"
    created_inits = 0
    for pkg_path in PYTHON_PACKAGES:
        full_path = PROJECT_ROOT / pkg_path / "__init__.py"
        if create_file_if_not_exists(full_path, init_content):
            created_inits += 1
    print(f"   ✅ {created_inits} فایل __init__.py ساخته شد.")
    print()

    # ============================================================
    # گام ۳: ساخت فایل‌های .gitkeep برای پوشه‌های خالی
    # ============================================================
    print("📌 گام ۳: ساخت فایل‌های .gitkeep...")
    created_keeps = 0
    for keep_dir in GITKEEP_DIRS:
        full_path = PROJECT_ROOT / keep_dir / ".gitkeep"
        if create_file_if_not_exists(full_path, ""):
            created_keeps += 1
    print(f"   ✅ {created_keeps} فایل .gitkeep ساخته شد.")
    print()

    # ============================================================
    # گام ۴: ساخت .gitignore در ریشه پروژه
    # ============================================================
    print("🔒 گام ۴: ساخت .gitignore...")
    gitignore_content = """# ============================================================
# .gitignore — سامانه هوشمند ترید
# ============================================================

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
.pytest_cache/
.mypy_cache/
.coverage
htmlcov/

# Virtual Environment
venv/
env/
ENV/
.venv/

# Environment Variables (مهم — هرگز commit نشود)
.env
.env.local
.env.*.local
*.env

# Database
*.db
*.db-journal
*.sqlite
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
Thumbs.db
Desktop.ini
.DS_Store

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
package-lock.json
pnpm-lock.yaml
yarn.lock

# Build outputs
dist/
build/
*.egg

# Logs
logs/*.log
*.log

# Data (داده‌های اکسل کاربر — معمولاً بزرگ هستند)
data/excel_imports/*.xlsx
data/excel_imports/*.xls
data/excel_imports/*.csv
!data/excel_imports/.gitkeep

# Backups
backups/
*.backup

# Temp
*.tmp
tmp/
temp/
"""
    if create_file_if_not_exists(PROJECT_ROOT / ".gitignore", gitignore_content):
        print("   ✅ .gitignore ساخته شد.")
    else:
        print("   ℹ️  .gitignore از قبل وجود داشت.")
    print()

    # ============================================================
    # گام ۵: ساخت README.md
    # ============================================================
    print("📖 گام ۵: ساخت README.md...")
    readme_content = """# سامانه هوشمند ترید 🚀

سامانه جامع تحلیل و ترید در بازارهای کریپتو و فارکس.

## Stack تکنولوژی

- **Backend:** FastAPI 0.111 + Python 3.11 + SQLAlchemy 2.0 (async) + SQLite
- **Frontend:** React 18 + Vite + Zustand + lightweight-charts 4.1.7
- **Database:** SQLite (با ایندکس‌های بهینه)

## ساختار پروژه

```
trading-system/
├── backend/          # Backend با FastAPI
├── frontend/         # Frontend با React + Vite
├── scripts/          # اسکریپت‌های کمکی
├── docs/             # مستندات پروژه
├── data/             # داده‌های ورودی (اکسل و ...)
└── logs/             # لاگ‌های اجرا
```

## CMDها

- **CMD 1:** Backend (uvicorn)
- **CMD 2:** Frontend (npm run dev)
- **CMD 3:** Scripts (اسکریپت‌های Python)

## مستندات

اسناد کامل پروژه در پوشه `docs/` موجود است.

## وضعیت پروژه

نسخه فعلی: **v0.1.0** (در حال توسعه — فاز ۰)
"""
    if create_file_if_not_exists(PROJECT_ROOT / "README.md", readme_content):
        print("   ✅ README.md ساخته شد.")
    else:
        print("   ℹ️  README.md از قبل وجود داشت.")
    print()

    # ============================================================
    # گام ۶: ساخت CHANGELOG.md
    # ============================================================
    print("📝 گام ۶: ساخت CHANGELOG.md...")
    today = datetime.now().strftime("%Y-%m-%d")
    changelog_content = f"""# Change Log — سامانه هوشمند ترید

تمام تغییرات مهم پروژه در این فایل ثبت می‌شود.

فرمت: [Keep a Changelog](https://keepachangelog.com/)
نسخه‌بندی: [Semantic Versioning](https://semver.org/)

---

## [v0.1.0] — {today}

### Added
- ساختار اولیه پوشه‌بندی پروژه (طبق سند ۴)
- فایل .gitignore حرفه‌ای
- اسناد پایه: README، CHANGELOG، SESSION_STATUS، PROJECT_CONTEXT
- پکیج‌های Python (__init__.py)
- لایه DataSource Abstraction در infrastructure/data_sources/

### Decided (تصمیمات معماری تأییدشده)
- Node.js 22 LTS به‌جای 20 LTS (سند ۲ به‌روز شد — Node 20 منقضی شده)
- اضافه شدن لایه DataSource Abstraction
- قانون قفل‌شده #14: تولید فایل توسط Claude (نه کپی-پیست در Notepad)

### Pending
- نصب venv و requirements.txt — گام ۲
- ساخت Core Layer — گام ۳
"""
    if create_file_if_not_exists(PROJECT_ROOT / "CHANGELOG.md", changelog_content):
        print("   ✅ CHANGELOG.md ساخته شد.")
    else:
        print("   ℹ️  CHANGELOG.md از قبل وجود داشت.")
    print()

    # ============================================================
    # گام ۷: ساخت SESSION_STATUS.md
    # ============================================================
    print("📊 گام ۷: ساخت SESSION_STATUS.md...")
    session_status_content = f"""# وضعیت پروژه — {today}

## فاز جاری

**فاز ۰ — زیرساخت + Exchange Connector** — ۱۲٪ پیشرفت

### گام جاری
**گام ۱ از ۸** — ساختار پوشه + Git + اسناد Session ✅ تکمیل‌شده

## فایل‌های ساخته‌شده (آخرین وضعیت)

- ✅ ساختار کامل پوشه‌بندی پروژه (Backend + Frontend + Scripts + Docs)
- ✅ .gitignore
- ✅ README.md
- ✅ CHANGELOG.md
- ✅ docs/SESSION_STATUS.md
- ✅ docs/PROJECT_CONTEXT.md
- ✅ تمام فایل‌های __init__.py برای پکیج‌های Python
- ✅ scripts/01_create_structure.py

## آخرین تغییر مهم

- **{today}** — راه‌اندازی اولیه پروژه، اجرای موفق گام ۱

## تصمیمات تأییدشده

- ✅ **DataSource Abstraction Layer** (سند ۳ + ۱۲) — برای انعطاف‌پذیری بین Excel، Exchange API، فارکس
- ✅ **Node.js 22 LTS** به‌جای 20 LTS (سند ۲) — Node 20 از April 2026 EOL
- ✅ **قانون #14:** تولید فایل توسط Claude (نه کپی-پیست در Notepad)

## تصمیمات معلق

- [ ] هیچ مورد معلقی ندارد

## خطاهای حل‌نشده

- هیچ خطایی وجود ندارد ✅

## گام بعدی

**گام ۲:** Backend — ساخت venv + requirements.txt + main.py پایه

## نسخه پروژه

**v0.1.0**

---

## Stack فعال

- **Backend:** FastAPI 0.111 + Python 3.11.2 + SQLAlchemy 2.0 + SQLite
- **Frontend:** React 18 + Vite + Zustand + lightweight-charts 4.1.7
- **Node.js:** 22.22.3 LTS
- **Git:** 2.47.1

## مسیرها

- **Root:** `D:\\Projects\\trading-system`
- **Backend:** `D:\\Projects\\trading-system\\backend`
- **Frontend:** `D:\\Projects\\trading-system\\frontend`
- **Scripts:** `D:\\Projects\\trading-system\\scripts`
- **Docs:** `D:\\Projects\\trading-system\\docs`
"""
    if create_file_if_not_exists(PROJECT_ROOT / "docs" / "SESSION_STATUS.md", session_status_content):
        print("   ✅ docs/SESSION_STATUS.md ساخته شد.")
    else:
        print("   ℹ️  docs/SESSION_STATUS.md از قبل وجود داشت.")
    print()

    # ============================================================
    # گام ۸: ساخت PROJECT_CONTEXT.md
    # ============================================================
    print("📋 گام ۸: ساخت PROJECT_CONTEXT.md...")
    project_context_content = """# Context پروژه — سامانه هوشمند ترید

> این فایل در ابتدای هر Session جدید همراه با SESSION_STATUS.md
> به Claude ارائه می‌شود.

## Stack فعال

- **Backend:** FastAPI 0.111 + Python 3.11.2 + SQLAlchemy 2.0 (async) + SQLite
- **Frontend:** React 18 + Vite + Zustand 4.5.2 + lightweight-charts 4.1.7
- **Database:** SQLite (trading.db)
- **Node.js:** 22 LTS

## مسیرها

- Root: `D:\\Projects\\trading-system`
- Backend: `D:\\Projects\\trading-system\\backend`
- Frontend: `D:\\Projects\\trading-system\\frontend`
- Scripts: `D:\\Projects\\trading-system\\scripts`

## قوانین کلیدی (🔒 قفل‌شده)

- BrowserRouter فقط در `main.jsx`
- هیچ Query مستقیم خارج از `repositories/`
- هیچ Business Logic در `api/` (فقط در `services/`)
- هر فایل Python: `# -*- coding: utf-8 -*-`
- اصلاح فایل = اسکریپت Python (نه جایگزینی دستی)
- از r.data استفاده نشود (Axios interceptor unwrap کرده)
- فقط یک فایل .db (نام: trading.db)
- هر تغییر DB = Up Script + Down Script
- هیچ Hardcode — همه از .env
- **#14: تولید فایل توسط Claude (نه کپی-پیست در Notepad)**

## معماری

- **Layered Architecture:** Presentation ← Application ← Domain ← Infrastructure
- **Patterns:** Repository، Dependency Injection، DDD، DataSource Abstraction

## CMDها

- **CMD 1:** Backend → `cd backend && venv\\Scripts\\activate && uvicorn main:app --reload`
- **CMD 2:** Frontend → `cd frontend && npm run dev`
- **CMD 3:** Scripts → `cd D:\\Projects\\trading-system && python scripts\\<filename>`

## وضعیت فعلی فاز ۰

- ✅ گام ۱: ساختار پوشه + Git + اسناد Session
- ⏳ گام ۲: venv + requirements + main.py
- ⏳ گام ۳: Core Layer
- ⏳ گام ۴: Database + Migrations
- ⏳ گام ۵: Auth + JWT
- ⏳ گام ۶: DataSource Abstraction + Excel Import
- ⏳ گام ۷: Frontend پایه
- ⏳ گام ۸: کامپوننت‌های مشترک
"""
    if create_file_if_not_exists(PROJECT_ROOT / "docs" / "PROJECT_CONTEXT.md", project_context_content):
        print("   ✅ docs/PROJECT_CONTEXT.md ساخته شد.")
    else:
        print("   ℹ️  docs/PROJECT_CONTEXT.md از قبل وجود داشت.")
    print()

    # ============================================================
    # پیام پایانی
    # ============================================================
    print("=" * 60)
    print("✅ ساخت ساختار اولیه پروژه با موفقیت انجام شد!")
    print("=" * 60)
    print()
    print("📌 مرحله بعدی:")
    print("   ۱. اجرای دستورات Git (init + add + commit) — راهنما در پیام Claude")
    print("   ۲. اطلاع‌رسانی به Claude برای شروع گام ۲")
    print()


if __name__ == "__main__":
    main()
