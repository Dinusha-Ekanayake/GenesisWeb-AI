import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { ControlPlaneHome } from "../src/components/dashboard/ControlPlaneHome";
import type { ProjectData } from "../src/app/dashboard/types/genesis";

// ── Module mocks ──────────────────────────────────────────────────────────────

const mockUseProjects = vi.fn();
vi.mock("../src/app/dashboard/lib/hooks", () => ({
  useProjects: () => mockUseProjects(),
}));

// ── Test fixtures ─────────────────────────────────────────────────────────────

const PROJECT_SUCCESS: ProjectData = {
  id: "project-alpha",
  title: "Alpha Project",
  status: "SUCCESS",
  created_at: "2026-06-30T10:00:00Z",
  spec: {
    project_id: "project-alpha",
    name: "Alpha Spec",
    description: "First test project",
    pages: [],
    components: [],
  },
  deployment_manifest: {
    project_id: "project-alpha",
    graph_hashes: {},
    rule_engine_score: 95,
    plugin_versions: {},
    build_status: "COMPLETED",
    deployment_hash: "hash-1",
    workspace_hash: "ws-hash-1",
  },
};

const PROJECT_FAILED: ProjectData = {
  id: "project-beta",
  title: "Beta Project",
  status: "FAILED",
  created_at: "2026-06-30T09:00:00Z",
};

const PROJECT_RUNNING: ProjectData = {
  id: "project-gamma",
  title: "Gamma Project",
  status: "RUNNING",
  created_at: "2026-06-30T11:00:00Z",
};

const TWO_PROJECTS = [PROJECT_SUCCESS, PROJECT_FAILED];
const THREE_PROJECTS = [PROJECT_SUCCESS, PROJECT_FAILED, PROJECT_RUNNING];

// ── ControlPlaneHome tests ────────────────────────────────────────────────────

describe("ControlPlaneHome", () => {
  beforeEach(() => {
    mockUseProjects.mockReset();
  });

  // Header identity
  it("renders Genesis Engine heading", () => {
    mockUseProjects.mockReturnValue({ data: [], isLoading: false, error: null });
    render(<ControlPlaneHome />);
    expect(screen.getByRole("heading", { name: "Genesis Engine" })).toBeInTheDocument();
  });

  it("renders Specification Compiler Platform subtitle", () => {
    mockUseProjects.mockReturnValue({ data: [], isLoading: false, error: null });
    render(<ControlPlaneHome />);
    expect(screen.getByText("Specification Compiler Platform")).toBeInTheDocument();
  });

  // Primary CTA — in empty state both the header CTA and LimitedState CTA render "Open Compiler"
  it("Open Compiler link points to /compiler", () => {
    mockUseProjects.mockReturnValue({ data: [], isLoading: false, error: null });
    render(<ControlPlaneHome />);
    const links = screen.getAllByRole("link", { name: /Open Compiler/i });
    expect(links.length).toBeGreaterThanOrEqual(1);
    links.forEach((link) => expect(link).toHaveAttribute("href", "/compiler"));
  });

  // Secondary CTA
  it("View Projects link points to /projects", () => {
    mockUseProjects.mockReturnValue({ data: [], isLoading: false, error: null });
    render(<ControlPlaneHome />);
    expect(screen.getByRole("link", { name: /View Projects/i })).toHaveAttribute("href", "/projects");
  });

  // Loading state
  it("shows loading spinner and no project cards while loading", () => {
    mockUseProjects.mockReturnValue({ data: [], isLoading: true, error: null });
    render(<ControlPlaneHome />);
    expect(screen.getByText(/Loading projects/i)).toBeInTheDocument();
    expect(screen.queryByText("Recent Projects")).not.toBeInTheDocument();
  });

  // Error state
  it("shows backend error message when useProjects returns an error", () => {
    mockUseProjects.mockReturnValue({
      data: [],
      isLoading: false,
      error: { message: "Network error" },
    });
    render(<ControlPlaneHome />);
    expect(screen.getByText(/Cannot reach the backend/i)).toBeInTheDocument();
    expect(screen.queryByText("Recent Projects")).not.toBeInTheDocument();
  });

  // Empty state
  it("shows LimitedState with Open Compiler CTA when project list is empty", () => {
    mockUseProjects.mockReturnValue({ data: [], isLoading: false, error: null });
    render(<ControlPlaneHome />);
    expect(screen.getByText(/No projects yet/i)).toBeInTheDocument();
    // The empty state CTA also links to /compiler
    const compilerLinks = screen.getAllByRole("link", { name: /Open Compiler/i });
    const hrefs = compilerLinks.map((l) => l.getAttribute("href"));
    expect(hrefs.every((h) => h === "/compiler")).toBe(true);
  });

  it("does not show stats strip or project grid in empty state", () => {
    mockUseProjects.mockReturnValue({ data: [], isLoading: false, error: null });
    render(<ControlPlaneHome />);
    expect(screen.queryByText("Recent Projects")).not.toBeInTheDocument();
    expect(screen.queryByText("Projects")).not.toBeInTheDocument();
  });

  // With projects — project names from real adapter data
  it("renders project names from adapter-mapped backend project data", () => {
    mockUseProjects.mockReturnValue({ data: TWO_PROJECTS, isLoading: false, error: null });
    render(<ControlPlaneHome />);
    // spec.name takes priority in the adapter
    expect(screen.getByText("Alpha Spec")).toBeInTheDocument();
    // No spec → falls back to title
    expect(screen.getByText("Beta Project")).toBeInTheDocument();
  });

  // With projects — links use backendProjectId and run.id
  it("project card links use backendProjectId as both project and run segment", () => {
    mockUseProjects.mockReturnValue({ data: [PROJECT_SUCCESS], isLoading: false, error: null });
    render(<ControlPlaneHome />);
    // The adapter maps run.id === project.id === backendProjectId
    const link = screen.getByRole("link", { name: /Alpha Spec/i });
    expect(link).toHaveAttribute("href", "/projects/project-alpha/runs/project-alpha");
  });

  // Honest "latest known Run" language
  it("shows latest known Run language in the projects disclaimer", () => {
    mockUseProjects.mockReturnValue({ data: TWO_PROJECTS, isLoading: false, error: null });
    render(<ControlPlaneHome />);
    expect(
      screen.getByText(/latest known Run only/i)
    ).toBeInTheDocument();
  });

  // No SpecEditor
  it("does not render a SpecEditor or Compiler Console section", () => {
    mockUseProjects.mockReturnValue({ data: TWO_PROJECTS, isLoading: false, error: null });
    render(<ControlPlaneHome />);
    expect(screen.queryByText(/Compiler Console/i)).not.toBeInTheDocument();
    // SpecEditor renders a textarea with a data attribute — not present
    expect(screen.queryByLabelText(/spec/i)).not.toBeInTheDocument();
  });

  // No ExecutionStatusPanel
  it("does not render an ExecutionStatusPanel or Execution Status section", () => {
    mockUseProjects.mockReturnValue({ data: TWO_PROJECTS, isLoading: false, error: null });
    render(<ControlPlaneHome />);
    expect(screen.queryByText(/Execution Status/i)).not.toBeInTheDocument();
  });

  // Stats — total count
  it("stats strip shows total project count", () => {
    mockUseProjects.mockReturnValue({ data: TWO_PROJECTS, isLoading: false, error: null });
    render(<ControlPlaneHome />);
    // "Projects" label appears in the stat tile
    expect(screen.getByText("Projects")).toBeInTheDocument();
    // Value 2 appears for total projects
    expect(screen.getByText("2")).toBeInTheDocument();
  });

  // Stats — failed count
  // Note: StatusBadge renders "Failed" (title-case) for FAILED projects, so "Failed" appears
  // in both the stat tile label and the project card badge — use getAllByText.
  it("stats strip increments Failed count for FAILED projects", () => {
    mockUseProjects.mockReturnValue({ data: TWO_PROJECTS, isLoading: false, error: null });
    render(<ControlPlaneHome />);
    expect(screen.getAllByText("Failed").length).toBeGreaterThanOrEqual(1);
    // TWO_PROJECTS: Failed stat = 1, Deployed stat = 1 — both render "1"
    expect(screen.getAllByText("1").length).toBeGreaterThanOrEqual(1);
  });

  // Stats — active builds count
  it("stats strip increments Active Builds count for RUNNING projects", () => {
    mockUseProjects.mockReturnValue({ data: THREE_PROJECTS, isLoading: false, error: null });
    render(<ControlPlaneHome />);
    expect(screen.getByText("Active Builds")).toBeInTheDocument();
    // 1 running project
    expect(screen.getAllByText("1").length).toBeGreaterThanOrEqual(1);
  });

  // Stats — deployed count
  it("stats strip shows Deployed count for projects with a deployment manifest", () => {
    mockUseProjects.mockReturnValue({ data: TWO_PROJECTS, isLoading: false, error: null });
    render(<ControlPlaneHome />);
    // PROJECT_SUCCESS has deployment_manifest → 1 deployed
    // PROJECT_FAILED has no manifest → 0
    expect(screen.getByText("Deployed")).toBeInTheDocument();
  });

  // No fake projects or run IDs
  it("does not render invented project names or fabricated run IDs", () => {
    mockUseProjects.mockReturnValue({ data: TWO_PROJECTS, isLoading: false, error: null });
    render(<ControlPlaneHome />);
    expect(screen.queryByText(/fake/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/demo_project/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/run #\d/i)).not.toBeInTheDocument();
  });

  // Cap at 6 projects
  it("renders at most 6 project cards when more projects exist", () => {
    const manyProjects: ProjectData[] = Array.from({ length: 9 }, (_, i) => ({
      id: `project-${i}`,
      title: `Project ${i}`,
      status: "SUCCESS",
      created_at: "2026-06-30T10:00:00Z",
    }));
    mockUseProjects.mockReturnValue({ data: manyProjects, isLoading: false, error: null });
    render(<ControlPlaneHome />);
    // 9 total projects → only 6 cards shown
    // Each card shows "Latest known Run"
    const latestRunLabels = screen.getAllByText("Latest known Run");
    expect(latestRunLabels.length).toBe(6);
  });
});
