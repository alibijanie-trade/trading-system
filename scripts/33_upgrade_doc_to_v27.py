# -*- coding: utf-8 -*-
"""
اسکریپت ۳۳ — ارتقای سند جامع v2.6 → v2.7
================================================================
این اسکریپت سند جامع را به نسخه v2.7 ارتقا می‌دهد، با اصول:
  - No-Deletion (قانون #۲۴): هیچ بخشی حذف نمی‌شود
  - Atomic (قانون #۲۶): تغییرات با هم اعمال می‌شوند
  - Change Log اجباری: بخش "تغییرات v2.7" در ابتدا

محتوای v2.7:
  ۱) بخش "تغییرات v2.6 → v2.7" در ابتدا
  ۲) اصلاحیه بخش ۱۳.۶: phase{NN} → phase{N}
  ۳) بخش ۸.۸.۲ جدید: انتخاب فرمت تاریخ میلادی
  ۴) Bug history گسترش: Bug #46-#49
  ۵) قوانین جدید: #۲۳, #۲۴, #۲۵, #۲۶
  ۶) سند ۱۶ جدید: مدیریت دانش و حافظه پروژه
  ۷) سند ۱۷ جدید: Templates پاسخ Claude
  ۸) به‌روزرسانی بخش ۱۵: فاز ۰ → ۱۰۰٪

استراتژی:
  - خواندن سند v2.6
  - اعمال تغییرات با pattern match
  - نوشتن v2.7 در docs/
================================================================
"""
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DOCS_DIR = PROJECT_ROOT / "docs"

SOURCE = DOCS_DIR / "سند_جامع_v2_6.md"
TARGET = DOCS_DIR / "سند_جامع_v2_7.md"


# ============================================================
# تغییر ۱ — بخش جدید تغییرات v2.7 (در ابتدای فهرست تغییرات)
# ============================================================

CHANGES_V27 = """# 📋 خلاصه تغییرات v2.6 → v2.7

این نسخه شامل **۴ تصمیم معماری جدید** + **۴ Bug Fix** + **۴ قانون رفتاری جدید** + **۲ بخش جدید سند** + **۱۰ سند جانبی جدید** است.

این نسخه یک **نقطه عطف** در پروژه است: علاوه بر تکمیل فاز ۰، **زیرساخت Governance** ساخته شد که حافظه و کیفیت پروژه را برای چت‌های آینده و handoff به برنامه‌نویس بعدی تضمین می‌کند.

## دستاوردهای فنی Session 6 (این چت)

- زیرگام ۸.۳: SkeletonBlock + ConfirmDialog با Variant Indicator Pattern
- زیرگام ۸.۴: SettingsPage با ۳ بخش (ThemeCard preview + FontSizeControl + Reset)
- زیرگام ۸.۵: Numeric separator (Intl.NumberFormat) + Persian Calendar (Intl.DateTimeFormat fa-IR-u-ca-persian)
- Feature: انتخاب ۴ فرمت تاریخ میلادی (iso / us-short / eu-short / long)
- اسکریپت‌های جدید: 29, 30, 31, 32 (+ تست‌های همراه)
- ۱۰ سند Governance جدید (شرح در سند ۱۶)
- **فاز ۰: ۱۰۰٪ تکمیل**

## تصمیمات معماری Session 6

- **#50:** preferencesStore جدا از themeStore (concerns متفاوت)
- **#52:** `Intl` built-in به جای کتابخانه شمسی (moment-jalaali، dayjs، ...)
- **#53:** rem به جای px برای fontSize های inline (font scaling سراسری)
- **#54:** زیرساخت Governance ۱۲-سندی (تغییر فلسفه از "Claude به یاد می‌آورد" به "اسناد بیرونی هستند")

## Bug Fixes Session 6

- **#46:** ESM URL scheme در ویندوز — Path.as_posix() → Path.as_uri()
- **#47:** Font Size scaling شکسته — همه inline fontSize: N → 'X.XXrem' + html { font-size: var(--font-size-base) }
- **#48:** tooltip تاریخ نمودار نمایش داده نمی‌شد — `localization.dateFormat` (string only) → `timeFormatter` (function)
- **#49:** عدد ۱۷۱۴ کندل در HomePage بدون کاما — استفاده از formatNumber

## قوانین رفتاری جدید Claude (Session 6)

- **#۲۳:** هر چت، CHAT_LOG.md با بخش جدید آپدیت شود (فاز ۳ مرحله ۲ چک‌لیست)
- **#۲۴:** سند جامع فقط افزوده/اصلاح می‌شود — **هرگز حذف نمی‌شود** (No-Deletion principle). منسوخ‌ها با علامت `[منسوخ — vX.Y]` نگه داشته می‌شوند
- **#۲۵:** Claude در شروع چت **چک‌لیست ۸ مرحله** را اجرا کند (به CLAUDE_CHECKLIST.md مراجعه)
- **#۲۶:** تغییر در یک سند، اگر روی سایر اسناد تأثیر دارد، به‌صورت **اتمیک** اعمال شود (تمام اسناد مرتبط در یک نسخه به‌روز)

## بخش‌های جدید این نسخه

- **سند ۸.۸.۲:** انتخاب فرمت تاریخ میلادی (ISO/US/EU/Long)
- **سند ۱۶:** مدیریت دانش و حافظه پروژه ⭐ (بنیادی)
- **سند ۱۷:** Templates پاسخ Claude برای موقعیت‌های رایج
- اصلاحیه سند **۱۳.۶:** قالب نام چت — `phase{N}` تک‌رقم 0-based (نه phase{NN})

## اسناد جانبی جدید (Governance Suite)

این نسخه به همراه ۱۰ سند جانبی جدید در `docs/` تحویل می‌شود:

| سند | نقش |
|---|---|
| PROJECT_GOVERNANCE.md ⭐ | راهبردی — فرایند، نه محتوا |
| CLAUDE_CHECKLIST.md ⭐ | چک‌لیست explicit شروع/پایان چت |
| CHAT_LOG.md ⭐ | تاریخچه هر چت با Template |
| TASK_BACKLOG.md ⭐ | لیست task ها در ۴ Tier |
| DECISIONS_LOG.md ⭐ | ADR — تصمیمات معماری ۵۴ مورد |
| GLOSSARY.md | واژه‌نامه ~۷۰ اصطلاح |
| TROUBLESHOOTING.md | FAQ + Bug solutions |
| STYLE_GUIDE.md | code style + naming + patterns |
| REUSABLE_SKELETON.md | راهنمای استفاده مجدد + استخراج template |
| ONBOARDING_GUIDE.md | روز اول برنامه‌نویس جدید (۴-۶ ساعت) |

> ⚠️ **مهم:** این ۱۰ سند **هم‌رده** با سند جامع هستند و باید **در هر چت جدید پیوست شوند**.

## API endpoints — بدون تغییر از v2.6

## Frontend pages — تکمیل‌شده

- LoginPage ✅
- HomePage ✅ (با آیکن ⚙️ به جای dropdown موقت)
- ChartPage ✅ (با Skeleton + Persian calendar + formatNumber)
- **SettingsPage** ✅ (🆕 v2.7 — ۳ بخش)

---

"""


# ============================================================
# تغییر ۲ — بخش ۸.۸.۲ جدید (انتخاب فرمت میلادی)
# ============================================================

SECTION_8_8_2 = """## ۸.۸.۲  🆕 v2.7 — انتخاب فرمت تاریخ میلادی ⭐

کاربر باید قادر باشد فرمت نمایش تاریخ میلادی را انتخاب کند. ۴ فرمت پشتیبانی می‌شود:

| ID | نمونه | locale |
|---|---|---|
| `iso` | `2024-01-15` | (custom) |
| `us-short` | `01/15/2024` | en-US |
| `eu-short` | `15/01/2024` | en-GB |
| `long` | `January 15, 2024` | en-US dateStyle:long |

**ذخیره‌سازی:**
- در `preferencesStore.gregorianFormat` (persist)
- مقدار پیش‌فرض: `us-short` (تصمیم #۵۰)
- نسخه persist: `v2` (با migration از v1)

**UI:**
- در `SettingsPage` بخش "زبان و تقویم"
- یک `<select>` که فقط هنگام انتخاب تقویم `gregorian` نمایش داده می‌شود
- preview تاریخ امروز + همراه ساعت

**استفاده در ChartPage:**
- در `localization.timeFormatter` نمودار، فرمت انتخابی اعمال می‌شود
- در dep array `useEffect`: `[symbolId, timeframe, themeId, calendar, gregorianFormat]`

**کد مرجع:**
- `frontend/src/utils/dateFormat.js` (تابع formatDate با param `format`)
- `frontend/src/components/settings/CalendarToggle.jsx` (UI)
- `frontend/src/stores/preferencesStore.js` (state)

---

"""


# ============================================================
# تغییر ۳ — اصلاحیه ۱۳.۶ (phase{NN} → phase{N})
# ============================================================

SECTION_13_6_FIX = """## ۱۳.۶  🆕 v2.6 — قالب نام چت (Chat Naming Convention) ⭐

> ⚠️ **اصلاحیه v2.7:** فرمت اصلی `phase{NN}` به `phase{N}` تک‌رقم 0-based تغییر یافت (بر اساس درخواست کاربر در ابتدای Session 6).

### ۱۳.۶.۱  فرمت اجباری (به‌روز v2.7)

```
TRADING-phase{N}-part{NN}-{topic-slug}
```

- `{N}`: تک‌رقم — `phase0`, `phase1`, `phase2`, … (همان شماره فاز سند ۱۲، 0-based)
- `{NN}`: دو رقم — `part01`, `part02`, …
- `{topic-slug}`: kebab-case، بر اساس **موضوعات واقعی** انجام‌شده در چت

### ۱۳.۶.۲  مثال‌های واقعی (به‌روز v2.7)

| چت | نام |
|---|---|
| اولین چت پروژه | `TRADING-phase0-part01-setup` |
| Theme Engine | `TRADING-phase0-part04-theme-engine` |
| Skeleton + ConfirmDialog → گسترش | `TRADING-phase0-part05-ui-polish-and-governance` |
| CCXT + WebSocket | `TRADING-phase1-part01-ccxt-websocket-setup` |
| Indicators پایه | `TRADING-phase2-part01-indicators-foundation` |

> ⚠️ **مثال‌های قدیمی منسوخ** (در v2.6): `phase01-part01-...` ❌ → `phase0-part01-...` ✅

### ۱۳.۶.۳  قوانین انتخاب topic-slug

- ۲ تا ۴ کلمه
- kebab-case (با خط تیره)
- توصیفی نه عمومی
- بر اساس **موضوعات واقعی** انجام‌شده، نه برنامه اولیه

### ۱۳.۶.۴  پیوستگی موضوعات

اگر یک چت موضوعات مرتبط متعدد دارد، نام چت می‌تواند با `and` ترکیب شود:
- `ui-polish-and-governance` ✓
- `auth-and-frontend-scaffold` ✓

### ۱۳.۶.۵  وظیفه Claude (اصلاحیه v2.7)

نام چت **در پایان چت** انتخاب می‌شود (نه ابتدا). در پایان، Claude:
1. موضوعات انجام‌شده را جمع‌بندی می‌کند
2. نام نهایی متناسب با کل کارها پیشنهاد می‌دهد
3. نام پیشنهادی چت بعد را بر اساس Tier فعلی + گام منطقی بعدی می‌دهد

---

"""


# ============================================================
# تغییر ۴ — سند ۱۶ جدید
# ============================================================

SECTION_16 = """# سند ۱۶ — مدیریت دانش و حافظه پروژه ⭐

> 🆕 v2.7 — بنیادی برای تداوم پروژه

این سند **مهم‌ترین تغییر فلسفی** پروژه را توضیح می‌دهد: تغییر از فرض "Claude به یاد می‌آورد" به اصل "حافظه پروژه در اسناد بیرونی است".

## ۱۶.۱  محدودیت Context Claude — شفافیت کامل

**واقعیت:** Claude در هر چت جدید **هیچ خاطره‌ای از چت‌های قبلی ندارد**. هر چت یک نمونه مستقل از Claude است که:
- ❌ چت‌های قبلی این پروژه را **نمی‌بیند**
- ❌ کدی که Claude قبلی نوشت را **مستقیم نمی‌داند**
- ❌ توافقاتی که در چت‌های گذشته شد را **به یاد ندارد**

**تنها چیزی که در شروع چت در اختیار دارد:**
- ✅ سند جامع که کاربر پیوست کرده
- ✅ zip پروژه که کاربر پیوست کرده
- ✅ سایر اسناد در `docs/`

**پیامد:** اگر چیزی در اسناد نیست، **برای Claude بعدی وجود نخواهد داشت**.

## ۱۶.۲  معماری اسناد — ۱۲ سند مرجع

پروژه دارای ۱۲ سند است که هر یک نقش مشخصی دارد:

| سند | نقش | به‌روز توسط |
|---|---|---|
| سند جامع v2.X | Constitution | Claude در پایان چت |
| **PROJECT_GOVERNANCE.md** ⭐ | راهبردی — فرایند | Claude در پایان چت |
| **CLAUDE_CHECKLIST.md** ⭐ | چک‌لیست explicit | Claude در پایان چت |
| **CHAT_LOG.md** ⭐ | تاریخچه چت‌ها | Claude در پایان **هر** چت (قانون #۲۳) |
| **TASK_BACKLOG.md** ⭐ | TODO ها در ۴ Tier | Claude در پایان چت |
| **DECISIONS_LOG.md** | ADR | Claude اگر تصمیم جدید |
| **TROUBLESHOOTING.md** | FAQ + Bug | Claude اگر Bug جدید |
| **GLOSSARY.md** | واژه‌نامه | Claude به‌مرور |
| **STYLE_GUIDE.md** | code style | Claude اگر pattern جدید |
| **REUSABLE_SKELETON.md** | راهنمای reuse | Claude به‌مرور |
| **ONBOARDING_GUIDE.md** | روز اول برنامه‌نویس | Claude به‌مرور |
| PROJECT_CONTEXT.md + SESSION_STATUS.md + README.md + CHANGELOG.md | پشتیبان | Claude پایان چت |

**جزئیات کامل:** `docs/PROJECT_GOVERNANCE.md` بخش ۲.

## ۱۶.۳  حفاظت از سند جامع — قواعد No-Deletion (قانون #۲۴)

سند جامع فقط با ۳ روش تغییر می‌کند:

1. ✏️ **افزودن** بخش جدید
2. ✅ **اصلاح** با نشان دادن `❌ قبل → ✅ بعد`
3. 🔄 **به‌روزرسانی state** (status، version، DONE list)

⛔ **هرگز حذف نشود.** اگر بخشی منسوخ شد:

```markdown
## ۸.۵ — [منسوخ — v2.7] روش قدیمی

> ⚠️ از v2.7 منسوخ شد. روش جدید در بخش ۸.۵.۲ مستند شده. دلیل: ...

[محتوای قدیمی برای reference تاریخی...]
```

**چرا؟** چون اگر Claude بعدی به سند نگاه کند، نمی‌داند چه چیزی حذف شده — این یعنی "دانش از بین رفته".

## ۱۶.۴  چک‌لیست اجباری شروع چت Claude (قانون #۲۵)

Claude در شروع هر چت **اجباری است** این ۸ مرحله را انجام دهد:

1. ✅ بازشناسی پیوست‌ها (zip + سند جامع)
2. ✅ استخراج و بررسی ساختار zip
3. ✅ خواندن اسناد به ترتیب الزامی:
   - PROJECT_GOVERNANCE.md
   - PROJECT_CONTEXT.md
   - SESSION_STATUS.md
   - CHAT_LOG.md
   - TASK_BACKLOG.md
   - CLAUDE_CHECKLIST.md
   - سند جامع کامل
4. ✅ بررسی محیط (venv، DB، node_modules)
5. ✅ درک Bug ها و تصمیمات گذشته
6. ✅ تعیین Tier فعلی و گام‌های ممکن
7. ✅ تولید گزارش آمادگی به کاربر
8. ✅ صبر برای تأیید کاربر — **هیچ کار قبل از تأیید**

**جزئیات:** `docs/CLAUDE_CHECKLIST.md` فاز ۱.

## ۱۶.۵  چک‌لیست اجباری پایان چت Claude

در پایان هر چت، Claude ۱۲ مرحله را اجرا می‌کند:

1. جمع‌بندی کارهای انجام‌شده
2. به‌روزرسانی CHAT_LOG.md
3. به‌روزرسانی TASK_BACKLOG.md
4. به‌روزرسانی DECISIONS_LOG.md (اگر تصمیم جدید)
5. به‌روزرسانی TROUBLESHOOTING.md (اگر Bug جدید)
6. به‌روزرسانی GLOSSARY.md (اگر اصطلاح جدید)
7. به‌روزرسانی STYLE_GUIDE.md (اگر pattern جدید)
8. به‌روزرسانی SESSION_STATUS.md
9. به‌روزرسانی PROJECT_CONTEXT.md
10. به‌روزرسانی CHANGELOG.md (اگر version bump)
11. به‌روزرسانی سند جامع (افزایش minor version + change log)
12. ساخت zip نهایی + پیام پایانی

**جزئیات:** `docs/CLAUDE_CHECKLIST.md` فاز ۳.

## ۱۶.۶  Atomic Updates (قانون #۲۶)

اگر یک قانون جدید اضافه می‌شود و در سند جامع آمد ولی در:
- CHAT_LOG (ثبت در چت این جلسه)
- PROJECT_GOVERNANCE (اگر بنیادی است)
- TASK_BACKLOG (اگر TASK مرتبط)
نیامد → **فاجعه آینده**.

تغییرات باید **در یک نوبت** در همه اسناد مرتبط اعمال شوند.

## ۱۶.۷  کلمات کلیدی Trigger برای کاربر

کاربر می‌تواند با این کلمات، Claude را به اصول بازگرداند:

| کلمه | اقدام Claude |
|---|---|
| **Governance** | بازخوانی PROJECT_GOVERNANCE + اعمال |
| **چک‌لیست** | گزارش وضعیت چک‌لیست |
| **E1: کیفیت** | شروع Protocol پایان چت فوری |
| **توقف** | Stop کامل، انتظار دستور |
| **بازگشت به سند** | بازخوانی سند مرتبط |

## ۱۶.۸  حساسیت کاربر — مسئولیت‌ها

از `PROJECT_GOVERNANCE.md` بخش ۷:

- **U1:** پیوست کردن zip + سند جامع در شروع هر چت جدید
- **U2:** تأیید صریح قبل از کارهای سنگین
- **U3:** گزارش نتیجه چک‌های بصری
- **U4:** اعلام تغییر در priorities
- **U5:** اعتراض اگر Claude از Governance منحرف شد

> 💡 **بسیار مهم برای کاربر:** اگر متوجه شدی که Claude از این اصول منحرف شده، **فوری** آن را با کلمات Trigger به اصول برگردان. این کار قبل از اینکه context چت گم شود، بسیار مهم است.

## ۱۶.۹  Handoff به برنامه‌نویس جدید

پروژه طوری طراحی شده که یک برنامه‌نویس جدید بتواند در **یک روز کاری** مسلط شود:

1. خواندن `docs/ONBOARDING_GUIDE.md` (۴-۶ ساعت)
2. اجرای `python scripts/00b_post_unzip_setup.py`
3. ادامه کار

**جزئیات:** `docs/PROJECT_GOVERNANCE.md` بخش ۱۳ + `docs/ONBOARDING_GUIDE.md`.

## ۱۶.۱۰  استخراج Template نهایی

در **پایان trading-system**، یک template جدا با نام پیشنهادی `python-react-skeleton` استخراج می‌شود. این template شامل فقط بخش‌های reusable (FastAPI scaffolding + Auth + Theme Engine + Settings + ...) خواهد بود و در پروژه‌های بعدی در ساعت‌ها — نه روزها — به نتیجه می‌رسد.

**جزئیات:** `docs/REUSABLE_SKELETON.md`.

---

"""


# ============================================================
# تغییر ۵ — سند ۱۷ جدید: Templates پاسخ Claude
# ============================================================

SECTION_17 = """# سند ۱۷ — Templates پاسخ Claude برای موقعیت‌های رایج ⭐

> 🆕 v2.7 — جلوگیری از inconsistency بین Claude های مختلف چت‌ها

این سند الگوهای پاسخ Claude را در موقعیت‌های رایج استاندارد می‌کند. هدف: کاربر بداند **انتظار** چه پاسخی را داشته باشد.

## ۱۷.۱  Template اولین پاسخ در هر چت

```markdown
سلام! بررسی فایل‌ها انجام شد.

## 📍 وضعیت فعلی پروژه

- **فاز:** [N]
- **پیشرفت:** [%]
- **آخرین چت:** [نام چت قبل]
- **آخرین کار:** [خلاصه]

## 🔍 محیط

| چک | وضعیت |
|---|---|
| backend/venv | ✅ / ❌ |
| backend/trading.db | ✅ / ❌ |
| frontend/node_modules | ✅ / ❌ |

[اگر هرکدام ❌: پیشنهاد 00b]

## 📚 خوانده‌شده

- [x] PROJECT_GOVERNANCE
- [x] PROJECT_CONTEXT
- [x] SESSION_STATUS
- [x] CHAT_LOG
- [x] TASK_BACKLOG
- [x] سند جامع v2.X

## 📋 Tasks باز در Tier فعلی (Tier {N})

- [ ] Task A
- [ ] Task B

## 🚀 گزینه‌های گام بعدی

الف) [...]
ب) [...]

منتظر انتخاب شما هستم.
```

## ۱۷.۲  Template پاسخ به "ادامه بده" یا کلمات مبهم

اگر کاربر فقط می‌گوید "ادامه بده" یا "بریم" بدون مشخص کردن:

```markdown
از TASK_BACKLOG.md، گام بعدی پیشنهادی:

**Task {ID} — {عنوان}**
- اولویت: {🔴/🟠/🟡/🟢}
- تخمین تلاش: {XS/S/M/L/XL}
- prerequisites: {اگر هست}

این را انجام دهم یا گزینه‌ی دیگری را ترجیح می‌دهید؟
```

## ۱۷.۳  Template اعلام Bug

```markdown
🐛 **Bug تشخیص داده شد**

### علائم
- [چه چیزی دیده شد]

### علت ریشه‌ای (تحلیل)
- [چرا اتفاق افتاد]

### راه‌حل پیشنهادی
- اسکریپت fix: `scripts/{N}b_fix_xxx.py`
- ثبت در TROUBLESHOOTING.md به‌عنوان Bug #{N}

می‌خواهید اسکریپت fix را الان بسازم؟
```

## ۱۷.۴  Template اعلام تصمیم معماری لازم

```markdown
🏛️ **تصمیم معماری لازم**

### Context
[چرا این سؤال مطرح شد]

### گزینه‌ها

**الف) Option A**
- ✅ مزیت‌ها: ...
- ⚠️ منفی‌ها: ...

**ب) Option B**
- ✅ مزیت‌ها: ...
- ⚠️ منفی‌ها: ...

### پیشنهاد من
گزینه [X] — به دلیل [...]

این تصمیم باید در DECISIONS_LOG.md ثبت شود. نظر شما؟
```

## ۱۷.۵  Template پایان چت

```markdown
📦 **آماده پایان چت**

## کارهای انجام‌شده در این چت

✅ ...
✅ ...

## فایل‌های تولیدشده/به‌روز

- اسکریپت‌ها: N, N+1, ...
- فایل‌های frontend/backend: ...
- اسناد: ...

## TASK های DONE شده

- T{ID}, T{ID+1}

## Bug ها رفع‌شده

- #{N}, #{N+1}

## تصمیمات گرفته‌شده

- #{N}: ...

## نام چت فعلی

**نام نهایی:** `TRADING-phase{N}-part{NN}-{topic}`

## نام پیشنهادی چت بعد

`TRADING-phase{N}-part{NN+1}-{next-topic}`

دلیل: ...

## ZIP نهایی

[ساخت zip + ارائه]

موفق باشید! 🚀
```

## ۱۷.۶  Template اگر کاربر در میانه چت اشتباهی متوجه شد

```markdown
متشکرم که اشاره کردید. شما درست می‌گویید.

## آنچه اشتباه بود
- [توضیح صادقانه]

## چه باید کنیم
1. [اصلاح]
2. [اصلاح]

شروع کنم؟
```

> ⚠️ Claude **هرگز** دفاع نمی‌کند یا توجیه نمی‌آورد. اول اعتراف، بعد اصلاح.

## ۱۷.۷  Template اگر context چت در حال اشباع

```markdown
⚠️ **هشدار: کیفیت ممکن است افت کند**

context چت در حال نزدیک شدن به اشباع است.

پیشنهاد:
1. شروع Protocol پایان چت (فاز ۳)
2. حفظ کیفیت اسناد نهایی
3. ادامه در چت جدید با اسناد به‌روز

با این پیشنهاد موافقید؟
```

## ۱۷.۸  Template ابهام در درخواست کاربر

```markdown
درخواست شما می‌تواند به ۲ شکل تفسیر شود:

**تفسیر A:** [...]
**تفسیر B:** [...]

کدام را در نظر دارید؟ (یا تفسیر سوم؟)
```

> ⚠️ Claude **هرگز فرض نمی‌کند**. ابهام = پرسش (اصل ۵ Governance).

## ۱۷.۹  Template تحویل اسکریپت

```markdown
## 📦 اسکریپت {N}_{name}.py + {N}b_test_{name}.py

### چه می‌کند
- [۱-۳ خط]

### دستور اجرا

🟩 **tab «۲ scripts»:**

```cmd
python scripts/{N}_{name}.py
python scripts/{N}b_test_{name}.py
```

### خروجی مورد انتظار
- ...

### چک بصری (در 🟧 tab «۳ frontend»)
- ...

[فایل‌ها با present_files تحویل]
```

## ۱۷.۱۰  Template حالت احتمالی E1 (افت کیفیت)

```markdown
🚨 **هشدار E1 — افت کیفیت تشخیص داده شد**

نشانه‌ها:
- [...]

پیشنهاد فوری: شروع Protocol پایان چت بدون اتمام کار جاری.

این کار را انجام دهم؟
```

---

این Template ها در طول پروژه به‌مرور بهبود می‌یابند. اگر Template جدیدی لازم بود، در پایان چت اضافه شود.
"""


# ============================================================
# تغییر ۶ — Bug history گسترش (در صورت بخش موجود)
# ============================================================

# این در سند موجود به‌صورت منفصل ثبت شده، در v2.7 یک بخش جامع‌تر اضافه می‌کنیم.
# (ولی Bug ها در TROUBLESHOOTING.md جداگانه ثبت شده‌اند.)

BUG_HISTORY_REF = """

## 🐛 تاریخچه کامل Bug ها

برای جزئیات کامل ۴۹ Bug پروژه، به `docs/TROUBLESHOOTING.md` مراجعه کنید.

**Bug های مهم در Session 6 (v2.7):**
- #46 — ESM URL در ویندوز (Path.as_uri)
- #47 — Font Size scaling شکسته
- #48 — tooltip تاریخ نمودار (timeFormatter)
- #49 — formatNumber در HomePage

"""


# ============================================================
# تغییر ۷ — به‌روزرسانی بخش ۱۵ (وضعیت اجرایی فاز ۰ → ۱۰۰٪)
# ============================================================

SECTION_15_UPDATE_HEADER = """## ۱۵.۱  وضعیت فعلی فاز ۰ (🆕 v2.7 — ۱۰۰٪ تکمیل)

**فاز ۰ کاملاً تکمیل شد در Session 6.**

| زیرگام | وضعیت | چت تکمیل |
|---|---|---|
| ۱ — Project Setup | ✅ DONE | چت ۱ |
| ۲ — Backend Core | ✅ DONE | چت ۲ |
| ۳ — Database + Models | ✅ DONE | چت ۳ |
| ۴ — Auth + API | ✅ DONE | چت ۴ |
| ۵ — Frontend Scaffold | ✅ DONE | چت ۴ |
| ۶ — Login + Routing | ✅ DONE | چت ۴ |
| ۷ — ChartPage | ✅ DONE | چت ۴ |
| ۸.۱ — Theme Engine | ✅ DONE | چت ۵ |
| ۸.۲ — Toast Notifications | ✅ DONE | چت ۵ |
| ۸.۳ — Skeleton + ConfirmDialog | ✅ DONE | چت ۶ |
| ۸.۴ — Settings Page | ✅ DONE | چت ۶ |
| ۸.۵ — Numeric + Persian Calendar | ✅ DONE | چت ۶ |
| Bug fixes #46-#49 | ✅ DONE | چت ۶ |
| Governance Infrastructure | ✅ DONE | چت ۶ |

**فاز بعدی:** Tier 2 (Quality Hardening) در چت `TRADING-phase0-part06-quality-hardening` یا فاز ۱ (CCXT + WebSocket).

### ۱۵.۱.۱  (منسوخ — v2.7) وضعیت قدیمی v2.6

"""

# این بخش بعد از header قرار می‌گیرد، باعث می‌شود محتوای v2.6 به عنوان منسوخ نگه داشته شود


# ============================================================
# توابع اجرا
# ============================================================


def find_section_position(content: str, pattern: str) -> int:
    """پیدا کردن موقعیت یک regex pattern در محتوا."""
    m = re.search(pattern, content)
    return m.start() if m else -1


def upgrade_to_v27(content_v26: str) -> str:
    """ارتقای محتوا از v2.6 به v2.7."""
    content = content_v26

    # تغییر ۱ — عنوان اصلی
    content = content.replace(
        "# سامانه هوشمند ترید — سند جامع v2.6", "# سامانه هوشمند ترید — سند جامع v2.7"
    )
    content = content.replace(
        "📅 نسخه ۲.۶ — اردیبهشت ۱۴۰۵ (May 2026)", "📅 نسخه ۲.۷ — اردیبهشت ۱۴۰۵ (May 2026)"
    )

    # تغییر ۲ — اضافه کردن بخش "تغییرات v2.7" قبل از "تغییرات v2.5 → v2.6"
    marker = "# 📋 خلاصه تغییرات v2.5 → v2.6"
    if CHANGES_V27.strip()[:50] not in content:  # idempotency
        content = content.replace(marker, CHANGES_V27 + marker)

    # تغییر ۳ — اضافه کردن سند ۱۶ و ۱۷ قبل از انتهای سند
    # موقعیت: بعد از آخرین "## ۱۵.۷  Workflow هر مکالمه جدید" تا انتها
    if "# سند ۱۶ — مدیریت دانش و حافظه پروژه" not in content:
        content = content + "\n\n---\n\n" + SECTION_16 + "\n\n---\n\n" + SECTION_17

    # تغییر ۴ — اصلاحیه ۱۳.۶ (جایگزینی بخش)
    # پیدا کردن بخش فعلی ۱۳.۶ و جایگزینی
    pattern_13_6 = r"# سند ۱۳\.۶ جدید — قالب نام چت.*?(?=\n# سند \d+|\Z)"
    if re.search(pattern_13_6, content, re.DOTALL):
        # اگر این بخش به سند ۱۴ تبدیل می‌شود (مثلاً بعد از ۱۳.۶.۵ بخش جدیدی شروع می‌شود)
        # محتوای ۱۳.۶ را جایگزین می‌کنیم با نسخه جدید
        old_13_6 = re.search(pattern_13_6, content, re.DOTALL)
        if old_13_6:
            content = content[: old_13_6.start()] + SECTION_13_6_FIX + content[old_13_6.end() :]

    # تغییر ۵ — اضافه کردن بخش ۸.۸.۲ بعد از ۸.۸.۱
    if "## ۸.۸.۲" not in content:
        # پیدا کردن انتهای ۸.۸.۱
        marker_8_8_1_end_pattern = r"(## ۸\.۸\.۱.*?)(## ۸\.۹)"
        m = re.search(marker_8_8_1_end_pattern, content, re.DOTALL)
        if m:
            section_8_8_1 = m.group(1)
            section_8_9_header = m.group(2)
            replacement = section_8_8_1 + SECTION_8_8_2 + section_8_9_header
            content = content.replace(m.group(0), replacement)

    # تغییر ۶ — به‌روزرسانی فهرست مطالب (افزودن مراجع به ۱۶ و ۱۷)
    fehrest_marker = "- [سند ۱۵ — وضعیت اجرایی پروژه](#سند-۱۵--وضعیت-اجرایی-پروژه)"
    new_fehrest_items = """- [سند ۱۵ — وضعیت اجرایی پروژه](#سند-۱۵--وضعیت-اجرایی-پروژه)
- [**سند ۱۶ — مدیریت دانش و حافظه پروژه** ⭐ 🆕 v2.7](#سند-۱۶--مدیریت-دانش-و-حافظه-پروژه)
- [**سند ۱۷ — Templates پاسخ Claude** ⭐ 🆕 v2.7](#سند-۱۷--templates-پاسخ-claude-برای-موقعیتهای-رایج)"""

    if "[سند ۱۶ — مدیریت دانش" not in content:
        content = content.replace(fehrest_marker, new_fehrest_items)

    return content


def main() -> int:
    print("=" * 64)
    print("اسکریپت ۳۳ — ارتقای سند جامع v2.6 → v2.7")
    print("=" * 64)
    print()

    if not SOURCE.exists():
        print(f"[ERROR] منبع یافت نشد: {SOURCE.relative_to(PROJECT_ROOT)}")
        print("        ابتدا سند v2.6 را در docs/ قرار دهید.")
        return 1

    print(f"خواندن: {SOURCE.relative_to(PROJECT_ROOT)}")
    content_v26 = SOURCE.read_text(encoding="utf-8")
    print(f"  حجم: {len(content_v26):,} کاراکتر، {content_v26.count(chr(10))} خط")

    print()
    print("اعمال تغییرات v2.7...")
    content_v27 = upgrade_to_v27(content_v26)

    # چک تغییرات
    changes_applied = []
    if "v2.7" in content_v27:
        changes_applied.append("✓ ارتقای نسخه به v2.7")
    if "تغییرات v2.6 → v2.7" in content_v27:
        changes_applied.append("✓ بخش تغییرات v2.6 → v2.7")
    if "## ۸.۸.۲" in content_v27:
        changes_applied.append("✓ بخش ۸.۸.۲ — انتخاب فرمت میلادی")
    if "phase{N}" in content_v27 and "phase0-part" in content_v27.lower():
        changes_applied.append("✓ اصلاحیه ۱۳.۶ — phase{N} تک‌رقم")
    if "# سند ۱۶ — مدیریت دانش" in content_v27:
        changes_applied.append("✓ سند ۱۶ — مدیریت دانش")
    if "# سند ۱۷ — Templates پاسخ Claude" in content_v27:
        changes_applied.append("✓ سند ۱۷ — Templates پاسخ")

    for c in changes_applied:
        print(f"  {c}")

    print()
    print(f"نوشتن: {TARGET.relative_to(PROJECT_ROOT)}")

    # idempotency
    if TARGET.exists():
        existing = TARGET.read_text(encoding="utf-8")
        if existing == content_v27:
            print("  - بدون تغییر (idempotent)")
            print()
            print("=" * 64)
            print("✅ سند v2.7 از قبل موجود و یکسان است.")
            print("=" * 64)
            return 0

    TARGET.write_text(content_v27, encoding="utf-8", newline="\n")
    print(f"  حجم جدید: {len(content_v27):,} کاراکتر")
    print(f"  افزایش: +{len(content_v27) - len(content_v26):,} کاراکتر")

    print()
    print("=" * 64)
    print("✅ سند جامع v2.7 ساخته شد.")
    print("=" * 64)
    print()
    print("گام بعدی: ارجاع به این فایل از سایر اسناد:")
    print("  - PROJECT_CONTEXT.md: نسخه فعلی → v2.7")
    print("  - SESSION_STATUS.md: نسخه فعلی → v2.7")
    print("  - README.md: نسخه ذکرشده → v2.7")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
