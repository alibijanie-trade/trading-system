# 📊 سامانه هوشمند ترید

> سامانه‌ای حرفه‌ای و ماژولار برای تحلیل و معامله ارز دیجیتال — با تمرکز بر کیفیت کد، طراحی حرفه‌ای، و حافظه پروژه قابل ادامه.

---

## ✨ ویژگی‌های کلیدی

- 🎨 **۵ تم** قابل تنظیم با Variant Indicator Pattern (Binance accurate)
- 📊 **نمودار شمعی** با lightweight-charts + تقویم شمسی/میلادی
- 🔐 **Auth** کامل با JWT + bcrypt + OAuth2 password flow
- 🌐 **API** RESTful با FastAPI + OpenAPI خودکار
- 💾 **DataSource Abstraction** — Excel در فاز ۰، CCXT در فاز ۱
- 🎯 **Theme Engine** سراسری + Settings Page با ۳ بخش
- 📅 **تقویم شمسی** با `Intl` built-in (بدون کتابخانه خارجی)
- 🔢 **جداکننده سه‌رقمی** + ۴ فرمت تاریخ میلادی
- 📋 **Governance modular** — Constitution v2.18 (main + ۷ ماژول) + MDRS v2 + قانون تداوم دوحلقه‌ای برای handoff حرفه‌ای

---

## 🚀 شروع سریع

### پیش‌نیازها

- **Python** 3.11 یا بالاتر
- **Node.js** 22 LTS
- **Git** (برای version control)

### راه‌اندازی در ۳ دقیقه

```cmd
# 1. unzip یا clone پروژه
cd trading-system

# 2. اجرای اسکریپت magic — همه چیز را خودکار راه‌اندازی می‌کند
python scripts/00b_post_unzip_setup.py

# 3. فعال‌سازی venv (Windows)
venv\Scripts\activate

# 4. اجرای backend (tab «1»)
cd backend
uvicorn app.main:app --reload --port 8000

# 5. اجرای frontend (tab «3»، در ترمینال جدید)
cd frontend
npm run dev

# 6. مرورگر → http://localhost:5173
# Login: admin / 1
```

---

## 📁 ساختار پروژه

```
trading-system/
├── backend/              ← FastAPI server
│   ├── app/
│   │   ├── api/v1/routes/    ← endpoint files
│   │   ├── auth/             ← JWT, bcrypt, dependencies
│   │   ├── config/           ← settings.py
│   │   ├── core/             ← logger, exceptions, response
│   │   ├── database/         ← async SQLAlchemy
│   │   ├── infrastructure/   ← DataSource pattern
│   │   ├── models/           ← SQLAlchemy models
│   │   ├── repositories/     ← DB query layer
│   │   └── main.py
│   ├── alembic/              ← migrations
│   ├── .env                  ← config (در .gitignore)
│   └── requirements.txt
│
├── frontend/             ← React + Vite app
│   ├── src/
│   │   ├── components/       ← UI components
│   │   │   ├── common/       ← Toast, ConfirmDialog, ...
│   │   │   └── settings/     ← ThemeCard, FontSizeControl, ...
│   │   ├── pages/            ← Login, Home, Chart, Settings
│   │   ├── stores/           ← Zustand state
│   │   ├── services/         ← axios client
│   │   ├── themes/           ← ۵ تم
│   │   ├── utils/            ← formatNumber, formatDate
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
│
├── scripts/              ← Python automation
│   ├── 00b_post_unzip_setup.py  ← راه‌اندازی خودکار
│   ├── 01_*.py تا 32_*.py
│   └── Nb_test_*.py            ← تست‌ها (قانون #۲۲)
│
└── docs/                 ← اسناد جامع
    ├── constitution/         ← Constitution v2.18 (Modular) ⭐
    ├── CHAT_LOG.md           ⭐
    ├── TASK_BACKLOG.md       ⭐
    ├── DECISIONS_LOG.md      ⭐
    ├── REUSABLE_SKELETON.md  ⭐
    ├── ONBOARDING_GUIDE.md   ⭐
    ├── SESSION_STATUS.md
    ├── STYLE_GUIDE.md
    ├── GLOSSARY.md
    ├── TROUBLESHOOTING.md
    ├── PENDING_FOR_NEXT_VERSION.md
    └── reviews/
```

---

## 📚 اسناد مرجع

### من برنامه‌نویس جدید هستم
→ از **`docs/ONBOARDING_GUIDE.md`** شروع کنید (۴-۶ ساعت).

### من می‌خواهم پروژه را با Claude ادامه دهم
→ **`docs/constitution/main.md`** (Constitution v2.18) را بخوانید + boot protocol در `claude_workspace/CHAT_BOOT_TRIGGER_TEMPLATE.md`.

### می‌خواهم بدانم چه task هایی باقی‌مانده
→ **`docs/TASK_BACKLOG.md`**.

### Bug پیدا کردم
→ **`docs/TROUBLESHOOTING.md`** را اول جستجو کنید.

### می‌خواهم پروژه جدیدی شروع کنم
→ **`docs/REUSABLE_SKELETON.md`**.

### اصطلاحی نا‌آشناست
→ **`docs/GLOSSARY.md`**.

---

## 🎯 فاز فعلی

**فاز ۰ — زیرساخت — ✅ ۱۰۰٪ تکمیل**

| زیرگام | وضعیت |
|---|---|
| ۱ — Project Setup | ✅ |
| ۲ — Backend Core | ✅ |
| ۳ — Database + Models | ✅ |
| ۴ — Auth + API | ✅ |
| ۵ — Frontend Scaffold | ✅ |
| ۶ — Login + Routing | ✅ |
| ۷ — ChartPage | ✅ |
| ۸.۱ — Theme Engine | ✅ |
| ۸.۲ — Toast Notifications | ✅ |
| ۸.۳ — Skeleton + ConfirmDialog | ✅ |
| ۸.۴ — Settings Page | ✅ |
| ۸.۵ — Numeric + Persian Calendar | ✅ |
| Governance Infrastructure | ✅ |

**فاز بعدی:** Tier 2 (Quality Hardening) یا فاز ۱ (CCXT + WebSocket).

---

## 🛠️ Stack

### Backend
- **FastAPI** 0.115+ — web framework
- **SQLAlchemy** 2.0+ async — ORM
- **Alembic** — migrations
- **Pydantic** 2.x — validation
- **Loguru** — logging
- **bcrypt** + **python-jose** — auth
- **SQLite** (فاز ۰) → **PostgreSQL** (فاز ۲+)

### Frontend
- **React** 19.2 + **Vite** 8
- **react-router-dom** — routing
- **zustand** — state management + persist
- **axios** — HTTP client
- **lightweight-charts** — charting
- **Vazirmatn** font (CDN)

### Tooling
- **Python** scripts برای automation
- **Node.js** برای runtime tests
- **Git** برای version control

---

## 🏛️ معماری

### Backend — Layered Architecture
```
HTTP Request
    ↓
routes/      ← endpoint definition، HTTP concerns
    ↓
services/    ← business logic (اگر پیچیده شد)
    ↓
repositories/ ← DB queries (هیچ‌جا غیر از اینجا)
    ↓
models/      ← SQLAlchemy schema
```

### Frontend — Component-based + Stores
```
pages/                  ← یک per route
    ↓ استفاده از
components/common/      ← Toast, ConfirmDialog, ...
components/<feature>/   ← مخصوص feature
    ↓ state از
stores/                 ← zustand stores
    ↓ API از
services/api.js         ← axios + interceptors
```

### Theme System
```
themes/themes.js          ← تعریف ۵ تم
    ↓
themeStore (zustand)      ← تم فعال + fontSize
    ↓
ThemeProvider             ← تزریق CSS vars به :root
    ↓
:root { --color-...: ... } ← متغیرها در دسترس همه کامپوننت‌ها
    ↓
Components                ← style={{ color: "var(--color-primary)" }}
```

---

## 📜 قوانین کلیدی

این پروژه **۹۰ قانون قفل‌شده** دارد که در **Constitution v2.18 (Modular)** ثبت شده‌اند. ساختار مدولار در `docs/constitution/`:

- [`main.md`](docs/constitution/main.md) — فهرست و navigation
- [`01a_rules_core.md`](docs/constitution/01a_rules_core.md) — ۹۰ قانون Locked (بوت-کریتیکال)
- [`01_rules.md`](docs/constitution/01_rules.md) — شرح مفصل قوانین (on-demand)
- [`02_lessons.md`](docs/constitution/02_lessons.md) — درس‌نامه M1-M110
- [`03_bugs.md`](docs/constitution/03_bugs.md) — Bug catalog
- [`04_principles.md`](docs/constitution/04_principles.md) — ۸ اصل بنیادی
- [`05_architecture.md`](docs/constitution/05_architecture.md) — Stack و معماری
- [`06_meta.md`](docs/constitution/06_meta.md) — Session و Templates و Tooling

مهم‌ترین قوانین:

- **#۱:** هر فایل Python باید با `# -*- coding: utf-8 -*-` شروع شود
- **#۲۱:** هر چیز قابل تست با کد، با کد تست شود (نه Swagger UI)
- **#۲۲:** هر اسکریپت `{N}_*.py` باید `{N}b_test_*.py` همراه داشته باشد
- **#۲۳:** هر چت، CHAT_LOG با بخش جدید آپدیت شود
- **#۲۴:** Constitution فقط افزوده/اصلاح می‌شود — **هرگز حذف نمی‌شود** (No-Deletion)
- **#۲۵:** Claude در شروع چت چک‌لیست ۸ مرحله را انجام دهد
- **#۲۶:** تغییرات اسناد به‌صورت اتمیک اعمال شوند
- **#۶۰ ⭐⭐⭐:** PENDING-EOC در لحظه در `docs/PENDING_FOR_NEXT_VERSION.md` ثبت شود
- **#۶۶ ⭐⭐⭐ 🆕 v2.12:** Push اجباری در پایان هر چت (در branch infra/، پس از هر commit)

برای لیست کامل: **`docs/constitution/01_rules.md`** (بخش ۱.۹ جدول authoritative).

---

## 🎨 طراحی

پروژه از **Variant Indicator Pattern** (Constitution ۰۵_architecture) پیروی می‌کند:

- کانتینر همیشه از `var(--color-card)` + `var(--color-border)`
- نوع (danger/warning/info) فقط با **accent باریک ۴px** + icon رنگی
- **هرگز:** کادر کامل با رنگ نوع

```jsx
// ✅ صحیح
<div style={{
  background: "var(--color-card)",
  borderInlineStart: "4px solid var(--color-warning)",
}}>

// ❌ ممنوع
<div style={{ background: "var(--color-warning)" }}>
```

---

## 🐛 اگر مشکلی پیش آمد

1. **اول:** `docs/TROUBLESHOOTING.md` را جستجو کنید
2. **دوم:** اسکریپت‌های `Nb_test_*.py` را اجرا کنید
3. **سوم:** logs در `backend/logs/` را چک کنید
4. **چهارم:** برای مشکلات محیطی (npm install، venv): `python scripts/00b_post_unzip_setup.py` را دوباره اجرا کنید

---

## 🤝 توسعه با Claude

این پروژه با Claude AI به‌صورت تعاملی توسعه یافته. در هر چت جدید:

1. **`claude_workspace/CHAT_BOOT_TRIGGER_TEMPLATE.md`** را بخوانید و دستورات boot را به Claude بدهید
2. Claude خودکار:
   - فایل‌های boot را می‌خواند
   - وضعیت فعلی را گزارش می‌دهد
   - گزینه‌های گام بعدی را ارائه می‌دهد

**جزئیات کامل:** `docs/constitution/main.md` بخش سسیون و متا.

---

## 📊 آمار پروژه

| متریک | مقدار |
|---|---|
| چت‌های انجام‌شده | ۲۳+ (تا part23) |
| اسکریپت‌های idempotent | ~۶۴ |
| اسکریپت‌های تست همراه | ~۴۰ |
| Bug های رفع‌شده | ۵۴ (#۱‌-۵۴ با ۳ Reserved: #۵۰-۵۲) |
| تصمیمات معماری ثبت‌شده | ۷۱ (Max ID) |
| **قوانین قفل‌شده** | **۹۰** (#۱-۹۰) |
| **درس‌نامه ردیف‌ها** | M1-M110 |
| **نسخه Constitution** | **v2.18 (Modular)** |
| تم‌های built-in | ۵ |
| اسناد مرجع | ۸ (ماژول‌های modular constitution) + governance docs |
| Lines of code (frontend) | ~۲۵۰۰ |
| Lines of code (backend) | ~۳۰۰۰ |
| Bundle size (gzipped) | ~۱۴۴KB |
| GitHub | `alibijanie-trade/trading-system` (Private) |

---

## 📝 License

(در فاز فعلی تعیین نشده — پروژه شخصی)

---

## 🙏 سپاسگزاری

این پروژه با همکاری انسان و Claude AI ساخته شده. هر اسکریپت، هر تصمیم، هر تم در نتیجه یک گفتگوی دقیق و حرفه‌ای شکل گرفته.

---

**نسخه فعلی:** v0.6.0 (Constitution v2.18 Modular)
**فاز:** ۰ تکمیل‌شده + فاز ۱ skeleton
**برنچ جاری:** `infra/v2.14-source-of-truth`
**به‌روز:** 2026-06-24
