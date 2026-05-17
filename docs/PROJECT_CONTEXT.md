# 🗂️ PROJECT_CONTEXT — Context پروژه برای Claude

> **هدف یک‌خطی:** خلاصه‌سازی سریع context پروژه برای Claude در هر چت — تا با یک نگاه بداند کجاست.

> **محل قرارگیری:** `docs/PROJECT_CONTEXT.md`  
> **به‌روز توسط:** Claude در پایان چت اگر تغییر اساسی  
> **نسخه:** v0.5.0 (2026-05-17)

---

## 📌 معرفی پروژه

**نام:** سامانه هوشمند ترید (Intelligent Trading System)  
**دامنه:** تحلیل و معامله ارز دیجیتال + فارکس  
**حالت توسعه:** فاز ۰ تکمیل، آماده فاز ۱  
**زبان UI:** فارسی (RTL)  
**کاربر هدف:** معامله‌گر شخصی (single-user در فاز ۰، multi-user در فاز ۸)

---

## 🛠️ Stack فعال

### Backend
| ابزار | نسخه | نقش |
|---|---|---|
| Python | 3.11+ | runtime |
| FastAPI | 0.115+ | web framework |
| SQLAlchemy | 2.0+ async | ORM |
| Alembic | latest | migrations |
| Pydantic | 2.x | validation |
| Loguru | latest | logging |
| bcrypt | direct | password hashing |
| python-jose | latest | JWT |
| SQLite | 3.x | DB (فاز ۰) |

### Frontend
| ابزار | نسخه | نقش |
|---|---|---|
| Node.js | 22 LTS | runtime |
| React | 18 | UI |
| Vite | 8.x | bundler |
| react-router-dom | latest | routing |
| zustand | 4.5+ | state management |
| axios | latest | HTTP client |
| lightweight-charts | latest | nمودار |
| Vazirmatn | CDN | فونت |

---

## 📁 مسیرها

```
D:\Projects\trading-system\        ← root پروژه (در ماشین کاربر)
├── backend/
│   ├── app/                       ← کد backend
│   ├── alembic/                   ← migrations
│   ├── venv/                      ← virtual env (در .gitignore)
│   ├── trading.db                 ← DB (در .gitignore — توسط 00b ساخته می‌شود)
│   ├── .env                       ← config (در .gitignore)
│   ├── .env.example               ← نمونه
│   └── requirements.txt
├── frontend/
│   ├── src/                       ← کد frontend
│   ├── node_modules/              ← (در .gitignore)
│   └── package.json
├── scripts/                       ← اسکریپت‌های Python خودکار
│   ├── 00b_post_unzip_setup.py
│   ├── 01_*.py تا 33_*.py
│   └── Nb_test_*.py
└── docs/                          ← اسناد ۱۲گانه
    ├── سند_جامع_v2_7.md          ⭐ Constitution
    ├── PROJECT_GOVERNANCE.md     ⭐
    ├── CLAUDE_CHECKLIST.md       ⭐
    ├── CHAT_LOG.md               ⭐
    ├── TASK_BACKLOG.md           ⭐
    ├── DECISIONS_LOG.md          ⭐
    ├── REUSABLE_SKELETON.md      ⭐
    ├── ONBOARDING_GUIDE.md       ⭐
    ├── STYLE_GUIDE.md
    ├── GLOSSARY.md
    ├── TROUBLESHOOTING.md
    ├── PROJECT_CONTEXT.md        ← این فایل
    └── SESSION_STATUS.md
```

---

## 🔑 قوانین کلیدی (خلاصه ۲۶ قانون)

**اساسی:**
- **#۱:** هر فایل Python با `# -*- coding: utf-8 -*-` شروع شود
- **#۲:** فقط async DB calls (نه sync)
- **#۳:** Repository pattern برای queries (نه query در routes)
- **#۴:** Standard Response model در همه endpoint ها

**Frontend:**
- **#۵:** بدون hex hardcoded — همه از CSS variables تم
- **#۶:** fontSize با rem (نه px ثابت) — Bug #47
- **#۷:** Variant Indicator Pattern برای کامپوننت‌های typed
- **#۸:** Interactive States الزامی (hover/active/focus-visible/disabled)

**Process:**
- **#۲۰:** Claude در پایان چت zip + سند v(N+1) می‌سازد
- **#۲۱:** هر چیز قابل تست با کد، با کد تست شود (نه Swagger UI)
- **#۲۲:** هر اسکریپت `{N}_*.py` باید `{N}b_test_*.py` همراه داشته باشد

**Governance (جدید v2.7):**
- **#۲۳:** هر چت، CHAT_LOG با بخش جدید آپدیت شود
- **#۲۴:** سند جامع فقط افزوده/اصلاح — **هرگز حذف نمی‌شود**
- **#۲۵:** Claude در شروع چت چک‌لیست ۸ مرحله را اجرا کند
- **#۲۶:** تغییرات اسناد به‌صورت اتمیک اعمال شوند

**فهرست کامل:** سند جامع v2.7 — بخش ۱.۹.

---

## 🎨 طراحی

- **۵ تم** پیش‌فرض: binance-dark (default)، light-minimal، dark-modern، pastel، sky-blue
- **رنگ‌های دقیق Binance** در تم پیش‌فرض
- **Variant Indicator Pattern** (سند ۸.۸.۱): کانتینر از تم + accent ۴px + icon رنگی
- **Interactive States** (سند ۸.۷.۱): تمام عناصر تعاملی باید feedback داشته باشند
- **فرمت تاریخ**: شمسی (پیش‌فرض) یا میلادی با ۴ گزینه

---

## 💻 CMDهای پرتکرار

### Backend (🟦 tab 1)
```cmd
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### Scripts (🟩 tab 2)
```cmd
cd D:\Projects\trading-system
venv\Scripts\activate
python scripts/N_xxx.py
python scripts/Nb_test_xxx.py
```

### Frontend (🟧 tab 3)
```cmd
cd frontend
npm run dev
# → http://localhost:5173
```

### Setup اولیه (هر بار unzip جدید)
```cmd
python scripts/00b_post_unzip_setup.py
```

---

## 🏛️ معماری

### Backend — Layered
```
HTTP Request
   ↓ FastAPI route
routes/ (endpoint, validation)
   ↓ optional service layer
services/ (business logic)
   ↓ DB access
repositories/ (queries — هیچ‌جای دیگر)
   ↓ ORM
models/ (SQLAlchemy schema)
   ↓
SQLite (فاز ۰) / PostgreSQL (فاز ۲+)
```

### Frontend — Component + Stores
```
pages/             ← یک per route
   ↓ استفاده از
components/common/ ← Toast, Dialog, Skeleton, ...
   ↓ state
stores/ (Zustand)  ← auth, theme, toast, confirm, preferences
   ↓ API
services/api.js    ← axios + JWT interceptor
```

### Theme System
```
themes/themes.js → themeStore → ThemeProvider → :root { --color-X } → Components
```

---

## 🔐 Auth

- **JWT** با expire ۷ روز
- **localStorage** برای token (فاز ۰)
- **bcrypt** برای password
- **OAuth2 password flow** برای login
- **Dependencies**: `current_user`, `current_admin`
- **Default user**: `admin` / `1` (فقط در dev — قابل تغییر در `.env`)

---

## 📡 API Endpoints موجود

| Method | Path | محافظت | نقش |
|---|---|---|---|
| GET | `/health` | عمومی | health check |
| POST | `/auth/login` | عمومی | login، توکن JWT |
| POST | `/auth/logout` | JWT | logout |
| GET | `/auth/me` | JWT | اطلاعات کاربر |
| GET | `/ohlcv/{symbol_id}` | JWT | داده شمعی |

**جزئیات کامل:** سند جامع v2.7 — سند ۶.

---

## 📋 تصمیمات معماری تأییدشده (خلاصه)

برای فهرست کامل ۵۴ تصمیم: `docs/DECISIONS_LOG.md`.

**مهم‌ترین:**
- **#1:** FastAPI + React + Vite + zustand + SQLAlchemy
- **#2:** Repository Pattern (همه queries در repos)
- **#3:** DataSource Abstraction (Excel در فاز ۰، CCXT در فاز ۱)
- **#4:** Layered Architecture
- **#13:** bcrypt مستقیم (نه passlib)
- **#34:** Variant Indicator Pattern
- **#50:** preferencesStore جدا از themeStore
- **#52:** Intl built-in (نه moment-jalaali)
- **#53:** rem برای fontSize
- **#54:** Governance Infrastructure ۱۲-سندی ⭐
- **#55:** ErrorBoundary defense-in-depth (root + per-route)
- **#56:** Vitest به‌جای Jest برای frontend tests
- **#57:** ARCHITECTURE.md یک فایل واحد (نه چند فایل در `architecture/`)

---

## 📊 وضعیت پروژه

**فاز:** ۰ — **تکمیل ۱۰۰٪** ✅ + Tier 2 (Quality Hardening): **۴/۹ تکمیل (~۴۴٪)**  
**نسخه پروژه:** v0.5.0  
**نسخه سند جامع:** v2.7  
**آخرین چت:** `TRADING-phase0-part06-quality-hardening` (2026-05-17)

**فاز بعدی پیشنهادی:** ادامه Tier 2 (T2.05-T2.09: Git workflow audit، Pre-commit hooks، Anti-pattern catalog، Backend test coverage، API_DOCS) یا پرش به فاز ۱ (CCXT + WebSocket).

**سند معماری:** `docs/ARCHITECTURE.md` — high-level فنی با ۶ دیاگرام Mermaid ⭐

---

## 🎯 برای Claude

اگر شما Claude هستید:
- **اول:** چک‌لیست شروع چت در `CLAUDE_CHECKLIST.md` فاز ۱
- **دوم:** خواندن `SESSION_STATUS.md` و `CHAT_LOG.md` (به‌خصوص چت ۷)
- **سوم:** صبر برای تأیید کاربر قبل از هر کار

---

## 📌 پایان PROJECT_CONTEXT

**نسخه:** v0.5.0 (2026-05-17 — پایان چت ۷)
