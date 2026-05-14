# Context پروژه — سامانه هوشمند ترید

> این فایل در ابتدای هر Session جدید همراه با SESSION_STATUS.md
> به Claude ارائه می‌شود.

## Stack فعال

- **Backend:** FastAPI 0.111 + Python 3.11.2 + SQLAlchemy 2.0 (async) + SQLite
- **Frontend:** React 18 + Vite + Zustand 4.5.2 + lightweight-charts 4.1.7
- **Database:** SQLite (trading.db)
- **Node.js:** 22 LTS

## مسیرها

- Root: `D:\Projects\trading-system`
- Backend: `D:\Projects\trading-system\backend`
- Frontend: `D:\Projects\trading-system\frontend`
- Scripts: `D:\Projects\trading-system\scripts`

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

- **CMD 1:** Backend → `cd backend && venv\Scripts\activate && uvicorn main:app --reload`
- **CMD 2:** Frontend → `cd frontend && npm run dev`
- **CMD 3:** Scripts → `cd D:\Projects\trading-system && python scripts\<filename>`

## وضعیت فعلی فاز ۰

- ✅ گام ۱: ساختار پوشه + Git + اسناد Session
- ⏳ گام ۲: venv + requirements + main.py
- ⏳ گام ۳: Core Layer
- ⏳ گام ۴: Database + Migrations
- ⏳ گام ۵: Auth + JWT
- ⏳ گام ۶: DataSource Abstraction + Excel Import
- ⏳ گام ۷: Frontend پایه
- ⏳ گام ۸: کامپوننت‌های مشترک
