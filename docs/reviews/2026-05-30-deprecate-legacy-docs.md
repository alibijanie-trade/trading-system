# Review #009 — Deprecate Legacy Monolithic Docs

> **تاریخ:** 2026-05-30
> **Trigger:** §2.2 + §2.4 (حذف از scope / redirect-stub + moving files between tiers)
> **Related artifacts:** ۱۰ سند legacy (سند_جامع_v2_6..v2_11، PROJECT_GOVERNANCE، CLAUDE_CHECKLIST، PROJECT_CONTEXT، ARCHITECTURE) · Constitution v2.16 modular · part17
> **Status:** Approved (روی دیسک implemented؛ commit در part17 chat-end)

## ۱. Context — چرا الان؟

Constitution از v2.12 به ساختار modular مهاجرت کرد (`docs/constitution/`). اسناد یکپارچهٔ legacy (سند جامع v2.6–v2.11) و اسناد حاکمیتی پیش-modular (PROJECT_GOVERNANCE، CLAUDE_CHECKLIST، PROJECT_CONTEXT، ARCHITECTURE) هنوز بدون نشان deprecated در `docs/` بودند → ریسک رجوع اشتباه به source-of-truth منسوخ. این بخشی از باقیماندهٔ Phase 3 (Objective 2) است.

## ۲. Options Considered

1. **Option A — banner DEPRECATED درجا (بدون حذف):** هر فایل یک banner یک‌خطی بالای عنوان می‌گیرد که به مرجع modular فعال اشاره می‌کند. pros: حفظ #۲۴، صفر شکست مسیر/لینک تاریخی، کم‌ریسک. cons: فایل‌ها در `docs/` می‌مانند (شلوغی بصری جزئی).
2. **Option B — انتقال به `docs/archive/`:** pros: پوشهٔ docs تمیزتر. cons: مسیرها/لینک‌های تاریخی می‌شکنند + نیاز redirect-stub جدا برای هرکدام + ریسک بالاتر.
3. **Option C — حذف:** ممنوع طبق #۲۴ (No-Deletion).

## ۳. Decision

**Selected:** Option A.
**Rationale:** کم‌ریسک‌ترین گزینهٔ #۲۴-سازگار، بدون شکستن ارجاعات تاریخی. هر فایل یک banner یک‌خطی بالای عنوان گرفت که به مرجع modular فعال اشاره می‌کند. `PROJECT_CONSTITUTION.md` (که خود یک redirect stub فعال به modular است) عمداً خارج از scope ماند.

## ۴. Impact

- **Files changed:** ۱۰ (banner prepend) — `سند_جامع_v2_6/7/8/9/10/11`، `PROJECT_GOVERNANCE`، `CLAUDE_CHECKLIST`، `PROJECT_CONTEXT`، `ARCHITECTURE`.
- **Commits:** part17 chat-end (atomic؛ hash backfill per M101).
- **Constitution impact:** هیچ تغییر normative — banner صرفاً metadata/redirect (نوع §3.3).
- **Manifest impact:** Tier این فایل‌ها → Legacy/deprecated (به‌روزرسانی PROJECT_MANIFEST در drift/chat-end در صورت لزوم).
- **Backward compatibility:** safe (محتوای اسناد دست‌نخورده، فقط banner افزوده).

## ۵. Lessons Applied

- **#۲۴** (No-Deletion) — banner به‌جای حذف.
- **#۶۹** (Review Trigger Enforcement) — این Review پاسخ trigger §2.2/§2.4 است.
- **REVIEW_PROTOCOL §9.1** (Conceptual Cohesion) — یک Review واحد برای ۱۰ فایل هم‌مفهوم، نه ۱۰ Review مستقل.
- **#۸۶ / M104** — شمارهٔ Review (#۰۰۹) از منبع زندهٔ `REVIEW_LOG.md` مشتق شد، نه حافظه.

## ۶. Signatures

- **Claude:** این Review + اعمال ۱۰ banner (هر کدام با read-back diff).
- **User:** تأیید گزینهٔ A («پیشنهاد خودت» + تأیید B1 sequence در Pre-Task Checkpoint).
- **Commit boundary:** `<pending part17 chat-end>` (backfill per M101 در boot چت بعد یا chat-end).
