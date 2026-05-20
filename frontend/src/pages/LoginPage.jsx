import { useState, useEffect } from "react";
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
  fontSize: "1rem",
};

const labelStyle = {
  display: "block",
  marginBottom: 6,
  fontSize: "0.93rem",
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
        <h1 style={{ fontSize: "1.57rem", marginBottom: 24, textAlign: "center", fontWeight: 600 }}>
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
            fontSize: "1.07rem",
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
            fontSize: "0.86rem",
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
