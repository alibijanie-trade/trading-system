# وضعیت پروژه — 2026-05-15 (پایان چت ۳: تثبیت اسناد)

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
