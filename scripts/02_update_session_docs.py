# -*- coding: utf-8 -*-
"""
اسکریپت گام ۱.۵ — به‌روزرسانی اسناد Session با تصمیمات تأییدشده
================================================================
این اسکریپت سه فایل را به‌روز می‌کند:
  1. docs/PROJECT_CONTEXT.md  (بازنویسی کامل)
  2. docs/SESSION_STATUS.md   (بازنویسی کامل)
  3. CHANGELOG.md             (افزودن ورودی v0.1.1)

اسکریپت idempotent است: اگر دو بار اجرا شود، v0.1.1 دوباره
به CHANGELOG اضافه نمی‌شود.

نحوه اجرا (در CMD 3):
    cd /d D:\\Projects\\trading-system
    python scripts\\02_update_session_docs.py

نسخه: 1.0.0
تاریخ: 2026-05-14
================================================================
"""

import sys
from datetime import datetime
from pathlib import Path

# ============================================================
# تنظیمات
# ============================================================
PROJECT_ROOT = Path(r"D:\Projects\trading-system")
TODAY = datetime.now().strftime("%Y-%m-%d")
NEW_VERSION = "v0.1.1"

# ============================================================
# محتوای جدید PROJECT_CONTEXT.md
# ============================================================
PROJECT_CONTEXT_CONTENT = r"""# Context پروژه — سامانه هوشمند ترید

> این فایل در ابتدای هر Session جدید همراه با SESSION_STATUS.md
> به Claude ارائه می‌شود.
>
> آخرین به‌روزرسانی: 2026-05-14 (v0.1.1)

---

## Stack فعال

| لایه | تکنولوژی | نسخه |
|------|----------|------|
| Backend | FastAPI + Python | FastAPI 0.111 + Python 3.11.2 |
| ORM | SQLAlchemy | 2.0.30 (async) |
| Database | SQLite | فایل: trading.db |
| Migration | Alembic | 1.13.1 |
| Frontend | React + Vite + Zustand | React 18 + Zustand 4.5.2 |
| Charts | lightweight-charts | 4.1.7 |
| Node.js | LTS | 22.x |
| Encryption | cryptography.Fernet | جدیدترین |

## مسیرها

- **Root:** `D:\Projects\trading-system`
- **Backend:** `D:\Projects\trading-system\backend`
- **Frontend:** `D:\Projects\trading-system\frontend`
- **Scripts:** `D:\Projects\trading-system\scripts`
- **Docs:** `D:\Projects\trading-system\docs`
- **Data (Excel):** `D:\Projects\trading-system\data\excel_imports`

## CMDها

| CMD | کاربرد | دستور آغازین |
|-----|--------|--------------|
| CMD 1 | Backend (uvicorn) | `cd backend && venv\Scripts\activate && uvicorn main:app --reload` |
| CMD 2 | Frontend (npm dev) | `cd frontend && npm run dev` |
| CMD 3 | Scripts (Python) | `cd D:\Projects\trading-system && python scripts\<filename>` |

## قوانین کلیدی (🔒 قفل‌شده)

- BrowserRouter فقط در `main.jsx`
- هیچ Query مستقیم خارج از `repositories/`
- هیچ Business Logic در `api/` (فقط در `services/`)
- هر فایل Python: `# -*- coding: utf-8 -*-`
- اصلاح فایل = اسکریپت Python (نه جایگزینی دستی)
- از `r.data` استفاده نشود (Axios interceptor unwrap کرده)
- فقط یک فایل .db (نام: `trading.db`)
- هر تغییر DB = Up Script + Down Script
- هیچ Hardcode — همه از `.env`
- **#14:** تولید فایل توسط Claude به‌صورت Artifact (نه کپی-پیست در Notepad)

## معماری

- **Layered Architecture:** Presentation ← Application ← Domain ← Infrastructure
- **Patterns:** Repository، Dependency Injection، DDD، **DataSource Abstraction**

---

## ✅ تصمیمات معماری تأییدشده

این بخش حیاتی است — تمام تصمیماتی که در Sessionهای قبل تأیید شده‌اند.

### Session 1 (راه‌اندازی پروژه)

1. **Node.js 22 LTS** به‌جای 20 LTS (Node 20 از April 2026 EOL)
2. **DataSource Abstraction Layer** — مسیر: `infrastructure/data_sources/`
3. **قانون #14:** تولید فایل توسط Claude به‌صورت Artifact

### Session 2 (پیش از فاز ۰)

4. **رمزنگاری API Key:** `cryptography.Fernet`
   - کلید توسط اسکریپت setup خودکار تولید می‌شود
   - در `.env` ذخیره و در `.gitignore` است
   - هشدار برجسته در setup: «از `.env` بک‌آپ بگیرید»

5. **Migration:** Alembic
   - برای ALTER COLUMN در SQLite، جدول recreate می‌شود
   - هر تغییر DB باید Up Script + Down Script داشته باشد

6. **WebSocket Auth:** Handshake پس از اتصال
   - Client اولین پیام: `{"type": "auth", "token": "..."}`
   - مهلت ۵ ثانیه؛ سپس server اتصال را می‌بندد
   - دلیل: عدم ثبت token در URL/لاگ Nginx/Referer

7. **Timezone:** UTC در DB — تبدیل به Asia/Tehran در UI

8. **اتصال صرافی در فاز ۰:** بدون اتصال — فقط Excel
   - کانکتور Binance در فاز ۱ یا ۲ اضافه می‌شود

9. **تست‌نویسی فاز ۰:** فقط critical (auth، encryption، repository base)
   - باقی تست‌ها در فاز ۱۳

10. **فونت‌ها (جایگزین رایگان به‌جای B Titr و B Mitra):**
    - UI: **Vazirmatn**
    - سرستون جداول: **Estedad**
    - داده‌های جدول: **IRANSans**

11. **Seeding اولیه:**
    - کاربر `admin` با `username=1, password=1` (هشدار تغییر در production)
    - یک رکورد `Binance` در جدول `Exchanges`
    - بدون seed نمادها (با ورود اولین Excel ساخته می‌شوند)

12. **تقویم پیش‌فرض:** میلادی (قابل تغییر در تنظیمات)

13. **PRAGMA SQLite (در اتصال DB):**
    - `foreign_keys = ON`
    - `journal_mode = WAL`
    - `synchronous = NORMAL`
    - `cache_size = -64000` (64 MB)

---

## وضعیت فعلی فاز ۰

- ✅ **گام ۱:** ساختار پوشه + Git + اسناد Session
- ✅ **گام ۱.۵:** به‌روزرسانی اسناد با تصمیمات Session 2
- ⏳ **گام ۲:** Backend پایه (venv + requirements + main.py + .env.example)
- ⏳ **گام ۳:** Core Layer (config + logger + exceptions + security)
- ⏳ **گام ۴:** Database + Models + Alembic + اولین Migration
- ⏳ **گام ۵:** Auth + JWT + RBAC
- ⏳ **گام ۶:** DataSource Abstraction + Excel Reader
- ⏳ **گام ۷:** Frontend پایه (Vite + React + Router + Axios + authStore)
- ⏳ **گام ۸:** کامپوننت‌های مشترک + Theme Engine + Login UI
"""

# ============================================================
# محتوای جدید SESSION_STATUS.md
# ============================================================
SESSION_STATUS_CONTENT = r"""# وضعیت پروژه — 2026-05-14

## فاز جاری

**فاز ۰ — زیرساخت + Exchange Connector** — ۱۸٪ پیشرفت

### گام جاری

**گام ۱.۵ از ۸** — به‌روزرسانی اسناد با تصمیمات Session 2 ✅ تکمیل‌شده

## فایل‌های ساخته‌شده (آخرین وضعیت)

- ✅ ساختار کامل پوشه‌بندی پروژه (Backend + Frontend + Scripts + Docs)
- ✅ .gitignore + README.md + CHANGELOG.md (v0.1.1)
- ✅ docs/SESSION_STATUS.md (به‌روز با ۱۳ تصمیم)
- ✅ docs/PROJECT_CONTEXT.md (به‌روز با ۱۳ تصمیم)
- ✅ تمام فایل‌های __init__.py برای پکیج‌های Python
- ✅ scripts/01_create_structure.py
- ✅ scripts/02_update_session_docs.py

## آخرین تغییر مهم

- **2026-05-14** — گام ۱.۵: ثبت ۱۰ تصمیم Session 2 در PROJECT_CONTEXT و SESSION_STATUS و CHANGELOG

## تصمیمات تأییدشده (مرجع کامل: PROJECT_CONTEXT.md)

### Session 1
1. ✅ Node.js 22 LTS (به‌جای 20)
2. ✅ DataSource Abstraction Layer
3. ✅ قانون #14: تولید فایل توسط Claude به‌صورت Artifact

### Session 2
4. ✅ رمزنگاری API Key: `cryptography.Fernet`
5. ✅ Migration: Alembic + recreate در ALTER
6. ✅ WebSocket Auth: handshake JSON پس از اتصال (5s timeout)
7. ✅ Timezone: UTC در DB، تبدیل در UI
8. ✅ فاز ۰: بدون اتصال صرافی (فقط Excel)
9. ✅ تست فاز ۰: فقط critical
10. ✅ فونت‌ها: Vazirmatn + Estedad + IRANSans (رایگان)
11. ✅ Seeding: admin/1/1 + Binance row
12. ✅ تقویم پیش‌فرض: میلادی
13. ✅ PRAGMA SQLite: foreign_keys + WAL + NORMAL + 64MB cache

## تصمیمات معلق

- [ ] هیچ مورد معلقی ندارد ✅

## خطاهای حل‌نشده

- هیچ خطایی وجود ندارد ✅

## گام بعدی

**گام ۲:** Backend پایه
- ساخت venv در `backend/`
- `requirements.txt` با نسخه‌های قطعی (طبق سند ۲)
- `.env.example` (نمونه عمومی) و `.env` (با Fernet key تولیدشده)
- `backend/main.py` پایه با CORS + Health check endpoint
- تست اجرا با uvicorn
- پیام موفقیت: API روی `http://127.0.0.1:8000/api/v1/health` پاسخ بدهد

## نسخه پروژه

**v0.1.1**

---

## Stack فعال

- **Backend:** FastAPI 0.111 + Python 3.11.2 + SQLAlchemy 2.0 + SQLite
- **Frontend:** React 18 + Vite + Zustand + lightweight-charts 4.1.7
- **Node.js:** 22 LTS
- **Encryption:** cryptography.Fernet

## مسیرها

- **Root:** `D:\Projects\trading-system`
- **Backend:** `D:\Projects\trading-system\backend`
- **Frontend:** `D:\Projects\trading-system\frontend`
- **Scripts:** `D:\Projects\trading-system\scripts`
- **Docs:** `D:\Projects\trading-system\docs`
"""

# ============================================================
# ورودی جدید برای CHANGELOG.md (پیش از v0.1.0 درج می‌شود)
# ============================================================
CHANGELOG_NEW_ENTRY = r"""## [v0.1.1] — 2026-05-14

### Added
- ثبت ۱۰ تصمیم معماری Session 2 در `docs/PROJECT_CONTEXT.md`
- بخش جدید «تصمیمات معماری تأییدشده» در PROJECT_CONTEXT
- اسکریپت `scripts/02_update_session_docs.py`

### Decided (تصمیمات معماری تأییدشده در Session 2)
- **رمزنگاری API Key:** `cryptography.Fernet` (به‌جای AES-256 خام) + تولید خودکار کلید در setup
- **Migration:** Alembic؛ برای ALTER COLUMN در SQLite → recreate جدول
- **WebSocket Auth:** handshake JSON پس از اتصال (timeout = 5s)
- **Timezone:** UTC در DB، تبدیل به Asia/Tehran در UI
- **فاز ۰ — منبع داده:** فقط Excel (بدون اتصال صرافی)
- **تست فاز ۰:** فقط critical (auth / encryption / repository-base)
- **فونت‌ها:** Vazirmatn (UI) + Estedad (سرستون) + IRANSans (داده) — همگی رایگان
- **Seeding:** کاربر admin/1/1 + رکورد Binance؛ بدون seed نمادها
- **تقویم پیش‌فرض:** میلادی
- **PRAGMA SQLite:** foreign_keys=ON + journal_mode=WAL + synchronous=NORMAL + cache_size=-64000

### Pending
- گام ۲: Backend پایه — venv + requirements.txt + main.py + .env

---

"""


# ============================================================
# توابع کمکی
# ============================================================
def write_file_full(path: Path, content: str) -> None:
    """فایل را با محتوای جدید کاملاً بازنویسی می‌کند."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def update_changelog(path: Path, new_entry: str, version_tag: str) -> str:
    """
    ورودی جدید را قبل از اولین ورودی موجود اضافه می‌کند.
    اگر version_tag از قبل در فایل باشد، چیزی اضافه نمی‌کند (idempotent).

    خروجی: یکی از مقادیر "added", "skipped", "error"
    """
    if not path.exists():
        return "error"

    current = path.read_text(encoding="utf-8")

    # چک idempotency
    if f"[{version_tag}]" in current:
        return "skipped"

    # marker: اولین خط شروع v
    marker = "## [v0.1.0]"
    if marker not in current:
        return "error"

    # درج ورودی جدید قبل از v0.1.0
    new_content = current.replace(marker, new_entry + marker, 1)
    path.write_text(new_content, encoding="utf-8")
    return "added"


# ============================================================
# تابع اصلی
# ============================================================
def main() -> None:
    print("=" * 60)
    print("🔄 گام ۱.۵ — به‌روزرسانی اسناد Session")
    print("=" * 60)
    print(f"📁 مسیر ریشه: {PROJECT_ROOT}")
    print(f"📅 تاریخ: {TODAY}")
    print(f"🏷️  نسخه جدید: {NEW_VERSION}")
    print()

    # بررسی وجود پوشه ریشه
    if not PROJECT_ROOT.exists():
        print(f"❌ خطا: پوشه ریشه وجود ندارد: {PROJECT_ROOT}")
        sys.exit(1)

    docs_dir = PROJECT_ROOT / "docs"
    if not docs_dir.exists():
        print(f"❌ خطا: پوشه docs وجود ندارد: {docs_dir}")
        print("   ابتدا 01_create_structure.py را اجرا کنید.")
        sys.exit(1)

    # ============================================================
    # ۱) PROJECT_CONTEXT.md
    # ============================================================
    print("📋 [1/3] به‌روزرسانی docs/PROJECT_CONTEXT.md ...")
    context_path = docs_dir / "PROJECT_CONTEXT.md"
    write_file_full(context_path, PROJECT_CONTEXT_CONTENT)
    print(f"   ✅ بازنویسی شد ({len(PROJECT_CONTEXT_CONTENT):,} کاراکتر)")
    print()

    # ============================================================
    # ۲) SESSION_STATUS.md
    # ============================================================
    print("📊 [2/3] به‌روزرسانی docs/SESSION_STATUS.md ...")
    status_path = docs_dir / "SESSION_STATUS.md"
    write_file_full(status_path, SESSION_STATUS_CONTENT)
    print(f"   ✅ بازنویسی شد ({len(SESSION_STATUS_CONTENT):,} کاراکتر)")
    print()

    # ============================================================
    # ۳) CHANGELOG.md
    # ============================================================
    print(f"📝 [3/3] افزودن ورودی {NEW_VERSION} به CHANGELOG.md ...")
    changelog_path = PROJECT_ROOT / "CHANGELOG.md"
    result = update_changelog(changelog_path, CHANGELOG_NEW_ENTRY, NEW_VERSION)
    if result == "added":
        print(f"   ✅ ورودی {NEW_VERSION} اضافه شد")
    elif result == "skipped":
        print(f"   ℹ️  ورودی {NEW_VERSION} از قبل وجود داشت — رد شد (idempotent)")
    else:
        print(f"   ❌ خطا: marker در CHANGELOG پیدا نشد. لطفاً فایل را بررسی کنید.")
        sys.exit(1)
    print()

    # ============================================================
    # پیام پایانی
    # ============================================================
    print("=" * 60)
    print("✅ گام ۱.۵ با موفقیت تکمیل شد!")
    print("=" * 60)
    print()
    print("📌 مراحل بعدی:")
    print()
    print("   ۱. فایل‌های به‌روز شده را در Notepad باز و چک کنید:")
    print(r"      D:\Projects\trading-system\docs\PROJECT_CONTEXT.md")
    print(r"      D:\Projects\trading-system\docs\SESSION_STATUS.md")
    print(r"      D:\Projects\trading-system\CHANGELOG.md")
    print()
    print("   ۲. Commit کنید (در CMD 3):")
    print(r"      cd /d D:\Projects\trading-system")
    print(
        r"      git add docs/PROJECT_CONTEXT.md docs/SESSION_STATUS.md CHANGELOG.md scripts/02_update_session_docs.py"
    )
    print(r'      git commit -m "docs(session): record 10 architecture decisions (v0.1.1)"')
    print()
    print("   ۳. سپس به Claude پیام دهید: «گام ۱.۵ انجام شد، گام ۲ را شروع کن»")
    print()


if __name__ == "__main__":
    main()
