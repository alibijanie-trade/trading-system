# ماژول ۰۲ — درس‌نامه اشتباهات Claude

> بخشی از **Constitution v2.12 (Modular)** — [بازگشت به main](./main.md)
>
> **محتوا:** درس‌نامه اشتباهات Claude (M1-M83+) با علت ریشه‌ای، راه‌حل، و cross-refs.
> **منبع v2.11:** سند ۱۸ (M1-M63)
> **به‌روزرسانی v2.12:** افزودن M64-M83 از PENDING (Z2.1-Z2.21)
> **Created in commit:** `<git log -1 --format=%h پس از commit 3 پر شود>`

---

## 📋 فهرست درس‌ها

> این فهرست در commit 3 (مرحله ۳ Migration) از سند ۱۸ منبع v2.11 پر می‌شود، سپس در مرحله ۴ (Atomic Update) با M64-M83 از PENDING گسترش می‌یابد.

### دسته‌بندی موضوعی (پس از migration کامل)

- **Verify-before-act** (M37, M61, M82): اعتماد نکردن به status، read-back، verification claim verification
- **Self-binding** (M62, M77): Claude خود را به قوانین ذکر شده ملزم می‌کند
- **Documentation drift** (M71, M73, M75, M78): تناقض درون و بین اسناد
- **Reserved IDs policy** (M22, M24, M29, M32-M43, M45-M55, M79): نگه‌داری gap های شناخته
- **Process** (M23, M56, M57, M58, M59, M63, M72): فرآیند پایان چت و handoff
- **Tooling** (M30, M44, M66): محدودیت‌های MCP، Claude Desktop، فایل‌های بزرگ
- **Code execution** (M9, M67, M69): Windows + UTF-8 + asyncio quirks
- **MCP retry strategy** (M83): retry قبل از restructure

---

## 🚧 وضعیت این ماژول

⚠️ **این فایل فعلاً skeleton است.** محتوای M1-M63 در **commit 3** از سند جامع v2.11 (سند ۱۸) migrate می‌شود.

پس از migration، ساختار هر درس این خواهد بود:

```markdown
## M{N} — [عنوان کوتاه]

**کشف‌شده در:** چت Z (یا «Reserved / Unknown»)
**اهمیت:** 🔴 critical | 🟠 high | 🟡 medium | 🟢 low | 💡 informational
**Cross-refs:** قانون #X، Bug #Y

### اشتباه
[چه اتفاقی افتاد]

### علت ریشه‌ای
[چرا اتفاق افتاد]

### راه‌حل
[چه‌کار باید کرد]

### مثال عینی
[scenario که در آن اتفاق افتاد]

### قوانین مرتبط
[لیست قوانین که برای جلوگیری از این اشتباه ایجاد شدند]
```

---

## 🔮 افزوده‌های v2.12 (در commit 8)

درس‌های جدید که در مرحله ۴ Atomic Update به این ماژول اضافه می‌شوند (از PENDING Z2.1-Z2.21):

### درس‌های فنی چت ۱۰ (M64-M70)

- **M64** JSX runtime در plugin-react vs esbuild
- **M65** تشخیص shell از prompt
- **M66** ⚠️ Filesystem MCP و فایل‌های >۲۰۰KB hang می‌کند
- **M67** 🔴 BOM لازم برای pip روی Windows
- **M68** نسخه‌های pinned باید با PyPI verify شوند
- **M69** asyncio.run() در FastAPI handler crash می‌کند
- **M70** سادگی workflow > لایه‌بندی پیچیده

### درس‌های process چت ۱۰ cleanup round 1 (M71-M73)

- **M71** ⚠️ Documentation Drift Self-Reference Paradox
- **M72** End-of-Chat Verification Checklist
- **M73** Cross-Document Consistency Audit

### درس‌های چت ۱۱ cleanup round 2 (M74-M79)

- **M74** Full-Range Decision Audit (نه Local)
- **M75** Within-File Consistency Check
- **M76** Decision vs Rule تمایز مبهم (Locked vs Proposed)
- **M77** ⭐ HEAD Self-Reference نباید Hardcode باشد (placeholder الزامی)
- **M78** Re-read After Edit (عدم اتکا به diff)
- **M79** Reserved IDs Explicit مستند شوند

### درس‌های چت ۱۱.۰.الف (M82-M83)

- **M82** ⭐ Verification Claim Must Be Verified Itself (cleanup round ادعا کرد سینک، نشد)
- **M83** Retry First, Restructure Last (MCP transient fail → rename نزن، retry بزن)

> M80, M81 → Reserved (gap policy، آیتم‌های احتمالی کشف نشده)

---

**📌 پایان skeleton 02_lessons.md — منتظر محتوای migration در commit 3**
