# Decision Log

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
