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

Milestone 13 is complete for Login / Auth UX Integration only:

- Created `frontend/src/lib/auth/login.ts` — `loginWithCredentials(username, password)` wraps `POST /auth/token`, maps 401 → "Incorrect username or password.", network throw → "Unable to reach the server. Check that the backend is running.", other non-ok → "Login failed. Please try again.", returns `access_token` string.
- Rewrote `frontend/src/app/login/page.tsx` — replaced all hardcoded slate/blue Tailwind classes with design tokens (`bg-surface-base`, `bg-surface-raised`, `border-border`, `bg-accent`, `text-accent-foreground`, `text-[color:var(--error)]`, etc.); added `htmlFor`/`id` on all form fields; error div uses `role="alert"`; imports from `login.ts` + `setToken` from `api-client.ts`.
- Modified `frontend/src/components/layout/AppHeader.tsx` — added `LogOut` icon button with `aria-label="Sign out"` that calls `removeToken()` + `router.push("/login")`. Visible on every authenticated page.
- Replaced 2-test `frontend/tests/Login.test.tsx` with 10-test M13 suite: username/password fields rendered, Sign In button, calls `loginWithCredentials` with credentials, stores token, redirects to `/dashboard`, shows error on invalid credentials, shows error on network failure, button disabled during flight, no signup/register/OAuth/reset UI.
- Updated `frontend/tests/app-shell.test.tsx` — extracted `mockPush` to module scope; added test: "sign out removes genesis_token and redirects to /login".
- Did not create `frontend/src/lib/auth/token.ts` — `api-client.ts` already exports `getToken`/`setToken`/`removeToken` with SSR guards.
- Did not add logout to SettingsPage — it is a server component; adding logout there would require making it client-side.
- Did not add signup, register, OAuth, profile, password reset, or role management.

Current validation baseline after M13: **22 files / 231 tests pass**.

Milestone 14 is complete for Auth Guard / Unauthorized Redirect only:

- Created `frontend/src/components/auth/AuthGuard.tsx` — `"use client"` component with 3-state `"checking" | "authenticated" | "unauthenticated"` status. On mount: reads `getToken()` (from `api-client.ts`); if present sets "authenticated" and renders children; if absent sets "unauthenticated" and calls `router.replace("/login")`. Renders `null` in non-authenticated states — no flash of protected content.
- Modified `frontend/src/app/(app)/layout.tsx` — wraps `<AppShell>` in `<AuthGuard>`. Protects all `(app)` routes.
- Modified `frontend/src/app/dashboard/layout.tsx` — same pattern. Protects `/dashboard` and `/dashboard/project/[id]`.
- `frontend/src/app/login/page.tsx` — unchanged, remains public (no layout guard above it).
- `frontend/src/app/page.tsx` — unchanged, remains public.
- Created `frontend/tests/auth-guard.test.tsx` — 3 tests: renders children with token, calls `router.replace("/login")` without token, does not render children without token.
- No existing test files modified — all tests render components directly, bypassing layouts.

Current validation baseline after M14: **23 files / 234 tests pass**.

Milestone 15 is complete for Auth Expiry / 401 Handling only:

- Modified `frontend/src/app/dashboard/lib/api-client.ts` — added 401 branch at the top of the `!res.ok` block in `fetchWrapper`. On 401 with `typeof window !== "undefined"`: calls `removeToken()`, calls `window.location.replace("/login")` unless already on `/login` (`window.location.pathname !== "/login"`), throws `new APIError(401, "Authentication expired. Please sign in again.")`.
- The login endpoint (`POST /auth/token`) is not affected — `loginWithCredentials` uses raw `fetch`, not `fetchWrapper`. Wrong-password 401s do not trigger the global handler.
- Modified `frontend/tests/api.test.ts` — added `describe("fetchWrapper 401 handling")` with 5 tests: removes token, redirects when not on /login, does not redirect when on /login, throws auth-expired error, non-401 errors leave token intact and do not redirect.
- Tests mock `window.location` per-test using `vi.stubGlobal("location", { pathname, replace: vi.fn() })` with `vi.unstubAllGlobals()` cleanup.

Current validation baseline after M15: **23 files / 239 tests pass**.

Milestone 16 is complete for Authenticated End-to-End Smoke Test Runner only:

- Created `scripts/smoke_test_genesis.py` — developer smoke-test script using Python stdlib only (no external dependencies, no venv activation required for running).
- Uses only `urllib.request`, `urllib.parse`, `urllib.error`, `argparse`, `json`, `sys` — compatible with Python 3.8+ system installs.
- Default mode is read-only. `--generate` flag opt-in enables POST endpoints (`/genesis/validate`, `/genesis/generate`) that may create a workspace entry or invoke the LLM if `OPENAI_API_KEY` is set.
- CLI args: `--backend-url` (default `http://127.0.0.1:8000`), `--api-prefix` (default `/api/v1`), `--username` (default `developer`), `--password` (default `devpassword`), `--generate` (flag, default off).
- Automated checks: `GET /health` (exits immediately if unreachable), `POST /auth/token` (exits if 401 or fail), `GET /genesis/projects`, per-project `GET /projects/{id}` / `/workspace` / `/manifest` / `/graphs` (first project only; 404 skipped, not failed), `POST /genesis/validate` + `POST /genesis/generate` (only with `--generate`).
- Non-automated section: prints a formatted frontend manual checklist (8 routes + 5 auth flow verification steps) with localhost:3000 URLs.
- Exit code 0 = all automated checks passed, 1 = any automated check failed.
- Graceful failure: if backend is unreachable at step 1, prints startup instructions (`venv` activation + uvicorn command) and exits 1 without running further checks.
- Verified: `python -m py_compile scripts/smoke_test_genesis.py` → syntax OK. `python scripts/smoke_test_genesis.py --help` → correct output. `python scripts/smoke_test_genesis.py --backend-url http://127.0.0.1:9999` → exit code 1 with unreachable message.
- No frontend source files changed. No backend code changed. No API contracts changed. No tests added (script is self-testing via subprocess). Validation baseline unchanged: **23 files / 239 tests pass**.

Milestone 17 is complete for Real Compiler Generate Smoke Test only:

**Generate smoke test result: PASS (all automated checks passed)**

- `POST /genesis/validate` → PASS, `integrity_score=100`
- `POST /genesis/generate` → PASS, `project_id=smoke_test_001`
- Generate response manifest contains: 6 `graph_hashes` (FeatureGraph, PageGraph, ComponentGraph, ApiGraph, DatabaseGraph, DependencyGraph), `rule_engine_score=100`, `plugin_versions` (FastApiMinimalGenerator 1.0, NextJsMinimalGenerator 1.0), `build_status=SUCCESS`, `deployment_hash`, `workspace_hash`
- Physical workspace created at `workspace/smoke_test_001/` with 8 real files: `backend/app/main.py`, `frontend/app/dashboard/page.tsx`, `frontend/app/navbar/page.tsx`, `docker-compose.yml`, `Dockerfile.backend`, `Dockerfile.frontend`, `execution_trace.json`, `spec.json`

**Backend behavior confirmed (consistent across all 8 projects):**
- `GET /genesis/projects/{id}` returns `planning_report: null`, `deployment_manifest: null` for all projects — backend generates and returns manifest data in the `/generate` response body but does NOT persist it back to the project record
- `GET /genesis/projects/{id}/manifest` returns `data: {}` for all projects (empty dict, not null)
- `GET /genesis/projects/{id}/graphs` returns `data: {}` for all projects
- `GET /genesis/projects/{id}/workspace` returns real workspace files after generation (7 items for smoke_test_001)
- `execution_trace` IS populated in the project detail (12 events for smoke_test_001 after two generate runs)

**Frontend adapter is correct for real generated project shape:**
- `planning_report: null` → `run.planningReport = undefined` → Planning Report surface shows honest LimitedState
- `deployment_manifest: null` + no `artifact_files` → `run.artifactBundle = undefined` → Artifacts surface shows honest LimitedState
- `execution_trace: [12 events]` → `run.compilationTrace` populated → Compiler trace surface shows real events
- `spec.name = "Smoke Test"` → `run.projectName = "Smoke Test"` (via `project.spec?.name`)
- `status: "SUCCESS"` → `run.status = "SUCCESS"` → SUCCESS badge
- `hasArchitectureGraphs = false` (graphs not in project detail) → Architecture surface shows honest LimitedState
- `hasWorkspaceFiles = false` (workspace not in project detail), BUT workspace surface fetches separately via `GET /workspace` → returns 7 real files
- `hasCompilationTrace = true` → Compiler surface on run detail shows trace

**No code changes made.** No null guards missing. No broken route links. No adapter mapping errors. The adapter correctly handles the real backend response shape as it existed before this milestone.

**Cosmetic note (not a bug):** The smoke test prints "null (not yet compiled)" for the manifest endpoint because the backend consistently returns `data: {}` (falsy) for all projects after generation. The test correctly shows `[PASS]` — the message is slightly misleading but functionally accurate in that no structured manifest is accessible via `GET /manifest`.

No files changed. Validation baseline unchanged: **23 files / 239 tests pass**.

Milestone 18 is complete for Generated App Quality Benchmark only:

**Created `scripts/benchmark_genesis.py`** — stdlib-only benchmark runner; runs validate + generate for 3 benchmark specs; inspects workspace file tree and prints key file contents. Verified syntax with `py_compile`.

**Benchmark specs used:**
- A: `benchmark_portfolio_001` — 5 pages, 5 components (Personal Portfolio)
- B: `benchmark_tasks_001` — 7 pages, 7 components (Task Management Dashboard)
- C: `benchmark_crm_001` — 9 pages, 9 components (SaaS CRM Application)

**All 3 validated at score=100. All 3 generated with build_status=SUCCESS.**

**Generator behavior (consistent across all 3):**
- The `FastApiMinimalGenerator` and `NextJsMinimalGenerator` plugins are deterministic template engines, NOT LLM-based code generators
- Every entry in `pages[]` and `components[]` receives identical treatment: one `frontend/app/{name_lowercase}/page.tsx` (7-line boilerplate returning `<div><h1>X Page</h1><p>Generated deterministically.</p></div>`) and one GET+POST endpoint in `backend/app/main.py` returning `{'message': 'GET/POST X generated deterministically'}`
- Components are generated as standalone app routes, NOT as importable React modules
- No `package.json`, `requirements.txt`, `tsconfig.json`, or `next.config.js` is generated (Dockerfile explicitly notes this limitation)
- Generation time: 2.6–6.2 seconds — confirming no LLM invocation
- Output is structurally identical for all 3 benchmarks regardless of spec complexity

**Benchmark score table (0–5 per criterion, 7 criteria):**

| Criterion | A Portfolio | B Tasks | C CRM |
|---|---|---|---|
| 1. Pages/routes generated | 3 | 3 | 3 |
| 2. Component structure quality | 1 | 1 | 1 |
| 3. Backend/API structure | 1 | 1 | 1 |
| 4. Styling/layout quality | 0 | 0 | 0 |
| 5. Build/run readiness | 2 | 2 | 2 |
| 6. Real functionality vs placeholder | 0 | 0 | 0 |
| 7. Completeness against prompt | 1 | 1 | 1 |
| **Total** | **8/35** | **8/35** | **8/35** |

**Score notes:**
- Pages/routes (3): Page names match spec and files exist, but components are wrongly placed as routes, no root index route, no layout.tsx
- Component structure (1): Files exist but are not importable React components — no props, no exports, no composition
- Backend/API (1): Endpoints exist per name but frontend-only components (Navbar, Sidebar, Chart) incorrectly receive API routes; all return placeholder strings
- Styling (0): No CSS, no Tailwind, no design system applied
- Build/run (2): Pages are syntactically valid; Docker build would fail (missing package.json, requirements.txt — Dockerfile acknowledges this)
- Functionality (0): Pure placeholders; no contact form fields, no Kanban board, no auth logic
- Completeness (1): Entry names match spec; content is 100% boilerplate

**Biggest generator gaps (ranked by impact):**
1. No component/page distinction — components should be importable React modules in `src/components/`, not standalone routes in `app/`
2. No actual code generation — spec description is completely ignored; every file is identical boilerplate regardless of what was requested
3. No layout/navigation — no `layout.tsx`, no inter-page links, no shared navigation
4. No build configuration — missing `package.json`, `requirements.txt`, `tsconfig.json`, `next.config.js`
5. No TypeScript interfaces or props
6. No styling
7. Frontend-only concepts (Navbar, Chart, Sidebar) incorrectly receive backend API routes
8. Complexity has zero effect on output — A portfolio and a full CRM produce structurally identical output

**Strongest generated output:** All three score identically. B (Task Management) has the most realistic page name set for a functional app.

**Weakest generated output:** C (CRM) demonstrates most clearly that increasing spec complexity has zero effect on output quality or content.

**Can Genesis currently generate advanced websites?** No. Current output is structural scaffolding — empty page stubs with correct names. Real application code generation requires LLM-backed generator plugins (e.g., `FastApiLLMGenerator`, `NextJsLLMGenerator`).

**Files changed in M18:** `scripts/benchmark_genesis.py` (created). Three workspace directories created under `workspace/` by the generator itself (not tracked by frontend validation).
Frontend validation baseline unchanged: **23 files / 239 tests pass**.

Milestone 19 is complete for Genesis Engine Product Direction Reset and Target Architecture Plan only:

---

## M19 Architecture Report

### Current Implementation Diagnosis

**Two parallel generation paths exist — and only one is connected to the HTTP API.**

**Path A: HTTP Direct-Spec (what benchmarks used)**
`POST /genesis/generate` → `CompilerService.run_pipeline()` → `ExecutionOrchestrator.run_full_pipeline()` → `PlanningEngine.validate_blueprint()` → `GenerationEngine.execute()` → `BuildOrchestrator.execute_build()` → returns `DeploymentManifest`

**Path B: LangGraph NL-Prompt (implemented, not HTTP-exposed)**
`run_langgraph_e2e.py` → `ProjectManager` → `RequirementAnalyzer` (GPT-4-turbo structured output, `langchain_openai.ChatOpenAI`) → `GenesisCompiler` → `GenesisGenerator` → same deterministic pipeline
- `RequirementAnalyzer` calls `get_llm()` which returns `ChatOpenAI(model="gpt-4-turbo", temperature=0)` and uses `llm.with_structured_output(ProjectSpecification)`
- `SystemArchitect` LangGraph node exists (also calls GPT-4-turbo) but is not wired into the workflow graph
- No HTTP endpoint points to the LangGraph path

**Root Cause of Missing Artifact Persistence (Critical Bug)**

`run_full_pipeline()` (`genesis_engine/core/orchestrator.py:42`) has a silent persistence failure:
1. `PlanningEngine.validate_blueprint()` computes all 6 graphs (FeatureGraph, PageGraph, ComponentGraph, ApiGraph, DatabaseGraph, DependencyGraph) and the PlanningReport — but does NOT write them to disk. Only `PlanningEngine.plan()` calls `workspace_adapter.flush_transaction()` which creates `artifacts/`.
2. `run_full_pipeline()` calls `validate_blueprint()` directly and never calls `plan()`. So `artifacts/` is never created.
3. The planning report write at line 97–100 is gated on `if report_path.exists():` — this condition is always false because `artifacts/` was never created. Report is never written.
4. The 6 architecture graph JSON files are never written at all — computed in memory, discarded.
5. The deployment manifest is saved to `dist/{project_id}/deployment_manifest.json` (via Packager), not to `workspace/{project_id}/artifacts/deployment_manifest.json` where the HTTP API reads it from. This is why `GET /manifest` always returns `{}`.

**Fix is minimal:** Create `artifacts/` directory before the conditional, write report unconditionally, write each graph JSON, and write the final manifest to both `dist/` and `workspace/artifacts/`.

**Root Cause of Component/Page Conflation**

`PlanningEngine._convert_spec_to_ir()` (`planning_engine.py:45`):
```python
features = spec.pages + spec.components  # pages and components merged into one list
```
This feeds into `FeaturePlanner` → every item becomes a `FeatureNode` → `PagePlanner` → every item becomes a route → `ApiPlanner` → every item gets GET+POST endpoints. Components (Navbar, Sidebar, Table) should be importable React modules, not routes.

**Root Cause of Spec Description Being Ignored**

`GenesisIR` is built from `spec.pages + spec.components` only. The `description` field is discarded. No planner uses the description to infer entities, auth requirements, data models, or UI patterns.

**Plugin System State**

Only two plugins exist:
- `FastApiMinimalGenerator` — GET+POST endpoint per feature, all in `backend/app/main.py`, placeholder string responses
- `NextJsMinimalGenerator` — `frontend/app/{route}/page.tsx` per page, 7-line boilerplate

No plugins for: package.json, requirements.txt, tsconfig.json, next.config.js, TypeScript types, CSS/Tailwind layout, database models, CRUD endpoints, auth, tests, or seed data.

**Packager State**

`Packager.bundle()` writes `deployment_bundle.zip` and `deployment_manifest.json` to `dist/{project_id}/` — a directory the HTTP API does NOT read from. The workspace HTTP endpoint reads from `workspace/{project_id}/artifacts/`. This disconnect is why manifests are never visible via the frontend.

---

### Target Architecture

**Product Principle:**
- LLM decides what should be built
- Compiler decides how it is built
- Tests decide whether it works
- Frontend shows every decision transparently

**Layer A: Prompt Understanding**
Convert natural language to rich structured spec. Already partially implemented via `RequirementAnalyzer` (GPT-4-turbo). Needs to be HTTP-exposed and the `ProjectSpecification` model needs richer fields: `entities`, `features`, `auth_requirements`, `database_models`, `api_routes`, `ui_style`, `navigation_structure`, `app_type`, `deployment_target`.

**Layer B: Requirement Expansion Agent**
`RequirementAnalyzer` already exists in `backend/app/agents/nodes/requirement_analysis.py`. Needs HTTP endpoint exposure and richer system prompt to expand vague prompts ("Create CRM" → customers, deals, activities, pipeline, dashboard, auth, team roles, forms, filters, APIs).

**Layer C: Deterministic Validation**
Rule Engine (`genesis_engine/rules/`) already exists with `RequirePrimaryKeyRule`, `SecureMutationsRule`, `ApiToDatabaseMappingRule`, `OrphanPageRule`. Rules can be extended to check: every component has valid import path, no component generated as route unless page-level, every form maps to an entity, every protected page has auth rule.

**Layer D: Architecture Graph Layer**
6 graphs already built: FeatureGraph, PageGraph, ComponentGraph, ApiGraph, DatabaseGraph, DependencyGraph. Missing: AuthGraph, DeploymentGraph. Graphs are correct data structures but need to be persisted to `workspace/artifacts/`.

**Layer E: Blueprint Selection**
`PagePlanner` hardcodes `"DashboardLayout"` for all pages regardless of app type. A blueprint selector should map `spec.app_type` to page patterns, component patterns, and API patterns appropriate for portfolio/dashboard/CRM/ecommerce/etc.

**Layer F: Plugin-Based Code Generation**
Currently only FastApi + NextJs minimal plugins. Target: `NextJsAppRouterGenerator`, `ReactComponentGenerator`, `TailwindLayoutGenerator`, `FastAPIGenerator`, `DatabaseSchemaGenerator`, `AuthGenerator`, `CrudGenerator`, `DockerGenerator`, `PackageConfigGenerator`, `TestGenerator`.

**Layer G: LLM-Assisted Code Fill**
`RequirementAnalyzer` already uses GPT-4-turbo. New: use LLM selectively for page-specific UI content, domain-specific field names, realistic sample data, component render logic, and business logic. LLM should NOT control file paths or architecture structure — the deterministic compiler controls structure.

**Layer H: Build/Test Verification**
Currently `BuildOrchestrator` only creates Docker templates and a zip. Real verification: `npm install` + `npm run build`, `python -m pytest`, `docker compose config`. Report build results in `planning_report.build_logs`.

**Layer I: Repair Loop**
When build fails: capture stderr, identify affected file, call LLM repair agent with minimal context, apply patch, rerun build. Limit to N attempts.

**Layer J: Artifact Persistence**
`Packager` already produces `deployment_manifest.json` — but saves to `dist/`. Fix: also write to `workspace/artifacts/`. Planning report, all 6 graph JSONs, and manifest must be in `workspace/{project_id}/artifacts/` so the HTTP API can serve them to the frontend.

---

### Gap Analysis

| Gap | Current State | Target State | Priority | Milestone |
|---|---|---|---|---|
| Planning report not persisted | artifacts/ never created; conditional write always skips | Unconditionally written to workspace/{id}/artifacts/planning_report.json | Critical | M20 |
| Architecture graphs not persisted | Computed in memory, discarded | Written as *_graph.json to workspace/{id}/artifacts/ | Critical | M20 |
| Deployment manifest in wrong path | dist/{id}/deployment_manifest.json only | Also written to workspace/{id}/artifacts/deployment_manifest.json | Critical | M20 |
| Component/page conflation | pages + components → same flat feature list | Separate: pages → routes, components → importable modules | High | M23 |
| Spec description ignored | IR discards description | Feeds LLM expansion (M29) or enriched spec (M21) | High | M21 |
| No package.json / build configs | Missing from generated output | PackageConfigGenerator plugin produces all config files | High | M24 |
| LangGraph NL path not HTTP-exposed | Only accessible via run_langgraph_e2e.py | Exposed via POST /genesis/generate-from-prompt | Medium | M29 |
| No blueprint selection | All apps get DashboardLayout + same template | Blueprint selector maps app_type to page/component/API patterns | Medium | M22 |
| No LLM-backed generator plugins | Minimal deterministic only | LLM fills real component code, layout, business logic | Medium | M30 |
| No real Next.js app structure | flat app/{name}/page.tsx per item | layout.tsx, navigation, component imports, responsive layout | High | M25 |
| No real FastAPI structure | all routes in main.py, placeholder responses | routers/, models/, schemas/, CRUD per entity | High | M26 |
| No build/test runner | generates files only | npm install + build, pytest, docker compose config | Low | M27 |
| No repair loop | no recovery from failures | LLM repair agent patches and retries | Low | M28 |
| SystemArchitect node unused | Implemented, not in workflow | Wire into LangGraph workflow between RequirementAnalyzer and GenesisCompiler | Medium | M29 |

---

### New Milestone Roadmap (M20 onward)

**M20 — Persist Manifest, Architecture Graphs, and Planning Report**
Fix the artifact persistence gap. Create `artifacts/` directory unconditionally in `run_full_pipeline()`. Write all 6 graph JSONs. Write planning report unconditionally. Write manifest to `workspace/artifacts/` in addition to `dist/`. This unblocks all 5 frontend surfaces (planning report, architecture, artifacts, graphs, manifest). Zero new features — pure bug fix for data that is already computed.

**M21 — Rich App Spec v2**
Extend `ProjectSpecification` to include `app_type`, `entities`, `features_list`, `auth_requirements`, `database_models`, `api_routes`, `ui_style`. Update planners to consume the richer spec. Update validation rules.

**M22 — Blueprint Selection System**
Add blueprint registry. Map `app_type` to appropriate page structures, component trees, and API patterns. Blueprints: portfolio, marketing_site, dashboard, admin_panel, task_management, crm, ecommerce, lms, booking_platform, blog_cms, saas_dashboard.

**M23 — Fix Component vs Page Generation**
Separate `pages[]` and `components[]` in `_convert_spec_to_ir()`. Pages → routes via PagePlanner. Components → importable React modules in `frontend/components/`. Backend ApiPlanner should not generate endpoints for frontend-only components (Navbar, Sidebar, etc.).

**M24 — Package Config and Build-Ready App Output**
New `PackageConfigGenerator` plugin: generates `package.json` (Next.js, Tailwind, TypeScript deps), `tsconfig.json`, `next.config.js`. New `PythonConfigGenerator`: generates `requirements.txt` (FastAPI, uvicorn, pydantic). Generated app should be installable.

**M25 — Next.js App Router Advanced Generator**
Replace `NextJsMinimalGenerator` with `NextJsAppRouterGenerator`: generates real `layout.tsx` with navigation, imports components from `frontend/components/`, responsive Tailwind layout, per-page real structure appropriate to page type.

**M26 — FastAPI + CRUD + Database Schema Generator**
Replace `FastApiMinimalGenerator` with `FastAPIGenerator`: generates routers per entity, SQLAlchemy models, Pydantic schemas, CRUD endpoints, dependency injection pattern, proper `main.py` that mounts routers.

**M27 — Build/Test Runner for Generated Apps**
`BuildOrchestrator` runs `npm install + npm run build`, `python -m pytest`, `docker compose config`. Logs results to `build_logs` in planning report. Marks build_status as SUCCESS/FAIL based on real build output.

**M28 — Repair Loop**
When M27 build fails: capture stderr, find relevant file, call LLM repair agent, apply patch, rerun M27. Max N attempts. Log repair attempts in planning report.

**M29 — LLM Requirement Expansion Agent (HTTP-exposed)**
Wire existing `RequirementAnalyzer` + `SystemArchitect` LangGraph nodes to a new HTTP endpoint `POST /genesis/generate-from-prompt`. Accepts `{ "project_id": "...", "prompt": "Build a CRM..." }`. Returns planning report + generated app. `OPENAI_API_KEY` required.

**M30 — LLM-Assisted Code Fill**
After deterministic graph building, call LLM to fill page-specific content: real component render logic, domain-specific field names, realistic sample data, business logic details, copy/text. LLM fills content; compiler controls structure and file paths.

**M31 — Benchmark Suite v2**
Rerun M18 benchmark specs (A portfolio, B tasks, C CRM) against the improved generator stack. Score against 7-criterion rubric. Compare to M18 baseline of 8/35.

---

### Recommended Immediate Next Milestone

**M20 — Persist Manifest, Architecture Graphs, and Planning Report**

Reason: This is the highest-leverage fix with the smallest code surface. The planning report, all 6 graphs, and the manifest are already computed by the current pipeline — the only reason they don't appear in the frontend is a missing directory creation and an incorrect conditional write. Fixing M20:
- Makes every existing frontend surface (Planning Report, Architecture, Artifacts) show real data for the first time
- Requires changes to only 1 file: `genesis_engine/core/orchestrator.py` (~5–10 lines)
- Zero new features, zero new model changes, zero API contract changes
- Validates the entire frontend display pipeline end-to-end with real data
- Creates the transparency foundation that makes every subsequent milestone verifiable

No new plugins, no new models, no new routes. Just fix the artifact directory creation and write paths.

---

### Files Inspected

- `backend/app/api/genesis_controller.py`
- `backend/app/services/compiler_service.py`
- `backend/app/agents/workflow.py`
- `backend/app/agents/state.py`
- `backend/app/agents/llm.py`
- `backend/app/agents/nodes/requirement_analysis.py`
- `backend/app/agents/nodes/genesis_compiler.py`
- `backend/app/agents/nodes/genesis_generator.py`
- `backend/app/agents/nodes/system_architect.py`
- `genesis_engine/core/orchestrator.py`
- `genesis_engine/core/planning_engine.py`
- `genesis_engine/core/generation_engine.py`
- `genesis_engine/core/runtime.py`
- `genesis_engine/models/spec.py`
- `genesis_engine/models/ir.py`
- `genesis_engine/models/graphs.py`
- `genesis_engine/models/outputs.py`
- `genesis_engine/pipeline/execution.py`
- `genesis_engine/pipeline/planners/feature_planner.py`
- `genesis_engine/pipeline/planners/page_planner.py`
- `genesis_engine/pipeline/planners/component_planner.py`
- `genesis_engine/pipeline/planners/api_planner.py`
- `genesis_engine/plugins/implementations/fastapi_plugin.py`
- `genesis_engine/plugins/implementations/nextjs_plugin.py`
- `genesis_engine/deployment/build_orchestrator.py`
- `genesis_engine/deployment/packager.py`
- `genesis_engine/utils/workspace_adapter.py`
- `run_e2e_compiler.py`
- `run_langgraph_e2e.py`
- `scripts/smoke_test_genesis.py`
- `scripts/benchmark_genesis.py`

No files modified in M19. Frontend validation baseline unchanged: **23 files / 239 tests pass**.

Milestone 20 is complete for Persist Manifest, Architecture Graphs, and Planning Report only:

- Modified `genesis_engine/core/orchestrator.py` — `run_full_pipeline()`: replaced the always-false `if report_path.exists():` conditional write with unconditional artifact persistence. Artifacts are written AFTER `execute_build()` to avoid disturbing the tamper-detection hash check inside `BuildOrchestrator.execute_build()`.
- After `execute_build()` returns the manifest: creates `workspace/{id}/artifacts/` unconditionally, writes all 6 graph JSONs (`feature_graph.json`, `page_graph.json`, `component_graph.json`, `api_graph.json`, `database_graph.json`, `dependency_graph.json`), writes `architecture_graphs.json` (combined), writes `planning_report.json` unconditionally, writes `deployment_manifest.json` to `workspace/{id}/artifacts/` so the HTTP API can read it.
- Did not change any API contracts, frontend code, frontend tests, or other backend files.

**Before M20 (all projects):**
- `GET /projects/{id}`: `planning_report: null`, `deployment_manifest: null`
- `GET /projects/{id}/manifest`: `data: {}`
- `GET /projects/{id}/graphs`: `data: {}`

**After M20 (all newly generated projects):**
- `GET /projects/{id}`: `planning_report: { rule_validation_status: "PASS", graph_integrity_score: 100, ... }`, `deployment_manifest: { project_id: "...", build_status: "SUCCESS", ... }`
- `GET /projects/{id}/manifest`: `{ project_id: "...", build_status: "SUCCESS", rule_engine_score: 100, ... }`
- `GET /projects/{id}/graphs`: 6 graph entries (api_graph, component_graph, database_graph, dependency_graph, feature_graph, page_graph)

**Root cause of tamper detection during initial fix attempt:** The first implementation wrote artifacts BEFORE calling `execute_build()`. `BuildOrchestrator.execute_build()` re-hashes the workspace to detect tampering and compares against `report.workspace_hash` (which was computed before the artifacts were written). Writing artifacts first changed the workspace hash, causing the tamper check to fail. Fix: move all artifact writes to AFTER `execute_build()` returns.

**Smoke test results:**
- `python scripts/smoke_test_genesis.py` (read-only): PASS — manifest present, 6 graphs
- `python scripts/smoke_test_genesis.py --generate`: PASS — all checks including POST /genesis/validate and POST /genesis/generate

**API verification (artifact_persistence_001):**
- `GET /projects/artifact_persistence_001`: status=SUCCESS, planning_report non-null (rule_validation_status=PASS, graph_integrity_score=100), deployment_manifest non-null
- `GET /projects/artifact_persistence_001/manifest`: project_id=artifact_persistence_001, build_status=SUCCESS, rule_engine_score=100
- `GET /projects/artifact_persistence_001/graphs`: 6 graphs

**Frontend validation after M20:** lint pass, build pass, **23 files / 239 tests pass**, diff --check pass (CRLF warnings only). No frontend files touched.

Milestone 21 is complete for Separate Pages and Components in Compiler IR only:

**Root cause fixed:** `_convert_spec_to_ir()` in `genesis_engine/core/planning_engine.py` was concatenating `spec.pages + spec.components` into a single flat `ir.features` list. Every downstream planner treated pages and components identically, causing components like Navbar and Footer to become routes and API endpoints.

**4 files changed (backend only, no frontend product code touched):**

1. `genesis_engine/models/ir.py` — added `components: List[str]` field to `GenesisIR` so spec-declared components can be carried separately from page features.

2. `genesis_engine/core/planning_engine.py` — fixed `_convert_spec_to_ir()` to use `features=spec.pages` (pages only) and `components=spec.components` (separate). `FeaturePlanner`, `PagePlanner`, and `ApiPlanner` all read `ir.features` and were automatically fixed without needing changes.

3. `genesis_engine/pipeline/planners/component_planner.py` — added spec-declared component nodes to `ComponentGraph` with `created_by="SpecComponent"` (distinct from auto-generated `DashboardLayout` and page macro views). This populates the graph for downstream plugin consumption.

4. `genesis_engine/plugins/implementations/nextjs_plugin.py` — extended to emit `frontend/components/{Name}.tsx` for each `ComponentGraph` node where `metadata.created_by == "SpecComponent"`. Pages continue to generate under `frontend/app/{route}/page.tsx` unchanged.

**Generated output for `component_ir_001` (3 pages + 4 components):**

| Item | Before M21 | After M21 |
|---|---|---|
| `feature_graph` nodes | 7 (pages+components) | 3 (pages only) |
| `api_graph` endpoints | 14 (2×7) | 6 (2×3 pages) |
| `component_graph` nodes | 8 auto | 8 (4 auto + 4 spec) |
| `frontend/app/` files | 7 page files | 3 page files |
| `frontend/components/` files | none | 4 component stubs |
| Backend endpoints for Navbar etc. | `GET/POST /api/v1/navbar` | none |

**Verified generated structure (component_ir_001):**
```
frontend/app/home/page.tsx
frontend/app/projects/page.tsx
frontend/app/contact/page.tsx
frontend/components/Navbar.tsx
frontend/components/ProjectCard.tsx
frontend/components/ContactForm.tsx
frontend/components/Footer.tsx
backend/app/main.py  (6 endpoints: GET+POST for home, projects, contact only)
artifacts/ (9 files: all M20 persistence still works)
```

**API verification (component_ir_001):**
- `GET /projects/component_ir_001`: total_features=3, total_pages=3, total_apis=6, total_components=8, rule_validation_status=PASS
- `GET /projects/component_ir_001/manifest`: build_status=SUCCESS, rule_engine_score=100
- `GET /projects/component_ir_001/graphs`: 6 graph entries

**Smoke tests:** Both read-only and `--generate` pass. `py_compile` clean for both scripts.

**Frontend validation after M21:** lint pass, build pass, **23 files / 239 tests pass** (baseline unchanged). No frontend product files were touched.

**Remaining risks (deferred to future milestones):**
- Component stubs in `frontend/components/` are minimal (just a `<div><span>{Name}</span></div>`). Real component code generation is M25+ scope.
- Pages still use `"DashboardLayout"` as the layout for all routes regardless of app type — M22 (blueprint selection) scope.
- `planning_report.total_features` now reports only page count (3), not total spec items (7). This is semantically correct but is a visible change in the planning report for existing projects.

Milestone 22 is complete for Planning-First Architecture and Tech Stack Proposal only:

**New concept: ProposedApplicationPlan.** The backend now has a planning-only endpoint that converts a natural language prompt into a structured application proposal before any code is generated. Nothing is written to disk. No compiler or generator is called. The plan requires explicit user approval before generation can proceed.

**New endpoint: `POST /api/v1/genesis/propose`.** Accepts `{ "prompt": "...", "preferences": {...} }`. Returns `ProposedApplicationPlan` with `approval_status: "PENDING"` and `requires_approval_before_generation: true`. Does not conflict with existing `POST /genesis/plan` (which validates a structured spec).

**4 files added/modified (backend only, no frontend product code):**

1. `genesis_engine/models/planning.py` (new) — `ProposedApplicationPlan`, `TechnologyStack` (with 7 sub-models: FrontendStack, BackendStack, DatabaseStack, AiStack, AuthStack, DeploymentStack, TestingStack), `LLMApplicationProposal` (flat schema for LLM structured output)

2. `backend/app/services/planning_service.py` (new) — `PlanningService` with LLM path (via `langchain_openai.ChatOpenAI` + `with_structured_output(LLMApplicationProposal)`) and deterministic fallback (keyword detection → 9 blueprint templates). `generation_method` field is always honest: `"llm"` or `"deterministic_fallback"`.

3. `backend/app/api/genesis_controller.py` — added `POST /genesis/propose` endpoint; also added `import json` (pre-existing bug: SSE generator at line ~326 called `json.dumps()` without the import).

4. `scripts/plan_genesis.py` (new) — planning smoke test with 3 example prompts (photography portfolio, CRM, hotel booking).

**Planning flow (confirmed working):**
- `POST /genesis/propose` with `{ "prompt": "Create a CRM..." }` → returns pages, components, entities, API routes, tech stack, assumptions, warnings, `approval_status: "PENDING"`
- No workspace directories created
- No compiler or generator invoked
- LLM fallback clearly labeled: `generation_method: "deterministic_fallback"` + explicit FALLBACK warning in `plan.warnings`

**`plan_genesis.py` output for 3 prompts (fallback path — no OPENAI_API_KEY set):**
- Prompt A (photography portfolio) → `app_type=portfolio`, 5 pages, 7 components, 3 entities, 5 API routes
- Prompt B (CRM) → `app_type=crm`, 7 pages, 8 components, 6 entities, 10 API routes
- Prompt C (hotel booking) → `app_type=booking_platform`, 7 pages, 7 components, 6 entities, 8 API routes
- All 3: `approval_status=PENDING`, `requires_approval_before_generation=true`

**Smoke tests after M22:** Both read-only and `--generate` pass. `py_compile` clean for all scripts and new files.

**Frontend validation after M22:** Frontend not touched. Baseline unchanged: **23 files / 239 tests pass**.

**Remaining risks:**
- LLM path is untested without `OPENAI_API_KEY` in this session. The LLM path requires `OPENAI_API_KEY` (or `OPENAI_BASE_URL` for OpenRouter). It will be exercised when an API key is set in the backend environment.
- `ProposedApplicationPlan` is not yet connected to the compiler. A future milestone (M23+) will add an approval-gated generate flow: user approves the plan → plan converts to `ProjectSpecification` → existing compiler runs.
- Blueprint templates are fixed for 9 app types. LLM path will produce more nuanced, prompt-derived proposals.

## Next Task

Stop here until the user explicitly approves the next milestone. M22 (Planning-First Architecture and Tech Stack Proposal) is complete. Current validation baseline: 23 files / 239 tests.
