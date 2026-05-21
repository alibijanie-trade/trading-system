# Constitution سامانه هوشمند ترید — v2.12 (Modular)

> **Intelligent Trading System — Modular Constitution**
> در بازارهای مالی | ارز دیجیتال و فارکس
>
> **نسخه:** 2.12 (modular split از v2.11)
> **تاریخ شروع split:** اردیبهشت ۱۴۰۵ (May 2026)
> **چت مسئول:** ۱۱.۰.الف (`TRADING-infra-governance-constitution-split`)
> **Branch:** `infra/governance-overhaul`
> **Created in commit:** `<git log -1 --format=%h پس از commit 1 پر شود>`

---

## 🎯 چرا این Constitution Modular است؟

نسخه v2.11 یک فایل ~۲۲۰KB بود که با Filesystem MCP در فایل‌های بزرگ کند می‌شد (M66). split به ۶ ماژول + main این مشکل را حل می‌کند:

- هر ماژول < ۵۰KB → MCP-safe
- ویرایش هدفمند بدون لمس کل سند
- cross-refs صریح به‌جای جستجوی متنی
- precedent برای پروژه‌های آینده

---

## 📚 ساختار ماژول‌ها

| ماژول | محتوا | برآورد اندازه |
|---|---|---|
| **[main.md](./main.md)** | این فایل — index + cross-refs + Vision + Quick-start | ~8KB |
| **[01_rules.md](./01_rules.md)** | قوانین Locked #۱-N (با شرح کامل، نمونه، استثناها) | ~45KB |
| **[02_lessons.md](./02_lessons.md)** | درس‌نامه اشتباهات Claude (M1-M83+) با علت ریشه‌ای و راه‌حل | ~50KB |
| **[03_bugs.md](./03_bugs.md)** | کاتالوگ Bug ها (#1-#54+) با علائم، علت، fix | ~30KB |
| **[04_principles.md](./04_principles.md)** | ۸ اصل بنیادی + سطح‌بندی 🔒/🎯/💡 + No-Deletion + Atomic Updates | ~12KB |
| **[05_architecture.md](./05_architecture.md)** | Stack + DB Schema + Backend + Frontend + UI/UX + Security + Roadmap | ~40KB |
| **[06_meta.md](./06_meta.md)** | Session/Context + Templates + MCP + Claude Desktop + claude_workspace + Skills | ~35KB |

---

## 🗝️ راهنمای نمادها (سراسری در همه ماژول‌ها)

| نماد | معنا |
|---|---|
| 🔒 | **قفل‌شده** — قابل تغییر نیست مگر با توافق صریح صاحب پروژه |
| 🎯 | **تصمیم‌شده** — با پیشنهاد مستدل Claude + تأیید صاحب پروژه قابل تغییر است |
| 💡 | **پیشنهادی** — Claude می‌تواند بهبود بدهد، باید دلیل و مزیت را توضیح دهد و منتظر تأیید بماند |
| 🆕 v2.X | تغییر اضافه‌شده در نسخه v2.X |
| ⭐ | بخش حیاتی — توجه ویژه |
| ⚠️ | هشدار/توجه |

---

## 🧭 Quick-start برای Claude در شروع هر چت جدید

طبق قانون #۴۸ (پروتکل اجباری شروع چت)، Claude باید این مسیر را طی کند:

1. **`main.md`** (همین فایل) — برای آشنایی با ساختار modular
2. **`04_principles.md`** — برای فهم سطح‌بندی و فلسفه پروژه
3. **`01_rules.md`** — قوانین کامل Locked
4. **`02_lessons.md`** — درس‌نامه برای جلوگیری از تکرار اشتباهات
5. **`docs/PENDING_FOR_NEXT_VERSION.md`** — PENDING آیتم‌های ادغام نشده
6. **`docs/SESSION_STATUS.md`** — وضعیت فعلی پروژه
7. **`docs/DECISIONS_LOG.md`** — تصمیمات معماری ثبت‌شده
8. **`docs/CHAT_LOG.md`** بخش چت قبل
9. **اجرای M73 audit** — Cross-Document Consistency Check

سایر ماژول‌ها (`03_bugs.md`, `05_architecture.md`, `06_meta.md`) **on-demand** خوانده می‌شوند — وقتی موضوع مرتبط مطرح شد.

---

## 🔗 Cross-references اصلی

### قوانین مهم در `01_rules.md`

- **#۴۸** پروتکل اجباری شروع چت → `01_rules.md#قانون-48`
- **#۶۰** PENDING-EOC در لحظه ثبت → `01_rules.md#قانون-60`
- **#۶۲** فایل handoff دائمی → `01_rules.md#قانون-62`
- **#۶۳** Convention `🟢 ▶️ EXECUTE` → `01_rules.md#قانون-63`
- **#۶۴** عدم نمایش جزئیات تصحیح خطا → `01_rules.md#قانون-64`
- **#۶۵** ثبت درس از اشتباهات با نمایش → `01_rules.md#قانون-65`
- **#۶۶** Push اجباری در پایان هر چت (Locked در v2.12) → `01_rules.md#قانون-66`

### درس‌های مهم در `02_lessons.md`

- **M23** ⭐⭐⭐ عدم تولید handoff → `02_lessons.md#m23`
- **M66** Filesystem MCP و فایل‌های بزرگ → `02_lessons.md#m66`
- **M71-M73** Documentation Drift + Verification + Audit → `02_lessons.md#m71-m73`
- **M74-M79** درس‌های cleanup round 2 → `02_lessons.md#m74-m79`
- **M82** Verification Claim Must Be Verified → `02_lessons.md#m82`
- **M83** Retry First, Restructure Last → `02_lessons.md#m83`

### اصول بنیادی در `04_principles.md`

- اصل ۸ مشاوره: کاربردی، مهندسی، صادقانه، بدون تعارف، همه‌جانبه
- اصل طلایی: «امروز ساده، فردا قابل‌توسعه»
- No-Deletion (قانون #۲۴): سند جامع هرگز حذف نمی‌شود
- Atomic Updates (قانون #۲۶): تغییر در یک سند → اعمال هم‌زمان در همه اسناد مرتبط
- M82: Verification Claim Must Be Verified Itself

### معماری در `05_architecture.md`

- Stack: FastAPI + SQLAlchemy + React + Vite + SQLite
- DB Schema: ۱۲ جدول اصلی + AuditLog
- Backend: Layered Architecture (Presentation/Application/Domain/Infrastructure)
- Frontend: BrowserRouter + Zustand + axios interceptor
- UI/UX: RTL + Theme Engine + Design System بایننس
- Security: bcrypt + JWT + Fernet + RBAC + AuditLog
- Roadmap: ۱۵ فاز

### Meta در `06_meta.md`

- Session Management + Context handoff
- Templates پاسخ Claude (۱۰ Template)
- Filesystem MCP Integration
- Claude Desktop Configuration (Memory + Project Knowledge + Custom Instructions + Settings)
- `claude_workspace/` structure
- Skills اختصاصی پروژه (placeholder)

---

## 📊 آمار Constitution v2.12

| دسته | تعداد |
|---|---|
| قوانین Locked | <ادغام در مرحله ۴ پر می‌شود> |
| درس‌نامه ردیف | <ادغام در مرحله ۴ پر می‌شود> |
| Bug ها | <ادغام در مرحله ۴ پر می‌شود> |
| ماژول‌ها | ۷ (شامل main.md) |
| اندازه کل (تقریبی) | ~۲۲۰KB توزیع شده در ۷ فایل |
| بزرگترین ماژول | <ادغام در مرحله ۴ پر می‌شود> |

---

## 🚧 وضعیت Migration (در حین چت ۱۱.۰.الف)

- [x] Skeleton (commit 1) — این فایل + ۶ ماژول خالی + archive
- [ ] Migrate سند ۱ → `01_rules.md` (commit 2)
- [ ] Migrate سند ۱۸ → `02_lessons.md` (commit 3)
- [ ] Migrate Bug catalog → `03_bugs.md` (commit 4)
- [ ] Migrate principles → `04_principles.md` (commit 5)
- [ ] Migrate سند ۲-۸+۱۲ → `05_architecture.md` (commit 6)
- [ ] Migrate سند ۱۳-۱۷+۱۹-۲۵ → `06_meta.md` (commit 7)
- [ ] Archive سند قدیمی + Atomic Update v2.12 (commit 8)

پس از merge این branch به main، این لیست به‌روز می‌شود.

---

## 📜 تاریخچه نسخه‌ها

| نسخه | تاریخ | چت(ها) | تغییرات اصلی |
|---|---|---|---|
| v2.12 | May 2026 | ۱۱.۰.الف+ب+ج | **Modular split** — تقسیم به ۶ ماژول + atomic update با ادغام PENDING |
| v2.11 | May 2026 | ۸+۹ | UX hardening — قوانین #۶۲-۶۵ |
| v2.10 | May 2026 | ۷+۸ | Filesystem MCP + claude_workspace |
| v2.9 | May 2026 | ۷ | Tier 2 Quality Hardening |
| v2.8 | May 2026 | ۶ | Atomic Update چت ۶ + قوانین #۲۷-۳۲ |
| v2.7 | May 2026 | ۵.ب | Governance ۱۲-سندی + قوانین #۲۳-۲۶ |
| v2.6 | May 2026 | ۵.الف | Theme Engine + Variant Pattern |
| v2.5 | May 2026 | ۴ | Auth + Frontend scaffold + قوانین #۱۹-۲۰ |
| v2.4 | May 2026 | ۳ | DB Infrastructure + DataSource Layer + قوانین #۱۶-۱۸ |
| v2.3 | May 2026 | ۲ | Chat Handoff Protocol |
| v2.2 | May 2026 | ۲ | اولین versioning رسمی |
| v2.1 | May 2026 | ۱ | Stack hardening + Fernet + AuditLog |
| v2.0 | May 2026 | ۱ | بنیاد اولیه |

---

**📌 پایان main.md**

برای جزئیات هر بخش، به ماژول مربوطه مراجعه کنید. این فایل صرفاً index و navigation است.
