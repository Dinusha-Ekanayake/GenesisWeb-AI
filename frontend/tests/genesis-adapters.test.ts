import { describe, expect, it } from "vitest";
import type { ProjectData } from "../src/app/dashboard/types/genesis";
import { toProjectViewModel, toRunViewModel } from "../src/lib/genesis/adapters";
import { toRunCapabilities } from "../src/lib/genesis/capabilities";

const baseProject: ProjectData = {
  id: "project-123",
  title: "Backend Title",
  status: "SUCCESS",
  created_at: "2026-06-29T10:00:00Z",
  spec: {
    project_id: "spec-project-123",
    name: "Specification Name",
    description: "Specification description",
    pages: ["Dashboard"],
    components: ["StatusPanel"],
  },
};

const planningReport = {
  total_features: 1,
  total_pages: 1,
  total_apis: 1,
  total_entities: 1,
  total_components: 1,
  dependency_count: 0,
  planning_duration_ms: 42,
  rule_validation_status: "SUCCESS" as const,
  total_errors: 0,
  total_warnings: 0,
  failed_rules: [],
  rule_trace: [],
  graph_integrity_score: 100,
  graph_hashes: {},
  workspace_hash: "workspace-hash",
  assumptions: [],
};

const deploymentManifest = {
  project_id: "project-123",
  graph_hashes: {},
  rule_engine_score: 100,
  plugin_versions: {},
  build_status: "ready",
  deployment_hash: "deployment-hash",
  workspace_hash: "manifest-workspace-hash",
};

describe("Genesis frontend adapters", () => {
  it("maps a backend project to a project view model with one latest run", () => {
    const viewModel = toProjectViewModel(baseProject);

    expect(viewModel).toMatchObject({
      id: "project-123",
      backendProjectId: "project-123",
      name: "Specification Name",
      description: "Specification description",
    });
    expect(viewModel.lastRun?.source).toBe("backend-project-as-latest-run");
    expect(viewModel.runs).toHaveLength(1);
    expect(viewModel.runs[0]).toMatchObject({
      id: "project-123",
      backendProjectId: "project-123",
      projectId: "project-123",
      projectName: "Specification Name",
      status: "SUCCESS",
      capabilities: {
        hasExplicitRunHistory: false,
      },
    });
  });

  it("maps run details while preserving backend ids and source", () => {
    const project = {
      ...baseProject,
      backendWorkspaceId: "workspace-789",
      planning_report: planningReport,
      execution_trace: [{ timestamp: "2026-06-29T10:00:01Z", event: "Compiled", details: { status: "ok" } }],
      deployment_manifest: deploymentManifest,
      graphs: { endpoints: [{ id: "listProjects" }] },
      artifact_files: [{ path: "dist/deployment_bundle.zip", type: "zip", size_bytes: 1024 }],
    };

    const run = toRunViewModel(project);

    expect(run).toMatchObject({
      id: "project-123",
      backendProjectId: "project-123",
      backendWorkspaceId: "workspace-789",
      source: "backend-project-as-latest-run",
      projectId: "project-123",
      projectName: "Specification Name",
      status: "SUCCESS",
      createdAt: "2026-06-29T10:00:00Z",
      durationMs: 42,
      specification: baseProject.spec,
      planningReport,
      architectureGraphs: { endpoints: [{ id: "listProjects" }] },
      compilationTrace: project.execution_trace,
    });
    expect(run.artifactBundle).toMatchObject({
      manifest: deploymentManifest,
      workspaceHash: "manifest-workspace-hash",
      deploymentHash: "deployment-hash",
      files: [{
        name: "deployment_bundle.zip",
        path: "dist/deployment_bundle.zip",
        type: "zip",
        sizeBytes: 1024,
        backendProjectId: "project-123",
        backendWorkspaceId: "workspace-789",
      }],
    });
  });

  it("derives capabilities only from real backend fields", () => {
    const capabilities = toRunCapabilities({
      ...baseProject,
      planning_report: planningReport,
      deployment_manifest: deploymentManifest,
      execution_trace: [{ timestamp: "2026-06-29T10:00:01Z", event: "Compiled", details: {} }],
      graphs: { pages: [] },
      workspace_files: [],
    });

    expect(capabilities).toEqual({
      hasExplicitRunHistory: false,
      hasPlanningReport: true,
      hasArchitectureGraphs: true,
      hasWorkspaceFiles: true,
      hasArtifactManifest: true,
      hasCompilationTrace: true,
    });
  });

  it("does not invent unsupported run fields", () => {
    const run = toRunViewModel({
      id: "minimal-project",
      title: "",
      status: "",
      created_at: "",
    });

    expect(run.projectName).toBe("minimal-project");
    expect(run.backendWorkspaceId).toBeUndefined();
    expect(run.specification).toBeUndefined();
    expect(run.planningReport).toBeUndefined();
    expect(run.architectureGraphs).toBeUndefined();
    expect(run.compilationTrace).toBeUndefined();
    expect(run.artifactBundle).toBeUndefined();
    expect(run.capabilities).toEqual({
      hasExplicitRunHistory: false,
      hasPlanningReport: false,
      hasArchitectureGraphs: false,
      hasWorkspaceFiles: false,
      hasArtifactManifest: false,
      hasCompilationTrace: false,
    });
  });

  it("falls back to title and then backend id for display names", () => {
    expect(toProjectViewModel({ ...baseProject, spec: undefined }).name).toBe("Backend Title");
    expect(toProjectViewModel({ ...baseProject, title: "", spec: undefined }).name).toBe("project-123");
  });
});
