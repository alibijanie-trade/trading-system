# -*- coding: utf-8 -*-
"""
اسکریپت ۲۷c — اصلاح تم binance-dark با رنگ‌های واقعی بایننس
================================================================
این اسکریپت idempotent است.

مشکل: در اسکریپت ۲۷ نام تم "binance-dark" بود ولی رنگ‌ها از TradingView گرفته شده.
علت: ChartPage از lightweight-charts (محصول TradingView) استفاده می‌کرد و من رنگ‌های
     آن را به اشتباه به‌عنوان "بایننس" پنداشتم.

تغییرات:
  1. themes.js  → فقط بلوک "binance-dark" بازنویسی می‌شود (۴ تم دیگر دست‌نخورده)
  2. index.css  → :root fallback به مقادیر صحیح بایننس به‌روز می‌شود

رنگ‌های اصلاح‌شده:
  --color-bg:           #1e222d  →  #181A20  (تیره‌تر، مشکی‌تر)
  --color-card:         #2a2e39  →  #1E2329  (Binance elevated)
  --color-border:       #363a45  →  #2B3139  (نازک‌تر)
  --color-text:         #d1d4dc  →  #EAECEF  (تیزتر)
  --color-text-muted:   #787b86  →  #848E9C  (Binance secondary)
  --color-success:      #26a69a  →  #0ECB81  (سبز خالص بایننس)
  --color-danger:       #ef5350  →  #F6465D  (قرمز-صورتی بایننس)
  --color-link:         #2962ff  →  #F0B90B  ⭐ مهم‌ترین: طلایی به جای آبی
================================================================
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FRONTEND_SRC = PROJECT_ROOT / "frontend" / "src"
THEMES_JS = FRONTEND_SRC / "themes" / "themes.js"
INDEX_CSS = FRONTEND_SRC / "index.css"


# ============================================================
# بلوک جدید binance-dark — دقیقاً مطابق رنگ‌های رسمی بایننس
# ============================================================
NEW_BINANCE_BLOCK = """  "binance-dark": {
    id: "binance-dark",
    name: "بایننس تاریک",
    isDark: true,
    vars: {
      "--color-primary": "#F0B90B",
      "--color-primary-hover": "#FCD535",
      "--color-bg": "#181A20",
      "--color-bg-elevated": "#1E2329",
      "--color-card": "#1E2329",
      "--color-card-hover": "#2B2F36",
      "--color-border": "#2B3139",
      "--color-border-strong": "#474D57",
      "--color-text": "#EAECEF",
      "--color-text-muted": "#848E9C",
      "--color-text-inverse": "#181A20",
      "--color-success": "#0ECB81",
      "--color-success-bg": "#0F2A1F",
      "--color-danger": "#F6465D",
      "--color-danger-bg": "#2A1517",
      "--color-info": "#1890FF",
      "--color-warning": "#F0B90B",
      "--color-link": "#F0B90B",
      "--color-grid": "#2B3139",
      "--shadow-card": "0 4px 12px rgba(0,0,0,0.5)",
    },
  },"""


# ============================================================
# index.css جدید — :root fallback با رنگ‌های بایننس
# ============================================================
NEW_INDEX_CSS = """/* ============================================================
   Reset + پایه — زیرگام ۸ (Theme Engine)
   متغیرهای CSS توسط ThemeProvider روی :root تزریق می‌شوند.
   مقادیر :root زیر صرفاً fallback اولیه‌اند (پیش از mount).
   🆕 ۲۷c — رنگ‌های fallback به استانداردهای رسمی بایننس اصلاح شد.
   ============================================================ */

:root {
  /* رنگ‌ها — fallback بایننس واقعی (پیش از تزریق ThemeProvider) */
  --color-primary: #F0B90B;
  --color-primary-hover: #FCD535;
  --color-bg: #181A20;
  --color-bg-elevated: #1E2329;
  --color-card: #1E2329;
  --color-card-hover: #2B2F36;
  --color-border: #2B3139;
  --color-border-strong: #474D57;
  --color-text: #EAECEF;
  --color-text-muted: #848E9C;
  --color-text-inverse: #181A20;
  --color-success: #0ECB81;
  --color-success-bg: #0F2A1F;
  --color-danger: #F6465D;
  --color-danger-bg: #2A1517;
  --color-info: #1890FF;
  --color-warning: #F0B90B;
  --color-link: #F0B90B;
  --color-grid: #2B3139;
  --shadow-card: 0 4px 12px rgba(0,0,0,0.5);

  /* تایپوگرافی */
  --font-size-base: 14px;
  --font-family-ui: "Vazirmatn", "Segoe UI", system-ui, -apple-system, sans-serif;
}

*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body, #root {
  min-height: 100vh;
}

body {
  font-family: var(--font-family-ui);
  font-size: var(--font-size-base);
  line-height: 1.6;
  background: var(--color-bg);
  color: var(--color-text);
  direction: rtl;
  transition: background-color 0.2s ease, color 0.2s ease;
}

button {
  cursor: pointer;
  font-family: inherit;
  font-size: inherit;
  border: none;
  outline: none;
  background: transparent;
  color: inherit;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

a {
  color: var(--color-link);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

input, select, textarea {
  font-family: inherit;
  font-size: inherit;
  outline: none;
  background: transparent;
  color: inherit;
}

/* اسکرول‌بار سفارشی — هماهنگ با تم */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--color-bg); }
::-webkit-scrollbar-thumb {
  background: var(--color-border-strong);
  border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover { background: var(--color-text-muted); }
"""


def replace_binance_block(themes_src: str) -> tuple[str, bool]:
    """
    بلوک "binance-dark" را به‌صورت idempotent جایگزین می‌کند.
    خروجی: (متن جدید, آیا تغییر کرد)
    """
    import re

    # الگو: از "binance-dark": { تا انتهای }, با احتساب nested braces
    pattern = re.compile(
        r'  "binance-dark":\s*\{.*?^  \},',
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(themes_src)
    if not match:
        return themes_src, False

    old_block = match.group(0)
    if old_block.strip() == NEW_BINANCE_BLOCK.strip():
        # قبلاً اصلاح شده — هیچ تغییری لازم نیست (idempotent)
        return themes_src, False

    new_src = themes_src[: match.start()] + NEW_BINANCE_BLOCK + themes_src[match.end() :]
    return new_src, True


def main() -> int:
    print("=" * 64)
    print("اسکریپت ۲۷c — اصلاح تم binance-dark با رنگ‌های واقعی بایننس")
    print("=" * 64)
    print()

    if not THEMES_JS.exists():
        print(f"[ERROR] فایل پیدا نشد: {THEMES_JS}")
        print("        ابتدا اسکریپت ۲۷ را اجرا کنید.")
        return 1

    if not INDEX_CSS.exists():
        print(f"[ERROR] فایل پیدا نشد: {INDEX_CSS}")
        return 1

    # ---- themes.js ----
    print("📝 themes.js:")
    src = THEMES_JS.read_text(encoding="utf-8")
    new_src, changed = replace_binance_block(src)
    if not changed:
        # تشخیص: آیا بلوک قبلاً صحیح است یا regex match نشد؟
        if '"--color-link": "#F0B90B"' in src:
            print("  - تم binance-dark قبلاً اصلاح شده (idempotent — بدون تغییر)")
        else:
            print("  [ERROR] بلوک «binance-dark» در themes.js پیدا نشد!")
            return 1
    else:
        THEMES_JS.write_text(new_src, encoding="utf-8", newline="\n")
        print(f"  ✓ بلوک binance-dark بازنویسی شد")
        # نمایش تغییرات کلیدی
        print("    --color-link:        #2962ff → #F0B90B  (طلایی)")
        print("    --color-bg:          #1e222d → #181A20  (تیره‌تر)")
        print("    --color-text:        #d1d4dc → #EAECEF  (تیزتر)")
        print("    --color-success:     #26a69a → #0ECB81  (سبز بایننس)")
        print("    --color-danger:      #ef5350 → #F6465D  (قرمز بایننس)")

    # ---- index.css ----
    print()
    print("📝 index.css:")
    current_css = INDEX_CSS.read_text(encoding="utf-8")
    if current_css == NEW_INDEX_CSS:
        print("  - قبلاً اصلاح شده (idempotent — بدون تغییر)")
    else:
        INDEX_CSS.write_text(NEW_INDEX_CSS, encoding="utf-8", newline="\n")
        print(f"  ✓ :root fallback به رنگ‌های بایننس به‌روز شد")

    print()
    print("=" * 64)
    print("✅ تم binance-dark اکنون دقیقاً مطابق بایننس است.")
    print("=" * 64)
    print()
    print("Vite hot reload خودکار اعمال می‌کند.")
    print()
    print("چک نهایی:")
    print("  ۱) مرورگر را refresh کن (F5)")
    print("  ۲) لینک «BTC/USDT — روزانه» باید طلایی باشد (نه آبی)")
    print("  ۳) پس‌زمینه باید مشکی‌تر (#181A20)")
    print("  ۴) رفتن به /chart/1 → کندل‌های سبز رنگ #0ECB81 (سبز بایننس)")
    print()
    print("سپس: python scripts\\27d_test_binance_colors.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
