# Pre-commit Hooks — راهنمای کامل (Hybrid mode)

> **نسخه:** v1.0 (2026-05-18 — چت ۷ / T2.06)
> **حالت:** Hybrid (critical اجباری + minor warning)
> **مرجع بالاتر:** ANTI_PATTERNS.md + GIT_WORKFLOW.md + BACKEND_TESTING.md

---

## فهرست

- [۱. مفهوم Hybrid Mode](#۱-مفهوم-hybrid-mode)
- [۲. هوک‌های فعال در پروژه](#۲-هوکهای-فعال-در-پروژه)
- [۳. نصب اولیه](#۳-نصب-اولیه)
- [۴. روال روزانه](#۴-روال-روزانه)
- [۵. Bypass در اضطرار](#۵-bypass-در-اضطرار)
- [۶. ساختار فایل‌ها](#۶-ساختار-فایلها)
- [۷. عیب‌یابی](#۷-عیبیابی)
- [۸. هوک‌های سفارشی — افزودن جدید](#۸-هوکهای-سفارشی--افزودن-جدید)
- [۹. CI/CD آینده](#۹-cicd-آینده)
- [۱۰. ارجاعات](#۱۰-ارجاعات)

---

## ۱. مفهوم Hybrid Mode

پروژه از **حالت Hybrid** استفاده می‌کند — ترکیبی از اجباری و warning:

| نوع چک | حالت | چرا |
|---|---|---|
| **Format** (black, isort) | 🔴 اجباری + **auto-fix** | یکنواختی مطلق کد |
| **Trailing whitespace, EOL** | 🔴 اجباری + auto-fix | پیش‌گیری از diff های نویزی |
| **A1, A4, A8, A10** (critical) | 🔴 اجباری | bug-prone یا security-related |
| **A6** (print در backend) | 🟡 warning | ممکن است در dev موقتاً لازم باشد |
| **pytest unit** | 🔴 اجباری | سریع (<10s)، تأیید لایه پایه |
| **vitest** | 🔴 اجباری | سریع (<5s)، تأیید frontend |
| **pytest integration** | ⚪ skip | کند (>30s) — در CI اجرا می‌شود |
| **اسکریپت‌های `*b_test_*.py`** | ⚪ skip | طولانی — در commit مرحله ای اجرا می‌شوند |

> 💡 **bypass اضطرار:** `git commit --no-verify` + پیام `[skip-hooks: REASON]`

---

## ۲. هوک‌های فعال در پروژه

### ۲.۱ هوک‌های framework رسمی (`pre-commit`)

| Hook | عمل | فایل‌های هدف |
|---|---|---|
| `trailing-whitespace` | حذف فضاهای انتهای خط | همه (به‌جز .md) |
| `end-of-file-fixer` | اطمینان از خط جدید پایان | همه |
| `check-yaml` | syntax YAML | `.yaml`, `.yml` |
| `check-json` | syntax JSON | `.json` |
| `check-added-large-files` | جلوگیری از فایل > 1MB | همه |
| `check-merge-conflict` | تشخیص `<<<<<<< HEAD` | همه |
| `mixed-line-ending` | LF در همه فایل‌ها | همه (به‌جز `.cmd`, `.bat`) |
| `black` | فرمت Python (auto-fix) | `backend/app/`, `backend/tests/`, `scripts/` |
| `isort` | مرتب‌سازی imports (auto-fix) | همان مسیرها |

### ۲.۲ هوک‌های سفارشی محلی

| Hook | عمل | اجباری؟ |
|---|---|---|
| `check-anti-patterns` | بررسی A1-A10 (Hybrid: critical+minor) | بسته به anti-pattern |
| `pytest-unit` | اجرای `pytest tests/unit` | ✅ اجباری اگر backend تغییر کرد |
| `vitest` | اجرای vitest روی frontend | ✅ اجباری اگر frontend تغییر کرد |

---

## ۳. نصب اولیه

### پیش‌نیاز — نصب dev dependencies

🟦 **tab «1 backend»**
```cmd
cd D:\Projects\trading-system\backend
venv\Scripts\activate
pip install pre-commit==3.7.1 black==24.4.2 isort==5.13.2 -i https://mirrors.aliyun.com/pypi/simple/
```

### نصب hooks در `.git/hooks/`

🟩 **tab «2 scripts»**
```cmd
cd D:\Projects\trading-system
python scripts\install_git_hooks.py
```

### تست اولیه

```cmd
pre-commit run --all-files
```

اولین اجرا کند است (clone repo های hook). از اجرای دوم به بعد سریع.

---

## ۴. روال روزانه

### حالت طبیعی

```cmd
git add docs/MY_FILE.md
git commit -m "docs(governance): update X"
```

```
✓ trailing-whitespace                 passed
✓ end-of-file-fixer                   passed
✓ black                               passed (no python changes)
✓ check-anti-patterns                 passed
[main abc1234] docs(governance): update X
```

### وقتی auto-fix اعمال می‌شود

```cmd
git commit -m "feat: new feature"
```

```
❌ black                              files were modified
Reformatted backend/app/services/x.py

ℹ️ کد فرمت شد. لطفاً تغییرات را بپذیرید:
   git add .
   git commit -m "feat: new feature"
```

این عادی است — مجدد commit کنید.

### وقتی A1-A10 critical violation

```cmd
git commit -m "feat: ..."
```

```
❌ check-anti-patterns                failed

  🔴 A1: hex color hardcoded در JSX
    [A1] frontend/src/App.jsx:42 — color: '#1976d2',

📌 برای bypass (فقط در اضطرار):
   git commit --no-verify -m "[skip-hooks: REASON] ..."
```

**اقدام صحیح:** کد را اصلاح کنید (طبق `docs/ANTI_PATTERNS.md` بند A1).

---

## ۵. Bypass در اضطرار

طبق **قانون #۴۲** (افزوده در چت ۷):

> `--no-verify` فقط در اضطرار + commit message شامل `[skip-hooks: REASON]`

### موارد قابل قبول

| سناریو | مثال |
|---|---|
| Hook خودش bug دارد | `git commit --no-verify -m "[skip-hooks: hook-bug] fix x"` |
| Migration حساس | `git commit --no-verify -m "[skip-hooks: db-migration] alembic"` |
| WIP موقت قبل از merge | `git commit --no-verify -m "[skip-hooks: wip] partial"` |

### موارد غیرقابل قبول

- ❌ «hook کنده، صبر ندارم» — منتظر شوید
- ❌ «A1 violation است ولی موقتی» — همان لحظه اصلاح کنید
- ❌ «pytest fail است ولی بقیه کار می‌کند» — اصلاح کنید

---

## ۶. ساختار فایل‌ها

```
trading-system/
├── .pre-commit-config.yaml              ← config framework
├── scripts/
│   ├── 54_setup_precommit_hybrid.py     ← این اسکریپت
│   ├── 54b_test_precommit_setup.py      ← تست راه‌اندازی
│   ├── install_git_hooks.py             ← نصب راحت
│   ├── check_anti_patterns.py           ← هوک سفارشی A1-A10
│   ├── run_pytest_unit.cmd              ← هوک pytest unit
│   └── run_vitest.cmd                   ← هوک vitest
└── docs/
    └── PRECOMMIT.md                     ← این مستند
```

---

## ۷. عیب‌یابی

### مشکل ۱: `pre-commit not found`

🟦 **tab «1 backend»**
```cmd
cd backend
venv\Scripts\activate
pip install pre-commit==3.7.1
```

### مشکل ۲: `pre-commit install` خطای permission

اجرا با cmd رمز administrator (راست‌کلیک → Run as administrator).

### مشکل ۳: hook ها بسیار کند

اولین اجرا کند است. کش در `~/.cache/pre-commit/` ذخیره می‌شود. از دوم به بعد سریع.

اگر باز هم کند:
```cmd
pre-commit clean
pre-commit install
```

### مشکل ۴: `check-anti-patterns` همه فایل‌ها را چک می‌کند

این عمدی است — `pass_filenames: false` در config. برای محدودسازی، `pre-commit run` فقط روی staged files اجرا می‌شود.

### مشکل ۵: vitest در ویندوز کار نمی‌کند

🟧 **tab «3 frontend»**
```cmd
cd frontend
npm install
npm test -- --run
```

### مشکل ۶: pytest unit در ویندوز کار نمی‌کند

🟦 **tab «1 backend»**
```cmd
cd backend
venv\Scripts\activate
pytest tests/unit
```

---

## ۸. هوک‌های سفارشی — افزودن جدید

برای افزودن یک hook جدید (مثلاً برای anti-pattern جدید A11):

### مرحله ۱ — افزودن به `check_anti_patterns.py`

```python
CRITICAL["A11"] = {
    "name": "نام مشکل",
    "pattern": r"regex_pattern",
    "files": [".py"],
    "exclude_paths": ["tests/"],
    "exclude_context": ["# noqa"],
}
```

### مرحله ۲ — تست دستی

```cmd
python scripts\check_anti_patterns.py
```

### مرحله ۳ — افزودن به `ANTI_PATTERNS.md`

طبق قانون #۲۶ (Atomic Update) همه اسناد مرتبط.

---

## ۹. CI/CD آینده

برنامه (Tier 3):

| فاز | اقدام |
|---|---|
| فاز ۱ | افزودن GitHub Action: `pre-commit/action` |
| فاز ۲ | اجرای integration tests در CI |
| فاز ۳ | coverage threshold + bundle size check |

نمونه `.github/workflows/precommit.yml` (آینده):

```yaml
name: pre-commit
on: [push, pull_request]
jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - uses: pre-commit/action@v3.0.1
```

---

## ۱۰. ارجاعات

- **ANTI_PATTERNS.md** — تعریف A1-A10
- **BACKEND_TESTING.md** — تنظیمات pytest
- **GIT_WORKFLOW.md** — Conventional Commits
- **PROJECT_GOVERNANCE.md** — قانون #۴۲ (bypass conditions) + قانون #۴۳ (Hybrid mode)

---

## 📌 پایان PRECOMMIT

**نسخه:** v1.0 (2026-05-18 — چت ۷ / T2.06)
**ساختار:** ۹ بخش + ۱۰ ارجاع
**حالت:** Hybrid (critical + minor)
**هوک‌ها:** ۹ framework + ۳ سفارشی
