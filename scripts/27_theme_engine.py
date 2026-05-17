# -*- coding: utf-8 -*-
"""
اسکریپت ۲۷ — زیرگام ۸.۱: Theme Engine Foundation
================================================================
این اسکریپت idempotent است — اجرای مجدد بدون عوارض جانبی.

فایل‌های جدید (۳):
  frontend/src/themes/themes.js                          (new)
  frontend/src/stores/themeStore.js                      (new)
  frontend/src/components/common/ThemeProvider.jsx       (new)

فایل‌های به‌روز (۵):
  frontend/src/index.css                                 (override)
  frontend/src/main.jsx                                  (override)
  frontend/src/pages/LoginPage.jsx                       (override — مهاجرت به CSS vars)
  frontend/src/pages/HomePage.jsx                        (override — مهاجرت + theme switcher موقت)
  frontend/src/pages/ChartPage.jsx                       (override — مهاجرت + chart colors از CSS vars)

۵ تم: binance-dark (پیش‌فرض) / light-minimal / dark-modern / pastel / sky-blue

پس از اجرا — Vite hot reload خودکار اعمال می‌کند.
================================================================
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FRONTEND_SRC = PROJECT_ROOT / "frontend" / "src"

# مسیرها
THEMES_DIR = FRONTEND_SRC / "themes"
THEMES_JS = THEMES_DIR / "themes.js"
THEME_STORE = FRONTEND_SRC / "stores" / "themeStore.js"
THEME_PROVIDER = FRONTEND_SRC / "components" / "common" / "ThemeProvider.jsx"
INDEX_CSS = FRONTEND_SRC / "index.css"
MAIN_JSX = FRONTEND_SRC / "main.jsx"
LOGIN_PAGE = FRONTEND_SRC / "pages" / "LoginPage.jsx"
HOME_PAGE = FRONTEND_SRC / "pages" / "HomePage.jsx"
CHART_PAGE = FRONTEND_SRC / "pages" / "ChartPage.jsx"


# ============================================================
# 1) themes.js — تعریف ۵ تم
# ============================================================
THEMES_JS_CONTENT = """/* ============================================================
   تعریف تم‌ها — هر تم یک object از CSS variables است.
   ThemeProvider مقادیر را روی :root تزریق می‌کند.
   ============================================================ */

export const THEMES = {
  "binance-dark": {
    id: "binance-dark",
    name: "بایننس تاریک",
    isDark: true,
    vars: {
      "--color-primary": "#F0B90B",
      "--color-primary-hover": "#FCD535",
      "--color-bg": "#1e222d",
      "--color-bg-elevated": "#2a2e39",
      "--color-card": "#2a2e39",
      "--color-card-hover": "#363a45",
      "--color-border": "#363a45",
      "--color-border-strong": "#4a4f5c",
      "--color-text": "#d1d4dc",
      "--color-text-muted": "#787b86",
      "--color-text-inverse": "#0a0a0a",
      "--color-success": "#26a69a",
      "--color-success-bg": "#1f3a36",
      "--color-danger": "#ef5350",
      "--color-danger-bg": "#3a1f1f",
      "--color-info": "#2962ff",
      "--color-warning": "#ff9800",
      "--color-link": "#2962ff",
      "--color-grid": "#2a2e39",
      "--shadow-card": "0 4px 12px rgba(0,0,0,0.3)",
    },
  },

  "light-minimal": {
    id: "light-minimal",
    name: "روشن مینیمال",
    isDark: false,
    vars: {
      "--color-primary": "#F0B90B",
      "--color-primary-hover": "#E0A900",
      "--color-bg": "#ffffff",
      "--color-bg-elevated": "#f8f9fa",
      "--color-card": "#ffffff",
      "--color-card-hover": "#f1f3f5",
      "--color-border": "#e9ecef",
      "--color-border-strong": "#ced4da",
      "--color-text": "#212529",
      "--color-text-muted": "#6c757d",
      "--color-text-inverse": "#ffffff",
      "--color-success": "#2e7d32",
      "--color-success-bg": "#e8f5e9",
      "--color-danger": "#c62828",
      "--color-danger-bg": "#ffebee",
      "--color-info": "#1565c0",
      "--color-warning": "#ef6c00",
      "--color-link": "#1565c0",
      "--color-grid": "#eef0f2",
      "--shadow-card": "0 2px 8px rgba(0,0,0,0.06)",
    },
  },

  "dark-modern": {
    id: "dark-modern",
    name: "تاریک مدرن",
    isDark: true,
    vars: {
      "--color-primary": "#7c3aed",
      "--color-primary-hover": "#a78bfa",
      "--color-bg": "#0f0e17",
      "--color-bg-elevated": "#1a1825",
      "--color-card": "#1f1d2e",
      "--color-card-hover": "#2a2740",
      "--color-border": "#2e2c43",
      "--color-border-strong": "#3a384f",
      "--color-text": "#e0def4",
      "--color-text-muted": "#908caa",
      "--color-text-inverse": "#0f0e17",
      "--color-success": "#9ccfd8",
      "--color-success-bg": "#1a2e33",
      "--color-danger": "#eb6f92",
      "--color-danger-bg": "#3a1e2a",
      "--color-info": "#3e8fb0",
      "--color-warning": "#f6c177",
      "--color-link": "#a78bfa",
      "--color-grid": "#262338",
      "--shadow-card": "0 4px 16px rgba(0,0,0,0.4)",
    },
  },

  "pastel": {
    id: "pastel",
    name: "پاستلی",
    isDark: false,
    vars: {
      "--color-primary": "#ff8a9a",
      "--color-primary-hover": "#ff6b80",
      "--color-bg": "#fff5f5",
      "--color-bg-elevated": "#ffeaea",
      "--color-card": "#ffffff",
      "--color-card-hover": "#fff0f3",
      "--color-border": "#f5d6dc",
      "--color-border-strong": "#e8b4be",
      "--color-text": "#4a4453",
      "--color-text-muted": "#8a8294",
      "--color-text-inverse": "#ffffff",
      "--color-success": "#8fbc8f",
      "--color-success-bg": "#edf6ed",
      "--color-danger": "#cd5c5c",
      "--color-danger-bg": "#fbe8e8",
      "--color-info": "#a8c5dd",
      "--color-warning": "#ddb892",
      "--color-link": "#b56576",
      "--color-grid": "#f5e8eb",
      "--shadow-card": "0 2px 8px rgba(180,120,140,0.12)",
    },
  },

  "sky-blue": {
    id: "sky-blue",
    name: "آبی آسمانی",
    isDark: false,
    vars: {
      "--color-primary": "#0284c7",
      "--color-primary-hover": "#0369a1",
      "--color-bg": "#f0f9ff",
      "--color-bg-elevated": "#e0f2fe",
      "--color-card": "#ffffff",
      "--color-card-hover": "#f0f9ff",
      "--color-border": "#bae6fd",
      "--color-border-strong": "#7dd3fc",
      "--color-text": "#0c4a6e",
      "--color-text-muted": "#0369a1",
      "--color-text-inverse": "#ffffff",
      "--color-success": "#16a34a",
      "--color-success-bg": "#dcfce7",
      "--color-danger": "#dc2626",
      "--color-danger-bg": "#fee2e2",
      "--color-info": "#0284c7",
      "--color-warning": "#ea580c",
      "--color-link": "#0284c7",
      "--color-grid": "#e0f2fe",
      "--shadow-card": "0 2px 10px rgba(2,132,199,0.1)",
    },
  },
};

export const DEFAULT_THEME_ID = "binance-dark";

export function getTheme(themeId) {
  return THEMES[themeId] || THEMES[DEFAULT_THEME_ID];
}

export function listThemes() {
  return Object.values(THEMES);
}
"""


# ============================================================
# 2) themeStore.js — Zustand store با persist
# ============================================================
THEME_STORE_CONTENT = """/* ============================================================
   Zustand store برای تم — themeId + fontSize + customColors
   persist در localStorage با کلید "theme-storage"
   ============================================================ */
import { create } from "zustand";
import { persist } from "zustand/middleware";
import { DEFAULT_THEME_ID } from "../themes/themes.js";

export const DEFAULT_FONT_SIZE = 14;
export const MIN_FONT_SIZE = 11;
export const MAX_FONT_SIZE = 20;

const useThemeStore = create(
  persist(
    (set) => ({
      themeId: DEFAULT_THEME_ID,
      fontSize: DEFAULT_FONT_SIZE,
      customColors: {}, // override های کاربر: { "--color-primary": "#ff0000", ... }

      setTheme: (id) => set({ themeId: id }),

      setFontSize: (px) => {
        const n = Number(px) || DEFAULT_FONT_SIZE;
        const clamped = Math.max(MIN_FONT_SIZE, Math.min(MAX_FONT_SIZE, n));
        set({ fontSize: clamped });
      },

      setCustomColor: (varName, value) =>
        set((s) => ({ customColors: { ...s.customColors, [varName]: value } })),

      removeCustomColor: (varName) =>
        set((s) => {
          const next = { ...s.customColors };
          delete next[varName];
          return { customColors: next };
        }),

      resetCustomColors: () => set({ customColors: {} }),

      resetAll: () =>
        set({
          themeId: DEFAULT_THEME_ID,
          fontSize: DEFAULT_FONT_SIZE,
          customColors: {},
        }),
    }),
    {
      name: "theme-storage",
      version: 1,
    }
  )
);

export default useThemeStore;
"""


# ============================================================
# 3) ThemeProvider.jsx — اعمال CSS variables روی :root
# ============================================================
THEME_PROVIDER_CONTENT = """/* ============================================================
   ThemeProvider — متغیرهای CSS تم فعلی را روی :root اعمال می‌کند.
   هر بار themeId/fontSize/customColors تغییر کند، اعمال مجدد می‌شود.
   ============================================================ */
import { useEffect } from "react";
import useThemeStore from "../../stores/themeStore.js";
import { getTheme } from "../../themes/themes.js";

export default function ThemeProvider({ children }) {
  const themeId = useThemeStore((s) => s.themeId);
  const fontSize = useThemeStore((s) => s.fontSize);
  const customColors = useThemeStore((s) => s.customColors);

  useEffect(() => {
    const theme = getTheme(themeId);
    const root = document.documentElement;

    // اعمال متغیرهای تم
    Object.entries(theme.vars).forEach(([k, v]) => {
      root.style.setProperty(k, v);
    });

    // اعمال override های کاربر
    Object.entries(customColors).forEach(([k, v]) => {
      root.style.setProperty(k, v);
    });

    // font-size base
    root.style.setProperty("--font-size-base", `${fontSize}px`);

    // attributeهای کمکی برای styling شرطی
    root.setAttribute("data-theme", themeId);
    root.setAttribute("data-theme-mode", theme.isDark ? "dark" : "light");
    root.style.colorScheme = theme.isDark ? "dark" : "light";
  }, [themeId, fontSize, customColors]);

  return children;
}
"""


# ============================================================
# 4) index.css — مهاجرت کامل به CSS variables
# ============================================================
INDEX_CSS_CONTENT = """/* ============================================================
   Reset + پایه — زیرگام ۸ (Theme Engine)
   متغیرهای CSS توسط ThemeProvider روی :root تزریق می‌شوند.
   مقادیر :root زیر صرفاً fallback اولیه‌اند (پیش از mount).
   ============================================================ */

:root {
  /* رنگ‌ها — fallback (پیش از تزریق ThemeProvider) */
  --color-primary: #F0B90B;
  --color-primary-hover: #FCD535;
  --color-bg: #1e222d;
  --color-bg-elevated: #2a2e39;
  --color-card: #2a2e39;
  --color-card-hover: #363a45;
  --color-border: #363a45;
  --color-border-strong: #4a4f5c;
  --color-text: #d1d4dc;
  --color-text-muted: #787b86;
  --color-text-inverse: #0a0a0a;
  --color-success: #26a69a;
  --color-success-bg: #1f3a36;
  --color-danger: #ef5350;
  --color-danger-bg: #3a1f1f;
  --color-info: #2962ff;
  --color-warning: #ff9800;
  --color-link: #2962ff;
  --color-grid: #2a2e39;
  --shadow-card: 0 4px 12px rgba(0,0,0,0.3);

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


# ============================================================
# 5) main.jsx — wrap با ThemeProvider
# ============================================================
MAIN_JSX_CONTENT = """import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App.jsx";
import ThemeProvider from "./components/common/ThemeProvider.jsx";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ThemeProvider>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </ThemeProvider>
  </React.StrictMode>
);
"""


# ============================================================
# 6) LoginPage.jsx — مهاجرت به CSS vars
# ============================================================
LOGIN_PAGE_CONTENT = """import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import api from "../services/api.js";
import useAuthStore from "../stores/authStore.js";

/* استایل‌های مشترک — همگی از CSS variables */
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

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (accessToken) {
      const target = location.state?.from?.pathname || "/";
      navigate(target, { replace: true });
    }
  }, [accessToken, navigate, location]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
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

      const target = location.state?.from?.pathname || "/";
      navigate(target, { replace: true });
    } catch (err) {
      if (err.code === "ERR_NETWORK") {
        setError("خطا در ارتباط با سرور. آیا Backend در حال اجراست؟");
      } else if (err.response?.status === 401) {
        setError("نام کاربری یا رمز عبور اشتباه است");
      } else if (err.response?.data?.message) {
        setError(err.response.data.message);
      } else {
        setError("خطای ناشناخته. دوباره تلاش کنید.");
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
        <h1 style={{ fontSize: 22, marginBottom: 24, textAlign: "center" }}>
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

        {error && (
          <div
            style={{
              padding: "10px 12px",
              background: "var(--color-danger-bg)",
              color: "var(--color-danger)",
              border: "1px solid var(--color-danger)",
              borderRadius: 4,
              marginBottom: 16,
              fontSize: 13,
            }}
          >
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !username || !password}
          style={{
            width: "100%",
            padding: "12px",
            background: loading ? "var(--color-primary-hover)" : "var(--color-primary)",
            color: "var(--color-text-inverse)",
            borderRadius: 4,
            fontSize: 15,
            fontWeight: 600,
            transition: "background 0.2s",
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
# 7) HomePage.jsx — مهاجرت + theme switcher موقت
# ============================================================
HOME_PAGE_CONTENT = """import { useEffect } from "react";
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
          <h1 style={{ fontSize: 22, marginBottom: 4 }}>سامانه هوشمند ترید</h1>
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
          {/* Theme Switcher موقت — در زیرگام ۸.۴ (Settings Page) جایگزین می‌شود */}
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
            }}
          >
            خروج
          </button>
        </div>
      </header>

      <section>
        <h2
          style={{
            fontSize: 16,
            marginBottom: 12,
            color: "var(--color-text-muted)",
            fontWeight: 500,
          }}
        >
          نمودارها
        </h2>
        <ul style={{ listStyle: "none" }}>
          <li
            style={{
              padding: 14,
              background: "var(--color-card)",
              borderRadius: 4,
              border: "1px solid var(--color-border)",
            }}
          >
            <Link
              to="/chart/1"
              style={{
                fontSize: 15,
                display: "flex",
                justifyContent: "space-between",
              }}
            >
              <span>📊 BTC/USDT — روزانه</span>
              <span style={{ color: "var(--color-text-muted)", fontSize: 12 }}>
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
# 8) ChartPage.jsx — مهاجرت + رنگ‌های chart از CSS vars
# ============================================================
CHART_PAGE_CONTENT = """import { useEffect, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { createChart, CrosshairMode } from "lightweight-charts";
import api from "../services/api.js";
import useThemeStore from "../stores/themeStore.js";

const TIMEFRAMES = [
  { value: "1d", label: "روزانه (1d)" },
  { value: "1h", label: "یک‌ساعته (1h)" },
  { value: "15m", label: "۱۵ دقیقه (15m)" },
];

/* تبدیل ISO 8601 (بدون timezone) → Unix seconds UTC */
function isoToUnix(isoStr) {
  const withZ = isoStr.endsWith("Z") ? isoStr : isoStr + "Z";
  return Math.floor(new Date(withZ).getTime() / 1000);
}

/* خواندن یک متغیر CSS از :root (در زمان فراخوانی) */
function readVar(name, fallback = "") {
  if (typeof window === "undefined") return fallback;
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return v || fallback;
}

export default function ChartPage() {
  const { symbolId } = useParams();
  const chartContainerRef = useRef(null);
  const chartRef = useRef(null);

  // به‌روزرسانی نمودار با تغییر تم — themeId در dep array
  const themeId = useThemeStore((s) => s.themeId);

  const [timeframe, setTimeframe] = useState("1d");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [meta, setMeta] = useState({ count: 0, total: 0 });

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      setLoading(true);
      setError("");

      try {
        const resp = await api.get(
          `/ohlcv/${symbolId}?timeframe=${timeframe}&limit=1000`
        );
        if (cancelled) return;

        const data = resp.data.data;
        setMeta({ count: data.count, total: data.total });

        if (!data.candles || data.candles.length === 0) {
          setError(`داده‌ای برای تایم‌فریم ${timeframe} موجود نیست`);
          setLoading(false);
          return;
        }

        const candleData = data.candles.map((c) => ({
          time: isoToUnix(c.timestamp),
          open: c.open,
          high: c.high,
          low: c.low,
          close: c.close,
        }));

        // رنگ‌ها از CSS variables تم فعلی
        const upColor = readVar("--color-success", "#26a69a");
        const downColor = readVar("--color-danger", "#ef5350");
        const bgColor = readVar("--color-card", "#1e222d");
        const textColor = readVar("--color-text", "#d1d4dc");
        const gridColor = readVar("--color-grid", "#2a2e39");
        const borderColor = readVar("--color-border", "#363a45");

        const volumeData = data.candles.map((c) => ({
          time: isoToUnix(c.timestamp),
          value: c.volume,
          color: c.close >= c.open ? `${upColor}80` : `${downColor}80`,
        }));

        // پاک کردن نمودار قبلی
        if (chartRef.current) {
          chartRef.current.remove();
          chartRef.current = null;
        }

        const chart = createChart(chartContainerRef.current, {
          width: chartContainerRef.current.clientWidth,
          height: 500,
          layout: {
            background: { color: bgColor },
            textColor: textColor,
          },
          grid: {
            vertLines: { color: gridColor },
            horzLines: { color: gridColor },
          },
          crosshair: { mode: CrosshairMode.Normal },
          timeScale: {
            timeVisible: true,
            secondsVisible: false,
            borderColor: borderColor,
          },
          rightPriceScale: { borderColor: borderColor },
        });
        chartRef.current = chart;

        const candleSeries = chart.addCandlestickSeries({
          upColor: upColor,
          downColor: downColor,
          borderVisible: false,
          wickUpColor: upColor,
          wickDownColor: downColor,
        });
        candleSeries.setData(candleData);

        const volumeSeries = chart.addHistogramSeries({
          priceFormat: { type: "volume" },
          priceScaleId: "",
        });
        volumeSeries.priceScale().applyOptions({
          scaleMargins: { top: 0.8, bottom: 0 },
        });
        volumeSeries.setData(volumeData);

        chart.timeScale().fitContent();

        setLoading(false);
      } catch (err) {
        if (cancelled) return;
        if (err.code === "ERR_NETWORK") {
          setError("خطا در ارتباط با سرور");
        } else if (err.response?.status === 404) {
          setError("نماد یافت نشد");
        } else {
          setError(err.response?.data?.message || "خطای ناشناخته");
        }
        setLoading(false);
      }
    };

    load();

    const handleResize = () => {
      if (chartRef.current && chartContainerRef.current) {
        chartRef.current.applyOptions({
          width: chartContainerRef.current.clientWidth,
        });
      }
    };
    window.addEventListener("resize", handleResize);

    return () => {
      cancelled = true;
      window.removeEventListener("resize", handleResize);
      if (chartRef.current) {
        chartRef.current.remove();
        chartRef.current = null;
      }
    };
  }, [symbolId, timeframe, themeId]); // themeId → بازسازی نمودار با تغییر تم

  return (
    <div style={{ padding: 24, maxWidth: 1200, margin: "0 auto" }}>
      <div style={{ marginBottom: 16 }}>
        <Link to="/">← بازگشت به صفحه اصلی</Link>
      </div>

      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 16,
        }}
      >
        <h1 style={{ fontSize: 22 }}>BTC/USDT</h1>
        <select
          value={timeframe}
          onChange={(e) => setTimeframe(e.target.value)}
          style={{
            background: "var(--color-card)",
            color: "var(--color-text)",
            padding: "8px 12px",
            borderRadius: 4,
            border: "1px solid var(--color-border)",
            fontSize: 14,
          }}
        >
          {TIMEFRAMES.map((tf) => (
            <option key={tf.value} value={tf.value}>
              {tf.label}
            </option>
          ))}
        </select>
      </header>

      {meta.count > 0 && !error && (
        <div
          style={{
            fontSize: 13,
            color: "var(--color-text-muted)",
            marginBottom: 12,
          }}
        >
          {meta.count} از {meta.total} کندل نمایش داده می‌شود
        </div>
      )}

      {error && (
        <div
          style={{
            padding: 12,
            background: "var(--color-danger-bg)",
            color: "var(--color-danger)",
            border: "1px solid var(--color-danger)",
            borderRadius: 4,
            marginBottom: 12,
            fontSize: 14,
          }}
        >
          {error}
        </div>
      )}

      <div style={{ position: "relative" }}>
        <div
          ref={chartContainerRef}
          style={{
            width: "100%",
            minHeight: 500,
            background: "var(--color-card)",
            borderRadius: 4,
          }}
        />
        {loading && (
          <div
            style={{
              position: "absolute",
              inset: 0,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              background: "var(--color-bg)",
              opacity: 0.7,
              color: "var(--color-text-muted)",
              fontSize: 14,
              zIndex: 10,
            }}
          >
            در حال بارگذاری نمودار...
          </div>
        )}
      </div>
    </div>
  );
}
"""


# ============================================================
# تابع کمکی برای نوشتن فایل با ایجاد parent ها
# ============================================================
def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"  ✓ {path.relative_to(PROJECT_ROOT)}")


def main():
    print("=" * 64)
    print("اسکریپت ۲۷ — زیرگام ۸.۱: Theme Engine Foundation")
    print("=" * 64)
    print()

    # بررسی پیش‌نیاز: پوشه frontend/src باید موجود باشد
    if not FRONTEND_SRC.exists():
        print(f"[ERROR] پوشه frontend پیدا نشد: {FRONTEND_SRC}")
        print("        قبل از این اسکریپت زیرگام‌های ۷.۱ تا ۷.۳ باید اجرا شده باشند.")
        raise SystemExit(1)

    print("📁 فایل‌های جدید:")
    write_file(THEMES_JS, THEMES_JS_CONTENT)
    write_file(THEME_STORE, THEME_STORE_CONTENT)
    write_file(THEME_PROVIDER, THEME_PROVIDER_CONTENT)

    print()
    print("✏️  فایل‌های به‌روز:")
    write_file(INDEX_CSS, INDEX_CSS_CONTENT)
    write_file(MAIN_JSX, MAIN_JSX_CONTENT)
    write_file(LOGIN_PAGE, LOGIN_PAGE_CONTENT)
    write_file(HOME_PAGE, HOME_PAGE_CONTENT)
    write_file(CHART_PAGE, CHART_PAGE_CONTENT)

    print()
    print("=" * 64)
    print("✅ ۸ فایل ساخته/به‌روز شد.")
    print("=" * 64)
    print()
    print("Vite خودش hot reload می‌کند.")
    print()
    print("تست‌ها:")
    print("  ۱) مرورگر: http://localhost:5173/")
    print("     → اگر لاگین هستی، صفحه home با dropdown «بایننس تاریک» در header")
    print("  ۲) از dropdown، تم «روشن مینیمال» را انتخاب کن")
    print("     → کل صفحه باید بلافاصله سفید شود (body + card + متن)")
    print("  ۳) refresh کن (F5) → تم انتخابی persist باشد")
    print("  ۴) برو /login → باید رنگ‌بندی تم انتخابی را داشته باشد")
    print("  ۵) برگرد / → /chart/1")
    print("     → نمودار + کندل‌ها باید با رنگ‌های تم رندر شوند")
    print("  ۶) از home تم را عوض کن، برگرد /chart/1")
    print("     → نمودار با رنگ‌های تم جدید بازسازی می‌شود")
    print("  ۷) DevTools → Application → Local Storage")
    print("     → کلید `theme-storage` با مقدار JSON دیده شود")
    print()
    print("اگر همه چک‌ها سبز شد، زیرگام ۸.۱ کامل است.")
    print("گام بعدی: اسکریپت ۲۸ — Toast Notifications")


if __name__ == "__main__":
    main()
