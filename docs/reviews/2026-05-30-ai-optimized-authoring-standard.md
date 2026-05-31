# Review #011 — AI-Optimized Prompt/Artifact Authoring Standard (v2.17)

> **تاریخ:** 2026-05-30
> **Trigger:** §۲.۱ (Constitution change — ۱ Locked rule جدید #۸۸؛ batch اتمیک با #۸۷/Review #۰۱۰)
> **Related artifacts:** docs/constitution/01_rules.md, docs/constitution/main.md, docs/DECISIONS_LOG.md, docs/SESSION_STATUS.md, scripts/63_pre_commit_audit.py, .pre-commit-config.yaml
> **Status:** **Implemented**
> **⚠️ یادداشت backfill (صداقت، #۸۴/M82):** این فایل review در part18 (هنگام codify) **ساخته نشد** — فقط ردیف #۰۱۱ در REVIEW_LOG ثبت شد. شکاف LOG↔file در boot part19 کشف و این فایل backfill شد. Commit boundary اصلیِ codify = `29b2b56` (part18). اقدام مکانیکی جلوگیری از تکرار: check_13 (Review #۰۱۲، part19).

## ۱. Context — چرا الان؟

کاربر در part18 یک دستور دائمی داد: هر «artifact نوشتاری» پروژه — پرامپت چت بعد، فایل handoff، متن Instructions/Project Knowledge، Scope Contract، و هر دستور به یک Claude دیگر — باید طبق اصول prompt-engineering بهینهٔ مدل نوشته شود. مشاهدهٔ پشتیبان: artifactهای نوشتاری بدون ساختار/DoD/گارد، در چت بعد خطای تفسیر و drift می‌سازند (هم‌خانوادهٔ M23/M59 — Claude بعدی فقط همان متن را می‌بیند).

## ۲. Options Considered — گزینه‌ها

۱. **Option A — Rule #۸۸ Locked (۸ معیار)، batch اتمیک با #۸۷** (selected)
   - Pros: استاندارد شمارش‌پذیر (DoD)؛ enforceable به‌صورت checklist؛ هم‌راستا اصل ۳ (radical honesty) + #۷۹ (QHP)
   - Cons: رفتاری (اتکا به self-discipline) — ثبت‌شده در meta-deliverable reliability-audit
۲. **Option B — principle در 04_principles.md (نه Rule)** — Cons: principle ضمانت per-artifact DoD نمی‌دهد؛ کاربر «دستور دائمی» خواست نه فلسفه
۳. **Option C — defer** — Cons: درخواست دائمی صریح کاربر معلق می‌ماند

## ۳. Decision — تصمیم

**Selected:** Option A (Rule #۸۸ Locked، ۸ معیار، batch اتمیک با #۸۷، v2.17). مرجع: Decision #۷۰.

**Rationale:**
- «دستور دائمی» = Locked rule، نه principle (#۶۱ spirit — انتخاب مطلوب صریح)
- شمارهٔ #۸۸ (نه #۸۷) تا با Settings/Instructions Sync Reminder تصادم نکند
- ۸ معیار = Definition-of-Done شمارش‌پذیر (criterion 3 خودِ قانون) → قابل self-check per turn (خط AOA)
- متوازن با #۱۶ (کم‌حرفی): برای پیام‌های صرفاً مکالمه‌ای سخت‌گیری لازم نیست؛ روی artifactهای پایدار اعمال

## ۴. Impact — اثر

### Files changed (در commit codify `29b2b56`)
- `docs/constitution/01_rules.md` — قانون #۸۸ (جدول ۱.۹ + بخش «شرح کامل قوانین Sync & Authoring» با ۸ معیار + footer #۱-۸۸)
- `docs/constitution/main.md` — frontmatter v2.16→v2.17 + آمار (rule count ۸۸) + version history + cross-ref #۸۷-۸۸
- `docs/DECISIONS_LOG.md` — Decision #۷۰
- `docs/SESSION_STATUS.md` — surgical (Constitution v2.17، rule count ۸۸)
- `scripts/63_pre_commit_audit.py` — CURRENT_VERSION→v2.17 + ACCEPTABLE [v2.14..v2.17]
- `.pre-commit-config.yaml` — hook label (v2.17)
- `docs/reviews/2026-05-30-ai-optimized-authoring-standard.md` — این فایل (backfill part19)

### Constitution impact
- ۱ rule جدید Locked (#۸۸)؛ version v2.16 → v2.17 (همراه #۸۷)

### Audit coupling
- check_1 (rule counts) → هر سه منبع = ۸۸ (الزامی، با #۸۷)
- check_6 (version) → ACCEPTABLE_VERSIONS شامل v2.17
- check_10 (review numbering) → #۰۱۱ متوالی پس از #۰۱۰
- check_13 (NEW part19) → این فایل اکنون موجود است → row↔file برقرار

### Backward compatibility
- safe: قواعد #۱-۸۷ unchanged؛ #۸۸ additive

## ۵. Lessons Applied — درس‌های کاربردی

- **اصل ۳ (radical honesty) + #۷۹ (QHP)**: criterion 3 قانون = DoD شمارش‌پذیر (اعداد N/M، نه واژهٔ مبهم) ✅
- **#۸۶ (منبع زنده)**: criterion 7 = ارجاع به git/فایل نه حافظه ✅
- **#۱۶ (کم‌حرفی)**: متوازن — فقط artifactهای پایدار، نه پیام مکالمه‌ای ✅
- **M82/#۸۴ (backfill)**: این فایل با اذعان صریح به شکاف LOG↔file part18 ساخته شد ✅
- **dogfood**: خود این فایل review طبق ۸ معیار #۸۸ ساختاربندی شد (نقش/هدف، بخش‌بندی، DoD، گارد، منبع زنده) ✅

## ۶. Signatures

- Claude: confirmed (codify part18 commit `29b2b56` + این فایل backfill part19)
- User: explicit approval (دستور دائمی part18 + تأیید scope part19)
- Commit boundary: codify atomic commit `29b2b56` (part18)؛ این فایل backfill در commit part19 (hash از git زنده در boot بعد، M101)
