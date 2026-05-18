# API Documentation — سامانه هوشمند ترید

> **نسخه:** v1.0 (2026-05-18 — چت ۷ / T2.09)
> **API Version:** v0.2.0
> **Base URL:** `http://localhost:8000/api/v1`
> **Swagger UI:** `http://localhost:8000/docs`
> **مرجع بالاتر:** سند جامع v2.8 بخش ۶

---

## فهرست

- [۱. اطلاعات کلی](#۱-اطلاعات-کلی)
- [۲. ساختار استاندارد پاسخ](#۲-ساختار-استاندارد-پاسخ)
- [۳. احراز هویت (OAuth2 + Bearer)](#۳-احراز-هویت-oauth2--bearer)
- [۴. کدهای HTTP و خطا](#۴-کدهای-http-و-خطا)
- [۵. Endpoints](#۵-endpoints)
  - [۵.۱ `GET /` — Root](#۵۱-get--root)
  - [۵.۲ `GET /api/v1/health` — Health Check](#۵۲-get-apiv1health--health-check)
  - [۵.۳ `POST /api/v1/auth/login` — ورود](#۵۳-post-apiv1authlogin--ورود)
  - [۵.۴ `POST /api/v1/auth/refresh` — توکن جدید](#۵۴-post-apiv1authrefresh--توکن-جدید)
  - [۵.۵ `POST /api/v1/auth/logout` — خروج](#۵۵-post-apiv1authlogout--خروج)
  - [۵.۶ `GET /api/v1/auth/me` — اطلاعات کاربر فعلی](#۵۶-get-apiv1authme--اطلاعات-کاربر-فعلی)
  - [۵.۷ `GET /api/v1/ohlcv/{symbol_id}` — کندل‌ها](#۵۷-get-apiv1ohlcvsymbol_id--کندلها)
- [۶. مثال‌های End-to-End](#۶-مثالهای-end-to-end)
- [۷. عیب‌یابی](#۷-عیبیابی)
- [۸. تست با ابزارهای مختلف](#۸-تست-با-ابزارهای-مختلف)

---

## ۱. اطلاعات کلی

| ویژگی | مقدار |
|---|---|
| **Framework** | FastAPI 0.111.0 |
| **API Version** | `v0.2.0` |
| **Base URL** | `http://localhost:8000/api/v1` |
| **Documentation** | `http://localhost:8000/docs` (Swagger UI خودکار) |
| **OpenAPI Schema** | `http://localhost:8000/openapi.json` |
| **CORS** | فعال (طبق `CORS_ORIGINS` در `.env`) |
| **Content-Type پیش‌فرض** | `application/json` (به‌جز `/auth/login` که `multipart/form-data`) |
| **زبان پیام** | فارسی |

### Endpoint Map خلاصه

| # | Method | Path | Auth | تگ |
|---|---|---|---|---|
| ۱ | GET | `/` | ❌ | Root |
| ۲ | GET | `/api/v1/health` | ❌ | Health |
| ۳ | POST | `/api/v1/auth/login` | ❌ | Auth |
| ۴ | POST | `/api/v1/auth/refresh` | ❌ | Auth |
| ۵ | POST | `/api/v1/auth/logout` | ✅ | Auth |
| ۶ | GET | `/api/v1/auth/me` | ✅ | Auth |
| ۷ | GET | `/api/v1/ohlcv/{symbol_id}` | ✅ | OHLCV |

---

## ۲. ساختار استاندارد پاسخ

**هر پاسخ API** (موفق یا خطا) دارای این ۴ کلید است (سند ۶ بند ۶.۲):

```json
{
  "success": true,
  "message": "پیام فارسی برای نمایش به کاربر",
  "data": { /* پاسخ یا null */ },
  "errors": null
}
```

### نمونه پاسخ موفق

```json
{
  "success": true,
  "message": "ورود موفق",
  "data": {
    "access_token": "eyJhbGciOi...",
    "refresh_token": "eyJhbGciOi...",
    "token_type": "bearer",
    "expires_in": 1800
  },
  "errors": null
}
```

### نمونه پاسخ خطا

```json
{
  "success": false,
  "message": "داده‌های ورودی نامعتبر است",
  "data": null,
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "field": "body.refresh_token",
      "message": "Field required",
      "type": "missing"
    }
  ]
}
```

> ⚠️ **هرگز** ساختار پاسخ را تغییر ندهید. این قرارداد بین Backend و Frontend است.

---

## ۳. احراز هویت (OAuth2 + Bearer)

### جریان کلی

```
1. کاربر → POST /auth/login (username + password)
2. API   → access_token (۳۰ دقیقه) + refresh_token (۷ روز)
3. کاربر → endpoint های protected با هدر:
           Authorization: Bearer <access_token>
4. وقتی access منقضی شد → POST /auth/refresh
5. خروج → POST /auth/logout (refresh token revoke می‌شود)
```

### مدت اعتبار توکن‌ها

| توکن | مدت پیش‌فرض | قابل تغییر در |
|---|---|---|
| access_token | ۳۰ دقیقه (`1800` ثانیه) | `.env` → `ACCESS_TOKEN_EXPIRE_MINUTES` |
| refresh_token | ۷ روز | `.env` → `REFRESH_TOKEN_EXPIRE_DAYS` |

### هدر برای endpoint های Auth-protected

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### رفتار خطا

| وضعیت توکن | HTTP | پاسخ |
|---|---|---|
| توکن وجود ندارد | `401` | `Authorization header missing` |
| توکن نامعتبر | `401` | `توکن نامعتبر است` |
| توکن منقضی | `401` | `توکن منقضی شده — لطفاً refresh کنید` |
| توکن valid ولی user inactive | `403` | `حساب غیرفعال است` |

---

## ۴. کدهای HTTP و خطا

| HTTP | معنا | سناریو |
|---|---|---|
| `200` | OK | عملیات موفق |
| `201` | Created | منبع جدید ساخته شد |
| `400` | Bad Request | داده ورودی نامعتبر (validation error) |
| `401` | Unauthorized | احراز هویت ناموفق یا توکن نامعتبر |
| `403` | Forbidden | احراز هویت موفق ولی دسترسی ندارد |
| `404` | Not Found | منبع وجود ندارد (مثلاً `symbol_id` نامعتبر) |
| `422` | Unprocessable | Pydantic validation error در FastAPI |
| `500` | Internal Error | خطای ناشناخته سرور (لاگ شده) |

### کدهای خطای دامنه پروژه

ساختار `errors[]`:

```json
{
  "code": "USER_NOT_FOUND",
  "field": "username",
  "message": "کاربری با این نام یافت نشد",
  "type": "value_error"
}
```

| code | معنا |
|---|---|
| `VALIDATION_ERROR` | داده ورودی پاس Pydantic نشد |
| `AUTH_INVALID_CREDENTIALS` | username/password اشتباه |
| `AUTH_TOKEN_EXPIRED` | توکن منقضی شده |
| `AUTH_TOKEN_INVALID` | توکن نامعتبر |
| `SYMBOL_NOT_FOUND` | symbol_id در DB وجود ندارد |
| `OHLCV_NOT_FOUND` | کندلی برای ترکیب symbol+timeframe نیست |

---

## ۵. Endpoints

### ۵.۱ `GET /` — Root

**نقش:** صفحه ریشه — اطلاعات کلی API.

**Auth:** ❌

**Request:**
```http
GET /
```

**Response 200:**
```json
{
  "success": true,
  "message": "سامانه هوشمند ترید فعال است",
  "data": {
    "name": "Trading System",
    "version": "0.2.0",
    "docs": "/docs",
    "health": "/api/v1/health"
  },
  "errors": null
}
```

---

### ۵.۲ `GET /api/v1/health` — Health Check

**نقش:** بررسی سلامت API — برای monitoring و readiness probe.

**Auth:** ❌

**Request:**
```http
GET /api/v1/health
```

**Response 200:**
```json
{
  "success": true,
  "message": "API سالم است",
  "data": {
    "status": "ok",
    "version": "0.2.0",
    "environment": "development",
    "timestamp": "2026-05-18T05:30:00.123456+00:00"
  },
  "errors": null
}
```

**کاربردهای رایج:**
- Pre-flight check قبل از سایر درخواست‌ها
- Liveness/Readiness probe در Kubernetes/Docker
- مانیتورینگ uptime

---

### ۵.۳ `POST /api/v1/auth/login` — ورود

**نقش:** ورود کاربر با username/password — استاندارد OAuth2 password flow.

**Auth:** ❌

**Content-Type:** `application/x-www-form-urlencoded` (نه JSON!)

**Request:**
```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin123
```

**Form Fields:**
| فیلد | نوع | الزامی |
|---|---|---|
| `username` | string | ✅ |
| `password` | string | ✅ |

**Response 200:**
```json
{
  "success": true,
  "message": "ورود موفق",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800
  },
  "errors": null
}
```

**خطاها:**
- `401`: username یا password اشتباه
- `403`: حساب غیرفعال شده
- `422`: فیلد form ارسال نشده

> 💡 **نکته Swagger UI:** روی دکمه `Authorize` (آیکون قفل) کلیک کنید. فقط username/password بدهید — Swagger توکن را خودش در همه درخواست‌های بعدی استفاده می‌کند.

---

### ۵.۴ `POST /api/v1/auth/refresh` — توکن جدید

**نقش:** صدور access_token جدید بدون نیاز به re-login.

**Auth:** ❌ (فقط نیاز به refresh_token در body)

**Request:**
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response 200:**
```json
{
  "success": true,
  "message": "توکن جدید صادر شد",
  "data": {
    "access_token": "eyJhbGc... (جدید)",
    "refresh_token": "eyJhbGc... (همان قبلی یا جدید بسته به rotation)",
    "token_type": "bearer",
    "expires_in": 1800
  },
  "errors": null
}
```

**خطاها:**
- `401`: refresh_token منقضی، revoke شده، یا نامعتبر است

---

### ۵.۵ `POST /api/v1/auth/logout` — خروج

**نقش:** خروج کاربر — refresh_token باطل می‌شود.

**Auth:** ✅ (هدر `Authorization: Bearer <access_token>`)

**Request:**
```http
POST /api/v1/auth/logout
Content-Type: application/json
Authorization: Bearer eyJhbGc...

{
  "refresh_token": "eyJhbGc..."
}
```

**Response 200:**
```json
{
  "success": true,
  "message": "خروج موفق",
  "data": null,
  "errors": null
}
```

> ⚠️ **نکته:** access_token پس از خروج تا انقضای طبیعی (۳۰ دقیقه) همچنان معتبر می‌ماند. برای blacklist واقعی نیاز به Redis در فاز ۵+ است.

---

### ۵.۶ `GET /api/v1/auth/me` — اطلاعات کاربر فعلی

**نقش:** دریافت اطلاعات کاربر — مفید برای تأیید توکن و نمایش پروفایل.

**Auth:** ✅

**Request:**
```http
GET /api/v1/auth/me
Authorization: Bearer eyJhbGc...
```

**Response 200:**
```json
{
  "success": true,
  "message": "اطلاعات کاربر",
  "data": {
    "id": 1,
    "username": "admin",
    "role": "admin",
    "is_active": true
  },
  "errors": null
}
```

**خطاها:**
- `401`: توکن نامعتبر یا منقضی

---

### ۵.۷ `GET /api/v1/ohlcv/{symbol_id}` — کندل‌ها

**نقش:** دریافت کندل‌های یک نماد در یک تایم‌فریم — مرتب صعودی (قدیمی‌ترین اول).

**Auth:** ✅

**Path Parameters:**
| پارامتر | نوع | توضیح |
|---|---|---|
| `symbol_id` | int | شناسه نماد (FK به جدول symbols) |

**Query Parameters:**
| پارامتر | نوع | پیش‌فرض | توضیح |
|---|---|---|---|
| `timeframe` | string | — (الزامی) | `1d`, `1h`, `15m`, `5m` و … |
| `limit` | int | `100` | حداکثر کندل (۱ تا ۱۰۰۰) |
| `offset` | int | `0` | شروع از کندل چندم |
| `from_ts` | datetime (ISO 8601) | — | فقط کندل‌های ≥ این زمان |
| `to_ts` | datetime (ISO 8601) | — | فقط کندل‌های ≤ این زمان |

**Request:**
```http
GET /api/v1/ohlcv/1?timeframe=1d&limit=50&offset=0
Authorization: Bearer eyJhbGc...
```

**Response 200:**
```json
{
  "success": true,
  "message": "50 کندل بازگردانده شد",
  "data": {
    "symbol_id": 1,
    "timeframe": "1d",
    "count": 50,
    "total": 1714,
    "limit": 50,
    "offset": 0,
    "candles": [
      {
        "timestamp": "2024-01-01T00:00:00+00:00",
        "open": 42283.5,
        "high": 42950.1,
        "low": 41912.0,
        "close": 42795.6,
        "volume": 18342.5
      }
      // ...
    ]
  },
  "errors": null
}
```

**خطاها:**
- `401`: توکن نامعتبر
- `404`: `symbol_id` در DB وجود ندارد
- `422`: `timeframe` ارسال نشده، یا `limit` خارج از بازه ۱–۱۰۰۰

> 💡 **رابطه `count` و `total`:**
> - `count` = تعداد کندل در پاسخ این درخواست (با اعمال limit/offset/from_ts/to_ts)
> - `total` = تعداد کل کندل برای فیلتر بالا (بدون اعمال limit/offset)
> برای pagination کلاینت از `total` استفاده می‌کند.

---

## ۶. مثال‌های End-to-End

### ۶.۱ — جریان کامل با curl (Windows cmd)

🟦 **tab «1 backend»**

```cmd
:: ۱) Health check (بدون auth)
curl http://localhost:8000/api/v1/health

:: ۲) ورود — توکن‌ها را در متغیر می‌گیریم
:: نکته: curl در Windows با cmd از syntax %% استفاده می‌کند
curl -X POST http://localhost:8000/api/v1/auth/login ^
     -H "Content-Type: application/x-www-form-urlencoded" ^
     -d "username=admin&password=admin123"

:: ۳) GET /auth/me با access_token
curl http://localhost:8000/api/v1/auth/me ^
     -H "Authorization: Bearer <access_token>"

:: ۴) دریافت کندل‌ها
curl "http://localhost:8000/api/v1/ohlcv/1?timeframe=1d&limit=10" ^
     -H "Authorization: Bearer <access_token>"

:: ۵) خروج
curl -X POST http://localhost:8000/api/v1/auth/logout ^
     -H "Content-Type: application/json" ^
     -H "Authorization: Bearer <access_token>" ^
     -d "{\"refresh_token\":\"<refresh_token>\"}"
```

### ۶.۲ — جریان کامل با httpx (Python)

🟩 **tab «2 scripts»**

```python
import httpx

BASE = "http://localhost:8000/api/v1"

with httpx.Client(base_url=BASE) as c:
    # ۱) Health
    r = c.get("/health")
    print("health:", r.json()["data"]["status"])

    # ۲) Login (form data!)
    r = c.post("/auth/login", data={"username": "admin", "password": "admin123"})
    tokens = r.json()["data"]
    access = tokens["access_token"]
    refresh = tokens["refresh_token"]

    # ۳) Authenticated request
    auth = {"Authorization": f"Bearer {access}"}
    me = c.get("/auth/me", headers=auth).json()["data"]
    print("user:", me["username"])

    # ۴) کندل‌ها
    r = c.get("/ohlcv/1", params={"timeframe": "1d", "limit": 5}, headers=auth)
    data = r.json()["data"]
    print(f"candles: {data['count']}/{data['total']}")

    # ۵) Logout
    c.post("/auth/logout", json={"refresh_token": refresh}, headers=auth)
```

### ۶.۳ — Swagger UI

🟧 **tab «3 frontend»** (مرورگر)

1. سرور را اجرا کنید: `uvicorn main:app --reload`
2. مرورگر باز شود: `http://localhost:8000/docs`
3. روی **Authorize** (آیکون قفل) کلیک کنید
4. فقط `username` و `password` بدهید — Swagger توکن را در همه درخواست‌ها خودکار اضافه می‌کند
5. هر endpoint را `Try it out` کنید

---

## ۷. عیب‌یابی

### مشکل ۱: `405 Method Not Allowed` در `/auth/login`

**علت:** ارسال JSON به جای form data.

**راه‌حل:** Content-Type باید `application/x-www-form-urlencoded` باشد:

🟩 **tab «2 scripts»**
```python
# ❌ اشتباه:
c.post("/auth/login", json={"username": "...", "password": "..."})

# ✅ صحیح:
c.post("/auth/login", data={"username": "...", "password": "..."})
```

### مشکل ۲: `401 Unauthorized` پس از مدتی

**علت:** access_token منقضی شده (پیش‌فرض ۳۰ دقیقه).

**راه‌حل:** `POST /auth/refresh` با refresh_token.

### مشکل ۳: `422 Unprocessable Entity` در `/ohlcv/{id}`

**علت‌های احتمالی:**
- `timeframe` ارسال نشده
- `limit > 1000` یا `limit < 1`
- `from_ts` با فرمت ISO 8601 صحیح نیست

**نمونه ISO 8601 معتبر:** `2024-01-01T00:00:00Z` یا `2024-01-01T00:00:00+00:00`

### مشکل ۴: `404 Not Found` در `/ohlcv/{id}`

**علت:** `symbol_id` در جدول `symbols` وجود ندارد.

**راه‌حل:**

🟦 **tab «1 backend»**
```cmd
sqlite3 backend\trading.db "SELECT id, symbol FROM symbols LIMIT 10;"
```

### مشکل ۵: CORS error در frontend (مرورگر)

**علت:** آدرس frontend در `CORS_ORIGINS` در `.env` تعریف نشده.

**راه‌حل:** `.env` در ریشه backend:
```env
CORS_ORIGINS=["http://localhost:5173","http://localhost:5174"]
```

سپس restart سرور.

---

## ۸. تست با ابزارهای مختلف

| ابزار | کاربرد |
|---|---|
| **Swagger UI** (`/docs`) | کشف و تست تعاملی — برای exploration |
| **httpx (Python)** | اتمیشن، تست end-to-end (پیشنهاد قانون #۱۹) |
| **curl** | تست سریع یک endpoint از terminal |
| **Postman / Insomnia** | برای کاربرانی که UI گرافیکی می‌خواهند |
| **pytest + httpx.AsyncClient** | تست خودکار در CI/CD (فاز ۱+) |

> 🔒 **قانون #۱۹ (v2.5):** برای automation تست API، **اولویت با اسکریپت Python (httpx) است** — نه Swagger UI. علت: تکرارپذیری، لاگ قابل ذخیره، یکپارچگی با pytest.

---

## ۹. ارجاعات

- **سند جامع v2.8** بخش ۶ — مرجع کامل قراردادهای API
- **سند جامع v2.8** بند ۶.۲ — ساختار استاندارد پاسخ
- **سند جامع v2.8** بند ۶.۶ — Auth endpoints
- **سند جامع v2.8** بند ۶.۸ — OHLCV endpoints
- **GIT_WORKFLOW.md** — رویه commit پس از تغییر endpoint
- **CLAUDE_CHECKLIST.md** — قانون #۱۹ (تست با httpx)

---

## 📌 پایان API_DOCS

**نسخه:** v1.0 (2026-05-18 — چت ۷ / T2.09)
**ساختار:** ۸ بخش + ۷ endpoint detail
**API Version:** v0.2.0
