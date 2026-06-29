import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import WorkspaceExplorer from '../src/app/dashboard/components/WorkspaceExplorer';

vi.mock('../src/app/dashboard/lib/hooks', () => ({
  useProjectWorkspace: () => ({ data: [], isLoading: false, error: null }),
  useProjectFile: () => ({ data: null, isLoading: false, error: null })
}));

describe('WorkspaceExplorer', () => {
  it('renders correctly', () => {
    render(<WorkspaceExplorer projectId="test" />);
    expect(screen.getByText(/Select a file to preview/i)).toBeInTheDocument();
  });
});
