# Current Milestone

Status: complete — Milestone 5.3.

## Active Scope

Milestone 5.2 — Planning Report Surface only.

Goal: turn `/projects/[id]/runs/[runId]/report` into a useful Planning Report page using only real backend-backed data already available through the adapter.

What is being built:

- `frontend/src/components/run/RunPlanningReport.tsx` — new pure component; receives `RunViewModel` from the adapter; shows rule validation status, integrity score, planning duration, 8 metric tiles, optional rule coverage, failed rules, assumptions, rule execution trace, and graph hashes
- `frontend/tests/run-planning-report.test.tsx` — new tests
- Modifying `frontend/src/components/routes/RunRouteScaffold.tsx` — replace the old fallthrough report card with an explicit `report` surface branch using `RunPlanningReport`

Reuse decision: A new `RunPlanningReport` component is created rather than reusing `PlanningReportViewer`. `PlanningReportViewer` uses hardcoded slate/dark colors inconsistent with the design token system. The legacy component remains unchanged.

## Out Of Scope

- Architecture, Workspace, Artifacts surfaces (later M5 sub-milestones)
- Full compiler changes
- Dashboard redesign
- Removal of legacy routes
- Backend, API, auth, or compiler behavior changes
- New backend endpoints
- Mock data or fake planning report data
- Git commit, push, staging, or history modification

## Completed Milestones

- M1: Design system foundation
- M1.1: Validation tooling stabilization
- M1.2: Build/test baseline fixed
- M1.3: .gitignore hygiene
- M1.5: Frontend adapter
- M2: App shell and navigation architecture
- M3: Route architecture
- M3.1: Route/shell QA
- M4: Compiler Experience
- M5.1: Run Overview

## Validation Commands

From `frontend/`:

```powershell
npm.cmd run lint
npm.cmd run build
npm.cmd test
git diff --check
```

Expected baseline (M5.1): lint pass, build pass, 13 files / 47 tests pass, diff --check pass (CRLF warnings only).

## Stopping Point

Stop after Milestone 5.2 Planning Report is implemented and validated.
