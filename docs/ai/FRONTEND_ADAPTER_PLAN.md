# Frontend Adapter Plan

Status: planned for Milestone 1.5. Do not implement until explicitly approved.

## Problem

The current frozen backend exposes project/workspace-shaped data. The target frontend UI must be Run-centered.

Current backend shape includes concepts such as:

- project list
- project detail
- project status
- project telemetry
- project manifest
- graphs
- workspace files

Target frontend shape is:

```text
Organization
  Project
    Run
      Specification
      Planning Report
      Architecture
      Compilation Trace
      Artifact Bundle
```

The frontend must bridge this mismatch without inventing backend APIs, fake endpoints, mock Run history, or hardcoded data.

## Planned Location

Do not place new adapter or domain files under `src/app/dashboard/lib`. That would couple the Run-centered model to the legacy dashboard route.

Use a route-neutral frontend library location instead:

```text
frontend/src/lib/genesis/view-models.ts
frontend/src/lib/genesis/adapters.ts
frontend/src/lib/genesis/capabilities.ts
```

## Planned View Models

`ProjectViewModel` should preserve the backend project ID explicitly:

```ts
type ProjectViewModel = {
  id: string;
  backendProjectId: string;
  name: string;
  description?: string;
  lastRun?: RunViewModel;
  runs: RunSummaryViewModel[];
};
```

`RunViewModel` should represent the UI's atomic work unit while preserving backend call targets:

```ts
type RunViewModel = {
  id: string;
  backendProjectId: string;
  backendWorkspaceId?: string;
  source: "backend-project-as-latest-run";
  projectId: string;
  projectName: string;
  status: RunStatus;
  createdAt?: string;
  durationMs?: number;
  specification?: ProjectSpecification;
  planningReport?: PlanningReport;
  architectureGraphs?: Record<string, unknown>;
  compilationTrace?: ExecutionTrace[];
  artifactBundle?: ArtifactBundleViewModel;
  capabilities: RunCapabilities;
};
```

`RunCapabilities` should describe which Run-level surfaces are backed by real data:

```ts
type RunCapabilities = {
  hasExplicitRunHistory: boolean;
  hasPlanningReport: boolean;
  hasArchitectureGraphs: boolean;
  hasWorkspaceFiles: boolean;
  hasArtifactManifest: boolean;
  hasCompilationTrace: boolean;
};
```

`ArtifactBundleViewModel` should represent deployable and inspectable outputs:

- `manifest`
- `files`
- `workspaceHash`
- `deploymentHash`

## Mapping Strategy

- Treat each existing backend project/workspace record as the latest known Run until explicit backend Run history exists.
- Derive project name from specification name/title when available, then fall back to backend ID.
- Preserve raw backend IDs so existing frozen endpoints continue to work.
- The UI may display Run-centered language, but backend calls must continue using `backendProjectId` or `backendWorkspaceId` until real backend Run endpoints exist.
- Keep API calls in the existing frontend API client.
- Add pure frontend adapter functions only after approval, such as `toProjectViewModel(project)` and `toRunViewModel(project)`.
- Add adapter tests when implementation begins.
- Render unavailable target fields as honest empty states rather than fake data.

## Guardrails

- Do not add mock runs.
- Do not create fake backend routes.
- Do not change auth, compiler submission, SSE, artifact download, or deployment contracts.
- Do not hide missing backend capabilities behind hardcoded UI data.
- Do not require backend schema changes for frontend route migration.
- Do not implement this during Milestone 1 unless explicitly approved. This remains Milestone 1.5.
