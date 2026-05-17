# -*- coding: utf-8 -*-
"""
اسکریپت ۲۷e — Binance UI Polish (interactive states)
================================================================
این اسکریپت idempotent است.

مشکل: در اسکریپت ۲۷c رنگ‌های تم درست شدند، ولی state های تعاملی نبودند:
  - hover state روی دکمه‌ها → روشن شدن
  - focus state روی input/button → حلقه طلایی
  - active state → فرورفتن لحظه‌ای
  - select با hover/focus → border بایننس
  - کارت‌های لینک‌دار با hover → پس‌زمینه تغییر

این جزئیات همان چیزی است که "حس واقعی بایننس" را می‌سازد.

تغییرات:
  1. frontend/src/index.css  → اضافه شدن interactive states سراسری
  2. frontend/src/pages/HomePage.jsx → افزودن data-card-link به Link
================================================================
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FRONTEND_SRC = PROJECT_ROOT / "frontend" / "src"
INDEX_CSS = FRONTEND_SRC / "index.css"
HOME_PAGE = FRONTEND_SRC / "pages" / "HomePage.jsx"


# ============================================================
# index.css جدید — همان ۲۷c + interactive states
# ============================================================
NEW_INDEX_CSS = """/* ============================================================
   Reset + پایه — زیرگام ۸ (Theme Engine)
   متغیرهای CSS توسط ThemeProvider روی :root تزریق می‌شوند.
   مقادیر :root زیر صرفاً fallback اولیه‌اند (پیش از mount).
   ۲۷c — رنگ‌های fallback به استانداردهای رسمی بایننس اصلاح شد.
   🆕 ۲۷e — interactive states (hover/focus/active) به سبک بایننس.
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

/* ============================================================
   🆕 Interactive states — حس بایننس
   ============================================================ */

button {
  cursor: pointer;
  font-family: inherit;
  font-size: inherit;
  border: none;
  outline: none;
  background: transparent;
  color: inherit;
  transition: filter 0.15s ease, transform 0.05s ease, background 0.15s ease, border-color 0.15s ease;
}

button:hover:not(:disabled) {
  filter: brightness(1.12);
}

button:active:not(:disabled) {
  transform: translateY(1px);
  filter: brightness(0.95);
}

button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
  filter: none;
}

a {
  color: var(--color-link);
  text-decoration: none;
  transition: opacity 0.15s ease;
}

a:hover {
  text-decoration: underline;
  opacity: 0.85;
}

input, select, textarea {
  font-family: inherit;
  font-size: inherit;
  outline: none;
  background: transparent;
  color: inherit;
  transition: border-color 0.15s ease, background 0.15s ease;
}

select {
  cursor: pointer;
}

select:hover {
  border-color: var(--color-border-strong) !important;
  background: var(--color-card-hover) !important;
}

select:focus {
  border-color: var(--color-primary) !important;
  outline: none;
}

input:focus, textarea:focus {
  border-color: var(--color-primary) !important;
  outline: none;
}

/* کارت‌های لینک‌دار — full clickable card با hover بایننس */
[data-card-link="true"] {
  display: block;
  transition: background 0.15s ease, border-color 0.15s ease, transform 0.15s ease;
  cursor: pointer;
}

[data-card-link="true"]:hover {
  background: var(--color-card-hover) !important;
  border-color: var(--color-border-strong) !important;
  text-decoration: none !important;
  opacity: 1;
}

/* ============================================================
   اسکرول‌بار سفارشی
   ============================================================ */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--color-bg); }
::-webkit-scrollbar-thumb {
  background: var(--color-border-strong);
  border-radius: 5px;
  transition: background 0.15s ease;
}
::-webkit-scrollbar-thumb:hover { background: var(--color-text-muted); }
"""


# ============================================================
# HomePage جدید — افزودن data-card-link به Link
# ============================================================
NEW_HOME_PAGE = """import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api.js";
import useAuthStore from "../stores/authStore.js";
import useThemeStore from "../stores/themeStore.js";
import { listThemes } from "../themes/themes.js";

export default function HomePage() {
  const navigate = useNavigate();
  const user = useAuthStore((s) => s.user);
  const setUser = useAuthStore((s) => s.setUser);
  const logout = useAuthStore((s) => s.logout);

  const themeId = useThemeStore((s) => s.themeId);
  const setTheme = useThemeStore((s) => s.setTheme);

  useEffect(() => {
    if (!user) {
      api
        .get("/auth/me")
        .then((resp) => setUser(resp.data.data))
        .catch(() => {});
    }
  }, [user, setUser]);

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <div style={{ padding: 24, maxWidth: 900, margin: "0 auto" }}>
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 32,
          paddingBottom: 16,
          borderBottom: "1px solid var(--color-border)",
        }}
      >
        <div>
          <h1 style={{ fontSize: 22, marginBottom: 4, fontWeight: 600 }}>
            سامانه هوشمند ترید
          </h1>
          {user ? (
            <div style={{ fontSize: 13, color: "var(--color-text-muted)" }}>
              کاربر:{" "}
              <strong style={{ color: "var(--color-text)" }}>
                {user.username}
              </strong>
              {" — "}نقش: {user.role}
            </div>
          ) : (
            <div style={{ fontSize: 13, color: "var(--color-text-muted)" }}>
              در حال بارگذاری...
            </div>
          )}
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          {/* Theme Switcher موقت — در زیرگام ۸.۴ جایگزین می‌شود */}
          <select
            value={themeId}
            onChange={(e) => setTheme(e.target.value)}
            title="تغییر تم"
            style={{
              background: "var(--color-card)",
              color: "var(--color-text)",
              padding: "8px 12px",
              borderRadius: 4,
              border: "1px solid var(--color-border)",
              fontSize: 13,
              cursor: "pointer",
            }}
          >
            {listThemes().map((t) => (
              <option key={t.id} value={t.id}>
                {t.name}
              </option>
            ))}
          </select>

          <button
            onClick={handleLogout}
            style={{
              background: "var(--color-card)",
              color: "var(--color-text)",
              padding: "8px 16px",
              borderRadius: 4,
              border: "1px solid var(--color-border)",
              fontSize: 13,
              fontWeight: 500,
            }}
          >
            خروج
          </button>
        </div>
      </header>

      <section>
        <h2
          style={{
            fontSize: 14,
            marginBottom: 12,
            color: "var(--color-text-muted)",
            fontWeight: 500,
            textTransform: "uppercase",
            letterSpacing: "0.5px",
          }}
        >
          نمودارها
        </h2>
        <ul style={{ listStyle: "none" }}>
          <li>
            <Link
              to="/chart/1"
              data-card-link="true"
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "14px 16px",
                background: "var(--color-card)",
                borderRadius: 4,
                border: "1px solid var(--color-border)",
                fontSize: 15,
                color: "var(--color-link)",
                fontWeight: 500,
              }}
            >
              <span>📊 BTC/USDT — روزانه</span>
              <span
                style={{
                  color: "var(--color-text-muted)",
                  fontSize: 12,
                  fontWeight: 400,
                }}
              >
                1714 کندل
              </span>
            </Link>
          </li>
        </ul>
      </section>
    </div>
  );
}
"""


def write_if_changed(path: Path, content: str, label: str) -> str:
    """نوشتن idempotent. خروجی: 'changed' یا 'unchanged'"""
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return "unchanged"
    path.write_text(content, encoding="utf-8", newline="\n")
    return "changed"


def main() -> int:
    print("=" * 64)
    print("اسکریپت ۲۷e — Binance UI Polish (interactive states)")
    print("=" * 64)
    print()

    if not INDEX_CSS.exists() or not HOME_PAGE.exists():
        print("[ERROR] فایل‌های پیش‌نیاز پیدا نشد. ابتدا ۲۷ + ۲۷c اجرا شود.")
        return 1

    # index.css
    print("📝 index.css:")
    status = write_if_changed(INDEX_CSS, NEW_INDEX_CSS, "index.css")
    if status == "unchanged":
        print("  - قبلاً اصلاح شده (idempotent)")
    else:
        print("  ✓ interactive states اضافه شد")
        print("    • button:hover  → filter brightness(1.12)")
        print("    • button:active → translateY(1px)")
        print("    • button:focus  → outline طلایی")
        print("    • select:hover  → border-color استرانگ")
        print("    • input:focus   → border طلایی")
        print("    • [data-card-link]:hover → پس‌زمینه روشن‌تر")

    # HomePage
    print()
    print("📝 HomePage.jsx:")
    status = write_if_changed(HOME_PAGE, NEW_HOME_PAGE, "HomePage")
    if status == "unchanged":
        print("  - قبلاً اصلاح شده (idempotent)")
    else:
        print("  ✓ data-card-link به Link اضافه شد")
        print("  ✓ تایپوگرافی بایننس‌مانند برای header «نمودارها»")
        print("  ✓ h1 با fontWeight 600")

    print()
    print("=" * 64)
    print("✅ Polish بایننس اعمال شد.")
    print("=" * 64)
    print()
    print("چک بصری بعد از refresh مرورگر:")
    print("  ۱) موس روی دکمه «خروج» → باید روشن‌تر شود")
    print("  ۲) Tab فشار بده → روی دکمه‌ها حلقه طلایی")
    print("  ۳) موس روی کارت «BTC/USDT» → پس‌زمینه روشن می‌شود")
    print("  ۴) کلیک روی dropdown تم → border طلایی هنگام focus")
    print()
    print("سپس: python scripts\\27f_test_polish.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
