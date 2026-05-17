# -*- coding: utf-8 -*-
"""
اسکریپت ۲۸c — اصلاح کادر Toast برای هماهنگی با تم (Bug #45)
================================================================
این اسکریپت idempotent است.

مشکل: در اسکریپت ۲۸، کادر toast با border رنگ نوع پیام بود (سبز/قرمز/زرد/آبی پررنگ).
این هویت تم را نقض می‌کرد — همه کادرها باید از تم بایننس پیروی کنند.

اصلاح:
  - background: var(--color-card)           ← هماهنگ با تم
  - border:     1px solid var(--color-border)  ← هماهنگ با تم
  - borderInlineStart: 3px solid <نوع>      ← فقط نوار باریک accent در start (RTL = راست)
  - icon: همچنان رنگی (indicator نوع)

فقط یک فایل تغییر می‌کند:
  frontend/src/components/common/Toast.jsx
================================================================
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
TOAST_JSX = PROJECT_ROOT / "frontend" / "src" / "components" / "common" / "Toast.jsx"


NEW_TOAST_JSX = """import useToastStore from "../../stores/toastStore.js";

const TYPE_CONFIG = {
  success: { icon: "✓", color: "var(--color-success)" },
  error:   { icon: "✕", color: "var(--color-danger)" },
  warning: { icon: "⚠", color: "var(--color-warning)" },
  info:    { icon: "ℹ", color: "var(--color-info)" },
};

export default function Toast({ id, type, message }) {
  const dismiss = useToastStore((s) => s.dismiss);
  const cfg = TYPE_CONFIG[type] || TYPE_CONFIG.info;

  return (
    <div
      role="alert"
      style={{
        display: "flex",
        alignItems: "flex-start",
        gap: 10,
        minWidth: 280,
        maxWidth: 420,
        padding: "12px 16px",
        background: "var(--color-card)",
        border: "1px solid var(--color-border)",
        borderInlineStart: `3px solid ${cfg.color}`,
        borderRadius: 4,
        boxShadow: "var(--shadow-card)",
        animation: "toast-slide-in 0.2s ease-out",
      }}
    >
      <span
        aria-hidden="true"
        style={{
          color: cfg.color,
          fontSize: 16,
          lineHeight: 1.2,
          marginTop: 1,
          fontWeight: 700,
        }}
      >
        {cfg.icon}
      </span>
      <span
        style={{
          flex: 1,
          color: "var(--color-text)",
          fontSize: 13,
          lineHeight: 1.5,
        }}
      >
        {message}
      </span>
      <button
        onClick={() => dismiss(id)}
        aria-label="بستن"
        style={{
          color: "var(--color-text-muted)",
          fontSize: 18,
          lineHeight: 1,
          padding: 0,
          marginRight: -4,
          marginTop: -2,
        }}
      >
        ×
      </button>
    </div>
  );
}
"""


def main() -> int:
    print("=" * 64)
    print("اسکریپت ۲۸c — اصلاح کادر Toast (Bug #45 — هماهنگی با تم)")
    print("=" * 64)
    print()

    if not TOAST_JSX.exists():
        print("[ERROR] Toast.jsx پیدا نشد. ابتدا اسکریپت ۲۸ را اجرا کنید.")
        return 1

    current = TOAST_JSX.read_text(encoding="utf-8")
    if current == NEW_TOAST_JSX:
        print(f"  - {TOAST_JSX.relative_to(PROJECT_ROOT)}  (idempotent — بدون تغییر)")
    else:
        TOAST_JSX.write_text(NEW_TOAST_JSX, encoding="utf-8", newline="\n")
        print(f"  ✓ {TOAST_JSX.relative_to(PROJECT_ROOT)}")
        print()
        print("    تغییرات:")
        print("      border:    `1px solid ${cfg.color}` → `1px solid var(--color-border)`")
        print("      جدید:      borderInlineStart: `3px solid ${cfg.color}` (accent باریک در start)")

    # ============================================================
    # تست خودکار سریع (در همین اسکریپت — efficient)
    # ============================================================
    print()
    print("=" * 64)
    print("📋 تست خودکار:")
    print("=" * 64)

    src = TOAST_JSX.read_text(encoding="utf-8")
    checks = [
        (
            "background از تم: var(--color-card)",
            'background: "var(--color-card)"' in src,
        ),
        (
            "border از تم: var(--color-border)",
            'border: "1px solid var(--color-border)"' in src,
        ),
        (
            "borderInlineStart accent با cfg.color",
            "borderInlineStart" in src and "${cfg.color}" in src,
        ),
        (
            "بدون border کامل رنگ نوع (Bug #45 رفع)",
            "border: `1px solid ${cfg.color}`" not in src,
        ),
        (
            "آیکون رنگی همچنان indicator نوع است",
            "color: cfg.color" in src,
        ),
        (
            "متن از تم: var(--color-text)",
            'color: "var(--color-text)"' in src,
        ),
        (
            "دکمه close از تم: var(--color-text-muted)",
            'color: "var(--color-text-muted)"' in src,
        ),
        (
            "animation همچنان موجود",
            "toast-slide-in" in src,
        ),
    ]

    passed = 0
    failed = 0
    for desc, ok in checks:
        mark = "✅" if ok else "❌"
        print(f"  {mark} {desc}")
        if ok:
            passed += 1
        else:
            failed += 1

    print()
    print("=" * 64)
    if failed == 0:
        print(f"✅ همه {passed} چک سبز — Toast حالا کاملاً هماهنگ با تم.")
        print("=" * 64)
        print()
        print("چک بصری در مرورگر:")
        print("  ۱) refresh مرورگر")
        print("  ۲) login admin/1 → toast سبز خوش‌آمد:")
        print("     - پس‌زمینه: همان رنگ کارت بایننس (#1E2329)")
        print("     - border: همان رنگ border بایننس (#2B3139)")
        print("     - فقط آیکون ✓ و نوار باریک سمت راست سبز")
        print("  ۳) login غلط → toast قرمز با همان design (فقط آیکون/نوار قرمز)")
        return 0
    else:
        print(f"❌ {failed} چک ناموفق از {passed + failed}")
        print("=" * 64)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
