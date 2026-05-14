# وضعیت پروژه — 2026-05-14

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
