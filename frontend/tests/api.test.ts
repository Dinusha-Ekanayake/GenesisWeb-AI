import { describe, it, expect, vi } from 'vitest';
import { GenesisAPI } from '../src/app/dashboard/lib/api';

describe('GenesisAPI', () => {
  it('login makes a POST request to /auth/token', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ access_token: 'fake-token' })
    });

    const token = await GenesisAPI.login('admin', 'admin');
    expect(token).toBe('fake-token');
    expect(fetch).toHaveBeenCalledWith(expect.stringContaining('/auth/token'), expect.any(Object));
  });
});
