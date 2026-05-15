# -*- coding: utf-8 -*-
"""
07_end_of_chat3_update_docs.py
═══════════════════════════════════════════════════════════
آپدیت پایان چت ۳ (تثبیت اسناد + سند ۱۴ پروتکل تعویض چت)

این اسکریپت دو فایل را بازنویسی می‌کند:
  - docs/SESSION_STATUS.md
  - docs/PROJECT_CONTEXT.md

اجرا در CMD 3 از ریشه پروژه:
    cd /d D:\\Projects\\trading-system
    python scripts\\07_end_of_chat3_update_docs.py

ویژگی‌ها:
  - Idempotent (اجرای مجدد مشکلی نمی‌سازد)
  - فقط در صورت تغییر، فایل را بازنویسی می‌کند
  - پیام‌های موفقیت/خطا به فارسی
═══════════════════════════════════════════════════════════
"""

import sys
from pathlib import Path

# UTF-8 برای کنسول ویندوز
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"

print("=" * 64)
print("📝 آپدیت اسناد Session — پایان چت ۳ (تثبیت اسناد)")
print("=" * 64)
print(f"📁 ریشه پروژه: {ROOT}")
print(f"📁 پوشه docs:  {DOCS_DIR}")
print()

if not DOCS_DIR.exists():
    print(f"❌ پوشه docs پیدا نشد: {DOCS_DIR}")
    print("   مطمئن شوید اسکریپت را از ریشه پروژه اجرا می‌کنید:")
    print("       cd /d D:\\Projects\\trading-system")
    print("       python scripts\\07_end_of_chat3_update_docs.py")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════
# محتوای SESSION_STATUS.md
# ═══════════════════════════════════════════════════════════
SESSION_STATUS = """# وضعیت پروژه — 2026-05-15 (پایان چت ۳: تثبیت اسناد)

## فاز جاری

فاز ۰ — زیرساخت — حدود ۶۰٪ پیشرفت (۵ از ۸ زیرگام کامل)

## نوع این چت

**📋 چت اسناد** — هیچ کد جدیدی در این چت نوشته نشد. خروجی‌های اصلی:
- تولید سند جامع v2.1.docx (نسخه Word)
- تبدیل و گسترش به سند جامع v2.2.md (Markdown — توصیه‌شده)
- افزودن سند ۱۴ جدید: «پروتکل تعویض چت (Chat Handoff Protocol)»
- افزودن قانون قفل‌شده #15
- تنظیم اسناد Session برای چت بعدی

## گام‌های انجام‌شده فاز ۰

- ✅ گام ۱: ساختار پوشه + Git + اسناد Session
- ✅ گام ۱.۵: ثبت ۱۳ تصمیم معماری Session 2 در PROJECT_CONTEXT
- ✅ گام ۲: Backend پایه (venv + requirements + main.py + .env + config + health)
- ✅ گام ۳: Core Layer (Logger + ۱۳ Exception + Handlers + Response)
- ✅ گام ۳.۵: Fix رنگ ANSI و emoji در Windows CMD (colorama)
- ⏳ **گام ۴.۱ — گام بعدی** — Database + Models + Repositories

## گام‌های معلق

- ⏳ گام ۴.۲: Alembic + اولین Migration + Seeding (admin + Binance)
- ⏳ گام ۵: Auth + JWT + RBAC + Audit Log
- ⏳ گام ۶: DataSource Abstraction + Excel Reader
- ⏳ گام ۷: Frontend پایه (Vite + React + Router + Axios + authStore)
- ⏳ گام ۸: کامپوننت‌های مشترک + Theme Engine + Login UI

## وضعیت تست‌شده (بدون تغییر از پایان چت قبل)

- ✅ uvicorn روی http://127.0.0.1:8000 اجرا می‌شود
- ✅ http://127.0.0.1:8000/ → JSON موفق با ساختار استاندارد
- ✅ http://127.0.0.1:8000/api/v1/health → JSON موفق
- ✅ http://127.0.0.1:8000/docs → Swagger UI
- ✅ http://127.0.0.1:8000/api/v1/no-such-route → JSON خطای 404 فارسی استاندارد
- ✅ فایل‌های log در backend/logs/ ساخته می‌شوند (app.log + error.log)
- ✅ emoji و رنگ‌های پیام‌های خود سیستم در CMD درست نمایش داده می‌شوند

## تصمیمات گرفته‌شده در این چت

- ✅ **افزودن سند ۱۴ — پروتکل تعویض چت (Chat Handoff Protocol)** — تأییدشده
- ✅ **افزودن قانون قفل‌شده #15** — اجرای اجباری پروتکل سند ۱۴ هنگام افت کیفیت — تأییدشده
- ✅ **انتقال سند ۱۴ قبلی (وضعیت اجرا) به سند ۱۵** — تأییدشده
- ✅ **افزایش نسخه سند جامع از v2.1 به v2.2** — تأییدشده
- ✅ **انتخاب Markdown به‌جای docx به‌عنوان فرمت پیش‌فرض سند جامع** — تأییدشده (با امکان تبدیل به docx در صورت درخواست)

## تصمیمات معلق برای چت بعدی

- [ ] **پروتکل پایان چت** — پیشنهاد شده ولی هنوز رسماً تأیید نشده. هدف: Claude در پایان هر چت (نه فقط هنگام افت کیفیت) به ابتکار خود اسکریپت آپدیت SESSION_STATUS و PROJECT_CONTEXT را بسازد. اگر تأیید شود، باید به سند v2.3 منتقل شود.

## خطاهای حل‌نشده

- (هیچ‌کدام)

## مسائل شناخته‌شده (Non-blocking)

- پیام‌های اولیه uvicorn (قبل از startup hook) هنوز ANSI خام دارند چون colorama پس از آن‌ها اجرا می‌شود — موکول به بعد، کاربر را متوقف نمی‌کند

## فایل‌های تولیدشده در این چت (در پنل سمت راست برای دانلود)

- `سند_جامع_v2.1.docx` (نسخه Word اولیه — اختیاری)
- `سند_جامع_v2.2.md` (نسخه نهایی Markdown — **توصیه‌شده برای چت بعدی**)
- `07_end_of_chat3_update_docs.py` (همین اسکریپت)

## برای شروع چت جدید

کاربر باید ۴ مورد را پیوست کند:

1. `سند_جامع_v2.2.md` (از پنل سمت راست چت قبلی)
2. `SESSION_STATUS.md` (همین فایل پس از آپدیت — از `docs/`)
3. `PROJECT_CONTEXT.md` (از `docs/`)
4. `trading-system.zip` (فایل فشرده کل پوشه پروژه بدون `venv` و `__pycache__`)

پیام شروع پیشنهادی در آخرین پاسخ Claude در چت قبلی آمده.

## گام بعدی — جزئیات زیرگام ۴.۱: Database + Models + Repositories

این گام شامل کارهای زیر است:

- اتصال async SQLAlchemy + aiosqlite در `backend/app/infrastructure/database/`
- اعمال PRAGMA ها در connect event (foreign_keys + WAL + NORMAL + cache 64MB)
- Base class با timestamps و soft delete mixin
- ۱۴ مدل: `Users, Sessions, Exchanges, ExchangeAPIKeys, Symbols, Watchlist, OhlcvData, Strategies, Signals, Trades, Portfolio, Alerts, RiskSettings, AppSettings, AuditLog`
- ایندکس‌های critical (مخصوصاً `idx_ohlcv_symbol_tf_ts`)
- Repository Pattern (`BaseRepository` + نمونه‌های تخصصی)
- Dependency Injection برای session

سپس زیرگام ۴.۲: Alembic + Migration اولیه + Seeding (admin/1/1 + Binance row).

## نسخه پروژه

- **کد:** v0.1.2 (بدون تغییر کد در این چت)
- **اسناد:** v2.2 (سند جامع)
- **آخرین commit:** پایان چت قبلی (گام ۳.۵)
"""


# ═══════════════════════════════════════════════════════════
# محتوای PROJECT_CONTEXT.md
# ═══════════════════════════════════════════════════════════
PROJECT_CONTEXT = """# Context پروژه — سامانه هوشمند ترید

> این فایل context پایدار پروژه است. در هر مکالمه جدید، Claude باید ابتدا این فایل را بخواند.

## Stack فعال

- **Backend:** FastAPI 0.111 + Python 3.11.2 + SQLAlchemy 2.0 (async) + SQLite
- **Frontend:** React 18 + Vite + Zustand 4.5.2 + lightweight-charts 4.1.7
- **Database:** SQLite (trading.db) با ۴ PRAGMA:
  - `foreign_keys=ON`
  - `journal_mode=WAL`
  - `synchronous=NORMAL`
  - `cache_size=-64000` (64 MB)
- **Node.js:** 22 LTS
- **Encryption:** `cryptography.Fernet` (44-char auto-generated key in `.env`)
- **Git:** نسخه ۲.۴۷.۱

## مسیرها

- **Root:** `D:\\Projects\\trading-system`
- **Backend:** `D:\\Projects\\trading-system\\backend`
- **Frontend:** `D:\\Projects\\trading-system\\frontend` (هنوز ساخته نشده)
- **Scripts:** `D:\\Projects\\trading-system\\scripts`
- **Docs:** `D:\\Projects\\trading-system\\docs`

## CMDها

| CMD | نقش | وضعیت |
|---|---|---|
| **CMD 1** | Backend (`uvicorn --reload`) | همیشه باز |
| **CMD 2** | Frontend (`npm run dev`) | هنوز نیاز نیست |
| **CMD 3** | Scripts + Git | موقتی |

## قوانین قفل‌شده (۱۵ قانون)

| # | قانون |
|---|---|
| ۱ | نقش‌های تعریف‌شده |
| ۲ | الزام توضیح گام‌به‌گام |
| ۳ | الزام فایل کامل یا اسکریپت در هر تغییر |
| ۴ | عدم تغییر بخش‌های تأییدشده |
| ۵ | رعایت معماری ساخته‌شده |
| ۶ | جلوگیری از Technical Debt |
| ۷ | Impact Analysis قبل از تغییر مهم |
| ۸ | رعایت Versioning Policy |
| ۹ | رعایت Change Control |
| ۱۰ | رعایت Migration Protocol (Up/Down Script) |
| ۱۱ | یادآوری حافظه در صورت نیاز |
| ۱۲ | مدیریت Context در هر Session جدید |
| ۱۳ | یادآوری موارد معلق تا انجام یا لغو صریح |
| **۱۴ 🆕 v2.1** | تولید فایل توسط Claude به‌صورت Artifact (نه کپی-پیست در Notepad) |
| **۱۵ 🆕 v2.2** | اجرای اجباری پروتکل تعویض چت (سند ۱۴) هنگام افت کیفیت |

## قوانین فنی کلیدی

- BrowserRouter فقط در `main.jsx`
- هیچ Query مستقیم خارج از `repositories/`
- هر فایل Python: `# -*- coding: utf-8 -*-`
- اصلاح فایل: اسکریپت Python — نه جایگزینی دستی
- اسکریپت‌ها idempotent باشند
- هرگز از `echo` برای متن فارسی — همیشه از فایل Python
- فقط یک فایل `.db` — نام: `trading.db`
- هیچ Hardcode — همه از `.env`

## تصمیمات معماری تأییدشده

### Session 1 — راه‌اندازی پروژه (۳ تصمیم)

1. **Node.js 22 LTS** (به‌جای 20 LTS — Node 20 از April 2026 EOL)
2. **افزودن لایه DataSource Abstraction** در `infrastructure/data_sources/`
3. **قانون قفل‌شده #14:** تولید فایل توسط Claude به‌صورت Artifact

### Session 2 — پیش از فاز ۰ و حین آن (۱۴ تصمیم)

4. **رمزنگاری API Key:** `cryptography.Fernet` (به‌جای AES-256 خام) + تولید خودکار کلید در setup
5. **Migration:** Alembic؛ برای ALTER COLUMN در SQLite → recreate جدول
6. **WebSocket Auth:** handshake JSON پس از اتصال (timeout = 5s)
7. **Timezone:** UTC در DB، تبدیل به Asia/Tehran در UI
8. **فاز ۰ — منبع داده:** فقط Excel (بدون اتصال صرافی)
9. **تست فاز ۰:** فقط critical (auth / encryption / repository-base)
10. **فونت‌ها:** Vazirmatn (UI) + Estedad (سرستون) + IRANSans (داده) — همگی رایگان
11. **Seeding:** کاربر admin/1/1 + رکورد Binance؛ بدون seed نمادها
12. **تقویم پیش‌فرض:** میلادی (قابل تنظیم)
13. **PRAGMA SQLite:** foreign_keys=ON + journal_mode=WAL + synchronous=NORMAL + cache_size=-64000
14. **pydantic-settings 2.2.1** (به‌جای BaseSettings قدیمی)
15. **colorama 0.4.6** برای Windows ANSI + UTF-8
16. **جدول AuditLog** اضافه شد به Schema (سند ۵.۱۲)
17. **Python 3.11.2** (به‌جای 3.11.9 — نسخه عملاً نصب‌شده)

### چت ۳ — تثبیت اسناد (۵ تصمیم)

18. **افزودن سند ۱۴ — پروتکل تعویض چت** (Chat Handoff Protocol)
19. **قانون قفل‌شده #15** — اجرای اجباری پروتکل سند ۱۴ هنگام افت کیفیت چت
20. **انتقال سند ۱۴ قدیمی (وضعیت اجرا) به سند ۱۵**
21. **افزایش نسخه سند جامع به v2.2**
22. **فرمت پیش‌فرض سند جامع: Markdown** (با امکان تبدیل به docx در صورت درخواست)

## سند مرجع

- **سند جامع فعلی:** v2.2 (در فایل `سند_جامع_v2.2.md`)
- **اولویت در صورت تناقض بین منابع:**
  1. سند جامع v2.2
  2. SESSION_STATUS.md
  3. PROJECT_CONTEXT.md (همین فایل)
  4. محتوای zip پروژه

## مسیرهای فایل‌های مرجع

- `D:\\Projects\\trading-system\\docs\\SESSION_STATUS.md` — وضعیت پویا (هر چت آپدیت می‌شود)
- `D:\\Projects\\trading-system\\docs\\PROJECT_CONTEXT.md` — این فایل (Context پایدار)
- سند جامع به‌عنوان فایل پیوست در چت‌ها استفاده می‌شود (به‌جای ذخیره دائمی)

## یادآوری مهم برای پایان هر چت

طبق ساختار فعلی، Claude باید در پایان هر چت یک اسکریپت آپدیت SESSION_STATUS و PROJECT_CONTEXT بسازد تا کاربر اجرا کند. این موضوع به‌عنوان «پروتکل پایان چت» در چت ۳ پیشنهاد شد و در چت بعدی برای تأیید رسمی مطرح خواهد شد.
"""


# ═══════════════════════════════════════════════════════════
# تابع نوشتن فایل با چک idempotency
# ═══════════════════════════════════════════════════════════
def write_file(path: Path, content: str, label: str) -> None:
    try:
        existing = path.read_text(encoding="utf-8") if path.exists() else ""
        if existing == content:
            print(f"✓ {label} بدون تغییر است (idempotent)")
            return
        path.write_text(content, encoding="utf-8")
        size_kb = len(content.encode("utf-8")) / 1024
        action = "بازنویسی" if existing else "ساخته"
        print(f"✅ {label} {action} شد ({size_kb:.1f} KB)")
    except Exception as e:
        print(f"❌ خطا در نوشتن {label}: {e}")
        sys.exit(1)


write_file(DOCS_DIR / "SESSION_STATUS.md", SESSION_STATUS, "SESSION_STATUS.md")
write_file(DOCS_DIR / "PROJECT_CONTEXT.md", PROJECT_CONTEXT, "PROJECT_CONTEXT.md")

print()
print("=" * 64)
print("✅ اسناد Session آپدیت شدند. اکنون می‌توانید چت را ببندید.")
print("=" * 64)
print()
print("📌 برای چت جدید، ۴ مورد را پیوست کنید:")
print("   ۱. سند_جامع_v2.2.md (از پنل سمت راست چت قبلی)")
print("   ۲. SESSION_STATUS.md (از docs/)")
print("   ۳. PROJECT_CONTEXT.md (از docs/)")
print("   ۴. trading-system.zip (پوشه پروژه بدون venv و __pycache__)")
print()
print("📌 پیام شروع پیشنهادی در آخرین پاسخ Claude در این چت آمده.")
print()
print("💡 پیشنهاد commit (در CMD 3):")
print("   git add docs/SESSION_STATUS.md docs/PROJECT_CONTEXT.md scripts/07_end_of_chat3_update_docs.py")
print('   git commit -m "docs(session): close chat 3 — add Chat Handoff Protocol (v2.2)"')
print()
