import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import DeploymentPanel from '../src/app/dashboard/components/DeploymentPanel';

vi.mock('../src/app/dashboard/lib/hooks', () => ({
  useProjectManifest: () => ({ data: null, isLoading: false, error: null })
}));

describe('DeploymentPanel', () => {
  it('renders correctly with no data', () => {
    render(<DeploymentPanel projectId="test" />);
    expect(screen.getByText(/No Deployment Artifacts/i)).toBeInTheDocument();
  });
});
