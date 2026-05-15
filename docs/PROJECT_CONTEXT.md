# Context پروژه — سامانه هوشمند ترید

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

- **Root:** `D:\Projects\trading-system`
- **Backend:** `D:\Projects\trading-system\backend`
- **Frontend:** `D:\Projects\trading-system\frontend` (هنوز ساخته نشده)
- **Scripts:** `D:\Projects\trading-system\scripts`
- **Docs:** `D:\Projects\trading-system\docs`

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

- `D:\Projects\trading-system\docs\SESSION_STATUS.md` — وضعیت پویا (هر چت آپدیت می‌شود)
- `D:\Projects\trading-system\docs\PROJECT_CONTEXT.md` — این فایل (Context پایدار)
- سند جامع به‌عنوان فایل پیوست در چت‌ها استفاده می‌شود (به‌جای ذخیره دائمی)

## یادآوری مهم برای پایان هر چت

طبق ساختار فعلی، Claude باید در پایان هر چت یک اسکریپت آپدیت SESSION_STATUS و PROJECT_CONTEXT بسازد تا کاربر اجرا کند. این موضوع به‌عنوان «پروتکل پایان چت» در چت ۳ پیشنهاد شد و در چت بعدی برای تأیید رسمی مطرح خواهد شد.
