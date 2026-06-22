# Custom Instructions — برای Project trading-system

> این متن را در Project Settings → Custom Instructions جای‌گذاری کنید.
> **مسیر در Claude Desktop:** Project → Settings → Custom Instructions
> **آخرین به‌روزرسانی:** part21 (2026-06-21) — sync با boot sequence v2.18

---

## متن Custom Instructions (کپی این بخش):

```
من روی پروژه trading-system (D:\Projects\trading-system) کار می‌کنم.

Stack: FastAPI + SQLAlchemy + React 19.2 + Vite، Windows 11، PowerShell.
زبان ارتباط: فارسی، اصطلاحات فنی انگلیسی.
Filesystem MCP فعال است.

پروتکل اجباری شروع هر چت (Rule #48 — v2.18):
با Filesystem MCP این فایل‌ها را به ترتیب بخوان:
1. claude_workspace/CHAT_BOOT_TRIGGER_TEMPLATE.md  (STEP 0→4)
2. claude_workspace/PHASE_LEDGER.md
3. docs/constitution/main.md  (index v2.18)
4. docs/constitution/01a_rules_core.md  (جدول #1-90 — boot-critical)
5. claude_workspace/LOCKED_RULES_INBOX.md  (QL-0..QL-6 binding)
6. docs/constitution/02_lessons.md  (M1-M110)
7. docs/constitution/06_meta.md
8. docs/SESSION_STATUS.md
9. docs/PENDING_FOR_NEXT_VERSION.md
10. claude_workspace/incoming_permanent/PHASE1_PART{N}_HANDOFF.txt

قوانین کلیدی:
- هر فایلی که می‌سازی یا ویرایش می‌کنی فوراً در FILE CHANGES LOG handoff ثبت کن
- git add -A ممنوع — فقط فایل‌های مشخص add شوند
- هش commit فقط از git rev-parse --short HEAD زنده (QL-4)
- shell = PowerShell (نه CMD-only cmdlets)
- تأیید صریح کاربر قبل از هر write/delete (Rule #51)
```

---

## یادداشت نگهداری

این فایل snapshot از متن Custom Instructions است.
هر بار که boot sequence یا قوانین کلیدی تغییر کردند، این فایل باید sync شود (Rule #87 — Materiality Threshold).

**نسخه constitution:** v2.18
**فایل مرجع:** `docs/constitution/main.md` بخش Quick-start
