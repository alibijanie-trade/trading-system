# Context پروژه — سامانه هوشمند ترید

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
