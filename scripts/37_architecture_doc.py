# -*- coding: utf-8 -*-
"""
اسکریپت ۳۷ — ARCHITECTURE.md با دیاگرام‌های Mermaid (T2.04)
================================================================
Task: T2.04 (Tier 2 — Quality Hardening)

این اسکریپت idempotent است — قابل اجرا چندبار بدون شکست.

محتوای کار:
  ساخت docs/ARCHITECTURE.md با ۶ دیاگرام Mermaid:
    ۱) System overview (flowchart)
    ۲) Backend layers (flowchart)
    ۳) Frontend hierarchy (flowchart)
    ۴) Theme system flow (sequenceDiagram)
    ۵) DataSource abstraction (classDiagram)
    ۶) Auth flow (sequenceDiagram)
  + جدول stores
  + درخت فایل‌ها

این سند مرجع سریع high-level است؛ جزئیات کامل در «سند جامع v2.7».

نحوه اجرا (tab «2 scripts»):
    python scripts\\37_architecture_doc.py

سپس برای تست:
    python scripts\\37b_test_architecture_doc.py
================================================================
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
ARCHITECTURE_MD = PROJECT_ROOT / "docs" / "ARCHITECTURE.md"


# ────────────────────────────────────────────────────────────────
# محتوای ARCHITECTURE.md
# ────────────────────────────────────────────────────────────────
ARCHITECTURE_CONTENT = """\
# 🏛️ ARCHITECTURE — معماری سامانه

> **هدف یک‌خطی:** نمای فنی high-level از معماری backend + frontend با دیاگرام‌های Mermaid برای کمک به onboarding و طراحی فازهای بعدی.

> **محل قرارگیری:** `docs/ARCHITECTURE.md`
> **نسخه پروژه در زمان نگارش:** v0.4.0
> **آخرین به‌روزرسانی:** 2026-05-17
> **منبع رسمی:** این فایل تصویر معماری را خلاصه می‌کند؛ برای جزئیات کامل (API specs، DB schemas، business rules) به «سند جامع v2.7» مراجعه کنید.

---

## ۱. نمای کلی سیستم

این پروژه یک اپلیکیشن single-page (SPA) با backend جداگانه است:

```mermaid
flowchart LR
  User([👤 کاربر]) -->|HTTPS| FE[Frontend<br/>React 19 + Vite 8]
  FE -->|REST + JWT| BE[Backend<br/>FastAPI + uvicorn]
  BE -->|SQLAlchemy async| DB[(SQLite<br/>trading.db)]
  BE -.->|آینده فاز ۱+| Exchange[(Binance<br/>صرافی)]

  classDef future stroke-dasharray: 5 5
  class Exchange future
```

**جریان داده در فاز ۰:**
- کاربر از طریق مرورگر با Frontend (`http://localhost:5173`) ارتباط دارد.
- Frontend با Backend (`http://localhost:8000/api/v1`) از طریق REST (با JWT برای auth) ارتباط دارد.
- داده‌های OHLCV فعلاً از فایل‌های Excel نمونه (`infrastructure/data_sources/excel_source.py`) خوانده می‌شوند.
- در فاز ۱، DataSource به ccxt + Binance WebSocket متصل می‌شود — **بدون تغییر در API frontend** (abstraction در backend).

---

## ۲. معماری Backend — لایه‌ای

ساختار 5-لایه طبق سند ۵.۲ سند جامع. اصل: هر لایه فقط با لایه‌ی **مستقیماً زیر خود** ارتباط دارد.

```mermaid
flowchart TB
  subgraph API["🌐 API Layer · app/api/v1/routes/"]
    Auth["auth.py"]
    Health["health.py"]
    OHLCV["ohlcv.py"]
  end

  subgraph Service["⚙️ Service Layer · app/services/"]
    AuthSvc["auth_service.py"]
    OtherSvc["(آینده: ohlcv_service, alert_service ...)"]
  end

  subgraph Repo["🗄️ Repository Layer · app/repositories/"]
    Base["base.py (BaseRepository generic)"]
    UserRepo["user_repository.py"]
    OHLCVRepo["ohlcv_repository.py"]
    SymbolRepo["symbol_repository.py"]
    SessionRepo["user_session_repository.py"]
  end

  subgraph Models["📦 Model Layer · app/models/ — 16 model"]
    M1["User, UserSession"]
    M2["Symbol, Exchange, ExchangeApiKey"]
    M3["OHLCVData, Alert, Signal"]
    M4["Portfolio, Trade, Strategy"]
    M5["Watchlist, RiskSettings, AppSettings"]
    M6["AuditLog"]
  end

  subgraph Infra["🏗️ Infrastructure Layer"]
    DS["data_sources/ (Base + Excel)"]
    DBSess["database/session.py"]
    Cache["cache/"]
    Backup["backup/"]
  end

  DBFile[("💾 SQLite<br/>trading.db")]

  API --> Service
  Service --> Repo
  Repo --> Models
  Models --> DBSess
  Service -.->|DataSource| Infra
  DBSess --> DBFile
  Infra --> DBFile
```

**نکات مهم:**
- `app/core/` (پایه‌ای): `config.py`, `security.py`, `exceptions.py`, `handlers.py`, `logging.py`, `response.py` — توسط همه‌ی لایه‌ها قابل استفاده.
- `app/api/v1/dependencies.py` — DI factory functions (`get_db`, `get_current_user`) که توسط FastAPI تزریق می‌شوند.
- `app/schemas/` — Pydantic DTOs برای request/response (نه entity).

---

## ۳. معماری Frontend — سلسله‌مراتب کامپوننت

```mermaid
flowchart TB
  Main["main.jsx<br/>ReactDOM.createRoot"]
  Strict["React.StrictMode"]
  TP["ThemeProvider<br/>تزریق CSS vars به :root"]
  Router["BrowserRouter"]
  App["App.jsx"]
  EBRoot["ErrorBoundary label='root'"]
  Toast["ToastContainer"]
  Confirm["ConfirmDialog"]
  Routes["Routes"]
  EBLogin["ErrorBoundary route:login"]
  EBHome["ErrorBoundary route:home"]
  EBChart["ErrorBoundary route:chart"]
  EBSet["ErrorBoundary route:settings"]
  Login["LoginPage"]
  Home["HomePage"]
  Chart["ChartPage"]
  Settings["SettingsPage"]

  Main --> Strict --> TP --> Router --> App
  App --> EBRoot
  App --> Toast
  App --> Confirm
  EBRoot --> Routes
  Routes --> EBLogin --> Login
  Routes --> EBHome --> Home
  Routes --> EBChart --> Chart
  Routes --> EBSet --> Settings
```

**استراتژی defense-in-depth برای ErrorBoundary:**
- مرز **سراسری** (`label='root'`) — کل Routes را در بر می‌گیرد. آخرین خط دفاع.
- مرز **per-route** — هر صفحه‌ی خود را protect می‌کند؛ کاربر می‌تواند با navigate به مسیر دیگر از خطا فرار کند.

---

## ۴. جریان تم (Theme System)

تم‌ها در `frontend/src/themes/themes.js` تعریف شده‌اند (۵ تم). هر تم یک object از CSS variables است:

```mermaid
sequenceDiagram
  actor U as کاربر
  participant SP as SettingsPage
  participant TS as themeStore<br/>(Zustand + localStorage)
  participant TP as ThemeProvider
  participant DOM as document.documentElement<br/>(:root)

  U->>SP: کلیک روی ThemeCard
  SP->>TS: setTheme('dark-modern')
  TS->>TS: persist در localStorage
  TS-->>TP: notify (Zustand subscription)
  TP->>TP: useEffect: read THEMES[id].vars
  TP->>DOM: setProperty(--color-primary, ...)
  TP->>DOM: setAttribute(dir, 'rtl')
  DOM-->>U: re-render با رنگ‌های جدید (بدون reload)
```

**قوانین قفل‌شده مرتبط:**
- قانون #۳: هیچ hex hardcoded در کد — همه از `var(--color-*)`.
- قانون #۲۰: همه فایل‌های `.jsx` که styling دارند باید از CSS variables استفاده کنند.

---

## ۵. انتزاع DataSource

طبق سند ۸.۴، backend نباید مستقیماً به Binance یا فایل Excel وابسته باشد. به‌جای آن:

```mermaid
classDiagram
  class BaseDataSource {
    <<abstract>>
    +fetch_ohlcv(symbol, interval, since, limit) AsyncGenerator
    +get_available_symbols() list
    +is_alive() bool
  }

  class ExcelDataSource {
    -file_path: Path
    -binance_mappings: dict
    +fetch_ohlcv(...) AsyncGenerator
    +get_available_symbols() list
    +is_alive() bool
  }

  class CCXTDataSource {
    -exchange: str
    -api_key_encrypted: str
    +fetch_ohlcv(...) AsyncGenerator
    +get_available_symbols() list
    +subscribe_ws(symbol) AsyncGenerator
    +is_alive() bool
  }

  BaseDataSource <|-- ExcelDataSource : "فاز ۰ (فعلی)"
  BaseDataSource <|-- CCXTDataSource : "فاز ۱+ (آینده)"
```

**فایده:** برای تست/development می‌توان از Excel استفاده کرد؛ در production به Binance switch می‌شود — بدون تغییر در service layer. هیچ کد بالاتری (Service یا API) نام کلاس concrete را نمی‌داند؛ فقط `BaseDataSource` را می‌بیند.

---

## ۶. جریان Authentication

```mermaid
sequenceDiagram
  actor U as کاربر
  participant LP as LoginPage
  participant API as POST /auth/login
  participant Svc as AuthService
  participant Repo as UserRepository
  participant DB as SQLite

  U->>LP: username + password
  LP->>API: POST x-www-form-urlencoded
  API->>Svc: authenticate(username, password)
  Svc->>Repo: get_by_username(username)
  Repo->>DB: SELECT * FROM User WHERE username=?
  DB-->>Repo: User row
  Repo-->>Svc: User entity
  Svc->>Svc: bcrypt.verify(password, hash)
  Svc->>Svc: encode JWT (HS256, SECRET_KEY)
  Svc-->>API: {access_token, refresh_token}
  API-->>LP: 200 OK + tokens
  LP->>LP: authStore.setTokens(...)
  LP->>API: GET /auth/me (Authorization: Bearer)
  API-->>LP: user info
  LP->>U: navigate to /
```

**نکات امنیتی:**
- JWT در فاز ۰ در `localStorage` ذخیره می‌شود (سند ۶.۴ — قابل قبول برای dev/فاز ۰).
- در فاز ۸+ به httpOnly cookie منتقل خواهد شد (XSS mitigation).
- پسوردها با bcrypt (cost=12) hash می‌شوند — قانون #۶.

---

## ۷. مدیریت State (Zustand)

پنج store در `frontend/src/stores/`:

| Store | فایل | مسئولیت | Persist؟ |
|---|---|---|---|
| `authStore` | `authStore.js` | JWT tokens + user info | ❌ (هر بار login) |
| `themeStore` | `themeStore.js` | id تم فعال | ✅ localStorage |
| `preferencesStore` | `preferencesStore.js` | calendar/language/fontSize/gregorianFormat | ✅ localStorage |
| `toastStore` | `toastStore.js` | لیست toastهای فعال + success/error/warning/info | ❌ |
| `confirmStore` | `confirmStore.js` | dialog سراسری تأیید با Promise resolver | ❌ |

**انتخاب Zustand به‌جای Redux:**
- API ساده‌تر — بدون reducer/action/dispatch boilerplate.
- Bundle size کوچک‌تر (~1KB در مقابل ~10KB).
- `persist` middleware برای localStorage built-in.

---

## ۸. ساختار فایل‌ها

```
trading-system/
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── routes/        # auth.py · health.py · ohlcv.py
│   │   │   ├── websocket/
│   │   │   └── dependencies.py
│   │   ├── core/              # config · security · exceptions · handlers · logging · response
│   │   ├── domain/            # entities/ · events/ · services/ · value_objects/
│   │   ├── infrastructure/    # backup/ · cache/ · data_sources/ · database/ · exchange/
│   │   ├── models/            # ۱۶ SQLAlchemy model
│   │   ├── repositories/      # ۵ repository (base + ۴ entity)
│   │   ├── schemas/           # Pydantic DTOs
│   │   └── services/          # auth_service.py (+ آینده‌ها)
│   ├── main.py
│   ├── .env / .env.example
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/        # Toast · ConfirmDialog · ErrorBoundary · ProtectedRoute · ThemeProvider · SkeletonBlock
│   │   │   ├── chart/
│   │   │   └── settings/
│   │   ├── pages/             # LoginPage · HomePage · ChartPage · SettingsPage
│   │   ├── stores/            # ۵ Zustand store
│   │   ├── services/api.js    # axios instance با JWT interceptor
│   │   ├── themes/themes.js   # ۵ تم
│   │   ├── utils/             # numberFormat · dateFormat
│   │   ├── hooks/
│   │   ├── constants/
│   │   ├── test/setup.js      # vitest setup
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── docs/                       # ۱۲+ سند governance
│   ├── سند_جامع_v2_7.md       # قانون اساسی پروژه
│   ├── PROJECT_CONTEXT.md     # context سریع برای Claude
│   ├── ARCHITECTURE.md        # این فایل
│   ├── TASK_BACKLOG.md
│   ├── SESSION_STATUS.md
│   ├── CHAT_LOG.md
│   ├── DECISIONS_LOG.md
│   ├── TROUBLESHOOTING.md
│   ├── GLOSSARY.md
│   ├── STYLE_GUIDE.md
│   ├── ONBOARDING_GUIDE.md
│   ├── REUSABLE_SKELETON.md
│   ├── PROJECT_GOVERNANCE.md
│   └── CLAUDE_CHECKLIST.md
│
├── scripts/                    # ۳۷+ Python script (idempotent + paired test)
├── CHANGELOG.md
└── README.md
```

---

## ۹. مرجع‌های بیشتر

| مرجع | کاربرد |
|---|---|
| **سند جامع v2.7** (`docs/سند_جامع_v2_7.md`) | منبع اصلی — همه‌ی API specs، DB schemas، قوانین قفل‌شده، business rules |
| **PROJECT_CONTEXT.md** | context سریع برای شروع چت‌های جدید Claude |
| **TASK_BACKLOG.md** | کارهای آینده گروه‌بندی شده per phase + tier |
| **DECISIONS_LOG.md** | توجیه فنی تصمیمات معماری (۵۴+ تصمیم) |
| **TROUBLESHOOTING.md** | باگ‌های شناسایی‌شده + راه‌حل (۴۹+ مورد) |
| **ONBOARDING_GUIDE.md** | راهنمای راه‌اندازی development env از صفر |
| **STYLE_GUIDE.md** | قوانین کدنویسی + naming + i18n |
| **CLAUDE_CHECKLIST.md** | پروتکل ۸-گام شروع چت + ۱۲-گام پایان |

---

## 🔄 تاریخچه

- **2026-05-17** — نسخه اولیه (T2.04). ۶ دیاگرام Mermaid + جدول stores + درخت فایل‌ها.

---

*این سند با اسکریپت `scripts/37_architecture_doc.py` تولید شده است (idempotent — قابل regenerate در هر تغییر معماری).*
"""


# ────────────────────────────────────────────────────────────────
# write_if_changed
# ────────────────────────────────────────────────────────────────
def write_if_changed(path: Path, content: str) -> str:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        return "created"
    try:
        current = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        current = path.read_text(encoding="cp1252")
    if current == content:
        return "unchanged"
    path.write_text(content, encoding="utf-8", newline="\n")
    return "updated"


def main() -> int:
    print("=" * 64)
    print("اسکریپت ۳۷ — ARCHITECTURE.md (T2.04)")
    print("=" * 64)
    print()

    print("📝 docs/ARCHITECTURE.md")
    status = write_if_changed(ARCHITECTURE_MD, ARCHITECTURE_CONTENT)
    icon = {"created": "🆕", "updated": "✏️", "unchanged": "✓"}[status]
    print(f"   {icon} {status}  → docs/ARCHITECTURE.md")
    print()

    print("-" * 64)
    print("✅ پایان. حالا برای تست اجرا کنید:")
    print("   python scripts/37b_test_architecture_doc.py")
    print()
    print("📌 نکته رندر:")
    print("   - GitHub/GitLab به‌صورت native دیاگرام Mermaid را رندر می‌کنند.")
    print("   - در VS Code، پلاگین 'Markdown Preview Mermaid Support' را نصب کنید.")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
