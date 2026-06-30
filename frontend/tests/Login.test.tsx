import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi, beforeEach } from "vitest";
import LoginPage from "../src/app/login/page";

const mockPush = vi.fn();

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: mockPush }),
}));

const mockLoginWithCredentials = vi.fn();
vi.mock("../src/lib/auth/login", () => ({
  loginWithCredentials: (...args: unknown[]) => mockLoginWithCredentials(...args),
}));

const mockSetToken = vi.fn();
vi.mock("../src/app/dashboard/lib/api-client", () => ({
  setToken: (...args: unknown[]) => mockSetToken(...args),
  removeToken: vi.fn(),
  getToken: vi.fn(),
}));

describe("LoginPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders username and password fields", () => {
    render(<LoginPage />);
    expect(screen.getByLabelText("Username")).toBeInTheDocument();
    expect(screen.getByLabelText("Password")).toBeInTheDocument();
  });

  it("renders the Sign In button", () => {
    render(<LoginPage />);
    expect(screen.getByRole("button", { name: "Sign In" })).toBeInTheDocument();
  });

  it("renders the Genesis Engine heading", () => {
    render(<LoginPage />);
    expect(screen.getByText("Genesis Engine")).toBeInTheDocument();
  });

  it("calls loginWithCredentials with typed credentials on submit", async () => {
    mockLoginWithCredentials.mockResolvedValue("tok-abc");
    render(<LoginPage />);
    fireEvent.change(screen.getByLabelText("Username"), { target: { value: "developer" } });
    fireEvent.change(screen.getByLabelText("Password"), { target: { value: "devpassword" } });
    fireEvent.click(screen.getByRole("button", { name: "Sign In" }));
    await waitFor(() => {
      expect(mockLoginWithCredentials).toHaveBeenCalledWith("developer", "devpassword");
    });
  });

  it("stores genesis_token on successful login", async () => {
    mockLoginWithCredentials.mockResolvedValue("tok-abc");
    render(<LoginPage />);
    fireEvent.change(screen.getByLabelText("Username"), { target: { value: "developer" } });
    fireEvent.change(screen.getByLabelText("Password"), { target: { value: "devpassword" } });
    fireEvent.click(screen.getByRole("button", { name: "Sign In" }));
    await waitFor(() => {
      expect(mockSetToken).toHaveBeenCalledWith("tok-abc");
    });
  });

  it("redirects to /dashboard on successful login", async () => {
    mockLoginWithCredentials.mockResolvedValue("tok-abc");
    render(<LoginPage />);
    fireEvent.change(screen.getByLabelText("Username"), { target: { value: "developer" } });
    fireEvent.change(screen.getByLabelText("Password"), { target: { value: "devpassword" } });
    fireEvent.click(screen.getByRole("button", { name: "Sign In" }));
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith("/dashboard");
    });
  });

  it("displays error on invalid credentials", async () => {
    mockLoginWithCredentials.mockRejectedValue(new Error("Incorrect username or password."));
    render(<LoginPage />);
    fireEvent.change(screen.getByLabelText("Username"), { target: { value: "wrong" } });
    fireEvent.change(screen.getByLabelText("Password"), { target: { value: "bad" } });
    fireEvent.click(screen.getByRole("button", { name: "Sign In" }));
    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent("Incorrect username or password.");
    });
  });

  it("displays error on network failure", async () => {
    mockLoginWithCredentials.mockRejectedValue(
      new Error("Unable to reach the server. Check that the backend is running.")
    );
    render(<LoginPage />);
    fireEvent.change(screen.getByLabelText("Username"), { target: { value: "developer" } });
    fireEvent.change(screen.getByLabelText("Password"), { target: { value: "devpassword" } });
    fireEvent.click(screen.getByRole("button", { name: "Sign In" }));
    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent(/Unable to reach the server/i);
    });
  });

  it("disables the submit button while request is in flight", async () => {
    mockLoginWithCredentials.mockImplementation(() => new Promise(() => {}));
    render(<LoginPage />);
    fireEvent.change(screen.getByLabelText("Username"), { target: { value: "developer" } });
    fireEvent.change(screen.getByLabelText("Password"), { target: { value: "devpassword" } });
    fireEvent.click(screen.getByRole("button", { name: "Sign In" }));
    await waitFor(() => {
      expect(screen.getByRole("button")).toBeDisabled();
    });
  });

  it("does not show signup, register, OAuth, or reset-password UI", () => {
    render(<LoginPage />);
    expect(screen.queryByText(/sign up/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/register/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/forgot password/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/reset password/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/google/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/oauth/i)).not.toBeInTheDocument();
  });
});
