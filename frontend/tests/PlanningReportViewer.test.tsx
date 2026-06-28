import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import PlanningReportViewer from '../src/app/dashboard/components/PlanningReportViewer';

describe('PlanningReportViewer', () => {
  it('renders correctly with no data', () => {
    render(<PlanningReportViewer report={null} />);
    expect(screen.getByText(/No planning report available/i)).toBeInTheDocument();
  });
});
