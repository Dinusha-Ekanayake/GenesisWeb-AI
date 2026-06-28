import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import WorkspaceExplorer from '../src/app/dashboard/components/WorkspaceExplorer';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

vi.mock('../src/app/dashboard/lib/hooks', () => ({
  useWorkspaceTree: () => ({ data: [], isLoading: false, error: null })
}));

const queryClient = new QueryClient();

describe('WorkspaceExplorer', () => {
  it('renders correctly', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <WorkspaceExplorer projectId="test" onSelectFile={() => {}} />
      </QueryClientProvider>
    );
    expect(screen.getByText(/Workspace/i)).toBeInTheDocument();
  });
});
