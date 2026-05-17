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
    expect(r).toMatch(/01\/15\/2024/);
  });

  it('eu-short contains DD/MM/YYYY pattern', () => {
    const r = formatDate(SAMPLE, 'gregorian', { format: 'eu-short' });
    expect(r).toMatch(/15\/01\/2024/);
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
