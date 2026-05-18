import React from 'react';
import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api.js";
import useAuthStore from "../stores/authStore.js";
import useConfirmStore from "../stores/confirmStore.js";
import { formatNumber } from "../utils/numberFormat.js";

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
          <h1 style={{ fontSize: "1.57rem", marginBottom: 4, fontWeight: 600 }}>
            سامانه هوشمند ترید
          </h1>
          {user ? (
            <div style={{ fontSize: "0.93rem", color: "var(--color-text-muted)" }}>
              کاربر:{" "}
              <strong style={{ color: "var(--color-text)" }}>
                {user.username}
              </strong>
              {" — "}نقش: {user.role}
            </div>
          ) : (
            <div style={{ fontSize: "0.93rem", color: "var(--color-text-muted)" }}>
              در حال بارگذاری...
            </div>
          )}
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
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
              fontSize: "1.29rem",
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
              fontSize: "0.93rem",
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
            fontSize: "1rem",
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
                fontSize: "1.07rem",
                color: "var(--color-link)",
                fontWeight: 500,
              }}
            >
              <span>📊 BTC/USDT — روزانه</span>
              <span
                style={{
                  color: "var(--color-text-muted)",
                  fontSize: "0.86rem",
                  fontWeight: 400,
                }}
              >
                {formatNumber(1714)} کندل
              </span>
            </Link>
          </li>
        </ul>
      </section>
    </div>
  );
}
