# ماژول ۰۵ — معماری پروژه

> بخشی از **Constitution v2.17 (Modular)** — [بازگشت به main](./main.md)
>
> **محتوا:** محیط + Stack + پوشه‌بندی + DB Schema + Backend API + Frontend + UI/UX + Security + کدنویسی + تست + Roadmap
> **منبع v2.11:** سند ۲ (محیط) + سند ۳ (Stack) + سند ۴ (پوشه‌بندی) + سند ۵ (DB) + سند ۶ (Backend API) + سند ۷ (Frontend) + سند ۸ (UI/UX) + سند ۹ (امنیت) + سند ۱۰ (کدنویسی) + سند ۱۱ (تست) + سند ۱۲ (Roadmap)
> **Created in commit:** `<git log -1 --format=%h پس از commit 6 پر شود>`

---

## ۵.۱ محیط توسعه

| مورد | مقدار |
|---|---|
| **سیستم‌عامل** | Windows 11 — 64-bit |
| **مسیر ریشه** | `D:\Projects\trading-system` |
| **مسیر Backend** | `D:\Projects\trading-system\backend` |
| **مسیر Frontend** | `D:\Projects\trading-system\frontend` |
| **مسیر Scripts** | `D:\Projects\trading-system\scripts` |
| **مسیر اسناد** | `D:\Projects\trading-system\docs` |

🔒 Claude باید در تمام کدها و اسکریپت‌ها این مسیرها را به‌عنوان مرجع ثابت در نظر بگیرد.

### ۵.۱.۱ Windows Terminal با ۴-tab

| Tab | نام | رنگ | نقش |
|---|---|---|---|
| ۱ | `1 backend` | 🟦 | uvicorn (Backend) — همیشه باز |
| ۲ | `2 scripts` | 🟩 | Python scripts + alembic + pip + git |
| ۳ | `3 frontend` | 🟧 | npm (فاز ۷+) |
| ۴ | `4 BACKUP` | 🟥 | git backup + sync (فاز ۱+ فعال) |

🔒 نام tab ها حرف به حرف باید مطابق بالا باشد (قانون #۱۷ + #۳۱).

### 5.1.2 Shell Configuration — اصلاحیه v2.12 ✅

🔒 **Default shell در پروژه = PowerShell + venv فعال**

#### تاریخچه تغییر (درس برای پروژه)

در v2.11 و پایین‌تر (سند ۱.۷)، متن گفته بود «Default profile در Windows Terminal باید Command Prompt باشد»، در حالی که در عمل در تمام پروژه از PowerShell به‌عنوان shell اصلی استفاده شده است. این تناقض (تناقض ۹ در Discovery چت ۱۱.۰.الف) در v2.12 رسماً رفع شد.

بخش ۱.۷.۱ قدیمی (CMD profiles) به‌عنوان رفرنس تاریخی نگه داشته می‌شود (طبق قانون #۲۴ No-Deletion).

#### تنظیمات واقعی پروژه

| مورد | مقدار |
|---|---|
| **Default shell** | **PowerShell** در Windows Terminal |
| **Prompt نمایشی** | `(venv) PS D:\Projects\trading-system>` |
| **venv activation** | `.\backend\venv\Scripts\Activate.ps1` |
| **تغییر drive** | `cd D:\` (PowerShell بدون `/d` کار می‌کند) |
| **alternative** | CMD هم کار می‌کند ولی برخی دستورات multi-line در CMD دشوارتر است (M84) |

نکته مهم: در PowerShell، دستورات چندخطی git commit با multiple `-m` تکراری کار می‌کند. در CMD باید در یک خط بودن رعایت شود (M84).

#### چرا PowerShell ترجیح‌شده؟

۱. پشتیبانی بهتر از multi-line commands و strings با escape
۲. توابع بیشتر (مثل `Get-ChildItem`, `Test-Path`, `Get-Content`)
۳. UTF-8 native (کمتر مشکل encoding cp1252 نسبت به CMD)
۴. سازگاری بهتر با git operations پیچیده

### ۵.۱.۳ نکات Cross-shell

- در ویندوز برای تغییر drive از C: به D:، حتماً از `cd /d` استفاده شود (در CMD)
- در PowerShell `cd D:\` بدون `/d` کار می‌کند
- paste چند خطی: ممکن است Warning دهد، روی `Paste anyway` کلیک کنید
- ASCII-only در `print()` اسکریپت‌های Windows (قانون #۴۶) برای اجتناب از cp1252 crash

---

## ۵.۲ Backend Stack — نسخه‌های قطعی

> منبع: سند ۲.۲ v2.11 + اصلاحیه v2.12 ccxt 4.3.0→4.3.98

| ابزار / کتابخانه | نسخه | یادداشت |
|---|---|---|
| **Python** | 3.11.2 | (پیش‌تر 3.11.9 ذکر شده، نسخه عملاً نصب‌شده 3.11.2) |
| **FastAPI** | 0.111.0 | |
| **Uvicorn** | 0.29.0 | |
| **python-multipart** | 0.0.9 | برای OAuth2PasswordRequestForm |
| **SQLAlchemy** | 2.0.30 (async) | |
| **aiosqlite** | 0.20.0 | |
| **Alembic** | 1.13.1 | |
| **Pydantic** | 2.7.1 | |
| **pydantic-settings** | 2.2.1 | |
| **python-jose[cryptography]** | 3.3.0 | |
| **bcrypt** | 4.1.3 | جایگزین passlib (تصمیم #۴۰) |
| **cryptography** | 42.0.7 | برای Fernet |
| **python-dotenv** | 1.0.1 | |
| **colorama** | 0.4.6 | رنگ‌های ANSI در Windows |
| **httpx** | 0.27.0 | تست API + ccxt internal |
| **pandas** | 2.2.2 | خواندن Excel |
| **openpyxl** | 3.1.2 | برای .xlsx |
| **ccxt** | **4.3.98** 🆕 v2.12 | (اصلاحیه از 4.3.0 — درس M68) |
| **websockets** | **12.0** 🆕 v2.12 | فاز ۱+ |
| **python-telegram-bot** | 21.x | فاز ۸ |

⚠️ **`passlib` حذف شد** در v2.5 (تصمیم #۴۰). در `app/core/security.py` مستقیم از `bcrypt` استفاده می‌شود.

⚠️ Python 3.12 یا بالاتر استفاده نشود — برخی کتابخانه‌های FastAPI ناسازگار.

---

## ۵.۳ Frontend Stack — نسخه‌های قطعی

| ابزار / کتابخانه | نسخه | یادداشت |
|---|---|---|
| **Node.js** | 22.x LTS | (Node 20 از April 2026 EOL) |
| **React** | 18 | |
| **Vite** | 8.0.13 | |
| **React Router** | 6.23.1 | |
| **Axios** | 1.7.2 | |
| **Zustand** | 4.5.2 | با middleware `persist` |
| **lightweight-charts** | 4.1.7 | API قدیمی `addCandlestickSeries` |
| **dayjs** | 1.11.11 | فاز ۱+ |
| **jalali-moment** | 3.3.11 | فاز ۱+ |

🔒 در `requirements.txt` و `package.json` دقیقاً همین نسخه‌ها قرار گیرند.

---

## ۵.۴ متغیرهای محیطی (.env)

| کلید | کاربرد |
|---|---|
| `APP_ENV` | development / production |
| `APP_NAME` | نام اپلیکیشن |
| `APP_VERSION` | نسخه فعلی |
| `API_HOST` / `API_PORT` | آدرس و پورت Backend |
| `SECRET_KEY` | کلید JWT (تصادفی، تولید خودکار در setup) |
| `JWT_ALGORITHM` | HS256 |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | 30 |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS` | 7 |
| `ENCRYPTION_KEY` | Fernet (44 کاراکتر) |
| `DB_PATH` | مسیر SQLite |
| `FRONTEND_URL` | برای CORS |
| `TIMEZONE` | UTC (DB) |
| `DISPLAY_TIMEZONE` | Asia/Tehran (UI) |
| `BINANCE_API_KEY` | رمزنگاری‌شده (فاز ۱+) |
| `BINANCE_SECRET_KEY` | رمزنگاری‌شده (فاز ۱+) |

🔒 `.env` در `.gitignore` باشد. API Keyها رمزنگاری‌شده ذخیره شوند.

⚠️ `SECRET_KEY` و `ENCRYPTION_KEY` در اولین setup تصادفی تولید می‌شوند. **اگر `.env` گم شود، API Keyهای رمزشده غیرقابل بازیابی هستند.** بک‌آپ امن از `.env` ضروری است.

---

## ۵.۵ Layered Architecture

| لایه | مسئولیت | الزام |
|---|---|---|
| **Presentation (api/)** | Request + Validation + Response | بدون Business Logic |
| **Application (services/)** | Business Logic + Transaction | بدون Query مستقیم DB |
| **Domain (domain/)** | Entity + VO + Domain Event | بدون وابستگی Infrastructure |
| **Infrastructure** | DB + Repository + Cache + External + DataSource | پیاده‌سازی interface‌های Domain |

---

## ۵.۶ ساختار پوشه‌بندی Backend

```
backend/
├── main.py                        ← نقطه ورود FastAPI
├── requirements.txt
├── trading.db                     ← تنها فایل دیتابیس
├── .env                           ← تنظیمات حساس (در .gitignore)
├── .env.example                   ← نمونه عمومی
├── venv/
├── logs/                          ← فایل‌های لاگ + rotation
└── app/
    ├── api/v1/routes/             ← auth, symbols, ohlcv, strategies, backtest,
    │                                portfolio, signals, alerts, settings, health
    ├── api/v1/websocket/          ← market.py, signals.py
    ├── core/                      ← config, logging, exceptions, response,
    │                                handlers, security, dependencies
    ├── domain/                    ← entities, value_objects, events, services
    ├── services/                  ← auth, market, strategy, backtest,
    │                                exchange, risk
    ├── repositories/              ← base, symbol, ohlcv, strategy,
    │                                trade, user, audit
    ├── models/                    ← SQLAlchemy Models
    ├── schemas/                   ← Pydantic Schemas
    └── infrastructure/
        ├── database/              ← engine, session, base
        ├── data_sources/          ← Excel reader, CCXT source (skeleton)
        ├── exchange/              ← فاز ۱+
        ├── cache/
        └── backup/

migrations/versions/
tests/unit/ + tests/integration/
```

---

## ۵.۷ ساختار پوشه‌بندی Frontend

```
frontend/src/
├── main.jsx                       ← BrowserRouter فقط اینجا
├── App.jsx                        ← Routes
├── pages/                         ← Login, Dashboard, Chart, Strategies,
│                                    Backtest, Portfolio, Settings
├── components/common/             ← Table, Modal, Toast, Skeleton,
│                                    Tooltip, ConfirmDialog
├── components/chart/              ← CandlestickChart, IndicatorPanel
├── services/                      ← api.js (Axios+JWT), websocket.js
├── stores/                        ← authStore, marketStore, strategyStore,
│                                    settingsStore, portfolioStore
├── hooks/
├── utils/                         ← dateUtils, numberUtils, chartUtils
└── constants/                     ← theme.js, routes.js
```

---

## ۵.۸ قراردادهای نامگذاری

### Python

| نوع | الگو | مثال |
|---|---|---|
| فایل | snake_case | `auth_service.py` |
| کلاس | PascalCase | `StrategyService` |
| تابع | snake_case | `get_ohlcv_data()` |
| ثابت | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Repository | PascalCase + Repository | `OhlcvRepository` |
| Schema | PascalCase + Request/Response | `StrategyCreateRequest` |

### React

| نوع | الگو | مثال |
|---|---|---|
| کامپوننت | PascalCase.jsx | `CandlestickChart.jsx` |
| utility | camelCase.js | `dateUtils.js` |
| Store | camelCase + Store | `marketStore` |
| Hook | use + PascalCase | `useWebSocket` |
| ثابت | UPPER_SNAKE_CASE | `DEFAULT_TIMEFRAME` |

### Database

| نوع | الگو | مثال |
|---|---|---|
| جدول | PascalCase | `OhlcvData` |
| ستون | snake_case | `symbol_id` |
| کلید خارجی | نام جدول + `_id` | `symbol_id` |
| Soft Delete | `is_deleted` | `is_deleted` |
| ایندکس | `idx_` + جدول + ستون | `idx_ohlcv_symbol_tf_ts` |

### API Endpoints

| قانون | مثال |
|---|---|
| پیشوند پایه | `/api/v1/` |
| منابع جمع کوچک | `/api/v1/symbols` |
| عملیات خاص — فعل | `/api/v1/backtest/run` |
| WebSocket | `/ws/market`, `/ws/signals`, `/ws/orders` |

🔒 Claude هرگز فایل یا پوشه‌ای خارج از این ساختار بدون توافق صریح نسازد.

---

## ۵.۹ DB Schema — ۱۲ جدول اصلی + AuditLog

### اصول کلی

| اصل | تصمیم |
|---|---|
| **نرمال‌سازی** | حداقل 3NF |
| **Soft Delete** | فیلد `is_deleted` در همه جداول اصلی |
| **زمان‌بندی** | `created_at` + `updated_at` در همه جداول |
| **کلید اصلی** | `INTEGER PRIMARY KEY AUTOINCREMENT` |
| **رمزنگاری** | API Key رمزنگاری‌شده با Fernet — هرگز Plain Text |
| **Migration** | Up Script + Down Script برای هر تغییر |
| **Timezone** | تمام datetime ها UTC در DB، تبدیل در UI |

⚠️ SQLite از `ALTER COLUMN` پشتیبانی نمی‌کند — در صورت نیاز جدول recreate شود.

### PRAGMA SQLite (در اتصال)

🆕 v2.1 — چهار PRAGMA در هر اتصال:
- `foreign_keys = ON` (FK enforcement)
- `journal_mode = WAL` (concurrency بهتر)
- `synchronous = NORMAL` (تعادل سرعت/امنیت)
- `cache_size = -64000` (64 MB cache)

### خلاصه ۱۳ جدول

| # | نام | شرح کوتاه | فیلدهای حیاتی |
|---|---|---|---|
| ۱ | **Users** | احراز هویت | id, username, password_hash, role, is_active, is_deleted |
| ۲ | **Sessions** | JWT refresh | id, user_id, token, ip_address, expires_at, is_revoked |
| ۳ | **Exchanges** | صرافی‌ها | id, name, ccxt_id, is_active, supports_futures |
| ۴ | **ExchangeAPIKeys** | کلیدهای رمزنگاری‌شده | id, user_id, exchange_id, api_key_encrypted, secret_key_encrypted, permissions |
| ۵ | **Symbols** | نمادها | id, exchange_id, symbol, base_asset, quote_asset, market_type |
| ۶ | **Watchlist** | لیست کاربر | id, user_id, symbol_id, sort_order |
| ۷ ⭐ | **OhlcvData** | کندل‌های قیمت | id, symbol_id, timeframe, timestamp, OHLCV, is_closed, row_index |
| ۸ | **Strategies** | استراتژی‌ها (با versioning) | id, user_id, name, parent_id (FK self), entry/exit/risk JSON, timeframes |
| ۹ | **Signals** | سیگنال‌ها | id, strategy_id, symbol_id, signal_type, strength, suggested_entry/tp/sl |
| ۱۰ | **Trades** | معاملات | id, user_id, strategy_id, signal_id, symbol_id, exchange_id, order_type, status, entry/exit/quantity/pnl |
| ۱۱ | **Portfolio** | پوزیشن‌های باز | user_id, exchange_id, asset, balance_total/free/locked |
| ۱۲ | **Alerts/RiskSettings/AppSettings** | تنظیمات | user_id + JSON fields |
| ۱۳ | **AuditLog** 🆕 v2.1 | لاگ امنیتی | user_id, action, resource_type, resource_id, ip_address, user_agent, details JSON, status |

### ایندکس‌های حیاتی

🔒 **idx_ohlcv_symbol_tf_ts** روی `(symbol_id, timeframe, timestamp)` — حیاتی برای performance
🗂 **idx_symbols_exchange_symbol** روی `(exchange_id, symbol)`
🗂 **idx_audit_user_created** روی `(user_id, created_at DESC)`
🗂 **idx_audit_action_created** روی `(action, created_at DESC)`

### Foreign Keys & Cascade

```
Users ──< Sessions
Users ──< ExchangeAPIKeys >── Exchanges
Users ──< Watchlist >── Symbols >── Exchanges
Symbols ──< OhlcvData
Users ──< Strategies ──< Signals >── Symbols
Users ──< Trades >── Symbols, Exchanges, Strategies, Signals
Users ──< Portfolio >── Exchanges
Users ──< Alerts >── Symbols
Users ── RiskSettings   |   Users ── AppSettings
Users ──< AuditLog   🆕 v2.1
```

🔒 `PRAGMA foreign_keys = ON` در اتصال دیتابیس فعال شود.

### وضعیت فعلی داده (پایان چت ۱۰)

- **Users:** ۱ کاربر (admin / bcrypt-hashed `1`)
- **Exchanges:** ۱ صرافی (Excel، ccxt_id=excel)
- **Symbols:** ۱ نماد (BTC/USDT روی Excel)
- **OhlcvData:** **۱۷۱۴ کندل** BTC/USDT روزانه (2017-08-17 → 2022-04-26)
- **Migration head:** `08348dca2b9a` (add_row_index_to_ohlcv)

---

## ۵.۱۰ Backend API Endpoints

### Auth Flow

| مرحله | عملیات |
|---|---|
| ۱ | `POST /api/v1/auth/login` — دریافت username/password |
| ۲ | bcrypt verify password_hash |
| ۳ | Access Token (JWT، ۳۰ دقیقه، شامل user_id+role) |
| ۴ | Refresh Token (JWT، ۷ روز، ذخیره در Sessions) |
| ۵ | Access در body — Refresh در HttpOnly Cookie (فاز ۵+) |
| ۶ | `POST /auth/refresh` با Refresh Token |
| ۷ | `POST /auth/logout` — ابطال Refresh در DB |

🔒 Secret Key از `.env` — هرگز Hardcode نشود.

### ساختار استاندارد Response

```json
{
  "success": true,
  "message": "پیام فارسی",
  "data": { },
  "errors": null
}
```

### کدهای HTTP

| کد | معنی |
|---|---|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request — Validation |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 🆕 | Business Logic Error |
| 429 🆕 | Rate Limit |
| 500 | Server Error |
| 502 🆕 | Bad Gateway (سرویس خارجی) |

### Middleware — ترتیب اجرا

🔒 `CORS ← Rate Limit ← Auth ← RBAC ← Input Sanitize ← Audit Log`

### RBAC Matrix

| عملیات | Admin | Trader |
|---|---|---|
| مشاهده داده بازار | ✅ | ✅ |
| مدیریت استراتژی | ✅ | ✅ (خودش) |
| اجرای بک‌تست | ✅ | ✅ |
| ثبت اردر واقعی | ✅ | ✅ (با تأیید) |
| مدیریت API Key | ✅ | ✅ (خودش) |
| تنظیمات سیستم | ✅ | ❌ |
| مدیریت کاربران | ✅ | ❌ |
| Audit Log | ✅ | ❌ |

### Endpoints کامل

#### Auth
- `POST /api/v1/auth/login` (OAuth2 form) ✅
- `POST /api/v1/auth/refresh` ✅
- `POST /api/v1/auth/logout` ✅
- `GET /api/v1/auth/me` ✅
- `PUT /api/v1/auth/change-password` (فاز بعد)

#### Symbols + Watchlist
- `GET /api/v1/symbols` (لیست با فیلتر/pagination)
- `GET /api/v1/symbols/{id}`
- `GET /api/v1/symbols/search`
- `GET /api/v1/watchlist`
- `POST /api/v1/watchlist`
- `DELETE /api/v1/watchlist/{symbol_id}`

#### OHLCV + Strategies
- `GET /api/v1/ohlcv/{symbol_id}` ✅
- `POST /api/v1/ohlcv/import`
- `GET /api/v1/strategies`
- `POST /api/v1/strategies`
- `PUT /api/v1/strategies/{id}` (نسخه جدید)
- `GET /api/v1/strategies/{id}/versions`
- `POST /api/v1/strategies/from-ai`

#### Backtest + Trades + Signals + Alerts
- `POST /api/v1/backtest/run`
- `GET /api/v1/backtest/results`
- `POST /api/v1/backtest/compare`
- `GET /api/v1/trades`
- `POST /api/v1/trades`
- `DELETE /api/v1/trades/{id}`
- `GET /api/v1/portfolio`
- `GET /api/v1/signals`
- `POST /api/v1/alerts`
- `GET /api/v1/health` ✅

#### WebSocket

| Endpoint | کاربرد | Auth |
|---|---|---|
| `WS /ws/market?symbol=...&tf=...` | Real-time کندل و قیمت | ✅ |
| `WS /ws/signals` | سیگنال‌های جدید | ✅ |
| `WS /ws/orders` | وضعیت اردرهای باز | ✅ |

### WebSocket Authentication ⭐

🆕 v2.1 — handshake JSON پس از اتصال (نه query string):

```json
{ "type": "auth", "token": "<JWT access token>" }
```

- token معتبر → `{"type": "auth", "status": "ok"}` + ادامه
- token نامعتبر یا timeout 5s → close با code 1008

**دلیل:** token در URL ثبت نمی‌شود (لاگ Nginx، تاریخچه مرورگر، Referer header).

🔒 Reconnection خودکار با Exponential Backoff در هر دو طرف.

---

## ۵.۱۱ Frontend Architecture

### Zustand Stores

| Store | فیلدهای اصلی |
|---|---|
| **authStore** | user, token, isAuthenticated, login(), logout() |
| **marketStore** | selectedSymbol, selectedTimeframe, candles, currentPrice, ws |
| **strategyStore** | strategies, activeStrategy, backtestResults |
| **settingsStore/preferencesStore** | theme, calendarType, gregorianFormat, fontSize, activeExchanges |
| **portfolioStore** | positions, openTrades, balance |

🔒 Store‌ها نباید مستقیم با API ارتباط داشته باشند — فقط از طریق `services/api.js`.

### React Router

| Route | Component | محافظت |
|---|---|---|
| `/login` | LoginPage | عمومی |
| `/` | DashboardPage / HomePage | Auth |
| `/chart/:symbol` | ChartPage | Auth |
| `/strategies` | StrategiesPage | Auth |
| `/backtest` | BacktestPage | Auth |
| `/portfolio` | PortfolioPage | Auth |
| `/settings` | SettingsPage | Auth — Admin |

🔒 `BrowserRouter` فقط در `main.jsx`.

### Axios Instance

در `services/api.js`:
- `baseURL` از `.env`
- Request interceptor: `Authorization: Bearer {token}` از authStore
- Response interceptor: 401 → `POST /auth/refresh` → retry
- اگر refresh ناموفق → logout + redirect `/login`

🔒 از `r.data` استفاده نشود (interceptor قبلاً unwrap کرده).

### WebSocket Manager

در `services/websocket.js`:
- Reconnection خودکار با Exponential Backoff
- پس از اتصال، اولین پیام JSON auth با token (سند ۶.۱۱)
- پس از Reconnect، subscribe مجدد به symbol‌های قبلی
- داده‌های دریافتی مستقیم به marketStore

---

## ۵.۱۲ UI/UX Standards

### اصول عمومی

🔒 RTL کامل — تمام متن‌ها، فرم‌ها، جداول، منوها `direction: rtl`

- تقویم: شمسی + میلادی — قابل تنظیم — **پیش‌فرض میلادی** — فرمت YYYY/MM/DD
- جداسازی سه‌رقمی Real-Time با کاما در تمام فیلدهای عددی
- اعشار قیمت با همان تعداد رقم API
- Compact Layout — استفاده حداکثری از فضا
- Tab Navigation با Tab/Shift+Tab
- دکمه بازگشت در هر صفحه
- Skeleton Screen (نه Spinner) در بارگذاری‌های API
- Tooltip روی تمام فیلدهای تکنیکال — فارسی

### فونت‌ها (v2.1 — رایگان)

| کاربرد | فونت |
|---|---|
| سرستون جداول | **Estedad-Bold** |
| داده‌های جدول | **IRANSans** |
| متن‌های عمومی UI | **Vazirmatn** |

منابع:
- Estedad: `github.com/aminabedi68/Estedad`
- IRANSans: `font.ir`
- Vazirmatn: `github.com/rastikerdar/vazirmatn`

### Theme Engine

تم پیش‌فرض: **binance-dark** (تصمیم #۴۹، v2.6 — رنگ‌های رسمی بایننس)

| متغیر CSS | مقدار |
|---|---|
| `--color-primary` | `#F0B90B` (طلایی بایننس) |
| `--color-bg` | `#181A20` |
| `--color-card` | `#1E2329` |
| `--color-success` | `#0ECB81` |
| `--color-danger` | `#F6465D` |
| `--color-link` | `#F0B90B` |

🔒 حداقل ۵ تم: بایننس، مینیمال سفید، تاریک مدرن، پاستلی، Sky Blue
🔒 Custom Color Picker + Font Size Adjuster + High-Contrast Mode

### Interactive States (سند ۸.۷.۱ v2.6)

🔒 هر تم باید **کامل** باشد و شامل:

| State | پیاده‌سازی |
|---|---|
| hover | `filter: brightness(1.12)` |
| active | `transform: translateY(1px)` |
| focus-visible | `outline: 2px solid var(--color-primary)` |
| disabled | `opacity: 0.5; cursor: not-allowed` |
| select hover | تغییر border-color |
| input focus | border طلایی |
| card-link hover | تغییر background |
| transition | smooth با `0.15s ease` |

### Variant Indicator Pattern (سند ۸.۸.۱ v2.6) ⭐

برای کامپوننت‌های دارای variant (success/error/warning/info):

🔒 **کانتینر از تم** — `background: var(--color-card)` + `border: 1px solid var(--color-border)`
🔒 **accent برای نوع** — فقط نوار باریک (3-4px) در سمت start (RTL = راست)
🔒 **icon رنگی** — آیکون با رنگ نوع
🔒 **متن از تم** — `color: var(--color-text)`
⛔ **ممنوع** — border کامل با رنگ نوع، background پررنگ با رنگ نوع

**مثال صحیح Toast:**
```jsx
<div style={{
  background: "var(--color-card)",
  border: "1px solid var(--color-border)",
  borderInlineStart: `3px solid ${cfg.color}`,
  color: "var(--color-text)",
}}>
  <span style={{ color: cfg.color }}>{icon}</span>
  <span>{message}</span>
</div>
```

### فرمت تاریخ میلادی (سند ۸.۸.۲ v2.7)

| ID | نمونه | locale |
|---|---|---|
| `iso` | `2024-01-15` | (custom) |
| `us-short` ⭐ | `01/15/2024` | en-US (پیش‌فرض، تصمیم #۵۰) |
| `eu-short` | `15/01/2024` | en-GB |
| `long` | `January 15, 2024` | en-US dateStyle:long |

ذخیره در `preferencesStore.gregorianFormat` (persist v2 با migration از v1).

### کامپوننت‌های مشترک

| کامپوننت | الزامات |
|---|---|
| Table | Zebra، Border، Sort، Filter، Sticky Header، Inline Edit، Skeleton |
| Modal | دکمه بازگشت، ConfirmDialog برای عملیات مهم |
| Toast | فارسی، غیرمزاحم، auto-dismiss، Variant Indicator Pattern |
| Skeleton | جایگزین Spinner |
| Tooltip | روی فیلدهای تکنیکال، فارسی |

---

## ۵.۱۳ Security

### Authentication

🔒 رمز عبور با bcrypt hash — هرگز Plain Text
🔒 Session Timeout: ۳۰ دقیقه — Access: ۳۰ دقیقه — Refresh: ۷ روز
🔒 JWT Secret از `.env`

پیاده‌سازی واقعی (v2.5):
- **bcrypt مستقیم** (نه passlib) — تصمیم #۴۰
- **Refresh Token در DB** (Sessions جدول) — logout صرفاً `is_revoked=True`
- **JWT در localStorage** فاز ۰ — مهاجرت به HttpOnly Cookie در فاز ۵+
- **OAuth2PasswordRequestForm** — `application/x-www-form-urlencoded` (نه JSON)

### رمزنگاری API Key صرافی

🔒 `cryptography.Fernet` (AES-128-CBC + HMAC-SHA256) — هرگز Plain Text

- کلید Fernet (۴۴ کاراکتر) از `ENCRYPTION_KEY` در `.env`
- تولید کلید: `cryptography.fernet.Fernet.generate_key()` در اولین setup
- **هشدار حیاتی:** اگر `.env` گم شود، API Keyهای رمزنگاری‌شده غیرقابل بازیابی هستند
- در Log هرگز API Key نمایش داده نشود (فیلتر خودکار `logging.py`)

### کنترل دسترسی (RBAC)

- نقش‌ها: Admin / Trader / Viewer / API User
- AuditLog در جدول `AuditLog` (سند ۵.۹) با `user_id, IP, user_agent, timestamp, details JSON`
- Row-Level Security: کاربر فقط داده‌های خودش را ببیند

### محافظت از حملات

| حمله | روش محافظت |
|---|---|
| SQL Injection | SQLAlchemy ORM — هرگز Query خام |
| XSS | Input Sanitization + CSP Header |
| CSRF | CSRF Token در فرم‌های مهم |
| Brute Force | Rate Limiting `/auth/login` (حداکثر ۵ تلاش) |
| Path Traversal | اعتبارسنجی مسیر فایل‌ها |
| WebSocket Token Leak | handshake JSON (نه query string) |

### Security Headers

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Strict-Transport-Security`
- `Content-Security-Policy`

### لاگ امنیتی

- فیلتر خودکار `logging.py` — `password|token|secret|api_key|authorization|bearer` → `***REDACTED***`
- ثبت IP تمام Loginها در AuditLog
- هشدار در صورت Login از IP جدید
- Log‌ها بدون اطلاعات حساس

---

## ۵.۱۴ Code Quality

### Clean Code

- نام‌گذاری واضح
- توابع کوتاه (۲۰-۳۰ خط، یک وظیفه)
- DRY (Don't Repeat Yourself)
- کامنت‌گذاری کامل

### SOLID

- **S** — Single Responsibility (هر کلاس/تابع یک وظیفه)
- **O** — Open/Closed (باز برای توسعه، بسته برای تغییر)
- **L** — Liskov Substitution
- **I** — Interface Segregation
- **D** — Dependency Inversion

### Logging

- سطوح: DEBUG / INFO / WARNING / ERROR / CRITICAL
- خروجی دوگانه: کنسول رنگی (colorama) + فایل rotation روزانه (۳۰ روز)
- دو فایل: `backend/logs/app.log` + `backend/logs/error.log`
- هر Log شامل: timestamp (UTC) + level + module + message + user_id
- فیلتر امنیتی خودکار (regex)
- AuditLog در DB

### Error Handling

- کلاس پایه `AppException` + ۱۳ زیرکلاس:
  - ValidationError, AuthenticationError, AuthorizationError
  - NotFoundError, ConflictError, BusinessLogicError
  - RateLimitError, DatabaseError, ExternalServiceError
  - ConfigurationError, EncryptionError, ExchangeError
- ۴ Exception Handler: AppException + RequestValidationError + StarletteHTTPException + Exception (catch-all)
- پیام به کاربر: فارسی، کوتاه، بدون جزئیات فنی
- جزئیات فنی فقط در Log
- هرگز stack trace به Frontend

### جلوگیری از N+1 Query

- eager loading: `selectinload`, `joinedload`
- هرگز Query در داخل loop
- بررسی Query‌های تولیدشده در dev

### Git Strategy

| شاخه | کاربرد |
|---|---|
| `main` | production-ready |
| `develop` | توسعه جاری |
| `feature/[نام]` | ویژگی جدید |
| `fix/[نام]` | رفع خطا |
| `hotfix/[نام]` | رفع فوری production |
| `infra/[نام]` 🆕 v2.12 | infrastructure overhaul (مثل governance-overhaul) |

### Commit Format

```
type(scope): description

types: feat | fix | refactor | docs | style | test | chore

مثال‌ها:
  feat(backtest): add walk-forward analysis support
  fix(logging): add colorama and UTF-8 support for Windows CMD
```

### Semantic Versioning

- `MAJOR.MINOR.PATCH`
- MAJOR: تغییر ناسازگار
- MINOR: قابلیت جدید سازگار
- PATCH: رفع خطا

### Change Log

- **Added**: قابلیت‌های جدید
- **Changed**: تغییرات در موجود
- **Fixed**: رفع خطاها
- **Removed**: حذف قابلیت‌ها
- **Decided** 🆕: تصمیمات معماری
- **Pending** 🆕: گام‌های معلق

---

## ۵.۱۵ Testing

### Unit Tests

- target: ≥۷۰٪ پوشش
- در فاز ۰ فقط critical (auth، encryption، repository-base)
- مستقل از DB (Mocking)
- برای هر Service و Repository فایل تست جدا

### Integration Tests

- sqlite `:memory:`
- تست تمام Endpoints با HTTP client

### Performance Testing

- زمان پاسخ API: <300ms برای ۹۵٪
- Load Test: ۱۰ کاربر همزمان
- Query بهینه OhlcvData با ۱M+ رکورد

### Security Testing

- SQL Injection
- XSS
- CSRF
- RBAC
- Encryption (encrypt/decrypt با کلید معتبر/نامعتبر)

### مستندسازی

- Swagger/OpenAPI خودکار از FastAPI در `/docs`
- ERD کامل DB
- Sequence Diagram برای Auth Flow + WebSocket

### CI/CD

- اجرای تست‌ها در هر Commit
- Backup خودکار قبل از Deployment
- Rollback خودکار در شکست تست‌ها

### Bug Tracking

- Severity: Critical / High / Medium / Low
- Priority: P0 / P1 / P2 / P3
- هر Bug با Deadline

---

## ۵.۱۶ Roadmap — ۱۵ فاز

| فاز | عنوان | اولویت | وضعیت فعلی |
|---|---|---|---|
| **۰** | زیرساخت | ⭐⭐⭐⭐⭐ | ✅ **۱۰۰٪** |
| **۱** | داده بازار (Excel در فاز ۰، صرافی در ۱) + نمودار شمعی | ⭐⭐⭐⭐⭐ | ⏳ **در حال — skeleton آماده** |
| ۲ | اندیکاتورها + الگوهای تکنیکال | ⭐⭐⭐⭐⭐ | ⏸ منتظر |
| ۳ | موتور شرط + استراتژی‌ساز | ⭐⭐⭐⭐⭐ | ⏸ |
| ۴ | بک‌تست + نمایش گرافیکی پیشرفته | ⭐⭐⭐⭐⭐ | ⏸ |
| ۵ | مدیریت ریسک | ⭐⭐⭐⭐ | ⏸ |
| ۶ | معاملات Live + پورتفولیو | ⭐⭐⭐⭐ | ⏸ |
| ۷ | هوش مصنوعی و ML | ⭐⭐⭐⭐ | ⏸ |
| ۸ | ربات تلگرام | ⭐⭐⭐⭐ | ⏸ |
| ۹ | گزارشات BI + داشبورد | ⭐⭐⭐ | ⏸ |
| ۱۰ | RBAC + امنیت پیشرفته | ⭐⭐⭐ | ⏸ |
| ۱۱ | بهینه‌سازی عملکرد | ⭐⭐⭐ | ⏸ |
| ۱۲ | اتصال صرافی‌های جدید + فارکس | ⭐⭐ | ⏸ |
| ۱۲.۵ | Trading Journal | ⭐⭐ | ⏸ |
| ۱۳ | تست و مستندسازی | ⭐⭐ | ⏸ |
| ۱۴ | نگهداری (مداوم) | ⭐ | ⏸ |

🔒 هیچ فازی بدون تکمیل فاز قبلی شروع نشود مگر با تأیید مستقیم.

### تفکیک فاز ۰ (تکمیل‌شده)

- ✅ معماری پایه (Layered + Repository + DDD + DI)
- ✅ UI/UX پایه (RTL + تقویم + اعداد + Tab Navigation)
- ✅ Theme Engine (۵+ تم + Variant Pattern + Interactive States)
- ✅ Data Source Layer (Excel در فاز ۰، CCXT skeleton در فاز ۱)
- ✅ Auth + JWT + RBAC
- ✅ Frontend pages (Login + Home + Chart + Settings)
- ✅ Governance ۱۲-سندی (PROJECT_GOVERNANCE + CLAUDE_CHECKLIST + CHAT_LOG + ...)

### تفکیک فاز ۱ (در حال — skeleton آماده)

- ✅ Dependencies: ccxt 4.3.98 + websockets 12.0
- ✅ Decisions #۶۱-۶۴ (Architecture Q&A)
- ✅ CCXTDataSource skeleton + ۵ تست AsyncMock pass
- ⏳ T3.03: `binance_client.py` (REST wrapper)
- ⏳ T3.04: `binance_ws.py` (WebSocket subscriber با asyncio.Queue)
- ⏳ T3.05: `exchange_repository.py`
- ⏳ T3.06: WebSocket endpoint برای frontend
- ⏳ T3.07: Integration test با Binance واقعی (نیاز VPN)
- ⏳ T3.08: Endpoint REST برای fetch OHLCV

### کتابخانه‌های فاز ۷ (آماده‌سازی معماری)

| کتابخانه | کاربرد |
|---|---|
| scikit-learn | مدل‌های ML پایه |
| pandas | پردازش داده سری زمانی |
| numpy | محاسبات عددی |
| ta-lib | اندیکاتورهای تکنیکال |

---

## 🚧 وضعیت این ماژول

✅ **Migration کامل از v2.11** — ۱۶ بخش از سند ۲-۱۲ ادغام شدند.

🔮 **افزوده‌های آینده در commit 8:**
- بخش ۵.۱.۲ Shell: تبدیل توجه v2.12 به اصلاحیه رسمی (CMD → PowerShell+venv)
- بخش ۵.۱۶ Roadmap: به‌روزرسانی وضعیت فاز ۱ پس از پیشرفت
- اضافه‌کردن BTC/USDT 1d state در بخش ۵.۹.۴ (در حال حاضر در «وضعیت فعلی داده» اشاره شده)

---

**📌 پایان 05_architecture.md (commit 6 — migration completed)**
