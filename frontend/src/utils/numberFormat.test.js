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
