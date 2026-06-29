import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { CommandPalette } from "../src/components/commands/CommandPalette";

// ── Module mocks ──────────────────────────────────────────────────────────────

const mockPush = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: mockPush }),
}));

const mockToggleContextPanel = vi.fn();
const mockToggleRightPanel = vi.fn();
vi.mock("../src/components/layout/ShellProvider", () => ({
  useShell: () => ({
    toggleContextPanel: mockToggleContextPanel,
    toggleRightPanel: mockToggleRightPanel,
    contextPanelExpanded: true,
    rightPanelExpanded: false,
  }),
}));

// ── Helpers ───────────────────────────────────────────────────────────────────

function openPalette() {
  fireEvent.keyDown(document, { key: "k", ctrlKey: true });
}

// ── CommandPalette tests ──────────────────────────────────────────────────────

describe("CommandPalette", () => {
  beforeEach(() => {
    mockPush.mockReset();
    mockToggleContextPanel.mockReset();
    mockToggleRightPanel.mockReset();
  });

  // Visibility
  it("is not visible on mount", () => {
    render(<CommandPalette />);
    expect(screen.queryByRole("dialog", { name: "Command palette" })).not.toBeInTheDocument();
  });

  it("opens on Ctrl+K", () => {
    render(<CommandPalette />);
    fireEvent.keyDown(document, { key: "k", ctrlKey: true });
    expect(screen.getByRole("dialog", { name: "Command palette" })).toBeInTheDocument();
  });

  it("opens on Cmd+K", () => {
    render(<CommandPalette />);
    fireEvent.keyDown(document, { key: "k", metaKey: true });
    expect(screen.getByRole("dialog", { name: "Command palette" })).toBeInTheDocument();
  });

  it("closes on Escape", () => {
    render(<CommandPalette />);
    openPalette();
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("closes on backdrop click", () => {
    render(<CommandPalette />);
    openPalette();
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    // Click the outer dialog element (backdrop area)
    fireEvent.click(screen.getByRole("dialog"));
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("toggles closed on second Ctrl+K", () => {
    render(<CommandPalette />);
    openPalette();
    expect(screen.getByRole("dialog")).toBeInTheDocument();
    fireEvent.keyDown(document, { key: "k", ctrlKey: true });
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  // Commands rendered
  it("shows all navigation commands when open", () => {
    render(<CommandPalette />);
    openPalette();
    expect(screen.getByText("Open Dashboard")).toBeInTheDocument();
    expect(screen.getByText("Open Compiler")).toBeInTheDocument();
    expect(screen.getByText("Open Projects")).toBeInTheDocument();
    expect(screen.getByText("Open Runs")).toBeInTheDocument();
    expect(screen.getByText("Open Telemetry")).toBeInTheDocument();
    expect(screen.getByText("Open Team")).toBeInTheDocument();
    expect(screen.getByText("Open Settings")).toBeInTheDocument();
    expect(screen.getByText("Open Search")).toBeInTheDocument();
  });

  it("shows shell commands when open", () => {
    render(<CommandPalette />);
    openPalette();
    expect(screen.getByText("Toggle Context Panel")).toBeInTheDocument();
    expect(screen.getByText("Toggle Right Panel")).toBeInTheDocument();
  });

  it("shows shortcut hints for G-sequence commands", () => {
    render(<CommandPalette />);
    openPalette();
    expect(screen.getByText("G D")).toBeInTheDocument();
    expect(screen.getByText("G C")).toBeInTheDocument();
    expect(screen.getByText("G P")).toBeInTheDocument();
    expect(screen.getByText("G R")).toBeInTheDocument();
  });

  // Filtering
  it("filters commands by search query", () => {
    render(<CommandPalette />);
    openPalette();
    fireEvent.change(screen.getByLabelText("Search commands"), { target: { value: "compiler" } });
    expect(screen.getByText("Open Compiler")).toBeInTheDocument();
    expect(screen.queryByText("Open Dashboard")).not.toBeInTheDocument();
  });

  it("shows no commands found message for unmatched query", () => {
    render(<CommandPalette />);
    openPalette();
    fireEvent.change(screen.getByLabelText("Search commands"), { target: { value: "zzznomatch" } });
    expect(screen.getByText("No commands found.")).toBeInTheDocument();
  });

  // Command execution — navigation
  it("clicking a navigate command calls router.push and closes palette", () => {
    render(<CommandPalette />);
    openPalette();
    fireEvent.click(screen.getByText("Open Compiler").closest("li")!);
    expect(mockPush).toHaveBeenCalledWith("/compiler");
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("clicking Open Dashboard navigates to /dashboard", () => {
    render(<CommandPalette />);
    openPalette();
    fireEvent.click(screen.getByText("Open Dashboard").closest("li")!);
    expect(mockPush).toHaveBeenCalledWith("/dashboard");
  });

  // Command execution — shell
  it("clicking Toggle Context Panel calls toggleContextPanel and closes palette", () => {
    render(<CommandPalette />);
    openPalette();
    fireEvent.click(screen.getByText("Toggle Context Panel").closest("li")!);
    expect(mockToggleContextPanel).toHaveBeenCalledTimes(1);
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("clicking Toggle Right Panel calls toggleRightPanel and closes palette", () => {
    render(<CommandPalette />);
    openPalette();
    fireEvent.click(screen.getByText("Toggle Right Panel").closest("li")!);
    expect(mockToggleRightPanel).toHaveBeenCalledTimes(1);
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  // Direct keyboard shortcuts — shell
  it("Ctrl+\\ calls toggleContextPanel without opening palette", () => {
    render(<CommandPalette />);
    fireEvent.keyDown(document, { key: "\\", ctrlKey: true });
    expect(mockToggleContextPanel).toHaveBeenCalledTimes(1);
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("Ctrl+P calls toggleRightPanel without opening palette", () => {
    render(<CommandPalette />);
    fireEvent.keyDown(document, { key: "p", ctrlKey: true });
    expect(mockToggleRightPanel).toHaveBeenCalledTimes(1);
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  // G-sequence shortcuts
  it("G D sequence navigates to /dashboard", () => {
    render(<CommandPalette />);
    fireEvent.keyDown(document, { key: "g" });
    fireEvent.keyDown(document, { key: "d" });
    expect(mockPush).toHaveBeenCalledWith("/dashboard");
  });

  it("G C sequence navigates to /compiler", () => {
    render(<CommandPalette />);
    fireEvent.keyDown(document, { key: "g" });
    fireEvent.keyDown(document, { key: "c" });
    expect(mockPush).toHaveBeenCalledWith("/compiler");
  });

  it("G P sequence navigates to /projects", () => {
    render(<CommandPalette />);
    fireEvent.keyDown(document, { key: "g" });
    fireEvent.keyDown(document, { key: "p" });
    expect(mockPush).toHaveBeenCalledWith("/projects");
  });

  it("G R sequence navigates to /runs", () => {
    render(<CommandPalette />);
    fireEvent.keyDown(document, { key: "g" });
    fireEvent.keyDown(document, { key: "r" });
    expect(mockPush).toHaveBeenCalledWith("/runs");
  });

  // Input guard — Ctrl+K blocked when non-palette input is focused
  it("does not open when Ctrl+K is pressed while an external input is focused", () => {
    render(
      <>
        <input data-testid="external-input" />
        <CommandPalette />
      </>
    );
    screen.getByTestId("external-input").focus();
    fireEvent.keyDown(document, { key: "k", ctrlKey: true });
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  // No mock data
  it("does not render invented or fake commands", () => {
    render(<CommandPalette />);
    openPalette();
    expect(screen.queryByText(/fake/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/demo/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/mock/i)).not.toBeInTheDocument();
  });
});
