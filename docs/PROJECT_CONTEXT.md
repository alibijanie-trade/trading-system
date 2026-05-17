# Context پروژه — سامانه هوشمند ترید

> این فایل context پایدار پروژه است. در هر مکالمه جدید، Claude باید ابتدا این فایل را بخواند.

## Stack فعال (🆕 v2.5)

### Backend (Python 3.11.2)

- **Framework:** FastAPI 0.111 + Uvicorn 0.29
- **ORM:** SQLAlchemy 2.0.30 (async) + aiosqlite 0.20.0
- **DB:** SQLite (`trading.db` در `backend/`) با ۴ PRAGMA: `foreign_keys=ON`, `journal_mode=WAL`, `synchronous=NORMAL`, `cache_size=-64000`
- **Migration:** Alembic 1.13.1 (head: `08348dca2b9a`)
- **Auth:** python-jose 3.3.0 (JWT) + **bcrypt 4.1.3 مستقیم** (passlib حذف شد)
- **OAuth2 Form:** python-multipart 0.0.9
- **Encryption:** cryptography 42.0.7 (Fernet)
- **Validation:** Pydantic 2.7.1 + pydantic-settings 2.2.1
- **Data:** pandas 2.2.2 + openpyxl 3.1.2

### Frontend (Node.js 22 LTS) — 🆕 v2.5

- **Framework:** React 18 + Vite 8.0.13
- **Routing:** react-router-dom 6.23.1
- **State:** Zustand 4.5.2 (با middleware `persist` برای localStorage)
- **HTTP:** axios 1.7.2 (با JWT interceptor + handle 401)
- **Charts:** lightweight-charts 4.1.7

## محیط اجرا — Windows Terminal (🆕 v2.5: ایموجی رنگی)

| Tab | نام + ایموجی | نقش |
|---|---|---|
| **1** | 🟦 `tab «1 backend»` | uvicorn (Backend) |
| **2** | 🟩 `tab «2 scripts»` | scripts + alembic + git + pip + npm |
| **3** | 🟧 `tab «3 frontend»` | npm run dev (Vite) |

## مسیرها

- **Root:** `D:\Projects\trading-system`
- **Backend:** `D:\Projects\trading-system\backend`
- **Frontend:** `D:\Projects\trading-system\frontend` ✅ scaffold شد
- **Scripts:** `D:\Projects\trading-system\scripts`
- **Docs:** `D:\Projects\trading-system\docs`
- **Excel Imports:** `D:\Projects\trading-system\data\excel_imports`

## قوانین قفل‌شده (۲۰ قانون — به‌روزشده v2.5)

| # | قانون |
|---|---|
| ۱-۱۳ | (قوانین پایه از Session 1+2) |
| ۱۴ | تولید فایل توسط Claude به‌صورت Artifact |
| ۱۵ | اجرای اجباری پروتکل تعویض چت |
| ۱۶ | کم‌حرفی فنی — فقط دستور + خروجی |
| **۱۷ (توسعه‌یافته v2.5)** | **نام tab با ایموجی رنگی** — 🟦 backend / 🟩 scripts / 🟧 frontend |
| ۱۸ | لینک فایل دانلودی **قبل از** دستورات |
| **۱۹ 🆕 v2.5** | **تست endpoint از ترمینال (httpx) — اولویت بر Swagger UI** |
| **۲۰ 🆕 v2.5** | **تولید خودکار دستورات پاک‌سازی در پروتکل تعویض چت** — اسکریپت `00_cleanup_for_zip.py` |

## قوانین فنی کلیدی

- BrowserRouter فقط در `main.jsx`
- هیچ Query مستقیم خارج از `repositories/`
- هر فایل Python: `# -*- coding: utf-8 -*-`
- اصلاح فایل: اسکریپت Python — نه جایگزینی دستی
- اسکریپت‌ها idempotent باشند
- فقط یک فایل `.db` — نام: `trading.db` در `backend/`
- هیچ Hardcode — همه از `.env`
- **alembic.ini فقط ASCII** (cp1252 در ویندوز)
- **DATABASE_URL** absolute resolve نسبت به `BACKEND_DIR`
- **APP_VERSION** در `.env` بر default در `config.py` غلبه می‌کند — هنگام bump هر دو را آپدیت کن
- **bcrypt** مستقیم استفاده شود، نه passlib
- **JWT** در localStorage با Zustand `persist` (فاز ۰) — مهاجرت به HttpOnly Cookie در فاز ۵+

## رفتار اجباری Claude در پروتکل تعویض چت (🆕 v2.5)

طبق قانون #20 و سند ۱۴.۵:

1. در **پایان هر چت**، Claude اول دستور اجرای `scripts/00_cleanup_for_zip.py` را در 🟩 tab «2 scripts» می‌دهد.
2. در **ابتدای چت جدید**، اگر `trading-system.zip` حاوی `venv\`, `node_modules\`, `__pycache__\`, `*.log`, `*.db` بود، یادآوری اجرای اسکریپت بالا را می‌دهد.

## تصمیمات معماری تأییدشده

### Session 1-4: ۳۹ تصمیم (در سند جامع v2.5 ثبت)

### Session 5 (این چت): ۹ تصمیم جدید + ۲ Bug Fix + ۳ قانون

40. حذف passlib، bcrypt مستقیم
41. bump v0.1.3 → v0.2.0
42. Frontend stack (Vite + React + Zustand + Router + axios + lightweight-charts)
43. JWT در localStorage با Zustand persist (فاز ۰)
44. OAuth2PasswordRequestForm + python-multipart
45. JWT deterministic — پذیرفته‌شده
46. python-multipart==0.0.9
47. bcrypt==4.1.3
48. **🆕 اسکریپت `00_cleanup_for_zip.py` + قانون #20**
- Bug #38: APP_VERSION در .env
- Bug #39: passlib + bcrypt 4.x
- قانون #17 توسعه: ایموجی رنگی
- قانون #19: تست از ترمینال
- قانون #20: پاک‌سازی خودکار

## وضعیت داده DB

- **Users:** ۱ (admin / bcrypt-hashed `1`)
- **Sessions:** ۱+ (هر login یک رکورد refresh token)
- **Exchanges:** ۱ (`Excel`, ccxt_id=`excel`)
- **Symbols:** ۱ (`BTC/USDT` روی Excel)
- **OhlcvData:** **1714 کندل** BTC/USDT روزانه (2017-08-17 → 2022-04-26)
- **Migration head:** `08348dca2b9a`

## API Endpoints پیاده‌سازی‌شده (v2.5)

| Method | Endpoint | Auth |
|---|---|---|
| GET | `/api/v1/health` | ❌ |
| POST | `/api/v1/auth/login` | ❌ |
| POST | `/api/v1/auth/refresh` | ❌ |
| POST | `/api/v1/auth/logout` | ✅ |
| GET | `/api/v1/auth/me` | ✅ |
| GET | `/api/v1/ohlcv/{symbol_id}` | ✅ |

## Frontend Pages پیاده‌سازی‌شده (v2.5)

| مسیر | Component | محافظت |
|---|---|---|
| `/login` | `LoginPage.jsx` | ❌ |
| `/` | `HomePage.jsx` | ✅ |
| `/chart/:symbolId` | `ChartPage.jsx` | ✅ |

## سند مرجع

- **سند جامع فعلی:** v2.5 (نسخه lite — ~92KB)
- **اولویت در صورت تناقض:** سند جامع v2.5 > SESSION_STATUS > PROJECT_CONTEXT > zip

## مسیرهای فایل‌های مرجع

- `D:\Projects\trading-system\docs\SESSION_STATUS.md`
- `D:\Projects\trading-system\docs\PROJECT_CONTEXT.md`
- `D:\Projects\trading-system\scripts\00_cleanup_for_zip.py` 🆕 — ابزار پاک‌سازی
- سند جامع v2.5 به‌عنوان فایل پیوست در چت‌ها استفاده می‌شود
