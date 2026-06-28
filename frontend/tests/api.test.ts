import { describe, it, expect, vi } from 'vitest';
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
