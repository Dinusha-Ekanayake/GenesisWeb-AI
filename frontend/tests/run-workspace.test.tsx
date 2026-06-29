import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { RunWorkspace } from "../src/components/run/RunWorkspace";
import { RunRouteScaffold } from "../src/components/routes/RunRouteScaffold";
import type { RunViewModel } from "../src/lib/genesis/view-models";

// ── Module mocks ──────────────────────────────────────────────────────────────

const mockUseProject = vi.fn();
const mockUseProjectWorkspace = vi.fn();
const mockUseProjectFile = vi.fn();

vi.mock("../src/app/dashboard/lib/hooks", () => ({
  useProject: (...args: any[]) => mockUseProject(...args),
  useProjectWorkspace: (...args: any[]) => mockUseProjectWorkspace(...args),
  useProjectFile: (...args: any[]) => mockUseProjectFile(...args),
}));

// ── Test fixtures ─────────────────────────────────────────────────────────────

const WORKSPACE_TREE = [
  {
    name: "src",
    path: "src",
    is_dir: true,
    children: [
      { name: "main.ts", path: "src/main.ts", is_dir: false },
      { name: "utils.ts", path: "src/utils.ts", is_dir: false },
    ],
  },
  { name: "README.md", path: "README.md", is_dir: false },
];

const RUN: RunViewModel = {
  id: "project-1",
  backendProjectId: "project-1",
  source: "backend-project-as-latest-run",
  projectId: "project-1",
  projectName: "Test Project",
  status: "SUCCESS",
  capabilities: {
    hasExplicitRunHistory: false,
    hasPlanningReport: false,
    hasArchitectureGraphs: false,
    hasWorkspaceFiles: false,
    hasArtifactManifest: false,
    hasCompilationTrace: false,
  },
};

// ── RunWorkspace — component tests ────────────────────────────────────────────

describe("RunWorkspace", () => {
  beforeEach(() => {
    mockUseProjectWorkspace.mockReset();
    mockUseProjectFile.mockReset();
    // Default: file hook returns no data (no file selected yet)
    mockUseProjectFile.mockReturnValue({ data: null, isLoading: false, error: null });
  });

  it("shows loading spinner while workspace data is fetching", () => {
    mockUseProjectWorkspace.mockReturnValue({ data: null, isLoading: true, error: null });

    render(<RunWorkspace run={RUN} />);

    expect(screen.getByText(/Loading workspace/i)).toBeInTheDocument();
  });

  it("shows unavailable state when workspace API returns an error", () => {
    mockUseProjectWorkspace.mockReturnValue({
      data: null,
      isLoading: false,
      error: new Error("Network error"),
    });

    render(<RunWorkspace run={RUN} />);

    expect(screen.getByText(/Workspace files unavailable/i)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Open Compiler/i })).toHaveAttribute(
      "href",
      "/compiler"
    );
  });

  it("shows unavailable state when workspace API returns an empty array", () => {
    mockUseProjectWorkspace.mockReturnValue({ data: [], isLoading: false, error: null });

    render(<RunWorkspace run={RUN} />);

    expect(screen.getByText(/Workspace files unavailable/i)).toBeInTheDocument();
  });

  it("renders top-level file and directory names from real API data", () => {
    mockUseProjectWorkspace.mockReturnValue({
      data: WORKSPACE_TREE,
      isLoading: false,
      error: null,
    });

    render(<RunWorkspace run={RUN} />);

    // "src" directory and "README.md" file should be visible
    expect(screen.getByRole("button", { name: /^src$/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /^README\.md$/i })).toBeInTheDocument();
  });

  it("shows the backend project ID in the file tree header", () => {
    mockUseProjectWorkspace.mockReturnValue({
      data: WORKSPACE_TREE,
      isLoading: false,
      error: null,
    });

    render(<RunWorkspace run={RUN} />);

    expect(screen.getByText("project-1")).toBeInTheDocument();
  });

  it("shows the placeholder message before any file is selected", () => {
    mockUseProjectWorkspace.mockReturnValue({
      data: WORKSPACE_TREE,
      isLoading: false,
      error: null,
    });

    render(<RunWorkspace run={RUN} />);

    expect(screen.getByText(/Select a file to preview/i)).toBeInTheDocument();
  });

  it("does not show child files until a directory is expanded", () => {
    mockUseProjectWorkspace.mockReturnValue({
      data: WORKSPACE_TREE,
      isLoading: false,
      error: null,
    });

    render(<RunWorkspace run={RUN} />);

    // "main.ts" and "utils.ts" are inside "src" which is collapsed
    expect(screen.queryByRole("button", { name: /^main\.ts$/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /^utils\.ts$/i })).not.toBeInTheDocument();
  });

  it("expands a directory and reveals children when clicked", () => {
    mockUseProjectWorkspace.mockReturnValue({
      data: WORKSPACE_TREE,
      isLoading: false,
      error: null,
    });

    render(<RunWorkspace run={RUN} />);

    // Click the "src" directory button
    fireEvent.click(screen.getByRole("button", { name: /^src$/i }));

    // Children should now be visible
    expect(screen.getByRole("button", { name: /^main\.ts$/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /^utils\.ts$/i })).toBeInTheDocument();
  });

  it("collapses a directory when clicked again after expansion", () => {
    mockUseProjectWorkspace.mockReturnValue({
      data: WORKSPACE_TREE,
      isLoading: false,
      error: null,
    });

    render(<RunWorkspace run={RUN} />);

    const srcButton = screen.getByRole("button", { name: /^src$/i });
    // Expand
    fireEvent.click(srcButton);
    expect(screen.getByRole("button", { name: /^main\.ts$/i })).toBeInTheDocument();

    // Collapse
    fireEvent.click(srcButton);
    expect(screen.queryByRole("button", { name: /^main\.ts$/i })).not.toBeInTheDocument();
  });

  it("shows the selected file path in the header and renders file content", () => {
    mockUseProjectWorkspace.mockReturnValue({
      data: WORKSPACE_TREE,
      isLoading: false,
      error: null,
    });
    mockUseProjectFile.mockReturnValue({
      data: { content: "# Genesis Engine" },
      isLoading: false,
      error: null,
    });

    render(<RunWorkspace run={RUN} />);

    // Select the README.md file
    fireEvent.click(screen.getByRole("button", { name: /^README\.md$/i }));

    // File path shows in the header (file name now appears in both the tree button and the header code element)
    const readmeInstances = screen.getAllByText("README.md");
    expect(readmeInstances.length).toBeGreaterThanOrEqual(2);
    // File content renders in the pre block
    expect(screen.getByLabelText("File content: README.md")).toBeInTheDocument();
    expect(screen.getByText("# Genesis Engine")).toBeInTheDocument();
  });

  it("shows a loading spinner in the file viewer while content is loading", () => {
    mockUseProjectWorkspace.mockReturnValue({
      data: WORKSPACE_TREE,
      isLoading: false,
      error: null,
    });
    mockUseProjectFile.mockReturnValue({ data: null, isLoading: true, error: null });

    render(<RunWorkspace run={RUN} />);

    fireEvent.click(screen.getByRole("button", { name: /^README\.md$/i }));

    expect(screen.getByText(/Loading file/i)).toBeInTheDocument();
  });

  it("does not display file names that are not in the backend response", () => {
    mockUseProjectWorkspace.mockReturnValue({
      data: WORKSPACE_TREE,
      isLoading: false,
      error: null,
    });

    render(<RunWorkspace run={RUN} />);

    // Invented files that are not in the fixture must not appear
    expect(screen.queryByRole("button", { name: /fake-file\.ts/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /invented-module/i })).not.toBeInTheDocument();
  });

  it("calls useProjectWorkspace with the backend project ID, not a fabricated ID", () => {
    mockUseProjectWorkspace.mockReturnValue({
      data: WORKSPACE_TREE,
      isLoading: false,
      error: null,
    });

    render(<RunWorkspace run={RUN} />);

    // Must use run.backendProjectId ("project-1"), not any other ID
    expect(mockUseProjectWorkspace).toHaveBeenCalledWith("project-1");
  });

  it("calls useProjectFile with the backend project ID when a file is selected", () => {
    mockUseProjectWorkspace.mockReturnValue({
      data: WORKSPACE_TREE,
      isLoading: false,
      error: null,
    });
    mockUseProjectFile.mockReturnValue({
      data: { content: "export {}" },
      isLoading: false,
      error: null,
    });

    render(<RunWorkspace run={RUN} />);
    // Expand src directory, then click main.ts
    fireEvent.click(screen.getByRole("button", { name: /^src$/i }));
    fireEvent.click(screen.getByRole("button", { name: /^main\.ts$/i }));

    // File hook must be called with the backendProjectId and the real file path
    expect(mockUseProjectFile).toHaveBeenCalledWith("project-1", "src/main.ts");
  });
});

// ── RunRouteScaffold — workspace surface integration ──────────────────────────

describe("RunRouteScaffold workspace surface", () => {
  beforeEach(() => {
    mockUseProject.mockReset();
    mockUseProjectWorkspace.mockReset();
    mockUseProjectFile.mockReturnValue({ data: null, isLoading: false, error: null });
  });

  it("renders the file tree when the workspace API returns data", () => {
    mockUseProject.mockReturnValue({
      data: {
        id: "project-1",
        title: "Test Project",
        status: "SUCCESS",
        created_at: "2026-06-29T10:00:00Z",
      },
      isLoading: false,
      error: null,
    });
    mockUseProjectWorkspace.mockReturnValue({
      data: WORKSPACE_TREE,
      isLoading: false,
      error: null,
    });

    render(<RunRouteScaffold projectId="project-1" runId="project-1" surface="workspace" />);

    expect(screen.getByRole("button", { name: /^src$/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /^README\.md$/i })).toBeInTheDocument();
  });

  it("shows unavailable state when workspace API returns nothing", () => {
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
    mockUseProjectWorkspace.mockReturnValue({ data: [], isLoading: false, error: null });

    render(<RunRouteScaffold projectId="project-1" runId="project-1" surface="workspace" />);

    expect(screen.getByText(/Workspace files unavailable/i)).toBeInTheDocument();
    expect(screen.queryByLabelText(/Workspace file tree/i)).not.toBeInTheDocument();
  });
});
