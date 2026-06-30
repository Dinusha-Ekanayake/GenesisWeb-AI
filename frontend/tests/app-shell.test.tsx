import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi, beforeEach } from "vitest";
import { AppShell } from "../src/components/layout/AppShell";

let pathname = "/projects";

vi.mock("next/navigation", () => ({
  usePathname: () => pathname,
  useRouter: () => ({ push: vi.fn() }),
}));

describe("AppShell", () => {
  beforeEach(() => {
    pathname = "/projects";
    window.localStorage.clear();
  });

  it("renders dashboard content inside the shell", () => {
    render(<AppShell><div>Dashboard content</div></AppShell>);

    expect(screen.getByLabelText("Global navigation")).toBeInTheDocument();
    expect(screen.getByLabelText("Context navigation")).toBeInTheDocument();
    expect(screen.getByLabelText("Main work surface")).toHaveTextContent("Dashboard content");
    expect(screen.getAllByRole("link", { name: "Projects" }).some((link) => link.getAttribute("aria-current") === "page")).toBe(true);
  });

  it("marks target route navigation active", () => {
    pathname = "/runs";

    render(<AppShell><div>Runs content</div></AppShell>);

    expect(screen.getAllByRole("link", { name: "Runs" }).some((link) => link.getAttribute("aria-current") === "page")).toBe(true);
  });

  it("persists context and right panel state", async () => {
    render(<AppShell><div>Dashboard content</div></AppShell>);

    expect(screen.getByLabelText("Inspector panel")).toHaveAttribute("aria-hidden", "true");

    fireEvent.click(screen.getByRole("button", { name: /Collapse context panel/i }));
    fireEvent.click(screen.getByRole("button", { name: /Expand right panel/i }));

    await waitFor(() => {
      expect(window.localStorage.getItem("genesis:shell:context-panel-expanded")).toBe("false");
      expect(window.localStorage.getItem("genesis:shell:right-panel-expanded")).toBe("true");
      expect(screen.getByLabelText("Inspector panel")).toHaveAttribute("aria-hidden", "false");
    });
  });
});
