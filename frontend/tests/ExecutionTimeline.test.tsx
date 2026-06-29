import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import ExecutionTimeline from '../src/app/dashboard/components/ExecutionTimeline';

describe('ExecutionTimeline', () => {
  it('renders correctly with no traces', () => {
    render(<ExecutionTimeline traces={[]} />);
    expect(screen.getByText(/No execution trace available/i)).toBeInTheDocument();
  });
});
