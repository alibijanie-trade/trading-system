# -*- coding: utf-8 -*-
"""
اسکریپت ۳۵ — Error Boundaries (T2.01)
================================================================
Task: T2.01 (Tier 2 — Quality Hardening)

این اسکریپت idempotent است — قابل اجرا چندبار بدون شکست.

محتوای کار:
  ۱) ساخت frontend/src/components/common/ErrorBoundary.jsx
     کامپوننت کلاسی React که خطاهای زیرشاخه را catch می‌کند.

  ۲) به‌روزرسانی frontend/src/App.jsx برای wrap کردن:
     - یک ErrorBoundary سراسری (outer) — کل برنامه
     - یک ErrorBoundary به ازای هر Route (inner) — recovery per-page

طراحی ErrorBoundary:
  - class component (تنها روش React برای catch render-time errors)
  - Variant Indicator Pattern (سند ۸.۸.۱):
      کانتینر از تم + accent ۴px رنگ danger + icon ⚠
  - بدون hex hardcoded — همه از CSS variables
  - dev mode: نمایش stack trace در <details> collapsible
  - production mode: فقط پیام دوستانه + دکمه‌ها
  - دو دکمه: «تلاش مجدد» (reset state) + «بارگذاری مجدد» (window.reload)
  - دکمه تک‌بانه «کپی جزئیات» در dev (navigator.clipboard)
  - role="alert" + aria-live="assertive" برای accessibility

محدودیت‌های ذاتی ErrorBoundary (مستندسازی شده):
  ✗ خطاهای event handler — catch نمی‌شوند (باید try/catch دستی)
  ✗ خطاهای async (setTimeout, promises) — catch نمی‌شوند
  ✗ خطاهای SSR — catch نمی‌شوند
  ✓ خطاهای render در درخت زیرین — catch می‌شوند

نحوه اجرا (tab «2 scripts»):
    python scripts\\35_error_boundaries.py

سپس برای تست:
    python scripts\\35b_test_error_boundaries.py
================================================================
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FRONTEND_SRC = PROJECT_ROOT / "frontend" / "src"

ERROR_BOUNDARY_PATH = FRONTEND_SRC / "components" / "common" / "ErrorBoundary.jsx"
APP_JSX_PATH        = FRONTEND_SRC / "App.jsx"


# ────────────────────────────────────────────────────────────────
# محتوای ErrorBoundary.jsx
# ────────────────────────────────────────────────────────────────
ERROR_BOUNDARY_CONTENT = '''\
import { Component } from "react";

/**
 * ErrorBoundary — مرز خطای سراسری React
 *
 * طبق سند ۸.۸.۱ (Variant Indicator Pattern):
 *   - کانتینر از تم: var(--color-card) + var(--color-border)
 *   - accent باریک ۴px در سمت start (RTL = راست) با رنگ danger
 *   - icon ⚠ به عنوان indicator دوم
 *   - متن همیشه از var(--color-text)
 *
 * Props (همه اختیاری):
 *   - fallback: (info) => ReactNode      // فراخوانی به جای fallback پیش‌فرض
 *   - onReset: () => void                 // در زمان "تلاش مجدد"
 *   - label: string                       // نام مرز برای logging
 *
 * Accessibility:
 *   role="alert" + aria-live="assertive"
 *
 * بدون hex hardcoded — همه از CSS variables.
 *
 * محدودیت‌های ذاتی (React docs):
 *   - فقط خطاهای render-time در زیر-درخت
 *   - event handlers و async errors را catch نمی‌کند
 */

const DANGER = "var(--color-danger)";

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
      copied: false,
    };
  }

  static getDerivedStateFromError(error) {
    // به‌روزرسانی state برای render بعدی با fallback
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // logging رسمی — در آینده Sentry/Loguru
    const label = this.props.label ? `[${this.props.label}] ` : "";
    // eslint-disable-next-line no-console
    console.error(`${label}ErrorBoundary caught:`, error, errorInfo);
    this.setState({ errorInfo });
  }

  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
      copied: false,
    });
    if (typeof this.props.onReset === "function") {
      this.props.onReset();
    }
  };

  handleReload = () => {
    // full page reload — قوی‌ترین فرم recovery
    window.location.reload();
  };

  handleCopyDetails = async () => {
    const text = [
      `Error: ${this.state.error?.message ?? "unknown"}`,
      `Name: ${this.state.error?.name ?? "Error"}`,
      "",
      "Stack:",
      this.state.error?.stack ?? "(no stack)",
      "",
      "Component stack:",
      this.state.errorInfo?.componentStack ?? "(no component stack)",
    ].join("\\n");

    try {
      await navigator.clipboard.writeText(text);
      this.setState({ copied: true });
      setTimeout(() => {
        // فقط اگر هنوز mount است
        if (this.state.hasError) {
          this.setState({ copied: false });
        }
      }, 1500);
    } catch {
      // clipboard API ممکن است در HTTP یا without permission fail شود
      // silently ignore — کاربر می‌تواند stack را manual کپی کند
    }
  };

  render() {
    if (!this.state.hasError) {
      return this.props.children;
    }

    // اگر fallback سفارشی داده شده، آن را render کن
    if (typeof this.props.fallback === "function") {
      return this.props.fallback({
        error: this.state.error,
        errorInfo: this.state.errorInfo,
        reset: this.handleReset,
      });
    }

    const isDev = import.meta.env.DEV;
    const { error, errorInfo, copied } = this.state;

    return (
      <div
        role="alert"
        aria-live="assertive"
        aria-labelledby="error-boundary-title"
        style={{
          minHeight: "60vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: "var(--color-bg)",
          padding: "1.43rem",
          boxSizing: "border-box",
        }}
      >
        <div
          style={{
            background: "var(--color-card)",
            border: "1px solid var(--color-border)",
            borderInlineStart: `4px solid ${DANGER}`,
            borderRadius: 6,
            boxShadow: "var(--shadow-card)",
            width: "min(580px, 100%)",
            padding: "1.71rem 1.86rem",
          }}
        >
          {/* Header */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 12,
              marginBottom: "1.14rem",
            }}
          >
            <span
              aria-hidden="true"
              style={{
                color: DANGER,
                fontSize: "2rem",
                lineHeight: 1,
                fontWeight: 700,
              }}
            >
              ⚠
            </span>
            <h1
              id="error-boundary-title"
              style={{
                margin: 0,
                fontSize: "1.43rem",
                fontWeight: 600,
                color: "var(--color-text)",
              }}
            >
              خطایی رخ داد
            </h1>
          </div>

          {/* Message */}
          <p
            style={{
              margin: "0 0 1.43rem",
              fontSize: "1rem",
              lineHeight: 1.7,
              color: "var(--color-text)",
            }}
          >
            متأسفانه در نمایش این بخش از برنامه خطایی پیش آمد. می‌توانید
            تلاش مجدد کنید یا کل صفحه را دوباره بارگذاری کنید.
          </p>

          {/* Dev-only details */}
          {isDev && error && (
            <details
              style={{
                marginBottom: "1.43rem",
                padding: "0.86rem",
                background: "var(--color-bg-elevated)",
                border: "1px solid var(--color-border)",
                borderRadius: 4,
                fontSize: "0.86rem",
              }}
            >
              <summary
                style={{
                  cursor: "pointer",
                  color: "var(--color-text-muted)",
                  fontWeight: 500,
                  userSelect: "none",
                }}
              >
                جزئیات فنی (فقط در حالت توسعه)
              </summary>
              <div style={{ marginTop: "0.71rem" }}>
                <strong style={{ color: DANGER }}>
                  {error.name || "Error"}:
                </strong>{" "}
                <span style={{ color: "var(--color-text)" }}>
                  {error.message}
                </span>
              </div>
              {error.stack && (
                <pre
                  style={{
                    marginTop: "0.57rem",
                    marginBottom: 0,
                    fontFamily:
                      "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace",
                    fontSize: "0.79rem",
                    color: "var(--color-text-muted)",
                    whiteSpace: "pre-wrap",
                    wordBreak: "break-word",
                    maxHeight: 240,
                    overflow: "auto",
                    direction: "ltr",
                    textAlign: "left",
                  }}
                >
                  {error.stack}
                </pre>
              )}
              {errorInfo?.componentStack && (
                <div style={{ marginTop: "0.71rem" }}>
                  <div
                    style={{
                      color: "var(--color-text-muted)",
                      fontWeight: 500,
                      marginBottom: "0.36rem",
                    }}
                  >
                    Component stack:
                  </div>
                  <pre
                    style={{
                      margin: 0,
                      fontFamily:
                        "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace",
                      fontSize: "0.79rem",
                      color: "var(--color-text-muted)",
                      whiteSpace: "pre-wrap",
                      wordBreak: "break-word",
                      maxHeight: 160,
                      overflow: "auto",
                      direction: "ltr",
                      textAlign: "left",
                    }}
                  >
                    {errorInfo.componentStack}
                  </pre>
                </div>
              )}
            </details>
          )}

          {/* Buttons */}
          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              gap: 8,
              justifyContent: "flex-end",
            }}
          >
            {isDev && (
              <button
                type="button"
                onClick={this.handleCopyDetails}
                aria-live="polite"
                style={{
                  padding: "8px 14px",
                  fontSize: "0.86rem",
                  borderRadius: 4,
                  background: "transparent",
                  color: "var(--color-text-muted)",
                  border: "1px solid var(--color-border-strong)",
                  fontWeight: 500,
                  cursor: "pointer",
                }}
              >
                {copied ? "✓ کپی شد" : "کپی جزئیات"}
              </button>
            )}
            <button
              type="button"
              onClick={this.handleReset}
              style={{
                padding: "8px 16px",
                fontSize: "0.93rem",
                borderRadius: 4,
                background: "transparent",
                color: "var(--color-text)",
                border: "1px solid var(--color-border-strong)",
                fontWeight: 500,
                minWidth: 100,
                cursor: "pointer",
              }}
            >
              تلاش مجدد
            </button>
            <button
              type="button"
              onClick={this.handleReload}
              autoFocus
              style={{
                padding: "8px 16px",
                fontSize: "0.93rem",
                borderRadius: 4,
                background: DANGER,
                color: "var(--color-text-inverse)",
                border: `1px solid ${DANGER}`,
                fontWeight: 600,
                minWidth: 120,
                cursor: "pointer",
              }}
            >
              بارگذاری مجدد
            </button>
          </div>
        </div>
      </div>
    );
  }
}
'''


# ────────────────────────────────────────────────────────────────
# محتوای App.jsx (نسخه به‌روز)
# ────────────────────────────────────────────────────────────────
APP_JSX_CONTENT = '''\
import { Routes, Route, Navigate } from "react-router-dom";
import ProtectedRoute from "./components/common/ProtectedRoute.jsx";
import ToastContainer from "./components/common/ToastContainer.jsx";
import ConfirmDialog from "./components/common/ConfirmDialog.jsx";
import ErrorBoundary from "./components/common/ErrorBoundary.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import HomePage from "./pages/HomePage.jsx";
import ChartPage from "./pages/ChartPage.jsx";
import SettingsPage from "./pages/SettingsPage.jsx";

/**
 * استراتژی ErrorBoundary (دفاع در عمق):
 *   - مرز سراسری (outer) — کل Routes را در بر می‌گیرد. آخرین خط دفاع.
 *   - مرز per-route (inner) — هر صفحه‌ی خود را protect می‌کند تا
 *     کاربر بتواند با navigate به مسیر دیگر، از خطا فرار کند.
 */
export default function App() {
  return (
    <>
      <ErrorBoundary label="root">
        <Routes>
          <Route
            path="/login"
            element={
              <ErrorBoundary label="route:login">
                <LoginPage />
              </ErrorBoundary>
            }
          />
          <Route element={<ProtectedRoute />}>
            <Route
              path="/"
              element={
                <ErrorBoundary label="route:home">
                  <HomePage />
                </ErrorBoundary>
              }
            />
            <Route
              path="/chart/:symbolId"
              element={
                <ErrorBoundary label="route:chart">
                  <ChartPage />
                </ErrorBoundary>
              }
            />
            <Route
              path="/settings"
              element={
                <ErrorBoundary label="route:settings">
                  <SettingsPage />
                </ErrorBoundary>
              }
            />
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </ErrorBoundary>
      <ToastContainer />
      <ConfirmDialog />
    </>
  );
}
'''


# ────────────────────────────────────────────────────────────────
# write_if_changed
# ────────────────────────────────────────────────────────────────
def write_if_changed(path: Path, content: str) -> str:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        return "created"
    try:
        current = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        current = path.read_text(encoding="cp1252")
    if current == content:
        return "unchanged"
    path.write_text(content, encoding="utf-8", newline="\n")
    return "updated"


def main() -> int:
    print("=" * 64)
    print("اسکریپت ۳۵ — Error Boundaries (T2.01)")
    print("=" * 64)
    print()

    print("📝 ErrorBoundary.jsx")
    status = write_if_changed(ERROR_BOUNDARY_PATH, ERROR_BOUNDARY_CONTENT)
    icon = {"created": "🆕", "updated": "✏️", "unchanged": "✓"}[status]
    print(f"   {icon} {status}  → {ERROR_BOUNDARY_PATH.relative_to(PROJECT_ROOT)}")
    print()

    print("📝 App.jsx")
    status = write_if_changed(APP_JSX_PATH, APP_JSX_CONTENT)
    icon = {"created": "🆕", "updated": "✏️", "unchanged": "✓"}[status]
    print(f"   {icon} {status}  → {APP_JSX_PATH.relative_to(PROJECT_ROOT)}")
    print()

    print("-" * 64)
    print("✅ پایان. حالا برای تست اجرا کنید:")
    print("   python scripts/35b_test_error_boundaries.py")
    print()
    print("📌 یادآوری: ErrorBoundary فقط خطاهای render-time را catch می‌کند.")
    print("   خطاهای async/event-handler نیاز به try/catch دستی دارند.")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
