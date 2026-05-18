# -*- coding: utf-8 -*-
"""
اسکریپت ۳۰ — زیرگام ۸.۴: Settings Page
================================================================
این اسکریپت idempotent است — قابل اجرا چندبار بدون شکست.

محتوای زیرگام ۸.۴:
  ۱) SettingsPage — صفحه /settings با ۳ بخش:
       - انتخاب تم (۵ کارت با preview)
       - اندازه فونت (۴ preset + preview زنده)
       - بازگشت به پیش‌فرض (ConfirmDialog + Toast)
  ۲) ThemeCard — کارت preview تم با نوارهای رنگ + badge فعال
  ۳) FontSizeControl — ۴ preset button + ناحیه preview
  ۴) App.jsx — route /settings (protected)
  ۵) HomePage.jsx — حذف dropdown موقت تم، افزودن لینک ⚙️

اصول طراحی (طبق سند v2.6):
  - بدون hex hardcoded — همه از CSS variables
  - استثنا قاعده‌مند: در ThemeCard preview، رنگ‌ها از خود
    theme.vars خوانده می‌شوند (نه از :root) — چون می‌خواهیم رنگ‌های
    تم‌های دیگر را نشان دهیم نه تم فعلی.
  - استفاده از کامپوننت‌های زیرگام ۸.۳ (ConfirmDialog) و ۸.۲ (Toast)
  - themeStore موجود استفاده می‌شود (هیچ store جدیدی نیاز نیست)
  - Interactive states (۸.۷.۱) از index.css ارث می‌برد

فایل‌های جدید:
  frontend/src/pages/SettingsPage.jsx
  frontend/src/components/settings/ThemeCard.jsx
  frontend/src/components/settings/FontSizeControl.jsx

فایل‌های به‌روزرسانی:
  frontend/src/App.jsx                (افزودن route /settings)
  frontend/src/pages/HomePage.jsx     (حذف dropdown + Link گیر)
================================================================
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FRONTEND = PROJECT_ROOT / "frontend" / "src"

PAGES_DIR = FRONTEND / "pages"
SETTINGS_COMP_DIR = FRONTEND / "components" / "settings"

SETTINGS_PAGE = PAGES_DIR / "SettingsPage.jsx"
THEME_CARD = SETTINGS_COMP_DIR / "ThemeCard.jsx"
FONT_SIZE_CTRL = SETTINGS_COMP_DIR / "FontSizeControl.jsx"

APP_JSX = FRONTEND / "App.jsx"
HOME_JSX = PAGES_DIR / "HomePage.jsx"


# ============================================================
# ThemeCard.jsx
# ============================================================

THEME_CARD_JSX = """/**
 * ThemeCard — کارت انتخاب تم با پیش‌نمایش رنگ‌ها
 *
 * Props:
 *   theme:    object { id, name, isDark, vars }
 *   isActive: boolean
 *   onClick:  () => void
 *
 * نکته معماری:
 *   رنگ‌های preview از خود theme.vars خوانده می‌شوند، نه از :root.
 *   دلیل: می‌خواهیم رنگ‌های تم‌های دیگر را نشان دهیم نه تم فعال.
 *   این تنها استثنای قانون "بدون hex hardcoded" است و قاعده‌مند است
 *   (مقادیر از theme object می‌آیند، نه hardcoded).
 *
 * بقیه عناصر کارت (متن، border، badge):
 *   - بدنه کارت از تم فعلی: var(--color-card)
 *   - متن از تم فعلی: var(--color-text)
 *   - border فعال: var(--color-primary)
 */
export default function ThemeCard({ theme, isActive, onClick }) {
  const v = theme.vars;

  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={isActive}
      style={{
        position: "relative",
        background: "var(--color-card)",
        border: isActive
          ? "2px solid var(--color-primary)"
          : "1px solid var(--color-border)",
        borderRadius: 8,
        padding: 14,
        textAlign: "start",
        cursor: "pointer",
        overflow: "hidden",
        width: "100%",
      }}
    >
      {/* پیش‌نمایش رنگ‌ها — از theme.vars خود تم */}
      <div
        style={{
          display: "flex",
          gap: 6,
          marginBottom: 12,
          height: 36,
        }}
      >
        <div
          aria-hidden="true"
          title="bg"
          style={{
            flex: 1,
            background: v["--color-bg"],
            borderRadius: 4,
            border: `1px solid ${v["--color-border"]}`,
          }}
        />
        <div
          aria-hidden="true"
          title="card"
          style={{
            flex: 1,
            background: v["--color-card"],
            borderRadius: 4,
            border: `1px solid ${v["--color-border"]}`,
          }}
        />
        <div
          aria-hidden="true"
          title="primary"
          style={{
            width: 36,
            background: v["--color-primary"],
            borderRadius: 4,
          }}
        />
        <div
          aria-hidden="true"
          title="success"
          style={{
            width: 36,
            background: v["--color-success"],
            borderRadius: 4,
          }}
        />
        <div
          aria-hidden="true"
          title="danger"
          style={{
            width: 36,
            background: v["--color-danger"],
            borderRadius: 4,
          }}
        />
      </div>

      {/* نام تم + badge فعال */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: 8,
        }}
      >
        <span
          style={{
            fontSize: 14,
            fontWeight: 600,
            color: "var(--color-text)",
          }}
        >
          {theme.name}
        </span>
        {isActive && (
          <span
            style={{
              fontSize: 11,
              padding: "3px 10px",
              background: "var(--color-primary)",
              color: "var(--color-text-inverse)",
              borderRadius: 12,
              fontWeight: 600,
              whiteSpace: "nowrap",
            }}
          >
            ✓ فعال
          </span>
        )}
      </div>
    </button>
  );
}
"""


# ============================================================
# FontSizeControl.jsx
# ============================================================

FONT_SIZE_CONTROL_JSX = """/**
 * FontSizeControl — کنترل اندازه فونت با ۴ preset + preview زنده
 *
 * Props:
 *   value:    number (پیکسل فعلی)
 *   onChange: (px) => void
 *
 * Presets: 12 / 14 / 16 / 18 px
 * preview: متن نمونه که با تغییر value تغییر اندازه می‌دهد
 */
const PRESETS = [
  { label: "کوچک",     value: 12 },
  { label: "متوسط",    value: 14 },
  { label: "بزرگ",     value: 16 },
  { label: "خیلی بزرگ", value: 18 },
];

export default function FontSizeControl({ value, onChange }) {
  return (
    <div>
      {/* دکمه‌های preset */}
      <div
        role="radiogroup"
        aria-label="اندازه فونت"
        style={{ display: "flex", gap: 8, flexWrap: "wrap" }}
      >
        {PRESETS.map((p) => {
          const isActive = value === p.value;
          return (
            <button
              key={p.value}
              type="button"
              role="radio"
              aria-checked={isActive}
              onClick={() => onChange(p.value)}
              style={{
                flex: "1 1 110px",
                padding: "10px 12px",
                background: isActive
                  ? "var(--color-primary)"
                  : "var(--color-card)",
                color: isActive
                  ? "var(--color-text-inverse)"
                  : "var(--color-text)",
                border: `1px solid ${
                  isActive ? "var(--color-primary)" : "var(--color-border)"
                }`,
                borderRadius: 4,
                fontSize: 13,
                fontWeight: isActive ? 600 : 500,
              }}
            >
              {p.label} ({p.value}px)
            </button>
          );
        })}
      </div>

      {/* preview زنده */}
      <div
        style={{
          marginTop: 14,
          padding: "14px 16px",
          background: "var(--color-bg-elevated)",
          border: "1px solid var(--color-border)",
          borderRadius: 4,
          color: "var(--color-text)",
          fontSize: `${value}px`,
          lineHeight: 1.6,
        }}
      >
        نمونه متن: قیمت BTC/USDT برابر است با ۱۰۲٬۳۴۵ دلار آمریکا.
      </div>
    </div>
  );
}
"""


# ============================================================
# SettingsPage.jsx
# ============================================================

SETTINGS_PAGE_JSX = """import { Link } from "react-router-dom";
import useThemeStore from "../stores/themeStore.js";
import useConfirmStore from "../stores/confirmStore.js";
import useToastStore from "../stores/toastStore.js";
import { listThemes } from "../themes/themes.js";
import ThemeCard from "../components/settings/ThemeCard.jsx";
import FontSizeControl from "../components/settings/FontSizeControl.jsx";

/**
 * SettingsPage — صفحه /settings
 *
 * بخش‌ها:
 *   ۱) انتخاب تم (۵ کارت preview)
 *   ۲) اندازه فونت (۴ preset + preview زنده)
 *   ۳) بازگشت به تنظیمات پیش‌فرض (ConfirmDialog + Toast)
 *
 * از themeStore موجود استفاده می‌کند (هیچ store جدیدی نیاز نیست).
 */
export default function SettingsPage() {
  const themeId = useThemeStore((s) => s.themeId);
  const setTheme = useThemeStore((s) => s.setTheme);
  const fontSize = useThemeStore((s) => s.fontSize);
  const setFontSize = useThemeStore((s) => s.setFontSize);
  const resetAll = useThemeStore((s) => s.resetAll);

  const askConfirm = useConfirmStore((s) => s.confirm);
  const toastSuccess = useToastStore((s) => s.success);

  const themes = listThemes();

  const handleReset = async () => {
    const ok = await askConfirm({
      title: "بازگشت به تنظیمات پیش‌فرض",
      message:
        "همه تنظیمات (تم، اندازه فونت، رنگ‌های سفارشی) به حالت پیش‌فرض بازمی‌گردند. آیا مطمئن هستید؟",
      variant: "warning",
      confirmText: "بازگشت به پیش‌فرض",
      cancelText: "انصراف",
    });
    if (!ok) return;
    resetAll();
    toastSuccess("تنظیمات به حالت پیش‌فرض بازگشت.");
  };

  return (
    <div style={{ padding: 24, maxWidth: 900, margin: "0 auto" }}>
      <div style={{ marginBottom: 16 }}>
        <Link to="/">← بازگشت به صفحه اصلی</Link>
      </div>

      <header
        style={{
          marginBottom: 32,
          paddingBottom: 16,
          borderBottom: "1px solid var(--color-border)",
        }}
      >
        <h1
          style={{
            fontSize: 22,
            fontWeight: 600,
            color: "var(--color-text)",
          }}
        >
          ⚙️ تنظیمات
        </h1>
        <p
          style={{
            marginTop: 4,
            fontSize: 13,
            color: "var(--color-text-muted)",
          }}
        >
          تم، اندازه فونت و سایر تنظیمات ظاهری برنامه
        </p>
      </header>

      {/* بخش ۱ — انتخاب تم */}
      <section style={{ marginBottom: 36 }}>
        <SectionHeader
          title="ظاهر و تم"
          description="یک تم را برای ظاهر کلی برنامه انتخاب کنید"
        />
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
            gap: 12,
          }}
        >
          {themes.map((t) => (
            <ThemeCard
              key={t.id}
              theme={t}
              isActive={t.id === themeId}
              onClick={() => setTheme(t.id)}
            />
          ))}
        </div>
      </section>

      {/* بخش ۲ — اندازه فونت */}
      <section style={{ marginBottom: 36 }}>
        <SectionHeader
          title="اندازه فونت"
          description="اندازه متن سراسری برنامه — preview در پایین"
        />
        <FontSizeControl value={fontSize} onChange={setFontSize} />
      </section>

      {/* بخش ۳ — ریست */}
      <section
        style={{
          paddingTop: 20,
          borderTop: "1px solid var(--color-border)",
        }}
      >
        <SectionHeader
          title="بازنشانی"
          description="تمام تنظیمات را به حالت پیش‌فرض برگردانید"
        />
        <button
          type="button"
          onClick={handleReset}
          style={{
            padding: "10px 18px",
            background: "var(--color-card)",
            color: "var(--color-warning)",
            border: "1px solid var(--color-warning)",
            borderRadius: 4,
            fontSize: 13,
            fontWeight: 600,
          }}
        >
          🔄 بازگشت به تنظیمات پیش‌فرض
        </button>
      </section>
    </div>
  );
}

function SectionHeader({ title, description }) {
  return (
    <div style={{ marginBottom: 14 }}>
      <h2
        style={{
          fontSize: 15,
          fontWeight: 600,
          color: "var(--color-text)",
          marginBottom: 4,
        }}
      >
        {title}
      </h2>
      <p
        style={{
          fontSize: 12,
          color: "var(--color-text-muted)",
        }}
      >
        {description}
      </p>
    </div>
  );
}
"""


# ============================================================
# App.jsx — افزودن route /settings (protected)
# ============================================================

APP_JSX_NEW = """import { Routes, Route, Navigate } from "react-router-dom";
import ProtectedRoute from "./components/common/ProtectedRoute.jsx";
import ToastContainer from "./components/common/ToastContainer.jsx";
import ConfirmDialog from "./components/common/ConfirmDialog.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import HomePage from "./pages/HomePage.jsx";
import ChartPage from "./pages/ChartPage.jsx";
import SettingsPage from "./pages/SettingsPage.jsx";

export default function App() {
  return (
    <>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/chart/:symbolId" element={<ChartPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <ToastContainer />
      <ConfirmDialog />
    </>
  );
}
"""


# ============================================================
# HomePage.jsx — حذف dropdown موقت + لینک ⚙️ به /settings
# ============================================================

HOME_JSX_NEW = """import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api.js";
import useAuthStore from "../stores/authStore.js";
import useConfirmStore from "../stores/confirmStore.js";

export default function HomePage() {
  const navigate = useNavigate();
  const user = useAuthStore((s) => s.user);
  const setUser = useAuthStore((s) => s.setUser);
  const logout = useAuthStore((s) => s.logout);

  const askConfirm = useConfirmStore((s) => s.confirm);

  useEffect(() => {
    if (!user) {
      api
        .get("/auth/me")
        .then((resp) => setUser(resp.data.data))
        .catch(() => {});
    }
  }, [user, setUser]);

  const handleLogout = async () => {
    const ok = await askConfirm({
      title: "خروج از حساب",
      message: "آیا مطمئن هستید که می‌خواهید خارج شوید؟",
      variant: "warning",
      confirmText: "خروج",
      cancelText: "انصراف",
    });
    if (!ok) return;
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

        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          {/* لینک تنظیمات — جایگزین dropdown موقت تم در زیرگام ۸.۴ */}
          <Link
            to="/settings"
            title="تنظیمات"
            aria-label="تنظیمات"
            style={{
              display: "inline-flex",
              alignItems: "center",
              justifyContent: "center",
              width: 38,
              height: 38,
              background: "var(--color-card)",
              color: "var(--color-text)",
              borderRadius: 4,
              border: "1px solid var(--color-border)",
              fontSize: 18,
              textDecoration: "none",
            }}
          >
            ⚙️
          </Link>

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


# ============================================================
# تابع نوشتن idempotent
# ============================================================


def write_if_changed(path: Path, content: str, label: str) -> str:
    rel = path.relative_to(PROJECT_ROOT)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"  ✓ ایجاد:    {rel}  ({label})")
        return "created"

    current = path.read_text(encoding="utf-8")
    if current == content:
        print(f"  - بدون تغییر: {rel}  (idempotent)")
        return "unchanged"

    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"  ✓ به‌روز:   {rel}  ({label})")
    return "updated"


# ============================================================
# اجرای اصلی
# ============================================================


def main() -> int:
    print("=" * 64)
    print("اسکریپت ۳۰ — زیرگام ۸.۴: Settings Page")
    print("=" * 64)
    print()

    if not FRONTEND.exists():
        print("[ERROR] دایرکتوری frontend/src یافت نشد.")
        return 1

    required = [APP_JSX, HOME_JSX]
    missing = [p for p in required if not p.exists()]
    if missing:
        print("[ERROR] فایل‌های واجب یافت نشدند:")
        for p in missing:
            print(f"        - {p.relative_to(PROJECT_ROOT)}")
        print("        ابتدا اسکریپت ۲۹ را اجرا کنید.")
        return 1

    # پیش‌چک: themeStore باید fontSize و resetAll داشته باشد
    theme_store = FRONTEND / "stores" / "themeStore.js"
    if theme_store.exists():
        ts = theme_store.read_text(encoding="utf-8")
        if "fontSize" not in ts or "resetAll" not in ts:
            print("[ERROR] themeStore.js فاقد fontSize یا resetAll است.")
            print("        ابتدا اسکریپت ۲۷ (theme engine) را اجرا کنید.")
            return 1

    # پیش‌چک: confirmStore.js باید موجود باشد (از زیرگام ۸.۳)
    confirm_store = FRONTEND / "stores" / "confirmStore.js"
    if not confirm_store.exists():
        print("[ERROR] confirmStore.js یافت نشد.")
        print("        ابتدا اسکریپت ۲۹ (Skeleton + ConfirmDialog) را اجرا کنید.")
        return 1

    print("--- فایل‌های جدید ---")
    write_if_changed(THEME_CARD, THEME_CARD_JSX, "ThemeCard")
    write_if_changed(FONT_SIZE_CTRL, FONT_SIZE_CONTROL_JSX, "FontSizeControl")
    write_if_changed(SETTINGS_PAGE, SETTINGS_PAGE_JSX, "SettingsPage")

    print()
    print("--- فایل‌های به‌روزرسانی ---")
    write_if_changed(APP_JSX, APP_JSX_NEW, "route /settings")
    write_if_changed(HOME_JSX, HOME_JSX_NEW, "لینک ⚙️ به جای dropdown")

    print()
    print("=" * 64)
    print("✅ زیرگام ۸.۴ اعمال شد.")
    print("=" * 64)
    print()
    print("گام بعدی:")
    print("  🟩 tab «2 scripts»:  python scripts/30b_test_settings_page.py")
    print()
    print("سپس چک بصری در 🟧 tab «3 frontend»:")
    print("  ۱) refresh مرورگر → HomePage")
    print("  ۲) کلیک روی ⚙️ → رفتن به /settings")
    print("  ۳) کلیک روی هر کارت تم → اعمال آنی تم")
    print("  ۴) تغییر اندازه فونت → preview زنده + اعمال سراسری")
    print("  ۵) دکمه «بازگشت به پیش‌فرض» → ConfirmDialog → Toast سبز")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
