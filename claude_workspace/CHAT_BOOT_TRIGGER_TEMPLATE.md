# CHAT BOOT TRIGGER TEMPLATE — Enforcement Layer

> **هدف:** source-of-truth واحد و **mandatory** برای boot هر chat جدید
> (main یا helper) پروژه trading-system.
>
> ⚠️ این فایل enforcement را تضمین می‌کند. هیچ chat نباید task شروع کند
> قبل از complete کردن boot sequence این فایل.
>
> **Created:** 2026-05-26 (helper session part09 turn ۷۹)
> **Purpose:** حل F45 + F47 + F57 (constitution bypass despite boot files read)

---

## 🚨 MANDATORY BOOT SEQUENCE (همه chat‌های جدید)

این sequence را به ترتیب کامل دنبال کن. **هیچ step نباید skip شود.**

### STEP 0 — Pre-Flight (Mechanism D)

اول `Filesystem:list_allowed_directories` را call کن.
- اگر success → ادامه به STEP 1
- اگر timeout → STOP، گزارش HM-9 به user

### STEP 1 — MANDATORY READS (به ترتیب)

این فایل‌ها را **به همین ترتیب کامل بخوان**:

1. `docs/constitution/main.md` (Constitution v2.14 index)
2. `docs/constitution/01_rules.md` (همه قواعد #1-#77)
3. `docs/constitution/02_lessons.md` (همه M-lessons + HM-lessons)
4. `docs/constitution/06_meta.md` (meta principles)
5. `docs/سند_جامع_v2_11.md` (سند جامع پروژه)
6. `docs/HELPER_PROTOCOL.md` (helper consultation protocol)
7. `docs/SESSION_STATUS.md` (state-of-record فعلی)
8. `docs/PENDING_FOR_NEXT_VERSION.md` (Z-drift + lessons pending)
9. `claude_workspace/incoming_permanent/PART{N-1}_CHAT_END_DEFERRED_NOTE.txt`
   (اگر previous chat با defer ختم شد — فعلاً PART09)
10. `claude_workspace/HELPER_SESSION_TODO_part{N-1}_final.md`
    (اگر helper session قبلی داشت — فعلاً part09)
11. `claude_workspace/incoming_permanent/PART10_BOOT_ESCAPE_NOTE.txt`
    (اگر موجود باشد)
12. `claude_workspace/incoming_permanent/PHASE1_PART{N}_HANDOFF.txt`
    (اگر موجود)

### STEP 2 — MANDATORY ACKNOWLEDGMENT

⚠️ **پس از reading، باید explicit acknowledgment بدهی شامل:**

(الف) **تأیید reading همه فایل‌های بالا** — هر فایلی که accessible
نبود، صراحتاً ذکر شود.

(ب) **explicit list قواعد critical که در این session apply می‌شوند:**

```
Universal Rules:
- L1 (Persian Language Preference): apply می‌کنم
- L2 (Anti-Circular Mechanisms A-E): self-check هر turn
- Mechanism A-E (همان L2): max 2 reversal, option frozen,
  criteria registry, tool health, termination clause

Format Rules (Constitution):
- Rule #31: نام tab + رنگ tab بالای هر کادر کد
   🟦 tab «1 backend»      (آبی)
   🟩 tab «2 scripts»      (سبز)
   🟧 tab «3 frontend»     (نارنجی)
- Rule #63: ## 🟢 ▶️ EXECUTE — اقدام لازم برای هر فرمان
- Rule #29: فایل با Artifact یا code block، نه paste متن
- Rule #59: مسیر دانلود برای هر فایل

Workflow Rules:
- Rule #48: Boot Protocol اجباری در شروع هر chat
- Rule #51: تأیید explicit user قبل از write/delete
- Rule #60: PENDING-EOC در لحظه ثبت
- W3: Chat-End File Sync Verification
- W4: No Manual File (paste-ready به user به‌جای manual)
- W5: Self-Perpetuation

Helper-Specific (اگر helper chat):
- HELPER_PROTOCOL §1-9
- HM-META-H/I/J/K
- 8-Layer Review Framework (§4)
```

(پ) **acknowledgment که هیچ task اجرا نمی‌کنی قبل از این acknowledgment**

### STEP 3 — VERIFICATION FROM USER

⚠️ پس از STEP 2 acknowledgment، **متوقف شو و منتظر تأیید user باش.**

user می‌بیند acknowledgment تو را، و اگر هر قاعده critical حذف شده،
catch می‌کند. این یک defense layer انسانی است.

اگر user OK داد → STEP 4. اگر correction خواست → ابتدا اصلاح کن.

### STEP 4 — TASK EXECUTION

فقط حالا می‌توانی به task execution بروی. هر turn:

1. شروع با `[Mechanism Self-Check]` header (A-E)
2. اگر فرمان CMD/terminal دارد → از Rule #31 + #63 conventions استفاده کن
3. paste-readyها → کادر جدا (W2)
4. در chat-end → W3 verification + W5 self-perpetuation

---

## 🚨 SECTION A — Main Chat Specific

### پس از Boot Complete

main chat می‌تواند به regular work برود:
- review پیش‌نهادها از helper chat (اگر هست)
- اجرای task‌های planned
- chat-end housekeeping با W3

### Format Rules MANDATORY

هر فرمان CMD/terminal/PowerShell:

```
## 🟢 ▶️ EXECUTE — اقدام لازم

🟩 tab «2 scripts»

```bash
[فرمان اینجا]
```
```

هیچ توضیح **داخل** code block. توضیحات **بیرون** code block.

اگر چند فرمان مستقل → چند code block جدا، هر کدام با خط tab خودش.

---

## 🚨 SECTION B — Helper Chat Specific

### پس از Boot Complete

helper chat نقش consultation است (per HELPER_PROTOCOL §1.2).

- ❌ هرگز خودش write به پروژه نمی‌کند
- ✅ فقط paste-ready به main chat می‌دهد
- ✅ 8-Layer Review Framework استفاده می‌کند

### Paste-Ready Format (W2 + #31 + #63)

```
## Paste-Ready به main chat (کادر جدا)

[اینجا content paste-ready با Rule #31 + #63 conventions]
```

---

## 🚨 SECTION C — Self-Perpetuation Rules (W5)

### قاعده SP-1: Persist همه content جدید
هر chat-end باید F-observations، rules، P{N}-CANDIDATEs را در فایل
پایدار ثبت کند.

### قاعده SP-2: Update این Template
اگر قاعده جدید universal اضافه شد، **این فایل (CHAT_BOOT_TRIGGER_TEMPLATE.md)
را به‌روز کن** قبل از push.

### قاعده SP-3: ایجاد handoff files
هر chat-end باید بسازد:
- `PART{N}_CHAT_END_NOTE.txt` یا `PHASE1_PART{N+1}_HANDOFF.txt`

### قاعده SP-4: یادآوری به chat بعد
در فایل‌های handoff، یک خط explicit:
> «Chat بعد: از CHAT_BOOT_TRIGGER_TEMPLATE.md boot کن.
> هیچ shortcut، هیچ skip، هیچ assumption.»

### قاعده SP-5: Self-Re-Read
هر chat قبل از chat-end باید این SECTION C را re-read کند.

---

## 🚨 SECTION D — Updates Log

| Date | Source | Update |
|------|--------|--------|
| 2026-05-26 | helper part09 turn ۷۹ | Initial creation با enforcement layer (حل F57) |

---

## 🚨 SECTION E — Critical Notes

⚠️ این فایل source-of-truth برای boot است. هیچ‌گاه content آن را در
chat memory reinvent نکن — همیشه از disk بخوان.

⚠️ MANDATORY BOOT SEQUENCE bypass نشود. F57 (Constitution Bypass)
نشان داد که حتی با plan خوب، assumption که "main chat قواعد را honor
خواهد کرد" نادرست است. این فایل enforcement explicit است.

⚠️ user مجاز است هر زمان catch کند که Boot Sequence ناقص است و chat
را re-boot کند.

**End of CHAT_BOOT_TRIGGER_TEMPLATE.md**
