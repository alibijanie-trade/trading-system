# Change Log — سامانه هوشمند ترید

تمام تغییرات مهم پروژه در این فایل ثبت می‌شود.

فرمت: [Keep a Changelog](https://keepachangelog.com/)
نسخه‌بندی: [Semantic Versioning](https://semver.org/)

---

## [v0.1.1] — 2026-05-14

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

## [v0.1.0] — 2026-05-14

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
