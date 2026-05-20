import { useEffect, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { createChart, CrosshairMode } from "lightweight-charts";
import api from "../services/api.js";
import useThemeStore from "../stores/themeStore.js";
import usePreferencesStore from "../stores/preferencesStore.js";
import SkeletonBlock from "../components/common/SkeletonBlock.jsx";
import { formatNumber } from "../utils/numberFormat.js";
import { formatDate } from "../utils/dateFormat.js";

const TIMEFRAMES = [
  { value: "1d", label: "روزانه (1d)" },
  { value: "1h", label: "یک‌ساعته (1h)" },
  { value: "15m", label: "۱۵ دقیقه (15m)" },
];

function isoToUnix(isoStr) {
  const withZ = isoStr.endsWith("Z") ? isoStr : isoStr + "Z";
  return Math.floor(new Date(withZ).getTime() / 1000);
}

function readVar(name, fallback = "") {
  if (typeof window === "undefined") return fallback;
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return v || fallback;
}

export default function ChartPage() {
  const { symbolId } = useParams();
  const chartContainerRef = useRef(null);
  const chartRef = useRef(null);

  const themeId = useThemeStore((s) => s.themeId);
  const calendar = usePreferencesStore((s) => s.calendar);
  const gregorianFormat = usePreferencesStore((s) => s.gregorianFormat);

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

        const candleData = data.candles.map((c) => ({
          time: isoToUnix(c.timestamp),
          open: c.open,
          high: c.high,
          low: c.low,
          close: c.close,
        }));

        const upColor = readVar("--color-success", "#26a69a");
        const downColor = readVar("--color-danger", "#ef5350");
        const bgColor = readVar("--color-card", "#1e222d");
        const textColor = readVar("--color-text", "#d1d4dc");
        const gridColor = readVar("--color-grid", "#2a2e39");
        const borderColor = readVar("--color-border", "#363a45");

        const volumeData = data.candles.map((c) => ({
          time: isoToUnix(c.timestamp),
          value: c.volume,
          color: c.close >= c.open ? `${upColor}80` : `${downColor}80`,
        }));

        if (chartRef.current) {
          chartRef.current.remove();
          chartRef.current = null;
        }

        const chart = createChart(chartContainerRef.current, {
          width: chartContainerRef.current.clientWidth,
          height: 500,
          layout: {
            background: { color: bgColor },
            textColor: textColor,
          },
          grid: {
            vertLines: { color: gridColor },
            horzLines: { color: gridColor },
          },
          crosshair: { mode: CrosshairMode.Normal },
          timeScale: {
            timeVisible: true,
            secondsVisible: false,
            borderColor: borderColor,
          },
          rightPriceScale: { borderColor: borderColor },
          // 🆕 Bug #48 fix — timeFormatter به جای dateFormat (lightweight-charts v4.x API):
          //   dateFormat فقط string قبول می‌کند، timeFormatter تابع است.
          localization: {
            locale: "en-US",
            timeFormatter: (time) => {
              const d = typeof time === "number"
                ? new Date(time * 1000)
                : new Date(time);
              return formatDate(d, calendar, { format: gregorianFormat });
            },
            priceFormatter: (price) =>
              formatNumber(price, { maxDecimals: 2 }),
          },
        });
        chartRef.current = chart;

        const candleSeries = chart.addCandlestickSeries({
          upColor: upColor,
          downColor: downColor,
          borderVisible: false,
          wickUpColor: upColor,
          wickDownColor: downColor,
        });
        candleSeries.setData(candleData);

        const volumeSeries = chart.addHistogramSeries({
          priceFormat: { type: "volume" },
          priceScaleId: "",
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

    const handleResize = () => {
      if (chartRef.current && chartContainerRef.current) {
        chartRef.current.applyOptions({
          width: chartContainerRef.current.clientWidth,
        });
      }
    };
    window.addEventListener("resize", handleResize);

    return () => {
      cancelled = true;
      window.removeEventListener("resize", handleResize);
      if (chartRef.current) {
        chartRef.current.remove();
        chartRef.current = null;
      }
    };
  }, [symbolId, timeframe, themeId, calendar, gregorianFormat]);

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
        <h1 style={{ fontSize: "1.57rem" }}>BTC/USDT</h1>
        <select
          value={timeframe}
          onChange={(e) => setTimeframe(e.target.value)}
          style={{
            background: "var(--color-card)",
            color: "var(--color-text)",
            padding: "8px 12px",
            borderRadius: 4,
            border: "1px solid var(--color-border)",
            fontSize: "1rem",
          }}
        >
          {TIMEFRAMES.map((tf) => (
            <option key={tf.value} value={tf.value}>
              {tf.label}
            </option>
          ))}
        </select>
      </header>

      {loading ? (
        <div style={{ marginBottom: 12 }}>
          <SkeletonBlock variant="text" width={220} height={13} />
        </div>
      ) : meta.count > 0 && !error ? (
        <div
          style={{
            fontSize: "0.93rem",
            color: "var(--color-text-muted)",
            marginBottom: 12,
          }}
        >
          {formatNumber(meta.count)} از {formatNumber(meta.total)} کندل نمایش داده می‌شود
        </div>
      ) : null}

      {error && (
        <div
          style={{
            padding: 12,
            background: "var(--color-danger-bg)",
            color: "var(--color-danger)",
            border: "1px solid var(--color-danger)",
            borderRadius: 4,
            marginBottom: 12,
            fontSize: "1rem",
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
            background: "var(--color-card)",
            borderRadius: 4,
            opacity: loading ? 0 : 1,
            transition: "opacity 0.2s ease",
          }}
        />
        {loading && (
          <div
            style={{
              position: "absolute",
              inset: 0,
              padding: 16,
              display: "flex",
              flexDirection: "column",
              gap: 12,
              background: "var(--color-card)",
              borderRadius: 4,
              border: "1px solid var(--color-border)",
            }}
          >
            <div style={{ display: "flex", gap: 12 }}>
              <SkeletonBlock variant="rect" width={120} height={20} />
              <SkeletonBlock variant="rect" width={80} height={20} />
            </div>
            <SkeletonBlock
              variant="rect"
              width="100%"
              height="100%"
              style={{ flex: 1, minHeight: 380 }}
            />
            <SkeletonBlock variant="rect" width="100%" height={24} />
          </div>
        )}
      </div>
    </div>
  );
}
