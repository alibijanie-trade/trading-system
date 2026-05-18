# -*- coding: utf-8 -*-
"""
52_create_anti_patterns_doc.py — تولید docs/ANTI_PATTERNS.md (T2.07)

مستند ۱۰ anti-pattern کشف‌شده در این پروژه:
  A1  — Business logic در routes
  A2  — SQL queries در services
  A3  — بازگشت ORM models مستقیم به API
  A4  — Hardcoded secrets/config
  A5  — print() به‌جای logger
  A6  — Catching bare Exception
  A7  — Sync DB calls در async context
  A8  — اصلاح دستی فایل (نقض #۳۰)
  A9  — حذف محتوا از سند جامع (نقض #۲۴)
  A10 — اسکریپت بدون تست همراه (نقض #۲۲)

استفاده (از ریشه پروژه):
  python scripts\\52_create_anti_patterns_doc.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "ANTI_PATTERNS.md"


ANTI_PATTERNS_CONTENT = """# Anti-Patterns — الگوهای ضدمعماری پروژه

> **نسخه:** v1.0 (2026-05-18 — چت ۷ / T2.07)
> **مرجع بالاتر:** PROJECT_GOVERNANCE.md + سند جامع v2.8

این سند ۱۰ الگوی متداول ولی **اشتباه** را که در این پروژه باید **اجتناب** شوند، فهرست می‌کند. هر الگو شامل: توضیح، مثال نادرست (❌)، مثال صحیح (✅)، و تأثیر بلندمدت است.

---

## فهرست

- [چرا Anti-Patterns مهم‌اند؟](#چرا-anti-patterns-مهماند)
- [خلاصه ۱۰ Anti-Pattern](#خلاصه-۱۰-anti-pattern)
- [A1 — Business Logic در Routes](#a1--business-logic-در-routes)
- [A2 — SQL Queries در Services](#a2--sql-queries-در-services)
- [A3 — بازگشت ORM Models مستقیم به API](#a3--بازگشت-orm-models-مستقیم-به-api)
- [A4 — Hardcoded Secrets/Config](#a4--hardcoded-secretsconfig)
- [A5 — `print()` به‌جای Logger](#a5--print-بهجای-logger)
- [A6 — گرفتن `Exception` خالی](#a6--گرفتن-exception-خالی)
- [A7 — فراخوانی Sync در Async](#a7--فراخوانی-sync-در-async)
- [A8 — اصلاح دستی فایل (نقض #۳۰)](#a8--اصلاح-دستی-فایل-نقض-۳۰)
- [A9 — حذف محتوا از سند جامع (نقض #۲۴)](#a9--حذف-محتوا-از-سند-جامع-نقض-۲۴)
- [A10 — اسکریپت بدون تست همراه (نقض #۲۲)](#a10--اسکریپت-بدون-تست-همراه-نقض-۲۲)
- [قانون طلایی: Audit دوره‌ای](#قانون-طلایی-audit-دورهای)

---

## چرا Anti-Patterns مهم‌اند؟

این پروژه دارای **معماری لایه‌ای دقیق** است (سند ۱):

```
routes/  ←  presentation layer (فقط HTTP)
   ↓
services/  ←  business logic
   ↓
repositories/  ←  data access (SQL queries)
   ↓
models/  ←  ORM entities
```

هر anti-pattern یکی از **مرزهای لایه‌ها** را نقض می‌کند یا یک **قانون قفل‌شده** را شکسته. تأثیر:

- 🐌 **Tech Debt:** هر violation در آینده باید refactor شود
- 🧪 **تست‌ناپذیری:** کد mixed-concern قابل unit test نیست
- 🔄 **سختی تغییر:** یک bug در یک لایه به همه‌جا سرایت می‌کند
- 🔓 **آسیب امنیتی:** برخی anti-pattern ها (مثل hardcoded secrets) ریسک واقعی دارند

---

## خلاصه ۱۰ Anti-Pattern

| # | عنوان | لایه | شدت | قانون مرتبط |
|---|---|---|---|---|
| **A1** | Business logic در routes | Backend | 🔴 بحرانی | معماری لایه‌ای |
| **A2** | SQL در services | Backend | 🔴 بحرانی | معماری لایه‌ای |
| **A3** | بازگشت ORM models مستقیم | Backend | 🟡 متوسط | سند ۶.۲ |
| **A4** | Hardcoded secrets | Backend/Frontend | 🔴 بحرانی | سند ۱۰.۴ |
| **A5** | `print()` به‌جای logger | Backend | 🟡 متوسط | سند ۱۱ logging |
| **A6** | `except Exception:` خالی | Backend | 🟡 متوسط | سند ۱۰ error handling |
| **A7** | Sync در async | Backend | 🔴 بحرانی | FastAPI async pattern |
| **A8** | اصلاح دستی فایل | Process | 🟡 متوسط | قانون #۳۰ |
| **A9** | حذف از سند جامع | Process | 🔴 بحرانی | قانون #۲۴ |
| **A10** | اسکریپت بدون تست | Process | 🟡 متوسط | قانون #۲۲ |

---

## A1 — Business Logic در Routes

### 📋 توضیح

route ها (`app/api/v1/routes/*.py`) باید فقط:
- ورودی HTTP را به schema تبدیل کنند (`Depends`, `Body`, `Query`)
- service مناسب را صدا بزنند
- پاسخ را با `success_response()` برگردانند

**هر منطق business** (محاسبه، اعتبارسنجی پیچیده، orchestration چند منبع) باید در `services/` باشد.

### ❌ نادرست

```python
# app/api/v1/routes/auth.py
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm, db: AsyncSession = Depends(get_db)):
    # ❌ business logic داخل route
    user = await db.scalar(select(User).where(User.username == form.username))
    if not user or not bcrypt.verify(form.password, user.password_hash):
        raise HTTPException(401, "اطلاعات نامعتبر")
    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)
    await db.execute(insert(RefreshToken).values(...))
    await db.commit()
    return {"access_token": access, "refresh_token": refresh}
```

### ✅ صحیح

```python
# app/api/v1/routes/auth.py
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    tokens = await service.login(form.username, form.password)
    return success_response(data=tokens.model_dump(), message="ورود موفق")
```

```python
# app/services/auth_service.py
class AuthService:
    async def login(self, username: str, password: str) -> TokenPair:
        # ✅ business logic در service
        user = await self.user_repo.get_by_username(username)
        if not user or not self._verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        tokens = self._issue_tokens(user.id)
        await self.token_repo.store_refresh(tokens.refresh_token, user.id)
        return tokens
```

### 💥 تأثیر بلندمدت

- وقتی auth با OAuth یا SSO اضافه شود، باید همه routes تغییر کنند (به‌جای فقط service)
- تست route بدون mock کل DB ممکن نیست
- منطق `_verify_password` بین routes تکرار می‌شود (DRY violation)

### 📎 ارجاع

- سند جامع v2.8 بخش ۵ (معماری Backend)

---

## A2 — SQL Queries در Services

### 📋 توضیح

`services/` نباید مستقیماً `select()` یا `insert()` بنویسد. این کار فقط مال `repositories/` است.

### ❌ نادرست

```python
# app/services/ohlcv_service.py
async def get_candles(self, symbol_id: int, timeframe: str):
    # ❌ SQL در service
    stmt = select(OhlcvCandle).where(
        OhlcvCandle.symbol_id == symbol_id,
        OhlcvCandle.timeframe == timeframe,
    ).order_by(OhlcvCandle.timestamp)
    return (await self.db.scalars(stmt)).all()
```

### ✅ صحیح

```python
# app/repositories/ohlcv_repository.py
class OhlcvRepository:
    async def list_by_symbol_and_timeframe(
        self, symbol_id: int, timeframe: str, limit: int = 100,
    ) -> list[OhlcvCandle]:
        stmt = (
            select(OhlcvCandle)
            .where(OhlcvCandle.symbol_id == symbol_id, OhlcvCandle.timeframe == timeframe)
            .order_by(OhlcvCandle.timestamp)
            .limit(limit)
        )
        return list((await self.db.scalars(stmt)).all())
```

```python
# app/services/ohlcv_service.py
async def get_candles(self, symbol_id: int, timeframe: str):
    # ✅ delegation به repository
    return await self.ohlcv_repo.list_by_symbol_and_timeframe(symbol_id, timeframe)
```

### 💥 تأثیر بلندمدت

- وقتی DB تغییر کند (PostgreSQL، Redis cache layer)، باید همه services تغییر کنند
- query پیچیده در service غیرقابل تست بدون DB واقعی
- repository pattern قابلیت mock-سازی برای unit test را فراهم می‌کند

### 📎 ارجاع

- سند جامع v2.8 بخش ۵.۳ (Repository Pattern)

---

## A3 — بازگشت ORM Models مستقیم به API

### 📋 توضیح

هرگز `User` یا `OhlcvCandle` (SQLAlchemy ORM) را مستقیماً در پاسخ API برنگردانید. همیشه به Pydantic schema تبدیل کنید.

### ❌ نادرست

```python
@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return current_user  # ❌ ORM به‌طور مستقیم
```

دلایل:
- ممکن است فیلدهای حساس مانند `password_hash` نشت کنند
- Lazy-loaded relationship ها در serialization مشکل می‌سازند
- API schema با ORM coupling پیدا می‌کند

### ✅ صحیح

```python
@router.get("/me")
async def me(current_user: User = Depends(get_current_user)) -> dict:
    return success_response(
        data=UserMe.model_validate(current_user).model_dump(),
        message="اطلاعات کاربر",
    )
```

```python
# app/schemas/auth.py
class UserMe(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    role: str
    is_active: bool
    # ❌ password_hash نیست — صلاح نیست در پاسخ بیاید
```

### 💥 تأثیر بلندمدت

- نشت داده‌های حساس
- breaking change در DB schema = breaking change در API
- documentation خودکار FastAPI (OpenAPI) نامرتب می‌شود

### 📎 ارجاع

- سند جامع v2.8 بخش ۶.۲ (Response Wrapper)

---

## A4 — Hardcoded Secrets/Config

### 📋 توضیح

هیچ‌گاه password، API key، URL، یا config در کد hard-code نشود. همه چیز در `.env` و از طریق `settings` خوانده شود.

### ❌ نادرست

```python
# ❌ در کد
SECRET_KEY = "my-secret-key-1234"
DATABASE_URL = "sqlite+aiosqlite:///D:/trading.db"
ADMIN_PASSWORD = "admin123"
```

```javascript
// ❌ در frontend
const API_URL = "http://192.168.1.10:8000";
```

### ✅ صحیح

```python
# app/core/config.py
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    SECRET_KEY: str
    DATABASE_URL: str
    APP_ENV: str = "development"

settings = Settings()
```

```env
# .env (در .gitignore)
SECRET_KEY=<generated-secret>
DATABASE_URL=sqlite+aiosqlite:///./trading.db
APP_ENV=development
```

```javascript
// .env (frontend) — Vite
VITE_API_URL=http://localhost:8000
```

```javascript
// frontend/src/config.js
export const API_URL = import.meta.env.VITE_API_URL;
```

### 💥 تأثیر بلندمدت

- 🚨 **ریسک امنیتی واقعی** — push شدن secret به Git
- نیاز به rotate همه کلیدها در صورت leak
- تفاوت محیط dev/prod نیاز به rebuild دارد

### 📎 ارجاع

- سند جامع v2.8 بخش ۱۰.۴ (Security)
- `.gitignore` خط `*.env`

---

## A5 — `print()` به‌جای Logger

### 📋 توضیح

در FastAPI و asyncio، `print()` به stdout می‌رود ولی:
- بدون timestamp
- بدون level (INFO/WARNING/ERROR)
- در production قابل redirect به فایل/Sentry نیست
- در logger config تنظیم شده structured logging جا نمی‌گیرد

### ❌ نادرست

```python
async def login(self, username: str, password: str):
    print(f"User {username} attempting login")  # ❌
    user = await self.user_repo.get_by_username(username)
    if not user:
        print(f"User not found: {username}")  # ❌
        raise InvalidCredentialsError()
```

### ✅ صحیح

```python
from app.core.logging import get_logger

logger = get_logger(__name__)

async def login(self, username: str, password: str):
    logger.info("Login attempt for user: %s", username)  # ✅
    user = await self.user_repo.get_by_username(username)
    if not user:
        logger.warning("User not found: %s", username)  # ✅
        raise InvalidCredentialsError()
```

### 💡 نکات کاربردی

- `logger.info()` برای رویدادهای عادی
- `logger.warning()` برای موارد مشکوک ولی قابل قبول
- `logger.error()` برای خطاهایی که نیاز به توجه دارند
- **هرگز** password یا token در log نباشد (فقط username/user_id)
- از `%s` به جای f-string استفاده کنید — تنبل (lazy) و سریع‌تر

### 💥 تأثیر بلندمدت

- در production، print ها در stdout گم می‌شوند
- debug کردن مشکل بدون structured logging زمان‌بر است
- یکپارچگی با Sentry/Datadog ممکن نیست

### 📎 ارجاع

- سند جامع v2.8 بخش ۱۱ (Logging)
- `app/core/logging.py`

---

## A6 — گرفتن `Exception` خالی

### 📋 توضیح

`except Exception:` همه خطاها از جمله `KeyboardInterrupt`, `SystemExit`, و bug های واقعی را قورت می‌دهد. اگر می‌خواهید catch کنید، نوع دقیق را مشخص کنید.

### ❌ نادرست

```python
try:
    result = await some_operation()
except Exception:  # ❌ همه چیز را قورت می‌دهد
    pass  # ❌ بدتر: silent failure
```

### ✅ صحیح

```python
from app.core.exceptions import AppException
from sqlalchemy.exc import IntegrityError

try:
    result = await some_operation()
except IntegrityError as e:
    logger.warning("Duplicate entry: %s", e)
    raise AppException("داده قبلاً ثبت شده", code="DUPLICATE", status_code=409) from e
except AppException:
    # ✅ AppException در handler مرکزی پردازش می‌شود — اینجا re-raise
    raise
except Exception as e:
    # ✅ آخرین چاره: log + re-raise (نه pass!)
    logger.exception("Unexpected error in some_operation")
    raise
```

### 💥 تأثیر بلندمدت

- bug ها silent می‌شوند و در production هرگز کشف نمی‌شوند
- پیام مناسب به کاربر نمی‌رسد (خطای ۵۰۰ generic)
- debug کردن غیرممکن می‌شود

### 📎 ارجاع

- سند جامع v2.8 بخش ۱۰ (Error Handling)
- `app/core/exceptions.py`
- `app/core/handlers.py`

---

## A7 — فراخوانی Sync در Async

### 📋 توضیح

FastAPI روی asyncio اجرا می‌شود. اگر در یک endpoint `async def` فراخوانی blocking داشته باشید، **همه** request های همزمان block می‌شوند.

### ❌ نادرست

```python
import time
import requests  # ❌ blocking HTTP

@router.get("/external")
async def fetch_external():
    time.sleep(2)  # ❌ blocking
    r = requests.get("https://api.example.com/data")  # ❌ blocking
    return r.json()
```

نتیجه: هر درخواست ۲ ثانیه کل سرور را block می‌کند.

### ✅ صحیح

```python
import asyncio
import httpx  # ✅ async HTTP

@router.get("/external")
async def fetch_external():
    await asyncio.sleep(2)  # ✅ non-blocking
    async with httpx.AsyncClient() as client:
        r = await client.get("https://api.example.com/data")
    return r.json()
```

### 🔍 موارد رایج

| Blocking ❌ | Async ✅ |
|---|---|
| `requests.get()` | `httpx.AsyncClient.get()` |
| `time.sleep()` | `asyncio.sleep()` |
| `open(file).read()` | `aiofiles.open(file).read()` |
| `sqlite3.connect()` | `aiosqlite.connect()` (یا `AsyncSession`) |
| `pandas.read_excel()` (large) | `asyncio.to_thread(pandas.read_excel)` |

### 💥 تأثیر بلندمدت

- throughput سرور به‌شدت پایین می‌آید
- در load بالا → timeout و فروپاشی
- وضعیت deadlock در عملیات DB

### 📎 ارجاع

- سند جامع v2.8 بخش ۵.۲ (Async Stack)

---

## A8 — اصلاح دستی فایل (نقض #۳۰)

### 📋 توضیح

برای هر تغییر کوچک روی فایل موجود (افزودن خط، اصلاح یک مقدار)، **اسکریپت Python idempotent** بسازید — نه دستور دستی copy-paste یا edit در Notepad.

### ❌ نادرست

```
Claude: «فایل CLAUDE_CHECKLIST.md رو باز کن، خط ۲۳ این متن رو جایگزین کن: "..."»
```

مشکلات:
- اجرا نشدنی توسط Claude (فقط دستور برای انسان)
- در صورت تکرار، خطای انسانی محتمل
- بدون audit trail
- ضدِ idempotency

### ✅ صحیح

```python
# scripts/52_patch_checklist.py
def patch():
    path = Path("docs/CLAUDE_CHECKLIST.md")
    text = path.read_text(encoding="utf-8")

    # Idempotency check
    if "محتوای جدید" in text:
        print("[skip] از قبل اعمال شده")
        return

    old = "خط قدیمی"
    new = "خط جدید با محتوای دقیق"
    if old not in text:
        raise RuntimeError("انکر پیدا نشد")

    text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")
    print("✅ patch اعمال شد")
```

سپس قانون #۲۲: اسکریپت تست همراه `52b_test_patch_checklist.py`.

### 💥 تأثیر بلندمدت

- در ۱۰+ چت بعدی، Claude همان منطق را تکرار می‌کند → اتلاف وقت
- بدون اسکریپت، rollback ممکن نیست
- نقض اصل تکرارپذیری (Reproducibility)

### 📎 ارجاع

- قانون #۳۰ (سند جامع v2.8 جدول ۱.۹)
- قانون #۲۲ (تست همراه)

---

## A9 — حذف محتوا از سند جامع (نقض #۲۴)

### 📋 توضیح

سند جامع **هرگز** نباید بخش‌هایی از آن حذف شود. تنها افزودن و علامت‌گذاری `[منسوخ — vX.Y]` مجاز است.

### ❌ نادرست

نسخه جدید `v2.8` ساخته می‌شود و در آن:
- بخش‌های قدیمی فاز ۰ که «دیگر نیاز نیست» حذف شده‌اند
- توضیحات قدیمی auth که با نسخه جدید عوض شده، پاک شده‌اند

### ✅ صحیح

نسخه جدید `v2.8`:
- محتوای v2.7 کاملاً حفظ شده
- بخش‌های جدید **افزوده** شده‌اند
- بخش‌های منسوخ علامت‌گذاری شده‌اند:

```markdown
## ۶.۵ ساختار قدیمی auth (با token در URL)
> [منسوخ — v2.5] از v2.5 به بعد از OAuth2 + Bearer header استفاده می‌شود (سند ۶.۶).
```

### 💥 تأثیر بلندمدت

- از دست رفتن context تاریخی پروژه
- در آینده وقتی سؤال «چرا این کار انجام شد؟» مطرح شود، پاسخ پیدا نمی‌شود
- نقض اصل **تاریخچه پایدار** (Stable History)
- نقض قانون #۲۴ که در جدول ۱.۹ قفل‌شده است

### 📎 ارجاع

- قانون #۲۴ (سند جامع v2.8 جدول ۱.۹)
- سند ۱۶ (مدیریت دانش)

---

## A10 — اسکریپت بدون تست همراه (نقض #۲۲)

### 📋 توضیح

هر اسکریپت `{N}_*.py` که فایل تولید/اصلاح می‌کند، باید اسکریپت تست همراه `{N}b_test_*.py` داشته باشد.

### ❌ نادرست

```
scripts/
  ├── 47_upgrade_doc_to_v28.py    ← اسکریپت تغییر می‌دهد
  └── (تست همراه ندارد)              ← ❌ نقض #۲۲
```

پس از اجرا، هیچ‌کس نمی‌داند آیا تغییر درست اعمال شد یا نه.

### ✅ صحیح

```
scripts/
  ├── 47_upgrade_doc_to_v28.py    ← تغییر می‌دهد
  └── 47b_test_doc_v28.py         ← ✅ ۲۴ تست برای تأیید
```

تست همراه باید بررسی کند:
- آیا فایل خروجی موجود است؟
- آیا header به‌روز شده؟
- آیا content مورد انتظار اضافه شده؟
- آیا content قدیمی (که نباید حذف شود) همچنان موجود است؟
- آیا اجرای دوم idempotent است؟

### 💥 تأثیر بلندمدت

- اسکریپت موفق ولی خروجی اشتباه → کشف نشدنی
- در آینده وقتی refactor شد، نمی‌توان فهمید کجا breaking change رخ داده
- نقض اصل **Test-Driven Patch**

### 📎 ارجاع

- قانون #۲۲ (سند جامع v2.8 جدول ۱.۹)
- مثال خوب: `47_*.py` + `47b_*.py` + `48_*.py` + `48b_*.py`

---

## قانون طلایی: Audit دوره‌ای

### پایان هر چت

Claude باید قبل از فاز ۳ پایان چت، یک self-check روی این ۱۰ anti-pattern انجام دهد:

- [ ] **A1:** آیا business logic در route نوشته‌ام؟
- [ ] **A2:** آیا SQL در service گذاشته‌ام؟
- [ ] **A3:** آیا ORM model مستقیم برگردانده‌ام؟
- [ ] **A4:** آیا secret/config رو hard-code کرده‌ام؟
- [ ] **A5:** آیا `print()` استفاده کرده‌ام به‌جای logger؟
- [ ] **A6:** آیا `except Exception:` خالی نوشته‌ام؟
- [ ] **A7:** آیا blocking call در async گذاشته‌ام؟
- [ ] **A8:** آیا دستور دستی به جای اسکریپت Python داده‌ام؟
- [ ] **A9:** آیا چیزی از سند جامع حذف کرده‌ام؟
- [ ] **A10:** آیا اسکریپت تولید/اصلاح بدون تست همراه ساخته‌ام؟

اگر هر سؤال **YES** بود → **اصلاح قبل از تحویل** + ثبت در `CHAT_LOG.md`.

### معیار موفقیت

پروژه‌ای که در هر چت همه ۱۰ سؤال **NO** باشد، در مسیر **معماری سالم** قرار دارد.

---

## ارجاعات

- **PROJECT_GOVERNANCE.md** — مسئولیت‌های Claude (C1-C20)
- **CLAUDE_CHECKLIST.md** — فاز ۱ و ۲ و ۳
- **سند جامع v2.8** بخش ۱.۹ — قوانین قفل‌شده (#۲۲, #۲۴, #۳۰)
- **سند جامع v2.8** بخش ۵ — معماری Backend
- **GIT_WORKFLOW.md** — Anti-patterns در commit message
- **API_DOCS.md** — استفاده صحیح از endpoints

---

## 📌 پایان ANTI_PATTERNS

**نسخه:** v1.0 (2026-05-18 — چت ۷ / T2.07)
**ساختار:** ۱۰ anti-pattern + self-check
**مسئولیت اجرا:** Claude در پایان هر چت
"""


def write_if_changed(path: Path, content: str) -> bool:
    if path.exists():
        if path.read_text(encoding="utf-8") == content:
            return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    print("=" * 64)
    print("  52_create_anti_patterns_doc — تولید docs/ANTI_PATTERNS.md")
    print("=" * 64)
    print()

    written = write_if_changed(DOC, ANTI_PATTERNS_CONTENT)
    if written:
        print(f"  ✏️  ایجاد/به‌روزرسانی: {DOC.name}")
        print(f"  📏  حجم: {len(ANTI_PATTERNS_CONTENT):,} کاراکتر")
        print(f"  📄  تعداد خط: {ANTI_PATTERNS_CONTENT.count(chr(10))}")
    else:
        print(f"  ✓  no-op: {DOC.name} از قبل به‌روز است")

    print()
    print("=" * 64)
    print("  ✅ موفق")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
