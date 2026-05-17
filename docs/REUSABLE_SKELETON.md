# 🧬 REUSABLE_SKELETON — راهنمای استفاده مجدد از اسکلت پروژه

> **هدف یک‌خطی:** نشان می‌دهد کدام بخش‌های این پروژه به‌صورت reusable برای پروژه‌های آینده طراحی شده‌اند و چگونه یک پروژه جدید را با این اسکلت شروع کنیم.

> **محل قرارگیری:** `docs/REUSABLE_SKELETON.md`  
> **به‌روز توسط:** Claude به‌مرور (هرگاه بخشی به template اضافه/حذف شد)  
> **نسخه:** v1.0 (2026-05-17)

---

## 📑 فهرست

- [فلسفه](#فلسفه)
- [نقشه Reusability (چه چیزی reusable است)](#نقشه-reusability-چه-چیزی-reusable-است)
- [Quick Start — راه‌اندازی پروژه جدید](#quick-start--راهاندازی-پروژه-جدید)
- [راهنمای adaptation برای هر بخش](#راهنمای-adaptation-برای-هر-بخش)
- [Checklist استخراج Template](#checklist-استخراج-template)
- [الگوهای رایج پروژه‌ها و adaptation آن‌ها](#الگوهای-رایج-پروژهها-و-adaptation-آنها)
- [Anti-Patterns در استفاده مجدد](#anti-patterns-در-استفاده-مجدد)

---

## فلسفه

این پروژه از **روز اول** طوری طراحی شد که اسکلت آن **قابل استفاده مجدد** برای پروژه‌های آینده باشد. هدف:

> **در پروژه بعدی، فاز ۰ (همان زیرساختی که اینجا چند هفته طول کشید) باید در چند ساعت تکمیل شود.**

### اصل ۱ — جدایی Domain از Infrastructure

| دسته | Reusable | Domain-Specific |
|---|---|---|
| FastAPI scaffolding | ✅ | ❌ |
| Auth (JWT + bcrypt + OAuth2) | ✅ | ❌ |
| Theme Engine | ✅ | ❌ |
| Toast/Dialog/Skeleton | ✅ | ❌ |
| Settings Page | ✅ | ❌ |
| Number/Date Formatting | ✅ | ❌ |
| OhlcvData model | ❌ | ✅ (trading) |
| ChartPage logic | ❌ | ✅ (trading) |
| Excel DataSource | ⚠️ | تا حدی (data source pattern reusable است) |

### اصل ۲ — Naming Generic

اسامی نباید به trading اشاره کنند مگر اینکه واقعاً مخصوص trading باشند:
- ✅ `useThemeStore` (generic)
- ✅ `useAuthStore` (generic)
- ✅ `formatNumber` (generic)
- ❌ `tradingAuthStore` (اشتباه — ربطی به trading ندارد)
- ✅ `OhlcvData` (domain — OK چون واقعاً مفهوم ترید است)

### اصل ۳ — Config در `.env`

همه چیز قابل تغییر بین پروژه‌ها در `.env` باشد:
- `APP_NAME=Trading System` → در پروژه جدید: `APP_NAME=Inventory Manager`
- `DATABASE_URL`, `JWT_SECRET`, `CORS_ORIGINS`

---

## نقشه Reusability (چه چیزی reusable است)

### 🟢 100% Reusable (بدون تغییر)

#### Backend
```
backend/app/core/
├── logger.py           ✅ Loguru setup
├── exceptions.py       ✅ Exception hierarchy
├── handlers.py         ✅ Exception handlers
└── response.py         ✅ Standard response model

backend/app/config/
└── settings.py         ✅ Pydantic Settings template

backend/app/auth/
├── jwt.py              ✅ JWT utilities
├── password.py         ✅ bcrypt utilities
├── dependencies.py     ✅ current_user, current_admin
└── schemas.py          ✅ TokenResponse, LoginRequest

backend/app/database/
├── connection.py       ✅ Async SQLAlchemy setup
└── base.py             ✅ Base declarative

backend/app/repositories/
└── base.py             ✅ BaseRepository (generic CRUD)
```

#### Frontend
```
frontend/src/components/common/
├── ProtectedRoute.jsx  ✅ Route guard
├── ThemeProvider.jsx   ✅ Theme injection
├── Toast.jsx           ✅ Toast component
├── ToastContainer.jsx  ✅ Toast list
├── ConfirmDialog.jsx   ✅ Dialog modal
└── SkeletonBlock.jsx   ✅ Loading placeholder

frontend/src/components/settings/
├── ThemeCard.jsx       ✅ Theme preview card
├── FontSizeControl.jsx ✅ Font size selector
└── CalendarToggle.jsx  ✅ Calendar selector

frontend/src/stores/
├── authStore.js        ✅ JWT + user state
├── themeStore.js       ✅ Theme + fontSize
├── toastStore.js       ✅ Toast queue
├── confirmStore.js     ✅ Confirm dialog state
└── preferencesStore.js ✅ Calendar + format

frontend/src/utils/
├── numberFormat.js     ✅ formatNumber + parseFormattedNumber
└── dateFormat.js       ✅ formatDate + CALENDARS

frontend/src/themes/
└── themes.js           ✅ ۵ تم پیش‌فرض

frontend/src/services/
└── api.js              ✅ axios setup با interceptors

frontend/src/pages/
├── LoginPage.jsx       ✅ Login form template
└── SettingsPage.jsx    ✅ Settings page template
```

#### Scripts & Docs
```
scripts/
└── 00b_post_unzip_setup.py  ✅ راه‌اندازی خودکار

docs/
├── PROJECT_GOVERNANCE.md    ✅ Governance template
├── CLAUDE_CHECKLIST.md      ✅ Checklist template
├── REUSABLE_SKELETON.md     ✅ این سند
├── GLOSSARY.md              ⚠️ ساختار reusable، محتوا adapt شود
├── STYLE_GUIDE.md           ✅ کاملاً reusable
├── ONBOARDING_GUIDE.md      ⚠️ ساختار reusable
└── TROUBLESHOOTING.md       ⚠️ ساختار reusable
```

### 🟡 80% Reusable (با adapt محدود)

```
backend/app/api/v1/routes/
├── auth.py             ⚠️ login/register/me — 95% reusable
└── (سایر routes)        ⚠️ ساختار، نه محتوا

frontend/src/index.css   ⚠️ keyframes + interactive states reusable، رنگ‌ها از theme

scripts/
├── 27_theme_engine.py  ⚠️ ساختار، تم‌ها adapt شوند
├── 29_skeleton_confirm.py ⚠️ کاملاً reusable
└── ...
```

### 🔴 0% Reusable (Domain-Specific)

```
backend/app/models/ohlcv_data.py, symbol.py, exchange.py, timeframe.py
backend/app/repositories/ohlcv_repository.py
backend/app/api/v1/routes/ohlcv.py
backend/app/infrastructure/data_sources/excel_data_source.py
frontend/src/pages/ChartPage.jsx
frontend/src/pages/HomePage.jsx (دامنه — لینک نمودار)
```

---

## Quick Start — راه‌اندازی پروژه جدید

این فرایند **در آینده** (بعد از اتمام trading-system فاز نهایی) قابل استفاده است:

### مرحله ۱ — استخراج Template (در پایان trading-system)

```cmd
# در پایان trading-system، Claude اسکریپتی می‌سازد:
python scripts/99_extract_template.py --target ../python-react-skeleton

# این اسکریپت:
# - بخش‌های 🟢 (100% reusable) را کپی می‌کند
# - بخش‌های 🟡 (80%) را با علامت TODO کپی می‌کند
# - بخش‌های 🔴 (domain) را skip می‌کند
# - یک README جدید با instructions می‌سازد
```

### مرحله ۲ — Clone برای پروژه جدید

```cmd
git clone https://github.com/yourusername/python-react-skeleton.git my-new-project
cd my-new-project
```

### مرحله ۳ — Configuration

ویرایش `.env`:
```bash
APP_NAME=My New Project       # ← تغییر
APP_DESCRIPTION=...            # ← تغییر
JWT_SECRET=<generate-new>      # ← مهم!
DATABASE_URL=sqlite+aiosqlite:///./newproject.db
CORS_ORIGINS=http://localhost:5173
DEFAULT_ADMIN_USERNAME=admin
DEFAULT_ADMIN_PASSWORD=<change>
```

ویرایش `package.json` (frontend):
```json
{
  "name": "my-new-project-frontend",
  "version": "0.1.0"
}
```

ویرایش متن‌های UI:
- `frontend/src/pages/LoginPage.jsx`: عنوان
- `frontend/src/pages/HomePage.jsx`: عنوان h1

### مرحله ۴ — افزودن دامنه پروژه

برای هر مدل جدید:

```python
# 1. backend/app/models/your_model.py
class YourModel(Base):
    __tablename__ = "your_models"
    id = Column(Integer, primary_key=True)
    # ...

# 2. backend/app/repositories/your_model_repository.py
class YourModelRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(YourModel, db)
    # specific methods...

# 3. backend/app/api/v1/routes/your_models.py
@router.get("/your-models")
async def list_your_models(repo: YourModelRepository = Depends(...)):
    return Response.success(await repo.list())

# 4. Migration
alembic revision --autogenerate -m "Add YourModel"
alembic upgrade head

# 5. Frontend page
# frontend/src/pages/YourModelsPage.jsx
```

### مرحله ۵ — Customize Theme (اختیاری)

برای brand دیگر:
1. باز کردن `frontend/src/themes/themes.js`
2. ساخت تم جدید با id منحصربه‌فرد
3. تنظیم همه CSS variables
4. (اختیاری) حذف تم‌های دیگر

### مرحله ۶ — Run

```cmd
python scripts/00b_post_unzip_setup.py
# سپس
cd backend && venv\Scripts\activate
uvicorn app.main:app --reload
# tab دیگر
cd frontend
npm run dev
```

---

## راهنمای adaptation برای هر بخش

### Adaptation #1 — تغییر Auth System

اگر می‌خواهید Auth متفاوتی داشته باشید (مثلاً OAuth Google):

1. **حفظ:** `jwt.py`, `dependencies.py`
2. **افزودن:** `google_oauth.py`
3. **تغییر:** `auth.py` route — افزودن `/auth/google/callback`
4. **به‌روزرسانی:** `LoginPage.jsx` — افزودن دکمه Google

### Adaptation #2 — تغییر Database

اگر می‌خواهید PostgreSQL:

1. **تغییر `.env`:** `DATABASE_URL=postgresql+asyncpg://...`
2. **نصب `asyncpg`:** `pip install asyncpg`
3. **بقیه کد:** بدون تغییر (SQLAlchemy abstraction)

### Adaptation #3 — افزودن Page جدید

الگو:

```jsx
// 1. ساخت page
// frontend/src/pages/MyNewPage.jsx
export default function MyNewPage() {
  return <div style={{ padding: 24 }}>...</div>;
}

// 2. ثبت route
// frontend/src/App.jsx
<Route path="/my-new" element={<MyNewPage />} />

// 3. لینک از HomePage یا navbar
<Link to="/my-new">صفحه جدید</Link>
```

### Adaptation #4 — تم سفارشی

```javascript
// frontend/src/themes/themes.js
export const themes = {
  // ... موجود
  
  'my-brand': {
    id: 'my-brand',
    name: 'تم برند من',
    isDark: false,
    vars: {
      '--color-primary': '#3B82F6',     // آبی
      '--color-bg': '#FAFAFA',
      // ... همه variables
    }
  }
};
```

### Adaptation #5 — حذف بخش‌های trading-specific

اگر domain شما trading نیست، این فایل‌ها را حذف کنید:
```
backend/app/models/ohlcv_data.py
backend/app/models/symbol.py
backend/app/models/exchange.py
backend/app/models/timeframe.py
backend/app/models/market.py
backend/app/repositories/ohlcv_repository.py
backend/app/api/v1/routes/ohlcv.py
backend/app/infrastructure/data_sources/excel_data_source.py
frontend/src/pages/ChartPage.jsx
```

و در:
- `frontend/src/App.jsx`: حذف route `/chart/:symbolId`
- `frontend/src/pages/HomePage.jsx`: حذف لینک نمودار

---

## Checklist استخراج Template

این چک‌لیست در **پایان trading-system** اجرا می‌شود:

### پیش از استخراج
- [ ] همه فاز‌های trading-system تکمیل شده؟
- [ ] همه اسناد به‌روز هستند؟
- [ ] تست‌ها pass می‌شوند؟
- [ ] هیچ TODO کوچک باقی نیست؟

### حین استخراج
- [ ] فایل‌های 🟢 (Reusable کامل) کپی شدند؟
- [ ] فایل‌های 🟡 (نسبتاً Reusable) با علامت TODO کپی شدند؟
- [ ] فایل‌های 🔴 (Domain) skip شدند؟
- [ ] `.env.example` با مقادیر generic بازنویسی شد؟
- [ ] `README.md` با instructions جدید بازنویسی شد؟
- [ ] `package.json` نام reset شد؟
- [ ] `pyproject.toml`/`requirements.txt` نام reset شد؟

### پس از استخراج
- [ ] در یک folder خالی، Quick Start را اجرا کردی؟
- [ ] login admin/admin کار می‌کند؟
- [ ] تغییر تم در `/settings` کار می‌کند؟
- [ ] Toast/ConfirmDialog کار می‌کنند؟
- [ ] هیچ اشاره‌ای به trading در template نمانده؟

---

## الگوهای رایج پروژه‌ها و adaptation آن‌ها

### الگوی A — Admin Dashboard

**مثال:** سامانه مدیریت کاربران شرکت  
**زمان تخمینی با template:** ۱-۲ روز

**Adaptation:**
1. حذف بخش‌های ترید
2. افزودن Models: Department، Employee، Role
3. افزودن Pages: EmployeesPage، DepartmentsPage، RolesPage
4. استفاده از همان theme/auth/settings

### الگوی B — E-commerce Admin

**زمان:** ۳-۵ روز

**Adaptation:**
1. Models: Product، Category، Order
2. Pages: ProductsPage، OrdersPage، InventoryPage
3. افزودن file upload برای تصاویر محصول (extension)

### الگوی C — Blog/CMS

**زمان:** ۲-۳ روز

**Adaptation:**
1. Models: Post، Tag، Category، Comment
2. Markdown editor (افزودن `@uiw/react-md-editor`)
3. Pages: PostsListPage، PostEditorPage

### الگوی D — Task Manager

**زمان:** ۱ روز

**Adaptation:**
1. Models: Project، Task، User
2. Pages: ProjectsPage، KanbanPage
3. (Optional) drag-and-drop (`react-beautiful-dnd`)

---

## Anti-Patterns در استفاده مجدد

### ❌ Anti-Pattern R1 — Copy-Paste کل پروژه

اشتباه: ساده‌ترین کار = clone کل پروژه + تغییر اسم‌ها.

```
my-new-project/
├── backend/  (همه trading-system با rename)
├── frontend/
└── ...
```

**چرا اشتباه:**
- کد domain ترید همراهش می‌آید
- اشاره‌های ترید در docs، settings، …
- bloat (فایل‌های بی‌استفاده)

**درست:** استخراج فقط بخش‌های 🟢 و 🟡.

### ❌ Anti-Pattern R2 — تغییر اصول بنیادی

اشتباه: "این پروژه نیاز به Auth ندارد، dependency injection را حذف می‌کنم."

**چرا اشتباه:**
- اگر بعداً Auth خواستی، باید دوباره بسازی
- Layered Architecture را خراب می‌کند

**درست:** Auth را غیرفعال نگه دار (همه routes public) ولی ساختار را حفظ کن.

### ❌ Anti-Pattern R3 — اضافه کردن بخش‌های "احتیاطی"

اشتباه: "ممکن است در آینده WebSocket لازم بشه، الان اضافه می‌کنم."

**چرا اشتباه:**
- YAGNI (You Aren't Gonna Need It)
- پیچیدگی بی‌مورد در template

**درست:** فقط بخش‌های که در ۸۰٪ پروژه‌ها استفاده می‌شوند را در template نگه دار.

### ❌ Anti-Pattern R4 — فراموش کردن Update Template

اشتباه: تو در پروژه جدید یک bug fix می‌کنی ولی به template back-port نمی‌کنی.

**درست:** اگر یک بهبود generic در پروژه جدید کشف کردی، در template هم اعمال کن.

---

## محتویات Template نهایی (Vision)

ساختار آینده `python-react-skeleton`:

```
python-react-skeleton/
├── backend/
│   ├── app/
│   │   ├── core/             (logger, exceptions, handlers, response)
│   │   ├── config/           (settings template)
│   │   ├── auth/             (JWT, bcrypt, dependencies)
│   │   ├── database/         (async SQLAlchemy setup)
│   │   ├── repositories/     (BaseRepository فقط)
│   │   ├── api/v1/routes/    (auth.py فقط)
│   │   ├── models/           (User فقط)
│   │   └── main.py
│   ├── alembic/
│   ├── tests/                (smoke tests)
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/common/ (همه ۶ component reusable)
│   │   ├── components/settings/ (۳ component)
│   │   ├── stores/           (auth, theme, toast, confirm, preferences)
│   │   ├── utils/            (numberFormat, dateFormat)
│   │   ├── themes/           (۵ تم)
│   │   ├── services/         (api.js)
│   │   ├── pages/            (Login, Home minimal, Settings)
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── .env.example
│   ├── package.json
│   └── vite.config.js
│
├── scripts/
│   ├── 00b_post_unzip_setup.py
│   └── (template helpers)
│
├── docs/                     (همه docs reusable)
│   ├── PROJECT_GOVERNANCE.md
│   ├── CLAUDE_CHECKLIST.md
│   ├── REUSABLE_SKELETON.md  (این سند)
│   ├── STYLE_GUIDE.md
│   ├── ONBOARDING_GUIDE.md
│   ├── GLOSSARY.md           (generic terms)
│   └── README_TEMPLATE.md
│
├── README.md                 (Getting Started)
├── CHANGELOG.md              (Template version log)
└── .gitignore
```

---

## TASK های مرتبط در Backlog

از `TASK_BACKLOG.md`:
- T2.04: ARCHITECTURE.md (با دیاگرام لایه‌ای)
- T?? (آینده): استخراج خودکار template

---

## 📌 پایان REUSABLE_SKELETON

**نسخه:** v1.0 (2026-05-17)  
**وضعیت:** Vision document — استخراج template در پایان پروژه trading-system
