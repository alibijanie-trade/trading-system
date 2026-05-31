# Review #010 — Settings/Instructions/Project-Asset Sync Reminder (v2.17)

> **تاریخ:** 2026-05-30
> **Trigger:** §۲.۱ (Constitution change — ۱ Locked rule جدید #۸۷؛ batch اتمیک با #۸۸/Review #۰۱۱)
> **Related artifacts:** docs/constitution/01_rules.md, docs/constitution/main.md, docs/constitution/06_meta.md, docs/DECISIONS_LOG.md, docs/SESSION_STATUS.md, scripts/63_pre_commit_audit.py, .pre-commit-config.yaml
> **Status:** **Implemented**
> **⚠️ یادداشت backfill (صداقت، #۸۴/M82):** این فایل review در part18 (هنگام codify) **ساخته نشد** — فقط ردیف #۰۱۰ در REVIEW_LOG ثبت شد. شکاف LOG↔file در boot part19 کشف و این فایل backfill شد. Commit boundary اصلیِ codify = `29b2b56` (part18). اقدام مکانیکی جلوگیری از تکرار: check_13 (Review #۰۱۲، part19).

## ۱. Context — چرا الان؟

در چت part18، کاربر صریح درخواست کرد سه target خارج از دسترس Claude — که فقط کاربر دستی تغییر می‌دهد (M17) — هنگام هر تغییر **material** پروژه به‌صورت سیستماتیک sync شوند:

1. **Settings → General → کادر Instructions** (رفتار سراسری Claude).
2. **Projects → trading-system → کادر Instructions پروژه**.
3. **Projects → trading-system → فایل‌های Project Knowledge** (افزودن/جایگزینی مثل `PROJECT_KNOWLEDGE.md`).

مشکل ریشه‌ای: تغییرات قانون/درس/پروتکل/نسخه در فایل‌سیستم اعمال می‌شوند، ولی این سه کادر دستی عقب می‌مانند → Claude چت بعد با context کهنه boot می‌کند. قانون #۵۵ فقط Project Knowledge را پوشش می‌داد و جنبهٔ «یادآوری اجباری + گرفتن تأیید انجام + persist» را نداشت.

## ۲. Options Considered — گزینه‌ها

۱. **Option A — Rule #۸۷ Locked با Materiality Threshold + Full-Text Delivery، batch اتمیک با #۸۸** (selected)
   - Pros: تعمیم #۵۵ به هر سه target؛ یادآوری در‌لحظه + تأیید + persist؛ جلوگیری از over-reminding با آستانهٔ materiality
   - Cons: یک قانون رفتاری (نه مکانیکی) — اتکا به self-discipline Claude (ثبت‌شده در meta-deliverable reliability-audit)
۲. **Option B — صرفاً گسترش متن #۵۵** — Cons: جنبهٔ یادآوری/تأیید/persist و سه‌target بودن را codify نمی‌کند
۳. **Option C — defer** — Cons: drift سه کادر دستی ادامه می‌یابد؛ درخواست صریح کاربر معلق می‌ماند

## ۳. Decision — تصمیم

**Selected:** Option A (Rule #۸۷ Locked، batch اتمیک با #۸۸، v2.17). مرجع: Decision #۶۹.

**Rationale:**
- #۸۷ و #۸۸ هر دو «governance authoring/sync» اند → یک concept batch (M98 scope closure) → atomic
- Materiality Threshold از over-reminding برای تغییرات non-material جلوگیری می‌کند (تعادل با #۱۶ کم‌حرفی)
- Full-Text Delivery (کل متن کادر، نه «خط X را عوض کن») هم‌راستا #۲۹/#۸۸ — کاربر فقط select-all → paste

## ۴. Impact — اثر

### Files changed (در commit codify `29b2b56`)
- `docs/constitution/01_rules.md` — قانون #۸۷ (جدول ۱.۹ + بخش «شرح کامل قوانین Sync & Authoring» + footer)
- `docs/constitution/main.md` — frontmatter v2.16→v2.17 + آمار (۸۶→۸۸ با #۸۸) + version history + cross-ref #۸۷-۸۸
- `docs/constitution/06_meta.md` — §۶.۸ Project Knowledge: یادداشت v2.17 قانون #۸۷ (سه target manual)
- `docs/DECISIONS_LOG.md` — Decision #۶۹
- `docs/SESSION_STATUS.md` — surgical (Constitution v2.17، rule count)
- `scripts/63_pre_commit_audit.py` — CURRENT_VERSION→v2.17 + ACCEPTABLE [v2.14..v2.17]
- `.pre-commit-config.yaml` — hook label (v2.17)
- `docs/reviews/2026-05-30-settings-instructions-sync-reminder.md` — این فایل (backfill part19)

### Constitution impact
- ۱ rule جدید Locked (#۸۷)؛ version v2.16 → v2.17 (همراه #۸۸)

### Audit coupling
- check_1 (rule counts) → هر سه منبع باید با #۸۸ به ۸۸ برسند (الزامی)
- check_6 (version) → ACCEPTABLE_VERSIONS شامل v2.17
- check_10 (review numbering) → #۰۱۰ متوالی پس از #۰۰۹
- check_13 (NEW part19) → این فایل اکنون موجود است → row↔file برقرار

### Backward compatibility
- safe: قواعد #۱-۸۶ unchanged؛ #۸۷ additive

## ۵. Lessons Applied — درس‌های کاربردی

- **M17**: سه target خارج از Filesystem MCP اند؛ Claude فقط محتوای copy-ready آماده می‌کند، کاربر paste/attach می‌کند ✅
- **#۵۵ → #۸۷**: تعمیم Project Knowledge به هر سه target + یادآوری/تأیید/persist ✅
- **#۲۹/#۸۸ (Full-Text Delivery)**: کل متن کادر یک‌جا، نه «خط X» ✅
- **M82/#۸۴ (backfill)**: این فایل با اذعان صریح به شکاف LOG↔file part18 ساخته شد، نه وانمود به ساخت در زمان codify ✅

## ۶. Signatures

- Claude: confirmed (codify part18 commit `29b2b56` + این فایل backfill part19)
- User: explicit approval (درخواست صریح part18 + تأیید scope part19)
- Commit boundary: codify atomic commit `29b2b56` (part18)؛ این فایل backfill در commit part19 (hash از git زنده در boot بعد، M101)
