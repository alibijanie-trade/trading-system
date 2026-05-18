# -*- coding: utf-8 -*-
"""
اسکریپت ۲۹ — زیرگام ۸.۳: Skeleton + ConfirmDialog
================================================================
این اسکریپت idempotent است — قابل اجرا چندبار بدون شکست.

محتوای زیرگام ۸.۳:
  ۱) SkeletonBlock کامپوننت — placeholder متحرک با ۴ variant
  ۲) confirmStore (Zustand) — Promise-based askConfirm()
  ۳) ConfirmDialog کامپوننت — مودال با Variant Indicator Pattern
  ۴) ادغام در صفحات: ChartPage (Skeleton) + HomePage (Confirm logout)
  ۵) index.css — keyframes برای shimmer + dialog

اصول طراحی (طبق سند v2.6):
  - بدون hex hardcoded — فقط CSS variables تم
  - Variant Indicator Pattern (۸.۸.۱):
      کانتینر از تم + accent باریک ۴px + icon رنگی
  - Interactive States (۸.۷.۱):
      hover/active/focus-visible/disabled — همه از index.css
  - Skeleton: shimmer با gradient از CSS variables
  - ConfirmDialog: focus trap، Escape، backdrop click
  - prefers-reduced-motion پشتیبانی می‌شود

فایل‌های جدید:
  frontend/src/components/common/SkeletonBlock.jsx
  frontend/src/components/common/ConfirmDialog.jsx
  frontend/src/stores/confirmStore.js

فایل‌های به‌روزرسانی:
  frontend/src/index.css       (افزودن @keyframes + .skeleton-block)
  frontend/src/App.jsx         (mount <ConfirmDialog />)
  frontend/src/pages/HomePage.jsx   (await askConfirm)
  frontend/src/pages/ChartPage.jsx  (<SkeletonBlock>)
================================================================
"""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FRONTEND = PROJECT_ROOT / "frontend" / "src"

COMMON_DIR = FRONTEND / "components" / "common"
STORES_DIR = FRONTEND / "stores"
PAGES_DIR = FRONTEND / "pages"

SKELETON_JSX = COMMON_DIR / "SkeletonBlock.jsx"
CONFIRM_JSX = COMMON_DIR / "ConfirmDialog.jsx"
CONFIRM_STORE = STORES_DIR / "confirmStore.js"

INDEX_CSS = FRONTEND / "index.css"
APP_JSX = FRONTEND / "App.jsx"
HOME_JSX = PAGES_DIR / "HomePage.jsx"
CHART_JSX = PAGES_DIR / "ChartPage.jsx"


# ============================================================
# محتوای فایل‌های جدید
# ============================================================

SKELETON_BLOCK_JSX = """/**
 * SkeletonBlock — placeholder متحرک برای حالات بارگذاری
 * طبق سند ۸.۳ (Skeleton Screen برای loading states)
 *
 * Props:
 *   variant: "rect" | "text" | "circle" | "line"  (default: "rect")
 *   width:   string | number  (default: depends on variant)
 *   height:  string | number  (default: depends on variant)
 *   radius:  string | number  (default: depends on variant)
 *   count:   number           (default: 1) — برای variant های text/line
 *   gap:     number           (default: 8) — فاصله بین آیتم‌ها
 *   style:   object           — استایل اضافی
 *
 * رنگ از CSS variables تم — هیچ hex hardcoded:
 *   --color-card-hover   (پایه)
 *   --color-border-strong (موج shimmer)
 *
 * Accessibility:
 *   aria-hidden="true" + role="presentation"
 *   prefers-reduced-motion — animation غیرفعال می‌شود (در index.css)
 */
export default function SkeletonBlock({
  variant = "rect",
  width,
  height,
  radius,
  count = 1,
  gap = 8,
  style = {},
}) {
  const defaults = VARIANT_DEFAULTS[variant] || VARIANT_DEFAULTS.rect;

  const finalWidth = width ?? defaults.width;
  const finalHeight = height ?? defaults.height;
  const finalRadius = radius ?? defaults.radius;

  const toUnit = (v) => (typeof v === "number" ? `${v}px` : v);

  const items = Array.from({ length: Math.max(1, count) }, (_, i) => (
    <div
      key={i}
      className="skeleton-block"
      role="presentation"
      aria-hidden="true"
      style={{
        width: toUnit(finalWidth),
        height: toUnit(finalHeight),
        borderRadius: toUnit(finalRadius),
        marginBottom: count > 1 && i < count - 1 ? gap : 0,
        ...style,
      }}
    />
  ));

  return count > 1 ? <>{items}</> : items[0];
}

const VARIANT_DEFAULTS = {
  rect:   { width: "100%", height: 16, radius: 4 },
  text:   { width: "100%", height: 12, radius: 4 },
  circle: { width: 40,     height: 40, radius: "50%" },
  line:   { width: "100%", height: 1,  radius: 0 },
};
"""


CONFIRM_STORE_JS = """import { create } from "zustand";

/**
 * confirmStore — مدیریت ConfirmDialog سراسری
 *
 * Usage در هر کامپوننت:
 *   const askConfirm = useConfirmStore((s) => s.confirm);
 *   const ok = await askConfirm({
 *     title: "خروج",
 *     message: "آیا مطمئنید؟",
 *     variant: "warning",      // "danger" | "warning" | "info"
 *     confirmText: "خروج",
 *     cancelText: "انصراف",
 *   });
 *   if (!ok) return;
 *
 * هر بار فقط یک dialog فعال است (single-instance).
 * Promise با true (تأیید) یا false (انصراف/Escape/backdrop) resolve می‌شود.
 */

const INITIAL_STATE = {
  isOpen: false,
  title: "",
  message: "",
  variant: "info",
  confirmText: "تأیید",
  cancelText: "انصراف",
  resolver: null,
};

const useConfirmStore = create((set, get) => ({
  ...INITIAL_STATE,

  confirm: (opts = {}) =>
    new Promise((resolve) => {
      // اگر dialog قبلی باز است، آن را با false reject کن
      const prev = get().resolver;
      if (prev) prev(false);

      set({
        isOpen: true,
        title: opts.title || "",
        message: opts.message || "",
        variant: opts.variant || "info",
        confirmText: opts.confirmText || "تأیید",
        cancelText: opts.cancelText || "انصراف",
        resolver: resolve,
      });
    }),

  confirmAccept: () => {
    const { resolver } = get();
    if (resolver) resolver(true);
    set({ ...INITIAL_STATE });
  },

  confirmReject: () => {
    const { resolver } = get();
    if (resolver) resolver(false);
    set({ ...INITIAL_STATE });
  },
}));

export default useConfirmStore;
"""


CONFIRM_DIALOG_JSX = """import { useEffect, useRef } from "react";
import useConfirmStore from "../../stores/confirmStore.js";

/**
 * ConfirmDialog — مودال تأیید سراسری
 * طبق سند ۸.۸.۱ (Variant Indicator Pattern):
 *   - کانتینر از تم: var(--color-card) + var(--color-border)
 *   - accent باریک ۴px در سمت start (RTL = راست) با رنگ variant
 *   - icon رنگی به عنوان indicator دوم
 *   - متن همیشه از var(--color-text)
 *
 * Accessibility:
 *   role="dialog" + aria-modal="true" + aria-labelledby
 *   focus خودکار روی دکمه تأیید
 *   Escape → reject
 *   click backdrop → reject
 *
 * بدون hex hardcoded — همه از CSS variables.
 */

const VARIANT_CONFIG = {
  danger:  { icon: "⚠", color: "var(--color-danger)" },
  warning: { icon: "⚠", color: "var(--color-warning)" },
  info:    { icon: "ℹ", color: "var(--color-info)" },
};

export default function ConfirmDialog() {
  const isOpen = useConfirmStore((s) => s.isOpen);
  const title = useConfirmStore((s) => s.title);
  const message = useConfirmStore((s) => s.message);
  const variant = useConfirmStore((s) => s.variant);
  const confirmText = useConfirmStore((s) => s.confirmText);
  const cancelText = useConfirmStore((s) => s.cancelText);
  const confirmAccept = useConfirmStore((s) => s.confirmAccept);
  const confirmReject = useConfirmStore((s) => s.confirmReject);

  const confirmBtnRef = useRef(null);
  const cancelBtnRef = useRef(null);
  const cfg = VARIANT_CONFIG[variant] || VARIANT_CONFIG.info;

  // focus + keyboard handling
  useEffect(() => {
    if (!isOpen) return;

    const t = setTimeout(() => confirmBtnRef.current?.focus(), 50);

    const onKey = (e) => {
      if (e.key === "Escape") {
        e.preventDefault();
        confirmReject();
      } else if (e.key === "Tab") {
        // focus trap ساده — فقط بین دو دکمه چرخش کند
        const active = document.activeElement;
        if (e.shiftKey && active === cancelBtnRef.current) {
          e.preventDefault();
          confirmBtnRef.current?.focus();
        } else if (!e.shiftKey && active === confirmBtnRef.current) {
          e.preventDefault();
          cancelBtnRef.current?.focus();
        }
      }
    };
    window.addEventListener("keydown", onKey);

    return () => {
      clearTimeout(t);
      window.removeEventListener("keydown", onKey);
    };
  }, [isOpen, confirmAccept, confirmReject]);

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="confirm-dialog-title"
      aria-describedby="confirm-dialog-message"
      onClick={confirmReject}
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0, 0, 0, 0.5)",
        backdropFilter: "blur(2px)",
        WebkitBackdropFilter: "blur(2px)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
        animation: "dialog-fade-in 0.15s ease-out",
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          background: "var(--color-card)",
          border: "1px solid var(--color-border)",
          borderInlineStart: `4px solid ${cfg.color}`,
          borderRadius: 6,
          boxShadow: "var(--shadow-card)",
          width: "min(440px, 92vw)",
          padding: "20px 24px",
          animation: "dialog-slide-in 0.2s ease-out",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 10,
            marginBottom: 12,
          }}
        >
          <span
            aria-hidden="true"
            style={{
              color: cfg.color,
              fontSize: 20,
              fontWeight: 700,
              lineHeight: 1,
            }}
          >
            {cfg.icon}
          </span>
          <h3
            id="confirm-dialog-title"
            style={{
              margin: 0,
              fontSize: 16,
              fontWeight: 600,
              color: "var(--color-text)",
            }}
          >
            {title}
          </h3>
        </div>

        <p
          id="confirm-dialog-message"
          style={{
            margin: "0 0 20px",
            fontSize: 14,
            lineHeight: 1.7,
            color: "var(--color-text)",
          }}
        >
          {message}
        </p>

        <div
          style={{
            display: "flex",
            gap: 8,
            justifyContent: "flex-end",
          }}
        >
          <button
            ref={cancelBtnRef}
            type="button"
            onClick={confirmReject}
            style={{
              padding: "8px 16px",
              fontSize: 13,
              borderRadius: 4,
              background: "transparent",
              color: "var(--color-text)",
              border: "1px solid var(--color-border-strong)",
              fontWeight: 500,
              minWidth: 80,
            }}
          >
            {cancelText}
          </button>
          <button
            ref={confirmBtnRef}
            type="button"
            onClick={confirmAccept}
            style={{
              padding: "8px 16px",
              fontSize: 13,
              borderRadius: 4,
              background: cfg.color,
              color: "var(--color-text-inverse)",
              border: `1px solid ${cfg.color}`,
              fontWeight: 600,
              minWidth: 80,
            }}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
}
"""


# ============================================================
# index.css — محتوای کامل به‌روز
# (افزودن skeleton + dialog به نسخه فعلی)
# ============================================================

INDEX_CSS_NEW = """/* ============================================================
   Reset + پایه — زیرگام ۸ (Theme Engine)
   متغیرهای CSS توسط ThemeProvider روی :root تزریق می‌شوند.
   مقادیر :root زیر صرفاً fallback اولیه‌اند (پیش از mount).
   ۲۷c — رنگ‌های fallback به استانداردهای رسمی بایننس.
   ۲۷e — interactive states (hover/focus/active) به سبک بایننس.
   ۲۸  — @keyframes toast-slide-in برای Toast Notifications.
   🆕 ۲۹ — @keyframes dialog + .skeleton-block برای زیرگام ۸.۳.
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
   Toast animations (۲۸)
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
   🆕 Skeleton + Dialog animations (۲۹ — زیرگام ۸.۳)
   ============================================================ */

.skeleton-block {
  display: block;
  background: linear-gradient(
    90deg,
    var(--color-card-hover) 0%,
    var(--color-border-strong) 50%,
    var(--color-card-hover) 100%
  );
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.4s ease-in-out infinite;
  border-radius: 4px;
}

@keyframes skeleton-shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@keyframes dialog-fade-in {
  from { opacity: 0; }
  to   { opacity: 1; }
}

@keyframes dialog-slide-in {
  from {
    opacity: 0;
    transform: translateY(-8px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton-block {
    animation: none;
    background: var(--color-card-hover);
  }

  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
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


# ============================================================
# App.jsx — افزودن import + mount ConfirmDialog
# ============================================================

APP_JSX_NEW = """import { Routes, Route, Navigate } from "react-router-dom";
import ProtectedRoute from "./components/common/ProtectedRoute.jsx";
import ToastContainer from "./components/common/ToastContainer.jsx";
import ConfirmDialog from "./components/common/ConfirmDialog.jsx";
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
      <ConfirmDialog />
    </>
  );
}
"""


# ============================================================
# HomePage.jsx — افزودن askConfirm قبل از logout
# ============================================================

HOME_JSX_NEW = """import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api.js";
import useAuthStore from "../stores/authStore.js";
import useThemeStore from "../stores/themeStore.js";
import useConfirmStore from "../stores/confirmStore.js";
import { listThemes } from "../themes/themes.js";

export default function HomePage() {
  const navigate = useNavigate();
  const user = useAuthStore((s) => s.user);
  const setUser = useAuthStore((s) => s.setUser);
  const logout = useAuthStore((s) => s.logout);

  const themeId = useThemeStore((s) => s.themeId);
  const setTheme = useThemeStore((s) => s.setTheme);

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


# ============================================================
# ChartPage.jsx — جایگزینی متن loading با SkeletonBlock
# ============================================================

CHART_JSX_NEW = """import { useEffect, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { createChart, CrosshairMode } from "lightweight-charts";
import api from "../services/api.js";
import useThemeStore from "../stores/themeStore.js";
import SkeletonBlock from "../components/common/SkeletonBlock.jsx";

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

      {/* متادیتا — هنگام loading جایگزین با Skeleton */}
      {loading ? (
        <div style={{ marginBottom: 12 }}>
          <SkeletonBlock variant="text" width={220} height={13} />
        </div>
      ) : meta.count > 0 && !error ? (
        <div
          style={{
            fontSize: 13,
            color: "var(--color-text-muted)",
            marginBottom: 12,
          }}
        >
          {meta.count} از {meta.total} کندل نمایش داده می‌شود
        </div>
      ) : null}

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
            opacity: loading ? 0 : 1,
            transition: "opacity 0.2s ease",
          }}
        />
        {loading && (
          <div
            style={{
              position: "absolute",
              inset: 0,
              padding: 16,
              display: "flex",
              flexDirection: "column",
              gap: 12,
              background: "var(--color-card)",
              borderRadius: 4,
              border: "1px solid var(--color-border)",
            }}
          >
            {/* نوار بالا — شبیه ناحیه عنوان و قیمت */}
            <div style={{ display: "flex", gap: 12 }}>
              <SkeletonBlock variant="rect" width={120} height={20} />
              <SkeletonBlock variant="rect" width={80} height={20} />
            </div>
            {/* بدنه — شبیه ناحیه نمودار */}
            <SkeletonBlock
              variant="rect"
              width="100%"
              height="100%"
              style={{ flex: 1, minHeight: 380 }}
            />
            {/* نوار پایین — شبیه ناحیه تاریخ */}
            <SkeletonBlock variant="rect" width="100%" height={24} />
          </div>
        )}
      </div>
    </div>
  );
}
"""


# ============================================================
# تابع نوشتن idempotent
# ============================================================


def write_if_changed(path: Path, content: str, label: str) -> str:
    """
    اگر محتوای فعلی با content یکسان است: skip
    در غیر این صورت: بازنویسی
    خروجی: "created" | "updated" | "unchanged"
    """
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
    print("اسکریپت ۲۹ — زیرگام ۸.۳: Skeleton + ConfirmDialog")
    print("=" * 64)
    print()

    # پیش‌چک: ساختار frontend موجود است؟
    if not FRONTEND.exists():
        print("[ERROR] دایرکتوری frontend/src یافت نشد.")
        print("        ابتدا اسکریپت ۲۴ (scaffold) را اجرا کنید.")
        return 1

    # پیش‌چک: فایل‌های واجب موجودند؟
    required = [INDEX_CSS, APP_JSX, HOME_JSX, CHART_JSX]
    missing = [p for p in required if not p.exists()]
    if missing:
        print("[ERROR] فایل‌های واجب یافت نشدند:")
        for p in missing:
            print(f"        - {p.relative_to(PROJECT_ROOT)}")
        return 1

    print("--- فایل‌های جدید ---")
    write_if_changed(SKELETON_JSX, SKELETON_BLOCK_JSX, "SkeletonBlock")
    write_if_changed(CONFIRM_STORE, CONFIRM_STORE_JS, "confirmStore")
    write_if_changed(CONFIRM_JSX, CONFIRM_DIALOG_JSX, "ConfirmDialog")

    print()
    print("--- فایل‌های به‌روزرسانی ---")
    write_if_changed(INDEX_CSS, INDEX_CSS_NEW, "shimmer + dialog keyframes")
    write_if_changed(APP_JSX, APP_JSX_NEW, "mount ConfirmDialog")
    write_if_changed(HOME_JSX, HOME_JSX_NEW, "askConfirm در logout")
    write_if_changed(CHART_JSX, CHART_JSX_NEW, "SkeletonBlock در loading")

    print()
    print("=" * 64)
    print("✅ زیرگام ۸.۳ اعمال شد.")
    print("=" * 64)
    print()
    print("گام بعدی:")
    print("  🟩 tab «2 scripts»:  python scripts/29b_test_skeleton_confirm.py")
    print()
    print("سپس چک بصری در 🟧 tab «3 frontend»:")
    print("  ۱) refresh مرورگر")
    print("  ۲) رفتن به صفحه نمودار → ابتدا چند Skeleton shimmer دیده شود")
    print("  ۳) برگشت به HomePage → کلیک خروج → dialog نارنجی با accent راست")
    print("  ۴) تست Escape و کلیک backdrop → cancel")
    print("  ۵) تست Tab → focus بین دو دکمه می‌چرخد")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
