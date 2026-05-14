# Change Log — سامانه هوشمند ترید

تمام تغییرات مهم پروژه در این فایل ثبت می‌شود.

فرمت: [Keep a Changelog](https://keepachangelog.com/)
نسخه‌بندی: [Semantic Versioning](https://semver.org/)

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
