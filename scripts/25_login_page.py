# -*- coding: utf-8 -*-
"""
اسکریپت ۲۵ — زیرگام ۷.۲: پیاده‌سازی login واقعی
================================================================
این اسکریپت idempotent است.

فایل‌های به‌روز (۲ فایل):
  ۱) frontend/src/pages/LoginPage.jsx  (پیاده‌سازی کامل)
  ۲) frontend/src/pages/HomePage.jsx   (نمایش user + بازخوانی /auth/me)

نکته فنی:
  Backend از OAuth2PasswordRequestForm استفاده می‌کند
  → باید application/x-www-form-urlencoded ارسال شود (نه JSON)
  → از URLSearchParams استفاده می‌شود

پس از اجرا — Vite hot reload خودکار اعمال می‌کند:
  مرورگر: http://localhost:5173/
  → redirect به /login → فرم ورود نمایش داده می‌شود
  → admin / 1 → ورود موفق → redirect به /
================================================================
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
PAGES_DIR = FRONTEND_DIR / "src" / "pages"


# ============================================================
# ۱) frontend/src/pages/LoginPage.jsx
# ============================================================
LOGIN_PAGE_JSX = """import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import api from "../services/api.js";
import useAuthStore from "../stores/authStore.js";

/* استایل‌های مشترک */
const cardStyle = {
  width: "100%",
  maxWidth: 400,
  background: "#2a2e39",
  padding: 32,
  borderRadius: 8,
  boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
};

const inputStyle = {
  width: "100%",
  padding: "10px 12px",
  background: "#1e222d",
  border: "1px solid #363a45",
  borderRadius: 4,
  color: "#d1d4dc",
  fontSize: 14,
};

const labelStyle = {
  display: "block",
  marginBottom: 6,
  fontSize: 13,
  color: "#787b86",
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

  // اگر قبلاً لاگین است، redirect به مقصد قبلی یا /
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
      // OAuth2PasswordRequestForm نیاز به form-urlencoded دارد
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      const resp = await api.post("/auth/login", formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      const { access_token, refresh_token } = resp.data.data;
      setTokens(access_token, refresh_token);

      // دریافت اطلاعات کاربر
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
              background: "#3a1f1f",
              color: "#ff6b6b",
              border: "1px solid #5a2a2a",
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
            background: loading ? "#1a3a8f" : "#2962ff",
            color: "white",
            borderRadius: 4,
            fontSize: 15,
            fontWeight: 500,
            transition: "background 0.2s",
          }}
        >
          {loading ? "در حال ورود..." : "ورود"}
        </button>

        <div
          style={{
            marginTop: 20,
            paddingTop: 16,
            borderTop: "1px solid #363a45",
            fontSize: 12,
            color: "#787b86",
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
# ۲) frontend/src/pages/HomePage.jsx
# ============================================================
HOME_PAGE_JSX = """import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api.js";
import useAuthStore from "../stores/authStore.js";

export default function HomePage() {
  const navigate = useNavigate();
  const user = useAuthStore((s) => s.user);
  const setUser = useAuthStore((s) => s.setUser);
  const logout = useAuthStore((s) => s.logout);

  // اگر user در store نیست (مثلاً پس از refresh مرورگر)، از /auth/me بخوان
  useEffect(() => {
    if (!user) {
      api
        .get("/auth/me")
        .then((resp) => setUser(resp.data.data))
        .catch(() => {
          // interceptor 401 را خودش هندل می‌کند
        });
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
          borderBottom: "1px solid #363a45",
        }}
      >
        <div>
          <h1 style={{ fontSize: 22, marginBottom: 4 }}>سامانه هوشمند ترید</h1>
          {user ? (
            <div style={{ fontSize: 13, color: "#787b86" }}>
              کاربر: <strong style={{ color: "#d1d4dc" }}>{user.username}</strong>
              {" — "}نقش: {user.role}
            </div>
          ) : (
            <div style={{ fontSize: 13, color: "#787b86" }}>
              در حال بارگذاری...
            </div>
          )}
        </div>
        <button
          onClick={handleLogout}
          style={{
            background: "#2a2e39",
            color: "#d1d4dc",
            padding: "8px 16px",
            borderRadius: 4,
            border: "1px solid #363a45",
            fontSize: 13,
          }}
        >
          خروج
        </button>
      </header>

      <section>
        <h2
          style={{
            fontSize: 16,
            marginBottom: 12,
            color: "#787b86",
            fontWeight: 500,
          }}
        >
          نمودارها
        </h2>
        <ul style={{ listStyle: "none" }}>
          <li
            style={{
              padding: 14,
              background: "#2a2e39",
              borderRadius: 4,
              border: "1px solid #363a45",
            }}
          >
            <Link
              to="/chart/1"
              style={{ fontSize: 15, display: "flex", justifyContent: "space-between" }}
            >
              <span>📊 BTC/USDT — روزانه</span>
              <span style={{ color: "#787b86", fontSize: 12 }}>1714 کندل</span>
            </Link>
          </li>
        </ul>
      </section>
    </div>
  );
}
"""


FILES_TO_WRITE: dict[Path, str] = {
    PAGES_DIR / "LoginPage.jsx": LOGIN_PAGE_JSX,
    PAGES_DIR / "HomePage.jsx": HOME_PAGE_JSX,
}


def main() -> None:
    print("=" * 64)
    print("اسکریپت ۲۵ — زیرگام ۷.۲: پیاده‌سازی login واقعی")
    print("=" * 64)

    if not FRONTEND_DIR.exists():
        print(f"[ERROR] پوشه frontend پیدا نشد: {FRONTEND_DIR}")
        raise SystemExit(1)

    for path, content in FILES_TO_WRITE.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"  ✓ {path.relative_to(PROJECT_ROOT)}")

    print()
    print("=" * 64)
    print(f"✅ {len(FILES_TO_WRITE)} فایل به‌روز شد.")
    print("=" * 64)
    print()
    print("Vite خودش hot reload می‌کند — نیاز به restart نیست.")
    print()
    print("تست:")
    print("  ۱) مرورگر: http://localhost:5173/  (refresh یا باز کن)")
    print("  ۲) فرم ورود نمایش داده می‌شود")
    print("  ۳) admin / 1 → ورود → redirect به /")
    print("  ۴) صفحه اصلی + اطلاعات کاربر admin/admin نمایش داده می‌شود")
    print("  ۵) خروج → بازگشت به /login")


if __name__ == "__main__":
    main()
