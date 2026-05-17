# -*- coding: utf-8 -*-
"""
اسکریپت ۲۸ — زیرگام ۸.۲: Toast Notifications
================================================================
این اسکریپت idempotent است.

فایل‌های جدید (۳):
  frontend/src/stores/toastStore.js                   (new)
  frontend/src/components/common/Toast.jsx            (new)
  frontend/src/components/common/ToastContainer.jsx   (new)

فایل‌های به‌روز (۳):
  frontend/src/App.jsx              (افزودن <ToastContainer />)
  frontend/src/pages/LoginPage.jsx  (toast به جای div خطا)
  frontend/src/index.css            (افزودن @keyframes toast-slide-in)

ویژگی‌ها:
  - ۴ نوع: success / error / warning / info
  - فارسی + RTL + رنگ‌های بایننس
  - Auto-dismiss ۴ ثانیه
  - دکمه × برای dismiss دستی
  - Stack از پایین-چپ
  - انیمیشن slide-in ۲۰۰ms
================================================================
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FRONTEND_SRC = PROJECT_ROOT / "frontend" / "src"

TOAST_STORE = FRONTEND_SRC / "stores" / "toastStore.js"
TOAST_JSX = FRONTEND_SRC / "components" / "common" / "Toast.jsx"
TOAST_CONTAINER = FRONTEND_SRC / "components" / "common" / "ToastContainer.jsx"
APP_JSX = FRONTEND_SRC / "App.jsx"
LOGIN_PAGE = FRONTEND_SRC / "pages" / "LoginPage.jsx"
INDEX_CSS = FRONTEND_SRC / "index.css"


# ============================================================
# 1) toastStore.js
# ============================================================
TOAST_STORE_CONTENT = """/* ============================================================
   Zustand store برای Toast notifications
   API: useToastStore().success(msg, [duration])
        useToastStore().error(msg, [duration])
        useToastStore().warning(msg)
        useToastStore().info(msg)
        useToastStore().dismiss(id)
        useToastStore().clear()
   duration=0 → بدون auto-dismiss (پاک کردن دستی)
   ============================================================ */
import { create } from "zustand";

let nextId = 1;
const DEFAULT_DURATION = 4000;

const useToastStore = create((set, get) => ({
  toasts: [],

  add: (type, message, duration = DEFAULT_DURATION) => {
    const id = nextId++;
    set((s) => ({ toasts: [...s.toasts, { id, type, message, duration }] }));
    if (duration > 0) {
      setTimeout(() => get().dismiss(id), duration);
    }
    return id;
  },

  dismiss: (id) =>
    set((s) => ({ toasts: s.toasts.filter((t) => t.id !== id) })),

  clear: () => set({ toasts: [] }),

  success: (msg, dur) => get().add("success", msg, dur),
  error: (msg, dur) => get().add("error", msg, dur),
  warning: (msg, dur) => get().add("warning", msg, dur),
  info: (msg, dur) => get().add("info", msg, dur),
}));

export default useToastStore;
"""


# ============================================================
# 2) Toast.jsx
# ============================================================
TOAST_JSX_CONTENT = """import useToastStore from "../../stores/toastStore.js";

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
        border: `1px solid ${cfg.color}`,
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


# ============================================================
# 3) ToastContainer.jsx
# ============================================================
TOAST_CONTAINER_CONTENT = """import useToastStore from "../../stores/toastStore.js";
import Toast from "./Toast.jsx";

export default function ToastContainer() {
  const toasts = useToastStore((s) => s.toasts);

  return (
    <div
      aria-live="polite"
      style={{
        position: "fixed",
        bottom: 24,
        left: 24,
        zIndex: 9999,
        display: "flex",
        flexDirection: "column-reverse",
        gap: 8,
        pointerEvents: "none",
      }}
    >
      {toasts.map((t) => (
        <div key={t.id} style={{ pointerEvents: "auto" }}>
          <Toast {...t} />
        </div>
      ))}
    </div>
  );
}
"""


# ============================================================
# 4) App.jsx — افزودن <ToastContainer />
# ============================================================
APP_JSX_CONTENT = """import { Routes, Route, Navigate } from "react-router-dom";
import ProtectedRoute from "./components/common/ProtectedRoute.jsx";
import ToastContainer from "./components/common/ToastContainer.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import HomePage from "./pages/HomePage.jsx";
import ChartPage from "./pages/ChartPage.jsx";

export default function App() {
  return (
    <>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/chart/:symbolId" element={<ChartPage />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <ToastContainer />
    </>
  );
}
"""


# ============================================================
# 5) LoginPage.jsx — toast به جای div خطا
# ============================================================
LOGIN_PAGE_CONTENT = """import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import api from "../services/api.js";
import useAuthStore from "../stores/authStore.js";
import useToastStore from "../stores/toastStore.js";

const cardStyle = {
  width: "100%",
  maxWidth: 400,
  background: "var(--color-card)",
  padding: 32,
  borderRadius: 8,
  boxShadow: "var(--shadow-card)",
  border: "1px solid var(--color-border)",
};

const inputStyle = {
  width: "100%",
  padding: "10px 12px",
  background: "var(--color-bg)",
  border: "1px solid var(--color-border)",
  borderRadius: 4,
  color: "var(--color-text)",
  fontSize: 14,
};

const labelStyle = {
  display: "block",
  marginBottom: 6,
  fontSize: 13,
  color: "var(--color-text-muted)",
};

export default function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const accessToken = useAuthStore((s) => s.accessToken);
  const setTokens = useAuthStore((s) => s.setTokens);
  const setUser = useAuthStore((s) => s.setUser);
  const toastError = useToastStore((s) => s.error);
  const toastSuccess = useToastStore((s) => s.success);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (accessToken) {
      const target = location.state?.from?.pathname || "/";
      navigate(target, { replace: true });
    }
  }, [accessToken, navigate, location]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      const resp = await api.post("/auth/login", formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      const { access_token, refresh_token } = resp.data.data;
      setTokens(access_token, refresh_token);

      const meResp = await api.get("/auth/me");
      setUser(meResp.data.data);

      toastSuccess(`خوش آمدید، ${meResp.data.data.username}!`);

      const target = location.state?.from?.pathname || "/";
      navigate(target, { replace: true });
    } catch (err) {
      if (err.code === "ERR_NETWORK") {
        toastError("خطا در ارتباط با سرور. آیا Backend در حال اجراست؟");
      } else if (err.response?.status === 401) {
        toastError("نام کاربری یا رمز عبور اشتباه است");
      } else if (err.response?.data?.message) {
        toastError(err.response.data.message);
      } else {
        toastError("خطای ناشناخته. دوباره تلاش کنید.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: 24,
      }}
    >
      <form onSubmit={handleSubmit} style={cardStyle}>
        <h1 style={{ fontSize: 22, marginBottom: 24, textAlign: "center", fontWeight: 600 }}>
          ورود به سامانه
        </h1>

        <div style={{ marginBottom: 16 }}>
          <label htmlFor="username" style={labelStyle}>
            نام کاربری
          </label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            autoFocus
            autoComplete="username"
            style={{ ...inputStyle, direction: "ltr", textAlign: "left" }}
          />
        </div>

        <div style={{ marginBottom: 20 }}>
          <label htmlFor="password" style={labelStyle}>
            رمز عبور
          </label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            autoComplete="current-password"
            style={{ ...inputStyle, direction: "ltr", textAlign: "left" }}
          />
        </div>

        <button
          type="submit"
          disabled={loading || !username || !password}
          style={{
            width: "100%",
            padding: "12px",
            background: "var(--color-primary)",
            color: "var(--color-text-inverse)",
            borderRadius: 4,
            fontSize: 15,
            fontWeight: 600,
          }}
        >
          {loading ? "در حال ورود..." : "ورود"}
        </button>

        <div
          style={{
            marginTop: 20,
            paddingTop: 16,
            borderTop: "1px solid var(--color-border)",
            fontSize: 12,
            color: "var(--color-text-muted)",
            textAlign: "center",
          }}
        >
          فاز ۰ — پیش‌فرض: admin / 1
        </div>
      </form>
    </div>
  );
}
"""


# ============================================================
# 6) index.css — افزودن @keyframes toast-slide-in
# ============================================================
INDEX_CSS_CONTENT = """/* ============================================================
   Reset + پایه — زیرگام ۸ (Theme Engine)
   متغیرهای CSS توسط ThemeProvider روی :root تزریق می‌شوند.
   مقادیر :root زیر صرفاً fallback اولیه‌اند (پیش از mount).
   ۲۷c — رنگ‌های fallback به استانداردهای رسمی بایننس.
   ۲۷e — interactive states (hover/focus/active) به سبک بایننس.
   🆕 ۲۸ — @keyframes toast-slide-in برای Toast Notifications.
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
   Interactive states — حس بایننس (۲۷e)
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
   🆕 Toast animations (۲۸)
   ============================================================ */

@keyframes toast-slide-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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


def write_file(path: Path, content: str) -> str:
    """نوشتن idempotent. خروجی: 'changed' یا 'unchanged'"""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return "unchanged"
    path.write_text(content, encoding="utf-8", newline="\n")
    return "changed"


def main() -> int:
    print("=" * 64)
    print("اسکریپت ۲۸ — زیرگام ۸.۲: Toast Notifications")
    print("=" * 64)
    print()

    if not FRONTEND_SRC.exists():
        print("[ERROR] frontend/src پیدا نشد.")
        return 1

    files = [
        ("toastStore.js (جدید)", TOAST_STORE, TOAST_STORE_CONTENT),
        ("Toast.jsx (جدید)", TOAST_JSX, TOAST_JSX_CONTENT),
        ("ToastContainer.jsx (جدید)", TOAST_CONTAINER, TOAST_CONTAINER_CONTENT),
        ("App.jsx", APP_JSX, APP_JSX_CONTENT),
        ("LoginPage.jsx", LOGIN_PAGE, LOGIN_PAGE_CONTENT),
        ("index.css", INDEX_CSS, INDEX_CSS_CONTENT),
    ]

    for label, path, content in files:
        status = write_file(path, content)
        rel = path.relative_to(PROJECT_ROOT)
        if status == "unchanged":
            print(f"  - {rel}  (idempotent — بدون تغییر)")
        else:
            print(f"  ✓ {rel}")

    print()
    print("=" * 64)
    print("✅ Toast Notifications آماده است.")
    print("=" * 64)
    print()
    print("Vite hot reload خودکار اعمال می‌کند.")
    print()
    print("تست دستی سریع (بصری):")
    print("  ۱) برو /login → admin/1 → toast سبز «خوش آمدید، admin!» ظاهر شود")
    print("  ۲) logout سپس admin/wrongpass → toast قرمز «نام کاربری یا رمز...»")
    print("  ۳) چند بار سریع login غلط بزن → چندتا toast روی هم stack شوند")
    print("  ۴) دکمه × روی toast → فوراً پاک شود")
    print("  ۵) منتظر ۴ ثانیه بمان → toast خودش پاک شود")
    print()
    print("سپس: python scripts\\28b_test_toast.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
