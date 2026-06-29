# Decision Log

## 2026-06-30 02:00 +05:30

Decision: Implement the command palette and all keyboard shortcuts as a lightweight custom implementation — no `cmdk` or other palette library added.

Key decisions within M7:

1. **No new dependency.** `cmdk` is not installed and is not needed. The palette is a modal overlay with a plain `<input>` for filtering and a `<ul>` for results. A library would add bundle weight and testing friction for a feature this focused.

2. **Mount `CommandPalette` inside `ShellGrid` (wrapped in a React fragment), not in `ShellProvider` or a separate provider.** This gives the palette natural `useShell()` access (it is a child of `ShellProvider`) without modifying `ShellProvider`'s state shape. The palette renders as `position: fixed`, so it does not affect the grid layout.

3. **Separate `useKeyboardShortcuts.ts` hook.** Keyboard listening logic is extracted into its own file to keep `CommandPalette.tsx` focused on rendering. The hook accepts stable callbacks for `onOpen`, `onClose`, `toggleContextPanel`, `toggleRightPanel`, and `onNavigate`.

4. **G-sequence implemented via `awaitingSequence` state + 1s timeout.** On `g` keypress (not in input, palette closed), `awaitingSequence` becomes `true` and a 1s timeout is set. The next keypress (d/c/p/r) completes the navigation; any other key or timeout cancels. Tests fire both keys synchronously so the timeout never expires before the second key lands.

5. **Input guard: `isNonPaletteInput(paletteInputRef.current)`.** Checks `document.activeElement.tagName === "INPUT" | "TEXTAREA" | isContentEditable` AND `el !== paletteInputRef.current`. Ctrl+K/Cmd+K is blocked when any non-palette input is focused. All other shortcuts (Ctrl+\\, Ctrl+P, G-sequence) are fully blocked when any input is focused.

6. **`app-shell.test.tsx` mock extended with `useRouter`.** `CommandPalette` calls `useRouter()` from `next/navigation`. The existing test only mocked `usePathname`. Added `useRouter: () => ({ push: vi.fn() })` to the mock.

Files affected:

- `frontend/src/components/commands/commands.ts` — new; 10 command definitions (8 navigate, 2 shell)
- `frontend/src/components/commands/useKeyboardShortcuts.ts` — new; global keydown hook, G-sequence state
- `frontend/src/components/commands/CommandPalette.tsx` — new; modal overlay, search input, filtered list, shortcut badges
- `frontend/src/components/layout/AppShell.tsx` — added `<CommandPalette />` inside `ShellGrid`
- `frontend/tests/command-palette.test.tsx` — new; 23 tests
- `frontend/tests/app-shell.test.tsx` — added `useRouter` to `next/navigation` mock
- `docs/ai/ACTIVE_CONTEXT.md` — updated
- `docs/ai/DECISION_LOG.md` — updated
- `docs/ai/CURRENT_MILESTONE.md` — updated to M7 complete

Risk: Low. The palette renders null when closed — no layout or performance impact on the existing shell. Ctrl+P conflicts with the browser Print shortcut; `preventDefault()` works inside the app frame but cannot suppress browser-level print dialogs in all contexts. Ctrl+\\ is nonstandard and unambiguous. No backend API calls, no new dependencies, no mock data.

Outcome: Lint, build, and all 154 tests (19 files) pass. The Genesis app shell now has a global command palette (Ctrl+K/Cmd+K), G-sequence route shortcuts (G D/C/P/R), and direct shell panel shortcuts (Ctrl+\\ / Ctrl+P). Static navigation only — no fuzzy backend search, no invented endpoints.

## 2026-06-30 01:05 +05:30

Decision: Replace the legacy dashboard page with a `ControlPlaneHome` component that positions Genesis as a Specification Compiler control plane, not a chatbot or live-compilation panel.

Key decisions within M6:

1. **Remove SpecEditor and ExecutionStatusPanel from the dashboard.** These belong exclusively at `/compiler`. Keeping them on the dashboard created the false impression that the dashboard is the live compilation entry point.

2. **Remove `useSSE("*")` global subscription from the dashboard.** Without a live compilation workflow on the dashboard, there is no need to listen for server-sent events. The user is redirected to the Run detail page after compile (via CompilerWorkspace CTA), so the dashboard does not need to auto-refresh.

3. **Retain the stats strip.** Total Projects, Active Builds, Failed, and Deployed counts are derived from real backend project data via `useProjects()`. These are accurate live numbers, not invented metrics.

4. **Cap the Recent Projects grid at 6 cards.** The full project list is available at `/projects`. The dashboard is a control plane overview, not a full project manager.

5. **Use the existing adapter (`toProjectViewModel`) for card data.** Project card links use `backendProjectId` and `run.id` (which are identical under the current adapter identity rule), not URL-derived or invented IDs.

6. **Root `/` page redesigned** to match the compiler control plane tone: design tokens throughout (no hardcoded slate), "Specification Compiler" identity, "Open Compiler" primary CTA → `/compiler`, "View Projects" secondary CTA → `/projects`.

7. **`StatusBadge` renders title-case labels** (e.g., "Failed" for FAILED status). This caused a test collision when `getByText("Failed")` found both the stat tile label and the StatusBadge on a FAILED project card. Fixed with `getAllByText("Failed").length >= 1` assertion.

Files affected:

- `frontend/src/components/dashboard/ControlPlaneHome.tsx` — new; StatsStrip, RecentProjectsGrid, HeaderActions, RouteScaffold wrapper
- `frontend/src/app/dashboard/page.tsx` — replaced with single import of ControlPlaneHome; removed SpecEditor, ExecutionStatusPanel, useSSE, handleRunCompiler, handleValidateSpec, all slate classes
- `frontend/src/app/page.tsx` — redesigned landing page; design tokens; compiler control plane identity
- `frontend/tests/control-plane-home.test.tsx` — new; 19 tests
- `docs/ai/ACTIVE_CONTEXT.md` — updated
- `docs/ai/DECISION_LOG.md` — updated
- `docs/ai/CURRENT_MILESTONE.md` — updated to M6 complete

Risk: Low. The `/dashboard` route continues to exist. Legacy sub-routes (`/dashboard/project/[id]` etc.) are untouched. The adapter and all frozen hooks are used without modification.

Outcome: Lint, build, and all 131 tests (18 files) pass. The Genesis dashboard is now a compiler control plane: heading "Genesis Engine", subtitle "Specification Compiler Platform", stats strip from real data, adapter-backed project cards, honest Run language, "Open Compiler" primary CTA throughout.

## 2026-06-29 23:55 +05:30

Decision: QA pass (M5.6) found two issues to fix across the Run detail suite; all others confirmed clean.

Issue 1 — Accessibility: `RunOverview.SurfaceCard` rendered 5 links with identical visible text "Open" and no `aria-label`. Added `aria-label={`Open ${surface.label}`}` to give each link a unique accessible name ("Open Compiler", "Open Planning Report", "Open Architecture", "Open Workspace", "Open Artifacts"). Requires `run-overview.test.tsx` line 153 to query by the new descriptive name instead of `"Open"`.

Issue 2 — Visual consistency: `RunArchitectureGraph.GraphPanel.CardTitle` used `className="text-sm font-semibold capitalize"` while every other `CardTitle` override across the Run suite uses `text-base`. Changed to `className="text-base capitalize"`.

All other QA findings confirmed clean: no hardcoded slate colors, no fake data, no invented IDs or endpoints, no fabricated run history. All "Open Compiler" CTAs use an identical class string. All LimitedState unavailable copy follows the same pattern. All backend calls use `backendProjectId`. Responsive breakpoints present throughout.

Files affected:

- `frontend/src/components/run/RunOverview.tsx` — added `aria-label` to surface card link
- `frontend/src/components/run/RunArchitectureGraph.tsx` — fixed CardTitle text-size class
- `frontend/tests/run-overview.test.tsx` — updated link query to use descriptive accessible names
- `docs/ai/ACTIVE_CONTEXT.md` — updated
- `docs/ai/DECISION_LOG.md` — updated
- `docs/ai/CURRENT_MILESTONE.md` — updated to M5.6 complete

Risk: Low. Both changes are purely additive/corrective with no layout impact. Test count remains 112. No new features, no backend changes.

Outcome: Lint, build, and all 112 tests pass. The Run detail suite is now fully QA-passed.

## 2026-06-29 23:30 +05:30

Decision: Create `RunArtifacts.tsx` as a new pure component rather than reusing `DeploymentPanel` from the legacy dashboard.

Reason: `DeploymentPanel` contains a hardcoded list of 8 invented artifact filenames (`deployment_bundle.zip`, `api_graph.json`, `planning_report.json`, `execution_trace.json`, etc.) that it renders unconditionally regardless of what the backend returns. Reusing it would display fabricated artifact entries — a violation of the no-mock-data constraint. `RunArtifacts` shows only files present in `run.artifactBundle.files` from the adapter, which maps real `artifact_files` records from the backend project response.

Files affected:

- `frontend/src/components/run/RunArtifacts.tsx` — new; StatusBanner (build_status), HashesCard (workspace + deployment SHA-256), ManifestCard (metadata + plugin versions + graph hashes), ArtifactFilesCard (real files with download links, or empty message)
- `frontend/src/components/routes/RunRouteScaffold.tsx` — replaced old artifacts LimitedState with `<RunArtifacts run={run} />`; removed final Card-family imports (no longer used anywhere in this file)
- `frontend/tests/run-artifacts.test.tsx` — new; 17 tests using `@testing-library/react` (`fireEvent` not needed — pure component); `getByText("SUCCESS")` ambiguity fixed with `getAllByText` after "SUCCESS" was found in StatusBadge, StatusBanner, and ManifestCard simultaneously
- `docs/ai/ACTIVE_CONTEXT.md` — updated
- `docs/ai/DECISION_LOG.md` — updated
- `docs/ai/CURRENT_MILESTONE.md` — updated to M5.5 complete

Risk: Low. `RunArtifacts` is a pure component (no hooks). `buildArtifactUrl` uses `process.env.NEXT_PUBLIC_API_URL` with a localhost fallback — the same pattern used elsewhere in the frontend for direct API URLs. Download links are `<a href download>` anchors, not fetch calls, so no CORS or auth considerations apply at render time.

Outcome: Lint, build, and all 112 tests (17 files) pass. The `/projects/[id]/runs/[runId]/artifacts` surface renders the real adapter-sourced artifact bundle: cryptographic hashes, full deployment manifest, plugin versions, graph hashes, and real download links per file. No backend, API, auth, or compiler behavior was changed. No mock data or invented endpoints were added.

## 2026-06-29 16:48 +05:30

Decision: Use semantic CSS variables as the design token source of truth, with Tailwind consuming those variables.

Reason: The specification calls for a stable enterprise design foundation. Semantic tokens allow future route and shell work to use product concepts such as surface, border, text, accent, status, elevation, and animation without coupling screens to raw colors.

Files affected:

- `frontend/src/styles/tokens.css`
- `frontend/src/app/globals.css`
- `frontend/tailwind.config.ts`

Risk: Existing prototype screens may visually shift because Tailwind aliases now resolve through the token system.

## 2026-06-29 16:48 +05:30

Decision: Integrate Inter for UI text and JetBrains Mono for code and technical values through `next/font/google`.

Reason: The v3.0 frontend needs a consistent product typography foundation before app shell and Run screens are built.

Files affected:

- `frontend/src/app/layout.tsx`
- `frontend/src/app/globals.css`
- `frontend/tailwind.config.ts`

Risk: Font fetching required network access during build. It succeeded after escalation, but fresh environments may need dependency and network availability.

## 2026-06-29 16:48 +05:30

Decision: Delete duplicate `frontend/tailwind.config.js` and keep `frontend/tailwind.config.ts`.

Reason: Duplicate Tailwind configs create ambiguity about which token configuration is authoritative.

Files affected:

- `frontend/tailwind.config.js`
- `frontend/tailwind.config.ts`

Risk: Tooling that explicitly referenced the `.js` config would need to be updated, but the Next/Tailwind setup should resolve the TypeScript config.

## 2026-06-29 16:48 +05:30

Decision: Add or improve only low-level shared UI primitives during Milestone 1.

Reason: Milestone 1 scope was design system foundation only. Route migration, `/dashboard` migration, app shell architecture, and compiler/run screen redesign are not approved yet.

Files affected:

- `frontend/src/components/ui/button.tsx`
- `frontend/src/components/ui/card.tsx`
- `frontend/src/components/ui/badge.tsx`
- `frontend/src/components/ui/status-badge.tsx`
- `frontend/src/components/ui/input.tsx`
- `frontend/src/components/ui/empty-state.tsx`
- `frontend/src/components/ui/skeleton.tsx`
- `frontend/src/components/ui/spinner.tsx`

Risk: Primitives must remain compatible with existing prototype usage until later migration milestones.

## 2026-06-29 16:48 +05:30

Decision: Document the Run-centered adapter requirement before implementing route migration.

Reason: Current backend data is project/workspace-shaped, while the target frontend UI is Run-centered. A frontend-only adapter layer is needed to avoid inventing backend APIs or mock Run data.

Files affected:

- `docs/FrontendAdapterDesign.md`
- `docs/ai/FRONTEND_ADAPTER_PLAN.md`

Risk: If route work begins before the adapter contract is settled, the frontend may hardcode incorrect backend assumptions.

## 2026-06-29 16:56 +05:30

Decision: Keep future Genesis adapter/domain files out of legacy dashboard route folders.

Reason: The Run-centered model should be route-neutral so it can support the future Organization -> Project -> Run architecture without being coupled to `/dashboard`.

Files affected:

- `docs/ai/FRONTEND_ADAPTER_PLAN.md`
- `docs/ai/ACTIVE_CONTEXT.md`

Risk: Milestone 1.5 must still avoid backend API invention and must preserve raw backend project/workspace IDs for existing calls.

## 2026-06-29 16:56 +05:30

Decision: Complete status token coverage with semantic foreground tokens and keep primitive refs aligned with rendered elements.

Reason: Destructive/status UI should consume semantic tokens instead of raw color utilities, and shared primitive types should remain reliable for downstream route work.

Files affected:

- `frontend/src/styles/tokens.css`
- `frontend/tailwind.config.ts`
- `frontend/src/components/ui/button.tsx`
- `frontend/src/components/ui/card.tsx`

Risk: Low. Existing visual output may shift slightly for destructive buttons because text color now resolves through `--error-foreground`.

## 2026-06-29 17:03 +05:30

Decision: Add an explicit Next ESLint config, lock validation tool dependencies, and keep Vitest from collecting Playwright e2e specs.

Reason: `npm run lint` was interactive because no ESLint config existed. `@playwright/test` and `vitest` were referenced by scripts and config files but unavailable locally because the lockfile and install state did not include those declared dev dependencies. Vitest was also collecting `e2e/workflow.spec.ts`, which belongs to Playwright.

Files affected:

- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/.eslintrc.json`
- `frontend/vitest.config.ts`
- `docs/ai/ACTIVE_CONTEXT.md`
- `docs/ai/DECISION_LOG.md`

Risk: Dependency installation may require network access. Playwright browser binaries are separate from the `@playwright/test` package and should not be installed without explicit approval.

Outcome: Validation tooling is now present and non-interactive. Remaining build/test failures are existing product or test correctness issues outside Milestone 1.1 scope.

## 2026-06-29 17:16 +05:30

Decision: Fix the existing frontend build/test baseline without redesigning screens or changing backend contracts.

Reason: The project detail route was passing `projectId` to components whose current contracts require direct report/trace data. Several unit tests were stale against current component props and rendered copy.

Files affected:

- `frontend/src/app/dashboard/project/[id]/page.tsx`
- `frontend/src/app/dashboard/components/PlanningReportViewer.tsx`
- `frontend/tests/DeploymentPanel.test.tsx`
- `frontend/tests/ExecutionTimeline.test.tsx`
- `frontend/tests/GraphInspector.test.tsx`
- `frontend/tests/SpecEditor.test.tsx`
- `frontend/tests/WorkspaceExplorer.test.tsx`
- `frontend/vitest.config.ts`
- `docs/ai/ACTIVE_CONTEXT.md`
- `docs/ai/DECISION_LOG.md`

Risk: Low. The route now renders empty planning/trace states from existing project or telemetry data rather than calling new APIs. Tests now assert current component behavior rather than obsolete props.

Outcome: `npm.cmd run lint`, `npm.cmd run build`, `npm.cmd test`, and `git diff --check` all pass.

## 2026-06-29 17:20 +05:30

Decision: Remove only the invalid local Windows path from `.gitignore`.

Reason: The final `.gitignore` entry `C:\Users\Dinusha Ekanayake\` was an invalid ignore pattern with a dangling backslash. It caused repository tooling such as `rg --files` to report an invalid glob and could create source-control noise.

Files affected:

- `.gitignore`
- `docs/ai/ACTIVE_CONTEXT.md`
- `docs/ai/DECISION_LOG.md`

Risk: Low. The rest of the `.gitignore` diff remains unchanged, so any broader `.gitignore` rewrite still needs separate review if desired.

Outcome: `rg --files` runs without the invalid-glob warning.

## 2026-06-29 17:28 +05:30

Decision: Implement the Run-centered frontend adapter as a route-neutral, frontend-only view-model layer.

Reason: The current backend remains project/workspace-shaped, while the target UI is Run-centered. The adapter gives future UI work stable Run language without changing backend APIs or pretending real Run endpoints exist.

Files affected:

- `frontend/src/lib/genesis/view-models.ts`
- `frontend/src/lib/genesis/capabilities.ts`
- `frontend/src/lib/genesis/adapters.ts`
- `frontend/tests/genesis-adapters.test.ts`
- `docs/ai/ACTIVE_CONTEXT.md`
- `docs/ai/DECISION_LOG.md`

Risk: Low. The adapter is pure and not wired into routes yet. Future UI work must keep backend calls on `backendProjectId` or `backendWorkspaceId` until real backend Run endpoints exist.

Outcome: Adapter tests cover ID preservation, latest-run mapping, capability derivation, missing-field behavior, and display-name fallback. Full frontend validation passes.

## 2026-06-29 17:33 +05:30

Decision: Introduce the Genesis app shell as route-neutral layout infrastructure and wrap only the existing dashboard route group.

Reason: The specification requires a shell organized around a Global Rail, Context Panel, Header, Main Work Surface, and right panel foundation. Wrapping the dashboard layout preserves existing routes while replacing the old fixed flex sidebar with CSS Grid shell architecture.

Files affected:

- `frontend/src/components/layout/ShellProvider.tsx`
- `frontend/src/components/layout/AppShell.tsx`
- `frontend/src/components/layout/GlobalRail.tsx`
- `frontend/src/components/layout/ContextPanel.tsx`
- `frontend/src/components/layout/AppHeader.tsx`
- `frontend/src/components/layout/RightPanel.tsx`
- `frontend/src/components/layout/Breadcrumbs.tsx`
- `frontend/src/app/dashboard/layout.tsx`
- `frontend/tests/app-shell.test.tsx`
- `docs/ai/ACTIVE_CONTEXT.md`
- `docs/ai/DECISION_LOG.md`

Risk: Medium-low. The dashboard content now sits inside a new shell scroll/layout container, so later visual QA should check spacing and overflow in real browsers. Internal dashboard content was not redesigned.

Outcome: Existing routes remain compatible, `/login` stays outside the shell, shell state persists in localStorage, and full frontend validation passes.

## 2026-06-29 17:45 +05:30

Decision: Add target route shells in an `(app)` route group while preserving legacy dashboard routes.

Reason: The Genesis v3 route architecture must exist before deeper product screen migration, but the backend still exposes project/workspace-shaped data and legacy dashboard routes must remain compatible.

Files affected:

- `frontend/src/app/(app)/layout.tsx`
- `frontend/src/app/(app)/projects/page.tsx`
- `frontend/src/app/(app)/projects/[id]/page.tsx`
- `frontend/src/app/(app)/projects/[id]/runs/page.tsx`
- `frontend/src/app/(app)/projects/[id]/runs/[runId]/page.tsx`
- `frontend/src/app/(app)/projects/[id]/runs/[runId]/compiler/page.tsx`
- `frontend/src/app/(app)/projects/[id]/runs/[runId]/architecture/page.tsx`
- `frontend/src/app/(app)/projects/[id]/runs/[runId]/workspace/page.tsx`
- `frontend/src/app/(app)/projects/[id]/runs/[runId]/artifacts/page.tsx`
- `frontend/src/app/(app)/projects/[id]/runs/[runId]/report/page.tsx`
- `frontend/src/app/(app)/runs/page.tsx`
- `frontend/src/app/(app)/compiler/page.tsx`
- `frontend/src/app/(app)/telemetry/page.tsx`
- `frontend/src/app/(app)/team/page.tsx`
- `frontend/src/app/(app)/settings/page.tsx`
- `frontend/src/app/(app)/search/page.tsx`
- `frontend/src/components/routes/RouteScaffold.tsx`
- `frontend/src/components/routes/RunRouteScaffold.tsx`
- `frontend/src/components/layout/GlobalRail.tsx`
- `frontend/src/components/layout/ContextPanel.tsx`
- `frontend/src/lib/genesis/adapters.ts`
- `frontend/src/lib/genesis/capabilities.ts`
- `frontend/tests/route-architecture.test.tsx`
- `frontend/tests/app-shell.test.tsx`
- `docs/ai/ACTIVE_CONTEXT.md`
- `docs/ai/DECISION_LOG.md`

Risk: Medium. New routes are intentionally skeletal and only expose latest-known Run data. Future milestones must avoid treating frontend Run IDs as backend Run endpoints until the backend provides them.

Outcome: Target routes build successfully, shell navigation reaches them, adapter-backed project/run pages render honest limited states, and full frontend validation passes.

## 2026-06-29 21:59 +05:30

Decision: Create `RunWorkspace.tsx` as a new component rather than reusing `WorkspaceExplorer` from the legacy dashboard.

Reason: Three blockers prevent safe reuse. (1) `WorkspaceExplorer` uses Monaco Editor (`@monaco-editor/react`, dynamic SSR-disabled import) — a heavy dependency that requires canvas/DOM mocking in tests and is inconsistent with the `<pre>` blocks used throughout other M5 surfaces. (2) It uses hardcoded slate colors, not design tokens. (3) A `<pre>` block for file content is sufficient for a read-only workspace surface and produces clean, fully testable output. The new component calls the same frozen hooks (`useProjectWorkspace`, `useProjectFile`) with the correct `backendProjectId`.

Additional decision: `run.capabilities.hasWorkspaceFiles` is intentionally not used as a workspace gate. The `GET /genesis/projects/{id}` endpoint does not embed workspace files in its response — they are fetched separately via `GET /genesis/projects/{id}/workspace`. Therefore `hasWorkspaceFiles` is always `false` for standard project records. The workspace surface fetches and shows data when available, and shows an honest unavailable state when the workspace endpoint returns nothing.

Files affected:

- `frontend/src/components/run/RunWorkspace.tsx` — new; file tree with expand/collapse, `<pre>` file preview, LimitedState + Open Compiler link when unavailable
- `frontend/src/components/routes/RunRouteScaffold.tsx` — replaced old workspace LimitedState (which linked to the legacy dashboard) with `<RunWorkspace run={run} />`; added import
- `frontend/tests/run-workspace.test.tsx` — new; 16 tests using `fireEvent`
- `docs/ai/ACTIVE_CONTEXT.md` — updated
- `docs/ai/DECISION_LOG.md` — updated
- `docs/ai/CURRENT_MILESTONE.md` — updated

Risk: Low. `RunWorkspace` uses `useProjectWorkspace` and `useProjectFile` — the same hooks already used by `WorkspaceExplorer` in the legacy dashboard. The backend project ID is always taken from `run.backendProjectId`. The workspace endpoint is read-only (no mutations). One test failure fixed during development: `getByText("README.md")` matched both the file tree button and the file path header code element; fixed with `getAllByText(...).length >= 2` and `getByLabelText`.

Outcome: Lint, build, and all 95 tests pass. The `/projects/[id]/runs/[runId]/workspace` surface is a real workspace browser using the existing backend workspace API. No backend, API, auth, or compiler behavior was changed. No mock data or invented file paths were added.

## 2026-06-29 21:46 +05:30

Decision: Create `RunArchitectureGraph.tsx` as a new pure component rather than reusing `GraphInspector` from the legacy dashboard.

Reason: Three blockers prevent reuse. (1) `GraphInspector` calls `useProjectGraphs(projectId)` — a separate backend request that duplicates the data already provided by the adapter via `run.architectureGraphs`. Making a second backend call from within a Run surface would violate the identity rule (backend calls must use `backendProjectId`, not URL-derived IDs). (2) `GraphInspector` depends on `@xyflow/react` (React Flow), which is an SSR-incompatible dependency using dynamic import, requires canvas/SVG mocking in tests, and is not installed in the test environment. (3) `GraphInspector` uses hardcoded slate dark colors inconsistent with the design token system.

Files affected:

- `frontend/src/components/run/RunArchitectureGraph.tsx` — new; graph selector buttons, collection stats grid (endpoints/pages/components/features/tables counts), raw JSON pre block, unavailable state with Open Compiler link
- `frontend/src/components/routes/RunRouteScaffold.tsx` — replaced old badge-only architecture card with `<RunArchitectureGraph run={run} />`; removed unused `CapabilityBadge` import
- `frontend/tests/run-architecture.test.tsx` — new; 13 tests using `fireEvent` (not `userEvent` — package not installed)
- `docs/ai/ACTIVE_CONTEXT.md` — updated
- `docs/ai/DECISION_LOG.md` — updated
- `docs/ai/CURRENT_MILESTONE.md` — updated

Risk: Low. `RunArchitectureGraph` is a pure component except for `useState` (graph tab selection). The `useState` call is placed unconditionally before the early return guard to satisfy React's Rules of Hooks. All access to `unknown`-typed graph values goes through a safe object check in `deriveGraphStats`. The React Flow dependency is not imported and is not needed.

Outcome: Lint, build, and all 79 tests pass. The `/projects/[id]/runs/[runId]/architecture` surface renders real adapter-sourced graph data: graph-name tabs, known-collection counts, and full raw graph JSON. No backend, API, auth, or compiler behavior was changed. No mock data or invented endpoints were added.

## 2026-06-29 19:44 +05:30

Decision: Create `RunPlanningReport.tsx` as a new pure component rather than reusing `PlanningReportViewer` from the legacy dashboard.

Reason: `PlanningReportViewer` uses hardcoded Tailwind slate/dark color classes (`bg-slate-900`, `border-slate-800`, etc.) that are inconsistent with the design token system established in Milestone 1. A new component allows the planning report surface to use `bg-surface-raised`, `border-border`, `text-success`, `text-[color:var(--error)]`, and the rest of the semantic token set — matching the Run Overview and other M5 surfaces. The legacy component remains unchanged and continues to be used by the dashboard project detail page.

Files affected:

- `frontend/src/components/run/RunPlanningReport.tsx` — new; shows status header, 8-tile metrics grid, optional rule coverage, failed rules, assumptions, rule execution trace with PASS/FAIL/WARN badges, and graph hashes
- `frontend/src/components/routes/RunRouteScaffold.tsx` — replaced minimal 4-field fallthrough card with explicit `report` surface branch using `RunPlanningReport`
- `frontend/tests/run-planning-report.test.tsx` — new; 19 tests covering all sections, unavailable state, optional sections, status badges, and RunRouteScaffold integration
- `docs/ai/ACTIVE_CONTEXT.md` — updated
- `docs/ai/DECISION_LOG.md` — updated
- `docs/ai/CURRENT_MILESTONE.md` — updated

Risk: Low. `RunPlanningReport` is a pure component (no hooks, no API calls). All optional fields (`rule_coverage`, `failed_rules`, `assumptions`, `graph_hashes`) are guarded before rendering. The `rule_coverage` field is typed as optional in `PlanningReport`; a missing `--warning` CSS variable would degrade gracefully to the default text color.

Outcome: Lint, build, and all 66 tests pass. The `/projects/[id]/runs/[runId]/report` surface renders the full backend-sourced planning report — rule validation status, integrity score, planning duration, all 8 metrics, rule execution trace with per-rule PASS/FAIL/WARN status, rule coverage, assumptions, failed rules, and graph hashes. No backend, API, auth, or compiler behavior was changed. No mock data or fake endpoints were added.

## 2026-06-29 19:23 +05:30

Decision: Extract the Run Overview into a dedicated pure component (`RunOverview.tsx`) under `frontend/src/components/run/` rather than keeping it as an inline function inside `RunRouteScaffold.tsx`.

Reason: The overview is now substantial enough to warrant independent structure, testing, and future reuse. As a pure component (no hooks, no API calls), it receives `RunViewModel` directly from the adapter and is trivially testable. Keeping it in RunRouteScaffold would have made the file harder to maintain and impossible to unit-test in isolation.

Files affected:

- `frontend/src/components/run/RunOverview.tsx` — new; shows summary, backend identity, specification, and surface cards
- `frontend/src/components/routes/RunRouteScaffold.tsx` — removed `Overview` and `CapabilitySummary` inline functions; imports `RunOverview`
- `frontend/tests/run-overview.test.tsx` — new; 17 tests
- `docs/ai/ACTIVE_CONTEXT.md` — updated
- `docs/ai/DECISION_LOG.md` — updated
- `docs/ai/CURRENT_MILESTONE.md` — updated to M5.1

Risk: Low. The surface-card links on the overview use `run.backendProjectId` and `run.id` consistently. No backend calls are made from RunOverview. The `RunRouteScaffold` mismatch guard (which intercepts `runId !== projectId` before RunOverview is ever rendered) is tested and unchanged.

Outcome: Lint, build, and all 47 tests pass. The Run Overview is a real, useful, adapter-backed page. The `runId !== backendProjectId` mismatch guard correctly redirects to the latest known Run using only real backend IDs.

## 2026-06-29 19:06 +05:30

Decision: Implement the global `/compiler` page as a real compiler workspace by reusing existing legacy components and hooks directly, without duplication.

Reason: The legacy dashboard already has working `SpecEditor`, `ExecutionStatusPanel`, `GenesisAPI.runCompiler`, `GenesisAPI.validateSpec`, and `useSSE` implementations. Copying or re-implementing them would diverge from the frozen backend API contract and create maintenance risk.

Files affected:

- `frontend/src/components/compiler/CompilerWorkspace.tsx` — new; owns compile state, SSE subscription, completion CTA
- `frontend/src/app/(app)/compiler/page.tsx` — replaced LimitedState with CompilerWorkspace
- `frontend/src/components/routes/RunRouteScaffold.tsx` — compiler surface now shows read-only trace or limited state; links to /compiler for new compilations
- `frontend/tests/compiler.test.tsx` — new; 9 tests for workspace behavior, API dispatch, and run-specific surface
- `frontend/tests/route-architecture.test.tsx` — updated compiler test; CompilerWorkspace mocked so route-architecture file stays focused on route existence
- `docs/ai/ACTIVE_CONTEXT.md` — updated
- `docs/ai/DECISION_LOG.md` — updated
- `docs/ai/CURRENT_MILESTONE.md` — updated to M4

Risk: Medium-low. `SpecEditor` carries a hardcoded DEFAULT_SPEC (`project_id: "demo_project_001"`). This is the user's own spec starting point, not fake backend data. Future milestones may want to remove or make the default editable, but it does not violate the no-mock-data constraint. The completion CTA routes only when `manifest.project_id` is a non-empty string from the real API response; an empty or missing project_id suppresses the link.

Outcome: Lint, build, and all 30 tests pass. The `/compiler` route is the live Genesis Engine compiler workspace. The run-specific compiler surface remains read-only. No backend, API, auth, or compiler behavior was changed.

## 2026-06-29 17:50 +05:30

Decision: Harden route/shell navigation without adding product functionality.

Reason: QA found that the header used a hardcoded `API Connected` label that could imply fake backend status, and Context Panel navigation did not expose the top-level `/runs` route.

Files affected:

- `frontend/src/components/layout/AppHeader.tsx`
- `frontend/src/components/layout/ContextPanel.tsx`
- `frontend/tests/app-shell.test.tsx`
- `docs/ai/ACTIVE_CONTEXT.md`
- `docs/ai/DECISION_LOG.md`

Risk: Low. Changes are limited to shell labels/navigation and test coverage. No routes, backend calls, API contracts, compiler behavior, or dashboard internals were changed.

Outcome: Header now shows neutral `Shell Ready`, `/runs` is present in the Context Panel, shell tests cover active Runs navigation and right panel visibility, and full frontend validation passes.
