# -*- coding: utf-8 -*-
"""
اسکریپت ۳۶ — Vitest setup + Smoke tests (T2.02)
================================================================
Task: T2.02 (Tier 2 — Quality Hardening)

این اسکریپت idempotent است — قابل اجرا چندبار بدون شکست.

محتوای کار:
  ۱) به‌روزرسانی frontend/package.json:
     - افزودن devDependencies: vitest, @vitest/coverage-v8, jsdom,
       @testing-library/{react,jest-dom,user-event}
     - افزودن scripts: test, test:watch, test:coverage, test:ui

  ۲) به‌روزرسانی frontend/vite.config.js:
     - افزودن بلوک test با environment: 'jsdom' + setupFiles + globals

  ۳) ساخت frontend/src/test/setup.js:
     - import "@testing-library/jest-dom" برای matcherها

  ۴) ساخت ۵ فایل تست smoke:
     a) utils/numberFormat.test.js   — تست pure function
     b) utils/dateFormat.test.js     — تست Intl + jalali
     c) stores/confirmStore.test.js  — تست Zustand store + Promise
     d) components/common/ErrorBoundary.test.jsx — ⭐ تست catch خطا
     e) pages/LoginPage.test.jsx     — smoke test page render

نکات معماری:
  - vitest و Vite از یک config (vite.config.js field "test")
  - environment "jsdom" برای DOM access در component tests
  - globals: true → describe/it/expect بدون import
  - setup file: import jest-dom matchers (toBeInTheDocument و غیره)
  - بعد از اجرا، کاربر باید این دستور را روی ماشین خود اجرا کند:
        cd frontend && npm install
    تا dependencies جدید نصب شوند.

سپس برای اجرای تست‌ها:
    cd frontend
    npm test                # یک‌بار، quiet
    npm run test:watch      # حالت تعاملی
    npm run test:coverage   # با گزارش coverage

نحوه اجرا (tab «2 scripts»):
    python scripts\\36_vitest_setup.py

سپس برای تست خود اسکریپت:
    python scripts\\36b_test_vitest_setup.py
================================================================
"""

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FRONTEND = PROJECT_ROOT / "frontend"
SRC = FRONTEND / "src"

PACKAGE_JSON = FRONTEND / "package.json"
VITE_CONFIG = FRONTEND / "vite.config.js"
SETUP_JS = SRC / "test" / "setup.js"

TEST_NUMBER_FORMAT = SRC / "utils" / "numberFormat.test.js"
TEST_DATE_FORMAT = SRC / "utils" / "dateFormat.test.js"
TEST_CONFIRM_STORE = SRC / "stores" / "confirmStore.test.js"
TEST_ERROR_BOUNDARY = SRC / "components" / "common" / "ErrorBoundary.test.jsx"
TEST_LOGIN_PAGE = SRC / "pages" / "LoginPage.test.jsx"


# ────────────────────────────────────────────────────────────────
# Dependencies/scripts برای package.json
# ────────────────────────────────────────────────────────────────
NEW_DEV_DEPS = {
    "@testing-library/jest-dom": "^6.6.3",
    "@testing-library/react": "^16.1.0",
    "@testing-library/user-event": "^14.5.2",
    "@vitest/coverage-v8": "^3.0.0",
    "jsdom": "^25.0.1",
    "vitest": "^3.0.0",
}

NEW_SCRIPTS = {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "test:ui": "vitest --ui",
}


# ────────────────────────────────────────────────────────────────
# محتوای vite.config.js
# ────────────────────────────────────────────────────────────────
VITE_CONFIG_CONTENT = """\
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],

  // پیکربندی Vitest — همراه با Vite در یک فایل
  // مرجع: https://vitest.dev/config/
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.js'],
    css: false, // تست‌ها نیازی به پردازش CSS ندارند
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      include: ['src/**/*.{js,jsx}'],
      exclude: [
        'src/**/*.test.{js,jsx}',
        'src/test/**',
        'src/main.jsx',
        'src/assets/**',
      ],
    },
  },
})
"""


# ────────────────────────────────────────────────────────────────
# محتوای setup.js
# ────────────────────────────────────────────────────────────────
SETUP_CONTENT = """\
/**
 * Vitest setup — راه‌اندازی سراسری برای همه تست‌ها
 *
 * این فایل قبل از هر فایل تست load می‌شود.
 * - matcherهای jest-dom (مثل toBeInTheDocument) را اضافه می‌کند
 */
import '@testing-library/jest-dom/vitest';
"""


# ────────────────────────────────────────────────────────────────
# محتوای تست‌ها
# ────────────────────────────────────────────────────────────────
NUMBER_FORMAT_TEST = """\
import { describe, it, expect } from 'vitest';
import { formatNumber, parseFormattedNumber } from './numberFormat.js';

describe('formatNumber', () => {
  it('adds thousand separators (en-US default)', () => {
    expect(formatNumber(1714)).toBe('1,714');
    expect(formatNumber(102345.67)).toBe('102,345.67');
  });

  it('returns empty string for invalid input', () => {
    expect(formatNumber(null)).toBe('');
    expect(formatNumber(undefined)).toBe('');
    expect(formatNumber('')).toBe('');
    expect(formatNumber('abc')).toBe('');
    expect(formatNumber(Infinity)).toBe('');
    expect(formatNumber(NaN)).toBe('');
  });

  it('respects decimals option', () => {
    expect(formatNumber(102345.67, { decimals: 0 })).toBe('102,346');
    expect(formatNumber(1, { decimals: 2 })).toBe('1.00');
  });

  it('handles zero and negative', () => {
    expect(formatNumber(0)).toBe('0');
    expect(formatNumber(-1714)).toBe('-1,714');
  });
});

describe('parseFormattedNumber', () => {
  it('reverses formatNumber for integers', () => {
    expect(parseFormattedNumber('1,714')).toBe(1714);
  });

  it('reverses formatNumber for decimals', () => {
    expect(parseFormattedNumber('102,345.67')).toBe(102345.67);
  });

  it('returns null for invalid input', () => {
    expect(parseFormattedNumber('')).toBe(null);
    expect(parseFormattedNumber(null)).toBe(null);
    expect(parseFormattedNumber('abc')).toBe(null);
  });
});
"""


DATE_FORMAT_TEST = """\
import { describe, it, expect } from 'vitest';
import {
  formatDate,
  GREGORIAN_FORMATS,
  CALENDARS,
  isValidCalendar,
  isValidGregorianFormat,
} from './dateFormat.js';

// تاریخ ثابت برای تست‌ها — جلوگیری از وابستگی به Date.now()
const SAMPLE = '2024-01-15T12:00:00Z';

describe('formatDate — gregorian', () => {
  it('iso format returns YYYY-MM-DD', () => {
    expect(formatDate(SAMPLE, 'gregorian', { format: 'iso' })).toBe('2024-01-15');
  });

  it('us-short contains MM/DD/YYYY pattern', () => {
    const r = formatDate(SAMPLE, 'gregorian', { format: 'us-short' });
    expect(r).toMatch(/01\\/15\\/2024/);
  });

  it('eu-short contains DD/MM/YYYY pattern', () => {
    const r = formatDate(SAMPLE, 'gregorian', { format: 'eu-short' });
    expect(r).toMatch(/15\\/01\\/2024/);
  });

  it("long format includes 'January' and '2024'", () => {
    const r = formatDate(SAMPLE, 'gregorian', { format: 'long' });
    expect(r).toContain('January');
    expect(r).toContain('2024');
  });

  it('empty input returns empty string', () => {
    expect(formatDate('', 'gregorian')).toBe('');
    expect(formatDate(null, 'gregorian')).toBe('');
    expect(formatDate(undefined, 'gregorian')).toBe('');
  });
});

describe('formatDate — jalali', () => {
  it('returns Persian-Iranian year ۱۴۰۲ (یا 1402)', () => {
    const r = formatDate(SAMPLE, 'jalali');
    // بسته به محیط Node ممکن است digit shaping انجام شود یا نه
    expect(r).toMatch(/۱۴۰۲|1402/);
  });
});

describe('validators', () => {
  it('isValidCalendar', () => {
    expect(isValidCalendar('gregorian')).toBe(true);
    expect(isValidCalendar('jalali')).toBe(true);
    expect(isValidCalendar('xyz')).toBe(false);
  });

  it('isValidGregorianFormat', () => {
    expect(isValidGregorianFormat('iso')).toBe(true);
    expect(isValidGregorianFormat('invalid')).toBe(false);
  });
});

describe('constants', () => {
  it('GREGORIAN_FORMATS has all 4 formats', () => {
    expect(GREGORIAN_FORMATS).toEqual(['iso', 'us-short', 'eu-short', 'long']);
  });

  it('CALENDARS keys', () => {
    expect(CALENDARS.GREGORIAN).toBe('gregorian');
    expect(CALENDARS.JALALI).toBe('jalali');
  });
});
"""


CONFIRM_STORE_TEST = """\
import { describe, it, expect, beforeEach } from 'vitest';
import useConfirmStore from './confirmStore.js';

// helper برای reset به state اولیه قبل از هر تست
function resetStore() {
  useConfirmStore.setState({
    isOpen: false,
    title: '',
    message: '',
    variant: 'info',
    confirmText: 'تأیید',
    cancelText: 'انصراف',
    resolver: null,
  });
}

describe('confirmStore', () => {
  beforeEach(() => {
    resetStore();
  });

  it('confirm() opens dialog and returns a Promise', () => {
    const p = useConfirmStore.getState().confirm({ title: 'Test' });
    expect(p).toBeInstanceOf(Promise);

    const s = useConfirmStore.getState();
    expect(s.isOpen).toBe(true);
    expect(s.title).toBe('Test');
  });

  it('confirmAccept resolves Promise with true and closes dialog', async () => {
    const p = useConfirmStore.getState().confirm({ title: 'T' });
    useConfirmStore.getState().confirmAccept();

    await expect(p).resolves.toBe(true);
    expect(useConfirmStore.getState().isOpen).toBe(false);
  });

  it('confirmReject resolves Promise with false and closes dialog', async () => {
    const p = useConfirmStore.getState().confirm({ title: 'T' });
    useConfirmStore.getState().confirmReject();

    await expect(p).resolves.toBe(false);
    expect(useConfirmStore.getState().isOpen).toBe(false);
  });

  it('uses provided variant and texts', () => {
    useConfirmStore.getState().confirm({
      title: 'Delete',
      message: 'Sure?',
      variant: 'danger',
      confirmText: 'Yes',
      cancelText: 'No',
    });
    const s = useConfirmStore.getState();
    expect(s.variant).toBe('danger');
    expect(s.confirmText).toBe('Yes');
    expect(s.cancelText).toBe('No');
  });

  it('opening new dialog rejects previous one with false', async () => {
    const first = useConfirmStore.getState().confirm({ title: 'First' });
    useConfirmStore.getState().confirm({ title: 'Second' });
    await expect(first).resolves.toBe(false);
    expect(useConfirmStore.getState().title).toBe('Second');
  });
});
"""


ERROR_BOUNDARY_TEST = """\
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import ErrorBoundary from './ErrorBoundary.jsx';

// کامپوننت بمب برای trigger کردن render error
function Bomb() {
  throw new Error('kaboom from test');
}

function Safe() {
  return <div>safe content</div>;
}

describe('ErrorBoundary', () => {
  let consoleErrorSpy;

  beforeEach(() => {
    // React خطاهای caught را در console.error می‌نویسد + componentDidCatch ما هم
    // در تست نمی‌خواهیم noise ببینیم
    consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    consoleErrorSpy.mockRestore();
  });

  it('renders children when no error', () => {
    render(
      <ErrorBoundary>
        <Safe />
      </ErrorBoundary>
    );
    expect(screen.getByText('safe content')).toBeInTheDocument();
  });

  it('renders fallback with role="alert" when child throws', () => {
    render(
      <ErrorBoundary>
        <Bomb />
      </ErrorBoundary>
    );
    expect(screen.getByRole('alert')).toBeInTheDocument();
    expect(screen.getByText('خطایی رخ داد')).toBeInTheDocument();
  });

  it('shows reset and reload buttons in fallback UI', () => {
    render(
      <ErrorBoundary>
        <Bomb />
      </ErrorBoundary>
    );
    expect(screen.getByText('تلاش مجدد')).toBeInTheDocument();
    expect(screen.getByText('بارگذاری مجدد')).toBeInTheDocument();
  });

  it('uses custom fallback function if provided', () => {
    const fallback = ({ error }) => (
      <div>Custom: {error.message}</div>
    );
    render(
      <ErrorBoundary fallback={fallback}>
        <Bomb />
      </ErrorBoundary>
    );
    expect(screen.getByText(/Custom: kaboom/)).toBeInTheDocument();
  });

  it('calls onReset prop when reset is triggered via custom fallback', () => {
    const onReset = vi.fn();
    const fallback = ({ reset }) => (
      <button onClick={reset}>TryAgain</button>
    );
    render(
      <ErrorBoundary fallback={fallback} onReset={onReset}>
        <Bomb />
      </ErrorBoundary>
    );
    fireEvent.click(screen.getByText('TryAgain'));
    expect(onReset).toHaveBeenCalledTimes(1);
  });
});
"""


LOGIN_PAGE_TEST = """\
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import LoginPage from './LoginPage.jsx';

describe('LoginPage smoke test', () => {
  it('renders login form heading', () => {
    render(
      <MemoryRouter initialEntries={['/login']}>
        <LoginPage />
      </MemoryRouter>
    );
    expect(screen.getByText('ورود به سامانه')).toBeInTheDocument();
  });

  it('renders username and password fields', () => {
    render(
      <MemoryRouter initialEntries={['/login']}>
        <LoginPage />
      </MemoryRouter>
    );
    expect(screen.getByLabelText('نام کاربری')).toBeInTheDocument();
    expect(screen.getByLabelText('رمز عبور')).toBeInTheDocument();
  });

  it('renders submit button as disabled initially', () => {
    render(
      <MemoryRouter initialEntries={['/login']}>
        <LoginPage />
      </MemoryRouter>
    );
    const btn = screen.getByRole('button', { name: 'ورود' });
    expect(btn).toBeDisabled();
  });
});
"""


# ────────────────────────────────────────────────────────────────
# File helpers
# ────────────────────────────────────────────────────────────────
def write_if_changed(path: Path, content: str) -> str:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        return "created"
    try:
        current = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        current = path.read_text(encoding="cp1252")
    if current == content:
        return "unchanged"
    path.write_text(content, encoding="utf-8", newline="\n")
    return "updated"


def merge_dict_preserve_order(existing: dict, additions: dict) -> tuple[dict, bool]:
    """
    additions را با existing ادغام می‌کند بدون تغییر key های موجود.
    کلیدهای جدید به ترتیب alphabetic در پایان اضافه می‌شوند.

    Returns: (merged_dict, changed: bool)
    """
    merged = dict(existing)
    changed = False
    for k in sorted(additions.keys()):
        if k not in merged or merged[k] != additions[k]:
            merged[k] = additions[k]
            changed = True
    return merged, changed


def update_package_json() -> str:
    """به‌روزرسانی package.json با scripts و devDependencies جدید."""
    pkg = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))

    # backup مقادیر فعلی برای مقایسه
    original = json.dumps(pkg, sort_keys=False)

    # افزودن scripts
    scripts = pkg.get("scripts", {})
    scripts, _ = merge_dict_preserve_order(scripts, NEW_SCRIPTS)
    pkg["scripts"] = scripts

    # افزودن devDependencies
    devdeps = pkg.get("devDependencies", {})
    # برای مرتب‌بودن، کل devDependencies را sort می‌کنیم بعد از merge
    devdeps_merged, _ = merge_dict_preserve_order(devdeps, NEW_DEV_DEPS)
    pkg["devDependencies"] = dict(sorted(devdeps_merged.items()))

    new_content = json.dumps(pkg, indent=2, ensure_ascii=False) + "\n"

    if PACKAGE_JSON.read_text(encoding="utf-8") == new_content:
        return "unchanged"

    PACKAGE_JSON.write_text(new_content, encoding="utf-8", newline="\n")
    # تفکیک: آیا کلید جدید اضافه شد یا فقط آپدیت بود
    return "updated"


# ────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────
def main() -> int:
    print("=" * 64)
    print("اسکریپت ۳۶ — Vitest setup + Smoke tests (T2.02)")
    print("=" * 64)
    print()

    if not PACKAGE_JSON.exists():
        print(f"[ERROR] {PACKAGE_JSON} موجود نیست — frontend راه‌اندازی نشده؟")
        return 1

    # 1) package.json
    print("📝 package.json")
    status = update_package_json()
    icon = {"updated": "✏️", "unchanged": "✓"}[status]
    print(f"   {icon} {status}  → frontend/package.json")
    print()

    # 2) vite.config.js
    print("📝 vite.config.js")
    status = write_if_changed(VITE_CONFIG, VITE_CONFIG_CONTENT)
    icon = {"created": "🆕", "updated": "✏️", "unchanged": "✓"}[status]
    print(f"   {icon} {status}  → frontend/vite.config.js")
    print()

    # 3) setup.js
    print("📝 src/test/setup.js")
    status = write_if_changed(SETUP_JS, SETUP_CONTENT)
    icon = {"created": "🆕", "updated": "✏️", "unchanged": "✓"}[status]
    print(f"   {icon} {status}  → frontend/src/test/setup.js")
    print()

    # 4) فایل‌های تست
    test_files = [
        (TEST_NUMBER_FORMAT, NUMBER_FORMAT_TEST, "utils/numberFormat.test.js"),
        (TEST_DATE_FORMAT, DATE_FORMAT_TEST, "utils/dateFormat.test.js"),
        (TEST_CONFIRM_STORE, CONFIRM_STORE_TEST, "stores/confirmStore.test.js"),
        (TEST_ERROR_BOUNDARY, ERROR_BOUNDARY_TEST, "components/common/ErrorBoundary.test.jsx"),
        (TEST_LOGIN_PAGE, LOGIN_PAGE_TEST, "pages/LoginPage.test.jsx"),
    ]
    print("📝 فایل‌های تست (۵):")
    for path, content, label in test_files:
        status = write_if_changed(path, content)
        icon = {"created": "🆕", "updated": "✏️", "unchanged": "✓"}[status]
        print(f"   {icon} {status}  → frontend/src/{label}")
    print()

    print("-" * 64)
    print("✅ پایان اسکریپت ۳۶.")
    print()
    print("📌 گام بعدی (روی ماشین کاربر، tab «3 frontend»):")
    print("   cd frontend")
    print("   npm install            # نصب dev deps جدید")
    print("   npm test               # اجرای یک‌باره ۵ فایل تست")
    print("   npm run test:watch     # حالت تعاملی (re-run هنگام تغییر)")
    print("   npm run test:coverage  # گزارش پوشش")
    print()
    print("سپس برای validation:")
    print("   python scripts/36b_test_vitest_setup.py")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    sys.exit(main())
