import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import SpecEditor from '../src/app/dashboard/components/SpecEditor';

vi.mock('@monaco-editor/react', () => ({
  default: () => <div data-testid="monaco-editor" />
}));

describe('SpecEditor', () => {
  it('renders correctly', () => {
    render(<SpecEditor onRun={vi.fn()} loading={false} />);
    expect(screen.getByText(/ProjectSpecification\.json/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Run Compiler/i })).toBeInTheDocument();
  });
});
