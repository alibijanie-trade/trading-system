# -*- coding: utf-8 -*-
"""
اسکریپت ۲۶ — زیرگام ۷.۳: نمودار کندل (پایان فاز ۰)
================================================================
این اسکریپت idempotent است.

فایل به‌روز (۱ فایل):
  frontend/src/pages/ChartPage.jsx  (override — نمودار کامل)

ویژگی‌ها:
  - candlestick chart + volume histogram
  - dropdown انتخاب timeframe
  - responsive (resize)
  - loading + error states
  - StrictMode-safe (cleanup صحیح)

پس از اجرا — Vite hot reload خودکار اعمال می‌کند:
  مرورگر → http://localhost:5173/chart/1
================================================================
"""

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
CHART_PAGE_PATH = PROJECT_ROOT / "frontend" / "src" / "pages" / "ChartPage.jsx"


CHART_PAGE_JSX = """import { useEffect, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { createChart, CrosshairMode } from "lightweight-charts";
import api from "../services/api.js";

const TIMEFRAMES = [
  { value: "1d", label: "روزانه (1d)" },
  { value: "1h", label: "یک‌ساعته (1h)" },
  { value: "15m", label: "۱۵ دقیقه (15m)" },
];

/* تبدیل ISO 8601 (بدون timezone) → Unix seconds UTC */
function isoToUnix(isoStr) {
  // backend timestamp بدون Z می‌فرستد — UTC فرض می‌کنیم
  const withZ = isoStr.endsWith("Z") ? isoStr : isoStr + "Z";
  return Math.floor(new Date(withZ).getTime() / 1000);
}

export default function ChartPage() {
  const { symbolId } = useParams();
  const chartContainerRef = useRef(null);
  const chartRef = useRef(null);

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

        // تبدیل داده‌ها برای lightweight-charts
        const candleData = data.candles.map((c) => ({
          time: isoToUnix(c.timestamp),
          open: c.open,
          high: c.high,
          low: c.low,
          close: c.close,
        }));

        const volumeData = data.candles.map((c) => ({
          time: isoToUnix(c.timestamp),
          value: c.volume,
          color:
            c.close >= c.open
              ? "rgba(38,166,154,0.5)"
              : "rgba(239,83,80,0.5)",
        }));

        // پاک کردن نمودار قبلی (تغییر timeframe یا StrictMode)
        if (chartRef.current) {
          chartRef.current.remove();
          chartRef.current = null;
        }

        // ساخت نمودار جدید
        const chart = createChart(chartContainerRef.current, {
          width: chartContainerRef.current.clientWidth,
          height: 500,
          layout: {
            background: { color: "#1e222d" },
            textColor: "#d1d4dc",
          },
          grid: {
            vertLines: { color: "#2a2e39" },
            horzLines: { color: "#2a2e39" },
          },
          crosshair: { mode: CrosshairMode.Normal },
          timeScale: {
            timeVisible: true,
            secondsVisible: false,
            borderColor: "#363a45",
          },
          rightPriceScale: { borderColor: "#363a45" },
        });
        chartRef.current = chart;

        const candleSeries = chart.addCandlestickSeries({
          upColor: "#26a69a",
          downColor: "#ef5350",
          borderVisible: false,
          wickUpColor: "#26a69a",
          wickDownColor: "#ef5350",
        });
        candleSeries.setData(candleData);

        const volumeSeries = chart.addHistogramSeries({
          priceFormat: { type: "volume" },
          priceScaleId: "", // جدا کردن از price scale اصلی
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

    // Resize handler
    const handleResize = () => {
      if (chartRef.current && chartContainerRef.current) {
        chartRef.current.applyOptions({
          width: chartContainerRef.current.clientWidth,
        });
      }
    };
    window.addEventListener("resize", handleResize);

    // Cleanup
    return () => {
      cancelled = true;
      window.removeEventListener("resize", handleResize);
      if (chartRef.current) {
        chartRef.current.remove();
        chartRef.current = null;
      }
    };
  }, [symbolId, timeframe]);

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
            background: "#2a2e39",
            color: "#d1d4dc",
            padding: "8px 12px",
            borderRadius: 4,
            border: "1px solid #363a45",
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

      {meta.count > 0 && !error && (
        <div
          style={{ fontSize: 13, color: "#787b86", marginBottom: 12 }}
        >
          {meta.count} از {meta.total} کندل نمایش داده می‌شود
        </div>
      )}

      {error && (
        <div
          style={{
            padding: 12,
            background: "#3a1f1f",
            color: "#ff6b6b",
            border: "1px solid #5a2a2a",
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
            background: "#1e222d",
            borderRadius: 4,
          }}
        />
        {loading && (
          <div
            style={{
              position: "absolute",
              inset: 0,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              background: "rgba(30,34,45,0.7)",
              color: "#787b86",
              fontSize: 14,
              zIndex: 10,
            }}
          >
            در حال بارگذاری نمودار...
          </div>
        )}
      </div>
    </div>
  );
}
"""


def main() -> None:
    print("=" * 64)
    print("اسکریپت ۲۶ — زیرگام ۷.۳: نمودار کندل")
    print("=" * 64)

    if not CHART_PAGE_PATH.parent.exists():
        print(f"[ERROR] پوشه pages پیدا نشد: {CHART_PAGE_PATH.parent}")
        raise SystemExit(1)

    CHART_PAGE_PATH.write_text(CHART_PAGE_JSX, encoding="utf-8", newline="\n")
    print(f"  ✓ {CHART_PAGE_PATH.relative_to(PROJECT_ROOT)}")

    print()
    print("=" * 64)
    print("✅ ۱ فایل به‌روز شد.")
    print("=" * 64)
    print()
    print("Vite خودش hot reload می‌کند.")
    print()
    print("تست:")
    print("  ۱) مرورگر: http://localhost:5173/  (لاگین admin/1 اگر نیست)")
    print("  ۲) کلیک «📊 BTC/USDT — روزانه»")
    print("  ۳) نمودار کندل + volume باید نمایش داده شود")
    print("  ۴) dropdown timeframe → 1h یا 15m انتخاب کن")
    print("     → پیام «داده‌ای برای تایم‌فریم 1h موجود نیست» (طبیعی)")
    print("  ۵) برگرد به 1d → نمودار دوباره ظاهر می‌شود")
    print("  ۶) درگ نمودار، اسکرول، crosshair با حرکت ماوس")


if __name__ == "__main__":
    main()
