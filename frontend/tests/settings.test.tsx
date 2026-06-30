import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { SettingsPage } from "../src/components/settings/SettingsPage";

// ── Module mocks ──────────────────────────────────────────────────────────────

const mockToggleContextPanel = vi.fn();
const mockToggleRightPanel = vi.fn();
const mockSetContextPanelExpanded = vi.fn();
const mockSetRightPanelExpanded = vi.fn();

vi.mock("../src/components/layout/ShellProvider", () => ({
  useShell: () => ({
    contextPanelExpanded: true,
    rightPanelExpanded: false,
    toggleContextPanel: mockToggleContextPanel,
    toggleRightPanel: mockToggleRightPanel,
    setContextPanelExpanded: mockSetContextPanelExpanded,
    setRightPanelExpanded: mockSetRightPanelExpanded,
  }),
}));

const mockSetTheme = vi.fn();
vi.mock("next-themes", () => ({
  useTheme: () => ({
    theme: "dark",
    setTheme: mockSetTheme,
    resolvedTheme: "dark",
  }),
}));

// ── SettingsPage tests ────────────────────────────────────────────────────────

describe("SettingsPage", () => {
  beforeEach(() => {
    mockToggleContextPanel.mockReset();
    mockToggleRightPanel.mockReset();
    mockSetContextPanelExpanded.mockReset();
    mockSetRightPanelExpanded.mockReset();
    mockSetTheme.mockReset();
  });

  // Structure
  it("renders Settings heading", () => {
    render(<SettingsPage />);
    expect(screen.getByRole("heading", { name: "Settings" })).toBeInTheDocument();
  });

  it("shows local browser-only note", () => {
    render(<SettingsPage />);
    expect(screen.getByText(/stored locally in this browser/i)).toBeInTheDocument();
  });

  it("shows not synced to backend note", () => {
    render(<SettingsPage />);
    expect(screen.getByText(/not synced to any backend/i)).toBeInTheDocument();
  });

  // Appearance section
  it("shows Appearance section with theme options", () => {
    render(<SettingsPage />);
    expect(screen.getByRole("heading", { name: "Appearance" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "System" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Light" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Dark" })).toBeInTheDocument();
  });

  it("active theme button has aria-pressed true (dark is mocked active)", () => {
    render(<SettingsPage />);
    expect(screen.getByRole("button", { name: "Dark" })).toHaveAttribute("aria-pressed", "true");
    expect(screen.getByRole("button", { name: "Light" })).toHaveAttribute("aria-pressed", "false");
    expect(screen.getByRole("button", { name: "System" })).toHaveAttribute("aria-pressed", "false");
  });

  it("clicking Light theme calls setTheme with 'light'", () => {
    render(<SettingsPage />);
    fireEvent.click(screen.getByRole("button", { name: "Light" }));
    expect(mockSetTheme).toHaveBeenCalledWith("light");
  });

  it("clicking Dark theme calls setTheme with 'dark'", () => {
    render(<SettingsPage />);
    fireEvent.click(screen.getByRole("button", { name: "Dark" }));
    expect(mockSetTheme).toHaveBeenCalledWith("dark");
  });

  it("clicking System theme calls setTheme with 'system'", () => {
    render(<SettingsPage />);
    fireEvent.click(screen.getByRole("button", { name: "System" }));
    expect(mockSetTheme).toHaveBeenCalledWith("system");
  });

  // Shell preferences section
  it("shows Shell Preferences section", () => {
    render(<SettingsPage />);
    expect(screen.getByRole("heading", { name: "Shell Preferences" })).toBeInTheDocument();
  });

  it("shows Context Panel toggle reflecting expanded state from shell", () => {
    render(<SettingsPage />);
    const btn = screen.getByRole("button", { name: "Toggle Context Panel" });
    expect(btn).toBeInTheDocument();
    expect(btn).toHaveAttribute("aria-pressed", "true"); // contextPanelExpanded: true
  });

  it("shows Right Panel toggle reflecting collapsed state from shell", () => {
    render(<SettingsPage />);
    const btn = screen.getByRole("button", { name: "Toggle Right Panel" });
    expect(btn).toBeInTheDocument();
    expect(btn).toHaveAttribute("aria-pressed", "false"); // rightPanelExpanded: false
  });

  it("clicking Context Panel toggle calls toggleContextPanel", () => {
    render(<SettingsPage />);
    fireEvent.click(screen.getByRole("button", { name: "Toggle Context Panel" }));
    expect(mockToggleContextPanel).toHaveBeenCalledTimes(1);
  });

  it("clicking Right Panel toggle calls toggleRightPanel", () => {
    render(<SettingsPage />);
    fireEvent.click(screen.getByRole("button", { name: "Toggle Right Panel" }));
    expect(mockToggleRightPanel).toHaveBeenCalledTimes(1);
  });

  it("clicking Reset to defaults restores default shell state", () => {
    render(<SettingsPage />);
    fireEvent.click(
      screen.getByRole("button", { name: /Reset shell preferences to defaults/i })
    );
    expect(mockSetContextPanelExpanded).toHaveBeenCalledWith(true);
    expect(mockSetRightPanelExpanded).toHaveBeenCalledWith(false);
  });

  // Keyboard shortcuts section
  it("shows Keyboard Shortcuts section", () => {
    render(<SettingsPage />);
    expect(screen.getByRole("heading", { name: "Keyboard Shortcuts" })).toBeInTheDocument();
  });

  it("shows command palette shortcut entry", () => {
    render(<SettingsPage />);
    expect(screen.getByText("Open command palette")).toBeInTheDocument();
  });

  it("shows G D shortcut for Open Dashboard", () => {
    render(<SettingsPage />);
    expect(screen.getByText("G D")).toBeInTheDocument();
    expect(screen.getByText("Open Dashboard")).toBeInTheDocument();
  });

  it("shows Ctrl+\\ shortcut entry for context panel", () => {
    render(<SettingsPage />);
    expect(screen.getByText("Toggle context panel")).toBeInTheDocument();
  });

  it("shows Escape shortcut entry", () => {
    render(<SettingsPage />);
    expect(screen.getByText("Escape")).toBeInTheDocument();
    expect(screen.getByText("Close command palette")).toBeInTheDocument();
  });

  // No fake settings
  it("does not show fake account, billing, or team settings", () => {
    render(<SettingsPage />);
    expect(screen.queryByText(/billing/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/account/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/team/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/profile/i)).not.toBeInTheDocument();
  });
});
