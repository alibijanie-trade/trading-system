import React from 'react';
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
    ].join("\n");

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
