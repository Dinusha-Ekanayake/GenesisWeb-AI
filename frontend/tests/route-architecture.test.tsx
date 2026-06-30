import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import ProjectsPage from "../src/app/(app)/projects/page";
import RunsPage from "../src/app/(app)/runs/page";
import CompilerPage from "../src/app/(app)/compiler/page";
import SearchPage from "../src/app/(app)/search/page";
import type { ProjectData } from "../src/app/dashboard/types/genesis";

const useProjectsMock = vi.fn();

vi.mock("../src/app/dashboard/lib/hooks", () => ({
  useProjects: () => useProjectsMock(),
}));

// CompilerWorkspace has its own test suite in compiler.test.tsx.
// Mock it here so route-architecture tests stay focused on route existence.
vi.mock("../src/components/compiler/CompilerWorkspace", () => ({
  CompilerWorkspace: () => <div data-testid="compiler-workspace">Compiler Workspace</div>,
}));

const project: ProjectData = {
  id: "project-1",
  title: "Backend Project",
  status: "SUCCESS",
  created_at: "2026-06-29T10:00:00Z",
  spec: {
    project_id: "project-1",
    name: "Spec Project",
    description: "Mapped through the adapter",
    pages: [],
    components: [],
  },
};

describe("target route architecture", () => {
  beforeEach(() => {
    useProjectsMock.mockReset();
  });

  it("renders the projects route with adapter-backed project links", () => {
    useProjectsMock.mockReturnValue({ data: [project], isLoading: false, error: null });

    render(<ProjectsPage />);

    expect(screen.getByRole("heading", { name: "Projects" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Spec Project/i })).toHaveAttribute("href", "/projects/project-1");
  });

  it("renders the runs route as latest known runs without fake history", () => {
    useProjectsMock.mockReturnValue({ data: [project], isLoading: false, error: null });

    render(<RunsPage />);

    expect(screen.getByRole("heading", { name: "Runs" })).toBeInTheDocument();
    expect(screen.getByText("backend-project-as-latest-run")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Spec Project/i })).toHaveAttribute("href", "/projects/project-1/runs/project-1");
  });

  it("renders the compiler page with the compiler workspace (not a limited state)", () => {
    render(<CompilerPage />);

    expect(screen.getByTestId("compiler-workspace")).toBeInTheDocument();
    expect(screen.queryByText(/No new compiler UI/i)).not.toBeInTheDocument();
  });

  it("renders the search page with a Search heading and a search input", () => {
    useProjectsMock.mockReturnValue({ data: [], isLoading: false, error: null });

    render(<SearchPage />);

    expect(screen.getByRole("heading", { name: "Search" })).toBeInTheDocument();
    expect(screen.getByLabelText("Search")).toBeInTheDocument();
  });
});
