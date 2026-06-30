import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi, beforeEach } from "vitest";
import { AuthGuard } from "../src/components/auth/AuthGuard";

const mockReplace = vi.fn();

vi.mock("next/navigation", () => ({
  useRouter: () => ({ replace: mockReplace }),
}));

describe("AuthGuard", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    window.localStorage.clear();
  });

  it("renders children when genesis_token is present", async () => {
    window.localStorage.setItem("genesis_token", "tok-valid");
    render(<AuthGuard><div>Protected Content</div></AuthGuard>);
    expect(await screen.findByText("Protected Content")).toBeInTheDocument();
  });

  it("calls router.replace('/login') when genesis_token is absent", async () => {
    render(<AuthGuard><div>Protected Content</div></AuthGuard>);
    await waitFor(() => {
      expect(mockReplace).toHaveBeenCalledWith("/login");
    });
  });

  it("does not render protected children when genesis_token is absent", async () => {
    render(<AuthGuard><div>Protected Content</div></AuthGuard>);
    await waitFor(() => expect(mockReplace).toHaveBeenCalled());
    expect(screen.queryByText("Protected Content")).not.toBeInTheDocument();
  });
});
