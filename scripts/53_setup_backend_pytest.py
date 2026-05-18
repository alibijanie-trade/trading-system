# -*- coding: utf-8 -*-
"""
53_setup_backend_pytest.py — راه‌اندازی pytest برای backend (T2.08)

این اسکریپت idempotent:
  ۱. به backend/requirements.txt افزودن: pytest, pytest-asyncio, pytest-cov
  ۲. ساخت backend/pytest.ini (تنظیمات اجرای تست)
  ۳. ساخت backend/.coveragerc (تنظیمات coverage)
  ۴. ساخت backend/tests/conftest.py (fixtures مشترک)
  ۵. ساخت ۵ فایل تست smoke:
       - tests/unit/test_response.py
       - tests/unit/test_security.py
       - tests/unit/test_exceptions.py
       - tests/integration/test_health.py
       - tests/integration/test_root.py
  ۶. ساخت docs/BACKEND_TESTING.md

استفاده (از ریشه پروژه):
  python scripts\\53_setup_backend_pytest.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"
TESTS = BACKEND / "tests"
DOCS = ROOT / "docs"


# ============================================================
# 1) requirements.txt — افزودن dev dependencies
# ============================================================

DEV_DEPS_BLOCK = """
# --- Testing (T2.08 — چت ۷) ---
pytest==8.2.2
pytest-asyncio==0.23.7
pytest-cov==5.0.0
"""

DEV_DEPS_MARKER = "# --- Testing (T2.08 — چت ۷) ---"


def patch_requirements() -> tuple[bool, str]:
    req = BACKEND / "requirements.txt"
    text = req.read_text(encoding="utf-8")
    if DEV_DEPS_MARKER in text:
        return False, "requirements.txt: dev deps از قبل افزوده شده"

    new_text = text.rstrip() + "\n" + DEV_DEPS_BLOCK
    req.write_text(new_text, encoding="utf-8")
    return True, "requirements.txt: ۳ dev dependency افزوده شد (pytest, pytest-asyncio, pytest-cov)"


# ============================================================
# 2) pytest.ini
# ============================================================

PYTEST_INI = """[pytest]
# pytest configuration — Trading System Backend
# T2.08 (چت ۷)

testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# asyncio
asyncio_mode = auto

# markers
markers =
    unit: تست‌های unit (بدون DB، بدون شبکه)
    integration: تست‌های یکپارچه (DB in-memory، HTTP test client)
    slow: تست‌های کند (بیشتر از یک ثانیه)

# output
addopts =
    -ra
    --strict-markers
    --strict-config
    --tb=short
    --showlocals

# warnings
filterwarnings =
    ignore::DeprecationWarning:passlib.*
    ignore::DeprecationWarning:jose.*
"""


# ============================================================
# 3) .coveragerc
# ============================================================

COVERAGERC = """[run]
source = app
branch = True
omit =
    */tests/*
    */migrations/*
    */__init__.py
    main.py

[report]
exclude_lines =
    pragma: no cover
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:

show_missing = True
skip_empty = True
precision = 1

[html]
directory = htmlcov
"""


# ============================================================
# 4) conftest.py — fixtures مشترک
# ============================================================

CONFTEST = '''# -*- coding: utf-8 -*-
"""
conftest.py — Fixtures مشترک pytest برای کل tests/

این فایل به‌صورت خودکار توسط pytest پیدا می‌شود.

Fixtures:
  - anyio_backend     : asyncio backend برای anyio
  - test_app          : FastAPI app برای تست (بدون DB)
  - test_client       : httpx.AsyncClient متصل به test_app
"""

from __future__ import annotations

import os

# قبل از import کردن app، متغیرهای محیطی الزامی را تنظیم کنیم
# تا config.py با خطا مواجه نشود.
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production-only-pytest")
os.environ.setdefault(
    "ENCRYPTION_KEY",
    "dGVzdC1lbmNyeXB0aW9uLWtleS0zMi1ieXRlcy1mb3ItcHl0ZXN0ISE=",
)
os.environ.setdefault("APP_ENV", "development")

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient


@pytest.fixture
def anyio_backend() -> str:
    """anyio backend — همیشه asyncio."""
    return "asyncio"


@pytest.fixture(scope="session")
def app_module():
    """Import lazy از app برای جلوگیری از side effects."""
    from main import app
    return app


@pytest_asyncio.fixture
async def client(app_module):
    """httpx AsyncClient متصل به ASGI app — برای تست endpoints."""
    transport = ASGITransport(app=app_module)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
'''


# ============================================================
# 5) Test files
# ============================================================

TEST_RESPONSE = '''# -*- coding: utf-8 -*-
"""
tests/unit/test_response.py — تست توابع response wrapper

پوشش:
  - success_response : ساختار {success, message, data, errors}
  - error_response   : ساختار خطا + errors list
"""

import pytest

from app.core.response import error_response, success_response


pytestmark = pytest.mark.unit


class TestSuccessResponse:
    def test_default(self):
        r = success_response()
        assert r["success"] is True
        assert r["message"] == "عملیات با موفقیت انجام شد"
        assert r["data"] is None
        assert r["errors"] is None

    def test_with_data(self):
        r = success_response(data={"id": 5}, message="ساخته شد")
        assert r["success"] is True
        assert r["data"] == {"id": 5}
        assert r["message"] == "ساخته شد"
        assert r["errors"] is None

    def test_data_can_be_list(self):
        r = success_response(data=[1, 2, 3])
        assert r["data"] == [1, 2, 3]


class TestErrorResponse:
    def test_default(self):
        r = error_response(message="خطا رخ داد")
        assert r["success"] is False
        assert r["message"] == "خطا رخ داد"
        assert r["data"] is None

    def test_with_errors(self):
        r = error_response(
            message="نامعتبر",
            errors=[{"code": "X", "message": "Y"}],
        )
        assert r["errors"] == [{"code": "X", "message": "Y"}]
'''


TEST_SECURITY = '''# -*- coding: utf-8 -*-
"""
tests/unit/test_security.py — تست bcrypt + JWT helpers

پوشش:
  - hash_password / verify_password
  - create_access_token / decode_token
  - رفتار رمز عبور > 72 بایت (truncate)
"""

import os

# قبل از import مطمئن باشیم env var ها هست
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production-only-pytest")
os.environ.setdefault(
    "ENCRYPTION_KEY",
    "dGVzdC1lbmNyeXB0aW9uLWtleS0zMi1ieXRlcy1mb3ItcHl0ZXN0ISE=",
)

import pytest

from app.core.security import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)


pytestmark = pytest.mark.unit


class TestPassword:
    def test_hash_returns_string(self):
        h = hash_password("password123")
        assert isinstance(h, str)
        assert h.startswith("$2b$") or h.startswith("$2a$")

    def test_hash_is_different_each_call(self):
        h1 = hash_password("password123")
        h2 = hash_password("password123")
        assert h1 != h2  # bcrypt salt تصادفی

    def test_verify_correct_password(self):
        h = hash_password("mypassword")
        assert verify_password("mypassword", h) is True

    def test_verify_wrong_password(self):
        h = hash_password("mypassword")
        assert verify_password("wrongpassword", h) is False

    def test_long_password_truncated_to_72_bytes(self):
        """bcrypt 4.x طولانی‌تر از 72 بایت را silently truncate نمی‌کند.
        پروژه باید خودش این کار را انجام دهد."""
        long_pwd = "a" * 100
        h = hash_password(long_pwd)
        # اگر truncation کار کند: همان رمز با همان اول 72 بایت verify می‌شود
        assert verify_password("a" * 72, h) is True


class TestJWT:
    def test_create_and_decode_access_token(self):
        token = create_access_token(subject="user-123")
        assert isinstance(token, str)
        payload = decode_token(token)
        assert payload["sub"] == "user-123"
        assert payload["type"] == "access"

    def test_decoded_has_exp(self):
        token = create_access_token(subject="user-123")
        payload = decode_token(token)
        assert "exp" in payload
'''


TEST_EXCEPTIONS = '''# -*- coding: utf-8 -*-
"""
tests/unit/test_exceptions.py — تست سلسله مراتب AppException

پوشش:
  - AppException + subclasses (status_code، default_message، default_code)
  - override پیام و کد
"""

import pytest

from app.core.exceptions import (
    AppException,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ValidationError,
)


pytestmark = pytest.mark.unit


class TestAppException:
    def test_base_default(self):
        e = AppException()
        assert e.status_code == 500
        assert e.code == "INTERNAL_ERROR"
        assert e.message == "خطای داخلی سرور"

    def test_override_message_and_code(self):
        e = AppException(message="custom", code="CUSTOM_CODE")
        assert e.message == "custom"
        assert e.code == "CUSTOM_CODE"


class TestSubclasses:
    def test_validation_error(self):
        e = ValidationError()
        assert e.status_code == 400
        assert e.code == "VALIDATION_ERROR"

    def test_authentication_error(self):
        e = AuthenticationError()
        assert e.status_code == 401
        assert e.code == "AUTHENTICATION_FAILED"

    def test_authorization_error(self):
        e = AuthorizationError()
        assert e.status_code == 403
        assert e.code == "ACCESS_DENIED"

    def test_not_found_error(self):
        e = NotFoundError()
        assert e.status_code == 404

    def test_details_is_dict(self):
        e = NotFoundError(details={"resource_id": 5})
        assert e.details == {"resource_id": 5}
'''


TEST_HEALTH = '''# -*- coding: utf-8 -*-
"""
tests/integration/test_health.py — تست GET /api/v1/health

پوشش:
  - status 200
  - ساختار پاسخ {success, message, data, errors}
  - data شامل status, version, environment, timestamp
"""

import pytest


pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_health_endpoint_returns_200(client):
    r = await client.get("/api/v1/health")
    assert r.status_code == 200


async def test_health_response_structure(client):
    r = await client.get("/api/v1/health")
    body = r.json()
    assert "success" in body
    assert "message" in body
    assert "data" in body
    assert "errors" in body
    assert body["success"] is True
    assert body["errors"] is None


async def test_health_data_fields(client):
    r = await client.get("/api/v1/health")
    data = r.json()["data"]
    assert data["status"] == "ok"
    assert "version" in data
    assert "environment" in data
    assert "timestamp" in data
'''


TEST_ROOT = '''# -*- coding: utf-8 -*-
"""
tests/integration/test_root.py — تست GET /

پوشش:
  - status 200
  - ساختار پاسخ استاندارد
"""

import pytest


pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


async def test_root_returns_200(client):
    r = await client.get("/")
    assert r.status_code == 200


async def test_root_returns_app_info(client):
    r = await client.get("/")
    data = r.json()["data"]
    assert "name" in data
    assert "version" in data
    assert data["docs"] == "/docs"
'''


# ============================================================
# 6) BACKEND_TESTING.md
# ============================================================

BACKEND_TESTING_DOC = """# Backend Testing — راهنمای pytest برای backend

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
cd D:\\Projects\\trading-system\\backend
venv\\Scripts\\activate
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
cd D:\\Projects\\trading-system\\backend
venv\\Scripts\\activate
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

سپس `backend\\htmlcov\\index.html` را در مرورگر باز کنید.

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
cd D:\\Projects\\trading-system\\backend   :: حتماً وارد backend شوید
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
"""


# ============================================================
# helper: write_if_changed
# ============================================================


def write_if_changed(path: Path, content: str) -> bool:
    if path.exists():
        if path.read_text(encoding="utf-8") == content:
            return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


# ============================================================
# main
# ============================================================

FILES = [
    ("backend/pytest.ini", PYTEST_INI),
    ("backend/.coveragerc", COVERAGERC),
    ("backend/tests/conftest.py", CONFTEST),
    ("backend/tests/unit/test_response.py", TEST_RESPONSE),
    ("backend/tests/unit/test_security.py", TEST_SECURITY),
    ("backend/tests/unit/test_exceptions.py", TEST_EXCEPTIONS),
    ("backend/tests/integration/test_health.py", TEST_HEALTH),
    ("backend/tests/integration/test_root.py", TEST_ROOT),
    ("docs/BACKEND_TESTING.md", BACKEND_TESTING_DOC),
]


def main() -> int:
    print("=" * 64)
    print("  53_setup_backend_pytest — راه‌اندازی pytest برای backend")
    print("=" * 64)
    print()

    # 1) requirements.txt
    changed, msg = patch_requirements()
    print(f"  {'✏️' if changed else '✓'}  {msg}")

    # 2-9) همه فایل‌ها
    total_changes = 1 if changed else 0
    for rel, content in FILES:
        path = ROOT / rel
        if write_if_changed(path, content):
            print(f"  ✏️  {rel}")
            total_changes += 1
        else:
            print(f"  ✓  no-op: {rel}")

    print()
    print("=" * 64)
    if total_changes == 0:
        print("  ✅ idempotent — هیچ تغییری اعمال نشد")
    else:
        print(f"  ✅ موفق — {total_changes} تغییر اعمال شد")
    print("=" * 64)
    print()
    print("📌 گام بعدی:")
    print("   🟦 tab «1 backend»")
    print("     cd backend")
    print("     venv\\Scripts\\activate")
    print(
        "     pip install pytest==8.2.2 pytest-asyncio==0.23.7 pytest-cov==5.0.0 --no-audit --no-fund"
    )
    print("     pytest -v")
    return 0


if __name__ == "__main__":
    sys.exit(main())
