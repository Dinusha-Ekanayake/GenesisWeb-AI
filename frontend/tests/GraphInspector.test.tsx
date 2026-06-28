import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import GraphInspector from '../src/app/dashboard/components/GraphInspector';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

vi.mock('../src/app/dashboard/lib/hooks', () => ({
  useProjectGraphs: () => ({ data: { endpoints: [] }, isLoading: false, error: null })
}));

const queryClient = new QueryClient();

describe('GraphInspector', () => {
  it('renders correctly', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <GraphInspector projectId="test" />
      </QueryClientProvider>
    );
    expect(screen.getByText(/Tree/i)).toBeInTheDocument();
  });
});
