import React from 'react';
import { useEffect, useRef } from "react";
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
              fontSize: "1.43rem",
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
              fontSize: "1.14rem",
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
            fontSize: "1rem",
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
              fontSize: "0.93rem",
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
              fontSize: "0.93rem",
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
