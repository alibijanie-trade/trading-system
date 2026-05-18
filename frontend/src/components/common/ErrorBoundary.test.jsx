import React from 'react';
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
