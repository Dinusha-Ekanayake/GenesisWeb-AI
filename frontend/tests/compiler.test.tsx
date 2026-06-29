import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { CompilerWorkspace } from "../src/components/compiler/CompilerWorkspace";
import { RunRouteScaffold } from "../src/components/routes/RunRouteScaffold";
import { GenesisAPI } from "../src/app/dashboard/lib/genesis-api";
import { useProject } from "../src/app/dashboard/lib/hooks";
import type { ProjectData } from "../src/app/dashboard/types/genesis";

// ── Module mocks ──────────────────────────────────────────────────────────────

// Monaco cannot load in jsdom; mock SpecEditor to expose the same callback API.
vi.mock("../src/app/dashboard/components/SpecEditor", () => ({
  default: ({
    onRun,
    onValidate,
    loading,
  }: {
    onRun: (s: any) => Promise<void>;
    onValidate?: (s: any) => Promise<void>;
    loading: boolean;
  }) => (
    <div data-testid="spec-editor">
      <button
        onClick={() =>
          onRun({
            project_id: "test-project-id",
            name: "Test Spec",
            description: "",
            pages: [],
            components: [],
          })
        }
        disabled={loading}
      >
        Run Compiler
      </button>
      {onValidate && (
        <button
          onClick={() =>
            onValidate({
              project_id: "test-project-id",
              name: "Test Spec",
              description: "",
              pages: [],
              components: [],
            })
          }
        >
          Validate
        </button>
      )}
    </div>
  ),
}));

// ExecutionStatusPanel uses React Query hooks internally; mock it to a stable stub.
vi.mock("../src/app/dashboard/components/ExecutionStatusPanel", () => ({
  default: ({ projectId }: { projectId: string | null }) => (
    <div data-testid="execution-status-panel">
      {projectId === null ? "Awaiting Execution" : `Watching ${projectId}`}
    </div>
  ),
}));

vi.mock("../src/app/dashboard/lib/genesis-api", () => ({
  GenesisAPI: {
    runCompiler: vi.fn(),
    validateSpec: vi.fn(),
  },
}));

vi.mock("../src/app/dashboard/lib/hooks", () => ({
  useSSE: vi.fn(),
  useProject: vi.fn(),
  useProjectStatus: vi.fn(() => ({ data: null })),
  useProjectTelemetry: vi.fn(() => ({ data: [] })),
}));

vi.mock("sonner", () => ({
  toast: { success: vi.fn(), error: vi.fn() },
}));

vi.mock("next/navigation", () => ({
  usePathname: () => "/compiler",
}));

// ── Test fixtures ─────────────────────────────────────────────────────────────

const MANIFEST = {
  project_id: "real-backend-project-abc",
  graph_hashes: {},
  rule_engine_score: 100,
  plugin_versions: {},
  build_status: "COMPLETED",
  deployment_hash: "dep-hash-xyz",
  workspace_hash: "ws-hash-xyz",
};

const PROJECT_WITH_TRACE: ProjectData = {
  id: "project-1",
  title: "Test Project",
  status: "SUCCESS",
  created_at: "2026-06-29T10:00:00Z",
  spec: {
    project_id: "project-1",
    name: "Test Project",
    description: "",
    pages: [],
    components: [],
  },
  execution_trace: [
    { timestamp: "2026-06-29T10:00:01Z", event: "CompilationStarted", details: {} },
    { timestamp: "2026-06-29T10:00:05Z", event: "CompilationComplete", details: { status: "ok" } },
  ],
};

const PROJECT_WITHOUT_TRACE: ProjectData = {
  id: "project-1",
  title: "Test Project",
  status: "SUCCESS",
  created_at: "2026-06-29T10:00:00Z",
};

// ── CompilerWorkspace tests ───────────────────────────────────────────────────

describe("CompilerWorkspace", () => {
  beforeEach(() => {
    vi.mocked(GenesisAPI.runCompiler).mockReset();
    vi.mocked(GenesisAPI.validateSpec).mockReset();
  });

  it("renders spec editor and awaiting execution state when idle", () => {
    render(<CompilerWorkspace />);

    expect(screen.getByRole("heading", { name: "Compiler Workspace" })).toBeInTheDocument();
    expect(screen.getByTestId("spec-editor")).toBeInTheDocument();
    expect(screen.getByText("Awaiting Execution")).toBeInTheDocument();
    expect(screen.queryByRole("link", { name: /View latest known Run/i })).not.toBeInTheDocument();
  });

  it("calls GenesisAPI.runCompiler with the spec from the editor when compile is triggered", async () => {
    vi.mocked(GenesisAPI.runCompiler).mockResolvedValue({ status: "SUCCESS", manifest: MANIFEST });

    render(<CompilerWorkspace />);
    fireEvent.click(screen.getByRole("button", { name: "Run Compiler" }));

    await waitFor(() => {
      expect(vi.mocked(GenesisAPI.runCompiler)).toHaveBeenCalledOnce();
      expect(vi.mocked(GenesisAPI.runCompiler)).toHaveBeenCalledWith(
        expect.objectContaining({ project_id: "test-project-id" })
      );
    });
  });

  it("shows completion CTA with a link using the real backend project ID from the manifest", async () => {
    vi.mocked(GenesisAPI.runCompiler).mockResolvedValue({ status: "SUCCESS", manifest: MANIFEST });

    render(<CompilerWorkspace />);
    fireEvent.click(screen.getByRole("button", { name: "Run Compiler" }));

    await waitFor(() => {
      const link = screen.getByRole("link", { name: /View latest known Run/i });
      expect(link).toHaveAttribute(
        "href",
        `/projects/${MANIFEST.project_id}/runs/${MANIFEST.project_id}`
      );
    });
  });

  it("does not show a Run navigation link when compilation has not completed", () => {
    // runCompiler never resolves — the CTA must not appear
    vi.mocked(GenesisAPI.runCompiler).mockReturnValue(new Promise(() => {}));

    render(<CompilerWorkspace />);
    fireEvent.click(screen.getByRole("button", { name: "Run Compiler" }));

    expect(screen.queryByRole("link", { name: /View latest known Run/i })).not.toBeInTheDocument();
  });

  it("does not invent a Run route when manifest has no project_id", async () => {
    vi.mocked(GenesisAPI.runCompiler).mockResolvedValue({
      status: "SUCCESS",
      manifest: { ...MANIFEST, project_id: "" },
    });

    render(<CompilerWorkspace />);
    fireEvent.click(screen.getByRole("button", { name: "Run Compiler" }));

    // Wait for the async call to finish, then assert no CTA is present
    await waitFor(() => {
      expect(vi.mocked(GenesisAPI.runCompiler)).toHaveBeenCalled();
    });
    expect(screen.queryByRole("link", { name: /View latest known Run/i })).not.toBeInTheDocument();
  });
});

// ── Run-specific compiler surface tests ───────────────────────────────────────

describe("run-specific compiler surface (RunRouteScaffold surface=compiler)", () => {
  beforeEach(() => {
    vi.mocked(useProject).mockReset();
  });

  it("shows read-only trace when project has a compilation trace, without a live compile button", () => {
    vi.mocked(useProject).mockReturnValue({
      data: PROJECT_WITH_TRACE,
      isLoading: false,
      error: null,
    } as any);

    render(<RunRouteScaffold projectId="project-1" runId="project-1" surface="compiler" />);

    expect(screen.queryByRole("button", { name: /Run Compiler/i })).not.toBeInTheDocument();
    expect(screen.getByText(/Read-only compilation trace/i)).toBeInTheDocument();
  });

  it("displays the backend project ID in the trace header, not a frontend-invented ID", () => {
    vi.mocked(useProject).mockReturnValue({
      data: PROJECT_WITH_TRACE,
      isLoading: false,
      error: null,
    } as any);

    render(<RunRouteScaffold projectId="project-1" runId="project-1" surface="compiler" />);

    // backendProjectId must appear in the trace header
    expect(screen.getByText(/project-1/)).toBeInTheDocument();
    // Trace events from the stored execution_trace are shown
    expect(screen.getByText(/Compilation Started/i)).toBeInTheDocument();
  });

  it("links to /compiler for new compilations instead of embedding a live workflow", () => {
    vi.mocked(useProject).mockReturnValue({
      data: PROJECT_WITH_TRACE,
      isLoading: false,
      error: null,
    } as any);

    render(<RunRouteScaffold projectId="project-1" runId="project-1" surface="compiler" />);

    expect(screen.getByRole("link", { name: "New compilation" })).toHaveAttribute(
      "href",
      "/compiler"
    );
  });

  it("shows limited state with link to /compiler when project has no trace", () => {
    vi.mocked(useProject).mockReturnValue({
      data: PROJECT_WITHOUT_TRACE,
      isLoading: false,
      error: null,
    } as any);

    render(<RunRouteScaffold projectId="project-1" runId="project-1" surface="compiler" />);

    expect(screen.getByText(/No compilation trace available/i)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Open Compiler" })).toHaveAttribute(
      "href",
      "/compiler"
    );
  });
});
