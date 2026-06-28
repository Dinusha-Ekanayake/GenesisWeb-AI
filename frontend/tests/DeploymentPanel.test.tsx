import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import DeploymentPanel from '../src/app/dashboard/components/DeploymentPanel';

describe('DeploymentPanel', () => {
  it('renders correctly with no data', () => {
    render(<DeploymentPanel manifest={null} onDeploy={() => {}} isDeploying={false} />);
    expect(screen.getByText(/No deployment manifest available/i)).toBeInTheDocument();
  });
});
