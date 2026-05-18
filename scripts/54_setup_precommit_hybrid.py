# -*- coding: utf-8 -*-
"""
54_setup_precommit_hybrid.py — راه‌اندازی Pre-commit Hooks (T2.06 — Hybrid)

این اسکریپت idempotent، حالت Hybrid:
  - افزودن pre-commit، black، isort به backend requirements
  - ساخت .pre-commit-config.yaml (هوک‌های framework رسمی)
  - ساخت .git-hooks/check-anti-patterns.cmd (هوک سفارشی A1-A10)
  - ساخت .git-hooks/run-tests.cmd (هوک اجرای pytest unit + vitest)
  - ساخت scripts/install_git_hooks.py (نصب راحت hooks)
  - ساخت docs/PRECOMMIT.md

استفاده (از ریشه پروژه):
  python scripts\\54_setup_precommit_hybrid.py
سپس برای نصب hooks:
  python scripts\\install_git_hooks.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"
DOCS = ROOT / "docs"
SCRIPTS = ROOT / "scripts"
HOOKS_DIR = ROOT / ".git-hooks"


# ============================================================
# 1) requirements.txt — افزودن dev deps
# ============================================================

PRECOMMIT_DEPS_BLOCK = """
# --- Pre-commit Hooks (T2.06 — چت ۷) ---
pre-commit==3.7.1
black==24.4.2
isort==5.13.2
"""

PRECOMMIT_MARKER = "# --- Pre-commit Hooks (T2.06 — چت ۷) ---"


def patch_requirements() -> tuple[bool, str]:
    req = BACKEND / "requirements.txt"
    text = req.read_text(encoding="utf-8")
    if PRECOMMIT_MARKER in text:
        return False, "requirements.txt: precommit deps از قبل افزوده شده"
    new_text = text.rstrip() + "\n" + PRECOMMIT_DEPS_BLOCK
    req.write_text(new_text, encoding="utf-8")
    return True, "requirements.txt: ۳ dep افزوده شد (pre-commit, black, isort)"


# ============================================================
# 2) .pre-commit-config.yaml — framework
# ============================================================

PRECOMMIT_CONFIG = """# Pre-commit configuration — Trading System (Hybrid mode)
# T2.06 (چت ۷)
#
# نصب: pip install pre-commit && pre-commit install
# اجرای دستی: pre-commit run --all-files
# اضطرار: git commit --no-verify -m "[skip-hooks: REASON] ..."

default_language_version:
  python: python3.11

repos:
  # ========== Built-in hooks ==========
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
        exclude: ^docs/.*\\.md$  # markdown نیازمند trailing space برای line break
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
        exclude: ^frontend/package-lock\\.json$
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: check-merge-conflict
      - id: mixed-line-ending
        args: ['--fix=lf']
        exclude: '\\.cmd$|\\.bat$'

  # ========== Python: black (اجباری) ==========
  - repo: https://github.com/psf/black
    rev: 24.4.2
    hooks:
      - id: black
        language_version: python3
        files: ^(backend/app/|backend/tests/|scripts/).*\\.py$
        args: ['--line-length=100']

  # ========== Python: isort (اجباری) ==========
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        files: ^(backend/app/|backend/tests/|scripts/).*\\.py$
        args: ['--profile=black', '--line-length=100']

  # ========== Local custom hooks (anti-patterns + tests) ==========
  - repo: local
    hooks:
      # Hook 1 — Anti-Patterns A1-A10 (اجباری)
      - id: check-anti-patterns
        name: Anti-Patterns A1-A10 check
        entry: python scripts/check_anti_patterns.py
        language: system
        types: [python]
        pass_filenames: false

      # Hook 2 — pytest unit only (اجباری، سریع)
      - id: pytest-unit
        name: Backend pytest unit tests
        entry: scripts/run_pytest_unit.cmd
        language: system
        files: ^backend/(app|tests/unit)/.*\\.py$
        pass_filenames: false

      # Hook 3 — vitest (اجباری، سریع)
      - id: vitest
        name: Frontend vitest
        entry: scripts/run_vitest.cmd
        language: system
        files: ^frontend/src/.*\\.(jsx?|tsx?)$
        pass_filenames: false
"""


# ============================================================
# 3) check_anti_patterns.py — هوک سفارشی A1-A10
# ============================================================

CHECK_ANTI_PATTERNS = '''# -*- coding: utf-8 -*-
"""
check_anti_patterns.py — هوک سفارشی pre-commit برای A1-A10

این اسکریپت روی فایل‌های staged Python و JSX اجرا می‌شود.
حالت Hybrid:
  - critical (A1, A4, A8, A10): fail commit
  - minor (A6 print): warning only

استفاده مستقیم: python scripts\\check_anti_patterns.py
از pre-commit: خودکار
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ============================================================
# لیست anti-pattern ها (Hybrid: critical اجباری، minor warning)
# ============================================================

CRITICAL = {
    # A1 — hex color hardcoded در JSX (frontend only)
    "A1": {
        "name": "hex color hardcoded در JSX",
        "pattern": r"#[0-9a-fA-F]{3,6}",
        "files": [".jsx"],
        "exclude_paths": ["frontend/src/themes/", "frontend/src/index.css"],
        "exclude_context": ["// theme-tokens-allowed"],
    },
    # A4 — secrets hardcoded
    "A4": {
        "name": "secret hardcoded (password/key/token)",
        "pattern": r\'\'\'(SECRET_KEY|PASSWORD|API_KEY|TOKEN)\\s*=\\s*["\\\'][^"\\\']{8,}["\\\']\'\'\',
        "files": [".py"],
        "exclude_paths": ["tests/", "scripts/"],
        "exclude_context": ["# noqa: secret-allowed", "settings.", "os.environ"],
    },
    # A8 — localStorage در JSX (Claude artifacts)
    "A8": {
        "name": "localStorage در JSX (به‌جای Zustand store)",
        "pattern": r"localStorage\\.(get|set)Item",
        "files": [".jsx"],
        "exclude_paths": ["frontend/src/stores/", "frontend/src/utils/storage"],
        "exclude_context": [],
    },
    # A10 — sync I/O در async function
    "A10": {
        "name": "sync I/O (open/time.sleep/requests) در async context",
        "pattern": r"^\\s+(with open\\(|time\\.sleep|requests\\.)",
        "files": [".py"],
        "exclude_paths": ["scripts/", "tests/", "migrations/"],
        "exclude_context": ["# noqa: sync-allowed"],
    },
}

MINOR = {
    # A6 — print در backend
    "A6": {
        "name": "print() به‌جای logger در backend",
        "pattern": r"^\\s*print\\(",
        "files": [".py"],
        "exclude_paths": ["scripts/", "tests/", "migrations/", "backend/main.py"],
        "exclude_context": ["# noqa: print-allowed"],
    },
}


def get_staged_files() -> list[Path]:
    """فایل‌های staged از git."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True, text=True, check=True,
        )
        return [ROOT / f for f in result.stdout.splitlines() if f.strip()]
    except subprocess.CalledProcessError:
        return []


def check_file(path: Path, rule_id: str, rule: dict) -> list[str]:
    """بررسی یک فایل برای یک قانون. لیست violations برمی‌گرداند."""
    if not path.exists() or path.is_dir():
        return []

    ext = path.suffix
    if ext not in rule["files"]:
        return []

    rel = str(path.relative_to(ROOT)).replace("\\\\", "/")
    for excl in rule["exclude_paths"]:
        if rel.startswith(excl):
            return []

    violations = []
    pattern = re.compile(rule["pattern"], re.MULTILINE)
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []

    for m in pattern.finditer(text):
        # شماره خط
        line_num = text[:m.start()].count("\\n") + 1
        line = text.splitlines()[line_num - 1] if line_num <= len(text.splitlines()) else ""

        # exclude_context
        skip = False
        for ctx in rule["exclude_context"]:
            if ctx in line:
                skip = True
                break
        if skip:
            continue

        violations.append(f"  [{rule_id}] {rel}:{line_num} — {line.strip()[:100]}")

    return violations


def main() -> int:
    files = get_staged_files()
    if not files:
        # احتمالاً اجرای دستی — همه فایل‌های پروژه را چک کن
        files = list((ROOT / "backend").rglob("*.py")) + list((ROOT / "frontend" / "src").rglob("*.jsx"))
        files = [f for f in files if "venv" not in str(f) and "node_modules" not in str(f)]

    critical_violations = []
    minor_violations = []

    for rule_id, rule in CRITICAL.items():
        for f in files:
            critical_violations.extend(
                (rule_id, rule["name"], v) for v in check_file(f, rule_id, rule)
            )

    for rule_id, rule in MINOR.items():
        for f in files:
            minor_violations.extend(
                (rule_id, rule["name"], v) for v in check_file(f, rule_id, rule)
            )

    # گزارش
    if critical_violations:
        print("=" * 64)
        print("  ❌ Anti-Pattern Violations (CRITICAL — commit aborted)")
        print("=" * 64)
        for rule_id, name, v in critical_violations:
            print(f"\\n  🔴 {rule_id}: {name}")
            print(v)
        print()

    if minor_violations:
        print("=" * 64)
        print("  ⚠️  Anti-Pattern Warnings (MINOR — commit allowed)")
        print("=" * 64)
        for rule_id, name, v in minor_violations:
            print(f"\\n  🟡 {rule_id}: {name}")
            print(v)
        print()

    if critical_violations:
        print("📌 برای bypass (فقط در اضطرار):")
        print(\'   git commit --no-verify -m "[skip-hooks: REASON] ..."\')
        return 1

    if not critical_violations and not minor_violations:
        print("✓ هیچ anti-pattern یافت نشد.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


# ============================================================
# 4) run_pytest_unit.cmd — اجرای فقط unit tests
# ============================================================

RUN_PYTEST_UNIT = """@echo off
REM run_pytest_unit.cmd — اجرای pytest unit tests (سریع)
REM فقط tests/unit/ — integration ها skip می‌شوند برای سرعت

cd /d "%~dp0\\..\\backend"
if not exist "venv\\Scripts\\activate.bat" (
  echo [WARN] backend venv پیدا نشد — skip pytest
  exit /b 0
)

call venv\\Scripts\\activate.bat
pytest tests/unit -q --no-header --tb=short
"""


# ============================================================
# 5) run_vitest.cmd — اجرای vitest
# ============================================================

RUN_VITEST = """@echo off
REM run_vitest.cmd — اجرای vitest (frontend tests)

cd /d "%~dp0\\..\\frontend"
if not exist "node_modules\\.bin\\vitest" (
  echo [WARN] frontend node_modules نصب نیست — skip vitest
  exit /b 0
)

call npm test -- --run --reporter=dot
"""


# ============================================================
# 6) install_git_hooks.py — نصب hooks
# ============================================================

INSTALL_GIT_HOOKS = '''# -*- coding: utf-8 -*-
"""
install_git_hooks.py — نصب pre-commit hooks

این اسکریپت:
  ۱. تأیید نصب pre-commit framework
  ۲. اجرای `pre-commit install` در ریشه پروژه
  ۳. تست با `pre-commit run --all-files` (اختیاری)

نکته: نصب pre-commit framework قبلاً در requirements.txt آمده.
ابتدا: pip install -r backend/requirements.txt

استفاده:
  python scripts\\install_git_hooks.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    # تأیید pre-commit
    if shutil.which("pre-commit") is None:
        print("❌ pre-commit نصب نیست.")
        print("📌 ابتدا اجرا کنید:")
        print("   🟦 tab «1 backend»")
        print("     cd backend")
        print("     venv\\\\Scripts\\\\activate")
        print("     pip install pre-commit==3.7.1 black==24.4.2 isort==5.13.2 -i https://mirrors.aliyun.com/pypi/simple/")
        return 1

    # تأیید .pre-commit-config.yaml
    config = ROOT / ".pre-commit-config.yaml"
    if not config.exists():
        print(f"❌ {config} پیدا نشد. اول اسکریپت 54 را اجرا کنید.")
        return 1

    # نصب
    print("📦 نصب pre-commit hook در .git/hooks/...")
    r = subprocess.run(["pre-commit", "install"], cwd=ROOT)
    if r.returncode != 0:
        print("❌ نصب ناموفق")
        return r.returncode

    print()
    print("✅ Pre-commit hooks نصب شد.")
    print()
    print("📌 تست:")
    print("   pre-commit run --all-files")
    print()
    print("📌 bypass در اضطرار:")
    print(\'   git commit --no-verify -m "[skip-hooks: REASON] ..."\')
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


# ============================================================
# 7) PRECOMMIT.md
# ============================================================

PRECOMMIT_DOC = """# Pre-commit Hooks — راهنمای کامل (Hybrid mode)

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
cd D:\\Projects\\trading-system\\backend
venv\\Scripts\\activate
pip install pre-commit==3.7.1 black==24.4.2 isort==5.13.2 -i https://mirrors.aliyun.com/pypi/simple/
```

### نصب hooks در `.git/hooks/`

🟩 **tab «2 scripts»**
```cmd
cd D:\\Projects\\trading-system
python scripts\\install_git_hooks.py
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
venv\\Scripts\\activate
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
venv\\Scripts\\activate
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
python scripts\\check_anti_patterns.py
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
"""


# ============================================================
# helpers
# ============================================================


def write_if_changed(path: Path, content: str) -> bool:
    if path.exists():
        if path.read_text(encoding="utf-8") == content:
            return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


FILES = [
    (".pre-commit-config.yaml", PRECOMMIT_CONFIG),
    ("scripts/check_anti_patterns.py", CHECK_ANTI_PATTERNS),
    ("scripts/run_pytest_unit.cmd", RUN_PYTEST_UNIT),
    ("scripts/run_vitest.cmd", RUN_VITEST),
    ("scripts/install_git_hooks.py", INSTALL_GIT_HOOKS),
    ("docs/PRECOMMIT.md", PRECOMMIT_DOC),
]


def main() -> int:
    print("=" * 64)
    print("  54_setup_precommit_hybrid — pre-commit hooks (T2.06)")
    print("=" * 64)
    print()

    changed, msg = patch_requirements()
    print(f"  {'✏️' if changed else '✓'}  {msg}")

    total = 1 if changed else 0
    for rel, content in FILES:
        if write_if_changed(ROOT / rel, content):
            print(f"  ✏️  {rel}")
            total += 1
        else:
            print(f"  ✓  no-op: {rel}")

    print()
    print("=" * 64)
    if total == 0:
        print("  ✅ idempotent — هیچ تغییری اعمال نشد")
    else:
        print(f"  ✅ موفق — {total} تغییر")
    print("=" * 64)
    print()
    print("📌 گام بعدی:")
    print("   🟦 tab «1 backend» — نصب deps")
    print("     cd backend")
    print("     venv\\Scripts\\activate")
    print(
        "     pip install pre-commit==3.7.1 black==24.4.2 isort==5.13.2 -i https://mirrors.aliyun.com/pypi/simple/"
    )
    print()
    print("   🟩 tab «2 scripts» — نصب hooks")
    print("     python scripts\\install_git_hooks.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
