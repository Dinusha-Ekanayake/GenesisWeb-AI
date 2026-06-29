import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { RunArtifacts } from "../src/components/run/RunArtifacts";
import { RunRouteScaffold } from "../src/components/routes/RunRouteScaffold";
import type { RunViewModel, ArtifactBundleViewModel } from "../src/lib/genesis/view-models";
import type { DeploymentManifest } from "../src/app/dashboard/types/genesis";

// ── Module mocks ──────────────────────────────────────────────────────────────

const mockUseProject = vi.fn();
vi.mock("../src/app/dashboard/lib/hooks", () => ({
  useProject: (...args: any[]) => mockUseProject(...args),
}));

// ── Test fixtures ─────────────────────────────────────────────────────────────

const MANIFEST: DeploymentManifest = {
  project_id: "project-1",
  graph_hashes: {
    endpoint_graph: "hash-abc123",
    page_graph: "hash-def456",
  },
  rule_engine_score: 92,
  plugin_versions: {
    "genesis-core": "2.1.0",
    "genesis-api": "1.4.3",
  },
  build_status: "SUCCESS",
  deployment_hash: "deploy-hash-xyz789",
  workspace_hash: "workspace-hash-abc",
};

const BUNDLE_WITH_MANIFEST: ArtifactBundleViewModel = {
  manifest: MANIFEST,
  files: [
    {
      name: "deployment_bundle.zip",
      path: "artifacts/deployment_bundle.zip",
      type: "zip",
      sizeBytes: 204800,
      backendProjectId: "project-1",
    },
    {
      name: "deployment_manifest.json",
      path: "artifacts/deployment_manifest.json",
      type: "json",
      backendProjectId: "project-1",
    },
  ],
  workspaceHash: "workspace-hash-abc",
  deploymentHash: "deploy-hash-xyz789",
};

const BUNDLE_HASHES_ONLY: ArtifactBundleViewModel = {
  manifest: undefined,
  files: [],
  workspaceHash: "workspace-hash-only",
  deploymentHash: undefined,
};

const BUNDLE_NO_FILES: ArtifactBundleViewModel = {
  manifest: MANIFEST,
  files: [],
  workspaceHash: "workspace-hash-abc",
  deploymentHash: "deploy-hash-xyz789",
};

const RUN_WITH_BUNDLE: RunViewModel = {
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
    hasArtifactManifest: true,
    hasCompilationTrace: false,
  },
  artifactBundle: BUNDLE_WITH_MANIFEST,
};

const RUN_WITHOUT_BUNDLE: RunViewModel = {
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

// ── RunArtifacts — pure component tests ──────────────────────────────────────

describe("RunArtifacts", () => {
  it("shows unavailable state when artifactBundle is absent", () => {
    render(<RunArtifacts run={RUN_WITHOUT_BUNDLE} />);

    expect(screen.getByText(/No artifact bundle available/i)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Open Compiler/i })).toHaveAttribute(
      "href",
      "/compiler"
    );
  });

  it("does not render artifact content when bundle is absent", () => {
    render(<RunArtifacts run={RUN_WITHOUT_BUNDLE} />);

    expect(screen.queryByText("Deployment Bundle Ready")).not.toBeInTheDocument();
    expect(screen.queryByText("Cryptographic Hashes")).not.toBeInTheDocument();
    expect(screen.queryByText("Artifact Files")).not.toBeInTheDocument();
  });

  it("shows build status banner from real manifest data", () => {
    render(<RunArtifacts run={RUN_WITH_BUNDLE} />);

    expect(screen.getByText("Deployment Bundle Ready")).toBeInTheDocument();
    // "SUCCESS" appears in both the banner code element and the manifest metadata card
    const successInstances = screen.getAllByText("SUCCESS");
    expect(successInstances.length).toBeGreaterThanOrEqual(1);
  });

  it("shows the workspace hash from the bundle", () => {
    render(<RunArtifacts run={RUN_WITH_BUNDLE} />);

    expect(screen.getByText("Cryptographic Hashes")).toBeInTheDocument();
    expect(screen.getByText("workspace-hash-abc")).toBeInTheDocument();
  });

  it("shows the deployment hash from the bundle", () => {
    render(<RunArtifacts run={RUN_WITH_BUNDLE} />);

    expect(screen.getByText("deploy-hash-xyz789")).toBeInTheDocument();
  });

  it("hides the hashes card when both hashes are absent", () => {
    const runNoHashes: RunViewModel = {
      ...RUN_WITH_BUNDLE,
      artifactBundle: { ...BUNDLE_NO_FILES, workspaceHash: undefined, deploymentHash: undefined },
    };

    render(<RunArtifacts run={runNoHashes} />);

    expect(screen.queryByText("Cryptographic Hashes")).not.toBeInTheDocument();
  });

  it("shows hashes-only bundle without a manifest", () => {
    const runHashesOnly: RunViewModel = {
      ...RUN_WITH_BUNDLE,
      artifactBundle: BUNDLE_HASHES_ONLY,
    };

    render(<RunArtifacts run={runHashesOnly} />);

    expect(screen.getByText("workspace-hash-only")).toBeInTheDocument();
    // No manifest means no status banner or manifest card
    expect(screen.queryByText("Deployment Bundle Ready")).not.toBeInTheDocument();
    expect(screen.queryByText("Manifest Metadata")).not.toBeInTheDocument();
  });

  it("shows manifest metadata: project ID, rule engine score, build status", () => {
    render(<RunArtifacts run={RUN_WITH_BUNDLE} />);

    expect(screen.getByText("Manifest Metadata")).toBeInTheDocument();
    // project_id appears in manifest card (may also appear in identity)
    const projectIdInstances = screen.getAllByText("project-1");
    expect(projectIdInstances.length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText("92")).toBeInTheDocument(); // rule_engine_score
  });

  it("shows plugin versions from the manifest", () => {
    render(<RunArtifacts run={RUN_WITH_BUNDLE} />);

    expect(screen.getByText("Plugin Versions")).toBeInTheDocument();
    expect(screen.getByText("genesis-core")).toBeInTheDocument();
    expect(screen.getByText("genesis-api")).toBeInTheDocument();
    expect(screen.getByText("v2.1.0")).toBeInTheDocument();
    expect(screen.getByText("v1.4.3")).toBeInTheDocument();
  });

  it("shows graph hashes from the manifest", () => {
    render(<RunArtifacts run={RUN_WITH_BUNDLE} />);

    expect(screen.getByText("Graph Hashes")).toBeInTheDocument();
    expect(screen.getByText("hash-abc123")).toBeInTheDocument();
    expect(screen.getByText("hash-def456")).toBeInTheDocument();
  });

  it("shows real artifact file names from the bundle", () => {
    render(<RunArtifacts run={RUN_WITH_BUNDLE} />);

    expect(screen.getByText("Artifact Files")).toBeInTheDocument();
    expect(screen.getByText("deployment_bundle.zip")).toBeInTheDocument();
    expect(screen.getByText("deployment_manifest.json")).toBeInTheDocument();
  });

  it("does not invent artifact file names not in the bundle", () => {
    render(<RunArtifacts run={RUN_WITH_BUNDLE} />);

    // These are the hardcoded names from DeploymentPanel — must not appear unless in the fixture
    expect(screen.queryByText("execution_trace.json")).not.toBeInTheDocument();
    expect(screen.queryByText("planning_report.json")).not.toBeInTheDocument();
    expect(screen.queryByText("api_graph.json")).not.toBeInTheDocument();
  });

  it("download links use the backend project ID in the href, not an invented ID", () => {
    render(<RunArtifacts run={RUN_WITH_BUNDLE} />);

    const downloadLink = screen.getByRole("link", {
      name: /Download deployment_bundle\.zip/i,
    });
    const href = downloadLink.getAttribute("href") ?? "";
    expect(href).toContain("project-1"); // backendProjectId
    expect(href).toContain("deployment_bundle.zip");
    // Ensure it's not pointing at a fake or hardcoded path
    expect(href).toMatch(/genesis\/projects\/project-1\/artifacts\//);
  });

  it("download anchor has the download attribute set to the filename", () => {
    render(<RunArtifacts run={RUN_WITH_BUNDLE} />);

    const downloadLink = screen.getByRole("link", {
      name: /Download deployment_bundle\.zip/i,
    });
    expect(downloadLink).toHaveAttribute("download", "deployment_bundle.zip");
  });

  it("shows a no-files message when bundle has an empty files array", () => {
    const runNoFiles: RunViewModel = {
      ...RUN_WITH_BUNDLE,
      artifactBundle: BUNDLE_NO_FILES,
    };

    render(<RunArtifacts run={runNoFiles} />);

    expect(screen.getByText(/No artifact files are listed/i)).toBeInTheDocument();
    // No download links should appear
    expect(screen.queryByRole("link", { name: /Download/i })).not.toBeInTheDocument();
  });
});

// ── RunRouteScaffold — artifacts surface integration ──────────────────────────

describe("RunRouteScaffold artifacts surface", () => {
  beforeEach(() => {
    mockUseProject.mockReset();
  });

  it("renders artifact content when the project has a deployment manifest", () => {
    mockUseProject.mockReturnValue({
      data: {
        id: "project-1",
        title: "Test Project",
        status: "SUCCESS",
        created_at: "2026-06-29T10:00:00Z",
        deployment_manifest: MANIFEST,
      },
      isLoading: false,
      error: null,
    });

    render(<RunRouteScaffold projectId="project-1" runId="project-1" surface="artifacts" />);

    expect(screen.getByText("Deployment Bundle Ready")).toBeInTheDocument();
    // "SUCCESS" appears in the StatusBadge header, StatusBanner, and ManifestCard metadata row
    expect(screen.getAllByText("SUCCESS").length).toBeGreaterThanOrEqual(2);
    expect(screen.getByText("workspace-hash-abc")).toBeInTheDocument();
  });

  it("shows unavailable state when project has no deployment manifest or artifact data", () => {
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

    render(<RunRouteScaffold projectId="project-1" runId="project-1" surface="artifacts" />);

    expect(screen.getByText(/No artifact bundle available/i)).toBeInTheDocument();
    expect(screen.queryByText("Deployment Bundle Ready")).not.toBeInTheDocument();
  });
});
