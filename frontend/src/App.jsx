import { Routes, Route, Navigate } from "react-router-dom";
import ProtectedRoute from "./components/common/ProtectedRoute.jsx";
import ToastContainer from "./components/common/ToastContainer.jsx";
import ConfirmDialog from "./components/common/ConfirmDialog.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import HomePage from "./pages/HomePage.jsx";
import ChartPage from "./pages/ChartPage.jsx";
import SettingsPage from "./pages/SettingsPage.jsx";

export default function App() {
  return (
    <>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/chart/:symbolId" element={<ChartPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <ToastContainer />
      <ConfirmDialog />
    </>
  );
}
