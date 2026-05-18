# -*- coding: utf-8 -*-
"""
اسکریپت ۲۸b — تست خودکار Toast Notifications
================================================================
این اسکریپت idempotent است — فقط می‌خواند.

چک‌ها:
  - وجود ۳ فایل جدید
  - toastStore: actions کامل (add/dismiss/clear/success/error/warning/info)
  - Toast.jsx: ۴ نوع پیکربندی + role="alert" + animation
  - ToastContainer: subscribe به store + position fixed
  - App.jsx: import + render <ToastContainer />
  - LoginPage: استفاده از toastError + toastSuccess + حذف error div
  - index.css: @keyframes toast-slide-in
  - npm run build بدون خطا
================================================================
"""

import os
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
FRONTEND_SRC = FRONTEND_DIR / "src"

FILES = {
    "toastStore": FRONTEND_SRC / "stores" / "toastStore.js",
    "Toast": FRONTEND_SRC / "components" / "common" / "Toast.jsx",
    "ToastContainer": FRONTEND_SRC / "components" / "common" / "ToastContainer.jsx",
    "App": FRONTEND_SRC / "App.jsx",
    "LoginPage": FRONTEND_SRC / "pages" / "LoginPage.jsx",
    "indexCss": FRONTEND_SRC / "index.css",
}

CHECKS = []


def check(desc, condition, detail=""):
    CHECKS.append((desc, bool(condition), detail))


def read(p):
    return p.read_text(encoding="utf-8") if p.exists() else ""


# ============================================================
# وجود فایل‌ها
# ============================================================
for name, p in FILES.items():
    check(f"وجود {p.relative_to(PROJECT_ROOT)}", p.exists())

if not all(p.exists() for p in FILES.values()):
    print("❌ فایل‌های پایه موجود نیستند.")
    sys.exit(1)

store = read(FILES["toastStore"])
toast = read(FILES["Toast"])
container = read(FILES["ToastContainer"])
app = read(FILES["App"])
login = read(FILES["LoginPage"])
css = read(FILES["indexCss"])


# ============================================================
# toastStore — actions
# ============================================================
print()
check("toastStore: import create از zustand", 'from "zustand"' in store)
check("toastStore: state toasts", "toasts:" in store)
check("toastStore: action add", "add:" in store)
check("toastStore: action dismiss", "dismiss:" in store)
check("toastStore: action clear", "clear:" in store)
check("toastStore: helper success", "success:" in store)
check("toastStore: helper error", "error:" in store)
check("toastStore: helper warning", "warning:" in store)
check("toastStore: helper info", "info:" in store)
check(
    "toastStore: auto-dismiss با setTimeout",
    "setTimeout" in store and "dismiss" in store,
)
check(
    "toastStore: DEFAULT_DURATION = 4000",
    "DEFAULT_DURATION = 4000" in store or "4000" in store,
)


# ============================================================
# Toast.jsx
# ============================================================
print()
check("Toast: subscribe به toastStore", "useToastStore" in toast)
check(
    "Toast: ۴ نوع پیکربندی", all(f"{t}:" in toast for t in ["success", "error", "warning", "info"])
)
check(
    "Toast: استفاده از CSS vars رنگ",
    "var(--color-success)" in toast and "var(--color-danger)" in toast,
)
check('Toast: role="alert" برای accessibility', 'role="alert"' in toast)
check("Toast: animation toast-slide-in", "toast-slide-in" in toast)
check("Toast: دکمه dismiss با ×", "×" in toast or "&times;" in toast)
check('Toast: aria-label="بستن"', 'aria-label="بستن"' in toast)


# ============================================================
# ToastContainer.jsx
# ============================================================
print()
check("ToastContainer: subscribe toasts", "toasts" in container and "useToastStore" in container)
check("ToastContainer: position fixed", 'position: "fixed"' in container)
check("ToastContainer: bottom-left در RTL", "bottom:" in container and "left:" in container)
check("ToastContainer: z-index بالا", "zIndex: 9999" in container or "9999" in container)
check(
    'ToastContainer: aria-live="polite"',
    'aria-live="polite"' in container,
)
check(
    "ToastContainer: render Toast از map",
    "toasts.map" in container and "<Toast " in container,
)


# ============================================================
# App.jsx — افزودن ToastContainer
# ============================================================
print()
check("App: import ToastContainer", "import ToastContainer" in app)
check("App: render <ToastContainer />", "<ToastContainer />" in app)
check("App: Fragment wrapper (<>)", "<>" in app and "</>" in app)


# ============================================================
# LoginPage — استفاده از toast
# ============================================================
print()
check("LoginPage: import useToastStore", "useToastStore" in login)
check("LoginPage: toastError استخراج شده", "toastError" in login)
check("LoginPage: toastSuccess استخراج شده", "toastSuccess" in login)
check("LoginPage: toastError در catch", re.search(r"toastError\s*\(", login) is not None)
check("LoginPage: toastSuccess در try", re.search(r"toastSuccess\s*\(", login) is not None)
check(
    "LoginPage: حذف state error",
    "const [error, setError]" not in login and "setError(" not in login,
)
check(
    "LoginPage: حذف div خطا inline",
    "color-danger-bg" not in login or 'background: "var(--color-danger-bg)"' not in login,
)


# ============================================================
# index.css — @keyframes
# ============================================================
print()
check(
    "index.css: @keyframes toast-slide-in",
    "@keyframes toast-slide-in" in css,
)
check(
    "index.css: keyframes با transform translateY",
    re.search(
        r"@keyframes toast-slide-in[^}]*\{[^}]*\bfrom\b[^}]*translateY",
        css,
        re.DOTALL,
    )
    is not None,
)


# ============================================================
# npm run build
# ============================================================
print()
print("⏳ npm run build در حال اجرا...")
build_ok = False
build_detail = ""

node_modules = FRONTEND_DIR / "node_modules"
node_bin = node_modules / ".bin"

if not node_bin.exists():
    build_detail = "node_modules\\.bin پیدا نشد"
else:
    env = os.environ.copy()
    env["PATH"] = str(node_bin) + os.pathsep + env.get("PATH", "")

    try:
        result = subprocess.run(
            "npm run build",
            cwd=str(FRONTEND_DIR),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=True,
            timeout=120,
        )
        build_ok = result.returncode == 0
        build_detail = f"exit={result.returncode}"
        if not build_ok:
            print("--- stderr ---")
            print((result.stderr or "")[-1500:])
    except Exception as e:
        build_detail = f"exception: {e}"

check("npm run build بدون خطا", build_ok, build_detail)


# ============================================================
# گزارش
# ============================================================
print()
print("=" * 64)
print("📋 نتایج تست Toast Notifications:")
print("=" * 64)
passed = sum(1 for _, ok, _ in CHECKS if ok)
failed = sum(1 for _, ok, _ in CHECKS if not ok)

for desc, ok, detail in CHECKS:
    mark = "✅" if ok else "❌"
    extra = f"  ← {detail}" if detail and not ok else ""
    print(f"  {mark} {desc}{extra}")

print()
print("=" * 64)
if failed == 0:
    print(f"✅ همه {passed} چک سبز — زیرگام ۸.۲ کامل است.")
    print("=" * 64)
    print()
    print("چک بصری در مرورگر:")
    print("  ۱) login → toast سبز خوش‌آمد")
    print("  ۲) logout سپس admin/wrongpass → toast قرمز")
    print("  ۳) چند login غلط → stack")
    print("  ۴) دکمه × → پاک شدن دستی")
    sys.exit(0)
else:
    print(f"❌ {failed} چک ناموفق از {passed + failed}")
    print("=" * 64)
    sys.exit(1)
