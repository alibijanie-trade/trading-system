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
