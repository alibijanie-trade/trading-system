# 🔧 TROUBLESHOOTING — راهنمای رفع مشکلات

> **هدف یک‌خطی:** فهرست قابل جستجوی همه Bug های شناسایی‌شده در پروژه، علائم، علت، راه‌حل، و نحوه جلوگیری.

> **محل قرارگیری:** `docs/TROUBLESHOOTING.md`  
> **به‌روز توسط:** Claude هرگاه Bug جدید شناسایی/رفع شد (CLAUDE_CHECKLIST فاز ۳ مرحله ۵)  
> **نسخه:** v1.0 (2026-05-17)

---

## 📑 فهرست

- [راهنمای استفاده](#راهنمای-استفاده)
- [دسته‌بندی Bug ها](#دستهبندی-bug-ها)
- [Bug Catalog (به ترتیب شماره)](#bug-catalog-به-ترتیب-شماره)
- [FAQ — سؤالات متداول](#faq--سؤالات-متداول)
- [مشکلات محیطی پرتکرار](#مشکلات-محیطی-پرتکرار)

---

## راهنمای استفاده

### قالب هر Bug

```markdown
## Bug #N — {عنوان کوتاه}

**ثبت‌شده در:** چت {نام چت}  
**تاریخ:** YYYY-MM-DD  
**دسته:** [Frontend / Backend / Script / Environment / Docs]  
**شدت:** [Critical / High / Medium / Low]

### علائم
- چه چیز دیده می‌شد؟

### علت ریشه‌ای
- چرا اتفاق افتاد؟

### راه‌حل
- چه شد رفعش؟ (با کد یا اسکریپت)

### پیشگیری در آینده
- چگونه از تکرار جلوگیری کنیم؟

### اسکریپت رفع
- `scripts/{N}b_fix_xxx.py` یا `xxx`
```

### نحوه جستجو

سند بزرگ است. برای پیدا کردن سریع:
- جستجوی Ctrl+F با کلمه کلیدی مشکل (`emoji`, `cors`, `theme`, `path`, …)
- یا جستجوی شماره Bug اگر می‌دانید (`#43`, `#48`, …)

---

## دسته‌بندی Bug ها

| دسته | تعداد | شدت متوسط |
|---|---|---|
| Environment (Windows specific) | ~۸ | High |
| Frontend (Theme/Style) | ~۱۰ | Medium |
| Frontend (Logic) | ~۵ | High |
| Backend (Auth) | ~۳ | Critical |
| Backend (DB/Models) | ~۴ | High |
| Scripts (idempotency) | ~۳ | Medium |
| Docs (consistency) | ~۲ | Low |

> توجه: شماره Bug ها 1 تا 49 ثبت شده. Bug های 1-42 از چت‌های قبلی هستند که با جزئیات کمتر اینجا ذکر می‌شوند، Bug های 43+ با جزئیات کامل.

---

## Bug Catalog (به ترتیب شماره)

### Bug #1 تا #15 — مشکلات setup اولیه و Windows

این Bug ها در چت‌های ۱ و ۲ شناسایی و رفع شدند. عمدتاً:
- مسیرها در Windows (backslash vs forward slash) → استفاده از `pathlib.Path`
- encoding UTF-8 → `# -*- coding: utf-8 -*-` در همه فایل‌های Python
- venv activation در PowerShell → `venv\Scripts\Activate.ps1`
- emoji و ANSI color در Windows CMD → fix در Logger setup

### Bug #16 تا #25 — مشکلات Database و Auth

- passlib در Windows مشکل داشت → **bcrypt مستقیم**
- async SQLAlchemy session management → استفاده از `async with`
- timezone در timestamp → ذخیره به UTC، نمایش local
- CORS برای localhost:5173 → اضافه به middleware

### Bug #26 تا #35 — مشکلات API و Frontend اولیه

- اولین endpoint OHLCV بدون pagination → اضافه `limit` parameter
- axios interceptor برای JWT → افزودن `Authorization: Bearer`
- lightweight-charts timestamp Unix vs ISO → `isoToUnix()` helper
- LoginPage routing بدون ProtectedRoute → اضافه ProtectedRoute

### Bug #36 تا #42 — مشکلات اولین تجربه نمودار

- نمودار نقاشی نمی‌شد چون container size 0 بود → `chartContainerRef.current.clientWidth`
- crash هنگام unmount نمودار → cleanup در useEffect return
- multiple charts overlap → `chartRef.current?.remove()` قبل از create جدید
- داده‌های null → فیلتر کردن قبل از setData

---

### Bug #43 — Binance Color Accuracy ⭐

**ثبت‌شده در:** چت ۵ (theme-engine)  
**تاریخ:** 2026-05-17 (صبح)  
**دسته:** Frontend (Theme)  
**شدت:** Medium

#### علائم
رنگ‌های تم `binance-dark` با نسخه واقعی بایننس مطابقت نداشت — کاربر سایت بایننس را باز کرد و تفاوت را دید.

#### علت ریشه‌ای
رنگ‌های فرضی استفاده شده بود (`#26a69a` و `#ef5350` که default lightweight-charts است) به جای رنگ‌های واقعی بایننس.

#### راه‌حل
استخراج رنگ‌های دقیق از سایت بایننس:
- `--color-primary: #F0B90B` (Binance yellow)
- `--color-bg: #181A20`
- `--color-card: #1E2329`
- `--color-success: #0ECB81`
- `--color-danger: #F6465D`
- ...

#### پیشگیری در آینده
وقتی به یک سرویس reference می‌دهیم (مثل "تم بایننس")، رنگ‌ها را با ابزار color picker از سایت اصلی استخراج کنیم.

#### اسکریپت رفع
`scripts/27c_fix_binance_colors.py`

---

### Bug #44 — Interactive States Missing ⭐

**ثبت‌شده در:** چت ۵  
**تاریخ:** 2026-05-17  
**دسته:** Frontend (UX)  
**شدت:** Medium

#### علائم
دکمه‌ها و input ها هیچ feedback بصری نداشتند — hover/focus/active نامرئی بودند. حس "سایت سنگاپوری بدون جان".

#### علت ریشه‌ای
در ابتدای Theme Engine، فقط رنگ‌های پایه ست شده بود. State های تعاملی نادیده گرفته شدند.

#### راه‌حل
افزودن به `index.css`:
```css
button:hover:not(:disabled) { filter: brightness(1.12); }
button:active:not(:disabled) { transform: translateY(1px); filter: brightness(0.95); }
button:focus-visible { outline: 2px solid var(--color-primary); outline-offset: 2px; }
button:disabled { cursor: not-allowed; opacity: 0.5; filter: none; }
```
+ select hover/focus + input focus + `[data-card-link="true"]:hover`.

#### پیشگیری در آینده
سند جامع بخش **۸.۷.۱ — Interactive States Spec** اضافه شد. الزامی برای همه کامپوننت‌های تعاملی.

#### اسکریپت رفع
`scripts/27e_fix_interactive_states.py`

---

### Bug #45 — Toast Theme Inconsistency ⭐

**ثبت‌شده در:** چت ۵  
**تاریخ:** 2026-05-17  
**دسته:** Frontend (Design)  
**شدت:** High (الگوی بنیادی)

#### علائم
Toast های با variant سبز/قرمز کاملاً سبز/قرمز پررنگ بودند — با تم تیره خوب می‌شدند ولی با تم light میل به clash بود.

#### علت ریشه‌ای
کانتینر Toast با رنگ variant پر می‌شد (`background: success`)، که هویت "کارت بایننس" را گم می‌کرد.

#### راه‌حل
معرفی **Variant Indicator Pattern**:
- کانتینر همیشه از `--color-card` + `--color-border`
- نوع فقط با accent باریک ۳-۴px (در سمت start برای RTL) + icon رنگی
- متن همیشه از `--color-text`

این الگو در سند جامع بخش **۸.۸.۱** ثبت شد و **در تمام variant های آینده** الزامی شد.

#### پیشگیری در آینده
هر کامپوننت typed (Dialog، Alert، Badge، …) باید این الگو را رعایت کند. در `STYLE_GUIDE.md` ثبت شد.

#### اسکریپت رفع
`scripts/28c_fix_toast_theme.py`

---

### Bug #46 — ESM URL Scheme در ویندوز ⭐

**ثبت‌شده در:** چت ۶  
**تاریخ:** 2026-05-17  
**دسته:** Script (Python + Node interop)  
**شدت:** Low (در runtime test، نه production code)

#### علائم
اسکریپت `31b_test_numeric_calendar.py` در ویندوز خطا داد:
```
Error [ERR_UNSUPPORTED_ESM_URL_SCHEME]: Only URLs with a scheme in: file, data, and node
```

#### علت ریشه‌ای
کد Python از `Path.as_posix()` استفاده می‌کرد که در ویندوز خروجی `D:/Projects/...` می‌دهد. این string وقتی به import dynamic در Node.js پاس می‌شود، scheme نامعتبر تشخیص داده می‌شود.

#### راه‌حل
استفاده از `Path.as_uri()` که خروجی portable می‌دهد:
- ویندوز: `file:///D:/Projects/...`
- Linux/Mac: `file:///home/user/...`

هر دو معتبر برای ESM import.

#### پیشگیری در آینده
**قانون:** برای ESM import dynamic در Node از Python، همیشه `Path.as_uri()` استفاده شود، نه `as_posix()`.

#### اسکریپت رفع
اصلاح `31b_test_numeric_calendar.py` (یک خط تغییر).

---

### Bug #47 — Font Size Scaling شکسته ⭐

**ثبت‌شده در:** چت ۶  
**تاریخ:** 2026-05-17  
**دسته:** Frontend (Theme + CSS)  
**شدت:** High (feature شکسته بود)

#### علائم
در `/settings`، انتخاب اندازه فونت "بزرگ" یا "خیلی بزرگ" کار می‌کرد ولی **فقط روی متن preview** اعمال می‌شد. سایر متن‌ها در صفحه (header، دکمه‌ها، …) ثابت بودند.

#### علت ریشه‌ای
دو مشکل ترکیب شدند:
1. در `index.css`، body با `font-size: var(--font-size-base)` ست بود، ولی `html` نه.
2. در همه فایل‌های `.jsx`، inline style ها از مقادیر **px ثابت** استفاده می‌کردند:
   ```jsx
   <h1 style={{ fontSize: 22 }}>  // ❌ ۲۲px ثابت
   ```
   این px ها body را override می‌کردند. تغییر `--font-size-base` بی‌اثر بود.

#### راه‌حل
دو بخش:
1. در `index.css`:
   ```css
   html { font-size: var(--font-size-base); }
   body { font-size: 1rem; }
   ```
2. در ۹ فایل `.jsx`، تبدیل همه `fontSize: <N>` به `fontSize: '<X.XX>rem'`:
   ```jsx
   // ❌ قبل
   <h1 style={{ fontSize: 22 }}>
   
   // ✅ بعد (با baseline = 14px)
   <h1 style={{ fontSize: "1.57rem" }}>  // 22/14 = 1.57
   ```

جدول تبدیل در اسکریپت `32_phase0_polish.py` با regex خودکار شد.

#### پیشگیری در آینده
**Anti-Pattern A9 (در PROJECT_GOVERNANCE):** هرگز `fontSize` به‌صورت inline px ثابت — همیشه rem.  
**در STYLE_GUIDE.md:** قانون "rem نه px" برای font sizes.  
**در ESLint (آینده، Tier 3):** قانون custom برای detect خودکار.

#### اسکریپت رفع
`scripts/32_phase0_polish.py` (بخش regex transform)

---

### Bug #48 — Tooltip تاریخ نمودار نمایش داده نمی‌شد ⭐

**ثبت‌شده در:** چت ۶  
**تاریخ:** 2026-05-17  
**دسته:** Frontend (3rd-party library API)  
**شدت:** Medium

#### علائم
در `/chart/1`، hover روی شمعی → tooltip شامل قیمت نمایش داده می‌شد ولی **تاریخ نه**. به‌جای آن یک رشته خام یا empty نشان داده می‌شد.

#### علت ریشه‌ای
در lightweight-charts v4.x، property `localization.dateFormat` فقط **string** قبول می‌کند (مثل `'yyyy-MM-dd'`)، نه function. کد ما function پاس داده بود که silently ignore می‌شد.

```jsx
// ❌ قبل — function به dateFormat (نمی‌پذیرد)
localization: {
  dateFormat: (time) => formatDate(...)
}
```

#### راه‌حل
استفاده از `timeFormatter` که برای function طراحی شده:
```jsx
// ✅ بعد
localization: {
  locale: "en-US",
  timeFormatter: (time) => {
    const d = typeof time === "number" ? new Date(time * 1000) : new Date(time);
    return formatDate(d, calendar, { format: gregorianFormat });
  },
  priceFormatter: (price) => formatNumber(price, { maxDecimals: 2 }),
}
```

#### پیشگیری در آینده
**هنگام استفاده از library 3rd-party:** همیشه docs نسخه فعلی را چک کنیم. type signature را اعتبار سنجی کنیم.  
**در آینده با TypeScript (Tier 3):** خود TS این را در زمان compile catch می‌کرد.

#### اسکریپت رفع
`scripts/32_phase0_polish.py` (در محتوای کامل ChartPage.jsx)

---

### Bug #49 — `1714 کندل` در HomePage بدون جداکننده ⭐

**ثبت‌شده در:** چت ۶  
**تاریخ:** 2026-05-17  
**دسته:** Frontend (UI inconsistency)  
**شدت:** Low

#### علائم
در `/`، badge کنار لینک "BTC/USDT — روزانه" عدد `1714 کندل` را بدون کاما نشان می‌داد. ولی در `/chart/1`، متادیتا `1,714 از 1,714 کندل` با کاما بود.

#### علت ریشه‌ای
عدد `1714` به‌صورت **hardcoded string** در JSX نوشته شده بود:
```jsx
<span>1714 کندل</span>  // ❌
```

از `formatNumber` که در زیرگام ۸.۵ ساخته شد، استفاده نمی‌کرد.

#### راه‌حل
```jsx
<span>{formatNumber(1714)} کندل</span>  // ✅
```

+ import formatNumber در HomePage.

> ⚠️ **توجه آینده:** عدد `1714` خودش hardcoded است. در فاز ۲+، باید از API دریافت شود (`GET /symbols/1` که count را برگرداند). در فاز ۰ به‌صورت placeholder قبول است.

#### پیشگیری در آینده
**در STYLE_GUIDE.md:** هر عدد قابل نمایش به کاربر باید از `formatNumber` بگذرد.  
**در ESLint (آینده):** detect عدد بدون formatNumber در JSX (سخت ولی ممکن).

#### اسکریپت رفع
`scripts/32_phase0_polish.py` (بخش HomePage.jsx)

---

### Bug #52 — pre-commit `end-of-file-fixer` با نام فایل فارسی روی Windows کرش می‌کند ⭐

**ثبت‌شده در:** چت ۸ (در PENDING/D1.1) → چت ۹ (به‌صورت رسمی در سند جامع v2.11)  
**تاریخ:** 2026-05-19  
**دسته:** Environment (Windows + Python encoding + third-party tool)  
**شدت:** Medium (workaround در دسترس، کار اصلی hook انجام می‌شود)

#### علائم

اولین commit پس از ادغام v2.10:
```
fix end of files.........................................................Failed
- hook id: end-of-file-fixer
- exit code: 1
- files were modified by this hook
UnicodeEncodeError: 'charmap' codec can't encode characters in position 12-14
File "...\pre_commit_hooks\end_of_file_fixer.py", line 64, in main
    print(f'Fixing {filename}')
  File "C:\Program Files\Python311\Lib\encodings\cp1252.py"
```

نکته مهم: **کار اصلی hook (افزودن newline) انجام شد** — فقط `print(f'Fixing {filename}')` کرش کرد چون نمی‌تواند نام فارسی را در cp1252 encode کند.

#### علت ریشه‌ای

ترکیب چند عامل:
1. PowerShell ویندوز default encoding = `cp1252`
2. نام فایل `سند_جامع_v2_10.md` شامل حروف فارسی (Unicode) است
3. پکیج `pre-commit-hooks` (نسخه فعلی) از `print(f'Fixing {filename}')` بدون handling برای non-ASCII filenames استفاده می‌کند
4. Python `print()` تلاش می‌کند خروجی را با encoding default کنسول encode کند → کرش

مشابه قانون #۴۶ است ولی در کد third-party (نه کد ما) — پس قانون #۴۶ به تنهایی نمی‌توانست جلوگیری کند.

#### راه‌حل (Workaround موقت — استفاده شد در چت ۸)

```powershell
$env:PYTHONIOENCODING = "utf-8"
git add docs/ claude_workspace/
git commit -m "..."
```

این env var به Python می‌گوید stdout را UTF-8 encode کند، پس print با کاراکترهای فارسی کرش نمی‌کند. کار اصلی hook (افزودن newline) از قبل موفق بوده — فقط چاپ پیام موفقیت بود که کرش می‌کرد.

#### راه‌حل دائمی (پیشنهاد برای آینده)

**گزینه A — متغیر محیطی دائمی Windows (پیشنهاد مطلوب):**
```powershell
[Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User")
```
یک‌بار اجرا، در همه session های آینده فعال. بعد از اجرا، PowerShell را ببندید و دوباره باز کنید تا env var جدید load شود.

**گزینه B — افزودن به shell profile (`$PROFILE`):**
```powershell
# در $PROFILE اضافه شود:
$env:PYTHONIOENCODING = "utf-8"
```

**گزینه C — مستندسازی در ONBOARDING:** اضافه به `ONBOARDING_GUIDE.md` که `PYTHONIOENCODING=utf-8` در Windows env vars لازم است (در بخش setup اولیه).

#### پیشگیری در آینده

- **در `ONBOARDING_GUIDE.md`:** قرار دادن `PYTHONIOENCODING=utf-8` به‌عنوان مرحله اجباری Windows setup
- **در `PRECOMMIT.md`:** هشدار برای پروژه‌هایی با فایل‌های non-ASCII در Windows
- **در `00b_post_unzip_setup.py`:** اضافه کردن check برای `PYTHONIOENCODING` و در صورت عدم تنظیم، نمایش هشدار به کاربر
- **درس عمومی:** پکیج‌های Python third-party ممکن است در پروژه‌های با نام فایل non-ASCII روی Windows کرش کنند. تست با فایل‌های فارسی هنگام افزودن tool جدید الزامی است.

#### اسکریپت رفع

اسکریپت کد ندارد — این یک env var setup در سیستم کاربر است، نه bug در کد ما.

---

## FAQ — سؤالات متداول

### Q1: چرا اسکریپت‌ها idempotent هستند؟
چون ممکن است یک اسکریپت چندبار اجرا شود (مثلاً بعد از خطا، یا برای تست). اگر دفعه دوم خطا دهد یا state را خراب کند، debugging سخت می‌شود.

### Q2: چرا قانون #۲۲ مجبور به اسکریپت تست همراه است؟
چون کاربر باید سریع تأیید کند که اسکریپت اصلی درست کار کرده، بدون اینکه manual چک کند. تست خودکار = تضمین کیفیت قبل از تحویل.

### Q3: چرا تم بایننس به این دقت رنگ‌بندی شده؟
چون این پروژه برای کاربری است که سال‌ها با بایننس کار کرده. حس آشنایی مهم است.

### Q4: چرا preferencesStore جدا از themeStore؟
چون نگرانی (concerns) متفاوت‌اند: theme = ظاهر، preferences = behavior. اگر یک store بزرگ بسازیم، refactoring آینده سخت‌تر می‌شود. (Decision #50)

### Q5: چرا Variant Indicator Pattern؟
چون اگر کانتینر کامل با رنگ variant پر شود:
- در تم light: ممکن است contrast کافی نباشد
- در تم dark: هویت "کارت" گم می‌شود  
- یکپارچگی بصری از بین می‌رود

الگوی accent باریک حداکثر اطلاعات با حداقل آلودگی بصری می‌دهد.

### Q6: چرا کار با Swagger UI ممنوع است (قانون #۲۱)؟
چون:
- Swagger UI manual است (slow + خطا)
- خروجی قابل اشتراک نیست (نه لاگ، نه CI)
- در محیط headless کار نمی‌کند
اسکریپت httpx این مشکلات را ندارد.

### Q7: چرا فاز ۰ این‌قدر طول کشید؟
چون اسکلت محکم اولویت داشت. در پروژه‌های آینده با `REUSABLE_SKELETON.md`، این کار در ساعت‌ها انجام می‌شود نه روزها.

### Q8: اگر Claude اشتباهی کرد چه کنم؟
کلمه‌های Trigger در `CLAUDE_CHECKLIST.md` موجود:
- "Governance" → یادآوری اصول
- "چک‌لیست" → گزارش وضعیت
- "E1: کیفیت" → پایان چت فوری

### Q9: اگر می‌خواهم تم جدید اضافه کنم؟
فایل `frontend/src/themes/themes.js` را باز کنید، یک object جدید با id منحصربه‌فرد بسازید، همه CSS variables لازم را پر کنید. خودکار در SettingsPage ظاهر می‌شود (چون از `listThemes()` می‌خواند).

### Q10: اگر می‌خواهم Bug جدید گزارش کنم؟
به Claude بگویید، او اسکریپت fix را می‌سازد و در این سند ثبت می‌کند. شماره Bug پیوسته (#50, #51, ...).

---

## مشکلات محیطی پرتکرار

### M1 — venv فعال نیست
**علامت:** `python` به Python global اشاره می‌کند نه venv.  
**راه‌حل:** 
```cmd
cd D:\Projects\trading-system
venv\Scripts\activate
```
سپس prompt با `(venv)` شروع می‌شود.

### M2 — Frontend نصب نشده / خطای import
**علامت:** `Cannot find module 'react'` یا مشابه.  
**راه‌حل:**
```cmd
cd frontend
npm install
```

### M3 — Backend پاسخ نمی‌دهد
**علامت:** Frontend خطای `ERR_NETWORK`.  
**چک:**
1. آیا 🟦 tab «1 backend» فعال است؟
2. آیا `uvicorn app.main:app --reload` در حال اجرا است؟
3. آیا port 8000 توسط process دیگری گرفته نشده؟ → `netstat -ano | findstr :8000`

### M4 — DB خالی است / login کار نمی‌کند
**علامت:** Login با `admin/1` → خطای 401.  
**راه‌حل:**
```cmd
python scripts/00b_post_unzip_setup.py
```
این اسکریپت DB را seed می‌کند.

### M5 — تم تغییر نمی‌کند
**علامت:** انتخاب تم در `/settings` اثر ندارد.  
**چک:**
1. Console مرورگر: خطایی هست؟
2. localStorage: کلید `theme-storage` موجود است؟
3. در DevTools → Inspect element → `:root`: آیا CSS variables تغییر می‌کنند؟

### M6 — npm install در ایران شکست می‌خورد
**علامت:** `403 Forbidden` یا `ECONNRESET`.  
**راه‌حل:** اسکریپت `00b_post_unzip_setup.py` خودکار به mirrors ایران سوییچ می‌کند:
```
npm registry: https://registry.npmmirror.com
pip index: https://mirror-pypi.runflare.com/simple/
```

### M7 — npm build خطای lightningcss
**علامت:** `Cannot find module 'lightningcss-win32-x64-msvc'`.  
**راه‌حل:** نصب اضافه:
```cmd
npm install --save-dev lightningcss-win32-x64-msvc
```
این binary platform-specific است که گاهی auto-install نمی‌شود.

---

## 📌 پایان TROUBLESHOOTING

**نسخه:** v1.1 (2026-05-20 — چت ۹: افزودن Bug #52 — pre-commit + فارسی Windows)  
**Bug های ثبت‌شده با جزئیات:** ۸ (#43-#49، #52)  
**Bug های خلاصه:** ۴۲ (#1-#42)  
**Bug های دیگر در PENDING:** #50 (React import cleanup — E2.1)، #51 (python -c escape — لاگ‌شده در درس M)  
**FAQ:** ۱۰  
**مشکلات محیطی:** ۷
