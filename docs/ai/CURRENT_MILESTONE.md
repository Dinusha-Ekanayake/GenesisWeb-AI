# Current Milestone

Status: implementation in progress — Milestone 5.1.

## Active Scope

Milestone 5.1 — Run Overview only.

Goal: turn `/projects/[id]/runs/[runId]` into a real, honest Run Overview page using the existing frontend adapter and existing backend project/workspace-shaped data.

What is being built:

- `frontend/src/components/run/RunOverview.tsx` — new pure component; receives `RunViewModel` from the existing adapter; shows run summary, backend identity, specification summary, and capability-driven surface cards
- `frontend/tests/run-overview.test.tsx` — new tests for RunOverview and RunRouteScaffold mismatch guard
- Modifying `frontend/src/components/routes/RunRouteScaffold.tsx` — extract inline Overview into RunOverview; no other surface behavior changes

## Out Of Scope

- Architecture, Workspace, Artifacts, Planning Report surfaces (those are later M5 sub-milestones)
- Full compiler experience changes (M4 complete)
- Dashboard redesign
- Removal of legacy routes
- Backend, API, auth, or compiler behavior changes
- New backend endpoints
- Mock data or fake Run history
- Git commit, push, staging, or history modification

## Completed Milestones

- M1: Design system foundation
- M1.1: Validation tooling stabilization
- M1.2: Build/test baseline fixed
- M1.3: .gitignore hygiene
- M1.5: Frontend adapter (view-model contracts, mapping functions, adapter tests)
- M2: App shell and navigation architecture
- M3: Route architecture ((app) route group, target route shells)
- M3.1: Route/shell QA and navigation hardening
- M4: Compiler Experience (/compiler global workspace + run-specific read-only trace)

## Validation Commands

From `frontend/`:

```powershell
npm.cmd run lint
npm.cmd run build
npm.cmd test
git diff --check
```

Expected baseline (M4): lint pass, build pass, 12 files / 30 tests pass, diff --check pass (CRLF warnings only).

## Stopping Point

Stop after Milestone 5.1 Run Overview is implemented and validated.
