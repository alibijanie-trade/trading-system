# -*- coding: utf-8 -*-
"""
اسکریپت ۳۴b — تست خودکار اصلاحیه ۳۴ (.env.example audit)
================================================================
طبق قانون #۲۲ سند v2.7 — هر اسکریپت {N}_*.py باید
{N}b_test_*.py همراه داشته باشد.

پوشش تست (static checks، بدون نیاز به Node یا venv):

  Section A — backend/.env.example
    ۱) فایل وجود دارد
    ۲) با header comment شروع می‌شود
    ۳) همه کلیدهای required از config.py (Settings class) موجودند
    ۴) همه کلیدهای optional از config.py موجودند
    ۵) APP_VERSION با CHANGELOG.md همخوان است
    ۶) SECRET_KEY مقدار placeholder دارد (نه کلید واقعی)
    ۷) ENCRYPTION_KEY مقدار placeholder دارد
    ۸) دستورالعمل تولید SECRET_KEY در کامنت‌ها هست
    ۹) دستورالعمل تولید ENCRYPTION_KEY در کامنت‌ها هست
    ۱۰) Drift detector: کلید جدید در config.py که در .env.example نباشد

  Section B — frontend/.env.example
    ۱) فایل وجود دارد
    ۲) با header comment شروع می‌شود
    ۳) VITE_API_URL موجود است
    ۴) هشدار امنیتی Vite در کامنت ذکر شده
    ۵) Drift detector: همه VITE_* استفاده‌شده در src/ موجود باشند

  Section C — Cross-validation
    ۱) backend/.env (state کاربر) دست‌نخورده باقی مانده
       — یعنی هنوز SECRET_KEY و ENCRYPTION_KEY واقعی دارد
       (یا اگر فایل غایب است، پیام راهنما)

  Section D — Git safety
    ۱) .gitignore دارد .env را ignore می‌کند
    ۲) .gitignore دارد .env.example را ignore *نمی‌کند*

نحوه اجرا:
    python scripts/34b_test_env_examples.py
================================================================
"""

import ast
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
BACKEND = PROJECT_ROOT / "backend"
FRONTEND = PROJECT_ROOT / "frontend"

BACKEND_ENV_EXAMPLE = BACKEND / ".env.example"
BACKEND_ENV         = BACKEND / ".env"
BACKEND_CONFIG_PY   = BACKEND / "app" / "core" / "config.py"

FRONTEND_ENV_EXAMPLE = FRONTEND / ".env.example"
FRONTEND_SRC         = FRONTEND / "src"

CHANGELOG = PROJECT_ROOT / "CHANGELOG.md"
GITIGNORE = PROJECT_ROOT / ".gitignore"


# ────────────────────────────────────────────────────────────────
# Checks utility (همان pattern اسکریپت‌های قبلی)
# ────────────────────────────────────────────────────────────────
class Checks:
    def __init__(self):
        self.results = []
        self._section = ""

    def section(self, name):
        self._section = name
        print()
        print(f"--- {name} ---")

    def add(self, name, ok, detail=""):
        full_name = f"[{self._section}] {name}" if self._section else name
        self.results.append((full_name, ok, detail))
        mark = "✅" if ok else "❌"
        print(f"  {mark} {name}")
        if not ok and detail:
            print(f"     ↳ {detail}")

    @property
    def passed(self):
        return sum(1 for _, ok, _ in self.results if ok)

    @property
    def failed(self):
        return sum(1 for _, ok, _ in self.results if not ok)

    @property
    def all_pass(self):
        return self.failed == 0


# ────────────────────────────────────────────────────────────────
# Helper: استخراج کلیدهای Settings از config.py با AST
# ────────────────────────────────────────────────────────────────
def extract_settings_fields(config_py_path: Path) -> tuple[set[str], set[str]]:
    """
    با AST، فیلدهای کلاس Settings را استخراج می‌کند.

    Returns:
      (required_fields, optional_fields)
      — required: فیلدهای بدون مقدار پیش‌فرض (مثل SECRET_KEY: str)
      — optional: فیلدهای با مقدار پیش‌فرض (مثل APP_ENV: ... = "development")

    فیلدهای computed (با @property) نادیده گرفته می‌شوند.
    """
    src = config_py_path.read_text(encoding="utf-8")
    tree = ast.parse(src)

    required: set[str] = set()
    optional: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "Settings":
            for stmt in node.body:
                # AnnAssign = یک خط مثل `SECRET_KEY: str` یا `APP_ENV: ... = "..."`
                if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                    name = stmt.target.id
                    # نام‌های UPPER_CASE = فیلدهای BaseSettings
                    if not name.isupper() and "_" not in name:
                        continue
                    if not (name[0].isupper() or name.startswith("_")):
                        continue
                    if stmt.value is None:
                        required.add(name)
                    else:
                        optional.add(name)
    return required, optional


# ────────────────────────────────────────────────────────────────
# Helper: استخراج کلیدها از فایل .env-style
# ────────────────────────────────────────────────────────────────
KEY_LINE = re.compile(r"^([A-Z][A-Z0-9_]*)\s*=\s*(.*)$", re.MULTILINE)


def parse_env_keys(content: str) -> dict[str, str]:
    """
    فقط خطوط بدون کامنت (نه `# KEY=value`) را برمی‌گرداند.
    """
    keys: dict[str, str] = {}
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        m = re.match(r"^([A-Z][A-Z0-9_]*)\s*=\s*(.*)$", stripped)
        if m:
            keys[m.group(1)] = m.group(2)
    return keys


# ────────────────────────────────────────────────────────────────
# Helper: استخراج VITE_* استفاده‌شده در frontend/src
# ────────────────────────────────────────────────────────────────
VITE_USAGE = re.compile(r"import\.meta\.env\.(VITE_[A-Z0-9_]+)")


def find_vite_keys_in_src(src_dir: Path) -> set[str]:
    keys: set[str] = set()
    if not src_dir.exists():
        return keys
    for path in src_dir.rglob("*.*"):
        if path.suffix not in (".js", ".jsx", ".ts", ".tsx"):
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for m in VITE_USAGE.finditer(content):
            keys.add(m.group(1))
    return keys


# ────────────────────────────────────────────────────────────────
# Helper: نسخه از CHANGELOG
# ────────────────────────────────────────────────────────────────
CHANGELOG_VERSION = re.compile(r"^## \[(\d+\.\d+\.\d+)\]", re.MULTILINE)


def latest_changelog_version(changelog_path: Path) -> str | None:
    if not changelog_path.exists():
        return None
    content = changelog_path.read_text(encoding="utf-8")
    m = CHANGELOG_VERSION.search(content)
    return m.group(1) if m else None


# ────────────────────────────────────────────────────────────────
# Sections
# ────────────────────────────────────────────────────────────────
def section_a_backend(c: Checks):
    c.section("A) backend/.env.example")

    # 1) وجود
    exists = BACKEND_ENV_EXAMPLE.exists()
    c.add("فایل موجود است", exists, str(BACKEND_ENV_EXAMPLE))
    if not exists:
        return

    content = BACKEND_ENV_EXAMPLE.read_text(encoding="utf-8")

    # 2) Header comment
    first_line = content.splitlines()[0] if content else ""
    c.add(
        "با header comment شروع می‌شود",
        first_line.startswith("#"),
        f"اولین خط: {first_line[:60]!r}",
    )

    # کلیدها از config.py
    if not BACKEND_CONFIG_PY.exists():
        c.add("config.py موجود برای drift detection", False, str(BACKEND_CONFIG_PY))
        return
    try:
        required, optional = extract_settings_fields(BACKEND_CONFIG_PY)
    except Exception as e:
        c.add("AST parse config.py", False, str(e))
        return
    c.add(
        "AST parse config.py موفق",
        True,
        f"required={len(required)}, optional={len(optional)}",
    )

    env_keys = parse_env_keys(content)

    # 3) Required keys
    missing_required = required - env_keys.keys()
    c.add(
        f"همه کلیدهای required موجود ({len(required)})",
        not missing_required,
        f"غایب: {sorted(missing_required)}" if missing_required else "",
    )

    # 4) Optional keys
    missing_optional = optional - env_keys.keys()
    c.add(
        f"همه کلیدهای optional موجود ({len(optional)})",
        not missing_optional,
        f"غایب: {sorted(missing_optional)}" if missing_optional else "",
    )

    # 5) APP_VERSION matches CHANGELOG
    cl_version = latest_changelog_version(CHANGELOG)
    if cl_version:
        env_version = env_keys.get("APP_VERSION", "").strip('"').strip("'")
        c.add(
            f"APP_VERSION = {cl_version} (همگام با CHANGELOG)",
            env_version == cl_version,
            f"در .env.example: {env_version!r}، در CHANGELOG: {cl_version!r}",
        )
    else:
        c.add("CHANGELOG نسخه دارد", False, "هیچ ## [X.Y.Z] پیدا نشد")

    # 6,7) Placeholder values for sensitive keys
    sk = env_keys.get("SECRET_KEY", "")
    c.add(
        "SECRET_KEY مقدار placeholder دارد",
        "replace" in sk.lower() or "your" in sk.lower() or "example" in sk.lower(),
        f"مقدار: {sk!r}",
    )
    ek = env_keys.get("ENCRYPTION_KEY", "")
    c.add(
        "ENCRYPTION_KEY مقدار placeholder دارد",
        "replace" in ek.lower() or "your" in ek.lower() or "example" in ek.lower(),
        f"مقدار: {ek!r}",
    )

    # 8,9) دستورالعمل تولید کلیدها در کامنت
    c.add(
        "راهنمای تولید SECRET_KEY (secrets.token_urlsafe) در کامنت",
        "secrets.token_urlsafe" in content,
        "",
    )
    c.add(
        "راهنمای تولید ENCRYPTION_KEY (Fernet.generate_key) در کامنت",
        "Fernet.generate_key" in content,
        "",
    )

    # 10) Drift detector — کلید اضافه/کم
    expected = required | optional
    actual = set(env_keys.keys())
    only_in_config = expected - actual
    only_in_example = actual - expected
    # only_in_example می‌تواند کلیدهای آینده (Exchange API) باشد — ولی commented
    # طبق طراحی، اگر uncommented باشد، باید در config باشد
    drift_ok = not only_in_config
    c.add(
        "Drift: همه فیلدهای Settings در .env.example هستند",
        drift_ok,
        f"فقط در config: {sorted(only_in_config)}" if only_in_config else "",
    )


def section_b_frontend(c: Checks):
    c.section("B) frontend/.env.example")

    # 1) وجود
    exists = FRONTEND_ENV_EXAMPLE.exists()
    c.add("فایل موجود است", exists, str(FRONTEND_ENV_EXAMPLE))
    if not exists:
        return

    content = FRONTEND_ENV_EXAMPLE.read_text(encoding="utf-8")

    # 2) Header comment
    first_line = content.splitlines()[0] if content else ""
    c.add(
        "با header comment شروع می‌شود",
        first_line.startswith("#"),
        f"اولین خط: {first_line[:60]!r}",
    )

    env_keys = parse_env_keys(content)

    # 3) VITE_API_URL موجود
    c.add(
        "VITE_API_URL موجود است",
        "VITE_API_URL" in env_keys,
        f"کلیدهای موجود: {sorted(env_keys.keys())}",
    )

    # 4) هشدار امنیتی Vite
    has_security_warning = (
        "VITE_" in content
        and ("امنیت" in content or "security" in content.lower() or "حساس" in content)
    )
    c.add(
        "هشدار امنیتی Vite (prefix VITE_) در کامنت ذکر شده",
        has_security_warning,
        "",
    )

    # 5) Drift detector — VITE_* استفاده‌شده در کد
    src_keys = find_vite_keys_in_src(FRONTEND_SRC)
    if src_keys:
        missing_in_example = src_keys - set(env_keys.keys())
        c.add(
            f"همه VITE_* استفاده‌شده در src/ ({len(src_keys)}) در .env.example هستند",
            not missing_in_example,
            f"غایب: {sorted(missing_in_example)}" if missing_in_example else "",
        )
    else:
        c.add("کلیدی VITE_ در src/ پیدا نشد (نه fail نه pass)", True, "skipped")


def section_c_user_state(c: Checks):
    c.section("C) Cross-validation — backend/.env کاربر دست‌نخورده")

    if not BACKEND_ENV.exists():
        c.add(
            "backend/.env موجود",
            True,
            "غایب — این OK است (در .gitignore، توسط 00b ساخته می‌شود). skipping further checks.",
        )
        return

    content = BACKEND_ENV.read_text(encoding="utf-8")
    env_keys = parse_env_keys(content)

    sk = env_keys.get("SECRET_KEY", "")
    ek = env_keys.get("ENCRYPTION_KEY", "")

    # SECRET_KEY باید واقعی باشد (نه placeholder)
    c.add(
        "SECRET_KEY در .env کاربر مقدار واقعی دارد (نه placeholder)",
        bool(sk) and "replace" not in sk.lower() and len(sk) >= 32,
        f"طول: {len(sk)}",
    )
    # ENCRYPTION_KEY باید Fernet 44-char باشد
    c.add(
        "ENCRYPTION_KEY در .env کاربر طول مناسب دارد",
        bool(ek) and "replace" not in ek.lower() and len(ek) >= 32,
        f"طول: {len(ek)}",
    )


def section_d_gitignore(c: Checks):
    c.section("D) Git safety — .gitignore")

    if not GITIGNORE.exists():
        c.add(".gitignore موجود است", False, str(GITIGNORE))
        return

    content = GITIGNORE.read_text(encoding="utf-8")

    # باید .env ignore شود
    # نکته: ".env" در یک خط (نه فقط بخشی از .env.local)
    lines = [ln.strip() for ln in content.splitlines()]
    has_dotenv_ignore = ".env" in lines or "/.env" in lines
    c.add(
        ".env در .gitignore ignore شده",
        has_dotenv_ignore,
        f"خطوط مرتبط: {[ln for ln in lines if 'env' in ln.lower()][:5]}",
    )

    # نباید .env.example را ignore کند
    # الگوهای ignore این پروژه: ".env", ".env.local", ".env.*.local", "*.env"
    # هیچ‌کدام .env.example را مچ نمی‌کنند، ولی برای اطمینان چک می‌کنیم:
    bad_patterns = [
        ".env.example",
        "*.example",
        "**/.env*",  # خیلی broad
    ]
    blocking = [p for p in bad_patterns if p in lines]
    c.add(
        ".env.example را ignore نمی‌کند",
        not blocking,
        f"الگوهای مشکل‌ساز: {blocking}" if blocking else "",
    )


# ────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────
def main() -> int:
    print("=" * 64)
    print("اسکریپت ۳۴b — تست .env.example audit")
    print("=" * 64)

    c = Checks()
    section_a_backend(c)
    section_b_frontend(c)
    section_c_user_state(c)
    section_d_gitignore(c)

    print()
    print("=" * 64)
    print(f"خلاصه: {c.passed} ✅   |   {c.failed} ❌   |   جمع: {len(c.results)}")
    print("=" * 64)

    return 0 if c.all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
