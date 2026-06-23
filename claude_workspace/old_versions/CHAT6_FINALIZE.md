# 📜 CHAT6_FINALIZE — جمع‌بندی نهایی چت ۶

> **هدف یک‌خطی:** ثبت دقیق همه دستاوردها، قوانین جدید، باگ‌ها و کارهای معلق چت ۶ برای handoff به چت ۷.

> **محل قرارگیری:** `docs/CHAT6_FINALIZE.md`
> **چت:** `TRADING-phase0-part06-quality-hardening`
> **تاریخ:** 2026-05-17
> **نسخه:** v1.0

---

## ۱. خلاصه دستاوردها

### ✅ کارهای Tier 2 تکمیل‌شده (T2.01-T2.04)

| Task | شرح | اسکریپت | تست |
|---|---|---|---|
| T2.03 | `.env.example` audit (backend + ساخت frontend) | `34_env_examples_audit.py` | ۲۰/۲۰ static ✅ |
| T2.01 | Error Boundaries (defense-in-depth) | `35_error_boundaries.py` | ۳۱/۳۱ static ✅ |
| T2.02 | vitest setup + ۵ smoke test | `36_vitest_setup.py` | **۳۰/۳۰ runtime ✅** |
| T2.04 | ARCHITECTURE.md با ۶ دیاگرام Mermaid | `37_architecture_doc.py` | ۳۶/۳۶ static ✅ |

### ✅ Git Infrastructure

- بازیابی git history — چت‌های ۴-۶ به‌صورت retroactive commit شدند
- ۱۲ commit کلاً در history
- `.gitignore` تمیز و کامل
- پاکسازی فایل‌های `.bak` و `.log`

### ✅ Sync Infrastructure

- اسکریپت `scripts/43_sync_from_zip.py` — workflow استاندارد برای sync کردن state چت Claude به پروژه local
- روش dry-run + apply با backup خودکار

---

## ۲. قوانین جدید کشف‌شده در این چت (#۲۷ - #۳۲)

این قوانین در این چت کشف شدند ولی هنوز در `سند_جامع_v2_7.md` و `CLAUDE_CHECKLIST.md` به‌صورت formal ادغام نشده‌اند. **اولویت اول چت ۷:** ادغام این قوانین در اسناد رسمی.

### قانون قفل‌شده #۲۷ — تأیید صریح کاربر برای پایان چت

Claude **هرگز** فرآیند پایان چت (۱۲ مرحله فاز ۳ CLAUDE_CHECKLIST) را به‌صورت خودکار شروع نکند.

**رفتار صحیح:**
- بعد از اتمام task، Claude خلاصه می‌دهد و **منتظر دستور بعدی می‌ماند**
- جملاتی مثل «گام بعدی چیست؟» **تأییدیه پایان نیستند**
- تأییدیه‌های صریح: «چت رو ببند»، «end of chat»، «zip نهایی بساز و چت رو ببند»

**استثنا:** سقف context window — با هشدار قبلی.

### قانون قفل‌شده #۲۸ — کوتاه گفتن خطا

وقتی کد به خطا می‌خورد، **فقط اقدامات اجرایی** که کاربر باید انجام دهد گفته شود — بدون توضیحات فنی طولانی درباره علت یا روش تشخیص.

❌ بد: «این خطا به این دلیل است که... من می‌خواهم با این روش حل کنم...»
✅ خوب: «این دستور را بزنید: [دستور]»

### قانون قفل‌شده #۲۹ — ارائه فایل با Artifact یا code block

فایل‌های ساخت/اصلاح **همیشه** به‌صورت Artifact (در کادر سمت راست) یا code block با لینک فعال در پایان پیام ارائه شوند.

❌ ممنوع: paste متن فایل برای دستی copy کردن در Notepad
✅ صحیح: Artifact یا code block استاندارد با دکمه Copy

**نکته:** برای Python script ها، Artifact پشتیبانی نمی‌شود، ولی code block استاندارد قابل قبول است.

### قانون قفل‌شده #۳۰ — اصلاحات کوچک فایل = اسکریپت Python

برای اصلاح کوچک روی فایل موجود (مثل افزودن خط)، از اسکریپت Python استفاده شود — نه دستور دستی.

این اسکریپت باید **idempotent** باشد (در صورت اجرای دوم، تغییری ندهد).

### قانون قفل‌شده #۳۱ — شماره tab + رنگ tab بالای هر کادر کد

بالای هر کادر کد، **هم شماره tab و هم رنگ tab** ذکر شود.

**رنگ‌بندی پیش‌فرض ۴ tab:**

| Tab | رنگ | کاربرد | پوشه فعال پیش‌فرض |
|---|---|---|---|
| `1 backend` | 🟦 آبی | سرور + تست backend + venv | `backend/` |
| `2 scripts` | 🟩 سبز | اسکریپت‌های Python | پروژه root |
| `3 frontend` | 🟧 نارنجی | React + تست frontend | `frontend/` |
| `4 BACKUP` | 🟥 قرمز | git + backup + sync | پروژه root |

**مثال نحوه استفاده در دستور:**

```
**🟥 tab «4 BACKUP»**
git status
```

### قانون قفل‌شده #۳۲ — npm install در ایران: روش قطعی

**علت مشکل:** `registry.npmjs.org` در ایران فیلتر است. حتی با VPN آلمان، گاهی کند است.

**روش قطعی تست‌شده (2026-05-17):**

```cmd
cd <frontend-path>
npm config set registry https://registry.npmmirror.com/
npm install --save-dev --no-audit --no-fund --prefer-offline <packages>
```

**نکات:**
- `--no-audit` و `--no-fund` ~۳۰s صرفه‌جویی
- `--prefer-offline` ابتدا از cache local استفاده می‌کند
- **زمان نصب ۱۴۸ پکیج: ۱ دقیقه** (تست‌شده)

اگر باز هم کند بود، اسکریپت `00b_post_unzip_setup.py` راه fallback خودکار دارد.

---

## ۳. باگ‌های کشف‌شده در این چت

### Bug #50 — `import React` در فایل‌های .jsx برای vitest

**مشاهده:** فایل‌های `.jsx` در پروژه با React 19 + Vite کار می‌کنند (به دلیل JSX runtime automatic در plugin react)، **ولی** در vitest با jsdom، گاهی این automatic مدوله نمی‌شود و خطای `React is not defined` می‌دهد.

**راه‌حل موقت (اعمال‌شده):** افزودن `import React from 'react';` به همه ۱۵ فایل `.jsx` در `frontend/src/`.

**راه‌حل بهتر (TODO در چت ۷):** پیدا کردن علت ریشه‌ای — احتمالاً تنظیم `jsx: 'automatic'` در `tsconfig.json` یا `vite.config.js` در بلوک test.

**فایل‌های متأثر:** ۱۵ فایل `.jsx` در `frontend/src/`
**اسکریپت اصلاح:** `scripts/45_fix_react_imports_all_jsx.py`

### Bug #51 — Escape characters در `python -c` در CMD ویندوز

**مشاهده:** نوشتن کد Python در `python -c "..."` با CMD ویندوز، escape کاراکترهای `\n` بسیار حساس است. در یک مورد، `\n` به‌صورت literal text نوشته شد به‌جای newline واقعی.

**درس آموخته:** برای ساخت/اصلاح فایل، **همیشه** یک اسکریپت Python جداگانه بسازید و اجرا کنید — نه `python -c` با کد طولانی.

**اسکریپت اصلاح:** `scripts/46_fix_broken_imports.py`

---

## ۴. کارهای معلق برای چت ۷ — Tier 2 ادامه

### T2.05 — Git workflow audit + GIT_WORKFLOW.md

**هدف:** نوشتن سند `docs/GIT_WORKFLOW.md` با:
- Conventional Commits convention (feat/fix/docs/test/...)
- Branching strategy
- `.gitignore` policy
- اسکریپت audit `scripts/38_git_workflow_audit.py`
- چک‌لیست اولین commit

**تخمین:** ۱ ساعت

### T2.06 — Pre-commit hooks

**هدف:**
- `.pre-commit-config.yaml` (pre-commit framework Python — استاندارد چندزبانه)
- `backend/requirements-dev.txt` (pre-commit, ruff, pytest, ...)
- `docs/PRECOMMIT.md`
- Hooks: ruff (Python), eslint (JS/JSX), block-env-files

**تخمین:** ۱.۵ ساعت

### T2.07 — Anti-pattern catalog مفصل

**هدف:** `docs/ANTI_PATTERNS.md` با:
- برای هر A1-A10: scenario واقعی، مثال bad/good، روش تشخیص
- چک‌لیست self-review قبل از commit

**تخمین:** ۱ ساعت

### T2.08 — Backend pytest + coverage

**هدف:**
- `backend/pyproject.toml` (pytest + coverage + ruff config)
- `backend/tests/conftest.py` (env vars test)
- `backend/tests/unit/test_security.py` (bcrypt + JWT — ۱۲ تست)
- `backend/tests/unit/test_response.py` (response wrappers — ۹ تست)
- `backend/tests/integration/test_health.py` (TestClient — ۳ تست)
- `docs/BACKEND_TESTING.md`

**تخمین:** ۲ ساعت

### T2.09 — API_DOCS.md

**هدف:** `docs/API_DOCS.md` با مستندات تمام ۶ endpoint:
- GET /health
- POST /auth/login
- POST /auth/refresh
- POST /auth/logout
- GET /auth/me
- GET /ohlcv/{symbol_id}

برای هر endpoint: method، path، auth، request format، response example، curl، Python httpx.

**تخمین:** ۱ ساعت

---

## ۵. وضعیت Git در پایان چت ۶

```
1c66d39 (HEAD -> main) fix(jsx): add React imports + install vitest deps for T2.02 verification
e79b947 feat(tier2): T2.01-T2.04 complete + Tier 2 governance docs
65e90b6 chore: tighten .gitignore (bak/log/coverage/pytest-cache)
f3034c0 chore: remove .bak/.log files and tighten .gitignore
f787e97 feat: retrospective sync - chat 4-6 state (auth, frontend, theme, toast, ui-polish, governance)
c59f200 docs(session): close chat 3 - finalize v2.3
2d30c21 docs(session): close chat 3 - add Chat Handoff Protocol (v2.2)
5e8d990 fix(logging): add colorama and UTF-8 support for Windows CMD
ac0caaa feat(core): add logger, exceptions, handlers, response wrapper
d2ade7b feat(backend): bootstrap FastAPI app with config, env, health endpoint
11e44be docs(session): record 10 architecture decisions (v0.1.1)
b8a02d0 feat: initial project structure (Phase 0 - Step 1)
```

**۱۲ commit کل**، working tree clean.

---

## ۶. اسکریپت‌های ساخته‌شده در این چت

| اسکریپت | کاربرد |
|---|---|
| `00b_post_unzip_setup.py` | (از چت ۵) راه‌اندازی خودکار venv + DB + node_modules با fallback |
| `33_upgrade_doc_to_v27.py` | (از چت ۵) ارتقای سند جامع |
| `34_env_examples_audit.py` + `34b_test_env_examples.py` | T2.03 |
| `35_error_boundaries.py` + `35b_test_error_boundaries.py` | T2.01 |
| `36_vitest_setup.py` + `36b_test_vitest_setup.py` | T2.02 |
| `37_architecture_doc.py` + `37b_test_architecture_doc.py` | T2.04 |
| `43_sync_from_zip.py` | sync فایل‌های منبع از zip Claude به local — idempotent + dry-run + apply + backup |
| `45_fix_react_imports_all_jsx.py` | افزودن import React به همه .jsx (Bug #50) |
| `46_fix_broken_imports.py` | اصلاح escape characters خراب (Bug #51) |

---

## ۷. رویه استاندارد چت‌های آینده — بر اساس تجربه چت ۶

این رویه که در چت ۶ کشف و تثبیت شد، **برای تمام چت‌های بعدی** اعمال می‌شود:

### الف) آغاز چت

1. کاربر zip state چت قبل را به Claude می‌دهد (مرجع، نه جایگزین)
2. Claude `00b_post_unzip_setup.py` را در ذهن دارد ولی نیازی به اجرا نیست در container
3. کاربر روی پوشه واقعی پروژه (نه از zip) کار می‌کند

### ب) در طول چت

- Claude کارها را در container انجام می‌دهد
- در پایان هر task، **منتظر دستور بعدی** (قانون #۲۷)
- فایل‌های جدید با Artifact یا code block با دکمه Copy (قانون #۲۹)

### ج) پایان چت — Sync Protocol

۱. Claude یک zip از state container می‌سازد
۲. کاربر zip را در `D:\Projects\` می‌گذارد
۳. کاربر اسکریپت sync را با dry-run اجرا می‌کند:
```cmd
python scripts\43_sync_from_zip.py "D:\Projects\<zip>"
```
۴. گزارش را بررسی، سپس apply:
```cmd
python scripts\43_sync_from_zip.py "D:\Projects\<zip>" --apply
```
۵. `git status` → `git diff` → `git add -A` → `git commit -m "..."`

### د) رنگ tabها

طبق قانون #۳۱ — همه دستورات با شماره + رنگ tab برچسب می‌خورند.

---

## ۸. نکات حساس برای Claude چت ۷

- ✅ این سند را اول بخوان
- ✅ `SESSION_STATUS.md` را برای snapshot دقیق state بخوان
- ✅ `TASK_BACKLOG.md` را برای ادامه Tier 2 بخوان
- ✅ قوانین #۲۷-#۳۲ را در ذهن داشته باش (حتی اگر هنوز در سند جامع formal نشده‌اند)
- ⚠️ قبل از شروع T2.05-T2.09، **اول قوانین #۲۷-#۳۲ را به سند جامع و CLAUDE_CHECKLIST اضافه کن** (atomic update — قانون #۲۶)
- ⚠️ اگر کاربر گفت «شروع کن»، بپرس کدام task اول
- ⚠️ هرگز چت را خودکار نبند — منتظر تأیید صریح (قانون #۲۷)

---

## ۹. آمار

| متریک | مقدار |
|---|---|
| Tasks تکمیل‌شده | ۴ از ۹ (T2.01-T2.04) |
| Tasks معلق | ۵ (T2.05-T2.09) |
| Commits در این چت | ۵ commit جدید |
| فایل‌های .jsx اصلاح‌شده (import React) | ۱۵ |
| تست‌های vitest passed | ۳۰/۳۰ |
| قوانین جدید کشف‌شده | ۶ (#۲۷-#۳۲) |
| باگ‌های کشف‌شده | ۲ (#۵۰، #۵۱) |

---

## 📌 پایان CHAT6_FINALIZE

**نسخه:** v1.0
**تهیه‌کننده:** Claude در پایان چت ۶
**به‌روز توسط:** Claude بعدی در صورت نیاز
