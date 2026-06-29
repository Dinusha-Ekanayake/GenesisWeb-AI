import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { RunArchitectureGraph } from "../src/components/run/RunArchitectureGraph";
import { RunRouteScaffold } from "../src/components/routes/RunRouteScaffold";
import type { RunViewModel } from "../src/lib/genesis/view-models";

// ── Module mocks ──────────────────────────────────────────────────────────────

const mockUseProject = vi.fn();
vi.mock("../src/app/dashboard/lib/hooks", () => ({
  useProject: (...args: any[]) => mockUseProject(...args),
}));

// ── Test fixtures ─────────────────────────────────────────────────────────────

const ENDPOINT_GRAPH = {
  endpoints: [
    { id: "ep-1", name: "GET /users", metadata: {} },
    { id: "ep-2", name: "POST /users", metadata: {} },
    { id: "ep-3", name: "DELETE /users/:id", metadata: { depends_on: ["ep-1"] } },
  ],
  pages: [{ id: "pg-1", name: "UserList" }],
};

const PAGE_GRAPH = {
  pages: [
    { id: "pg-home", name: "Home" },
    { id: "pg-about", name: "About" },
  ],
  components: [{ id: "comp-nav", name: "Navbar" }],
};

const RUN_WITH_GRAPHS: RunViewModel = {
  id: "project-1",
  backendProjectId: "project-1",
  source: "backend-project-as-latest-run",
  projectId: "project-1",
  projectName: "Test Project",
  status: "SUCCESS",
  capabilities: {
    hasExplicitRunHistory: false,
    hasPlanningReport: false,
    hasArchitectureGraphs: true,
    hasWorkspaceFiles: false,
    hasArtifactManifest: false,
    hasCompilationTrace: false,
  },
  architectureGraphs: {
    endpoint_graph: ENDPOINT_GRAPH,
    page_graph: PAGE_GRAPH,
  },
};

const RUN_WITHOUT_GRAPHS: RunViewModel = {
  id: "project-1",
  backendProjectId: "project-1",
  source: "backend-project-as-latest-run",
  projectId: "project-1",
  projectName: "Test Project",
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

const RUN_WITH_UNKNOWN_GRAPH: RunViewModel = {
  ...RUN_WITH_GRAPHS,
  architectureGraphs: {
    custom_graph: { someKey: "someValue", nested: { a: 1 } },
  },
};

// ── RunArchitectureGraph — pure component tests ───────────────────────────────

describe("RunArchitectureGraph", () => {
  it("shows unavailable state when hasArchitectureGraphs capability is false", () => {
    render(<RunArchitectureGraph run={RUN_WITHOUT_GRAPHS} />);

    expect(screen.getByText(/No architecture graphs available/i)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Open Compiler/i })).toHaveAttribute(
      "href",
      "/compiler"
    );
  });

  it("shows unavailable state when architectureGraphs is undefined", () => {
    const runWithUndefinedGraphs: RunViewModel = {
      ...RUN_WITH_GRAPHS,
      architectureGraphs: undefined,
      capabilities: {
        ...RUN_WITH_GRAPHS.capabilities,
        hasArchitectureGraphs: false,
      },
    };

    render(<RunArchitectureGraph run={runWithUndefinedGraphs} />);

    expect(screen.getByText(/No architecture graphs available/i)).toBeInTheDocument();
  });

  it("renders graph name selector buttons for each graph", () => {
    render(<RunArchitectureGraph run={RUN_WITH_GRAPHS} />);

    // "endpoint_graph" → "endpoint graph", "page_graph" → "page graph"
    expect(screen.getByRole("button", { name: /endpoint graph/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /page graph/i })).toBeInTheDocument();
  });

  it("shows graph count indicator", () => {
    render(<RunArchitectureGraph run={RUN_WITH_GRAPHS} />);

    expect(screen.getByText(/2 graphs available/i)).toBeInTheDocument();
  });

  it("shows collection stats for known arrays in the active graph", () => {
    render(<RunArchitectureGraph run={RUN_WITH_GRAPHS} />);

    // First graph: ENDPOINT_GRAPH has 3 endpoints and 1 page
    expect(screen.getByText("3")).toBeInTheDocument(); // endpoints
    expect(screen.getByText("endpoints")).toBeInTheDocument();
  });

  it("renders the active graph JSON in a pre block", () => {
    render(<RunArchitectureGraph run={RUN_WITH_GRAPHS} />);

    const pre = screen.getByLabelText(/endpoint_graph graph data/i);
    expect(pre).toBeInTheDocument();
    // JSON content includes actual data from the fixture — not invented
    expect(pre.textContent).toContain("GET /users");
    expect(pre.textContent).toContain("ep-1");
  });

  it("does not invent graph nodes or edges beyond what the fixture provides", () => {
    render(<RunArchitectureGraph run={RUN_WITH_GRAPHS} />);

    const pre = screen.getByLabelText(/endpoint_graph graph data/i);
    // Confirm only the fixture's 3 endpoints appear — not any invented ones
    expect(pre.textContent).toContain("DELETE /users/:id");
    expect(pre.textContent).not.toContain("PUT /users");
    expect(pre.textContent).not.toContain("PATCH /users");
  });

  it("switches to a different graph when a selector button is clicked", () => {
    render(<RunArchitectureGraph run={RUN_WITH_GRAPHS} />);

    // Initially endpoint_graph is active
    expect(screen.getByLabelText(/endpoint_graph graph data/i)).toBeInTheDocument();

    // Click the page graph button
    fireEvent.click(screen.getByRole("button", { name: /page graph/i }));

    // Now page_graph should be shown
    expect(screen.getByLabelText(/page_graph graph data/i)).toBeInTheDocument();
  });

  it("handles a graph with an unknown shape gracefully (no stats, still renders JSON)", () => {
    render(<RunArchitectureGraph run={RUN_WITH_UNKNOWN_GRAPH} />);

    // No stats grid because no known collections match
    expect(screen.queryByText("endpoints")).not.toBeInTheDocument();
    expect(screen.queryByText("pages")).not.toBeInTheDocument();

    // But the raw JSON is still rendered
    const pre = screen.getByLabelText(/custom_graph graph data/i);
    expect(pre.textContent).toContain("someValue");
  });

  it("marks the active graph button with aria-pressed=true", () => {
    render(<RunArchitectureGraph run={RUN_WITH_GRAPHS} />);

    const activeBtn = screen.getByRole("button", { name: /endpoint graph/i });
    expect(activeBtn).toHaveAttribute("aria-pressed", "true");

    const inactiveBtn = screen.getByRole("button", { name: /page graph/i });
    expect(inactiveBtn).toHaveAttribute("aria-pressed", "false");
  });

  it("shows a singular 'graph available' label when there is exactly one graph", () => {
    const runWithOneGraph: RunViewModel = {
      ...RUN_WITH_GRAPHS,
      architectureGraphs: { endpoint_graph: ENDPOINT_GRAPH },
    };

    render(<RunArchitectureGraph run={runWithOneGraph} />);

    expect(screen.getByText(/1 graph available/i)).toBeInTheDocument();
    expect(screen.queryByText(/graphs available/i)).not.toBeInTheDocument();
  });
});

// ── RunRouteScaffold — architecture surface integration ───────────────────────

describe("RunRouteScaffold architecture surface", () => {
  beforeEach(() => {
    mockUseProject.mockReset();
  });

  it("renders architecture graph content when project has graph data", () => {
    mockUseProject.mockReturnValue({
      data: {
        id: "project-1",
        title: "Test Project",
        status: "SUCCESS",
        created_at: "2026-06-29T10:00:00Z",
        architecture_graphs: {
          endpoint_graph: ENDPOINT_GRAPH,
        },
      },
      isLoading: false,
      error: null,
    });

    render(
      <RunRouteScaffold projectId="project-1" runId="project-1" surface="architecture" />
    );

    expect(screen.getByRole("button", { name: /endpoint graph/i })).toBeInTheDocument();
    expect(screen.getByText(/1 graph available/i)).toBeInTheDocument();
  });

  it("shows unavailable state when project has no architecture graphs", () => {
    mockUseProject.mockReturnValue({
      data: {
        id: "project-1",
        title: "Test Project",
        status: "UNKNOWN",
        created_at: "2026-06-29T10:00:00Z",
      },
      isLoading: false,
      error: null,
    });

    render(
      <RunRouteScaffold projectId="project-1" runId="project-1" surface="architecture" />
    );

    expect(screen.getByText(/No architecture graphs available/i)).toBeInTheDocument();
    expect(screen.queryByText(/graph available/i)).not.toBeInTheDocument();
  });
});
