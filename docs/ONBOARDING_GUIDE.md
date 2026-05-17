# 🚀 ONBOARDING_GUIDE — راهنمای برنامه‌نویس جدید

> **هدف یک‌خطی:** اگر شما برنامه‌نویس جدیدی هستید که این پروژه به شما واگذار شده — این سند شما را در یک روز کاری مسلط می‌کند.

> **محل قرارگیری:** `docs/ONBOARDING_GUIDE.md`  
> **مخاطب:** برنامه‌نویس جدید (Python + React)  
> **زمان مطالعه + اجرا:** ۴-۶ ساعت  
> **نسخه:** v1.0 (2026-05-17)

---

## 📑 فهرست

- [خوش‌آمدید](#خوشآمدید)
- [مرحله ۱ — ۳۰ دقیقه: نگاه کلی](#مرحله-۱--۳۰-دقیقه-نگاه-کلی)
- [مرحله ۲ — ۱ ساعت: راه‌اندازی محلی](#مرحله-۲--۱-ساعت-راهاندازی-محلی)
- [مرحله ۳ — ۲ ساعت: مطالعه اسناد](#مرحله-۳--۲-ساعت-مطالعه-اسناد)
- [مرحله ۴ — ۱ ساعت: گشت در کد](#مرحله-۴--۱-ساعت-گشت-در-کد)
- [مرحله ۵ — ۳۰ دقیقه: اولین تغییر](#مرحله-۵--۳۰-دقیقه-اولین-تغییر)
- [Cheat Sheet دستورات](#cheat-sheet-دستورات)
- [۱۰ سؤال متداول روز اول](#۱۰-سؤال-متداول-روز-اول)

---

## خوش‌آمدید

سلام! 👋

این یک پروژه **سامانه هوشمند ترید** است، با backend Python (FastAPI) و frontend React. خواست این است که شما در **یک روز کاری** به سطحی برسید که بتوانید کار را ادامه دهید.

پروژه با Claude AI به‌صورت تعاملی توسعه یافته. هر چت یک "نشست کاری" است که در پایانش یک zip به‌روز تولید می‌شود. شما در نقش "ادامه‌دهنده" می‌توانید با خواندن اسناد، **دقیقاً بدانید پروژه کجا ایستاده**.

### نکته بسیار مهم — Governance

این پروژه ساختار اداره (Governance) سختگیرانه‌ای دارد. **قبل از هر تغییر در کد**، باید `PROJECT_GOVERNANCE.md` و `CLAUDE_CHECKLIST.md` را خوانده باشید. نه فقط برای style — برای جلوگیری از خراب کردن کار قبلی.

---

## مرحله ۱ — ۳۰ دقیقه: نگاه کلی

### قدم ۱.۱ — خواندن README

```
README.md (در root پروژه)
```

این به شما می‌گوید:
- پروژه چیست
- Stack
- چگونه راه‌اندازی کنید

### قدم ۱.۲ — درک ساختار پوشه

```
trading-system/
├── backend/           ← FastAPI server
│   ├── app/
│   │   ├── api/v1/routes/   ← endpoint ها
│   │   ├── auth/            ← JWT, bcrypt
│   │   ├── config/          ← settings.py
│   │   ├── core/            ← logger, exceptions
│   │   ├── database/        ← async SQLAlchemy
│   │   ├── infrastructure/  ← DataSource pattern
│   │   ├── models/          ← SQLAlchemy models
│   │   ├── repositories/    ← DB queries
│   │   └── main.py
│   ├── alembic/             ← migrations
│   └── .env
│
├── frontend/          ← React app
│   ├── src/
│   │   ├── components/      ← UI components
│   │   ├── pages/           ← صفحات
│   │   ├── stores/          ← Zustand state
│   │   ├── services/        ← API client
│   │   ├── themes/          ← ۵ تم
│   │   ├── utils/           ← formatNumber, formatDate
│   │   ├── App.jsx          ← Routes
│   │   └── main.jsx
│   └── package.json
│
├── scripts/           ← Python automation
│   ├── 00b_post_unzip_setup.py  ← راه‌اندازی خودکار
│   ├── 01_*.py تا 32_*.py       ← اسکریپت‌های توسعه
│   └── 27b_test_*.py             ← تست‌ها (قانون #۲۲)
│
└── docs/              ← اسناد پروژه
    ├── PROJECT_GOVERNANCE.md     ⭐ راهبردی
    ├── CLAUDE_CHECKLIST.md       ⭐ چک‌لیست
    ├── CHAT_LOG.md               ⭐ تاریخچه چت‌ها
    ├── TASK_BACKLOG.md           ⭐ TODO ها
    ├── DECISIONS_LOG.md          ⭐ تصمیمات معماری
    ├── REUSABLE_SKELETON.md      ⭐ template
    ├── GLOSSARY.md
    ├── TROUBLESHOOTING.md
    ├── STYLE_GUIDE.md
    ├── ONBOARDING_GUIDE.md       ⭐ این سند
    ├── PROJECT_CONTEXT.md
    └── SESSION_STATUS.md
```

### قدم ۱.۳ — دیدن CHANGELOG

```
CHANGELOG.md
```

به شما می‌گوید کدام نسخه‌ها کجا بودند.

---

## مرحله ۲ — ۱ ساعت: راه‌اندازی محلی

### پیش‌نیازها

- Python 3.11+
- Node.js 22 LTS
- Git (برای version control)

### قدم ۲.۱ — Clone یا Unzip

```cmd
# اگر zip دارید:
unzip trading-system.zip
cd trading-system

# اگر git:
git clone <repo-url> trading-system
cd trading-system
```

### قدم ۲.۲ — اجرای 00b

این یک اسکریپت "magic" است که همه چیز را راه‌اندازی می‌کند:

```cmd
python scripts/00b_post_unzip_setup.py
```

این اسکریپت:
- venv می‌سازد
- pip install با fallback به mirror ایران
- npm install با fallback
- DB می‌سازد و seed می‌کند
- در صورت موفقیت، گزارش می‌دهد

**زمان:** ۳-۸ دقیقه بسته به سرعت اینترنت.

### قدم ۲.۳ — اجرای Backend

```cmd
# tab «1 backend»
cd backend
venv\Scripts\activate    # Windows
# source venv/bin/activate   # Linux/Mac

uvicorn app.main:app --reload --port 8000
```

**انتظار:**
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**تست:** در مرورگر `http://localhost:8000/health` → پاسخ JSON.

### قدم ۲.۴ — اجرای Frontend

```cmd
# tab «3 frontend»
cd frontend
npm run dev
```

**انتظار:**
```
  VITE v8.x  ready in 500 ms
  ➜  Local:   http://localhost:5173/
```

### قدم ۲.۵ — Login و گردش اولیه

1. مرورگر: `http://localhost:5173`
2. Login با:
   - Username: `admin`
   - Password: `1`
3. HomePage باز شد
4. کلیک ⚙️ → SettingsPage
5. تغییر تم: کلیک یک تم دیگر → آنی اعمال شود
6. تغییر فونت: بزرگ → همه چیز بزرگ
7. تغییر تقویم: شمسی → preview شمسی
8. برگشت `/` → کلیک "BTC/USDT — روزانه"
9. نمودار شمعی نمایش داده شود
10. hover روی شمعی → tooltip تاریخ + قیمت

✅ **اگر همه این مراحل کار کردند، شما آماده‌اید.**

---

## مرحله ۳ — ۲ ساعت: مطالعه اسناد

به ترتیب، با وقفه برای فکر:

### قدم ۳.۱ — Governance (۳۰ دقیقه) ⭐ مهم‌ترین

```
docs/PROJECT_GOVERNANCE.md
```

این سند **مهم‌ترین** سند است. شامل:
- اصول بنیادی پروژه (۶ اصل قفل‌شده)
- معماری ۱۲ سند
- protocol شروع/پایان چت
- Anti-Patterns ممنوع (A1-A10)
- Emergency Procedures

**سؤالی که باید بتوانید پاسخ دهید:**
- چرا hex hardcoded ممنوع است؟
- اگر یک Bug پیدا کردم، در کدام سند ثبت می‌شود؟
- اصل No-Deletion چیست؟

### قدم ۳.۲ — CHAT_LOG (۴۵ دقیقه)

```
docs/CHAT_LOG.md
```

این سند **داستان پروژه** است. ۶ چت تا کنون انجام شده. بخوانید:
- چت ۱ تا ۴ سریع (همه چیز پایه)
- چت ۵ با دقت بیشتر (Theme Engine)
- چت ۶ کامل (UI Polish + Governance — این‌جا بیشترین تغییر اخیر)

**سؤالی که باید بتوانید پاسخ دهید:**
- چه bug هایی در چت ۶ رفع شدند؟
- چرا Variant Indicator Pattern معرفی شد؟
- آخرین قانون اضافه‌شده چیست؟

### قدم ۳.۳ — Decisions (۲۰ دقیقه)

```
docs/DECISIONS_LOG.md
```

اگر کنجکاو "چرا"ها هستید، این سند را بخوانید. ۵۴ تصمیم با rationale.

### قدم ۳.۴ — TASK_BACKLOG (۱۵ دقیقه)

```
docs/TASK_BACKLOG.md
```

اینجا می‌بینید چه کارهایی باقی‌مانده. ۴ Tier:
- Tier 1: همه DONE
- Tier 2: شروع نشده (chat بعدی)
- Tier 3 و 4: بعدتر

**سؤال:** اولین task بعدی شما کدام است؟

### قدم ۳.۵ — Troubleshooting (۱۵ دقیقه)

```
docs/TROUBLESHOOTING.md
```

فقط نگاه کنید چه FAQ و چه Bug هایی موجود است. وقتی مشکل پیش آمد، اینجا اول جستجو کنید.

### قدم ۳.۶ — Glossary (۱۰ دقیقه)

```
docs/GLOSSARY.md
```

اصطلاحات نا‌آشنا را اینجا جستجو کنید.

### قدم ۳.۷ — Style Guide (۱۵ دقیقه)

```
docs/STYLE_GUIDE.md
```

قواعد code style. هر کد جدیدی که می‌نویسید، باید این قواعد را رعایت کند.

### قدم ۳.۸ — سند جامع (۳۰ دقیقه — overview، نه کامل)

```
سند_جامع_v2.7.md
```

این **constitution** پروژه است. در روز اول کافی است:
- فهرست را ببینید
- بخش‌های مهم با ⭐ را بخوانید
- بخش "تغییرات این نسخه" را ببینید

برای reference کامل، در طول کار به آن مراجعه می‌کنید.

---

## مرحله ۴ — ۱ ساعت: گشت در کد

### قدم ۴.۱ — Backend Tour

به ترتیب باز کنید:

```
1. backend/app/main.py        ← entry point
2. backend/app/config/settings.py  ← config
3. backend/app/core/logger.py      ← logging
4. backend/app/core/response.py    ← standard response
5. backend/app/database/connection.py ← async SQLAlchemy
6. backend/app/models/user.py      ← اولین model
7. backend/app/repositories/base.py ← BaseRepository
8. backend/app/auth/dependencies.py ← current_user
9. backend/app/api/v1/routes/auth.py ← login/me
10. backend/app/api/v1/routes/ohlcv.py ← endpoint domain
```

### قدم ۴.۲ — Frontend Tour

```
1. frontend/src/main.jsx          ← entry
2. frontend/src/App.jsx           ← routes
3. frontend/src/index.css         ← global styles (مهم!)
4. frontend/src/themes/themes.js  ← ۵ تم
5. frontend/src/stores/themeStore.js  ← Zustand pattern
6. frontend/src/components/common/ThemeProvider.jsx
7. frontend/src/components/common/ConfirmDialog.jsx  ← Variant Pattern
8. frontend/src/utils/dateFormat.js   ← Intl pattern
9. frontend/src/pages/LoginPage.jsx   ← اولین page
10. frontend/src/pages/SettingsPage.jsx ← composition
```

### قدم ۴.۳ — Scripts Tour

```
1. scripts/00b_post_unzip_setup.py  ← مهم! این را خوب بخوانید
2. scripts/29_skeleton_confirm.py   ← یک اسکریپت idempotent مثال
3. scripts/29b_test_skeleton_confirm.py ← یک اسکریپت تست مثال
```

**مفاهیم کلیدی که در اسکریپت‌ها می‌بینید:**
- `write_if_changed()` — idempotency
- regex transforms
- Path.as_uri() (نه as_posix)
- runtime test با Node.js

---

## مرحله ۵ — ۳۰ دقیقه: اولین تغییر

اکنون که آماده هستید، یک تغییر کوچک انجام دهید تا workflow را تجربه کنید.

### پروژه کوچک: افزودن نام خود به HomePage

#### قدم ۵.۱ — افزودن متن شخصی

`frontend/src/pages/HomePage.jsx` را باز کنید.

پیدا کنید:
```jsx
<h1 style={{ fontSize: "1.57rem", marginBottom: 4, fontWeight: 600 }}>
  سامانه هوشمند ترید
</h1>
```

بعد از آن یک خط اضافه کنید:
```jsx
<div style={{ fontSize: "0.86rem", color: "var(--color-text-muted)" }}>
  توسعه: {YOUR_NAME}
</div>
```

#### قدم ۵.۲ — تست در مرورگر

Frontend در حال اجراست. به مرورگر برگردید — Vite HMR خودکار refresh می‌کند. نام شما باید زیر عنوان دیده شود.

#### قدم ۵.۳ — اعتبارسنجی Style Guide

چک کنید:
- ✅ آیا hex hardcoded ندارید؟ (همه از `var(--...)`)
- ✅ آیا fontSize با rem است؟ (نه عدد ثابت)
- ✅ آیا روی همه ۵ تم خوب دیده می‌شود؟ (تست با ⚙️ → تغییر تم)

### پروژه کوچک ۲: اضافه کردن یک Toast

در `HomePage.jsx`:

```jsx
import useToastStore from "../stores/toastStore.js";

// در داخل کامپوننت:
const toastSuccess = useToastStore((s) => s.success);

// در jsx، یک دکمه:
<button
  onClick={() => toastSuccess("سلام " + YOUR_NAME)}
  style={{
    padding: "8px 16px",
    background: "var(--color-primary)",
    color: "var(--color-text-inverse)",
    borderRadius: 4,
    fontSize: "0.93rem",
    fontWeight: 500,
  }}
>
  سلام بگو
</button>
```

کلیک → Toast سبز ظاهر می‌شود.

✅ **اگر این کار کرد، شما به‌خوبی onboard شده‌اید!**

---

## Cheat Sheet دستورات

### Backend
```cmd
# فعال‌سازی venv
cd backend
venv\Scripts\activate

# اجرای سرور
uvicorn app.main:app --reload --port 8000

# migration جدید
alembic revision --autogenerate -m "Add SomeModel"
alembic upgrade head

# تست با httpx
python scripts/Nb_test_xxx.py
```

### Frontend
```cmd
cd frontend

# اجرای dev server
npm run dev

# build production
npm run build

# نصب پکیج جدید
npm install some-package
```

### Scripts
```cmd
# (در root پروژه)
venv\Scripts\activate

# اجرای اسکریپت
python scripts/N_xxx.py

# تست
python scripts/Nb_test_xxx.py
```

### Database
```cmd
# دیدن schema
python -c "from app.database import Base; print([t.name for t in Base.metadata.tables.values()])"

# پشتیبان از DB
copy backend\trading.db backend\trading.db.backup

# بازنشانی DB
del backend\trading.db
python scripts/00b_post_unzip_setup.py
```

### Git (اگر استفاده می‌شود)
```cmd
git status
git add .
git commit -m "feat: add ..."
git push
```

---

## ۱۰ سؤال متداول روز اول

### Q1: من VS Code استفاده می‌کنم. تنظیمات خاصی نیاز است؟

پیشنهادی:
- Extension: Python, Pylance, ESLint, Prettier
- `.vscode/settings.json` (اختیاری) برای format on save

### Q2: چرا تست Backend با کد نه Swagger UI؟

طبق **قانون #۲۱** سند جامع. دلایل در `TROUBLESHOOTING.md` Q6 آمده.

### Q3: اگر یک Bug پیدا کردم، چه کنم؟

1. اول در `TROUBLESHOOTING.md` چک کنید (شاید قبلاً ثبت شده)
2. اگر جدید است:
   - اسکریپت `Nb_fix_xxx.py` بسازید (idempotent)
   - در پایان چت در `TROUBLESHOOTING.md` ثبت شود
   - شماره `#N` بگیرد

### Q4: اگر می‌خواهم feature جدید اضافه کنم؟

1. در `TASK_BACKLOG.md` چک کنید آیا قبلاً برنامه‌ریزی شده
2. اگر نه، یک TASK جدید با ID اضافه کنید
3. کار را شروع کنید (با Claude یا خودتان)
4. در پایان: ثبت در CHAT_LOG، TASK_BACKLOG، CHANGELOG

### Q5: می‌خواهم تم را عوض کنم.

`frontend/src/themes/themes.js` را باز کنید. هر تم یک object است. عوض کردن یا اضافه کردن ساده است.

### Q6: می‌خواهم زبان انگلیسی اضافه کنم.

این در `TASK_BACKLOG.md` به‌عنوان Tier 3 موجود است (T3.14-T3.17). فعلاً پروژه فارسی-only است.

### Q7: API هیچ docs ندارد؟

دارد. `http://localhost:8000/docs` Swagger UI خودکار. ولی **برای تست از اسکریپت httpx استفاده کنید**، نه manual.

### Q8: چطور با Claude کار کنم؟

نگاه کنید به `PROJECT_GOVERNANCE.md` بخش ۴ و ۵ (Protocol شروع و پایان چت). در ابتدای هر چت Claude باید چک‌لیست را اجرا کند.

### Q9: اگر در میانه کار Claude اشتباه کرد؟

کلمات Trigger در `CLAUDE_CHECKLIST.md`:
- "Governance" → یادآوری
- "چک‌لیست" → گزارش
- "E1: کیفیت" → پایان فوری

### Q10: می‌خواهم پروژه جدیدی شروع کنم با همین اسکلت.

نگاه کنید به `REUSABLE_SKELETON.md`. در پایان trading-system، یک template جدا استخراج می‌شود.

---

## چک‌لیست آمادگی برای ادامه کار

پس از یک روز کاری، شما باید بتوانید:

- [ ] پروژه را روی محیط محلی اجرا کنید
- [ ] Login کنید و در همه صفحات گردش کنید
- [ ] یک تغییر کوچک در frontend بکنید
- [ ] یک endpoint جدید در backend اضافه کنید
- [ ] اگر کسی پرسید "زیرگام ۸.۴ چیست؟" بدانید (Settings Page)
- [ ] اگر کسی پرسید "Bug #47 چیست؟" بدانید (Font scaling)
- [ ] اگر کسی پرسید "Variant Indicator Pattern چیست؟" بدانید
- [ ] بدانید TODO بعدی در `TASK_BACKLOG.md` چیست
- [ ] بدانید قانون #۲۱ و #۲۲ چه می‌گویند

---

## 🎉 خوش‌آمدگویی نهایی

اگر تا اینجا رسیدید، شما به این پروژه پیوسته‌اید. به یاد داشته باشید:

> **این پروژه با عشق و دقت ساخته شده. اسناد نقشه راه شما هستند. وقتی شک کردید، بپرسید.**

موفق باشید! 🚀

---

## 📌 پایان ONBOARDING_GUIDE

**نسخه:** v1.0 (2026-05-17)  
**زمان مطالعه:** ~۴-۶ ساعت  
**به‌روز در:** پایان هر فاز پروژه
