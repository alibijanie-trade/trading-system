# ماژول ۰۵ — معماری پروژه

> بخشی از **Constitution v2.12 (Modular)** — [بازگشت به main](./main.md)
>
> **محتوا:** Stack + DB Schema + Backend + Frontend + UI/UX + Security + Roadmap
> **منبع v2.11:** سند ۲ (محیط) + سند ۳ (Stack) + سند ۴ (پوشه‌بندی) + سند ۵ (DB) + سند ۶ (Backend API) + سند ۷ (Frontend) + سند ۸ (UI/UX) + سند ۹ (امنیت) + سند ۱۰ (کدنویسی) + سند ۱۱ (تست) + سند ۱۲ (Roadmap)
> **به‌روزرسانی v2.12:**
> - اصلاحیه ccxt 4.3.0 → 4.3.98 (از PENDING Z2.7)
> - افزودن websockets 12.0 (از فاز ۱)
> - افزودن BTC/USDT 1d data state (۱۷۱۴ کندل) + CCXTDataSource skeleton
> - به‌روزرسانی روی PowerShell+venv (تناقض ۹ — نسبت به Default profile سند ۱.۷)
> **Created in commit:** `<git log -1 --format=%h پس از commit 6 پر شود>`

---

## 📋 فهرست بخش‌ها (پس از migration)

> این فهرست در commit 6 (مرحله ۳ Migration) از منبع v2.11 پر می‌شود.

### بخش ۱ — محیط توسعه

- سیستم‌عامل: Windows 11 64-bit
- مسیرها: `D:\Projects\trading-system\` و subdirectoryها
- Shell: **PowerShell با venv فعال** (v2.12 update — قبلاً CMD گفته بود، در عمل PowerShell استفاده می‌شود)
- Windows Terminal با تب‌های رنگی: 🟦 backend، 🟩 scripts، 🟧 frontend، 🟥 BACKUP

### بخش ۲ — Backend Stack

- Python 3.11.2 + FastAPI 0.111 + Uvicorn 0.29
- SQLAlchemy 2.0 (async) + aiosqlite 0.20 + Alembic 1.13
- Pydantic 2.7 + pydantic-settings 2.2
- bcrypt 4.1.3 (مستقیم، نه passlib — تصمیم #40)
- cryptography 42 + Fernet
- pandas 2.2 + openpyxl 3.1
- **ccxt 4.3.98** (v2.12 update — تصحیح از 4.3.0)
- **websockets 12.0** (v2.12 — افزوده برای فاز ۱)

### بخش ۳ — Frontend Stack

- Node.js 22 LTS
- React 18 + Vite 8.0.13
- React Router 6.23 + axios 1.7 + Zustand 4.5
- lightweight-charts 4.1.7
- (آینده) dayjs 1.11 + jalali-moment 3.3

### بخش ۴ — Layered Architecture

- Presentation (api/) — Validation + Response
- Application (services/) — Business Logic
- Domain (domain/) — Entity + VO + Events
- Infrastructure (database/data_sources/exchange/cache/) — DB + DataSource + External

### بخش ۵ — DB Schema (۱۲ جدول اصلی + AuditLog)

1. Users — احراز هویت
2. Sessions — JWT refresh tokens
3. Exchanges — صرافی‌ها (Excel، Binance، …)
4. ExchangeAPIKeys — کلیدهای API رمزنگاری‌شده
5. Symbols — نمادها (BTC/USDT، …)
6. Watchlist — لیست تماشای کاربر
7. **OhlcvData** ⭐ — کندل‌های قیمت (۱۷۱۴ کندل BTC/USDT 1d موجود)
8. Strategies — استراتژی‌های ترید (با versioning)
9. Signals — سیگنال‌های تولیدشده
10. Trades — معاملات (paper + live)
11. Portfolio — پوزیشن‌های باز
12. Alerts — هشدارها + RiskSettings + AppSettings
13. AuditLog — لاگ امنیتی (افزوده v2.1)

### بخش ۶ — API Endpoints

- Auth: login/refresh/logout/me/change-password
- Symbols + Watchlist: CRUD
- OHLCV: get/import
- Strategies: CRUD + versions + from-ai
- Backtest: run/results/compare
- Trades + Portfolio + Signals + Alerts
- WebSocket: /ws/market، /ws/signals، /ws/orders (با handshake JSON auth)

### بخش ۷ — Frontend Architecture

- BrowserRouter فقط در `main.jsx`
- Axios instance + JWT interceptor در `services/api.js`
- Zustand stores: authStore، marketStore، strategyStore، settingsStore، portfolioStore
- WebSocket Manager در `services/websocket.js`

### بخش ۸ — UI/UX Standards

- RTL کامل
- Theme Engine با CSS variables (تم پیش‌فرض: binance-dark)
- Variant Indicator Pattern (accent + icon، نه border کامل)
- Interactive States (hover/focus/active/disabled) برای هر تم
- تقویم شمسی/میلادی toggle + ۴ فرمت میلادی (iso/us-short/eu-short/long)
- فونت‌های رایگان: Vazirmatn + Estedad + IRANSans
- Skeleton Screen (نه Spinner)
- Toast Notifications فارسی

### بخش ۹ — Security

- bcrypt مستقیم برای password hash
- JWT (HS256) — Access ۳۰ دقیقه + Refresh ۷ روز
- Fernet برای API keys صرافی (`ENCRYPTION_KEY` در `.env`)
- RBAC: Admin / Trader / Viewer
- WebSocket handshake JSON auth (نه query string)
- AuditLog در DB + filter امنیتی در logging
- Headers: X-Content-Type-Options، X-Frame-Options، CSP

### بخش ۱۰ — کدنویسی و کیفیت

- Clean Code + SOLID
- Logging: colorama + file rotation ۳۰ روزه
- Exception handling: AppException + ۱۳ زیرکلاس + ۴ handler
- N+1 prevention با eager loading
- Git Strategy: main/develop/feature/fix/hotfix
- Commit format: `type(scope): description`
- SemVer + Change Log

### بخش ۱۱ — تست

- Unit Tests: ≥۷۰٪ پوشش (target)
- Integration Tests با sqlite :memory:
- Performance: <۳۰۰ms برای ۹۵٪ requests
- Security Tests: SQL Injection، XSS، CSRF، RBAC، Encryption

### بخش ۱۲ — Roadmap (۱۵ فاز)

- فاز ۰: زیرساخت ✅ ۱۰۰٪
- **فاز ۱: داده بازار** ⏳ (skeleton آماده، در حال پیشرفت)
- فاز ۲: اندیکاتورها + الگوها
- فاز ۳: موتور شرط + استراتژی‌ساز
- فاز ۴: بک‌تست
- فاز ۵: ریسک
- فاز ۶: معاملات Live
- فاز ۷: AI/ML
- فاز ۸: تلگرام
- فاز ۹: گزارشات BI
- فاز ۱۰: RBAC پیشرفته
- فاز ۱۱: بهینه‌سازی
- فاز ۱۲: صرافی‌های جدید + فارکس
- فاز ۱۲.۵: Trading Journal
- فاز ۱۳: تست و مستندسازی
- فاز ۱۴: نگهداری

---

## 🚧 وضعیت این ماژول

⚠️ **این فایل فعلاً skeleton است.** محتوای کامل معماری در **commit 6** از منابع v2.11 (سند ۲-۸، ۱۲) migrate می‌شود.

⚠️ **نگرانی اندازه:** اگر این ماژول در migration بیش از ~۵۰KB شد، طبق نکته A کاربر در دستور شروع چت ۱۱.۰.الف، می‌توان به دو فایل split کرد:
- `05a_backend_db.md` (Stack + DB + Backend API)
- `05b_frontend_ui.md` (Frontend + UI/UX + Theme)

این تصمیم در حین commit 6 (نه الان) گرفته می‌شود.

---

**📌 پایان skeleton 05_architecture.md — منتظر محتوای migration در commit 6**
