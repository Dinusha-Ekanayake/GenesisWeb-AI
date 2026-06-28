import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import LoginPage from '../src/app/login/page';
import React from 'react';

vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: vi.fn() }),
}));

describe('LoginPage', () => {
  it('renders the sign-in form with username and password fields', () => {
    render(<LoginPage />);
    expect(screen.getByText(/Username/i)).toBeInTheDocument();
    expect(screen.getByText(/Password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Sign In/i })).toBeInTheDocument();
  });

  it('renders the Genesis Engine heading', () => {
    render(<LoginPage />);
    expect(screen.getByText('Genesis Engine')).toBeInTheDocument();
  });
});
