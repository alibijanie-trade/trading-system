# ماژول ۰۳ — کاتالوگ Bug ها

> بخشی از **Constitution v2.12 (Modular)** — [بازگشت به main](./main.md)
>
> **محتوا:** کاتالوگ Bug ها (#1-#54+) با علائم، علت ریشه‌ای، fix، تست regression.
> **منبع v2.11:** Bug ها در changelog های نسخه‌ها (v2.4-v2.7) + فایل جداگانه `docs/TROUBLESHOOTING.md`
> **به‌روزرسانی v2.12:** افزودن Bug #54 (Decisions Numbering Gap — ✅ Resolved در cleanup چت ۱۰)
> **Created in commit:** `<git log -1 --format=%h پس از commit 4 پر شود>`

---

## 📋 فهرست Bug ها (پس از migration)

> این فهرست در commit 4 (مرحله ۳ Migration) از منابع v2.11 پر می‌شود.

### دسته‌بندی به Severity

- **🔴 Critical** (بلوکر، باعث crash یا data loss می‌شود): #۳۸ APP_VERSION، #۳۹ passlib، #۴۰ npm registry، #۵۳ pip BOM
- **🟠 High** (functionality broken): #۳۱، #۳۲، #۴۱، #۴۶، #۴۷، #۴۸
- **🟡 Medium** (UX/style): #۴۲، #۴۳، #۴۴، #۴۵
- **🟢 Low** (cosmetic): #۴۹، #۵۰، #۵۱، #۵۲
- **✅ Resolved**: #۵۴ (Decisions Gap)

### دسته‌بندی به منشأ

- **Environment** (Windows، CMD، encoding): #۳۲، #۴۰، #۴۶، #۵۳
- **Dependency mismatch** (passlib، bcrypt، DB column): #۳۹، #۴۷، #۴۸
- **Code logic** (cargo cult): #۳۸، #۴۱، #۴۲، #۴۳
- **Documentation drift** (آمار اشتباه): #۵۴

---

## 🚧 وضعیت این ماژول

⚠️ **این فایل فعلاً skeleton است.** محتوای Bug ها در **commit 4** از سند جامع v2.11 + `docs/TROUBLESHOOTING.md` migrate می‌شود.

پس از migration، ساختار هر Bug این خواهد بود:

```markdown
## Bug #N — [عنوان کوتاه]

**نسخه/چت:** چت Z (vX.Y)
**Severity:** 🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low
**Status:** 🟢 Open | 🟡 In Progress | ✅ Resolved | 🔵 Won't Fix
**Cross-refs:** قانون #X، درس M{Y}

### علائم
[چه چیزی دیده شد]

### علت ریشه‌ای
[چرا اتفاق افتاد]

### Fix
[راه‌حل اعمال‌شده، با scripts/commits مرجع]

### تست Regression
[چطور verify می‌شود که برنگردد]

### Lessons learned
[درس(های) استخراج‌شده، با ارجاع به `02_lessons.md`]
```

---

## 🔮 افزوده‌های v2.12 (در commit 8)

Bug های جدید که در مرحله ۴ Atomic Update به این ماژول اضافه می‌شوند:

- **Bug #54** ✅ RESOLVED — Decisions Numbering Gap (#۵۷→#۶۵): در cleanup round 1 پایان چت ۱۰ کشف شد، در همان round رفع شد (backfill Decisions #۵۸-۶۶).
- **Bug #53** 🔴 — pip روی Windows با UTF-8 بدون BOM crash (رفع‌شده با utf-8-sig). درس M67.

> هیچ Bug جدید open در پایان چت ۱۱.۰.الف انتظار نمی‌رود (این چت infra است، نه code).

---

**📌 پایان skeleton 03_bugs.md — منتظر محتوای migration در commit 4**
