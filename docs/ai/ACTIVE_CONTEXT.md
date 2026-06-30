# Active Context

Last updated: 2026-06-30 09:35 +05:30

This repository is the Genesis Engine implementation. The frontend is being migrated from prototype UI toward the v3.0 specification. The product is a Specification Compiler platform, not a chatbot, CRUD dashboard, generic admin panel, or code generator UI.

Core product model:

```text
Organization -> Project -> Run
```

A Run is the atomic unit of work and contains Specification, Planning Report, Architecture, Compilation Trace, and Artifact Bundle.

## Current State

Milestone 0 is complete: repository-to-spec gap analysis was performed.

Milestone 1 is complete: frontend design system foundation was implemented. No backend code was changed. No new routes were added. `/dashboard` was not migrated. Existing routes, backend API calls, authentication, and compiler behavior were preserved.

Milestone 1.1 is complete for validation tooling stabilization only. It did not implement Milestone 1.5, adapter code, routes, app shell migration, backend changes, API changes, mock data, or fake endpoints.

Milestone 1 changed the frontend styling foundation only:

- Added semantic CSS tokens in `frontend/src/styles/tokens.css`, including surfaces, borders, text, accent, status, radius, spacing, elevation, and animation values
- Updated global styling in `frontend/src/app/globals.css`
- Integrated Inter and JetBrains Mono in `frontend/src/app/layout.tsx`
- Updated `frontend/tailwind.config.ts` to consume semantic tokens
- Removed duplicate `frontend/tailwind.config.js`
- Added or improved shared primitives: Button, Card, Badge, StatusBadge, Input, EmptyState, Skeleton, Spinner
- Added adapter planning notes in `docs/FrontendAdapterDesign.md` and `docs/ai/FRONTEND_ADAPTER_PLAN.md`

User explicitly instructed: do not push, commit, or stage anything without permission.

## Frozen Constraints

- Backend, APIs, authentication, deterministic compiler pipeline, deployment system, and data contracts are frozen.
- Do not modify backend code unless there is a frontend integration bug and user approval is requested first.
- Do not invent backend endpoints.
- Do not add mock data.
- Do not route-migrate or redesign screens without milestone approval.
- Existing frontend code is prototype code and must not override the specification.

## Important Decisions

- Semantic design tokens now live in CSS variables, with Tailwind configured as a consumer rather than the source of product semantics.
- Dark enterprise UI is the default token theme, with a `.light` token set available but not wired into a theme switcher.
- UI typography uses Inter for interface text and JetBrains Mono for code or technical values.
- Shared primitives were updated conservatively so existing routes can keep compiling.
- The future Run-centered UI must use a frontend adapter layer before route migration.
- The approved adapter planning location is `frontend/src/lib/genesis/`, but adapter implementation is not approved yet.

## Validation Status

Before Milestone 1.1 changes, `npm.cmd run build` compiled the app bundle, but Next type validation failed because local dependency `@playwright/test` was missing.

Before Milestone 1.1 changes, `npm.cmd test` failed because local dependency `vitest` was missing.

Before Milestone 1.1 changes, `npm.cmd run lint` opened the first-time Next ESLint configuration prompt because the frontend had no ESLint config.

Milestone 1.1 added explicit Next ESLint configuration, installed/locked frontend validation dependencies, and scoped Vitest to `frontend/tests` so Playwright e2e specs remain under `npm run test:e2e`.

After Milestone 1.1, validation commands are non-interactive and repeatable:

- `npm.cmd run lint` passes with no warnings or errors.
- `npm.cmd run build` compiles successfully, then fails on an existing route/component type mismatch in `src/app/dashboard/project/[id]/page.tsx`.
- `npm.cmd test` runs Vitest and fails on existing unit test/component mismatches, not missing tooling.
- `git diff --check` passes with CRLF warnings only.
- Playwright browser binaries were not installed; `npx.cmd playwright install --dry-run chromium` only reported intended install locations and download URLs.

Milestone 1.2 is complete for existing build/test baseline fixes only:

- Fixed `frontend/src/app/dashboard/project/[id]/page.tsx` to pass existing project planning report data and telemetry traces to child components using their current prop contracts.
- Updated `PlanningReportViewer` to accept missing reports and render an honest empty state.
- Updated stale unit tests to match current component props and empty-state copy.
- Adjusted `frontend/vitest.config.ts` to avoid duplicate Vite plugin type conflicts and use the automatic JSX runtime in tests.

Current validation status after Milestone 1.2:

- `npm.cmd run lint` passes.
- `npm.cmd run build` passes.
- `npm.cmd test` passes: 8 files, 10 tests.
- `git diff --check` passes with CRLF warnings only.

Milestone 1.3 is complete for `.gitignore` hygiene only:

- Removed only the invalid final `.gitignore` entry `C:\Users\Dinusha Ekanayake\`.
- Did not rewrite or normalize the rest of `.gitignore`.
- Did not modify frontend source, backend code, package files, routes, adapter code, app shell, API contracts, compiler behavior, mock data, or fake endpoints.
- `rg --files` works without the previous invalid-glob warning.

Milestone 1.5 is complete for the frontend adapter view-model contract only:

- Added route-neutral adapter files under `frontend/src/lib/genesis/`.
- Added view-model contracts for Project, Run, Run summary, Run capabilities, artifact bundle, and artifact files.
- Added pure mapping functions that treat each backend project/workspace record as the latest known Run.
- Preserved `backendProjectId`, optional `backendWorkspaceId`, and `source: "backend-project-as-latest-run"`.
- Added focused adapter tests in `frontend/tests/genesis-adapters.test.ts`.
- Did not add routes, migrate `/dashboard`, implement app shell, change backend/API/compiler behavior, add mock runs, or invent endpoints.

Current validation status after Milestone 1.5:

- `npm.cmd run lint` passes.
- `npm.cmd run build` passes.
- `npm.cmd test` passes: 9 files, 15 tests.
- `git diff --check` passes with CRLF warnings only.

Milestone 2 is complete for app shell and navigation architecture only:

- Added route-neutral shell components under `frontend/src/components/layout/`.
- Replaced the old fixed flex dashboard wrapper with a CSS Grid app shell in `frontend/src/app/dashboard/layout.tsx`.
- Implemented a 48px Global Rail, 0/240px Context Panel, 52px Header Bar, Main Work Surface, and right panel foundation.
- Added `ShellProvider` for context/right panel expanded state with localStorage persistence and hydration-safe defaults.
- Added active navigation and breadcrumbs from the current pathname.
- Kept `/login` outside the authenticated dashboard shell.
- Kept existing routes unchanged: `/`, `/login`, `/dashboard`, and `/dashboard/project/[id]`.
- Did not migrate `/dashboard`, create product routes, implement compiler/Run pages, change backend/API/compiler behavior, add mock data, or invent endpoints.

Current validation status after Milestone 2:

- `npm.cmd run lint` passes.
- `npm.cmd run build` passes.
- `npm.cmd test` passes: 10 files, 17 tests.
- `git diff --check` passes with CRLF warnings only.

Milestone 3 is complete for route architecture only:

- Added the target route shells under the `(app)` route group, wrapped by the existing app shell.
- Added `/projects`, `/projects/[id]`, `/projects/[id]/runs`, `/projects/[id]/runs/[runId]`, Run child route shells, `/runs`, `/compiler`, `/telemetry`, `/team`, `/settings`, and `/search`.
- Kept `/`, `/login`, `/dashboard`, and `/dashboard/project/[id]` working and unchanged as public/legacy compatibility routes.
- Used the frontend Genesis adapter to map backend project records into Project and latest-known Run view models.
- Did not invent Run history; unsupported surfaces render limited states.
- Did not implement full compiler, Run overview, architecture, workspace, artifact, or report experiences.
- Updated shell navigation to point at new target route shells without redirects.

Current validation status after Milestone 3:

- `npm.cmd run lint` passes.
- `npm.cmd run build` passes and lists the new target routes.
- `npm.cmd test` passes: 11 files, 20 tests.
- `git diff --check` passes with CRLF warnings only.

Milestone 5.1 is complete for the Run Overview only:

- Added `frontend/src/components/run/RunOverview.tsx` — pure prop-driven component receiving `RunViewModel` from the existing adapter.
- RunOverview shows: project name + status badge, backend project ID in summary description and explicit Backend Identity card, latest-known-run source label with honest explanation, created date and formatted duration if available, specification summary (spec ID, name, pages count, components count) if `run.specification` is present, and 5 surface cards (Compiler, Planning Report, Architecture, Workspace, Artifacts) with capability-driven Available/Unavailable badges and links to Run subroutes.
- All subroute links use `run.backendProjectId` and `run.id` — not any invented or URL-derived IDs.
- Backend Identity card explicitly shows `backendProjectId`, `backendWorkspaceId`, and `run.id` with clear labels and a note that backend API calls must use these IDs.
- Removed inline `Overview` and `CapabilitySummary` helper functions from `RunRouteScaffold.tsx`; `SurfaceContent` now delegates to `RunOverview`.
- Added `frontend/tests/run-overview.test.tsx` with 17 tests covering: name/status rendering, source label honesty, backend ID display, duration formatting, specification summary, surface card links, capability badge states, mismatch guard behavior, and absence of fabricated run history.
- Did not implement Architecture, Workspace, Artifacts, or Report surfaces.
- Did not change backend, API, auth, or compiler behavior.
- Did not add mock data, fake Run history, or invent backend endpoints.

Milestone 6 is complete for the Dashboard / Product Home Redesign only:

- Created `frontend/src/components/dashboard/ControlPlaneHome.tsx` — "use client" component using `useProjects()` and the existing adapter. Renders inside `RouteScaffold` (eyebrow: "Platform", title: "Genesis Engine", description: "Specification Compiler Platform"). Header actions: **Open Compiler** (accent/primary, links to `/compiler`) + **View Projects** (secondary, links to `/projects`). Content states: loading spinner, backend error banner (using error token, no hardcoded slate), empty `LimitedState` with "Open Compiler" CTA, or — when projects exist — a `StatsStrip` (4 tiles: Projects / Active Builds / Failed / Deployed, all derived from real `useProjects()` data) and a `RecentProjectsGrid` (up to 6 adapter-mapped project cards, each linking to `/projects/[id]/runs/[id]` using `backendProjectId`). Honest disclaimer: "Each project currently exposes its latest known Run only. Real Run history requires a future backend endpoint."
- Modified `frontend/src/app/dashboard/page.tsx` — replaced the entire previous content (SpecEditor, ExecutionStatusPanel, `handleRunCompiler`, `handleValidateSpec`, `useSSE("*")`, all hardcoded slate classes) with a single import and render of `ControlPlaneHome`. The `/dashboard` route continues to exist.
- Modified `frontend/src/app/page.tsx` — replaced the generic chatbot/assistant landing page (hardcoded slate gradients, "builds... from a simple prompt") with a proper Genesis control plane entry page using design tokens: "Specification Compiler" heading, subtitle, "Open Compiler" CTA → `/compiler`, "View Projects" CTA → `/projects`. No AppShell wrapper (standalone page).
- Created `frontend/tests/control-plane-home.test.tsx` — 19 tests: heading/subtitle, CTA links, loading state, error state, empty LimitedState with CTA, project names from adapter, card links using backendProjectId and run.id, "latest known Run" language, stats counts (Projects, Failed, Active Builds, Deployed), no SpecEditor, no ExecutionStatusPanel, no fabricated data, cap-at-6 projects.
- Two test fixes during development: (1) "Open Compiler" test used `getByRole` but empty state renders TWO "Open Compiler" links (header CTA + LimitedState CTA) — fixed with `getAllByRole`. (2) "Failed" stat label collides with `StatusBadge.label = "Failed"` for FAILED projects — fixed with `getAllByText`.
- `/projects` page unchanged. `/compiler` page unchanged. All legacy dashboard sub-routes unchanged.
- Removed prototype dashboard behaviors: no embedded SpecEditor, no ExecutionStatusPanel, no global SSE subscription, no slate color classes, no chatbot/assistant language.

Current validation status after Milestone 6:

- `npm.cmd run lint` passes.
- `npm.cmd run build` passes and lists all target/legacy routes.
- `npm.cmd test` passes: **18 files, 131 tests**.
- `git diff --check` passes with CRLF warnings only.

Milestone 5.6 is complete for the Run Detail Visual QA and Consistency Pass only:

- Inspected all six Run detail components and the shared RouteScaffold. No hardcoded slate colors, no fake data, no invented endpoints, no fabricated run history found anywhere in the suite.
- Fixed accessibility gap in `RunOverview.tsx`: the 5 surface card "Open" links had no `aria-label`, making all five indistinguishable to screen readers. Added `aria-label={`Open ${surface.label}`}` to each link (e.g., "Open Compiler", "Open Planning Report", "Open Architecture", "Open Workspace", "Open Artifacts").
- Fixed card title size inconsistency in `RunArchitectureGraph.tsx`: `GraphPanel.CardTitle` used `className="text-sm font-semibold capitalize"` while every other CardTitle across all Run surfaces uses `text-base`. Changed to `text-base capitalize` to match.
- Updated `run-overview.test.tsx` to query each surface link by its new descriptive accessible name instead of the generic `"Open"` string. The test now uses `getByRole("link", { name: "Open Compiler" })` etc., which is also a more robust assertion.
- All remaining findings were confirmed clean: no slate colors, no mock data, all "Open Compiler" CTAs use the same class string, all LimitedState copy is consistent, all backend calls use `backendProjectId`, responsive grid breakpoints present throughout. The `runId !== projectId` mismatch guard test remains green.
- Did not implement new features. Did not modify backend code. Did not change API contracts. Did not add mock data.

Current validation status after Milestone 5.6:

- `npm.cmd run lint` passes.
- `npm.cmd run build` passes and lists all target/legacy routes.
- `npm.cmd test` passes: **17 files, 112 tests**.
- `git diff --check` passes with CRLF warnings only.

Milestone 5.5 is complete for the Artifacts surface only:

- Added `frontend/src/components/run/RunArtifacts.tsx` — pure component (no hooks, no API calls). Receives `RunViewModel`. Shows: `StatusBanner` (from `manifest.build_status` — only when truthy), `HashesCard` (workspace + deployment SHA-256 hashes, hidden when both absent), `ManifestCard` (metadata: project_id, rule_engine_score, build_status; Plugin Versions list; Graph Hashes list), `ArtifactFilesCard` (real files from `run.artifactBundle.files` with download `<a href download>` anchors, or "No artifact files are listed" when empty). Unavailable state (LimitedState + Open Compiler link) when `run.artifactBundle` is absent.
- Download links are built via `buildArtifactUrl(file)` using `process.env.NEXT_PUBLIC_API_URL` and `file.backendProjectId` from the adapter — never a URL-derived or invented ID. The `download` attribute is set to `file.name`.
- Decision: did NOT reuse `DeploymentPanel` from the legacy dashboard. `DeploymentPanel` has a hardcoded list of 8 invented artifact filenames (`deployment_bundle.zip`, `api_graph.json`, `planning_report.json`, etc.) regardless of actual backend data. `RunArtifacts` shows only files returned by the backend adapter.
- Updated `frontend/src/components/routes/RunRouteScaffold.tsx` — replaced the old artifacts LimitedState with `<RunArtifacts run={run} />`. All Card-related imports were removed from `RunRouteScaffold` (the last card usage was replaced). Import list now includes: RunArchitectureGraph, RunPlanningReport, RunArtifacts, RunWorkspace, RunOverview.
- Added `frontend/tests/run-artifacts.test.tsx` with 17 tests: unavailable state + no artifact content, banner from real manifest data, workspace/deployment hashes, hashes-hidden-when-absent, hashes-only bundle without manifest, manifest metadata (project_id, rule_engine_score), plugin versions, graph hashes, real file names, no invented file names, download href uses backendProjectId, download attribute set to filename, no-files message, no download links when empty, and 2 RunRouteScaffold integration tests (with/without manifest).
- Two test failures were fixed during development: `getByText("SUCCESS")` matched multiple elements (StatusBadge in the RunRouteScaffold header, StatusBanner, and ManifestCard metadata row). Fixed with `getAllByText("SUCCESS").length >= N` assertions.
- Did not change backend, API, auth, or compiler behavior.
- Did not add mock data, fake artifact files, fake download links, or invent backend endpoints.

Current validation status after Milestone 5.5:

- `npm.cmd run lint` passes.
- `npm.cmd run build` passes and lists all target/legacy routes.
- `npm.cmd test` passes: **17 files, 112 tests**.
- `git diff --check` passes with CRLF warnings only.

Milestone 5.4 is complete for the Workspace surface only:

- Added `frontend/src/components/run/RunWorkspace.tsx` — component with hooks: `useProjectWorkspace(run.backendProjectId)` (file tree) and delegates `useProjectFile(run.backendProjectId, path)` to a `FileViewer` child. The `backendProjectId` is always used for API calls — never the URL `runId`. Shows: loading spinner, LimitedState when workspace API returns empty/error (+ Open Compiler link), file tree sidebar with expandable directories via `FileTreeNode` (recursive, each directory manages its own `useState(open)`), file content `<pre>` block in the right panel. No Monaco Editor — consistent with other M5 surfaces using `<pre>` for content.
- `run.capabilities.hasWorkspaceFiles` is NOT used as the workspace guard (the standard `GET /genesis/projects/{id}` endpoint does not embed workspace files; they come from a separate endpoint). The workspace surface always fetches and renders honestly based on the API response.
- Updated `frontend/src/components/routes/RunRouteScaffold.tsx` — replaced the old workspace LimitedState (which linked to the legacy dashboard workspace) with `<RunWorkspace run={run} />`.
- Added `frontend/tests/run-workspace.test.tsx` with 16 tests: loading state, API error state, empty-array state, file/directory names from real data, backend project ID in header, placeholder before file selection, directory expand/collapse via `fireEvent.click`, file content in pre after selection, file viewer loading state, no invented files, `useProjectWorkspace` called with backendProjectId, `useProjectFile` called with backendProjectId and real path, plus 2 RunRouteScaffold integration tests. One initial test failure (`getByText("README.md")` found two elements — tree button + header code) fixed with `getAllByText(...).length >= 2` + `getByLabelText("File content: README.md")`.
- Did not implement Artifacts surface.
- Did not change backend, API, auth, or compiler behavior.
- Did not add mock data, fake files, or invent backend endpoints.
- `@testing-library/user-event` is not installed — used `fireEvent` throughout.

Current validation status after Milestone 5.4:

- `npm.cmd run lint` passes.
- `npm.cmd run build` passes and lists all target/legacy routes.
- `npm.cmd test` passes: 16 files, 95 tests.
- `git diff --check` passes with CRLF warnings only.

Milestone 5.3 is complete for the Architecture Graph surface only:

- Added `frontend/src/components/run/RunArchitectureGraph.tsx` — pure component (uses `useState` for graph tab selection, no backend calls). Receives `RunViewModel`. Shows: graph-name selector buttons (one per key in `run.architectureGraphs`), a collection stats grid (counts of `endpoints`, `pages`, `components`, `features`, `tables` where present), and the selected graph's raw JSON in a scrollable `<pre>` block. Unavailable state (LimitedState + Open Compiler link) when `!run.capabilities.hasArchitectureGraphs` or the graph record is empty.
- Updated `frontend/src/components/routes/RunRouteScaffold.tsx` — replaced the old architecture badge card (showed only graph keys as badges) with `<RunArchitectureGraph run={run} />`. Removed the now-unused `CapabilityBadge` import.
- Added `frontend/tests/run-architecture.test.tsx` with 13 tests: unavailable state (capability false, undefined graphs), graph selector buttons, graph count label, collection stats, raw JSON in pre block, no invented data, graph tab switching via fireEvent.click, unknown graph shape (no stats, still shows JSON), aria-pressed on active button, singular/plural graph count label, and 2 RunRouteScaffold integration tests (with/without architecture_graphs in mocked project).
- Decision: did not reuse `GraphInspector`. Reason: `GraphInspector` calls `useProjectGraphs(projectId)` (a separate backend request we already satisfy via the adapter), depends on `@xyflow/react` (React Flow — not installed in test env, hard to mock), and uses hardcoded slate colors.
- Did not implement Workspace or Artifacts surfaces.
- Did not change backend, API, auth, or compiler behavior.
- Did not add mock data, fake Run history, or invent backend endpoints.
- `@testing-library/user-event` is not installed — used `fireEvent` from `@testing-library/react` instead.

Current validation status after Milestone 5.3:

- `npm.cmd run lint` passes.
- `npm.cmd run build` passes and lists all target/legacy routes.
- `npm.cmd test` passes: 15 files, 79 tests.
- `git diff --check` passes with CRLF warnings only.

Milestone 5.2 is complete for the Planning Report surface only:

- Added `frontend/src/components/run/RunPlanningReport.tsx` — pure prop-driven component receiving `RunViewModel` from the existing adapter. Shows: status header (rule_validation_status, integrity score, planning_duration_ms, error/warning counts), 8-tile metrics grid (features, pages, APIs, entities, components, dependencies, errors, warnings), optional rule coverage card (api_coverage, db_coverage, ui_coverage, overall_score), failed rules list (only when failed_rules is non-empty), planning assumptions list (only when non-empty), full rule execution trace with PASS/FAIL/WARN status badges per rule and inline context JSON, and graph/workspace hashes.
- Updated `frontend/src/components/routes/RunRouteScaffold.tsx` — replaced the old fallthrough minimal planning report card with an explicit `if (surface === "report") return <RunPlanningReport run={run} />;` branch. Removed the deferred-milestone placeholder card that showed only 4 fields.
- `RunPlanningReport` handles absent report with LimitedState "Planning report not available" + link to `/compiler`. All optional sections (rule_coverage, failed_rules, assumptions, graph_hashes) are silently omitted when empty or absent.
- Decision: did not reuse `PlanningReportViewer` from the legacy dashboard. Reason: it uses hardcoded slate/dark Tailwind colors inconsistent with the design token system. Legacy component is unchanged.
- Added `frontend/tests/run-planning-report.test.tsx` with 19 tests: unavailable state, success/failed status, integrity score, duration format, all 8 metric tiles, rule coverage present/absent, assumptions present/absent, rule trace entries with status badges, trace messages, graph hashes, failed rules present/absent, FAIL badge, no invented data when absent, empty trace message, plus 2 RunRouteScaffold integration tests (report surface with and without backend planning_report).
- Did not implement Architecture, Workspace, or Artifacts surfaces.
- Did not change backend, API, auth, or compiler behavior.
- Did not add mock data, fake Run history, or invent backend endpoints.

Current validation status after Milestone 5.2:

- `npm.cmd run lint` passes.
- `npm.cmd run build` passes and lists all target/legacy routes.
- `npm.cmd test` passes: 14 files, 66 tests.
- `git diff --check` passes with CRLF warnings only.

Milestone 5.1 is complete for the Run Overview only:

- Added `frontend/src/components/run/RunOverview.tsx` — pure prop-driven component receiving `RunViewModel` from the existing adapter.
- RunOverview shows: project name + status badge, backend project ID in summary description and explicit Backend Identity card, latest-known-run source label with honest explanation, created date and formatted duration if available, specification summary (spec ID, name, pages count, components count) if `run.specification` is present, and 5 surface cards (Compiler, Planning Report, Architecture, Workspace, Artifacts) with capability-driven Available/Unavailable badges and links to Run subroutes.
- All subroute links use `run.backendProjectId` and `run.id` — not any invented or URL-derived IDs.
- Backend Identity card explicitly shows `backendProjectId`, `backendWorkspaceId`, and `run.id` with clear labels and a note that backend API calls must use these IDs.
- Removed inline `Overview` and `CapabilitySummary` helper functions from `RunRouteScaffold.tsx`; `SurfaceContent` now delegates to `RunOverview`.
- Added `frontend/tests/run-overview.test.tsx` with 17 tests covering: name/status rendering, source label honesty, backend ID display, duration formatting, specification summary, surface card links, capability badge states, mismatch guard behavior, and absence of fabricated run history.
- Did not implement Architecture, Workspace, Artifacts, or Report surfaces.
- Did not change backend, API, auth, or compiler behavior.
- Did not add mock data, fake Run history, or invent backend endpoints.

Current validation status after Milestone 5.1:

- `npm.cmd run lint` passes.
- `npm.cmd run build` passes and lists all target/legacy routes.
- `npm.cmd test` passes: 13 files, 47 tests.
- `git diff --check` passes with CRLF warnings only.

Milestone 4 is complete for the compiler experience only:

- Implemented `frontend/src/components/compiler/CompilerWorkspace.tsx` as the primary compiler page component.
- Reused `SpecEditor`, `ExecutionStatusPanel`, `GenesisAPI`, and `useSSE` directly from their legacy locations without modification.
- `useSSE(activeProjectId)` subscribes to live backend events once `spec.project_id` is set before awaiting `runCompiler`, matching the legacy dashboard pattern so events stream during compilation.
- Completion CTA derives the navigation target from `compilationResult.manifest.project_id` (real backend ID returned by the API) mapped to `/projects/{id}/runs/{id}` using the latest-known-run identity rule.
- Run-specific `/projects/[id]/runs/[runId]/compiler` surface updated: shows read-only compilation trace from `run.compilationTrace` (adapter-mapped from `project.execution_trace`) when available; falls back to a LimitedState with a link to `/compiler`. No live compiler workflow, no SSE subscription, no submit button on the run-specific surface.
- Added `frontend/tests/compiler.test.tsx` with 9 tests covering: idle state, compile dispatch, completion CTA using real backend IDs, no fake Run history, read-only run-specific surface, and no live-workflow embedding.
- Updated `frontend/tests/route-architecture.test.tsx` to reflect that `/compiler` is no longer a LimitedState; CompilerWorkspace is mocked in that file to keep route-architecture tests focused on route existence only.
- Did not implement Architecture, Workspace, Artifacts, or Report pages.
- Did not redesign `/dashboard`.
- Did not remove legacy routes.
- Did not change backend, API, auth, or compiler behavior.
- Did not add mock data, fake Run history, or invent backend endpoints.

Current validation status after Milestone 4:

- `npm.cmd run lint` passes.
- `npm.cmd run build` passes and lists all target/legacy routes.
- `npm.cmd test` passes: 12 files, 30 tests.
- `git diff --check` passes with CRLF warnings only.

Milestone 3.1 is complete for route/shell QA and navigation hardening only:

- Inspected all target route shells and legacy compatibility routes.
- Verified route shells use honest limited states and adapter-backed latest-known Runs rather than fake Run history.
- Replaced hardcoded `API Connected` shell badge with neutral `Shell Ready` to avoid implying live backend status.
- Added `/runs` to the Context Panel navigation.
- Added shell test coverage for `/runs` active state and right panel visibility.
- Did not implement compiler experience, full Run pages, dashboard redesign, backend/API/compiler changes, mock data, or fake endpoints.

Current validation status after Milestone 3.1:

- `npm.cmd run lint` passes.
- `npm.cmd run build` passes and lists all target/legacy routes.
- `npm.cmd test` passes: 11 files, 21 tests.
- `git diff --check` passes with CRLF warnings only.

`git diff --check` passed with CRLF warnings only.

An attempted `npm.cmd install` hung silently and was stopped. No package or lockfile changes were detected from that attempt.

The root `.gitignore` has unrelated existing changes, including a final literal Windows path entry that causes `rg` to report an invalid glob. Do not modify `.gitignore` unless the user approves.

## Risks

- Local dependency install is incomplete or stale.
- `next/font/google` required network access once to fetch fonts; the build succeeded past font loading after escalation.
- The target UI is Run-centered, while current backend payloads remain project/workspace-shaped.
- Route migration before adapter design would risk inventing frontend-only assumptions or fake backend concepts.

Milestone 7 is complete for the Command Palette and Keyboard Shortcuts only:

- Created `frontend/src/components/commands/commands.ts` — typed `Command` definition and `COMMANDS` array: 8 navigation commands (Dashboard, Compiler, Projects, Runs, Telemetry, Team, Settings, Search), 2 shell commands (Toggle Context Panel, Toggle Right Panel). Navigate commands carry `{ type: "navigate", href }` action; shell commands carry `{ type: "shell", action }`. Four commands include shortcut hints: G D / G C / G P / G R for route shortcuts, Ctrl \\ and Ctrl P for shell toggles.
- Created `frontend/src/components/commands/useKeyboardShortcuts.ts` — custom hook accepting `isOpen`, `onOpen`, `onClose`, `paletteInputRef`, `toggleContextPanel`, `toggleRightPanel`, `onNavigate`. Registers one `keydown` listener on `document` via `useEffect`. Handles: Escape (closes palette), Ctrl+K/Cmd+K (toggle palette, blocked when non-palette input is focused), Ctrl+\\ (toggleContextPanel), Ctrl+P (toggleRightPanel), G-sequence (first G sets `awaitingSequence = true` with 1s timeout; d/c/p/r completes to mapped href). No new npm dependency — custom implementation only.
- Created `frontend/src/components/commands/CommandPalette.tsx` — "use client" modal overlay component. Closed state renders null (no DOM impact). Open state renders: fixed full-screen backdrop (click to close) + palette box (search input + filtered command list + keyboard shortcut badges). Calls `useShell()` for panel toggles, `useRouter()` for navigation, `useKeyboardShortcuts()` for all keyboard handling. Arrow key navigation + Enter execution. Filter is case-insensitive substring match over `cmd.label`.
- Modified `frontend/src/components/layout/AppShell.tsx` — imported `CommandPalette` and added `<CommandPalette />` as a sibling after the grid `<div>` inside `ShellGrid`, wrapped in a React fragment. This gives it access to `useShell()` (within the existing `ShellProvider` scope) while rendering as a fixed overlay outside the grid flow.
- Modified `frontend/tests/app-shell.test.tsx` — added `useRouter: () => ({ push: vi.fn() })` to the `next/navigation` mock. Required because `CommandPalette` (now mounted inside `AppShell`) calls `useRouter()`; the existing mock only exported `usePathname`.
- Created `frontend/tests/command-palette.test.tsx` — 23 tests: palette hidden on mount, opens on Ctrl+K, opens on Cmd+K, closes on Escape, closes on backdrop click, toggles off on second Ctrl+K, shows all 8 navigation commands + 2 shell commands, shortcut hints for G D / G C / G P / G R, filtering by query, no-match message, clicking a command navigates + closes, Open Dashboard navigates to /dashboard, Toggle Context Panel calls hook + closes, Toggle Right Panel calls hook + closes, Ctrl+\\ calls toggleContextPanel without opening palette, Ctrl+P calls toggleRightPanel without opening palette, G D / G C / G P / G R sequences navigate, input guard (Ctrl+K blocked when external input focused), no fake/demo/mock commands.
- Did not install any new npm dependency (no cmdk, no headless-ui). No backend code changed. No API contracts changed. No compiler behavior changed. No mock data added. No fake search results. Static navigation only.

Current validation status after Milestone 7:

- `npm.cmd run lint` passes.
- `npm.cmd run build` passes and lists all target/legacy routes.
- `npm.cmd test` passes: **19 files, 154 tests**.
- `git diff --check` passes with CRLF warnings only.

Milestone 8 is complete for the Search Route / Global Search Surface only:

- Created `frontend/src/components/search/search-index.ts` — pure module: `buildSearchResults(projects, query)` maps `ProjectData[]` through `toRunViewModel()` and filters by case-insensitive substring match against projectName, projectId, status, specName, specDescription. `deriveSurfaceLinks()` builds available surface hrefs from `RunCapabilities` flags using `backendProjectId` for all segments (identity rule: `run.id === project.id`). Returns `SearchResult[]` with `projectId`, `runId`, `projectName`, `status`, `specName?`, `specDescription?`, `surfaceLinks[]`.
- Created `frontend/src/components/search/SearchResultCard.tsx` — pure component: renders project name link → run overview, backend ID (`ID: {projectId}` in mono), spec description if present, "View Run" primary link, capability-gated surface links (Planning Report, Architecture, Workspace, Artifacts, Compiler Trace). All hrefs use `backendProjectId`. `aria-label` on "View Run" link for screen-reader disambiguation.
- Created `frontend/src/components/search/GlobalSearchPage.tsx` — "use client"; calls `useProjects()`, `buildSearchResults(projects, query)`, manages `useState(query)`. Renders inside `RouteScaffold(eyebrow: "Search", title: "Search")`. Four content states: loading (`LoadingState`), backend error (`ErrorState` with `--error` token), empty query (`EmptyQueryState` listing what can be searched), no-results (`LimitedState("No results")`), or result list. Persistent scope disclaimer: "Search currently covers projects and latest-known-run metadata only. File contents, compilation traces, and full Run history are not indexed."
- Modified `frontend/src/app/(app)/search/page.tsx` — replaced `LimitedState("Search deferred")` with a single import and render of `GlobalSearchPage`. Route remains at `/search`.
- Modified `frontend/tests/route-architecture.test.tsx` — added `SearchPage` import and one test: "renders the search page with a Search heading and a search input". Follows same mock pattern as existing route tests.
- Created `frontend/tests/global-search.test.tsx` — 23 tests: heading, input, placeholder (projects/runs/statuses), scope disclaimer, file-contents disclaimer, loading state, loading hides results list, error state, empty query explanatory state (what can be searched), results from real data, backend ID in card, spec description in card, filter by name / ID / status, View Run link uses backendProjectId, Artifacts surface link href, Planning Report surface link href, no surface links when capability absent, no-results state, no fake data, no file-search claim.

What is searchable: project name, backend project ID, status, spec name, spec description.
What is NOT yet searchable: file contents, compilation trace text, planning report rule names, architecture graph internals, real Run history.

Current validation status after Milestone 8:

- `npm.cmd run lint` passes.
- `npm.cmd run build` passes; `/search` now listed as `○ (Static)` at 2.22 kB.
- `npm.cmd test` passes: **20 files, 178 tests**.
- `git diff --check` passes with CRLF warnings only.

Milestone 9 is complete for the Settings / Preferences Surface only:

- Created `frontend/src/components/settings/AppearanceCard.tsx` — "use client"; calls `useTheme()` from `next-themes`. Renders three `aria-pressed` buttons: System / Light / Dark. Active button is highlighted with accent colors. `next-themes` is already wired in `Providers.tsx` with `attribute="class"` and `defaultTheme="system"`. Both `.dark` and `.light` CSS token classes exist in `tokens.css`.
- Created `frontend/src/components/settings/ShellPreferencesCard.tsx` — "use client"; calls `useShell()`. Renders two `ToggleRow` items (Context Panel, Right Panel) each showing current state ("Expanded"/"Collapsed"), a toggle button with `aria-label` and `aria-pressed`, and a "Reset to defaults" button that calls `setContextPanelExpanded(true)` + `setRightPanelExpanded(false)` — restoring the `ShellProvider` defaults without directly touching localStorage.
- Created `frontend/src/components/settings/ShortcutReferenceCard.tsx` — pure component (no hooks); renders a two-column table of all 8 keyboard shortcuts defined in M7: Ctrl/Cmd+K, Escape, G D, G C, G P, G R, Ctrl+\\, Ctrl+P. Uses `<kbd>` for key display.
- Created `frontend/src/components/settings/SettingsPage.tsx` — server component (no "use client"); composes the three cards inside `RouteScaffold(eyebrow: "Preferences", title: "Settings")`. Always-visible note: "Settings are stored locally in this browser and device. They are not synced to any backend."
- Modified `frontend/src/app/(app)/settings/page.tsx` — replaced `LimitedState("Settings deferred")` with `<SettingsPage />`. The route remains at `/settings`.
- Created `frontend/tests/settings.test.tsx` — 20 tests: heading, local-only note, not-synced note, appearance section + all three theme buttons, active theme aria-pressed, three setTheme calls, shell preferences section, context/right panel aria-pressed state, two toggle calls, reset call with correct args, keyboard shortcuts section, three specific shortcut entries, no fake account/billing/team settings.

What is exposed: context panel expanded/collapsed (localStorage via ShellProvider), right panel expanded/collapsed (localStorage via ShellProvider), color theme dark/light/system (localStorage via next-themes), shortcut reference (read-only), reset to defaults.
What is intentionally out of scope: backend user settings, account/profile, billing, team management, cloud-synced preferences, font/density/language.

Current validation status after Milestone 9:

- `npm.cmd run lint` passes.
- `npm.cmd run build` passes; `/settings` listed as `○ (Static)` at 2.94 kB.
- `npm.cmd test` passes: **21 files, 198 tests**.
- `git diff --check` passes with CRLF warnings only.

Milestone 10 is complete for the Telemetry Surface only:

- Created `frontend/src/components/telemetry/telemetry-metrics.ts` — pure `deriveTelemetryMetrics(projects)` using `toRunCapabilities()` to compute: totalProjects, statusCounts[], avgPlanningDurationMs, planningReportCount, architectureGraphCount, artifactManifestCount, compilationTraceCount.
- Created `frontend/src/components/telemetry/MetricCard.tsx`, `StatusBreakdown.tsx`, `CapabilityCoverage.tsx`, `RecentRunTelemetry.tsx` — composable display tiles; RecentRunTelemetry shows last 8 runs with links built via `backendProjectId`.
- Created `frontend/src/components/telemetry/TelemetryPage.tsx` — "use client"; pulls from `useProjects()`, shows always-visible scope note ("metadata only, no live telemetry"), loading/error/empty/data states.
- Updated `frontend/src/app/(app)/telemetry/page.tsx` to render `TelemetryPage`.
- Added `frontend/tests/telemetry.test.tsx` with 23 tests.
- Did not add live metrics, time-series charts, or a telemetry backend.

Milestone 11 is complete for the Final Route QA and Production Readiness Pass only:

- Removed `<Badge variant="secondary">Shell Ready</Badge>` from `AppHeader.tsx` and `<Badge variant="outline">Foundation</Badge>` from `RightPanel.tsx`.
- Updated `RightPanel.tsx` copy to honest: "Open a Run to inspect its surfaces — planning report, architecture graphs, workspace files, and artifact bundle."
- Fixed `ControlPlaneHome.tsx` "Deployed" stat to use `Boolean(p.deployment_manifest)` (presence) instead of `build_status === "COMPLETED"` (brittle string).
- Updated `/team` page description to remove stale "milestone" language.
- Updated `app-shell.test.tsx` and `control-plane-home.test.tsx` to match the above changes.

Current validation baseline after M11: **22 files / 222 tests pass**.

Milestone 12 is complete for Backend-Connected Manual Smoke Test Support only:

**Inspection findings:**
- Backend base URL: `http://127.0.0.1:8000/api/v1` (hardcoded fallback in `api-client.ts` and `hooks.ts`).
- Required env var: `NEXT_PUBLIC_API_URL` (optional for local dev; must include `/api/v1` suffix).
- No `frontend/.env.local` exists — the hardcoded fallback is the only config for local dev.
- JWT auth: `POST /api/v1/auth/token` with form-data, returns `{ access_token }`. Frontend reads from `localStorage.genesis_token`. No login page exists in the App Router — testers must manually POST and set localStorage.
- Static credentials: `developer` / `devpassword` (full permissions), `admin` / `admin`, `viewer` / `viewpassword`.
- Backend CORS: allows `http://localhost:3000` and `http://127.0.0.1:3000` — covers both local dev modes.
- SSE: `GET /api/v1/genesis/events?project_id=...&token=...` — token passed as query param (EventSource cannot set headers).
- 11 backend endpoints used; all under `/api/v1/genesis/...`.
- Pages offline-safe: `/settings`, `/team`, app shell nav, command palette, theme toggle.
- Pages requiring backend: `/projects`, `/runs`, `/telemetry`, `/search`, `/compiler`, all `/projects/[id]/runs/[runId]` surfaces.

**Real blocker found and fixed:**
- `docker-compose.yml` line 47 had `NEXT_PUBLIC_API_URL=http://localhost:8000` (missing `/api/v1`). Every API call under Docker would 404. Fixed to `http://localhost:8000/api/v1`.

No frontend source files changed. No tests added or changed. Validation baseline unchanged: **22 files / 222 tests pass**.

## Next Task

Stop here until the user explicitly approves the next milestone. M12 (Backend-Connected Manual Smoke Test Support) is complete. Current validation baseline: 22 files / 222 tests.
