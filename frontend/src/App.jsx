import React from 'react';
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
