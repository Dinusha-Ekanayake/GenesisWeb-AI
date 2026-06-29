# Current Milestone

Status: implementation in progress — Milestone 4.

## Active Scope

Milestone 4 — Compiler Experience.

Goal: turn the `/compiler` route shell into the real Genesis compiler workspace while preserving all existing backend/API/auth/compiler behavior.

What is being built:

- `frontend/src/components/compiler/CompilerWorkspace.tsx` — new primary compiler component
- Reuses `SpecEditor`, `ExecutionStatusPanel`, `GenesisAPI`, `useSSE` from existing legacy locations without modification
- Completion CTA after successful compilation using the real backend project ID from the returned manifest
- Read-only compilation trace view on the run-specific `/projects/[id]/runs/[runId]/compiler` surface
- New tests in `frontend/tests/compiler.test.tsx`

## Out Of Scope

- Full Run pages (Architecture, Workspace, Artifacts, Report)
- Dashboard redesign
- Removal of legacy routes
- Backend, API, auth, or compiler behavior changes
- New backend endpoints
- Mock data or fake Run history
- Git commit, push, staging, or history modification

## Frozen Constraints

- Backend, APIs, authentication, deterministic compiler pipeline, and data contracts are frozen.
- All backend calls must use `backendProjectId` or `backendWorkspaceId`, not frontend Run IDs.
- Completion CTA must route only using real backend IDs returned by `GenesisAPI.runCompiler`.
- The run-specific compiler surface is read-only; it must not start a live compiler workflow.

## Completed Milestones

- M1: Design system foundation
- M1.1: Validation tooling stabilization
- M1.2: Build/test baseline fixed
- M1.3: .gitignore hygiene
- M1.5: Frontend adapter (view-model contracts, mapping functions, adapter tests)
- M2: App shell and navigation architecture
- M3: Route architecture ((app) route group, target route shells)
- M3.1: Route/shell QA and navigation hardening

## Validation Commands

From `frontend/`:

```powershell
npm.cmd run lint
npm.cmd run build
npm.cmd test
git diff --check
```

Expected baseline (M3.1): lint pass, build pass, 11 files / 21 tests pass, diff --check pass (CRLF warnings only).

## Stopping Point

Stop after Milestone 4 compiler experience is implemented and validated.
