# -*- coding: utf-8 -*-
"""
50_create_git_workflow_doc.py — تولید docs/GIT_WORKFLOW.md (T2.05)

تولید مستند رسمی Git workflow پروژه شامل:
  - استراتژی branch
  - الگوی Conventional Commits + scope ها
  - تنظیمات Windows-specific (autocrlf، Persian filenames)
  - زمان commit، rollback، tag، backup
  - نکات Claude-driven workflow (zip + sync)

اسکریپت idempotent است: اجرای دوم تغییری ایجاد نمی‌کند.

استفاده (از ریشه پروژه):
  python scripts\\50_create_git_workflow_doc.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "GIT_WORKFLOW.md"


GIT_WORKFLOW_CONTENT = """# Git Workflow — راهنمای کار با Git در پروژه trading-system

> **نسخه:** v1.0 (2026-05-18 — چت ۷ / T2.05)
> **مرجع بالاتر:** PROJECT_GOVERNANCE.md + سند جامع v2.8

---

## فهرست

- [۱. استراتژی Branch](#۱-استراتژی-branch)
- [۲. تنظیمات اولیه (Windows)](#۲-تنظیمات-اولیه-windows)
- [۳. الگوی Commit Message — Conventional Commits](#۳-الگوی-commit-message--conventional-commits)
- [۴. زمان Commit](#۴-زمان-commit)
- [۵. Workflow اصلاح فایل از طریق Claude](#۵-workflow-اصلاح-فایل-از-طریق-claude)
- [۶. Persian Filenames](#۶-persian-filenames)
- [۷. مدیریت CRLF/LF](#۷-مدیریت-crlflf)
- [۸. Rollback و Revert](#۸-rollback-و-revert)
- [۹. Tag گذاری نسخه‌ها](#۹-tag-گذاری-نسخه‌ها)
- [۱۰. Backup — رابطه با قانون #۳۳](#۱۰-backup--رابطه-با-قانون-۳۳)
- [۱۱. .gitignore — تنظیم استاندارد پروژه](#۱۱-gitignore--تنظیم-استاندارد-پروژه)
- [۱۲. Alias های پیشنهادی](#۱۲-alias-های-پیشنهادی)
- [۱۳. سناریوهای رایج](#۱۳-سناریوهای-رایج)
- [۱۴. عیب‌یابی](#۱۴-عیب‌یابی)

---

## ۱. استراتژی Branch

این پروژه **Single-branch (main only)** است:

- **branch:** فقط `main`
- **بدون feature branch، بدون PR، بدون merge**
- علت: پروژه solo، یک Claude در یک چت، یک کاربر — overhead branch مدیریت ندارد

### استثناها (موارد توصیه‌شده برای branch موقت)

| مورد | علت | پاکسازی |
|---|---|---|
| مهاجرت Alembic ریسک‌دار | امکان revert سریع DB schema | merge → delete |
| Refactor بزرگ (>۵ فایل، >۵۰۰ خط) | جداکردن از main تا تست کامل | merge → delete |
| آزمایش معماری جدید (POC) | احتمال abandon | delete (بدون merge) |

### نمونه (در صورت نیاز)

```cmd
git checkout -b experiment/new-architecture
:: ... کار آزمایشی ...
git checkout main
git merge experiment/new-architecture  :: یا git branch -D
```

---

## ۲. تنظیمات اولیه (Windows)

### تنظیمات اجباری

```cmd
git config --global user.name "نام کاربر"
git config --global user.email "ایمیل@دامنه.ir"
git config --global core.autocrlf true
git config --global core.quotepath false
git config --global init.defaultBranch main
```

### تأیید تنظیمات

```cmd
git config --global --list
```

> 💡 `core.autocrlf=true` در Windows ضروری است (CRLF محلی، LF در repository).
> 💡 `core.quotepath=false` نام‌های فارسی را در `git status` و `git log` بدون escape نشان می‌دهد.

---

## ۳. الگوی Commit Message — Conventional Commits

### قالب کلی

```
<type>(<scope>): <description>

[body اختیاری]
[footer اختیاری]
```

### Type های مجاز

| type | کاربرد | مثال |
|---|---|---|
| **feat** | قابلیت جدید | `feat(backend): add OHLCV import endpoint` |
| **fix** | رفع bug | `fix(frontend): TimeRangePresets state mismatch` |
| **docs** | تغییر مستندات | `docs(governance): integrate rules #23-#32` |
| **refactor** | بازنویسی بدون تغییر رفتار | `refactor(repository): extract base CRUD methods` |
| **test** | افزودن/اصلاح تست | `test(frontend): vitest setup + 30 smoke tests` |
| **chore** | کارهای جانبی، تنظیمات | `chore(deps): bump SQLAlchemy to 2.0.30` |
| **perf** | بهبود عملکرد | `perf(repository): use bulk insert for OHLCV` |
| **style** | فرمت کد بدون تغییر منطق | `style(frontend): apply prettier` |

### Scope های پروژه

| scope | محتوا |
|---|---|
| `backend` | کد FastAPI، repository، services |
| `frontend` | کد React/Vite |
| `scripts` | اسکریپت‌های Python ریشه |
| `docs` | مستندات `docs/` |
| `governance` | فایل‌های Governance (CLAUDE_CHECKLIST، PROJECT_GOVERNANCE، CHAT_LOG، SESSION_STATUS، TASK_BACKLOG) |
| `tier1` / `tier2` / `tier3` | تکمیل task های Tier مربوطه |
| `deps` | تغییر در `requirements.txt` یا `package.json` |
| `migration` | تغییر در `alembic/versions/` |
| `chat<N>` | اتمیک end-of-chat (با هر فاز/تغییر همراه) |

### نمونه‌های صحیح

```
feat(backend): add OHLCV import endpoint with httpx test
fix(scripts): 47_upgrade_doc — handle ZWNJ in anchors
docs(governance): integrate rules #23-#32 + bump سند_جامع to v2.8
chore(deps): freeze frontend versions in package.json
test(backend): pytest setup + 5 smoke tests for /health
```

### قوانین

- **خط اول:** حداکثر ۷۲ کاراکتر (mobile-friendly در GitHub)
- **زمان فعل:** Imperative — `add`، نه `added` یا `adds`
- **بدون نقطه پایان** در خط اول
- **بدون emoji** در subject line (در body مجاز)
- **scope الزامی** — یکی از لیست بالا

---

## ۴. زمان Commit

### قانون اصلی — یک Commit به ازای هر "واحد منطقی"

| واحد | مثال |
|---|---|
| یک task کامل (مثل T2.05) | `feat(tier2): T2.05 — git workflow doc` |
| یک مرحله از task (مثل مرحله A چت ۷) | `docs(governance): atomic update rules #23-#32` |
| یک bugfix | `fix(frontend): timezone parsing` |
| یک سری migration مرتبط | `feat(migration): add desc indexes to OHLCV` |

### قانون — قبل از commit همیشه

1. ✅ تست‌های مرتبط را اجرا کنید (vitest، pytest، اسکریپت `*b_test_*.py`)
2. ✅ `git status` را بررسی کنید (فایل ناخواسته نباشد)
3. ✅ `git diff --cached` برای دیدن staged changes
4. ✅ پیام را با scope مناسب بنویسید

### Anti-patterns

- ❌ **WIP commit** — کار نیمه‌تمام push نکنید
- ❌ **Mixed concerns** — feat + fix در یک commit
- ❌ **General messages** — `update files`، `bug fix`، `changes`

---

## ۵. Workflow اصلاح فایل از طریق Claude

این پروژه از روش **zip + sync_from_zip** برای دریافت فایل از Claude استفاده می‌کند:

### گردش کار استاندارد

```
1. کاربر → Claude:    درخواست تغییر
2. Claude → اسکریپت Python + تست همراه (قانون #۲۲)
3. Claude → zip حاوی scripts/ و docs/ تغییر یافته
4. کاربر:             استخراج با scripts/43_sync_from_zip.py
5. کاربر:             اجرای اسکریپت + تست
6. کاربر:             git add + commit با scope مناسب
```

### نمونه پیام commit پس از Claude-driven change

```
docs(governance): integrate rules #23-#32 + bump سند_جامع to v2.8

اعمال‌شده با:
- scripts/47_upgrade_doc_to_v28.py
- scripts/48_atomic_governance_update.py
- scripts/48c_fixup_missing_patches.py

تست: 47b 24/24 + 48b 26/26 pass
```

### قانون idempotency

تمام اسکریپت‌های تولید/اصلاح فایل **idempotent** هستند (قانون #۳۰):

- اجرای دوم → تغییری ایجاد نمی‌کند
- `git diff` بعد از اجرای دوم → خالی

---

## ۶. Persian Filenames

### مشکل پیش‌فرض

بدون تنظیم `core.quotepath`، نام‌های فارسی به‌صورت escape شده نشان داده می‌شوند:

```
"docs/\330\263\331\206\330\257_\330\254\330\247\331\205\330\271_v2_8.md"
```

### راه‌حل (یک‌بار تنظیم)

```cmd
git config --global core.quotepath false
```

پس از تنظیم:

```
docs/سند_جامع_v2_8.md
```

### پشتیبانی Editor

- **VS Code:** نام فارسی خودکار پشتیبانی می‌شود
- **GitHub Web:** نام فارسی صحیح نمایش داده می‌شود
- **`git log --name-only`:** با `core.quotepath=false` صحیح نمایش می‌دهد

### استثنا — zip Persian filename

اسکریپت `43_sync_from_zip.py` فایل‌هایی با نام فارسی mojibake را skip می‌کند.
راه‌حل: اسکریپت‌های بعدی Claude (مانند `49_fix_chat7_phase_a_zip.py`) از `encode('cp437').decode('utf-8')` برای fix encoding استفاده می‌کنند.

---

## ۷. مدیریت CRLF/LF

### رویکرد پروژه

- **در repository:** LF (نرمال Unix)
- **در working copy ویندوز:** CRLF (نرمال Windows)
- **مدیریت خودکار:** `git config core.autocrlf true`

### Warning رایج

```
warning: in the working copy of 'docs/CLAUDE_CHECKLIST.md', LF will be replaced by CRLF the next time Git touches it
```

> ✅ این warning **عادی** است و نگران‌کننده نیست.
> Git فایل را به CRLF در checkout بعدی تبدیل می‌کند، در commit به LF برمی‌گرداند.

### `.gitattributes` (اختیاری — برای کنترل دقیق‌تر)

اگر می‌خواهید برای فایل‌های خاص رفتار متفاوتی داشته باشید:

```gitattributes
*.py    text eol=lf
*.md    text eol=lf
*.cmd   text eol=crlf
*.bat   text eol=crlf
```

---

## ۸. Rollback و Revert

### سناریو ۱ — لغو commit آخر، حفظ تغییرات

```cmd
git reset --soft HEAD~1
```

فایل‌های تغییر یافته در stage باقی می‌مانند.

### سناریو ۲ — لغو commit آخر، unstage تغییرات

```cmd
git reset HEAD~1
```

### سناریو ۳ — لغو کامل (تغییرات از بین می‌رود)

```cmd
git reset --hard HEAD~1
```

⚠️ غیرقابل بازگشت بدون backup یا reflog.

### سناریو ۴ — لغو با ایجاد commit جدید (امن‌ترین — برای history منتشرشده)

```cmd
git revert HEAD
```

### سناریو ۵ — بازگشت به commit مشخص

```cmd
git log --oneline -10
git reset --hard <hash>
```

### سناریو ۶ — بازیابی فایل از commit قبلی

```cmd
git checkout <hash> -- path/to/file.md
```

---

## ۹. Tag گذاری نسخه‌ها

### قانون — تنها در نقاط عطف پروژه

| Tag | شرایط |
|---|---|
| `v0.1.0` | پایان فاز ۰ (Backend foundation) |
| `v0.5.0` | پایان فاز ۰ + Tier 1/2 Governance |
| `v1.0.0` | اولین release قابل استفاده end-user |

### ایجاد tag

```cmd
git tag -a v0.5.0 -m "End of Phase 0 — Tier 2 Quality Hardening complete"
git push --tags
```

> 💡 از light tag (`git tag v0.5.0`) **استفاده نکنید**. همیشه annotated (`-a -m`) باشد.

---

## ۱۰. Backup — رابطه با قانون #۳۳

طبق **قانون #۳۳** (افزوده در چت ۷):

> Backup فقط در **پایان هر چت** انجام می‌شود — نه قبل از هر commit.
> Git history منبع اصلی rollback است.

### استثناها (نیازمند backup قبل از تغییر)

- ✅ مهاجرت Alembic روی DB واقعی (`alembic upgrade head` با داده production)
- ✅ تغییرات destructive خارج از Git (پاک‌کردن `data/excel_imports/`)
- ✅ Refactor بزرگ schema (تغییر type column، rename table)
- ❌ commit عادی — کافی نیست
- ❌ تغییر سند — کافی نیست

### اسکریپت backup

```cmd
python scripts\\02_backup.py
```

(یا هر اسکریپت backup فعلی پروژه — تأیید با `ls scripts/*backup*`)

---

## ۱۱. .gitignore — تنظیم استاندارد پروژه

`.gitignore` فعلی پروژه شامل:

- **Python:** `__pycache__/`, `*.py[cod]`, `.pytest_cache/`, `.coverage`
- **Virtual env:** `venv/`, `.venv/`
- **Environment vars:** `.env*`
- **Database:** `*.db`, `*.sqlite*`
- **IDE:** `.vscode/`, `.idea/`
- **OS:** `Thumbs.db`, `.DS_Store`
- **Node:** `node_modules/`, `package-lock.json`
- **Build:** `dist/`, `build/`
- **Logs:** `*.log`, `logs/`
- **Data:** `data/excel_imports/*.xlsx` (با حفظ `.gitkeep`)
- **Backups:** `backups/`, `*.backup`, `.sync-backup/`
- **Temp:** `*.tmp`, `tmp/`, `temp/`

### قانون — هرگز ignore نشوند

| فایل | علت |
|---|---|
| `docs/**/*.md` | همه مستندات پروژه track می‌شوند |
| `scripts/*.py` | همه اسکریپت‌های Python (به‌جز `__pycache__`) |
| `.env.example` | template برای محیط — همیشه track می‌شود |
| `requirements.txt` | dependencies دقیق |

---

## ۱۲. Alias های پیشنهادی

افزودن به `~/.gitconfig` (یا `git config --global alias.<name> <command>`):

```ini
[alias]
    st = status
    lg = log --oneline -15 --decorate --graph
    ll = log --pretty=format:"%h %ad %s" --date=short -20
    co = checkout
    br = branch
    ci = commit
    last = log -1 HEAD --stat
    unstage = reset HEAD --
    pop = stash pop
    amend = commit --amend --no-edit
```

### استفاده

```cmd
git st               :: git status
git lg               :: git log oneline + graph
git ll               :: git log با تاریخ
git unstage file.md  :: unstage فایل
git amend            :: ضمیمه به commit آخر بدون تغییر پیام
```

---

## ۱۳. سناریوهای رایج

### ۱۳.۱ — اضافه‌کردن فایل ناخواسته به commit

```cmd
git rm --cached path/to/file.log
git commit --amend --no-edit
```

سپس به `.gitignore` اضافه شود.

### ۱۳.۲ — Commit با scope اشتباه

```cmd
git commit --amend -m "feat(backend): correct scope"
```

⚠️ فقط برای commit آخر — اگر push شده، از `git revert` استفاده کنید.

### ۱۳.۳ — مرور تغییرات قبل از commit

```cmd
git diff                :: تغییرات unstaged
git diff --cached       :: تغییرات staged
git diff HEAD~1 HEAD    :: تفاوت با commit قبلی
```

### ۱۳.۴ — جست‌وجو در history

```cmd
git log --grep="governance"           :: commit با کلمه در message
git log --all --oneline -- docs/      :: commit های مرتبط با docs/
git log -p docs/CLAUDE_CHECKLIST.md   :: تاریخچه کامل یک فایل
git blame docs/سند_جامع_v2_8.md       :: نویسنده هر خط
```

### ۱۳.۵ — Stash برای کار موقت

```cmd
git stash                   :: ذخیره تغییرات بدون commit
git stash list              :: لیست stash ها
git stash pop               :: بازگشت تغییرات
git stash drop              :: حذف stash آخر
```

---

## ۱۴. عیب‌یابی

### مشکل ۱: warning CRLF/LF در `git add`

```
warning: in the working copy of 'file.md', LF will be replaced by CRLF
```

✅ **عادی** — نادیده بگیرید (نگاه به بخش ۷).

### مشکل ۲: نام فایل فارسی escape شده

```
"docs/\330\263\331\206\330\257_..."
```

✅ راه‌حل:
```cmd
git config --global core.quotepath false
```

### مشکل ۳: `failed to push` (پروژه remote ندارد)

این پروژه فعلاً remote ندارد. برای ایجاد:

```cmd
git remote add origin <url>
git push -u origin main
```

### مشکل ۴: `working tree dirty` پیش از sync_from_zip

```cmd
git status
:: اگر فایل uncommitted دارید:
git stash
:: یا
git commit -am "wip: ..."
:: سپس sync انجام دهید
```

### مشکل ۵: Recovery پس از `git reset --hard` اشتباه

```cmd
git reflog                  :: لیست تمام HEAD های قبلی
git reset --hard <hash>     :: بازگشت به state قبل از reset
```

⏰ این فقط در محدوده زمانی `gc.reflogExpire` (پیش‌فرض ۹۰ روز) کار می‌کند.

---

## ۱۵. ارجاعات

- **PROJECT_GOVERNANCE.md** — قوانین کلی پروژه
- **CLAUDE_CHECKLIST.md** — چک‌لیست ۳ فاز (شروع/میانه/پایان چت)
- **سند جامع v2.8** — جدول ۱.۹ قوانین قفل‌شده
- **CHAT_LOG.md** — تاریخچه تصمیمات بین چت‌ها

---

## 📌 پایان GIT_WORKFLOW

**نسخه:** v1.0 (2026-05-18 — چت ۷ / T2.05)
**ساختار:** ۱۴ بخش
**کاربرد:** مرجع کار با Git در پروژه trading-system
"""


def write_if_changed(path: Path, content: str) -> bool:
    if path.exists():
        if path.read_text(encoding="utf-8") == content:
            return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    print("=" * 64)
    print("  50_create_git_workflow_doc — تولید docs/GIT_WORKFLOW.md")
    print("=" * 64)
    print()

    written = write_if_changed(DOC, GIT_WORKFLOW_CONTENT)
    if written:
        print(f"  ✏️  ایجاد/به‌روزرسانی: {DOC.name}")
        print(f"  📏  حجم: {len(GIT_WORKFLOW_CONTENT):,} کاراکتر")
        print(f"  📄  تعداد خط: {GIT_WORKFLOW_CONTENT.count(chr(10))}")
    else:
        print(f"  ✓  no-op: {DOC.name} از قبل به‌روز است")

    print()
    print("=" * 64)
    print("  ✅ موفق")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
