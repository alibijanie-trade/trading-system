# -*- coding: utf-8 -*-
"""
اسکریپت ۲۴ — زیرگام ۷.۱: ساختار اولیه Frontend
================================================================
این اسکریپت idempotent است:
  - فایل‌های جدید را می‌سازد
  - فایل‌های موجود (scaffold Vite) را overwrite می‌کند
  - چیزی را پاک نمی‌کند

پیش‌نیاز:
  - 🟧 tab «3 frontend»: vite scaffold + npm install قبلاً انجام شده

فایل‌های ساخته/به‌روزرسانی‌شده (۱۰ فایل):
  ۱) frontend/.env                                  (جدید)
  ۲) frontend/src/main.jsx                          (override)
  ۳) frontend/src/App.jsx                           (override)
  ۴) frontend/src/index.css                         (override — RTL + dark)
  ۵) frontend/src/services/api.js                   (جدید)
  ۶) frontend/src/stores/authStore.js               (جدید)
  ۷) frontend/src/components/common/ProtectedRoute.jsx (جدید)
  ۸) frontend/src/pages/LoginPage.jsx               (جدید — placeholder)
  ۹) frontend/src/pages/HomePage.jsx                (جدید — placeholder)
  ۱۰) frontend/src/pages/ChartPage.jsx              (جدید — placeholder)

اسکریپت Python فقط فایل می‌سازد — هیچ دستور npm اجرا نمی‌کند.

پس از اجرا:
  🟧 tab «3 frontend»:
      npm run dev
  مرورگر: http://localhost:5173/
================================================================
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
SRC_DIR = FRONTEND_DIR / "src"


# ============================================================
# ۱) frontend/.env
# ============================================================
ENV_FILE = """VITE_API_URL=http://localhost:8000/api/v1
"""


# ============================================================
# ۲) frontend/src/main.jsx
# ============================================================
MAIN_JSX = """import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App.jsx";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
"""


# ============================================================
# ۳) frontend/src/App.jsx
# ============================================================
APP_JSX = """import { Routes, Route, Navigate } from "react-router-dom";
import ProtectedRoute from "./components/common/ProtectedRoute.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import HomePage from "./pages/HomePage.jsx";
import ChartPage from "./pages/ChartPage.jsx";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<ProtectedRoute />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/chart/:symbolId" element={<ChartPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
"""


# ============================================================
# ۴) frontend/src/index.css
# ============================================================
INDEX_CSS = """/* ============================================================
   Reset + پایه — فاز ۰ زیرگام ۷.۱
   Design System کامل در زیرگام ۸ پیاده می‌شود.
   ============================================================ */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body, #root {
  min-height: 100vh;
}

body {
  font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
  font-size: 14px;
  line-height: 1.6;
  background: #1e222d;
  color: #d1d4dc;
  direction: rtl;
}

button {
  cursor: pointer;
  font-family: inherit;
  border: none;
  outline: none;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

a {
  color: #2962ff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

input {
  font-family: inherit;
  font-size: inherit;
  outline: none;
}
"""


# ============================================================
# ۵) frontend/src/services/api.js
# ============================================================
API_JS = """/* ============================================================
   axios instance + JWT interceptor
   ============================================================ */
import axios from "axios";
import useAuthStore from "../stores/authStore.js";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1",
  timeout: 10000,
});

// Request interceptor — افزودن خودکار Bearer token
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().accessToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor — handle 401 (در فاز ۱+ refresh خودکار اضافه می‌شود)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      const path = window.location.pathname;
      if (path !== "/login") {
        useAuthStore.getState().logout();
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;
"""


# ============================================================
# ۶) frontend/src/stores/authStore.js
# ============================================================
AUTH_STORE_JS = """/* ============================================================
   Zustand store برای auth — JWT در localStorage persist می‌شود
   ============================================================ */
import { create } from "zustand";
import { persist } from "zustand/middleware";

const useAuthStore = create(
  persist(
    (set) => ({
      accessToken: null,
      refreshToken: null,
      user: null,

      setTokens: (accessToken, refreshToken) =>
        set({ accessToken, refreshToken }),

      setUser: (user) => set({ user }),

      logout: () =>
        set({ accessToken: null, refreshToken: null, user: null }),
    }),
    {
      name: "auth-storage",
    }
  )
);

export default useAuthStore;
"""


# ============================================================
# ۷) frontend/src/components/common/ProtectedRoute.jsx
# ============================================================
PROTECTED_ROUTE_JSX = """import { Navigate, Outlet, useLocation } from "react-router-dom";
import useAuthStore from "../../stores/authStore.js";

export default function ProtectedRoute() {
  const accessToken = useAuthStore((state) => state.accessToken);
  const location = useLocation();

  if (!accessToken) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  return <Outlet />;
}
"""


# ============================================================
# ۸) frontend/src/pages/LoginPage.jsx — placeholder
# ============================================================
LOGIN_PAGE_JSX = """/* صفحه ورود — نسخه placeholder
   پیاده‌سازی کامل در زیرگام ۷.۲ */
export default function LoginPage() {
  return (
    <div style={{ padding: 24, maxWidth: 400, margin: "60px auto" }}>
      <h1 style={{ fontSize: 22, marginBottom: 16 }}>صفحه ورود</h1>
      <p style={{ color: "#787b86" }}>
        پیاده‌سازی کامل در زیرگام ۷.۲
      </p>
    </div>
  );
}
"""


# ============================================================
# ۹) frontend/src/pages/HomePage.jsx — placeholder
# ============================================================
HOME_PAGE_JSX = """import { Link } from "react-router-dom";
import useAuthStore from "../stores/authStore.js";

export default function HomePage() {
  const logout = useAuthStore((state) => state.logout);

  return (
    <div style={{ padding: 24, maxWidth: 800, margin: "0 auto" }}>
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 32,
        }}
      >
        <h1 style={{ fontSize: 22 }}>سامانه هوشمند ترید</h1>
        <button
          onClick={logout}
          style={{
            background: "#2a2e39",
            color: "#d1d4dc",
            padding: "8px 16px",
            borderRadius: 4,
          }}
        >
          خروج
        </button>
      </header>

      <section>
        <h2 style={{ fontSize: 16, marginBottom: 12, color: "#787b86" }}>
          نمودارها
        </h2>
        <ul style={{ listStyle: "none" }}>
          <li style={{ padding: 12, background: "#2a2e39", borderRadius: 4 }}>
            <Link to="/chart/1">📊 BTC/USDT — روزانه</Link>
          </li>
        </ul>
      </section>
    </div>
  );
}
"""


# ============================================================
# ۱۰) frontend/src/pages/ChartPage.jsx — placeholder
# ============================================================
CHART_PAGE_JSX = """import { Link, useParams } from "react-router-dom";

export default function ChartPage() {
  const { symbolId } = useParams();

  return (
    <div style={{ padding: 24 }}>
      <div style={{ marginBottom: 16 }}>
        <Link to="/">← بازگشت به صفحه اصلی</Link>
      </div>
      <h1 style={{ fontSize: 22, marginBottom: 16 }}>
        نمودار (symbol_id = {symbolId})
      </h1>
      <p style={{ color: "#787b86" }}>
        نمودار کندل با lightweight-charts در زیرگام ۷.۳ ساخته می‌شود.
      </p>
    </div>
  );
}
"""


# ============================================================
# نقشه فایل‌ها → محتوا
# ============================================================
FILES_TO_WRITE: dict[Path, str] = {
    FRONTEND_DIR / ".env": ENV_FILE,
    SRC_DIR / "main.jsx": MAIN_JSX,
    SRC_DIR / "App.jsx": APP_JSX,
    SRC_DIR / "index.css": INDEX_CSS,
    SRC_DIR / "services" / "api.js": API_JS,
    SRC_DIR / "stores" / "authStore.js": AUTH_STORE_JS,
    SRC_DIR / "components" / "common" / "ProtectedRoute.jsx": PROTECTED_ROUTE_JSX,
    SRC_DIR / "pages" / "LoginPage.jsx": LOGIN_PAGE_JSX,
    SRC_DIR / "pages" / "HomePage.jsx": HOME_PAGE_JSX,
    SRC_DIR / "pages" / "ChartPage.jsx": CHART_PAGE_JSX,
}


def main() -> None:
    print("=" * 64)
    print("اسکریپت ۲۴ — زیرگام ۷.۱: ساختار اولیه Frontend")
    print("=" * 64)
    print(f"Frontend dir: {FRONTEND_DIR}")
    print()

    if not FRONTEND_DIR.exists():
        print(f"[ERROR] پوشه frontend پیدا نشد: {FRONTEND_DIR}")
        raise SystemExit(1)
    if not (FRONTEND_DIR / "package.json").exists():
        print("[ERROR] package.json پیدا نشد — آیا scaffold Vite انجام شده؟")
        raise SystemExit(1)

    for path, content in FILES_TO_WRITE.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        rel = path.relative_to(PROJECT_ROOT)
        print(f"  ✓ {rel}")

    print()
    print("=" * 64)
    print(f"✅ {len(FILES_TO_WRITE)} فایل نوشته/به‌روز شد.")
    print("=" * 64)
    print()
    print("مرحله بعد:")
    print()
    print("  🟧 tab «3 frontend»:")
    print("      npm run dev")
    print()
    print("  مرورگر:  http://localhost:5173/")
    print()
    print("  انتظار: redirect به /login → صفحه placeholder «صفحه ورود»")


if __name__ == "__main__":
    main()
