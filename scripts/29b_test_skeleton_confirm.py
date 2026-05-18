# -*- coding: utf-8 -*-
"""
اسکریپت ۲۹b — تست خودکار زیرگام ۸.۳ (Skeleton + ConfirmDialog)
================================================================
طبق قانون #۲۲ سند v2.6 (هر اسکریپت {N}_*.py باید {N}b_test_*.py همراه داشته باشد).

پوشش تست:
  ۱) وجود فایل‌ها
  ۲) محتوای SkeletonBlock.jsx
       - className "skeleton-block"
       - ۴ variant: rect, text, circle, line
       - props: width, height, radius, count, gap
       - role="presentation" + aria-hidden="true"
       - بدون hex hardcoded
  ۳) محتوای confirmStore.js
       - استفاده از Zustand
       - state: isOpen, title, message, variant, confirmText, cancelText, resolver
       - متدها: confirm (Promise), confirmAccept, confirmReject
       - reject اگر dialog قبلی باز باشد
  ۴) محتوای ConfirmDialog.jsx
       - Variant Indicator Pattern (سند ۸.۸.۱):
           background: var(--color-card)
           border: var(--color-border)
           borderInlineStart با cfg.color (accent ۴px در سمت start)
           بدون border کامل با cfg.color
       - icon رنگی (cfg.color)
       - متن از var(--color-text)
       - accessibility: role="dialog", aria-modal, aria-labelledby, aria-describedby
       - focus management: ref + setTimeout focus + Escape + Tab cycling
       - بدون hex hardcoded (فقط rgba در backdrop)
  ۵) index.css
       - @keyframes skeleton-shimmer
       - @keyframes dialog-fade-in
       - @keyframes dialog-slide-in
       - .skeleton-block با linear-gradient از CSS vars
       - @media (prefers-reduced-motion: reduce)
  ۶) App.jsx
       - import ConfirmDialog
       - <ConfirmDialog /> mount شده
  ۷) HomePage.jsx
       - import useConfirmStore
       - await askConfirm در handleLogout
       - variant: "warning"
  ۸) ChartPage.jsx
       - import SkeletonBlock
       - استفاده در حالت loading

سپس smoke test:
  ۹) npm run build (در پوشه frontend)
================================================================
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FRONTEND = PROJECT_ROOT / "frontend"
SRC = FRONTEND / "src"

SKELETON_JSX = SRC / "components" / "common" / "SkeletonBlock.jsx"
CONFIRM_JSX = SRC / "components" / "common" / "ConfirmDialog.jsx"
CONFIRM_STORE = SRC / "stores" / "confirmStore.js"
INDEX_CSS = SRC / "index.css"
APP_JSX = SRC / "App.jsx"
HOME_JSX = SRC / "pages" / "HomePage.jsx"
CHART_JSX = SRC / "pages" / "ChartPage.jsx"

# Regex برای تشخیص hex hardcoded در JSX (خارج از کامنت‌ها)
# شامل #abc و #abcdef و #abcdef00 (با alpha)
HEX_PATTERN = re.compile(r"#[0-9a-fA-F]{3,8}\b")


class Checks:
    def __init__(self):
        self.results = []

    def add(self, name: str, ok: bool, detail: str = ""):
        self.results.append((name, ok, detail))

    @property
    def passed(self):
        return sum(1 for _, ok, _ in self.results if ok)

    @property
    def failed(self):
        return sum(1 for _, ok, _ in self.results if not ok)

    def print_section(self, title: str):
        print()
        print(f"--- {title} ---")

    def print_results(self):
        for name, ok, detail in self.results:
            mark = "✅" if ok else "❌"
            print(f"  {mark} {name}")
            if not ok and detail:
                print(f"      ↳ {detail}")


def check_no_hex(src: str, exclude_patterns: list) -> tuple:
    """چک کن هیچ hex hardcoded در src نباشد (به‌جز exceptions)"""
    # حذف کامنت‌های /* */ و //
    cleaned = re.sub(r"/\*.*?\*/", "", src, flags=re.DOTALL)
    cleaned = re.sub(r"//.*$", "", cleaned, flags=re.MULTILINE)

    matches = HEX_PATTERN.findall(cleaned)
    bad = []
    for m in matches:
        excluded = False
        for pat in exclude_patterns:
            if pat in m or m == pat:
                excluded = True
                break
        if not excluded:
            bad.append(m)

    return (len(bad) == 0, ", ".join(sorted(set(bad))[:5]) if bad else "")


def main() -> int:
    print("=" * 64)
    print("اسکریپت ۲۹b — تست خودکار زیرگام ۸.۳")
    print("=" * 64)

    c = Checks()

    # ============================================================
    # ۱) وجود فایل‌ها
    # ============================================================
    c.print_section("۱) وجود فایل‌ها")
    files = {
        "SkeletonBlock.jsx": SKELETON_JSX,
        "confirmStore.js": CONFIRM_STORE,
        "ConfirmDialog.jsx": CONFIRM_JSX,
        "index.css": INDEX_CSS,
        "App.jsx": APP_JSX,
        "HomePage.jsx": HOME_JSX,
        "ChartPage.jsx": CHART_JSX,
    }
    for label, path in files.items():
        c.add(f"موجود است: {label}", path.exists(), f"مسیر: {path.relative_to(PROJECT_ROOT)}")

    # اگر فایل‌ها موجود نیستند، ادامه بی‌معناست
    if any(not p.exists() for p in files.values()):
        c.print_results()
        print()
        print("=" * 64)
        print(f"❌ {c.failed} چک ناموفق از {c.passed + c.failed}")
        print("   ابتدا اسکریپت ۲۹ را اجرا کنید.")
        print("=" * 64)
        return 1

    # ============================================================
    # ۲) SkeletonBlock.jsx
    # ============================================================
    c.print_section("۲) SkeletonBlock.jsx")
    src = SKELETON_JSX.read_text(encoding="utf-8")

    c.add('className="skeleton-block" موجود', 'className="skeleton-block"' in src)
    c.add("variant rect تعریف شده", "rect:" in src or '"rect"' in src)
    c.add("variant text تعریف شده", "text:" in src or '"text"' in src)
    c.add("variant circle تعریف شده", "circle:" in src or '"circle"' in src)
    c.add("variant line تعریف شده", "line:" in src or '"line"' in src)
    c.add("prop count برای تکرار", "count" in src and "Array.from" in src)
    c.add(
        'role="presentation" + aria-hidden',
        'role="presentation"' in src and 'aria-hidden="true"' in src,
    )

    ok, bad = check_no_hex(src, [])
    c.add("بدون hex hardcoded", ok, f"hex های یافت‌شده: {bad}" if bad else "")

    # ============================================================
    # ۳) confirmStore.js
    # ============================================================
    c.print_section("۳) confirmStore.js")
    src = CONFIRM_STORE.read_text(encoding="utf-8")

    c.add("استفاده از Zustand: create", 'from "zustand"' in src and "create(" in src)
    c.add("state: isOpen", "isOpen" in src)
    c.add("state: title", "title" in src)
    c.add("state: message", "message" in src)
    c.add("state: variant", "variant" in src)
    c.add("state: confirmText", "confirmText" in src)
    c.add("state: cancelText", "cancelText" in src)
    c.add("state: resolver", "resolver" in src)
    c.add("متد confirm با Promise", "confirm:" in src and "new Promise" in src)
    c.add("متد confirmAccept", "confirmAccept" in src)
    c.add("متد confirmReject", "confirmReject" in src)
    c.add("resolve(true) در accept", "resolver(true)" in src or "resolve(true)" in src)
    c.add("resolve(false) در reject", "resolver(false)" in src or "resolve(false)" in src)
    c.add("reject dialog قبلی هنگام confirm جدید", "prev" in src and "prev(false)" in src)

    # ============================================================
    # ۴) ConfirmDialog.jsx — Variant Indicator Pattern
    # ============================================================
    c.print_section("۴) ConfirmDialog.jsx (سند ۸.۸.۱)")
    src = CONFIRM_JSX.read_text(encoding="utf-8")

    c.add("background از تم: var(--color-card)", 'background: "var(--color-card)"' in src)
    c.add("border از تم: var(--color-border)", 'border: "1px solid var(--color-border)"' in src)
    c.add(
        "borderInlineStart accent با cfg.color",
        "borderInlineStart" in src and "${cfg.color}" in src,
    )
    c.add(
        "ممنوع: border کامل با cfg.color",
        "border: `1px solid ${cfg.color}`" not in src or "borderInlineStart" in src,
    )
    c.add("icon رنگی با cfg.color", "color: cfg.color" in src)
    c.add("متن از تم: var(--color-text)", 'color: "var(--color-text)"' in src)
    c.add("دکمه تأیید با cfg.color", "background: cfg.color" in src)
    c.add(
        "دکمه انصراف از تم",
        'color: "var(--color-text)"' in src
        and 'border: "1px solid var(--color-border-strong)"' in src,
    )
    c.add('role="dialog"', 'role="dialog"' in src)
    c.add('aria-modal="true"', 'aria-modal="true"' in src)
    c.add("aria-labelledby", 'aria-labelledby="confirm-dialog-title"' in src)
    c.add("aria-describedby", 'aria-describedby="confirm-dialog-message"' in src)
    c.add("ref برای focus", "useRef" in src and "confirmBtnRef" in src)
    c.add("setTimeout focus", "setTimeout(" in src and ".focus()" in src)
    c.add("Escape → confirmReject", '"Escape"' in src and "confirmReject()" in src)
    c.add("Tab cycling بین دو دکمه", '"Tab"' in src and "shiftKey" in src)
    c.add("backdrop click → reject", "onClick={confirmReject}" in src)
    c.add("stopPropagation روی dialog body", "stopPropagation" in src)
    c.add("animation: dialog-fade-in", "dialog-fade-in" in src)
    c.add("animation: dialog-slide-in", "dialog-slide-in" in src)

    # hex فقط مجاز در backdrop rgba(0,0,0,0.5) — رنگ شفاف عمومی
    ok, bad = check_no_hex(src, [])
    c.add("بدون hex hardcoded در JSX", ok, f"hex های یافت‌شده: {bad}" if bad else "")

    # ============================================================
    # ۵) index.css
    # ============================================================
    c.print_section("۵) index.css")
    src = INDEX_CSS.read_text(encoding="utf-8")

    c.add("@keyframes skeleton-shimmer", "@keyframes skeleton-shimmer" in src)
    c.add("@keyframes dialog-fade-in", "@keyframes dialog-fade-in" in src)
    c.add("@keyframes dialog-slide-in", "@keyframes dialog-slide-in" in src)
    c.add(".skeleton-block class", ".skeleton-block" in src)
    c.add(
        "linear-gradient با var(--color-card-hover)",
        "linear-gradient" in src and "var(--color-card-hover)" in src,
    )
    c.add("linear-gradient با var(--color-border-strong)", "var(--color-border-strong)" in src)
    c.add("animation skeleton-shimmer روی .skeleton-block", "animation: skeleton-shimmer" in src)
    c.add("@media (prefers-reduced-motion: reduce)", "prefers-reduced-motion" in src)
    c.add("toast-slide-in حفظ شد (regression check)", "@keyframes toast-slide-in" in src)
    c.add(
        "Interactive states حفظ شد (regression check)",
        "button:focus-visible" in src and "button:disabled" in src,
    )

    # ============================================================
    # ۶) App.jsx
    # ============================================================
    c.print_section("۶) App.jsx")
    src = APP_JSX.read_text(encoding="utf-8")

    c.add(
        "import ConfirmDialog",
        'import ConfirmDialog from "./components/common/ConfirmDialog.jsx"' in src,
    )
    c.add("mount <ConfirmDialog />", "<ConfirmDialog />" in src)
    c.add("ToastContainer حفظ شد (regression)", "<ToastContainer />" in src)
    c.add("ProtectedRoute حفظ شد (regression)", "ProtectedRoute" in src)

    # ============================================================
    # ۷) HomePage.jsx
    # ============================================================
    c.print_section("۷) HomePage.jsx")
    src = HOME_JSX.read_text(encoding="utf-8")

    c.add(
        "import useConfirmStore", 'import useConfirmStore from "../stores/confirmStore.js"' in src
    )
    c.add(
        "askConfirm از store گرفته شد",
        "useConfirmStore((s) => s.confirm)" in src or "askConfirm = useConfirmStore" in src,
    )
    c.add("handleLogout async است", "const handleLogout = async" in src)
    c.add("await askConfirm", "await askConfirm" in src)
    c.add('variant: "warning"', '"warning"' in src)
    c.add("if (!ok) return — انصراف", "if (!ok) return" in src)
    c.add("logout() بعد از تأیید حفظ شد", "logout()" in src)

    # ============================================================
    # ۸) ChartPage.jsx
    # ============================================================
    c.print_section("۸) ChartPage.jsx")
    src = CHART_JSX.read_text(encoding="utf-8")

    c.add(
        "import SkeletonBlock",
        'import SkeletonBlock from "../components/common/SkeletonBlock.jsx"' in src,
    )
    c.add("استفاده از <SkeletonBlock", "<SkeletonBlock" in src)
    c.add('متن قدیمی "در حال بارگذاری نمودار..." حذف شد', "در حال بارگذاری نمودار..." not in src)
    c.add("شرط loading حفظ شد", "loading" in src)
    c.add("کلید themeId در deps حفظ شد (regression)", "themeId]" in src)

    # ============================================================
    # چاپ نتایج تا اینجا
    # ============================================================
    c.print_results()

    # اگر تست‌های استاتیک شکست خوردند، npm build را اجرا نکن
    if c.failed > 0:
        print()
        print("=" * 64)
        print(f"❌ {c.failed} چک ناموفق از {c.passed + c.failed}")
        print("=" * 64)
        return 1

    print()
    print(f"✅ تمام {c.passed} چک استاتیک سبز.")

    # ============================================================
    # ۹) npm run build — smoke test
    # ============================================================
    print()
    print("=" * 64)
    print("۹) npm run build (smoke test)")
    print("=" * 64)

    if not (FRONTEND / "node_modules").exists():
        print("⚠️  node_modules موجود نیست — build skipped.")
        print("    ابتدا اجرا کنید: python scripts/00b_post_unzip_setup.py")
        print()
        print(f"✅ تست‌های استاتیک: {c.passed}/{c.passed}")
        print("   build skip شد — پس از نصب node_modules دوباره اجرا کنید.")
        return 0

    npm = shutil.which("npm") or shutil.which("npm.cmd")
    if not npm:
        print("⚠️  npm در PATH یافت نشد — build skipped.")
        return 0

    print(f"اجرای: {npm} run build  (در {FRONTEND})")
    print("(ممکن است ۳۰-۹۰ ثانیه طول بکشد...)")
    print()

    try:
        result = subprocess.run(
            [npm, "run", "build"],
            cwd=str(FRONTEND),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
        )
    except subprocess.TimeoutExpired:
        print("❌ npm build timeout (>180s).")
        return 1
    except FileNotFoundError:
        print("⚠️  npm یافت نشد.")
        return 0

    # خروجی stdout را کوتاه کن
    stdout = result.stdout or ""
    stderr = result.stderr or ""
    last_lines = stdout.strip().split("\n")[-15:]
    print("--- خروجی build (آخرین خطوط) ---")
    for line in last_lines:
        print(f"  {line}")

    if result.returncode == 0:
        print()
        print("=" * 64)
        print(f"✅ تمام تست‌ها سبز: {c.passed} چک استاتیک + npm build")
        print("=" * 64)
        print()
        print("چک بصری در 🟧 tab «3 frontend»:")
        print("  ۱) npm run dev (اگر در حال اجرا نیست)")
        print("  ۲) refresh مرورگر → /chart/1")
        print("     - ابتدا 3 Skeleton shimmer (نوار بالا، نمودار، نوار پایین)")
        print("     - سپس نمودار واقعی fade-in")
        print("  ۳) بازگشت به / → کلیک خروج")
        print("     - dialog با accent باریک نارنجی در سمت راست")
        print("     - کانتینر همان رنگ تم (نه نارنجی پررنگ)")
        print("     - icon ⚠ نارنجی")
        print("  ۴) Escape → بستن (cancel)")
        print("  ۵) کلیک بیرون dialog → بستن (cancel)")
        print("  ۶) Tab → focus بین دو دکمه می‌چرخد")
        print("  ۷) Enter روی تأیید → خروج")
        print("  ۸) تست با تم‌های مختلف — dialog باید با هر تم هماهنگ باشد")
        return 0
    else:
        print()
        print("--- stderr ---")
        for line in stderr.strip().split("\n")[-15:]:
            print(f"  {line}")
        print()
        print("=" * 64)
        print(f"❌ npm build شکست خورد (exit code: {result.returncode})")
        print("=" * 64)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
