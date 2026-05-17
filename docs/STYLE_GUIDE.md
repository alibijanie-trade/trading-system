# 🎨 STYLE_GUIDE — راهنمای Code Style و Naming Conventions

> **هدف یک‌خطی:** یکپارچگی کد در تمام پروژه — هر کد جدیدی باید این قواعد را رعایت کند.

> **محل قرارگیری:** `docs/STYLE_GUIDE.md`  
> **مرجع بالاتر:** سند جامع v2.7+ + `PROJECT_GOVERNANCE.md` بخش ۱۱ (Anti-Patterns)  
> **نسخه:** v1.0 (2026-05-17)

---

## 📑 فهرست

- [اصول کلی](#اصول-کلی)
- [قواعد Python (Backend)](#قواعد-python-backend)
- [قواعد JavaScript/React (Frontend)](#قواعد-javascriptreact-frontend)
- [قواعد CSS / Styling](#قواعد-css--styling)
- [قواعد Naming](#قواعد-naming)
- [قواعد فایل و پوشه](#قواعد-فایل-و-پوشه)
- [قواعد کامنت‌نویسی](#قواعد-کامنتنویسی)
- [قواعد Git Commit](#قواعد-git-commit)
- [الگوهای ممنوع (Anti-Patterns)](#الگوهای-ممنوع-anti-patterns)
- [الگوهای پیشنهادی](#الگوهای-پیشنهادی)

---

## اصول کلی

### ۱. Readability > Cleverness

```python
# ❌ زرنگ ولی نامفهوم
result = next(filter(lambda x: x.id == target_id, items), None)

# ✅ روشن
result = None
for item in items:
    if item.id == target_id:
        result = item
        break
```

### ۲. Explicit > Implicit

```python
# ❌ implicit
def calculate(data):
    return data * 1.09  # ۱.۰۹ چیست؟

# ✅ explicit
VAT_RATE = 1.09  # ۹٪ مالیات
def calculate(data):
    return data * VAT_RATE
```

### ۳. Single Responsibility

هر function، class، component، یا فایل باید **یک کار** انجام دهد.

### ۴. No Magic Numbers

```jsx
// ❌
<div style={{ marginTop: 14 }}>

// ✅ (در فاز ۰ قابل قبول، در فاز ۲+ به constants)
const SECTION_GAP = 14;
<div style={{ marginTop: SECTION_GAP }}>
```

### ۵. DRY (Don't Repeat Yourself)

اگر یک قطعه کد ۲ بار تکرار شد، مشکوک شو. اگر ۳ بار شد، حتماً refactor کن.

---

## قواعد Python (Backend)

### فایل header

هر فایل `.py` با این شروع می‌شود:

```python
# -*- coding: utf-8 -*-
"""
ماژول: shortdescription

شرح کامل ماژول...
"""
```

### Imports

به ترتیب (هر گروه با خط خالی):

```python
# 1. Standard library
from pathlib import Path
from datetime import datetime

# 2. Third-party
from fastapi import FastAPI, Depends
from sqlalchemy import select
from loguru import logger

# 3. Local
from app.config import settings
from app.models import User
from app.repositories import UserRepository
```

### Type Hints

**اجباری** برای function signatures:

```python
# ❌
def get_user(user_id, db):
    ...

# ✅
async def get_user(user_id: int, db: AsyncSession) -> User | None:
    ...
```

### Pydantic Models

```python
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    email: str | None = None
```

### Async/Await

```python
# ✅ همه DB calls
async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

# ❌ هرگز sync DB
def get_users(db):
    return db.query(User).all()  # ممنوع
```

### Exception Handling

```python
# ✅ specific
try:
    user = await repo.get_by_id(user_id)
except NotFoundException:
    raise HTTPException(404, "کاربر یافت نشد")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise

# ❌ catch همه
try:
    ...
except:  # bare except — هرگز
    pass
```

### Logging

```python
# ✅ Loguru
from loguru import logger
logger.info(f"User {user.id} logged in")

# ❌ print
print(f"User logged in")  # هرگز در production code
```

---

## قواعد JavaScript/React (Frontend)

### کامپوننت‌ها

```jsx
// ✅ Functional component با default export
export default function MyComponent({ prop1, prop2 = "default" }) {
  return <div>...</div>;
}

// ❌ Class component (فاز ۰ functional only)
class MyComponent extends React.Component { ... }
```

### Hooks

```jsx
// ✅ ترتیب hooks
export default function MyComponent() {
  // 1. useState
  const [count, setCount] = useState(0);
  
  // 2. useRef
  const inputRef = useRef(null);
  
  // 3. زoctust stores (هر کدام جدا برای optimize re-render)
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);
  
  // 4. useEffect ها
  useEffect(() => { ... }, []);
  
  // 5. event handlers (با use prefix یا handle prefix)
  const handleClick = () => { ... };
  
  // 6. render
  return <div>...</div>;
}
```

### Imports

```jsx
// به ترتیب
// 1. React core
import { useState, useEffect } from "react";

// 2. Third-party
import { Link, useNavigate } from "react-router-dom";

// 3. Local — stores
import useAuthStore from "../stores/authStore.js";

// 4. Local — utils
import { formatNumber } from "../utils/numberFormat.js";

// 5. Local — components
import SkeletonBlock from "../components/common/SkeletonBlock.jsx";
```

### Props destructuring

```jsx
// ✅ destructure در function signature
export default function Card({ title, description, onClick }) {
  return <div onClick={onClick}>...</div>;
}

// ❌ props.X
export default function Card(props) {
  return <div onClick={props.onClick}>...</div>;
}
```

### Conditional rendering

```jsx
// ✅ ساده
{isLoading && <Skeleton />}
{user ? <UserInfo /> : <LoginPrompt />}

// ❌ پیچیده در JSX
{isLoading ? <Skeleton /> : !error ? user ? <UserInfo /> : <Loading /> : <Error />}
// ↑ این را به متغیر یا helper جدا کن
```

### Event handlers

```jsx
// ✅ نام‌گذاری: handle*
const handleSubmit = () => { ... };
const handleInputChange = (e) => { ... };

<button onClick={handleSubmit}>
<input onChange={handleInputChange}>
```

### Async در React

```jsx
// ✅ async useEffect با pattern
useEffect(() => {
  let cancelled = false;
  
  const load = async () => {
    const data = await fetchData();
    if (cancelled) return;
    setData(data);
  };
  
  load();
  
  return () => { cancelled = true; };
}, []);

// ❌ async function مستقیم
useEffect(async () => { ... }, []);  // ممنوع
```

---

## قواعد CSS / Styling

### ۱. هیچ Hex Hardcoded

```jsx
// ❌
<div style={{ color: "#F0B90B", background: "#181A20" }}>

// ✅
<div style={{ color: "var(--color-primary)", background: "var(--color-bg)" }}>
```

این **مهم‌ترین** قانون style است. مرجع: Anti-Pattern A1.

### ۲. fontSize با rem

```jsx
// ❌
<h1 style={{ fontSize: 22 }}>

// ✅
<h1 style={{ fontSize: "1.57rem" }}>
```

جدول تبدیل (baseline = 14px):

| px | rem |
|---|---|
| 10 | 0.71 |
| 11 | 0.79 |
| 12 | 0.86 |
| 13 | 0.93 |
| 14 | 1 |
| 15 | 1.07 |
| 16 | 1.14 |
| 17 | 1.21 |
| 18 | 1.29 |
| 20 | 1.43 |
| 22 | 1.57 |
| 24 | 1.71 |

سایر مقادیر (padding, margin, width, …): به px قابل قبول است (فاز ۰).

### ۳. Variant Indicator Pattern

برای کامپوننت‌های typed (Toast، Dialog، Alert):

```jsx
// ✅ صحیح
<div style={{
  background: "var(--color-card)",      // کانتینر از تم
  border: "1px solid var(--color-border)",
  borderInlineStart: `4px solid ${variantColor}`,  // accent باریک
}}>
  <span style={{ color: variantColor }}>⚠</span>  {/* icon */}
  <p style={{ color: "var(--color-text)" }}>پیام</p>  {/* متن از تم */}
</div>

// ❌ کادر کامل با رنگ variant
<div style={{ background: variantColor, color: "white" }}>پیام</div>
```

### ۴. Interactive States

هر دکمه و input باید این state ها را داشته باشد:

```css
/* در index.css */
button:hover:not(:disabled) { filter: brightness(1.12); }
button:active:not(:disabled) { transform: translateY(1px); }
button:focus-visible { outline: 2px solid var(--color-primary); outline-offset: 2px; }
button:disabled { cursor: not-allowed; opacity: 0.5; }
```

این **در index.css** ست شده، نیازی به تکرار در هر کامپوننت نیست.

### ۵. RTL-Safe

```jsx
// ✅ logical properties
borderInlineStart: "4px solid red"      // در RTL = راست، در LTR = چپ
marginInlineEnd: 8                       // RTL-aware
paddingInline: "10px 20px"

// ❌ physical properties (مگر دلیل خاص)
borderLeft: "4px solid red"              // در RTL ممکن است اشتباه باشد
marginRight: 8
```

### ۶. Spacing Scale (پیشنهادی)

پراکنده نباشد:
- 4, 8, 12, 16, 20, 24, 32, 48 (px)

```jsx
// ✅
padding: 16
gap: 8

// ❌
padding: 13  // عدد عجیب — چرا 13؟
```

### ۷. Animations

استفاده از `@keyframes` در `index.css`، نه inline:

```css
@keyframes my-animation {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* استفاده */
.my-element {
  animation: my-animation 0.2s ease-out;
}
```

با پشتیبانی `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## قواعد Naming

### Python

| نوع | Convention | مثال |
|---|---|---|
| module | snake_case | `user_repository.py` |
| package | snake_case | `data_sources/` |
| class | PascalCase | `UserRepository` |
| function | snake_case | `get_user_by_id` |
| variable | snake_case | `current_user` |
| constant | UPPER_SNAKE | `MAX_RETRIES` |
| private | _underscore | `_internal_helper` |

### JavaScript / React

| نوع | Convention | مثال |
|---|---|---|
| component | PascalCase | `MyComponent` |
| component file | PascalCase.jsx | `MyComponent.jsx` |
| utility file | camelCase.js | `numberFormat.js` |
| hook | use* | `useThemeStore` |
| function | camelCase | `handleSubmit` |
| variable | camelCase | `userInfo` |
| constant | UPPER_SNAKE | `MAX_RETRIES` |
| private | _underscore | `_internalHelper` |

### CSS Variables

```css
--color-<purpose>          /* --color-primary, --color-bg */
--color-<purpose>-<state>  /* --color-card-hover */
--font-<purpose>           /* --font-size-base */
--shadow-<purpose>         /* --shadow-card */
```

### Generic vs Domain

```js
// ✅ Generic — قابل reuse
useAuthStore
useThemeStore
formatNumber
formatDate

// ✅ Domain — مخصوص ترید
OhlcvData
ChartPage
isoToUnix  // (اگر فقط برای OHLCV استفاده می‌شود)

// ❌ ترکیب نامناسب
tradingAuthStore  // چرا trading در auth؟
chartFormatNumber  // چرا chart در format؟
```

---

## قواعد فایل و پوشه

### ساختار

```
backend/app/
├── api/v1/routes/        ← فقط endpoint files
├── auth/                 ← JWT, deps, schemas
├── config/               ← settings
├── core/                 ← logger, exceptions, response, handlers
├── database/             ← connection, base
├── infrastructure/       ← data_sources, external integrations
├── models/               ← SQLAlchemy models
├── repositories/         ← DB queries
├── services/             ← business logic (اگر پیچیده شد)
└── main.py
```

```
frontend/src/
├── components/
│   ├── common/           ← reusable: ProtectedRoute, ThemeProvider, ...
│   ├── settings/         ← مخصوص SettingsPage
│   └── <feature>/        ← مخصوص feature خاص
├── pages/                ← یک فایل per route
├── stores/               ← zustand stores
├── services/             ← API client
├── themes/               ← تم‌ها
├── utils/                ← pure functions
├── App.jsx
├── main.jsx
└── index.css
```

### نام فایل

- یک فایل = یک export اصلی
- نام فایل = نام export (یا meaningful)

```
// ✅
UserRepository.py  → class UserRepository
formatNumber.js    → export formatNumber

// ❌
helpers.py         → ۲۰ تابع نامرتبط
utils.js           → خیلی generic
```

### حد و حدود اندازه فایل

- Python: < ~۳۰۰ خط (به جز models با schema بزرگ)
- React component: < ~۲۰۰ خط (اگر بزرگ شد، تقسیم کن)
- اگر فایل بزرگ شد، تقسیم به sub-modules

---

## قواعد کامنت‌نویسی

### Docstrings (Python)

```python
def calculate_returns(prices: list[float]) -> list[float]:
    """
    محاسبه بازدهی دوره‌ای از لیست قیمت‌ها.
    
    Args:
        prices: لیست قیمت‌ها به ترتیب زمانی.
    
    Returns:
        لیست بازدهی‌ها (یک مورد کمتر از prices).
    
    Raises:
        ValueError: اگر prices خالی باشد.
    """
    if not prices:
        raise ValueError("لیست قیمت‌ها نمی‌تواند خالی باشد")
    return [prices[i] / prices[i-1] - 1 for i in range(1, len(prices))]
```

### JSDoc (JavaScript)

```js
/**
 * فرمت‌بندی عدد با جداکننده سه‌رقمی.
 *
 * @param {number} value عدد ورودی
 * @param {object} options
 * @param {number} [options.decimals] تعداد رقم اعشار
 * @returns {string} عدد فرمت‌بندی‌شده
 *
 * @example
 *   formatNumber(1714) // "1,714"
 */
export function formatNumber(value, options = {}) { ... }
```

### Inline Comments — Why نه What

```python
# ❌ توضیح What (واضح است)
x = x + 1  # افزایش x

# ✅ توضیح Why
x = x + 1  # برای پوشش index صفر-based در نمایش
```

### TODO / FIXME

```python
# TODO(username): بهبود performance با cache در فاز ۲
# FIXME: rate limiting هنوز اعمال نشده — Bug #50 آینده
```

اگر TODO/FIXME می‌گذارید، در `TASK_BACKLOG.md` هم ثبت کنید.

---

## قواعد Git Commit

### Conventional Commits

```
<type>: <subject>

[body اختیاری]
```

**type ها:**

- `feat:` feature جدید
- `fix:` رفع Bug
- `docs:` فقط اسناد
- `style:` formatting، semicolons، …
- `refactor:` بازنویسی بدون تغییر رفتار
- `test:` تست
- `chore:` نگهداری، dependencies

**نمونه‌ها:**

```
feat: add SkeletonBlock component

اضافه شد SkeletonBlock با ۴ variant (rect, text, circle, line)
و shimmer animation طبق سند ۸.۳.

Closes: T8.3
```

```
fix: font size scaling broken (#47)

تبدیل همه inline fontSize از px به rem.
+ افزودن html { font-size: var(--font-size-base) }

Refs: Bug #47, TROUBLESHOOTING.md
```

### Pre-commit checklist (پیشنهادی)

- [ ] کد اجرا می‌شود؟
- [ ] tests pass می‌شوند؟
- [ ] hex hardcoded ندارم؟
- [ ] linter clean است؟
- [ ] commit message طبق convention است؟

---

## الگوهای ممنوع (Anti-Patterns)

از `PROJECT_GOVERNANCE.md` بخش ۱۱:

| ID | Anti-Pattern | چرا ممنوع |
|---|---|---|
| A1 | hex hardcoded در CSS/JSX | مغایر Theme Engine |
| A2 | Query مستقیم بیرون از Repository | شکست Repository Pattern |
| A3 | تست با Swagger UI | manual، slow، unshareable |
| A4 | حذف از سند | شکست No-Deletion principle |
| A5 | اسکریپت غیر idempotent | re-run خطا می‌دهد |
| A6 | اسکریپت بدون تست همراه | شکست قانون #۲۲ |
| A7 | کد منسوخ بدون علامت | confusing |
| A8 | فرض بدون پرسش | شکست اصل ۵ Governance |
| A9 | fontSize با px ثابت | شکست font scaling |
| A10 | به‌روزرسانی غیر-اتمیک | inconsistency فاجعه‌بار |

---

## الگوهای پیشنهادی

### Pattern P1 — write_if_changed (idempotency)

```python
def write_if_changed(path: Path, content: str, label: str) -> str:
    rel = path.relative_to(PROJECT_ROOT)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"  ✓ ایجاد:    {rel}  ({label})")
        return "created"
    
    current = path.read_text(encoding="utf-8")
    if current == content:
        print(f"  - بدون تغییر: {rel}  (idempotent)")
        return "unchanged"
    
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"  ✓ به‌روز:   {rel}  ({label})")
    return "updated"
```

### Pattern P2 — Variant Config

```jsx
const VARIANT_CONFIG = {
  danger:  { icon: "⚠", color: "var(--color-danger)" },
  warning: { icon: "⚠", color: "var(--color-warning)" },
  info:    { icon: "ℹ", color: "var(--color-info)" },
  success: { icon: "✓", color: "var(--color-success)" },
};

const cfg = VARIANT_CONFIG[variant] || VARIANT_CONFIG.info;
// استفاده: cfg.icon, cfg.color
```

### Pattern P3 — Promise-based Modal

```js
// در store
confirm: (opts) =>
  new Promise((resolve) => {
    set({ isOpen: true, ...opts, resolver: resolve });
  }),

// در کامپوننت
const ok = await askConfirm({ title, message });
if (!ok) return;
// ادامه عمل
```

### Pattern P4 — Async useEffect با cancel

```jsx
useEffect(() => {
  let cancelled = false;
  const load = async () => {
    const data = await fetchData();
    if (cancelled) return;
    setData(data);
  };
  load();
  return () => { cancelled = true; };
}, [deps]);
```

### Pattern P5 — Standard Response (Backend)

```python
from app.core.response import Response

# Success
return Response.success(data={"id": 1, "name": "..."})

# Error (در exception handler)
return Response.error(message="یافت نشد", status=404)
```

### Pattern P6 — Repository Pattern

```python
class UserRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)
    
    async def get_by_username(self, username: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    async def get_active_users(self) -> list[User]:
        result = await self.db.execute(
            select(User).where(User.is_active == True)
        )
        return result.scalars().all()
```

### Pattern P7 — `Intl` به‌جای کتابخانه

```js
// تاریخ
new Intl.DateTimeFormat("fa-IR-u-ca-persian", {
  year: "numeric", month: "2-digit", day: "2-digit"
}).format(date);

// عدد
new Intl.NumberFormat("en-US", {
  minimumFractionDigits: 2
}).format(value);
```

---

## 📌 پایان STYLE_GUIDE

**نسخه:** v1.0 (2026-05-17)  
**نکته:** این سند زنده است. اگر pattern یا قانونی کشف شد، اضافه شود.
