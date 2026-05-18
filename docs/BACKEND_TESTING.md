# Backend Testing — راهنمای pytest برای backend

> **نسخه:** v1.0 (2026-05-18 — چت ۷ / T2.08)
> **Stack:** pytest + pytest-asyncio + pytest-cov + httpx.AsyncClient
> **مرجع بالاتر:** ANTI_PATTERNS.md (A10) + GIT_WORKFLOW.md

---

## فهرست

- [۱. نصب وابستگی‌ها](#۱-نصب-وابستگیها)
- [۲. ساختار پوشه‌ها](#۲-ساختار-پوشهها)
- [۳. اجرای تست‌ها](#۳-اجرای-تستها)
- [۴. Coverage Report](#۴-coverage-report)
- [۵. نوشتن تست جدید](#۵-نوشتن-تست-جدید)
- [۶. Fixtures موجود](#۶-fixtures-موجود)
- [۷. Markers](#۷-markers)
- [۸. تست async functions](#۸-تست-async-functions)
- [۹. CI/CD آینده](#۹-cicd-آینده)
- [۱۰. عیب‌یابی](#۱۰-عیبیابی)

---

## ۱. نصب وابستگی‌ها

🟦 **tab «1 backend»**

```cmd
cd D:\Projects\trading-system\backend
venv\Scripts\activate
pip install -r requirements.txt --no-audit --no-fund --prefer-offline
```

dev dependencies اضافه‌شده در v0.2.0:
- `pytest==8.2.2`
- `pytest-asyncio==0.23.7`
- `pytest-cov==5.0.0`

---

## ۲. ساختار پوشه‌ها

```
backend/
├── pytest.ini              ← config اصلی
├── .coveragerc             ← config coverage
├── tests/
│   ├── __init__.py
│   ├── conftest.py         ← fixtures مشترک
│   ├── unit/               ← تست بدون DB/HTTP
│   │   ├── __init__.py
│   │   ├── test_response.py
│   │   ├── test_security.py
│   │   └── test_exceptions.py
│   └── integration/        ← تست با ASGI client
│       ├── __init__.py
│       ├── test_health.py
│       └── test_root.py
```

### فلسفه — Unit vs Integration

| نوع | با چه چیزی کار می‌کند | سرعت | مارکر |
|---|---|---|---|
| **unit** | فقط توابع pure، schemas، helpers | <50ms | `@pytest.mark.unit` |
| **integration** | ASGI client (httpx)، DB in-memory | 100–500ms | `@pytest.mark.integration` |

---

## ۳. اجرای تست‌ها

🟦 **tab «1 backend»**

### همه تست‌ها
```cmd
cd D:\Projects\trading-system\backend
venv\Scripts\activate
pytest
```

### فقط unit ها
```cmd
pytest -m unit
```

### فقط integration ها
```cmd
pytest -m integration
```

### یک فایل خاص
```cmd
pytest tests/unit/test_response.py
```

### یک تست خاص
```cmd
pytest tests/unit/test_response.py::TestSuccessResponse::test_default
```

### verbose + خطاهای کوتاه
```cmd
pytest -v --tb=short
```

### توقف در اولین failure
```cmd
pytest -x
```

---

## ۴. Coverage Report

### اجرا با coverage

```cmd
pytest --cov=app --cov-report=term-missing
```

### Report HTML (قابل مرور در مرورگر)

```cmd
pytest --cov=app --cov-report=html
```

سپس `backend\htmlcov\index.html` را در مرورگر باز کنید.

### هدف Coverage فاز ۰

- **حداقل ۶۰٪** برای `app/core/*` (security, response, exceptions, config)
- **حداقل ۴۰٪** برای `app/services/*` (auth_service)
- **حداقل ۸۰٪** برای endpoints public (`/health`, `/`)
- **معاف فعلاً:** repositories (نیاز به DB in-memory test، فاز ۱)

### مثال خروجی موفق

```
---------- coverage: platform win32, python 3.11.x -----------
Name                              Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------------------
app/core/response.py                 12      0      0      0   100%
app/core/security.py                 38      6      4      1    83.3%
app/core/exceptions.py               45      2      0      0    95.6%
...
TOTAL                               520    180     78     34    66.4%
```

---

## ۵. نوشتن تست جدید

### الگوی unit test

```python
# tests/unit/test_my_module.py
import pytest
from app.my_module import my_function

pytestmark = pytest.mark.unit


class TestMyFunction:
    def test_normal_case(self):
        assert my_function(2, 3) == 5

    def test_edge_case_zero(self):
        assert my_function(0, 0) == 0

    def test_raises_on_negative(self):
        with pytest.raises(ValueError):
            my_function(-1, 0)
```

### الگوی integration test

```python
# tests/integration/test_my_endpoint.py
import pytest

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_my_endpoint_returns_200(client):
    r = await client.get("/api/v1/my-endpoint")
    assert r.status_code == 200
    assert r.json()["success"] is True


async def test_my_endpoint_requires_auth(client):
    r = await client.get("/api/v1/protected-endpoint")
    assert r.status_code == 401
```

### قانون نام‌گذاری

- فایل: `test_<module>.py`
- کلاس: `Test<Feature>` (اختیاری، برای grouping)
- تابع: `test_<scenario>` — توصیفی، نه `test_1`
- ❌ بد: `test_user`، `test_api`
- ✅ خوب: `test_health_endpoint_returns_200`، `test_password_truncated_to_72_bytes`

---

## ۶. Fixtures موجود

تعریف‌شده در `tests/conftest.py`:

| Fixture | scope | کاربرد |
|---|---|---|
| `anyio_backend` | function | برمی‌گرداند `"asyncio"` |
| `app_module` | session | یک‌بار import می‌کند FastAPI app |
| `client` | function | `httpx.AsyncClient` متصل به ASGI app |

### استفاده

```python
async def test_with_client(client):
    r = await client.get("/api/v1/health")
    assert r.status_code == 200
```

### اضافه کردن fixture جدید

```python
# tests/conftest.py
@pytest.fixture
def sample_user():
    return {"username": "test_user", "password": "test123"}
```

---

## ۷. Markers

تعریف‌شده در `pytest.ini`:

| Marker | کاربرد |
|---|---|
| `unit` | تست بدون DB/شبکه — سریع |
| `integration` | تست با ASGI client — متوسط |
| `slow` | بیشتر از ۱ ثانیه — جدا از CI سریع |

### اعمال marker

```python
# روی کل فایل
pytestmark = pytest.mark.unit

# یا روی یک تست
@pytest.mark.slow
def test_heavy():
    ...
```

### اجرای انتخابی

```cmd
pytest -m "unit and not slow"
pytest -m "integration"
```

---

## ۸. تست async functions

این پروژه async-only است (تصمیم #۲۱). برای تست:

### تنظیم automatic mode

در `pytest.ini`:
```ini
asyncio_mode = auto
```

این یعنی هر تابع `async def test_*` خودکار async است.

### بدون auto mode (اختیاری)

```python
@pytest.mark.asyncio
async def test_something():
    ...
```

### تست exception async

```python
async def test_raises_async():
    with pytest.raises(NotFoundError):
        await service.get_or_404(id=99999)
```

---

## ۹. CI/CD آینده

برنامه (Tier 3):

| فاز | اقدام |
|---|---|
| فاز ۱ | افزودن DB in-memory fixture برای تست repositories |
| فاز ۲ | افزودن GitHub Actions workflow: `pytest + coverage` |
| فاز ۳ | حداقل coverage threshold (`--cov-fail-under=60`) |

نمونه `.github/workflows/test.yml` (آینده):

```yaml
name: tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r backend/requirements.txt
      - run: cd backend && pytest --cov=app --cov-fail-under=60
```

---

## ۱۰. عیب‌یابی

### مشکل ۱: `ImportError: SECRET_KEY` در import کردن config

**علت:** `app/core/config.py` متغیر env را الزامی می‌داند.

**راه‌حل:** در ابتدای `conftest.py` (یا تست) تنظیم شده:
```python
os.environ.setdefault("SECRET_KEY", "test-secret-key-...")
os.environ.setdefault("ENCRYPTION_KEY", "...")
```

### مشکل ۲: `RuntimeError: Event loop is closed` در ویندوز

**علت:** Windows ProactorEventLoop با aiosqlite گاهی conflict.

**راه‌حل:** در `conftest.py` فقط asyncio backend استفاده می‌کنیم — این مشکل را حل می‌کند.

### مشکل ۳: تست‌های integration کند هستند

**علت:** هر تست یک ASGI startup/shutdown دارد.

**راه‌حل:** برای تست‌های بسیار سریع، روی unit متمرکز شوید. integration فقط برای تأیید endpoints.

### مشکل ۴: `ModuleNotFoundError: No module named 'app'`

**علت:** pytest از پوشه اشتباه اجرا می‌شود.

**راه‌حل:**

🟦 **tab «1 backend»**
```cmd
cd D:\Projects\trading-system\backend   :: حتماً وارد backend شوید
pytest
```

### مشکل ۵: `pytest-asyncio` warning درباره mode

**علت:** نسخه قدیمی config.

**راه‌حل:** `pytest.ini` شامل `asyncio_mode = auto` است — نباید warning بدهد.

---

## ۱۱. ارجاعات

- **ANTI_PATTERNS.md** — A10 (اسکریپت بدون تست)
- **API_DOCS.md** — endpoints که تست می‌شوند
- **GIT_WORKFLOW.md** — commit با scope `test(backend)`
- **PROJECT_GOVERNANCE.md** — مسئولیت‌های Claude برای تست

---

## 📌 پایان BACKEND_TESTING

**نسخه:** v1.0 (2026-05-18 — چت ۷ / T2.08)
**ساختار:** ۱۰ بخش + ۱۱ ارجاع
**تست‌های smoke آماده:** ۵ فایل (3 unit + 2 integration)
