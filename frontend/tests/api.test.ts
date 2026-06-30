import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { GenesisAPI } from '../src/app/dashboard/lib/genesis-api';

describe('GenesisAPI', () => {
  it('runCompiler makes a POST request to /genesis/generate', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      headers: { get: () => 'application/json' },
      json: () =>
        Promise.resolve({
          success: true,
          data: { status: 'SUCCESS', manifest: {} },
          error: null,
          timestamp: '',
          request_id: '',
        }),
    } as any);

    const result = await GenesisAPI.runCompiler({
      project_id: 'test',
      title: 'Test',
      description: 'A test project',
      architecture: { frontend: 'react', backend: 'fastapi', database: 'postgres' },
      features: [],
      api_schema: { endpoints: [] },
      data_models: {},
    } as any);

    expect(result).toMatchObject({ status: 'SUCCESS' });
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/genesis/generate'),
      expect.any(Object)
    );
  });

  it('getProjects makes a GET request to /genesis/projects', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      headers: { get: () => 'application/json' },
      json: () =>
        Promise.resolve({
          success: true,
          data: [],
          error: null,
          timestamp: '',
          request_id: '',
        }),
    } as any);

    const projects = await GenesisAPI.getProjects();
    expect(Array.isArray(projects)).toBe(true);
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/genesis/projects'),
      expect.any(Object)
    );
  });
});

describe('fetchWrapper 401 handling', () => {
  let mockReplace: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    mockReplace = vi.fn();
    window.localStorage.clear();
    window.localStorage.setItem('genesis_token', 'expired-token');
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    window.localStorage.clear();
  });

  it('removes genesis_token on 401 response', async () => {
    vi.stubGlobal('location', { pathname: '/projects', replace: mockReplace });
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      json: () => Promise.resolve({ detail: 'Not authenticated' }),
    } as any);

    try { await GenesisAPI.getProjects(); } catch {}

    expect(window.localStorage.getItem('genesis_token')).toBeNull();
  });

  it('redirects to /login on 401 when not already on /login', async () => {
    vi.stubGlobal('location', { pathname: '/projects', replace: mockReplace });
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      json: () => Promise.resolve({ detail: 'Not authenticated' }),
    } as any);

    try { await GenesisAPI.getProjects(); } catch {}

    expect(mockReplace).toHaveBeenCalledWith('/login');
  });

  it('does not redirect when 401 occurs while already on /login', async () => {
    vi.stubGlobal('location', { pathname: '/login', replace: mockReplace });
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      json: () => Promise.resolve({ detail: 'Not authenticated' }),
    } as any);

    try { await GenesisAPI.getProjects(); } catch {}

    expect(mockReplace).not.toHaveBeenCalled();
  });

  it('throws auth-expired APIError on 401', async () => {
    vi.stubGlobal('location', { pathname: '/projects', replace: mockReplace });
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      json: () => Promise.resolve({ detail: 'Not authenticated' }),
    } as any);

    await expect(GenesisAPI.getProjects()).rejects.toMatchObject({
      status: 401,
      message: 'Authentication expired. Please sign in again.',
    });
  });

  it('non-401 errors do not remove token or redirect', async () => {
    vi.stubGlobal('location', { pathname: '/projects', replace: mockReplace });
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
      json: () => Promise.resolve({ detail: 'Internal Server Error' }),
    } as any);

    try { await GenesisAPI.getProjects(); } catch {}

    expect(window.localStorage.getItem('genesis_token')).toBe('expired-token');
    expect(mockReplace).not.toHaveBeenCalled();
  });
});
