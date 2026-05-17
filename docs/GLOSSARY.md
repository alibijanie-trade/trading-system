# 📖 GLOSSARY — واژه‌نامه پروژه

> **هدف یک‌خطی:** تعریف یکپارچه اصطلاحات تخصصی، اختصارات، و مفاهیم کلیدی پروژه — برای جلوگیری از سوءتفاهم بین Claude و کاربر و برنامه‌نویس.

> **محل قرارگیری:** `docs/GLOSSARY.md`  
> **به‌روز توسط:** Claude به‌مرور (اگر اصطلاح جدید معرفی شد)  
> **نسخه:** v1.0 (2026-05-17)

---

## 📑 فهرست

- [راهنما](#راهنما)
- [الف — اصطلاحات معماری پروژه](#الف--اصطلاحات-معماری-پروژه)
- [ب — اصطلاحات Frontend](#ب--اصطلاحات-frontend)
- [ج — اصطلاحات Backend](#ج--اصطلاحات-backend)
- [د — اصطلاحات Trading & Domain](#د--اصطلاحات-trading--domain)
- [هـ — اصطلاحات Governance & فرایند](#هـ--اصطلاحات-governance--فرایند)
- [و — اختصارات](#و--اختصارات)
- [ز — Tab های ترمینال](#ز--tab-های-ترمینال)

---

## راهنما

هر تعریف شامل:
- **اصطلاح** (به فارسی یا انگلیسی)
- **معنی کوتاه**
- **مرجع** (سند یا فایل که آنجا تعریف شده)
- **مثال** (در صورت لزوم)

ترتیب الفبایی در هر بخش (فارسی به ترتیب الفبا، انگلیسی هم به ترتیب الفبا).

---

## الف — اصطلاحات معماری پروژه

### Anti-Pattern (الگوی ضدّ)
الگوی برنامه‌نویسی که اشتباه شناخته‌شده است و باید از آن پرهیز شود.  
**مرجع:** `PROJECT_GOVERNANCE.md` بخش ۱۱ (A1 تا A10)  
**مثال:** Hex Hardcoded (`color: "#F0B90B"` به جای `var(--color-primary)`)

### CSS Variables (متغیرهای CSS)
متغیرهایی که در `:root` تعریف می‌شوند و در تمام JSX/CSS با `var(--name)` استفاده می‌شوند. توسط `ThemeProvider` بر اساس تم فعال تنظیم می‌شوند.  
**مرجع:** سند جامع بخش ۸.۱، `frontend/src/components/common/ThemeProvider.jsx`  
**مثال:** `--color-primary`, `--color-card`, `--color-text-muted`

### DataSource Abstraction
لایه‌ای که منبع داده (Excel، API، Database) را پشت یک interface مشترک پنهان می‌کند.  
**مرجع:** `backend/app/infrastructure/data_sources/`  
**مثال:** `ExcelDataSource`, `CcxtDataSource` (فاز ۱)

### Idempotent Script (اسکریپت ذاتاً تکرارپذیر)
اسکریپتی که چندبار اجرای آن نتیجه یکسانی دارد و باعث خطا یا خرابی state نمی‌شود. در این پروژه: اگر فایل از قبل موجود است و محتوای یکسان دارد، اسکریپت skip می‌کند.  
**مرجع:** پترن `write_if_changed` در اسکریپت‌های ۲۷+  
**مثال:** اجرای `python scripts/29_skeleton_confirm.py` دو بار — بار دوم همه فایل‌ها `بدون تغییر` می‌شوند.

### Layered Architecture (معماری لایه‌ای)
معماری Backend که در آن request از routes → services → repositories → models می‌گذرد. هر لایه مسئولیت متفاوتی دارد و فقط با لایه بعدی صحبت می‌کند.  
**مرجع:** سند جامع بخش ۴

### Migration
تغییر schema دیتابیس به‌صورت version-controlled با Alembic.  
**مرجع:** `backend/alembic/versions/`

### Repository Pattern
هر query دیتابیس فقط در یک Repository class اجرا می‌شود — نه مستقیماً در routes یا services. هدف: testability + جلوگیری از تکرار.  
**مرجع:** `backend/app/repositories/`  
**مثال:** `UserRepository.get_by_username()` به جای `db.execute(select(User)...)`.

### Variant Indicator Pattern
الگویی برای کامپوننت‌های typed (Toast/Dialog/Alert): کانتینر همیشه از CSS variables تم (`--color-card`, `--color-border`)، و نوع (danger/warning/info) فقط با **یک accent باریک ۳-۴px** + icon رنگی نشان داده می‌شود. **ممنوع:** کادر کامل با رنگ نوع.  
**مرجع:** سند جامع بخش ۸.۸.۱  
**مثال:** Toast، ConfirmDialog

---

## ب — اصطلاحات Frontend

### ConfirmDialog
مودال سراسری برای تأیید عمل کاربر. Promise-based API:
```js
const ok = await askConfirm({ title, message, variant, confirmText, cancelText });
```
**مرجع:** `frontend/src/components/common/ConfirmDialog.jsx`

### Focus Trap
محصور کردن focus در یک ناحیه (مثلاً dialog) — وقتی dialog باز است، Tab فقط بین عناصر داخل آن می‌چرخد.  
**مرجع:** ConfirmDialog

### Persist (Zustand persist)
middleware که state store را در localStorage ذخیره می‌کند تا با refresh مرورگر از دست نرود.  
**مرجع:** `frontend/src/stores/themeStore.js`, `preferencesStore.js`

### SkeletonBlock
کامپوننت placeholder متحرک برای حالت loading. ۴ variant: rect، text، circle، line.  
**مرجع:** `frontend/src/components/common/SkeletonBlock.jsx`

### Shimmer Animation
انیمیشن نوار روشن که از یک طرف به طرف دیگر اسکلت حرکت می‌کند — حس "در حال بارگذاری" می‌دهد.  
**مرجع:** `frontend/src/index.css` (`@keyframes skeleton-shimmer`)

### Theme Engine
سیستم مدیریت تم با ۵ تم پیش‌فرض + امکان توسعه. هر تم یک object با CSS variables است.  
**مرجع:** سند جامع بخش ۸، `frontend/src/themes/themes.js`

### Toast
اعلان موقت در گوشه صفحه (۴ نوع: success/error/info/warning).  
**مرجع:** `frontend/src/components/common/Toast.jsx`

### Variant
نوع کامپوننت — معمولاً `danger`, `warning`, `info`, `success`.  
**مرجع:** Toast، ConfirmDialog

---

## ج — اصطلاحات Backend

### CORS (Cross-Origin Resource Sharing)
مکانیزم امنیتی browser. در پروژه: فقط `localhost:5173` (Vite) مجاز است.  
**مرجع:** `backend/app/main.py`

### Dependency Injection (در FastAPI)
سیستم تزریق وابستگی FastAPI با `Depends()`. مثلاً `current_user` در endpoint protected.  
**مرجع:** `backend/app/auth/dependencies.py`

### JWT (JSON Web Token)
Token رمزنگاری‌شده برای auth. در پروژه: expire ۷ روز، در `localStorage` کاربر.  
**مرجع:** `backend/app/auth/jwt.py`

### OAuth2 Password Flow
استاندارد دریافت token با username+password (در `/auth/login`).  
**مرجع:** `backend/app/api/v1/routes/auth.py`

### Pydantic Settings
کلاس برای خواندن config از `.env` با type validation.  
**مرجع:** `backend/app/config/settings.py`

### Seeding
پر کردن اولیه DB با داده‌های لازم (admin user، exchange Excel، …).  
**مرجع:** `scripts/` اسکریپت‌های ابتدای پروژه

---

## د — اصطلاحات Trading & Domain

### Candle (شمعی)
یک data point در نمودار شمعی شامل: timestamp, open, high, low, close, volume.  
**مرجع:** `backend/app/models/ohlcv_data.py`

### Exchange (صرافی)
محل تجارت ارز/سهم. در فاز ۰: فقط Excel به‌عنوان exchange. در فاز ۱: Binance، KuCoin، …

### Market (بازار)
نوع بازار: spot، futures، …  
در فاز ۰: فقط spot.

### OHLCV
Open, High, Low, Close, Volume — داده استاندارد شمعی.

### Symbol (نماد)
جفت‌ارز/سهم — مثل `BTC/USDT`, `ETH/USDT`.

### Timeframe
بازه زمانی هر شمعی: `1m`, `5m`, `15m`, `1h`, `4h`, `1d`, `1w`.

---

## هـ — اصطلاحات Governance & فرایند

### ADR (Architecture Decision Record)
سند تک‌صفحه‌ای که یک تصمیم معماری را با context و trade-offs ثبت می‌کند.  
**مرجع:** `docs/DECISIONS_LOG.md`

### CHAT_LOG
سند تاریخچه چت‌ها — هر چت یک بخش.  
**مرجع:** `docs/CHAT_LOG.md`، قانون #۲۳

### Constitution (قانون اساسی پروژه)
سند جامع v2.X — مرجع نهایی برای قوانین، معماری، تصمیمات.

### Governance
نظام اداره و کنترل پروژه — قوانین، protocol ها، چک‌لیست‌ها.  
**مرجع:** `docs/PROJECT_GOVERNANCE.md`

### Handoff
انتقال پروژه به برنامه‌نویس/Claude بعدی.  
**مرجع:** `docs/ONBOARDING_GUIDE.md`، `PROJECT_GOVERNANCE` بخش ۱۳

### Tier (سطح)
دسته‌بندی اولویت task ها: Tier 1 (بحرانی)، Tier 2 (مهم)، Tier 3 (موازی)، Tier 4 (آینده).  
**مرجع:** `docs/TASK_BACKLOG.md`

### Protocol شروع/پایان چت
دستورالعمل ۸ مرحله‌ای / ۱۲ مرحله‌ای برای ابتدا و انتهای هر چت.  
**مرجع:** `docs/CLAUDE_CHECKLIST.md`، `PROJECT_GOVERNANCE` بخش ۴ و ۵

---

## و — اختصارات

| اختصار | معنی کامل |
|---|---|
| ADR | Architecture Decision Record |
| API | Application Programming Interface |
| ARIA | Accessible Rich Internet Applications |
| CORS | Cross-Origin Resource Sharing |
| CSS | Cascading Style Sheets |
| DB | Database |
| DI | Dependency Injection |
| ESM | ECMAScript Modules |
| FAQ | Frequently Asked Questions |
| FE | Frontend |
| BE | Backend |
| HTTP | HyperText Transfer Protocol |
| ISO 8601 | استاندارد تاریخ بین‌المللی |
| JSX | JavaScript XML |
| JWT | JSON Web Token |
| LTS | Long-Term Support (Node.js) |
| OHLCV | Open-High-Low-Close-Volume |
| ORM | Object-Relational Mapping |
| PWA | Progressive Web App |
| RTL | Right-To-Left |
| SSO | Single Sign-On |
| TF | Timeframe |
| TS | TypeScript |
| UI | User Interface |
| UTC | Coordinated Universal Time |
| UX | User Experience |
| WS | WebSocket |

---

## ز — Tab های ترمینال

این پروژه از ۳ tab همزمان در ترمینال استفاده می‌کند:

### 🟦 tab «1 backend»
- محل: `cd backend && venv\Scripts\activate`
- دستور رایج: `uvicorn app.main:app --reload --port 8000`
- وضعیت: سرور backend در حال اجراست

### 🟩 tab «2 scripts»
- محل: `cd D:\Projects\trading-system`
- venv: `venv\Scripts\activate` (مشترک با backend)
- دستور رایج: `python scripts/N_xxx.py`
- وضعیت: برای اجرای اسکریپت‌های idempotent

### 🟧 tab «3 frontend»
- محل: `cd frontend`
- دستور رایج: `npm run dev`
- وضعیت: Vite dev server روی `localhost:5173`

> 💡 **چرا این تفکیک مهم است:** هر بار Claude می‌گوید "🟩 tab «2 scripts»"، شما دقیقاً می‌دانید کدام پنجره را باز کنید.

---

## 📌 پایان GLOSSARY

**نسخه:** v1.0 (2026-05-17)  
**اصطلاحات افزوده‌شده:** ~۷۰ مورد
