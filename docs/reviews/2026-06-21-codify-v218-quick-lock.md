# Review #013 — codify-v218-quick-lock

**Date:** 2026-06-21
**Status:** Implemented
**Trigger:** §2.1 (Scope Contract + user explicit approval)
**Chat:** `TRADING-phase1-part21-codify-v218-and-governance-repair`
**Decision:** #71

---

## موضوع

Codification of Quick-Lock governance pattern into Constitution v2.18.

---

## خلاصه تصمیم

QL-0..QL-5 که از part19 در `claude_workspace/LOCKED_RULES_INBOX.md` quick-lock شده بودند، در این batch اتمیک به‌صورت رسمی codify شدند:

**قوانین جدید:**
- **#۸۹ Locked** — Quick-Lock Mechanism: قفل‌کردن = append به LOCKED_RULES_INBOX + binding فوری، بدون bump/Decision/Review. codify رسمی ادواری.
- **#۹۰ Locked** — No-Reliance on Human Memory/Attention: هر نیاز تکرارشونده باید گارد مکانیکی داشته باشد، نه یادآوری.

**تبصره‌های روی قوانین موجود:**
- #۵۱.۱ — Per-Task Write Approval Granularity (QL-2)
- #۶۲.۱ — Next-Chat-Name Declaration (QL-3)
- #۸۶.۱ — Live-HEAD-Only Hash (QL-4)
- #۸۷.۱ — Manual-Box Full-Text Protocol (QL-1)

**درس‌های جدید (M106-M109):**
- M106 — Clean-Commit Pre-Stage + Untracked Audit
- M107 — Partial Manual-Box Delivery Hazard
- M108 — MCP Liveness Mid-Conversation
- M109 — Tool-Discovery-First

**سایر تغییرات:**
- §۴.۱۲ در `04_principles.md` — اصل تأیید صریح کاربر در صدر اولویت‌ها
- بانر ⚠️ FROZEN HISTORICAL REFERENCE روی `docs/HELPER_PROTOCOL.md` (QL-6)
- QL-6 در `claude_workspace/LOCKED_RULES_INBOX.md`
- header sync همه ماژول‌ها → v2.18
- bump `docs/constitution/main.md` → v2.18
- `scripts/63_pre_commit_audit.py` CURRENT_VERSION → v2.18

---

## گزینه‌های بررسی‌شده

| گزینه | توضیح | نتیجه |
|---|---|---|
| A — atomic batch | همه QL-ها در یک commit اتمیک codify شوند | ✅ انتخاب‌شده |
| B — per-rule split | هر QL جداگانه codify شود | رد — اصطکاک زیاد |
| C — فقط تبصره | QL-ها فقط تبصره روی قوانین موجود، بدون شماره جدید | رد — #89/#90 مستقل هستند |

---

## دلیل انتخاب گزینه A

QL-ها از part19 binding بودند و در LOCKED_RULES_INBOX مستند. codify رسمی اتمیک آن‌ها را در constitution مستحکم و single source of truth را حفظ می‌کند. #89/#90 قوانین بنیادی مستقل هستند (نه صرفاً تبصره) و ارزش شماره جدید دارند.

---

## نتیجه

Constitution v2.18: **90 قانون Locked، 77 درس (M1-M109)، 13 Review، 66 Decision**

**commit:** part21 atomic commit (pending در زمان نوشتن این فایل)

---

**Cross-refs:**
- `docs/constitution/01_rules.md` — #۸۹/#۹۰ + تبصره‌ها
- `docs/constitution/02_lessons.md` — M106-M109
- `docs/constitution/04_principles.md` — §۴.۱۲
- `docs/DECISIONS_LOG.md` — Decision #71
- `docs/REVIEW_LOG.md` — ردیف #013
- `claude_workspace/LOCKED_RULES_INBOX.md` — QL-0..QL-6
