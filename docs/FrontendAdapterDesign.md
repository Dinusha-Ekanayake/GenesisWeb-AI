# Genesis Frontend Adapter Design

Status: planned for Milestone 1.5. Do not implement during Milestone 1.

## Problem

The frozen backend currently exposes data through project/workspace-shaped resources:

- Project lists and project detail records
- Project status
- Project telemetry
- Project manifest
- Project graphs
- Project workspace files

The target frontend product model is Run-centered:

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

The frontend must not invent backend endpoints to close this gap. Instead, it should introduce a frontend adapter layer that maps existing backend payloads into stable UI view models.

## Planned View Models

```ts
type ProjectViewModel = {
  id: string;
  name: string;
  description?: string;
  lastRun?: RunViewModel;
  runs: RunSummaryViewModel[];
};

type RunViewModel = {
  id: string;
  projectId: string;
  projectName: string;
  status: RunStatus;
  createdAt: string;
  durationMs?: number;
  specification?: ProjectSpecification;
  planningReport?: PlanningReport;
  architectureGraphs?: Record<string, unknown>;
  compilationTrace?: ExecutionTrace[];
  artifactBundle?: ArtifactBundleViewModel;
};

type ArtifactBundleViewModel = {
  manifest?: DeploymentManifest;
  files: ArtifactFileViewModel[];
  workspaceHash?: string;
  deploymentHash?: string;
};
```

## Mapping Strategy

- Treat each current backend project/workspace record as the latest known run until the backend exposes explicit run history.
- Derive the project name from `spec.name`, then `title`, then `id`.
- Derive the run ID from the backend record ID initially, preserving the raw ID for endpoint calls.
- Keep all endpoint calls in the existing `GenesisAPI` client.
- Add pure adapter functions such as `toProjectViewModel(project)` and `toRunViewModel(project)` in the frontend only.
- Keep raw backend IDs attached to view models so artifact, graph, telemetry, and workspace calls can continue using frozen endpoints.

## Guardrails

- Do not add mock runs.
- Do not create fake backend routes.
- Do not change auth, compiler submission, SSE, or artifact download contracts.
- Do not hide missing backend capabilities behind hardcoded data.
- When backend data cannot support a target UI field, expose that field as unavailable and render an honest empty state.

## Future Placement

Recommended location for Milestone 1.5:

```text
frontend/src/app/dashboard/lib/view-models.ts
frontend/src/app/dashboard/lib/adapters.ts
```

These files can later move to `frontend/src/lib` when route migration begins.
