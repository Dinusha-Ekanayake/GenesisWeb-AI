import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { RunOverview } from "../src/components/run/RunOverview";
import { RunRouteScaffold } from "../src/components/routes/RunRouteScaffold";
import type { RunViewModel } from "../src/lib/genesis/view-models";
import type { ProjectData } from "../src/app/dashboard/types/genesis";

// ── Module mocks ──────────────────────────────────────────────────────────────

const mockUseProject = vi.fn();
vi.mock("../src/app/dashboard/lib/hooks", () => ({
  useProject: (...args: any[]) => mockUseProject(...args),
}));

// ── Test fixtures ─────────────────────────────────────────────────────────────

const FULL_RUN: RunViewModel = {
  id: "project-123",
  backendProjectId: "project-123",
  backendWorkspaceId: "workspace-456",
  source: "backend-project-as-latest-run",
  projectId: "project-123",
  projectName: "My Genesis Project",
  status: "SUCCESS",
  createdAt: "2026-06-29T10:00:00Z",
  durationMs: 1234,
  capabilities: {
    hasExplicitRunHistory: false,
    hasPlanningReport: true,
    hasArchitectureGraphs: true,
    hasWorkspaceFiles: false,
    hasArtifactManifest: true,
    hasCompilationTrace: true,
  },
  specification: {
    project_id: "project-123",
    name: "My Genesis Project",
    description: "A complete test specification",
    pages: ["Dashboard", "Settings", "Reports"],
    components: ["Navbar", "DataTable"],
  },
};

const MINIMAL_RUN: RunViewModel = {
  id: "minimal-project",
  backendProjectId: "minimal-project",
  source: "backend-project-as-latest-run",
  projectId: "minimal-project",
  projectName: "minimal-project",
  status: "UNKNOWN",
  capabilities: {
    hasExplicitRunHistory: false,
    hasPlanningReport: false,
    hasArchitectureGraphs: false,
    hasWorkspaceFiles: false,
    hasArtifactManifest: false,
    hasCompilationTrace: false,
  },
};

const PROJECT_DATA: ProjectData = {
  id: "project-123",
  title: "My Genesis Project",
  status: "SUCCESS",
  created_at: "2026-06-29T10:00:00Z",
  spec: {
    project_id: "project-123",
    name: "My Genesis Project",
    description: "Test",
    pages: ["Dashboard"],
    components: ["Navbar"],
  },
};

// ── RunOverview — pure component tests ───────────────────────────────────────

describe("RunOverview", () => {
  it("renders the project name in the summary card heading and the surfaces section", () => {
    render(<RunOverview run={FULL_RUN} />);

    expect(screen.getByRole("heading", { level: 2, name: /Run Surfaces/i })).toBeInTheDocument();
    // The project name appears in the card title (h3) and possibly in the spec section
    expect(screen.getByRole("heading", { level: 3, name: "My Genesis Project" })).toBeInTheDocument();
  });

  it("shows backend-project-as-latest-run source label honestly", () => {
    render(<RunOverview run={FULL_RUN} />);

    expect(screen.getByText(/backend-project-as-latest-run/)).toBeInTheDocument();
    expect(screen.getByText(/Real Run history requires a future backend endpoint/i)).toBeInTheDocument();
  });

  it("shows the backend project ID explicitly in the summary and identity card", () => {
    render(<RunOverview run={FULL_RUN} />);

    // Both summary and identity card reference the backend project ID
    const projectIdElements = screen.getAllByText("project-123");
    expect(projectIdElements.length).toBeGreaterThanOrEqual(1);
  });

  it("shows the backend workspace ID in the identity card", () => {
    render(<RunOverview run={FULL_RUN} />);

    expect(screen.getByText("workspace-456")).toBeInTheDocument();
  });

  it("shows formatted duration when durationMs is present", () => {
    render(<RunOverview run={FULL_RUN} />);

    // 1234ms → 1.2s
    expect(screen.getByText("1.2s")).toBeInTheDocument();
  });

  it("shows Unavailable for duration when durationMs is absent", () => {
    render(<RunOverview run={MINIMAL_RUN} />);

    // There are two Unavailable cells (duration + workspace ID)
    const items = screen.getAllByText("Unavailable");
    expect(items.length).toBeGreaterThanOrEqual(1);
  });

  it("renders specification summary with pages and components count when spec is available", () => {
    render(<RunOverview run={FULL_RUN} />);

    // Spec has 3 pages and 2 components
    expect(screen.getByText("Specification")).toBeInTheDocument();
    expect(screen.getByText("A complete test specification")).toBeInTheDocument();
    expect(screen.getByText("3")).toBeInTheDocument(); // pages
    expect(screen.getByText("2")).toBeInTheDocument(); // components
  });

  it("shows honest unavailable message when specification is absent", () => {
    render(<RunOverview run={MINIMAL_RUN} />);

    expect(
      screen.getByText(/Specification not included in the backend response/i)
    ).toBeInTheDocument();
  });

  it("renders all 5 surface cards", () => {
    render(<RunOverview run={FULL_RUN} />);

    expect(screen.getByText("Compiler")).toBeInTheDocument();
    expect(screen.getByText("Planning Report")).toBeInTheDocument();
    expect(screen.getByText("Architecture")).toBeInTheDocument();
    expect(screen.getByText("Workspace")).toBeInTheDocument();
    expect(screen.getByText("Artifacts")).toBeInTheDocument();
  });

  it("surface card links use backendProjectId and run.id, not invented IDs", () => {
    render(<RunOverview run={FULL_RUN} />);

    const surfaceLabels = ["Compiler", "Planning Report", "Architecture", "Workspace", "Artifacts"];
    for (const label of surfaceLabels) {
      const link = screen.getByRole("link", { name: `Open ${label}` });
      const href = link.getAttribute("href") ?? "";
      expect(href).toMatch(/^\/projects\/project-123\/runs\/project-123\//);
    }
  });

  it("marks surfaces as Available based on capability flags", () => {
    render(<RunOverview run={FULL_RUN} />);

    const availableBadges = screen.getAllByText("Available");
    // hasPlanningReport, hasArchitectureGraphs, hasArtifactManifest, hasCompilationTrace = 4 true
    expect(availableBadges.length).toBe(4);
  });

  it("marks surfaces as Unavailable when capability is false", () => {
    render(<RunOverview run={FULL_RUN} />);

    // hasWorkspaceFiles = false → 1 Unavailable badge
    const unavailableBadges = screen.getAllByText("Unavailable");
    expect(unavailableBadges.length).toBe(1);
  });

  it("marks all surfaces as Unavailable for a minimal run with no capabilities", () => {
    render(<RunOverview run={MINIMAL_RUN} />);

    // 5 surface badges + "Unavailable" for Created, Duration, and Workspace ID fields = 8 total
    const unavailableInstances = screen.getAllByText("Unavailable");
    expect(unavailableInstances.length).toBe(8);
  });

  it("does not present invented run entries or fabricated run IDs", () => {
    render(<RunOverview run={FULL_RUN} />);

    // The source label must be "backend-project-as-latest-run", not a fabricated value
    expect(screen.getByText(/backend-project-as-latest-run/)).toBeInTheDocument();
    // No fabricated run IDs appear
    expect(screen.queryByText("fake-run-id")).not.toBeInTheDocument();
    // No "Run #N" pattern that would imply a fake history list
    expect(screen.queryByText(/run #\d/i)).not.toBeInTheDocument();
  });
});

// ── RunRouteScaffold — runId mismatch guard ───────────────────────────────────

describe("RunRouteScaffold run ID mismatch", () => {
  beforeEach(() => {
    mockUseProject.mockReset();
  });

  it("shows honest limited state when runId does not match the backend project ID", () => {
    mockUseProject.mockReturnValue({
      data: PROJECT_DATA,
      isLoading: false,
      error: null,
    });

    // "some-other-run" does not match project.id "project-123"
    render(
      <RunRouteScaffold
        projectId="project-123"
        runId="some-other-run"
        surface="overview"
      />
    );

    expect(screen.getByText(/Run history is not available yet/i)).toBeInTheDocument();
  });

  it("mismatch redirect link uses real backend project ID, not the mismatched runId", () => {
    mockUseProject.mockReturnValue({
      data: PROJECT_DATA,
      isLoading: false,
      error: null,
    });

    render(
      <RunRouteScaffold
        projectId="project-123"
        runId="some-other-run"
        surface="overview"
      />
    );

    // Link must use the real project.id for both URL segments
    expect(
      screen.getByRole("link", { name: /Open latest known Run/i })
    ).toHaveAttribute("href", "/projects/project-123/runs/project-123");
  });

  it("renders RunOverview (not mismatch state) when runId matches backend project ID", () => {
    mockUseProject.mockReturnValue({
      data: PROJECT_DATA,
      isLoading: false,
      error: null,
    });

    render(
      <RunRouteScaffold
        projectId="project-123"
        runId="project-123"
        surface="overview"
      />
    );

    // Overview renders "Run Surfaces" section heading
    expect(screen.getByRole("heading", { level: 2, name: /Run Surfaces/i })).toBeInTheDocument();
    expect(screen.queryByText(/Run history is not available/i)).not.toBeInTheDocument();
  });
});
