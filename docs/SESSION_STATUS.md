# وضعیت پروژه — 2026-05-16 (پایان چت ۳: زیرگام‌های ۵، ۷.۱، ۷.۲، ۷.۳ + ابزار پاک‌سازی)

## فاز جاری

**فاز ۰ — زیرساخت — حدود ۹۵٪ پیشرفت** — فقط زیرگام ۸ (Theme Engine + UX پیشرفته) باقی است.

## نوع این چت

**🔧 چت اجرایی + اسناد + ابزار** — پیشرفت چشمگیر:
- زیرگام ۵ (Auth + JWT) کامل
- زیرگام ۷ کامل (۷.۱ + ۷.۲ + ۷.۳)
- ۹ تصمیم جدید + ۲ Bug Fix
- ۳ قانون رفتاری جدید (#17 توسعه‌یافته + #19 جدید + **#20 جدید**)
- ابزار `00_cleanup_for_zip.py` برای پاک‌سازی خودکار پوشه

## گام‌های انجام‌شده در این چت

- ✅ **Endpoint GET /ohlcv/{symbol_id}** — اولین endpoint کامل (`20_ohlcv_api.py`, `21_test_api.py`)
- ✅ **زیرگام ۵ — Auth + JWT** (۱۴ فایل): `22_auth_jwt.py`, `22b_fix_env_app_version.py`, `22c_fix_bcrypt.py`, `23_test_auth.py`
- ✅ **زیرگام ۷.۱ — Frontend scaffold**: Vite + React + Zustand + Router + axios + lightweight-charts (`24_frontend_scaffold.py`)
- ✅ **زیرگام ۷.۲ — Login واقعی** (`25_login_page.py`)
- ✅ **زیرگام ۷.۳ — نمودار کندل** با candlestick + volume (`26_chart_page.py`)
- ✅ **🆕 ابزار `00_cleanup_for_zip.py`** — پاک‌سازی خودکار پوشه قبل از zip

## وضعیت تست‌شده

- ✅ `alembic current` → `08348dca2b9a (head)`
- ✅ uvicorn روی `http://127.0.0.1:8000` با نسخه `v0.2.0`
- ✅ Vite dev server روی `http://localhost:5173/`
- ✅ تمام ۶ تست API + ۷ تست Auth در ترمینال
- ✅ Frontend: login admin/1 → /home → /chart/1 → نمودار ۱۰۰۰ کندل BTC/USDT
- ✅ Interaction نمودار: درگ، اسکرول zoom، crosshair با قیمت/حجم

## تصمیمات گرفته‌شده در این چت (Session 5)

40. **حذف passlib، استفاده مستقیم از bcrypt 4.1.3** — `passlib 1.7.4` در `detect_wrap_bug` یک رشته >۷۲ بایت می‌فرستد که bcrypt 4.x reject می‌کند.
41. **bump نسخه v0.1.3 → v0.2.0** — Auth = MINOR feature طبق SemVer.
42. **Frontend stack نهایی** — Vite 8.0.13 + React 18 + Zustand 4.5.2 + Router 6.23.1 + axios 1.7.2 + lightweight-charts 4.1.7
43. **JWT در localStorage با Zustand persist** — فاز ۰ ساده‌تر، فاز ۵+ مهاجرت به HttpOnly Cookie.
44. **OAuth2PasswordRequestForm + python-multipart** — استاندارد FastAPI با `application/x-www-form-urlencoded`.
45. **JWT deterministic — پذیرفته‌شده** — افزودن `jti` به access هم در فاز ۵+ آینده‌نگرانه.
46. **python-multipart==0.0.9** اضافه به requirements.
47. **bcrypt==4.1.3** تثبیت در requirements (جایگزین passlib).
48. **🆕 اسکریپت `00_cleanup_for_zip.py` + قانون #20** — پاک‌سازی خودکار پوشه. Claude در پایان هر چت دستور اجرای آن را می‌دهد.

## Bug Fixes این چت

38. **APP_VERSION در .env بر default غلبه می‌کرد** → اصلاح با `22b_fix_env_app_version.py`
39. **passlib + bcrypt 4.x → ValueError در login** → اصلاح با `22c_fix_bcrypt.py` (تصمیم #40)

## قوانین رفتاری جدید Claude

- **#17 (توسعه‌یافته):** نام tab با ایموجی رنگی متمایز — 🟦 backend / 🟩 scripts / 🟧 frontend
- **#19 (جدید):** تست endpoint از ترمینال (httpx) — اولویت بر Swagger UI
- **#20 (جدید):** تولید خودکار دستورات پاک‌سازی — Claude در هر پروتکل تعویض چت دستور `00_cleanup_for_zip.py` را می‌دهد

## تصمیمات معلق برای چت بعدی

- (هیچ مورد معلقی نیست)

## خطاهای حل‌نشده

- (هیچ‌کدام)

## مسائل شناخته‌شده (Non-blocking)

- پیام‌های اولیه uvicorn هنوز ANSI خام دارند (قبل از colorama init)
- لاگ‌های sqlalchemy.engine verbose هستند چون `echo=settings.IS_DEVELOPMENT`
- JWT deterministic در همان ثانیه — قابل قبول
- 4 high severity vulnerabilities در npm — همگی dev dependencies. در deploy رسیدگی می‌شود.

## فایل‌های تولیدشده در این چت

### اسکریپت‌های Python (همه در `D:\Projects\trading-system\scripts\`):
- `00_cleanup_for_zip.py` 🆕 — **ابزار پاک‌سازی خودکار پوشه قبل از zip**
- `20_ohlcv_api.py` — اولین endpoint API
- `21_test_api.py` — ۶ تست API از ترمینال
- `22_auth_jwt.py` — Auth کامل (۱۴ فایل embedded)
- `22b_fix_env_app_version.py` — رفع bug `APP_VERSION` در .env
- `22c_fix_bcrypt.py` — حذف passlib، bcrypt مستقیم
- `23_test_auth.py` — ۷ تست Auth
- `24_frontend_scaffold.py` — ساختار اولیه Frontend (۱۰ فایل)
- `25_login_page.py` — Login واقعی + HomePage
- `26_chart_page.py` — نمودار کندل

### اسناد:
- `سند_جامع_v2.5.md` (نسخه lite — ~92KB، با حذف بخش‌های قدیمی/نظری)
- `SESSION_STATUS.md` (همین فایل)
- `PROJECT_CONTEXT.md`

## برای شروع چت جدید

کاربر باید ۴ مورد را پیوست کند:

1. `سند_جامع_v2.5.md`
2. `SESSION_STATUS.md` (همین فایل)
3. `PROJECT_CONTEXT.md`
4. `trading-system.zip` (پاک‌شده با اسکریپت `00_cleanup_for_zip.py`)

🔒 Claude در شروع چت جدید طبق قانون #20 / سند ۱۴.۵ عمل می‌کند: اگر zip حاوی فایل‌های اضافی است، یادآوری اجرای `00_cleanup_for_zip.py` را می‌دهد.

## گام بعدی — انتخاب با کاربر

دو گزینه پیش رو:
- **الف)** زیرگام ۸ — Theme Engine + Toast + Skeleton + RTL کامل (تکمیل فاز ۰ به ۱۰۰٪)
- **ب)** پرش به فاز ۱ — داده بازار (CCXT + WebSocket + ticks live + timeframes متعدد)

## نسخه پروژه

- **کد Backend:** v0.2.0 (Auth + bcrypt مستقیم)
- **کد Frontend:** v0.0.0 (Vite scaffold)
- **اسناد:** v2.5
- **DB Migration head:** `08348dca2b9a` (add_row_index_to_ohlcv)
- **OhlcvData:** 1714 رکورد (BTC/USDT روزانه)

## پیشرفت کلی

- فاز ۰: ~۹۵٪ (۱۲ از ۱۳ زیرگام کامل)
- فاز ۱-۸: ۰٪ (شروع نشده)
- **پیشرفت کلی پروژه: ~۱۱٪**
