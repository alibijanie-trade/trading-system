# ماژول ۰۶ — Meta (Session/Templates/Tooling)

> بخشی از **Constitution v2.18 (Modular)** — [بازگشت به main](./main.md)
>
> **محتوا:** Session/Context + Chat Handoff + Templates پاسخ + Claude MAX + Pre-commit + GitHub + Filesystem MCP + Claude Desktop + claude_workspace + Skills
> **منبع v2.11:** سند ۱۳ + ۱۴ + ۱۵ + ۱۶ + ۱۷ + ۱۹ + ۲۰ + ۲۱ + ۲۲ + ۲۳ + ۲۴ + ۲۵ (۱۲ سند)
> **Created in commit:** `<git log --diff-filter=A --oneline -- docs/constitution/06_meta.md>` (migrate سند ۱۳-۲۵ → 06_meta، commit 7/8؛ هش از git مشتق شود — نه hardcode در ماژول، per #۸۶/check_5)

---

## ۶.۱ Session Management

### ساختار SESSION_STATUS.md

این فایل **پویا** است و باید پس از هر گام به‌روز شود. هدف: هر مکالمه جدید Claude باید بداند پروژه دقیقاً تا کجا پیش رفته.

```markdown
# Session Status — [تاریخ]

## وضعیت کلی
- فاز جاری: ...
- Tier جاری: ...
- نسخه پروژه: ...
- Git HEAD: <placeholder یا git log -1>
- چت بعدی پیشنهادی: ...

## فاز X — وضعیت
✅ DONE / ⏳ TODO

## آمار نهایی پروژه
- قوانین Locked: N
- درس‌نامه: M
- چت‌های کامل: K
- Tests: pass count
- Backlog: N/M DONE
- PENDING: K آیتم

## محیط فعال
Python + FastAPI + ...

## فایل‌های مهم تولید/به‌روز شده در این چت
[لیست]

## Bug ها در این چت
[لیست]

## PENDING برای نسخه بعدی
[لیست]

## اولین گام‌های چت بعدی
...
```

### ساختار PROJECT_CONTEXT.md

این فایل **ثابت‌تر** است (تغییرات کم) و Context کلی پروژه را نگه می‌دارد:

```markdown
# Context پروژه — سامانه هوشمند ترید

## Stack فعال
Backend + Frontend + DB

## مسیرها
Root: D:\Projects\trading-system

## قوانین کلیدی (subset از سند جامع)
- BrowserRouter فقط در main.jsx
- ...

## CMDها / Tab‌ها
🟦 1 backend | 🟩 2 scripts | 🟧 3 frontend | 🟥 4 BACKUP

## تصمیمات معماری تأییدشده
[لیست همه Decisions از DECISIONS_LOG]
```

### ساختار CHAT_LOG.md

تاریخچه هر چت با template ثابت:

```markdown
## چت N — TRADING-phase{P}-part{NN}-{topic}

**تاریخ:** YYYY-MM-DD
**Duration:** ~X ساعت
**Tier:** ...
**فاز:** ...

### دستاوردها
- ✅ ...

### تصمیمات گرفته‌شده
- #N: ...

### Bug ها
- #N: ...

### درس‌های آموخته
- M{N}: ...

### Commits
- HASH عنوان

### فایل‌های تولیدشده
- مسیر/نام

### گام بعدی
...
```

### پروتکل شروع چت (قانون #۴۸)

طبق Modular Constitution v2.12، ترتیب الزامی خواندن:

1. **`docs/constitution/main.md`** (~۸KB، index)
2. **`docs/constitution/04_principles.md`** (~۱۵KB، فلسفه)
3. **`docs/constitution/01_rules.md`** (~۳۰KB، قوانین Locked)
4. **`docs/constitution/02_lessons.md`** (~۲۹KB، درس‌نامه)
5. **`docs/PENDING_FOR_NEXT_VERSION.md`** (PENDING آیتم‌ها)
6. **`docs/SESSION_STATUS.md`** (وضعیت فعلی)
7. **`docs/DECISIONS_LOG.md`** (تصمیمات معماری)
8. **`docs/CHAT_LOG.md`** بخش چت قبل
9. **اجرای M73 audit** — cross-document consistency check

سایر ماژول‌ها (`03_bugs.md`, `05_architecture.md`, `06_meta.md`) **on-demand** خوانده می‌شوند.

### پروتکل پایان چت (۱۲ مرحله، قانون #۲۷)

🔒 Claude **هرگز** خودکار شروع نمی‌کند. منتظر علائم صریح:
- «چت رو ببند»
- «end of chat»
- «zip نهایی بساز و چت رو ببند»

۱۲ مرحله پایان:
1. جمع‌بندی کارهای انجام‌شده
2. به‌روزرسانی CHAT_LOG.md (افزودن بخش جدید)
3. به‌روزرسانی TASK_BACKLOG.md
4. به‌روزرسانی DECISIONS_LOG.md (اگر تصمیم جدید)
5. به‌روزرسانی TROUBLESHOOTING.md (اگر Bug جدید)
6. به‌روزرسانی GLOSSARY.md (اگر اصطلاح جدید)
7. به‌روزرسانی STYLE_GUIDE.md (اگر pattern جدید)
8. به‌روزرسانی SESSION_STATUS.md
9. به‌روزرسانی PROJECT_CONTEXT.md
10. به‌روزرسانی CHANGELOG.md (اگر version bump)
11. به‌روزرسانی سند جامع/Constitution (افزایش version + change log)
12. ساخت **CHAT{N+1}_HANDOFF.txt** (قانون #۶۲) + پیام پایانی + push روی GitHub (قانون #۶۶ — Locked در v2.12)

---

## ۶.۲ Chat Handoff Protocol (سند ۱۴ منبع)

### شرایط فعال‌سازی

🔒 Claude باید **خودش به ابتکار خود** پروتکل را در یکی از موارد زیر پیشنهاد دهد:

**سناریو الف — افت کیفیت:**
- چت طولانی شده و سرعت محسوس کاهش یافته
- کیفیت ارائه افت کرده
- نزدیک شدن به محدودیت Context Window
- خطر فراموشی تصمیمات قبلی

**سناریو ب — پایان طبیعی چت:**
- علائم متنی فارسی: «تمام می‌کنم» / «خداحافظ» / «برای امروز کافی است» / «چت را می‌بندم» / «استراحت می‌کنم» / «فردا ادامه می‌دهیم» / «دیگه کافیه»
- علائم متنی انگلیسی: "bye" / "goodbye" / "done for today" / "see you later" / "closing chat" / "that's enough for now"

### ۷ مرحله اجباری

🔒 پس از تأیید کاربر، Claude **هفت مرحله** را با وسواس انجام می‌دهد:

| مرحله | اقدام |
|---|---|
| ۱ | پیشنهاد و اخذ تأیید صریح |
| ۲ | تولید SESSION_STATUS.md کامل (Artifact) |
| ۳ | تولید PROJECT_CONTEXT.md به‌روز (Artifact) |
| ۴ | تولید سند جامع/Constitution به‌روزشده با نسخه جدید |
| ۵ | یادآوری نیازمندی‌های چت جدید (لیست فایل‌ها) |
| ۶ | نکات افزایشی برای حداکثر هماهنگی |
| ۷ | پیام پایانی صریح با ساختار `در چت جدید این موارد را آپلود کن: ...` |

### قوانین قفل‌شده Handoff

🔒 سه فایل خروجی (SESSION_STATUS، PROJECT_CONTEXT، سند جامع) باید همگی Artifact قابل دانلود باشند — نه متن داخل چت.
🔒 سند جامع جدید باید تضمین کند هیچ بخش قبلی حذف نشده (#۲۴).
🔒 اگر چت جاری شامل تصمیمات تأییدشده‌ای است که هنوز در اسناد نیستند، اول آن‌ها را در PROJECT_CONTEXT/Constitution ثبت کن، **سپس** فایل‌ها را تولید کن.

### رفتار اجباری در تشخیص علائم پایان طبیعی

🔒 وقتی یکی از علائم تشخیص داده شد، **قبل از پاسخ خداحافظی نهایی**، Claude باید بپرسد:

> «آیا می‌خواهید قبل از بستن چت، اسکریپت آپدیت `SESSION_STATUS.md` و `PROJECT_CONTEXT.md` را بسازم؟»

🔒 Claude **هرگز** بدون پرسش صریح و گرفتن تأیید، فایل‌ها را نسازد.

### استثنا

اگر کاربر از همان ابتدای پیامش صریحاً گفت «اسکریپت پایان چت را بساز»، Claude مستقیماً مراحل ۲-۷ را اجرا می‌کند بدون پرسش.

---

## ۶.۳ Templates پاسخ Claude (سند ۱۷ منبع، ۱۲ Template)

### Template ۱ — اولین پاسخ در هر چت

```markdown
سلام! بررسی فایل‌ها انجام شد.

## 📍 وضعیت فعلی پروژه
- فاز: [N]
- پیشرفت: [%]
- آخرین چت: [نام]
- آخرین کار: [خلاصه]

## 🔍 محیط
| چک | وضعیت |
|---|---|
| backend/venv | ✅/❌ |
| backend/trading.db | ✅/❌ |
| frontend/node_modules | ✅/❌ |

## 📚 خوانده‌شده
- [x] main.md
- [x] 04_principles.md
- [x] 01_rules.md
- [x] 02_lessons.md
- [x] PENDING_FOR_NEXT_VERSION
- [x] SESSION_STATUS
- [x] CHAT_LOG

## 📋 Tasks باز در Tier فعلی
- [ ] Task A
- [ ] Task B

## 🚀 گزینه‌های گام بعدی
الف) ...
ب) ...

منتظر انتخاب شما هستم.
```

### Template ۲ — پاسخ به "ادامه بده"

از TASK_BACKLOG.md گام بعدی پیشنهادی استخراج، با اولویت + تخمین + prerequisites.

### Template ۳ — اعلام Bug

```markdown
🐛 **Bug تشخیص داده شد**

### علائم
[چه چیزی دیده شد]

### علت ریشه‌ای
[چرا]

### راه‌حل پیشنهادی
- اسکریپت fix: `scripts/{N}b_fix_*.py`
- ثبت در 03_bugs.md به‌عنوان Bug #N

اسکریپت fix را الان بسازم؟
```

### Template ۴ — اعلام تصمیم معماری لازم

با ۲-۳ گزینه + مزیت/منفی هر کدام + پیشنهاد Claude با ⭐ (قانون #۶۱).

### Template ۵ — پایان چت

شامل کارهای انجام‌شده، فایل‌های تولیدشده، TASKها DONE، Bug ها رفع‌شده، تصمیمات گرفته‌شده، نام چت فعلی، نام پیشنهادی چت بعد، ZIP نهایی.

### Template ۶ — اعتراف اشتباه

```markdown
متشکرم که اشاره کردید. شما درست می‌گویید.

## آنچه اشتباه بود
[توضیح صادقانه]

## چه باید کنیم
1. [اصلاح]
2. [اصلاح]

شروع کنم؟
```

⚠️ Claude **هرگز** دفاع نمی‌کند یا توجیه نمی‌آورد. اول اعتراف، بعد اصلاح.

### Template ۷ — هشدار context اشباع

```markdown
⚠️ **هشدار: کیفیت ممکن است افت کند**

context چت در حال نزدیک شدن به اشباع است.

پیشنهاد:
1. شروع Protocol پایان چت (فاز ۳)
2. حفظ کیفیت اسناد نهایی
3. ادامه در چت جدید با اسناد به‌روز

موافقید؟
```

### Template ۸ — ابهام در درخواست

```markdown
درخواست شما می‌تواند به ۲ شکل تفسیر شود:

**تفسیر A:** [...]
**تفسیر B:** [...]

کدام را در نظر دارید؟ (یا تفسیر سوم؟)
```

⚠️ Claude **هرگز فرض نمی‌کند**. ابهام = پرسش.

### Template ۹ — تحویل اسکریپت

```markdown
## 📦 اسکریپت {N}_{name}.py + {N}b_test_{name}.py

### چه می‌کند
[۱-۳ خط]

## 🟢 ▶️ EXECUTE — اقدام لازم

🟩 tab «۲ scripts»:
```cmd
python scripts/{N}_{name}.py
python scripts/{N}b_test_{name}.py
```

### خروجی مورد انتظار
- ...

### چک بصری (در 🟧 tab «۳ frontend»)
- ...
```

### Template ۱۰ — E1 افت کیفیت

```markdown
🚨 **هشدار E1 — افت کیفیت تشخیص داده شد**

نشانه‌ها:
- [...]

پیشنهاد فوری: شروع Protocol پایان چت بدون اتمام کار جاری.

این کار را انجام دهم؟
```

---

### Template ۱۱ — Pre-Action Checklist Visibility 🆕 v2.14

> پشتیبان: Rule #۷۶ (Pre-Action Checklist Visibility) + M100 (Hidden-Checklist Completion). انجام check های pre-action با explicit visibility در chat surface.

#### قالب bullet list (ساده)

```markdown
## 📋 Pre-Action Checklist — [نام task]

**Stage:** S{N}.{M} | **Severity:** [critical/high/medium/low]

- ✅ Check 1: [توضیح] — [reasoning]
- ✅ Check 2: [توضیح] — [reasoning]
- ⏸ Check 3: [توضیح] — [reasoning، skip causality]
- ❌ Check 4: [توضیح] — [reasoning، fail causality + recovery]

**نتیجه:** [proceed / pause for clarification / abort]
```

#### قالب table (پیچیده‌تر، با Note)

```markdown
## 📋 Pre-Add Checklist — [task]

| # | Check | Result | Note |
|---|---|---|---|
| ۱ | Tier classification valid؟ | ✅ | T1 governance per Rule #۶۸ |
| ۲ | Path validator؟ | ✅ | همه refs valid (manual pre-D19) |
| ۳ | Atomic boundary respected؟ | ✅ | M93 Triple-Rule scope clear |
| ۴ | Z-ID permanence؟ | ✅ | permanent IDs used (Rule #۷۴) |
| ... | ... | ... | ... |

**Verdict:** PROCEED (همه N check pass) / PAUSE (X check pending) / ABORT (Y check fail)
```

#### نمونه‌های مرجع

- `docs/PRE_ADD_CHECKLIST.md` §۵ Examples 1-3 (نمونه‌های اجرایی)
- `docs/HELPER_PROTOCOL.md` §۷ Upfront Constraint Checklist Pattern (تطبیق‌یافته برای helper drafting)

#### کاربرد

- قبل از write به T1 file → mandatory
- قبل از atomic commit → recommended
- قبل از boundary decisions (scope change، tier reclass، naming change) → mandatory
- mental checking ممنوع — partner (انسان یا future audit) باید visible verification را cross-check کند

---

### Template ۱۲ — Git Commit -F Flag Standard 🆕 v2.14

> پشتیبان: M99 (CMD Long-Command Paste-Break) + M95 + M97. standard pattern برای commit messages > 2-3 lines. Cross-refs قوانین #۴۲/#۴۳/#۶۶.

#### Workflow

```cmd
# 1. ساخت فایل commit message (Claude tools در Phase 1):
#    claude_workspace/commit_msg_{stage}.txt

# 2. user execute (after Phase 1 complete):
git add <staged-files>
git commit -F claude_workspace/commit_msg_{stage}.txt
git push origin <branch-name>
```

#### Requirements فایل commit message

🔒 **ASCII-only:** هیچ non-ASCII char (em-dash، Persian text، special quotes). M95+M97 enforced.
چرا؟ CMD cp1252 + utf-8 mismatch + quote tracking fragility → silent file corruption (M97 evidence).

🔒 **Location:** `claude_workspace/` (T5 workspace، نه T1).

🔒 **Naming:** `commit_msg_{stage_id}.txt`:
- `commit_msg_s3_1.txt` (sub-stage)
- `commit_msg_chat_end_part07.txt` (chat-end)
- `commit_msg_d24_chat_end.txt` (parallel deliverable)

🔒 **Preservation:** پس از commit، فایل **delete نشود** per Z3.18/Z3.23 policy (consumed by -F، نه committed). historical reference برای audit.

#### قالب standard commit message

```
{type}({scope}): {subject ≤72 chars ASCII}

{paragraph 1: high-level description, ≤80 chars per line ASCII}

Scope ({M98 closure}):
- {bullet 1}
- {bullet 2}

Out of scope (defer):
- {item} ({future stage})

{additional context paragraphs, ASCII only}

Refs: {M-N, Rule #N, HM-N, Decision #N, Z-N}
```

#### مثال‌های مرجع

- `claude_workspace/commit_msg_s3_1.txt` (S3.1 atomic — اولین نمونه post-D24 standard)
- `claude_workspace/commit_msg_d24_chat_end.txt` (D24 chat-end)
- `claude_workspace/commit_msg_s3_0_5.txt` (part05 S3.0.5 cleanup)

#### استثنا (inline -m مجاز)

برای commits کوتاه (≤2 خط، single-purpose mini-commit مثل cosmetic fix):

```cmd
git commit -m "fix(meta): typo correction"
```

inline -m flag OK برای این موارد. -F flag برای commits با subject + body + scope/refs.

#### قوانین مرتبط

- **Rule #۴۲:** `--no-verify` با `[skip-hooks: REASON]` (متمم — موارد bypass)
- **Rule #۴۳:** Hybrid hook mode (critical اجباری، minor warning)
- **Rule #۶۶:** Push اجباری در پایان هر چت (متمم — هر commit message file که -F شد، push هم هست)
- **Rule #۷۶:** Pre-Action Checklist Visibility (Template 11) — اعمال قبل از commit

#### EXECUTE multi-command paste (M105 — 🆕 v2.17)

برای EXECUTE block‌هایی که چند دستور دارند، دستورهای کوتاه/مرتبط باید با `&` در **یک خط** زنجیر شوند تا با یک paste + یک Enter پشت‌سرهم اجرا شوند (CMD خطوط جدا را وسط زنجیره متوقف می‌کند). الگو: `cd /d <root> & echo [1] & <cmd1> & echo [2] & <cmd2> & echo [DONE]`. جزئیات: `02_lessons.md` M105.

---

## ۶.۴ Claude MAX Real-Time (سند ۱۹ منبع)

### محدودیت مهم

Claude **نمی‌تواند** به‌جای کاربر تنظیمات Settings را تغییر دهد. این بخش فقط راهنمایی می‌کند.

### انتخاب Model بر اساس فاز

| فاز / موقعیت | Model | Adaptive Thinking | علت |
|---|---|---|---|
| Atomic End-of-Chat | **Opus 4.7** | ON | manipulation همزمان چند سند |
| Tier 2 Quality Hardening | Sonnet 4.6 | ON | سرعت + کیفیت کافی |
| فاز ۱ — Repository Layer | Sonnet 4.6 | ON | CRUD ساده |
| فاز ۲ — Indicators (RSI/MACD) | **Opus 4.7** | ON | منطق ریاضی |
| فاز ۳ — Trading Strategies | **Opus 4.7** | ON | الگوریتم پیچیده |
| فاز ۴ — UI Components | Sonnet 4.6 | OFF | template-heavy |
| Debugging پیچیده | **Opus 4.7** | ON | reasoning عمیق |
| Refactoring بزرگ | **Opus 4.7** | ON | حفظ ثبات معماری |
| Documentation روتین | Sonnet 4.6 | OFF | سریع کافی |
| Code review | **Opus 4.7** | ON | تشخیص anti-patterns |

**قانون عملی:** اگر ≥۳ مورد از این‌ها → **Opus**: چند فایل همزمان، منطق پیچیده، edge case های زیاد، decision معماری، debugging طولانی، reasoning زنجیره‌ای.

### تنظیمات Settings پیشنهادی (Max 5x)

| Setting | حالت |
|---|---|
| Artifacts | ✅ ON |
| Analysis tool | ✅ ON |
| Extended thinking | ✅ ON |
| File creation | ✅ ON |
| Web search | ✅ ON |
| Memory | ✅ ON |
| Custom instructions | ✅ پر کنید |
| GitHub Connector | بعد از setup repo |

### Custom Instructions پیشنهادی

```
من روی پروژه trading-system (D:\Projects\trading-system) کار می‌کنم.
Stack: FastAPI + SQLAlchemy + React + Vite، Windows 11.
زبان ارتباط: فارسی، اصطلاحات فنی انگلیسی.
من دانش برنامه‌نویسی ندارم — هر کار مرحله‌به‌مرحله.

قوانین قفل‌شده مهم (نسخه v2.14):
- #۲۷: پایان چت فقط با تأیید صریح
- #۳۰: اصلاحات کوچک = اسکریپت Python idempotent (یا MCP edit_file)
- #۳۱: بالای هر کادر کد: 🟦/🟩/🟧/🟥 + شماره tab
- #۴۶: ASCII-only در print() اسکریپت‌های Windows
- #۵۹: بلااستثنا اعلام مسیر دانلود
- #۶۰: PENDING-EOC در لحظه ثبت
- #۶۱: پیشنهاد مطلوب صریح
- #۶۲: handoff فایل دائمی با prefix ها
- #۶۳: Convention 🟢 ▶️ EXECUTE
- #۶۶: Push اجباری در پایان چت (Locked در v2.12)

مرجع کامل: docs/constitution/main.md (Modular v2.14)
```

### پروتکل توصیه Real-Time

در شروع مرحله جدید:

```markdown
🤖 **توصیه Claude MAX برای [مرحله]:**
- Model: [Opus 4.7 / Sonnet 4.6]
- Adaptive Thinking: [ON / OFF]
- علت: [توضیح ۱-۲ خط]
- آیا تأیید می‌کنید؟
```

---

## ۶.۵ Pre-commit Hooks (سند ۲۰ منبع)

### فلسفه Hybrid mode (انتخاب پروژه)

| Hook | حالت | چرا |
|---|---|---|
| trailing-whitespace, end-of-file-fixer, check-yaml, check-json | 🔴 اجباری (auto-fix) | استاندارد عمومی |
| black, isort | 🔴 اجباری (auto-fix) | یکنواختی Python |
| check-anti-patterns A1, A4, A8, A10 | 🔴 اجباری | security/bug-prone |
| check-anti-patterns A6 (print) | 🟡 warning | dev موقت |
| pytest-unit, vitest | حذف از pre-commit | کند، به pre-push منتقل |

### Bypass در اضطرار (قانون #۴۲)

```bash
git commit --no-verify -m "[skip-hooks: REASON] ..."
```

**موارد قابل قبول:**
- Hook خود bug دارد
- Migration حساس
- WIP موقت قبل از merge

**موارد غیرقابل قبول:**
- «hook کنده، صبر ندارم»
- «A1 violation است ولی موقتی»

### Mass Reformat اولیه

اولین اجرای hooks در پروژه legacy، انبوه فایل را reformat می‌کند (در چت ۷، ۷۸ فایل + ۶۰ CRLF). طبیعی است:

```bash
pre-commit run --all-files
git add -A
git commit --no-verify -m "style: apply black/isort to legacy files [skip-hooks: mass-format]"
```

---

## ۶.۶ GitHub Integration (سند ۲۱ منبع + قانون #۶۶ Locked در v2.12)

### چرا اول پروژه؟

- Backup remote (در صورت crash hard disk)
- Time-machine کامل کد
- آمادگی برای CI/CD آینده
- آمادگی برای collaboration

### چک‌لیست استاندارد (۵ مرحله)

**مرحله ۱ — ایجاد repository در GitHub**
- New repository → نام: `trading-system`
- Private (تا فاز ۴)
- بدون README/license/.gitignore (از قبل داریم)

**مرحله ۲ — تأیید `.gitignore` شامل secrets**
```bash
findstr "\.env" .gitignore
```

**مرحله ۳ — اتصال local به remote**
```bash
cd D:\Projects\trading-system
git remote add origin git@github.com:USERNAME/trading-system.git  # SSH
# یا: git remote add origin https://github.com/USERNAME/trading-system.git  # HTTPS
git branch -M main
git push -u origin main
```

**مرحله ۴ — Authentication**

*گزینه ۱ — Personal Access Token (ساده‌تر):*
- GitHub Settings → Developer settings → PAT (Classic)
- Scope: `repo`
- اولین `git push` username + token می‌خواهد

*گزینه ۲ — SSH key (امن‌تر، توصیه برای استفاده مکرر):*
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
type %USERPROFILE%\.ssh\id_ed25519.pub
```
سپس public key را در GitHub Settings → SSH and GPG keys اضافه کن.

**مرحله ۵ — تأیید push موفق**
```bash
git status
git log --oneline -5
```

### Best Practices

- **هرگز** `.env` را commit نکنید
- **هرگز** API keys را در commit بگذارید
- از **branch protection** برای `main` در GitHub Settings استفاده کنید (آینده)
- **regular push** — هر چند commit یک‌بار push

### قانون #۶۶ Locked در v2.12 ⭐⭐⭐

🔒 **Push اجباری در پایان هر چت:**

```bash
git add .
git commit -m "..."
git push origin <branch>
```

**استدلال:**
- Backup فوری
- جلوگیری از گم شدن کار با crash
- Sync بین local و remote
- Time-machine کامل

**در branch های infra/** (مثل `infra/governance-overhaul`): push بعد از هر commit جزئی، نه فقط پایان چت — برای granularity بالا.

---

## ۶.۷ Filesystem MCP (سند ۲۲ منبع)

### چیست و چرا؟

Filesystem MCP یک extension برای Claude Desktop است که به Claude اجازه می‌دهد مستقیماً با فایل‌سیستم کاربر تعامل کند — خواندن، نوشتن، edit، list، جستجو.

**مزایا:**
- متن handoff شروع چت کوتاه می‌شود (قانون #۵۰)
- Claude می‌تواند فایل‌ها را مستقیم بخواند و ویرایش کند
- اصلاحات کوچک با `edit_file` بدون اسکریپت Python ممکن است
- read-back verify سریع و خودکار (قانون #۳۷)
- ثبت لحظه‌ای PENDING-EOC (قانون #۶۰)

### Tools موجود

| دسته | Tool | تأیید؟ |
|---|---|---|
| read | `list_allowed_directories` | ❌ |
| read | `list_directory` / `list_directory_with_sizes` / `directory_tree` | ❌ |
| read | `read_text_file` (با head/tail/view_range) | ❌ |
| read | `read_multiple_files` | ❌ |
| read | `get_file_info` | ❌ |
| read | `search_files` | ❌ |
| write | `write_file` | ✅ تأیید |
| write | `edit_file` (با git-style diff + dryRun) | ✅ تأیید |
| write | `create_directory` | ✅ تأیید |
| write | `move_file` | ✅ تأیید |
| write | `copy_file_user_to_claude` | ✅ تأیید |

### Permissions Setup (قانون #۴۹)

در Claude Desktop → Settings → Connectors → Filesystem MCP:
- **Always Allow:** همه read-only tools
- **Needs Approval:** همه write/delete/copy
- **پوشه مجاز:** فقط `D:\Projects\trading-system` (و subdir‌ها)
- **محدودیت‌ها:** هرگز `.env` تغییر، هرگز خارج پروژه، هرگز سیستمی

### Workflow عملی (M61 — Full Safety Cycle)

```
1. Preview ساختار قبل از write   (M60)
2. درخواست تأیید از کاربر         (قانون #۵۱)
3. اجرای write_file یا edit_file
4. read-back verify فایل           (قانون #۳۷، M61، M82)
5. گزارش به کاربر                  (قانون #۵۹: مسیر صریح)
```

برای `edit_file`: همیشه `dryRun: true` اول → نمایش diff → تأیید → `dryRun: false`.

### استثنائات و توصیه‌ها

- **MCP در چت جاری load نمی‌شود (M30):** اگر در همین چت MCP فعال شد، در همین چت کار نمی‌کند. باید چت جدید باز شود.
- **مسیر تحویل صریح (قانون #۵۹):** بعد از هر write، مسیر فایل اعلام شود.
- **`.env` ممنوع:** حتی اگر کاربر بخواهد. به‌جای آن، اسکریپت Python idempotent.
- **حجم فایل (M66):** فایل‌های بزرگ‌تر از ~۲۰۰KB با MCP کند هستند. برای فایل‌های بزرگ، اسکریپت Python بهتر است.

### Troubleshooting (شامل M83)

| مشکل | علت | راه‌حل |
|---|---|---|
| `Path not allowed` | پوشه در permissions نیست | بررسی `list_allowed_directories` |
| `Empty edits array applied diff` | bug احتمالی MCP | با `read_text_file` verify کن — معمولاً edit واقعاً اعمال شده |
| `edit_file` با match نشدن `oldText` | encoding/whitespace/فارسی | اول `read_text_file` با `view_range` کن، سپس exact copy |
| فایل‌های فارسی نام | path encoding | همیشه با `\` و نام exact (بدون normalize) |
| Tool timeout / hang | transient MCP bug | **M83**: Retry First — قبل از rename یا restructure، retry کن |

---

## ۶.۸ Claude Desktop Configuration (سند ۲۳ منبع)

### Memory Toggles

در **Settings → Capabilities → Memory** (نه Profile، اصلاحیه v2.11):

| Toggle | حالت | اثر |
|---|---|---|
| Search and reference chats | ✅ ON | جستجوی مفهومی در چت‌های قبلی این Project |
| Generate memory from chat history | ✅ ON | Claude خودش memory می‌سازد |
| Import memory from other AI providers | (اختیاری) | import از ChatGPT/Gemini |
| Chat memory (نمایش) | — | چه memory ای ذخیره است |

⚠️ **هشدار:** Memory **جایگزین** فایل نیست. Memory برای جستجوی مفهومی خوب است، نه ثبت دقیق (M56). برای ثبت دقیق، همیشه از فایل استفاده شود.

### Project Knowledge

محتوای پیشنهادی برای trading-system:
- `PROJECT_KNOWLEDGE.md` (~۳-۵K کلمه) شامل:
  - معرفی پروژه
  - Stack (سند ۲ خلاصه)
  - فاز جاری + درصد
  - قوانین Locked مهم (subset از `01_rules.md`)
  - مسیر فایل‌های مرجع

**به‌روزرسانی:**
- پایان هر چت، Claude نسخه به‌روز را تولید (قانون #۵۵)
- کاربر در Project Knowledge جایگزین می‌کند
- snapshot در `claude_workspace/snapshots/` (قانون #۵۸)

> 🆕 v2.17 (قانون #۸۷): سه target خارج‌از‌MCP که فقط کاربر دستی تغییر می‌دهد (Settings→General Instructions، Project Instructions box، Project Knowledge files) باید هنگام هر تغییر **material** با یادآوری صریح + گرفتن تأیید انجام sync شوند (Materiality Threshold — برای تغییرات non-material یادآوری نده). همچنین هر artifact نوشتاری پروژه طبق ۸ معیار AI-Optimized Authoring (قانون #۸۸) نوشته شود. شرح کامل: `01_rules.md` بخش «شرح کامل قوانین Sync & Authoring (#۸۷-۸۸)».

### Settings → Capabilities & Feature Preview

> 🆕 v2.11 (C1.1): جدول بر اساس Settings audit واقعی در چت ۸ بازنگری شد.

| Setting | حالت پیشنهادی | علت |
|---|---|---|
| Search and reference chats | ✅ ON | جستجوی مفهومی |
| Generate memory from chat history | ✅ ON | حافظه پروژه |
| **Connector discovery** | ✅ OFF | امن‌تر — connector ها آگاهانه فعال |
| Artifacts | ✅ ON | تحویل فایل/code block |
| **AI-powered artifacts** | ✅ OFF | در فاز ۰ لازم نیست |
| Inline visualizations | ✅ ON | Mermaid diagrams |
| Cloud code execution | ✅ ON | sandbox Python |
| Allow network egress | ✅ ON | برای pip/npm/httpx |
| **Domain allowlist** | Package managers only | امن‌ترین |
| Extended thinking | ✅ ON | Opus reasoning |
| File creation | ✅ ON | docx/pdf/xlsx |
| Web search | ✅ ON | docs به‌روز |

### Settings → Connectors

| Connector | حالت |
|---|---|
| **Filesystem (MCP)** | ✅ ON با تنظیمات سند ۶.۷ |
| GitHub | ✅ ON بعد از سند ۶.۶ |
| Google Drive | ❌ OFF |
| Slack/Notion | ❌ OFF |

### Audit Settings در هر شروع چت

طبق قانون #۴۸:
- Filesystem MCP در دسترس؟ (تست با `list_allowed_directories`)
- Project Knowledge آپدیت است؟
- Memory toggles فعال؟

---

## ۶.۹ claude_workspace Structure (سند ۲۴ منبع)

### ساختار ۵-پوشه

```
D:\Projects\trading-system\claude_workspace\
├── incoming_permanent\    ← فایل‌های دریافتی دائم از کاربر
│   ├── CHAT{N}_HANDOFF.txt  ← فایل handoff (قانون #۶۲)
│   └── .gitkeep
├── old_versions\          ← نسخه‌های قدیمی فایل‌ها
│   └── .gitkeep
├── screenshots\           ← screenshots آپلودی (قانون #۵۷)
│   └── .gitkeep
├── snapshots\             ← snapshot های Project Knowledge (قانون #۵۸)
│   └── .gitkeep
└── zip_temp\              ← zip های موقت
    └── .gitkeep
```

### وظیفه هر پوشه

| پوشه | کاربرد | git |
|---|---|---|
| `incoming_permanent/` | فایل‌های دائم (Excel ورودی، logo، assets، **HANDOFF ها**) | tracked |
| `old_versions/` | نسخه‌های قدیمی قبل از حذف (تاریخ‌بندی) | tracked |
| `screenshots/` | screenshots دیباگ/توضیح | **gitignored** |
| `snapshots/` | snapshot های Project Knowledge با timestamp | tracked برای تاریخچه |
| `zip_temp/` | zip های موقت | **gitignored** |

### Policy `.gitignore`

```gitignore
# claude_workspace policy
claude_workspace/screenshots/*
!claude_workspace/screenshots/.gitkeep
claude_workspace/zip_temp/*
!claude_workspace/zip_temp/.gitkeep
```

### Naming Convention

| پوشه | فرمت |
|---|---|
| screenshots | `{YYYY-MM-DD}-{description-kebab}.png` |
| snapshots | `{YYYY-MM-DD}-{filename}.md` |
| old_versions | `{YYYY-MM-DD}-{original-name}.{ext}` |
| zip_temp | `{date}-{topic}.zip` |
| handoffs | `CHAT{N}_HANDOFF.txt` |

---

## ۶.۱۰ Skills اختصاصی پروژه (سند ۲۵ منبع، placeholder)

### Skills چیست؟

قابلیت Claude برای ساخت template/دستورالعمل reusable برای task‌های تکراری.

### Skills رسمی فعال

| Skill | کاربرد |
|---|---|
| `docx` | ساخت/خواندن Word |
| `xlsx` | Spreadsheet |
| `pptx` | Slide |
| `pdf` | PDF |
| `frontend-design` | React/Vue UI |
| `file-reading` | مسیریابی فایل |
| `pdf-reading` | خواندن PDF |
| `skill-creator` | meta — ساخت skill جدید |
| `product-self-knowledge` | اطلاعات محصولات Anthropic |

### Skills اختصاصی آینده

| Skill | کاربرد | اولویت |
|---|---|---|
| **trading-script-generator** | تولید اسکریپت `{N}_*.py` + test همراه | بالا |
| **trading-migration-helper** | تولید Alembic migration Up/Down | متوسط |
| **trading-component-generator** | تولید React component با theme + RTL | متوسط |
| **trading-test-runner** | اجرای pytest + vitest با report | پایین |
| **trading-endof-chat** | اجرای ۱۲ مرحله پایان چت | بالا |

### زمان ساخت

- **اولین Skill (`trading-endof-chat`):** پس از تثبیت ساختار modular constitution
- **دومین Skill (`trading-script-generator`):** اوایل فاز ۲ — pattern تثبیت‌شده
- **بقیه:** به‌مرور با کشف نیاز

### ساختار Skill

```
skills/trading-{name}/
├── SKILL.md          ← دستورالعمل اصلی
├── examples/         ← مثال‌های use case
└── templates/        ← قالب‌های reusable
```

### پروتکل ساخت

1. تشخیص task تکراری
2. اعلام به کاربر: «این task تکراری است — Skill می‌سازم؟»
3. در صورت تأیید، Skill با `skill-creator` ساخته شود
4. ثبت در این بخش (به‌روزرسانی جدول)
5. اعمال در چت‌های بعد

---

## ۶.۱۱ راهنمای تکامل پروژه — جزئیات بیشتر

> این بخش مکمل `04_principles.md` بخش ۴.۲ (سطح‌بندی) و ۴.۵ (۷-step process) است. اینجا جزئیات اجرایی تکمیلی.

### آپدیت اسناد پس از تأیید

- بخش تغییریافته در سند مربوطه آپدیت شود
- Change Log سند با نسخه جدید ثبت شود
- `SESSION_STATUS.md` با آخرین تغییر بروزرسانی شود
- اگر تغییر روی چند سند اثر دارد، همه آپدیت شوند (Atomic Updates، قانون #۲۶)

### چک‌لیست اجباری شروع چت

طبق قانون #۲۵ و #۴۸، Claude در شروع هر چت **هیچ کار قبل از تأیید کاربر** انجام نمی‌دهد. ۸ مرحله:

1. بازشناسی پیوست‌ها (zip + سند جامع)
2. استخراج و بررسی ساختار zip
3. خواندن اسناد به ترتیب الزامی (طبق بخش ۶.۱)
4. بررسی محیط (venv، DB، node_modules)
5. درک Bug ها و تصمیمات گذشته
6. تعیین Tier فعلی و گام‌های ممکن
7. تولید گزارش آمادگی به کاربر
8. صبر برای تأیید کاربر

---

## ۶.۱۲ Handoff به برنامه‌نویس جدید

پروژه طوری طراحی شده که برنامه‌نویس جدید بتواند در **یک روز کاری** مسلط شود:

1. خواندن `docs/ONBOARDING_GUIDE.md` (۴-۶ ساعت)
2. اجرای `python scripts/00b_post_unzip_setup.py`
3. ادامه کار

سند `docs/REUSABLE_SKELETON.md` راهنمای استفاده مجدد + استخراج template را دارد. در پایان پروژه، یک template جدا با نام پیشنهادی `python-react-skeleton` استخراج می‌شود.

---

## 🚧 وضعیت این ماژول

✅ **Migration کامل از v2.11 + Atomic Updates v2.12 + v2.14 (S3.2) + v2.18 (part21)**

✅ **افزوده‌های v2.14 اعمال‌شده (S3.2 part07):**
- Template ۱۱ — Pre-Action Checklist Visibility (پشتیبان Rule #۷۶ + M100)
- Template ۱۲ — Git Commit -F Flag Standard (پشتیبان M95+M97+M99 + Rule #۴۲/#۴۳/#۶۶/#۷۶ cross-refs)
- §۶.۳ heading: «۱۰ Template» → «۱۲ Template»

✅ **افزوده‌های v2.18 اعمال‌شده (part21):**
- Module header در header دارد: v2.18 ✅
- M106–M110 cross-refs به این ماژول اضافه شد

🔮 **افزوده‌های بعدی (S3.3-S3.4):**
- §۶.۵ Pre-commit hooks: Layer 1 Audit refresh post-S3.3 ACCEPTABLE_VERSIONS update
- §۶.۷ Filesystem MCP troubleshooting: ادغام M88+M93-M110 lessons
- §۶.۱ boot sequence: به‌روز به `01a_rules_core.md` (بجای `01_rules.md`) + شماره قوانین 90

---

**📌 پایان 06_meta.md (S3.2 اتمیک v2.14 applied · v2.18 header updated — part21)**

پس از commit 7، مرحله ۳ Migration کامل شد. v2.14 S3.1+S3.2 اتمیک update پس از آن اعمال شد. v2.18 در part21 با M106–M110 و boot protocol آپدیت شد.
