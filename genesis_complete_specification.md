# Genesis Engine
# Complete Product Design Specification
### All Five Phases — Principal Design Review

**Author:** Principal Product Designer / Senior Frontend Architect  
**Version:** 3.0 — Definitive  
**Status:** Awaiting Approval Before Implementation  
**Scope:** Frontend architecture and UX only. Backend, APIs, auth, and compiler are preserved entirely.

---

> The standard is not "good for an internal tool."  
> The standard is Linear. Vercel. Cursor. GitHub. Datadog.  
> That is the bar. Everything below it is a bug.

---

# PHASE 1 — Product UX Audit

## Scoring Methodology

Each dimension is scored 0–10:
- **0–3:** Broken or absent. Would prevent a commercial launch.
- **4–5:** Functional but unacceptable for a professional product.
- **6–7:** Adequate. Meets minimum standard.
- **8–10:** Production-grade. Comparable to the reference products.

---

## 1.1 Information Architecture — Score: 3/10

**The fundamental problem:** Genesis has *one* page doing *three* jobs.

The dashboard (`/dashboard`) simultaneously presents:
1. A spec authoring environment (SpecEditor with Monaco)
2. A live compilation monitor (ExecutionStatusPanel)
3. A historical project browser (Recent Workspaces table)

These represent three distinct user intentions — **Create**, **Monitor**, **Browse** — each with different mental models, different data requirements, and different interaction patterns. Collapsing them onto one page forces the user to context-switch mentally while the UI never changes.

Evidence in code (`dashboard/page.tsx`, lines 96–111):
```tsx
<div className="grid grid-cols-1 lg:grid-cols-2 gap-4 h-[500px]">
  <SpecEditor ... />
  <ExecutionStatusPanel ... />   {/* ← monitoring next to authoring */}
</div>
```

The object model is also wrong. The primary navigable object is a "workspace" (identified by its raw database ID slug, e.g., `demo_project_001`). This is technically correct but experientially wrong. Users think in terms of **runs** — compilation attempts with a clear result. The project ID `demo_project_001` appears as the table's primary column, not a human-readable project name.

**What a commercial platform does:** Linear's object model is `Workspace → Team → Project → Issue`. Every navigation level corresponds to a real mental model. Vercel's is `Team → Project → Deployment`. Genesis needs `Organization → Project → Run`.

**What needs to change:**
- Separate `/compiler` for authoring
- Separate `/runs` for monitoring
- Object model reoriented around `Run` as the atomic unit

---

## 1.2 Navigation — Score: 2/10

The sidebar in `dashboard/layout.tsx` contains five links. Reading the code:

```tsx
<Link href="/dashboard">Dashboard</Link>     // active
<Link href="/dashboard">Projects</Link>      // dead — same destination
<Link href="/dashboard">Execution Logs</Link>// dead — same destination
<Link href="/dashboard">Deployment</Link>    // dead — same destination
```

Four out of five navigation items are dead. They link to the same page as if they will be implemented later. They were not. This is the most immediate signal that the product is a prototype — a skeleton navigation that was never completed.

There is no active-state detection using the router. The `Dashboard` link is hardcoded with `bg-blue-500/10 text-blue-400` regardless of which route is active. Every other page would show no active nav item.

There is no mobile navigation. The sidebar is `hidden md:flex` with zero fallback. On any screen narrower than `md` (768px), the entire navigation structure disappears.

There is no breadcrumb system at the application level, only an `← Back to Workspaces` text link on the project detail page.

The workspace switcher ("Default Organization") is a static, non-interactive string.

**Score justification:** A navigation system where 80% of links are broken cannot score above 2. This is not a minor issue — it is the most visible indicator of product incompleteness.

---

## 1.3 Layout Hierarchy — Score: 4/10

The layout structure is correct in its bones — sidebar + header + content — but it fails in its execution.

**Fixed height disease:** The spec editor / status panel grid uses `h-[500px]`. The workspace explorer uses `h-[600px]`. The graph inspector uses `h-[600px]`. These hardcoded heights cause layout problems at every viewport that isn't exactly the design target. Content clips. Scrollbars appear in unexpected places. The UI fights the browser.

**No layout intelligence:** The `max-w-7xl mx-auto` container is applied to the entire dashboard without regard for content type. The Monaco editor inside the SpecEditor has an `h-full` that is constrained by a parent with a fixed height of 500px. The result is an editor that cannot adapt to the user's viewport.

**The Compiler Console panel** on the dashboard shows the execution status of the *most recently submitted* project only, tracked by `activeProjectId` state. If the user navigates away and back, this state is lost. The panel is stateless from the user's perspective.

**The Project Detail page** presents six tabs in a horizontal row. Six tabs is borderline acceptable; the problem is the tab content area has `min-h-[600px]` — another hardcoded height. The tab that holds the Workspace Explorer and Graph Inspector will render correctly on large screens, but the layout does not respond to viewport changes.

---

## 1.4 Cognitive Load — Score: 3/10

The dashboard asks the user to do too many things at once. When a user opens the dashboard with an active project, they see:
- A Monaco editor with JSON they may or may not want to edit
- An execution status panel that may or may not be relevant to their current goal
- A table of past projects

This creates three simultaneous focal points. The eye has no primary landing target. There is no visual hierarchy that guides attention.

The Project Detail page compounds this with six undifferentiated tabs. **Overview**, **Workspace Explorer**, **Planning Report**, **Graph Inspector**, **Execution Trace**, **Deployment Bundle** — these tabs are presented with identical visual weight, forcing the user to read all six labels to find what they want.

The **SpecEditor** toolbar shows the keyboard shortcut `(Ctrl+Enter)` as hidden text (`hidden xl:inline`) — the shortcut is invisible on most screens. Keyboard shortcuts that are invisible are not keyboard shortcuts.

---

## 1.5 Visual Hierarchy — Score: 3/10

**Typography:** The `globals.css` file specifies `font-family: Arial, Helvetica, sans-serif`. Arial is the most recognizable "unstyled" font on the web. No commercial developer platform ships with Arial as the primary typeface.

**Color palette:** The entire application uses Tailwind's built-in `slate-*` scale with `blue-500` as the sole accent. `#3B82F6` is the most recognized "Tailwind blue" on the internet. It immediately reads as "made with a Tailwind template." It has no distinctive personality.

**Elevation:** Every card and panel uses `bg-slate-900 border border-slate-800 rounded-xl`. There is one elevation level across the entire application. Dropdown menus, modals, inline content panels — all the same visual depth. There is no elevation hierarchy.

**Status indicators:** The status badge on the project table uses color + text, which is good. But the `graph_integrity_score` column shows a raw number (`84`) with no context: no unit, no range, no visual encoding (no color, no bar). A number in isolation communicates nothing.

---

## 1.6 Empty States — Score: 4/10

| Empty State Location | Current Implementation | Score |
|---|---|---|
| Project list (no projects) | `"No compiled workspaces found."` — one sentence, no icon, no CTA | 2/10 |
| ExecutionStatusPanel (no project) | Icon + heading + body — the best empty state in the app | 7/10 |
| GraphInspector (no graphs) | Icon + question `"Has the compiler run yet?"` | 5/10 |
| WorkspaceExplorer (no file selected) | `"Select a file to preview"` — functional but minimal | 5/10 |
| DeploymentPanel (no manifest) | Icon + heading + body — acceptable | 6/10 |

The best empty state in the application (`ExecutionStatusPanel` before a run) demonstrates that the team knows how to do this correctly. The pattern is not consistently applied.

A question mark in an empty state (`"Has the compiler run yet?"`) is a design smell. The system knows whether the compiler has run. The empty state should state the fact, not ask the user.

---

## 1.7 Error States — Score: 4/10

The backend offline error is displayed as an inline div on the dashboard page, between the stat cards and the spec editor. This is the worst possible location for a system-level error — it disappears if the user scrolls.

The `WorkspaceExplorer` error state is:
```tsx
<div className="text-red-400 p-8 text-center bg-slate-900 rounded-lg">
  Error loading workspace
</div>
```
No error code. No retry button. No explanation. No navigation option. This is a dead end.

Authentication errors are handled via `useEffect` watching the error state, routing to `/login` if `error.status === 401`. This is functionally correct but creates a jarring redirect without any explanation to the user about why they were redirected.

There is no global error boundary at the route level — only one at the application root in `providers.tsx`. A single component failure propagates to the global error boundary, taking down the entire application.

---

## 1.8 Mobile Behavior — Score: 1/10

The sidebar disappears entirely at < 768px (`hidden md:flex`). There is no mobile navigation replacement — no hamburger menu, no bottom nav, no drawer.

At mobile widths, the user sees:
- The header bar (partially visible, may overflow)
- The main content area with no navigation context

The application is non-functional on mobile. This would be acceptable if it were intentional and documented. It is neither — the sidebar simply hides and nothing replaces it.

The fixed heights (`h-[500px]`, `h-[600px]`) cause content overflow at every breakpoint below desktop.

---

## 1.9 Typography — Score: 2/10

```css
/* globals.css line 24 */
font-family: Arial, Helvetica, sans-serif;
```

This is the only type-related CSS in the global stylesheet. There is no type scale. There are no heading size tokens. There is no distinction between different levels of text hierarchy beyond Tailwind utility classes used inconsistently across components.

The Monaco editor correctly uses `JetBrains Mono` via its options object. The surrounding UI uses Arial. This creates an immediate and jarring font mismatch within the same component.

Tailwind utility classes like `text-2xl font-bold`, `text-base`, `text-sm`, and `text-xs` appear without a governing type scale. Each component author applies their own judgment, resulting in inconsistent heading sizes across pages.

---

## 1.10 Color System — Score: 3/10

The `globals.css` defines four CSS variables:
```css
--background: #ffffff;
--foreground: #0f172a;
--primary: #2563eb;
--primary-foreground: #ffffff;
```

Four variables is not a design system. It is a theme hint.

Every color decision in every component is made using Tailwind utility classes (`text-slate-400`, `bg-blue-500/10`, `border-emerald-500/20`) — these are not tokens, they are references to Tailwind's color scale. There is no semantic layer. If the product's brand color changes, every file must be edited individually.

The `dark:` prefix appears in `PlanningReportViewer.tsx` (`dark:bg-slate-900`, `dark:text-emerald-300`) but dark mode is handled by system preference via `globals.css` media query — not by `next-themes` which is installed but configured for the `system` default. This creates a mixed dark mode implementation where some components are explicitly dark-mode-aware and others are not.

---

## 1.11 Component Consistency — Score: 4/10

There are two UI components in `src/components/ui/` — `button.tsx` and `card.tsx`. These appear unused in the actual application. Every page builds its own ad-hoc components using inline Tailwind.

Component patterns that appear in multiple files without abstraction:
- Status badge: recreated in `dashboard/page.tsx`, `project/[id]/page.tsx`, `ExecutionStatusPanel.tsx`
- Loading spinner: inline `<Loader2 className="animate-spin">` in 6+ locations
- Empty state: different pattern in every component that needs one
- Card container: `bg-slate-900 border border-slate-800 rounded-xl` written inline across 15+ instances

The Tailwind config exists in two files: `tailwind.config.js` AND `tailwind.config.ts`. Duplicate configuration creates unpredictable behavior and signals a lack of project organization.

---

## 1.12 Developer Workflow — Score: 4/10

The primary compiler workflow requires:
1. Navigate to `/dashboard`
2. Find the Monaco editor (below the fold on smaller screens)
3. Manually type or paste a JSON spec (there is no template system or pre-loading)
4. Click "Run Compiler" or press `Ctrl+Enter`
5. Watch the right panel update
6. Manually find the new project in the table
7. Click "View Details"

Seven steps to compile and view results. The competitive standard (Vercel) is: push to git → view deployment. One trigger, one destination. Genesis needs to reduce its primary workflow to three steps: edit spec → compile → navigate to result (auto-redirect).

The SpecEditor has no project context. It doesn't know which project it's compiling for. Every compilation creates a new project. There is no concept of "re-running the last compilation for this project."

---

## 1.13 Accessibility — Score: 5/10

**Present and correct:**
- Skip to main content link
- `role="tablist"` and `role="tab"` on project detail tabs
- `aria-live="polite"` on the status badge
- `focus-visible:ring-2` focus rings on some elements

**Missing or broken:**
- Icon-only download buttons in `DeploymentPanel` have no `aria-label`
- Most buttons use `focus:outline-none` without a replacement ring
- The Monaco editor instances are not in the natural tab order
- The `FileTree` component in `WorkspaceExplorer` has no keyboard navigation (no arrow key support, no `role="tree"` or `role="treeitem"`)
- The `ReactFlow` graph canvas has no keyboard navigation
- Color is used as the only status indicator in some contexts (the stats table without icon fallback)

The accessibility foundation is better than most prototype applications, but incomplete for a commercial product.

---

## 1.14 Discoverability — Score: 2/10

There is no command palette. The `⌘K` interface is the most discoverable power-user feature in modern developer tools. Its absence is immediately felt by any user familiar with Linear, Vercel, or VS Code.

There is no global search.

Keyboard shortcuts exist in Monaco (`Ctrl+S`, `Ctrl+Enter`) but are displayed as `hidden xl:inline` — invisible to 90% of users. The Format button has no icon. The Validate button has a checkmark icon but no tooltip.

There is no onboarding flow for new users. The dashboard with a pre-filled Monaco editor and an empty project table gives no guidance on what to do next.

There is no documentation link anywhere in the UI.

---

## 1.15 Scalability — Score: 3/10

The `useSSE("*")` global wildcard subscription invalidates all project queries on every SSE event. With 5 projects, this is invisible. With 50 projects, every SSE event triggers a full list refetch. With 500, it becomes a performance problem.

The project table has no pagination. All projects load at once. There is no search or filter.

The navigation sidebar has no concept of project pinning, grouping, or favorites. At 20+ projects, the sidebar becomes a long scrolling list with no organization.

There is no concept of workspaces, organizations, or teams. Single-tenant by design — fine for a prototype, unacceptable for enterprise.

---

## Audit Summary

| Dimension | Score | Grade |
|---|---|---|
| Information Architecture | 3/10 | F |
| Navigation | 2/10 | F |
| Layout Hierarchy | 4/10 | D |
| Cognitive Load | 3/10 | F |
| Visual Hierarchy | 3/10 | F |
| Empty States | 4/10 | D |
| Error States | 4/10 | D |
| Mobile Behavior | 1/10 | F |
| Typography | 2/10 | F |
| Color System | 3/10 | F |
| Component Consistency | 4/10 | D |
| Developer Workflow | 4/10 | D |
| Accessibility | 5/10 | C |
| Discoverability | 2/10 | F |
| Scalability | 3/10 | F |
| **TOTAL** | **47/150** | **F — Prototype Grade** |

**Verdict:** The application has a solid backend, good data architecture, and a functional React Query + SSE data layer. The frontend is a prototype. It would not pass a design review at any commercial SaaS company. The gap between the current state and the target is significant but entirely addressable through systematic redesign.

---

---

# PHASE 2 — Product Redesign

## The Central Mental Model

Before designing a single screen, we must define the mental model the product creates in the user's mind.

**Current mental model:** "I have a dashboard where I can run the compiler."

**Target mental model:** "Genesis Engine is a compilation platform. I describe what I want to build in a specification. Genesis compiles it through a multi-agent pipeline. The output is a verified, deployable artifact. I can inspect every step of that compilation in complete detail."

The product's vocabulary changes accordingly:

| Old Term | New Term | Reason |
|---|---|---|
| "Workspace" | "Run" | A run is a compilation attempt. It has a result. It is the user's primary concern. |
| "Control Plane" | "Genesis Engine" | No jargon. The product name is the product name. |
| "Spec Editor" | "Compiler Console" | Positions it as a professional tool, not a text area |
| "Deployment Panel" | "Artifact Manager" | Artifacts are the output; deployment is what happens after |

## The Three Primary Workflows

Every design decision is justified by how it serves one of these three workflows.

**Workflow A: Compile**
> "I have a specification. I want to compile it and get an artifact."

Steps: Open Compiler → Write or load spec → Submit → Monitor live → Navigate to result

This is the most frequent action for active users. It must be the shortest possible path.

**Workflow B: Inspect**
> "A compilation finished. I want to understand what was built."

Steps: Open run → View architecture graph → Browse workspace → Download artifacts

This is the second most frequent action. It requires rich, explorable detail views.

**Workflow C: Diagnose**
> "A compilation failed. I need to understand why and fix it."

Steps: Open failed run → View compilation trace → Read planning report → Identify failed rule → Fix spec → Recompile

This workflow is less frequent but has the highest emotional stakes. Error states and diagnostic UX must be excellent.

## Navigation Model

### The Hierarchy

Genesis uses a three-level navigation hierarchy:

```
Level 0 — Global
  Organization overview, settings, team, telemetry

Level 1 — Project
  All runs for a project, project settings, spec library

Level 2 — Run
  All views into a single compilation run
```

### The Three-Zone Layout

```
┌────────────────────────────────────────────────────────────────────────────────┐
│  [48px Global Rail]  │  [240px Context Panel]  │  [Header: 52px]              │
│                      │                          │─────────────────────────────  │
│  Always visible      │  Collapses to 0px        │  [Primary Work Surface]      │
│  Icon rail only      │  when not needed         │                              │
│                      │                          │                              │
│                      │                          │                [Right Panel] │
│                      │                          │                [0 – 380px]   │
└────────────────────────────────────────────────────────────────────────────────┘
```

**Zone 1 — Global Rail (48px, always visible):**
Icons only. Eight items maximum. The leftmost anchor of the interface. Never hides. Never changes based on context.

**Zone 2 — Context Panel (0–240px, collapsible):**
Changes its content based on which global rail item is active. When "Projects" is active: shows project list. When a project is open: shows project navigation. When a run is open: shows run navigation. This is the spatial hierarchy navigator — it tells you where you are and what's around you.

**Zone 3 — Primary Work Surface:**
The main content area. Router outlet. Full height, scrollable internally.

**Zone 4 — Contextual Right Panel (0–380px, dockable):**
Persistent. Changes content based on main view. For Compiler: live agent output. For Architecture: node details. For Workspace: file metadata. Not a feature — a viewport into the current context.

### Why This Navigation Model

The current sidebar has dead links because the team built navigation without building destinations. The new navigation model ties directly to the object model — every link in the context panel corresponds to a real, navigable object.

The context panel's spatial transformation (changing content based on depth in the hierarchy) is borrowed from Linear's left panel pattern and GitHub's sidebar behavior. The user learns the navigation through spatial consistency: they always know that the context panel shows "what's near me in the hierarchy."

## Workspace Model

A **workspace** in the new model is a UI layout state, not a database object. When you open a run and arrange your panels (graph open, right panel showing node details), that is your workspace. It is persisted per-user.

This separates the database concept (Run) from the UI concept (Workspace), which is cleaner and more aligned with how tools like Figma, VS Code, and Linear manage UI state.

## Project Lifecycle State Machine

```
                              ┌──────────────────────────────────────────────┐
                              ↓                                              │
[NO_RUNS] → submit spec → [QUEUED] → [PLANNING] → [VALIDATING] → [GENERATING] → [PACKAGING] → [SUCCESS]
                                            │              │            │                      ↙
                                            └──────────────┴────────────┴──────→ [FAILED] ───┘
                                                                                    │
                                                                          [can retry with same
                                                                           or modified spec]
```

**State communication is tri-channel:** Color + Icon + Motion. Never color alone.

| State | Color Token | Icon | Motion |
|---|---|---|---|
| NO_RUNS | `--text-tertiary` | `Clock` outline | None |
| QUEUED | `--warning` | `Clock` filled | Static |
| PLANNING | `--accent` | `Brain` | Slow pulse ring |
| VALIDATING | `--accent` | `Shield` | Slow pulse ring |
| GENERATING | `--accent` | `Cpu` | Fast pulse ring |
| PACKAGING | `--accent` | `Package` | Slow pulse ring |
| SUCCESS | `--success` | `CheckCircle2` | None (static) |
| FAILED | `--error` | `XCircle` | None (static) |

## Compiler Workflow

The compiler workflow is redesigned as a **three-act experience**:

**Act 1: Specification** (`/compiler`)
The user writes, loads, or modifies a specification. The spec editor is the primary focus — Monaco, full height, with a status bar at the bottom. The right panel is empty ("Ready to compile").

**Act 2: Compilation** (right panel, live)
On submission, the right panel shows live compilation output. The main editor area does not change — the user can continue editing the next spec while this one compiles. The right panel shows phase blocks (Warp-inspired collapsible sections per phase) with live event streaming.

**Act 3: Result** (auto-navigate)
On completion, a toast appears: "Compilation complete — E-Commerce Platform (14.2s)". Clicking the toast or the "View Run →" button in the right panel navigates to the Run Overview. The right panel persists the completion state until the next compilation is triggered.

**Why this works:** The current design forces the user to stop and watch the compiler run because the status panel is on the dashboard. The new design allows the user to queue multiple compilations or continue authoring specs while a compilation runs in the right panel background.

## Keyboard Shortcut Philosophy

Shortcuts are organized in three tiers:

**Universal (any context):**
`⌘K` — Command Palette  
`⌘\` — Toggle context panel  
`⌘P` — Toggle right panel  
`Escape` — Close modal/palette/panel/dropdown

**Navigation (not in input):**
`G D` — Go to Dashboard  
`G P` — Go to Projects  
`G C` — Go to Compiler  
`G R` — Go to Runs  

**Contextual (page-specific):**
`1`–`6` — Switch run tabs (on any run page)  
`R` — Re-run (on run detail pages)  
`D` — Download artifacts  
`F` — Fit graph to screen (on Architecture page)  
`⌘Enter` — Compile (on Compiler page)  
`⌘S` — Validate spec  

All shortcuts are discoverable via:
1. Tooltips on every button that has a shortcut
2. The Command Palette (shortcuts shown right-aligned)  
3. `?` key opens a shortcut reference overlay

---

---

# PHASE 3 — Enterprise Design System

## Design Philosophy

The design system is built on four principles:

**Precision:** Every token has one meaning. Every component has one responsibility. There is no ambiguity.

**Restraint:** The interface serves the content. Decoration is eliminated. Animations communicate, they do not entertain.

**Density:** Information density is a feature for engineering tools. The system maximizes data visibility within comfortable readability bounds.

**Continuity:** Switching between pages never feels like changing contexts. Consistent spatial relationships, consistent component language, consistent typography.

---

## 3.1 Color System

### Why We Replace Tailwind's Default Palette

Tailwind's `slate-*` scale and `blue-500` (`#3B82F6`) are the most recognized "template colors" on the web. Any engineer who has used Tailwind recognizes them in milliseconds. A commercial product must have a distinct visual identity.

The new palette uses:
- **Void Black** as the background family — a blue-tinted dark that reads as "technical precision"
- **Iris** as the primary accent — a blue-violet that reads as "intelligent" rather than "default blue"

### Primitive Color Palette (HSL)

These are raw values. They are never used directly in components — only through semantic tokens.

```
Iris (primary brand):
  iris-50:    hsl(238, 100%, 97%)
  iris-100:   hsl(238, 95%,  93%)
  iris-200:   hsl(238, 90%,  85%)
  iris-300:   hsl(238, 85%,  75%)
  iris-400:   hsl(238, 80%,  68%)
  iris-500:   hsl(238, 75%,  62%)   ← primary accent
  iris-600:   hsl(238, 72%,  55%)
  iris-700:   hsl(238, 68%,  45%)
  iris-800:   hsl(238, 65%,  35%)
  iris-900:   hsl(238, 60%,  25%)
  iris-950:   hsl(238, 55%,  15%)

Void (dark backgrounds):
  void-50:    hsl(224, 71%,  4%)
  void-100:   hsl(224, 50%,  7%)
  void-200:   hsl(224, 38%,  10%)
  void-300:   hsl(224, 30%,  14%)
  void-400:   hsl(224, 24%,  18%)
  void-500:   hsl(224, 20%,  24%)
  void-600:   hsl(224, 16%,  35%)
  void-700:   hsl(224, 12%,  50%)
  void-800:   hsl(224, 10%,  65%)
  void-900:   hsl(224, 8%,   80%)
  void-950:   hsl(224, 6%,   94%)

Emerald (success):
  emerald-400: hsl(158, 64%, 52%)
  emerald-500: hsl(158, 60%, 45%)
  emerald-900: hsl(158, 45%, 10%)

Amber (warning):
  amber-400:  hsl(42,  95%, 58%)
  amber-500:  hsl(42,  90%, 50%)
  amber-900:  hsl(42,  60%, 10%)

Red (error):
  red-400:    hsl(0,   90%, 67%)
  red-500:    hsl(0,   85%, 58%)
  red-900:    hsl(0,   50%, 10%)
```

### Semantic Token Set — Dark Mode

```css
/* ─── SURFACES ─────────────────────────────────────────────────── */
--surface-app:        hsl(224, 71%, 4%);     /* Page background */
--surface-base:       hsl(224, 50%, 7%);     /* App shell, rail */
--surface-raised:     hsl(224, 38%, 10%);    /* Cards, panels */
--surface-overlay:    hsl(224, 30%, 14%);    /* Dropdowns, popovers */
--surface-elevated:   hsl(224, 24%, 18%);    /* Modals, command palette */
--surface-hover:      hsl(224, 28%, 16%);    /* Hover states */
--surface-selected:   hsl(238, 40%, 20%);    /* Selected items (iris-tinted) */
--surface-accent:     hsl(238, 55%, 15%);    /* Accent surface (iris-900) */

/* ─── BORDERS ───────────────────────────────────────────────────── */
--border-faint:       rgba(255, 255, 255, 0.04);
--border-subtle:      rgba(255, 255, 255, 0.07);
--border-default:     rgba(255, 255, 255, 0.11);
--border-strong:      rgba(255, 255, 255, 0.18);
--border-accent:      rgba(108, 121, 255, 0.45);
--border-success:     rgba(52,  196, 131, 0.40);
--border-warning:     rgba(245, 190,  36, 0.40);
--border-error:       rgba(247,  82,  82, 0.40);

/* ─── TEXT ──────────────────────────────────────────────────────── */
--text-primary:       hsl(224, 30%, 96%);    /* Primary content */
--text-secondary:     hsl(224, 14%, 62%);    /* Labels, descriptions */
--text-tertiary:      hsl(224, 10%, 42%);    /* Timestamps, meta */
--text-disabled:      hsl(224,  8%, 28%);    /* Disabled states */
--text-on-accent:     hsl(0,    0%, 100%);   /* Text on iris backgrounds */
--text-link:          hsl(238, 85%, 72%);    /* Hyperlinks */
--text-code:          hsl(224, 30%, 88%);    /* Code/monospace */

/* ─── ACCENT (IRIS) ─────────────────────────────────────────────── */
--accent:             hsl(238, 75%, 62%);    /* iris-500 */
--accent-subtle:      hsla(238, 75%, 62%, 0.12);
--accent-hover:       hsl(238, 80%, 68%);    /* iris-400 */
--accent-active:      hsl(238, 72%, 55%);    /* iris-600 */

/* ─── SEMANTIC STATUS ───────────────────────────────────────────── */
--success:            hsl(158, 64%, 52%);
--success-subtle:     hsla(158, 64%, 52%, 0.12);
--success-surface:    hsl(158, 45%, 10%);

--warning:            hsl(42,  95%, 58%);
--warning-subtle:     hsla(42,  95%, 58%, 0.12);
--warning-surface:    hsl(42,  60%, 10%);

--error:              hsl(0,   90%, 67%);
--error-subtle:       hsla(0,  90%, 67%, 0.12);
--error-surface:      hsl(0,   50%, 10%);

/* ─── SHADOWS ───────────────────────────────────────────────────── */
--shadow-xs:  0 1px  2px rgba(0, 0, 0, 0.40);
--shadow-sm:  0 2px  6px rgba(0, 0, 0, 0.50);
--shadow-md:  0 4px 16px rgba(0, 0, 0, 0.60);
--shadow-lg:  0 8px 32px rgba(0, 0, 0, 0.70);
--shadow-xl:  0 16px 64px rgba(0, 0, 0, 0.80);
--shadow-glow-accent:  0 0 24px hsla(238, 75%, 62%, 0.25);
--shadow-glow-success: 0 0 20px hsla(158, 64%, 52%, 0.20);
--shadow-glow-error:   0 0 20px hsla(0,   90%, 67%, 0.20);
```

### Semantic Token Set — Light Mode

```css
/* ─── SURFACES ─────────────────────────────────────────────────── */
--surface-app:        hsl(220, 14%, 96%);
--surface-base:       hsl(0,    0%, 100%);
--surface-raised:     hsl(220, 20%, 98%);
--surface-overlay:    hsl(0,    0%, 100%);
--surface-elevated:   hsl(0,    0%, 100%);
--surface-hover:      hsl(220, 14%, 94%);
--surface-selected:   hsl(238, 50%, 95%);
--surface-accent:     hsl(238, 80%, 96%);

/* ─── BORDERS ───────────────────────────────────────────────────── */
--border-faint:       rgba(0, 0, 0, 0.04);
--border-subtle:      rgba(0, 0, 0, 0.08);
--border-default:     rgba(0, 0, 0, 0.13);
--border-strong:      rgba(0, 0, 0, 0.20);
--border-accent:      rgba(94,  97, 243, 0.50);
--border-success:     rgba(22, 163, 74,  0.40);
--border-warning:     rgba(202, 138, 4,  0.40);
--border-error:       rgba(220,  38, 38, 0.40);

/* ─── TEXT ──────────────────────────────────────────────────────── */
--text-primary:       hsl(224, 50%, 10%);
--text-secondary:     hsl(224, 18%, 42%);
--text-tertiary:      hsl(224, 12%, 60%);
--text-disabled:      hsl(224,  8%, 75%);
--text-on-accent:     hsl(0,    0%, 100%);
--text-link:          hsl(238, 70%, 48%);
--text-code:          hsl(224, 40%, 20%);

/* ─── ACCENT ────────────────────────────────────────────────────── */
--accent:             hsl(238, 70%, 55%);
--accent-subtle:      hsla(238, 70%, 55%, 0.10);
--accent-hover:       hsl(238, 75%, 48%);
--accent-active:      hsl(238, 80%, 42%);

/* ─── SEMANTIC (adjusted for light) ────────────────────────────── */
--success:            hsl(158, 55%, 38%);
--success-subtle:     hsla(158, 55%, 38%, 0.10);
--success-surface:    hsl(158, 50%, 95%);

--warning:            hsl(42,  90%, 40%);
--warning-subtle:     hsla(42,  90%, 40%, 0.10);
--warning-surface:    hsl(42,  80%, 95%);

--error:              hsl(0,   75%, 50%);
--error-subtle:       hsla(0,  75%, 50%, 0.10);
--error-surface:      hsl(0,   60%, 96%);

/* ─── SHADOWS ───────────────────────────────────────────────────── */
--shadow-xs:  0 1px  2px rgba(0, 0, 0, 0.06);
--shadow-sm:  0 2px  6px rgba(0, 0, 0, 0.08);
--shadow-md:  0 4px 16px rgba(0, 0, 0, 0.10);
--shadow-lg:  0 8px 32px rgba(0, 0, 0, 0.12);
--shadow-xl:  0 16px 64px rgba(0, 0, 0, 0.14);
```

---

## 3.2 Typography System

### Typeface Choices

**Display & UI — Inter**
The best variable font for interface design. Sub-pixel rendering at 11px. Optical sizing at large sizes. Used by Linear, Vercel, Notion, Figma. The standard for premium developer tools.

**Monospace — JetBrains Mono**
Purpose-built for code display. Superior legibility at small sizes. Already used in Monaco. Extending it to all code-adjacent contexts (IDs, hashes, timestamps, paths) creates visual consistency.

```css
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'JetBrains Mono', 'Cascadia Code', 'Fira Code', monospace;
```

### Type Scale

All sizes in rem. Base: 16px. The scale follows a musical fourth ratio (×1.25) with some adjustments for practical use.

```css
/* Display sizes — page heroes only */
--text-display-xl:  2.25rem;  /* 36px — hero numbers in stats */
--text-display-lg:  1.875rem; /* 30px — page hero titles */
--text-display-md:  1.5rem;   /* 24px — section major headings */

/* Heading sizes — card headers, panel titles */
--text-heading-xl:  1.25rem;  /* 20px — page section headings */
--text-heading-lg:  1.125rem; /* 18px — card headers */
--text-heading-md:  1rem;     /* 16px — panel headers */
--text-heading-sm:  0.9375rem;/* 15px — subheadings */

/* Body sizes — content */
--text-body-lg:     0.9375rem;/* 15px — prominent body text */
--text-body-md:     0.875rem; /* 14px — standard body text */
--text-body-sm:     0.8125rem;/* 13px — secondary body text */

/* Label sizes — UI labels, table headers */
--text-label-lg:    0.75rem;  /* 12px — standard labels */
--text-label-sm:    0.6875rem;/* 11px — uppercase tracking labels */

/* Code sizes */
--text-code-lg:     0.875rem; /* 14px — code editors */
--text-code-md:     0.8125rem;/* 13px — inline code, paths */
--text-code-sm:     0.75rem;  /* 12px — hash values, timestamps */
```

### Font Weight System

```css
--weight-regular:  400;  /* Body text */
--weight-medium:   500;  /* Labels, navigation items */
--weight-semibold: 600;  /* Headings, active states */
--weight-bold:     700;  /* Display numbers, critical labels */
```

### Line Height System

```css
--leading-tight:   1.15;  /* Display type */
--leading-snug:    1.3;   /* Headings */
--leading-normal:  1.5;   /* Body text */
--leading-relaxed: 1.6;   /* Long-form content */
--leading-code:    1.6;   /* Monospace code */
```

### Letter Spacing System

```css
--tracking-tighter:  -0.04em;  /* Display headings */
--tracking-tight:    -0.02em;  /* Subheadings */
--tracking-normal:    0em;     /* Body text */
--tracking-wide:      0.04em;  /* Uppercase label-sm */
--tracking-wider:     0.08em;  /* STATUS BADGES uppercase */
```

### Typography Rules

**Uppercase text** is only used for two cases:
1. `label-sm` section headers in navigation panels (e.g., `RECENT RUNS`, `ALL PROJECTS`)
2. Status badge text (`SUCCESS`, `FAILED`, `RUNNING`)

No other text is uppercase. Uppercase decorative text is a design pattern from 2015.

**Monospace text** is used for:
- All code (Monaco editor contexts)
- Run IDs (`run_20240628_1`)
- File paths (`/src/components/Header.tsx`)
- Hash values (`sha256:4a3b...`)
- Timestamps in logs (`14:02:01.234`)
- Port numbers, URLs, environment values

Using monospace for identifiers that will be compared or copied character-by-character improves accuracy and signals "this is a technical value."

---

## 3.3 Spacing System

Base unit: **4px**. Every spacing value is a multiple of 4.

```css
--space-px:    1px;    /* hairline borders */
--space-0:     0px;
--space-0-5:   2px;    /* micro gaps */
--space-1:     4px;    /* icon-to-icon gaps */
--space-1-5:   6px;    /* tight inline spacing */
--space-2:     8px;    /* icon-to-label gap, sm padding */
--space-2-5:   10px;   /* compact button padding */
--space-3:     12px;   /* md padding, list item gaps */
--space-4:     16px;   /* standard padding */
--space-5:     20px;   /* comfortable padding */
--space-6:     24px;   /* card padding */
--space-7:     28px;   /* form field spacing */
--space-8:     32px;   /* section gaps */
--space-10:    40px;   /* major section gaps */
--space-12:    48px;   /* header heights */
--space-14:    56px;   /* large gaps */
--space-16:    64px;   /* section hero spacing */
--space-20:    80px;   /* page section spacing */
--space-24:    96px;   /* hero sections */
```

### Component Spacing Rules

**Button padding:**
- xs: `--space-1-5` vertical, `--space-3` horizontal
- sm: `--space-2` vertical, `--space-3` horizontal
- md: `--space-2-5` vertical, `--space-4` horizontal (default)
- lg: `--space-3` vertical, `--space-6` horizontal

**Card padding:**
- compact: `--space-4` all sides
- default: `--space-5` vertical, `--space-6` horizontal
- generous: `--space-6` vertical, `--space-8` horizontal

**Table cell padding:**
- default: `--space-3` vertical, `--space-4` horizontal
- compact: `--space-2` vertical, `--space-3` horizontal

**Gap between form elements:** `--space-5` (20px)  
**Gap between card sections:** `--space-6` (24px)  
**Gap between page sections:** `--space-8` (32px)

---

## 3.4 Elevation System

In dark interfaces, elevation is communicated through **background lightness**, not box shadows. Shadows are supplementary for floating elements.

```
Surface Level 0 — App background:      --surface-app      (darkest)
Surface Level 1 — App shell:           --surface-base
Surface Level 2 — Cards, panels:       --surface-raised
Surface Level 3 — Dropdowns, popovers: --surface-overlay
Surface Level 4 — Modals, command:     --surface-elevated  (lightest)
```

Each level is 2–4% lighter (in HSL lightness) than the previous. The gradient is subtle — enough to perceive depth, not enough to draw attention.

**Shadow usage:**
- Level 0–2: No shadow
- Level 3 (dropdowns): `--shadow-md`
- Level 4 (modals): `--shadow-xl`
- Floating focused elements (command palette): `--shadow-xl` + optional `--shadow-glow-accent`

---

## 3.5 Border Radius System

```css
--radius-xs:    3px;   /* Inline badges, pills */
--radius-sm:    6px;   /* Buttons (default), inputs, small cards */
--radius-md:    8px;   /* Cards, panels */
--radius-lg:    12px;  /* Large cards, dialogs */
--radius-xl:    16px;  /* Modals, command palette */
--radius-2xl:   24px;  /* Feature cards */
--radius-full:  9999px;/* Status dots, toggle switches */
```

**Rule:** The border radius should be proportional to the element size. Tiny elements (badges, dots) get `--radius-full`. Large containers (cards) get `--radius-md`. Full-screen modals get `--radius-xl`. A large element with a small radius (e.g., a full-height panel with `rounded-none`) is correct. A small element with a large radius (e.g., a 32px icon button with `rounded-xl`) reads as inconsistent.

---

## 3.6 Animation System

### Philosophy

Animation has one job: **communicate state changes**. Every animation must answer the question "what changed?" If it doesn't, it shouldn't exist.

Four categories:

**1. Spatial animations** — Express spatial relationships between elements
- Purpose: When an element enters or exits, from which direction?
- Sliding panels enter from their edge (right panel from right, context panel from left)
- Modals scale up from center (not slide — modal has no directional relationship to trigger)

**2. State animations** — Communicate property changes
- Purpose: The user's action changed something; what changed?
- Status badges: Crossfade on status change
- Numbers: Spring-count animation on load

**3. Attention animations** — Guide focus to new information
- Purpose: Something new appeared; where is it?
- New log events: Slide in from bottom
- New notifications: Bell pulse

**4. Operational animations** — Communicate ongoing activity
- Purpose: The system is working; it hasn't frozen
- RUNNING state: Pulse ring
- Loading: Shimmer sweep
- Spinner: Rotation

### Duration Tokens

```css
--duration-instant:  80ms;   /* Hover color changes */
--duration-fast:     120ms;  /* Dropdown appear/disappear */
--duration-default:  180ms;  /* Panel transitions, button feedback */
--duration-slow:     250ms;  /* Modal enter/exit */
--duration-slower:   350ms;  /* Page transitions */
--duration-spring:   400ms;  /* Spring-based number animations */
```

**Rule:** No animation exceeds 400ms except spring physics. Users do not wait for animations — they move faster than they. A 600ms panel slide is an obstacle, not a delight.

### Easing Tokens

```css
--ease-out:     cubic-bezier(0.0, 0.0, 0.2, 1);  /* Entering elements */
--ease-in:      cubic-bezier(0.4, 0.0, 1.0, 1);  /* Exiting elements */
--ease-in-out:  cubic-bezier(0.4, 0.0, 0.2, 1);  /* State changes */
--ease-bounce:  cubic-bezier(0.34, 1.56, 0.64, 1); /* Spring-like */
```

**Entering elements** use `ease-out` — they accelerate from the origin and decelerate as they arrive. This feels natural and responsive.

**Exiting elements** use `ease-in` — they accelerate away from their position. Exits should feel faster than entrances; users don't want to wait for things to leave.

### Motion Guidelines

**Skeleton loader animation:**
```css
@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position:  200% 0; }
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--surface-raised) 0%,
    var(--surface-overlay) 50%,
    var(--surface-raised) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.6s var(--ease-in-out) infinite;
}
```

**Pulse ring animation (RUNNING state):**
```css
@keyframes pulse-ring {
  0%   { transform: scale(1);    opacity: 0.8; }
  70%  { transform: scale(1.35); opacity: 0;   }
  100% { transform: scale(1.35); opacity: 0;   }
}
```

**Reduced motion:**
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 3.7 Component States Matrix

Every interactive component must have all six states defined:

| State | Visual Treatment |
|---|---|
| Default | Base styling |
| Hover | `--surface-hover` background, `--border-strong` border |
| Focus | `--border-accent` outline (2px, 2px offset) |
| Active/Pressed | `--surface-selected` background, slight scale(0.99) |
| Disabled | 40% opacity, `cursor-not-allowed`, no hover/focus effects |
| Loading | Spinner replaces label/icon, width locked (no layout shift) |

**Focus ring implementation:**
```css
:focus-visible {
  outline: 2px solid var(--border-accent);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}

/* Suppress for mouse users */
:focus:not(:focus-visible) {
  outline: none;
}
```

---

## 3.8 Iconography

**Library:** `lucide-react` (installed). Consistent 1.5px stroke weight. Never mix with other icon libraries.

**Icon sizing:**
```css
--icon-xs:  12px;  /* Inline text decorators */
--icon-sm:  14px;  /* Badge icons */
--icon-md:  16px;  /* Button icons, nav items */
--icon-lg:  20px;  /* Card action icons */
--icon-xl:  24px;  /* Feature icons */
--icon-2xl: 32px;  /* Section header icons */
--icon-3xl: 48px;  /* Empty state illustrations */
```

**Icon color:** Icons inherit `currentColor`. They are never given explicit colors in JSX — color is controlled by the parent's CSS color property.

**Icon-only buttons:** Must have `aria-label` matching the button's action. No exceptions.

---

## 3.9 Responsive Breakpoints

```css
--breakpoint-sm:  640px;   /* Large phone landscape */
--breakpoint-md:  768px;   /* Tablet portrait */
--breakpoint-lg:  1024px;  /* Small laptop */
--breakpoint-xl:  1280px;  /* Standard desktop */
--breakpoint-2xl: 1440px;  /* Large desktop */
--breakpoint-3xl: 1920px;  /* Ultra-wide */
```

**Product-level breakpoint behavior:**

| Breakpoint | Context Panel | Right Panel | Navigation |
|---|---|---|---|
| < 768px | Hidden (drawer) | Hidden (sheet) | Bottom tab bar |
| 768–1024px | Collapsed (icon only) | Hidden (manual open) | Collapsed rail |
| 1024–1280px | Collapsed (icon only) | Hidden (default, can open) | Collapsed rail |
| 1280–1440px | Expanded (240px) | Closed (default, can open) | Expanded |
| > 1440px | Expanded (240px) | Open (default 380px) | Expanded |

---

## 3.10 Accessibility Standards

**Target:** WCAG 2.1 Level AA

**Contrast requirements:**
- Normal text (< 18px or < 14px bold): ≥ 4.5:1
- Large text (≥ 18px or ≥ 14px bold): ≥ 3.0:1
- UI components: ≥ 3.0:1

**ARIA requirements (mandatory):**
- All icon-only interactive elements: `aria-label`
- All dynamically updating regions: `aria-live`
- All modal dialogs: `role="dialog"` + `aria-labelledby` + `aria-modal="true"`
- All tab sets: `role="tablist"` / `role="tab"` / `aria-selected` / `aria-controls`
- All tree views: `role="tree"` / `role="treeitem"` / `aria-expanded`
- All status changes: `aria-live="polite"` announcement
- All loading states: `aria-busy="true"` on the loading container

**Focus management:**
- Modal open: Focus moves to first interactive element inside
- Modal close: Focus returns to the trigger element
- Command palette close: Focus returns to the element that had focus when it opened
- Route change: Focus moves to the page `<h1>` (or first heading)

**Keyboard navigation for complex components:**
- File tree: `↑↓` to move, `→` to expand, `←` to collapse/go up, `Enter` to open file
- Data table: `↑↓` to move rows, `Enter` to open, `Space` to select
- Graph canvas: `F` to fit, `+/-` to zoom, `Escape` to deselect
- Command palette: `↑↓` to move, `Enter` to select, `Tab` to see contextual actions

---

---

# PHASE 4 — Component Architecture

## Design Conventions

All screen designs follow these conventions:
- Layout described as a grid with named areas
- `[fixed: Npx]` = fixed dimension, does not flex
- `[flex]` = fills remaining space
- `[collapse]` = can be hidden by user action
- `→` in interactions means "user action leads to"

---

## Screen 1 — Login (`/login`)

**Purpose:** Authentication gate. First brand impression.

**Layout:**
```
┌─ Full viewport ────────────────────────────────────────────────────────┐
│                                                                        │
│   Background: --surface-app                                            │
│   Pattern: SVG hexagonal grid, 3% opacity (brand motif)               │
│   Gradient: radial at center, iris-950 to transparent                 │
│                                                                        │
│                    ┌─ Card [fixed: 420px] ─────────────┐              │
│                    │  [Logo mark: 40px]                 │              │
│                    │  [Wordmark: heading-xl]            │              │
│                    │  [Tagline: body-sm, text-secondary]│              │
│                    │  ─────────────────────────────     │              │
│                    │  [Label: Username]                 │              │
│                    │  [Input: text]                     │              │
│                    │  [Label: Password]                 │              │
│                    │  [Input: password] [show/hide]     │              │
│                    │  [Checkbox: Remember me]           │              │
│                    │  [Button: Sign In → full width]    │              │
│                    │  [Link: Forgot password?]          │              │
│                    │  ─────────────────────────────     │              │
│                    │  [Version badge] [Status]          │              │
│                    └────────────────────────────────────┘              │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

**Component hierarchy:**
- `LoginPage`
  - `AuthCard` (glassmorphism: `backdrop-blur-sm bg-white/4 border border-white/8`)
    - `BrandMark`
    - `LoginForm`
      - `FormField` (Username)
      - `FormField` (Password) + `PasswordToggle`
      - `RememberCheckbox`
      - `SubmitButton`
      - `ForgotPasswordLink`
    - `CardFooter`

**Error state:** The card shakes (translateX oscillation, 300ms, `ease-bounce`) on authentication failure. An `InlineError` component appears between the password field and submit button. The specific field with the error gets an `--border-error` ring.

**Loading state:** The submit button shows a `Spinner` in place of the label "Sign In". Button width does not change (prevents layout shift). Button is disabled.

**Success state:** Button text transitions to "✓ Authenticated" for 800ms, then the router navigates to `/`.

**Keyboard:** Full form tab order. `Enter` in any field submits. `Escape` clears the error state.

**Responsive:** Card is full-width with `--space-4` horizontal padding at < 480px.

---

## Screen 2 — Organization Dashboard (`/`)

**Purpose:** The operational control room. Shows the health of all projects and surfaces active runs.

**Layout:**
```
App Shell Grid:
  ┌─ Rail [48px] ─┬─ Context [240px] ─┬─ Header [52px] ──────────────────────────────────────┐
  │               │                    │ [Breadcrumb: Org name]  [⌘K] [🔔] [Avatar]           │
  │               │  NAVIGATION        ├─────────────────────────────────────────────────────  │
  │  Global Rail  │  All Projects      │  [Primary Work Surface — scrollable]                 │
  │               │  Runs              │                                                      │
  │               │  Compiler          │  ┌─ Health Strip ───────────────────────────────────┐│
  │               │  Telemetry         │  │ [5 × StatCard horizontal]                        ││
  │               │  ─────────         │  └──────────────────────────────────────────────────┘│
  │               │  Team              │                                                      │
  │               │  Settings          │  ┌─ Active Runs ────────────────────────────────────┐│
  │               │                    │  │ [visible only when runs in progress]             ││
  │               │                    │  │ [ActiveRunCard × N, full width, stacked]        ││
  │               │                    │  └──────────────────────────────────────────────────┘│
  │               │                    │                                                      │
  │               │                    │  ┌─ Recent Projects ────────────────────────────────┐│
  │               │                    │  │ [ProjectCard × 5, 3-col grid]                   ││
  │               │                    │  └──────────────────────────────────────────────────┘│
  │               │                    │                                                      │
  │               │                    │  ┌─ Build Activity Chart ──────────────────────────┐│
  │               │                    │  │ [Bar chart: 30d build volume]                    ││
  │               │                    │  └──────────────────────────────────────────────────┘│
  │               │                    │                                                      │
  │               │                    │                            [Right Panel: Activity]   │
  └───────────────┴────────────────────┴──────────────────────────────────────────────────────┘
```

**Components:**

`StatCard` (×5, horizontal strip):
```
┌──────────────────────────────┐
│  [Icon]  [Label: text-label] │
│                              │
│  [Value: text-display-xl]    │
│  [Delta: ▲N text-success]    │
└──────────────────────────────┘
```
Stats: Total Projects | Active Compilations | 7-Day Success Rate | Avg Compile Time | Artifacts Generated

Clicking a stat card filters the Recent Projects section to the relevant subset.

`ActiveRunCard` (full-width, appears only when RUNNING):
```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ [PulseRing] GENERATING   │   E-Commerce Platform  ·  run_20240628_1               │
│ [████████████████░░░░ ]  │   Agent: ProductCatalogService                  14.2s  │
│ Planning ✓  Validating ✓  Generating ●  Packaging ○                      [Open →] │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

`ProjectCard` (3-column grid, 5 cards):
```
┌───────────────────────────────────────────────────────┐
│  [StatusBadge]                             [★] [⋯]   │
│                                                        │
│  [Project Name: heading-lg]                           │
│  [Project ID: text-code-sm, text-tertiary]            │
│                                                        │
│  [SparkLine: 7 recent runs]  [SuccessRate: N%]        │
│                                                        │
│  [Runs: N]  ·  [Last: relative timestamp]             │
└───────────────────────────────────────────────────────┘
```

The `SparkLine` shows the last 7 runs as small dots (green = success, red = fail). This gives the manager an instant quality trend at a glance.

**Right Panel — Activity Feed:**
Live SSE-driven event stream. Header: "Live Activity" + "Pause" toggle. Body: chronological event list, newest at top. Each entry: timestamp (code-sm) + project name (linked) + event description.

**Empty state (no projects):**
```
        ⬡  (graph icon, 64px, --text-tertiary with iris tint)

    No projects yet

    Genesis compiles your specification into a
    production-ready application artifact.
    Start by describing what you want to build.

    [Compile Your First Spec →]          [View Example]
```

**Loading state:** Health strip shows 5 `StatCard` skeletons. Active Runs section is hidden (not shown as loading — if nothing is running, nothing shows). Recent Projects shows 5 `ProjectCard` skeletons.

---

## Screen 3 — Projects (`/projects`)

**Purpose:** Browse, search, filter, and manage all projects.

**Layout:**
```
┌─ Toolbar ────────────────────────────────────────────────────────────────────┐
│  [StatusFilter: All|Success|Failed|Running]  [Search]  [Sort▾]  [⊞][☰]  [+New] │
└──────────────────────────────────────────────────────────────────────────────┘
┌─ Batch Bar (shown when items selected) ─────────────────────────────────────┐
│  [□ N selected]  [Download Artifacts]  [Archive]  [Delete...]  [✕ Clear]    │
└──────────────────────────────────────────────────────────────────────────────┘
┌─ Project Grid / List ────────────────────────────────────────────────────────┐
│  [Grid view: ProjectCard ×N, responsive columns]                            │
│  OR                                                                          │
│  [List view: ProjectTable with sortable columns]                            │
└──────────────────────────────────────────────────────────────────────────────┘
[Pagination: Load more / page nav]
```

**List view columns:** `□` Select | Name | Status | Runs | Success Rate | Last Run | Duration | Actions

**Grid→List toggle:** Persisted in layout preferences.

**Context menu (right-click on any project):** Open | Open in new tab | ─── | New Run | Rename | Copy ID | ─── | Pin | Archive | ─── | Delete…

**Empty state (no projects matching filter):**
```
        ⊘  (filter icon with slash)

    No matching projects

    Try adjusting your filters or search term.

    [Clear Filters]
```

**Empty state (no projects at all):** Same as Dashboard empty state.

---

## Screen 4 — Project Overview (`/projects/[id]`)

**Purpose:** The "home" of a project. Shows last run status prominently and quick paths to all actions.

**Layout:**
```
┌─ Project Header ─────────────────────────────────────────────────────────────┐
│  [ProjectName: heading-display]                [● SUCCESS]  [+ New Run] [⋯] │
│  [project_id: code-sm, text-tertiary]          [Last run: 2h ago, 14.2s]    │
│  [Stats: N Runs · N% Success Rate · N Artifacts]                            │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ Two-column grid ────────────────────────────────────────────────────────────┐
│  ┌─ Last Run Summary ─────────────────────┐  ┌─ Run History Chart ─────────┐│
│  │  [StatusBadge: large]                  │  │  [Bar chart: last 10 runs] ││
│  │  run_20240628_1                        │  │  Success vs Failed          ││
│  │  [Phase timeline: 4 rows]              │  └─────────────────────────────┘│
│  │  [View Full Run →]                     │                                 │
│  └────────────────────────────────────────┘  ┌─ Spec Summary ─────────────┐ │
│                                              │  Pages: N  APIs: N  etc.   │ │
│                                              │  [View Specification →]     │ │
│                                              └─────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ All Runs Table ─────────────────────────────────────────────────────────────┐
│  [Table: run ID | Status | Duration | Integrity | Date | Actions]           │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Empty state (no runs):**
```
        ⚡ (lightning icon)

    No runs for this project

    Compile a specification to generate
    your first run.

    [New Run →]
```

---

## Screen 5 — Compiler (`/compiler`)

**Purpose:** Spec authoring and compilation trigger. The primary creation tool.

**Layout:**
```
┌─ Compiler Header ────────────────────────────────────────────────────────────┐
│  [Breadcrumb: Compiler]  [Project: Select ▾]  [Templates ▾]                │
└──────────────────────────────────────────────────────────────────────────────┘
┌─ Editor Zone [flex] ─────────────────────────────────────────────────────────┐
│  ┌─ Tab bar ──────────────────────────────────────────────────────────────┐  │
│  │ [spec.json ×]  [template_basic.json ×]  [+]                           │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                               │
│  [Monaco Editor — full height, json mode, Genesis schema validation]        │
│                                                                               │
│  ┌─ Status Bar ───────────────────────────────────────────────────────────┐  │
│  │ ✓ Valid JSON · 6 fields · Ln 1, Col 1  [Format]  [Validate ⌘S]  [▶ Compile ⌘↵] │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘

[Right Panel — Compiler Output, see below]
```

**Right Panel — Three states:**

**Idle:**
```
        ⚡

    Ready to compile

    Edit your specification in the editor.
    Press ⌘↵ to begin compilation.

    [Load Example Spec]   [Browse Templates]
```

**Running (phase blocks):**
```
┌─ Phase: GENERATING ● ──────────────────────── 14.2s ──┐
│  → ProductCatalogService generated                     │
│  → CheckoutController generated                        │
│  → UserAuthModule generated  (live, auto-scrolling)   │
└────────────────────────────────────────────────────────┘

┌─ Phase: VALIDATION ✓ ──────────────────────── 1.8s ─── [▲] ┐
│  [expanded on click]                                         │
│  ✓ NoCircularDependencies                                    │
│  ✓ AllAPIsHaveModels                                         │
│  ⚠ UnreferencedComponents (2)                               │
└──────────────────────────────────────────────────────────────┘

┌─ Phase: PLANNING ✓ ───────────────────────── 2.1s ─────[▲] ┐
│  [collapsed]                                                 │
└──────────────────────────────────────────────────────────────┘
```

**Complete:**
```
┌─ ✓ Compilation Successful ────────────────────────────────┐
│  14.2s  ·  3 phases  ·  47 events  ·  Integrity: 92/100  │
│                                                            │
│  [View Run →]      [Download Artifacts ↓]                │
│  [Compile Again]                                           │
└────────────────────────────────────────────────────────────┘
```

---

## Screen 6 — Run Overview (`/projects/[id]/runs/[runId]`)

**Purpose:** Master view of a single compilation run. The "landing page" after a compilation.

**Layout:**
```
┌─ Run Header ─────────────────────────────────────────────────────────────────┐
│  E-Commerce Platform / run_20240628_1                  [● SUCCESS]  [Re-run]│
│  Jun 28, 2026 · 2:14 PM  ·  14.2s  ·  47 events  ·  Integrity 92/100      │
│  [View Trace]  [View Architecture]  [Download Artifacts]                    │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ Content Grid ───────────────────────────────────────────────────────────────┐
│  ┌─ Phase Timeline ────────────────┐   ┌─ Spec Summary ────────────────────┐ │
│  │  ● Planning      2.1s  ✓        │   │  Name: E-Commerce Platform        │ │
│  │  ● Validating    1.8s  ✓        │   │  Pages: 8 · APIs: 24              │ │
│  │  ● Generating    9.4s  ✓        │   │  Components: 18 · Entities: 6     │ │
│  │  ● Packaging     0.9s  ✓        │   │  Features: 12                     │ │
│  └─────────────────────────────────┘   └───────────────────────────────────┘ │
│                                                                               │
│  ┌─ Architecture Preview (mini graph, non-interactive, full width) ─────────┐ │
│  │  [React Flow canvas, fitView, no controls, no interaction]              │ │
│  │  [Click anywhere → navigates to /architecture]                          │ │
│  │  [Overlay text: "Click to explore full architecture →"]                 │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Context Panel (left, when run is open):**
```
← E-Commerce Platform
run_20240628_1     ● SUCCESS
──────────────────────────────
⊞ Overview                ← active
⚡ Compiler Trace
⬡ Architecture
📁 Workspace
📦 Artifacts
📋 Planning Report
```

This is the Run Navigator — it replaces the horizontal tab bar from the current design. Vertical navigation supports any number of sections without overflow.

---

## Screen 7 — Compiler Trace (`/projects/[id]/runs/[runId]/compiler`)

**Purpose:** Full audit trail of the compilation. Inspectable, filterable, exportable.

**Layout:**
```
┌─ Toolbar ────────────────────────────────────────────────────────────────────┐
│  [Phase: All ▾]  [Status: All ▾]  [Search events...]  [Gantt ⊞]  [Export ↓]│
└──────────────────────────────────────────────────────────────────────────────┘
┌─ Phase Stepper (sticky, collapses to summary bar on scroll) ─────────────────┐
│  ✓ Planning 2.1s  ·  ✓ Validating 1.8s  ·  ✓ Generating 9.4s  ·  ✓ Packaging 0.9s │
└──────────────────────────────────────────────────────────────────────────────┘
┌─ Phase Blocks (scrollable, virtualised) ────────────────────────────────────┐
│                                                                               │
│  ┌─ PLANNING PHASE ──────────────────────────── ✓ 2.1s  12 events ──── [▼] ┐│
│  │  14:02:01.012  →  SpecAnalysisStarted                                   ││
│  │  14:02:01.245  →  FeatureExpansion · 12 features resolved               ││
│  │  14:02:01.891  →  DependencyGraph · 47 edges                  [+details]││
│  │  ...                                                                     ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                               │
│  ┌─ VALIDATION PHASE ────────────────────────── ✓ 1.8s  8 events ──── [▼] ─┐│
│  │  [collapsed by default for completed phases]                             ││
│  └─────────────────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────────────────┘
```

**Gantt mode (toggle via toolbar):**
Switches the entire view from phase blocks to a horizontal Gantt timeline chart. Each phase is a horizontal bar at its temporal position. Clicking a bar scrolls back to block view and expands that phase.

**For RUNNING compilations:**
Active phase block is expanded and pinned at viewport bottom. Events stream in live. "Jump to bottom" sticky pill appears when user scrolls up.

**Keyboard:** `Ctrl+F` / `⌘F` opens an in-page search that highlights matching events across all phase blocks.

---

## Screen 8 — Architecture Graph (`/projects/[id]/runs/[runId]/architecture`)

**Purpose:** Visual exploration of the compiled application's structure. This is the most intellectually rich view in the product.

**Layout:**
```
┌─ Toolbar ────────────────────────────────────────────────────────────────────┐
│  Graph: [API ▾]  │  View: [● Canvas] [○ Table]  │  [Fit F] [+] [-]  [Export ▾] │
└──────────────────────────────────────────────────────────────────────────────┘
┌─ Graph Panel [flex-1] ──────────────────────────────────────────────────────┐
│  ┌─ Node Filter (240px, left) ──┐  ┌─ React Flow Canvas ──────────────────┐ │
│  │  FILTER BY TYPE             │  │                                       │ │
│  │  [□] API Endpoints    (24)  │  │  [Nodes rendered as custom React     │ │
│  │  [□] Pages             (8)  │  │   Flow nodes with type-specific      │ │
│  │  [□] Components       (18)  │  │   shapes and colors]                 │ │
│  │  [□] DB Entities       (6)  │  │                                       │ │
│  │  ─────────────────────────  │  │  [Background: dot grid]              │ │
│  │  SEARCH NODES               │  │  [Controls: zoom, fit, lock]         │ │
│  │  [input: filter by name]   │  │  [MiniMap: bottom-right]             │ │
│  │  ─────────────────────────  │  │                                       │ │
│  │  NODE LIST                  │  │                                       │ │
│  │  > ProductController        │  └───────────────────────────────────────┘ │
│  │    CartService              │                                            │
│  │    UserAuthAPI              │  [Right Panel: Node Detail, shown when    │
│  │    ...                      │   a node is selected]                     │
│  └──────────────────────────────┘                                           │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Node types and visual language:**
- API Endpoints: Rounded rectangle, iris border, `Zap` icon
- Pages: Rectangle, slate border, `FileText` icon
- Components: Hexagon (CSS clip-path), emerald border, `Layers` icon
- DB Entities: Rectangle with double top border (DB symbol), amber border, `Database` icon
- Features: Circle, purple border, `Star` icon

**Node selection → Right Panel:**
Slides in from right (200ms ease-out). Shows:
```
─────────────────────────────────────
ProductController
API Endpoint
GET /api/v1/products
─────────────────────────────────────
DEPENDENCIES (3)
  → ProductRepository
  → CacheLayer
  → AuthMiddleware
─────────────────────────────────────
USED BY (2)
  → ProductPage
  → SearchPage
─────────────────────────────────────
SOURCE FILE
  /src/api/ProductController.ts   [↗]
─────────────────────────────────────
Node Hash
sha256:4a3b...def9              [⎘]
─────────────────────────────────────
```

**Graph type switching (API/Page/Component/Feature/DB):**
Nodes animate position when switching between graph types. Nodes that exist in both types morph in place; new nodes fade in; removed nodes fade out. Duration: 300ms ease-in-out. This creates a sense of continuous space rather than page replacement.

**Export options:** PNG (viewport) | PNG (full) | SVG | JSON

**Empty state (no graph data):**
```
        ⬡  (network icon)

    Architecture unavailable

    This graph type was not produced
    by the compilation. This may indicate
    the spec contained no [type] definitions.

    [View Planning Report]    [Switch to Table View]
```

---

## Screen 9 — Workspace Explorer (`/projects/[id]/runs/[runId]/workspace`)

**Purpose:** Browse and inspect the generated source code.

**Layout:**
```
┌─ File Tree [fixed: 240px] ──────┬─ Editor Zone [flex] ──────────────────────┐
│  [Search files...]              │  ┌─ Tab Bar ────────────────────────────┐ │
│                                 │  │ [package.json×] [App.tsx×] [+]       │ │
│  ▶ src/                        │  └──────────────────────────────────────┘ │
│    ▶ components/               │  ┌─ Monaco Editor (read-only) ──────────┐ │
│    ▶ pages/                    │  │                                       │ │
│    ▶ api/                      │  │  [Full height, syntax highlighted,   │ │
│    ▼ styles/                   │  │   language-specific, line numbers]   │ │
│      globals.css  ←selected    │  │                                       │ │
│      theme.css                 │  └──────────────────────────────────────┘ │
│  ▶ public/                     │  ┌─ Status Bar ──────────────────────────┐ │
│  package.json                  │  │ CSS · 142 lines · [Copy ⎘] [Raw ↗]  │ │
│  tsconfig.json                 │  └──────────────────────────────────────┘ │
│                                 │                                            │
│  ─────────────────────────     │                                            │
│  47 files · 12 dirs            │                                            │
│  TypeScript 62% CSS 18% …     │                                            │
└─────────────────────────────────┴────────────────────────────────────────────┘
```

**File tree keyboard navigation:**
- `↑↓` — move selection
- `→` — expand directory (or open file if leaf)
- `←` — collapse directory (or go to parent)
- `Enter` — open selected file in new tab
- `⌘F` — focus search input

**Tab bar behavior:**
- Tabs overflow horizontally (scroll arrows at overflow edges)
- `⌘W` closes active tab
- Middle-click closes tab
- Dragging tabs to reorder (if feasible in implementation)
- Closing the last tab shows the "no file selected" empty state

**Empty state (no file selected):**
```
Select a file from the tree
to view its generated source code.
```

**Empty state (binary file selected):**
```
Binary file — preview unavailable.
[Download Raw ↓]
```

---

## Screen 10 — Artifact Manager (`/projects/[id]/runs/[runId]/artifacts`)

**Purpose:** Download and verify compilation outputs.

**Layout:**
```
┌─ Header ─────────────────────────────────────────────────────────────────────┐
│  Artifacts  ·  run_20240628_1  ·  ✓ Complete                               │
│  [Download All ↓]                                                           │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ SOURCE ──────────────────────────────────────────────────────────────────── ┐
│  📦  deployment_bundle.zip          Compiled Bundle  ·  12.4 MB  [↓]       │
│      sha256: 4a3b...def9                                          [⎘]       │
└───────────────────────────────────────────────────────────────────────────── ┘

┌─ METADATA ────────────────────────────────────────────────────────────────── ┐
│  {}  deployment_manifest.json       Build Metadata  ·  2.1 KB   [↓]       │
│  {}  planning_report.json           Plan Validation ·  8.4 KB   [↓]       │
└───────────────────────────────────────────────────────────────────────────── ┘

┌─ TELEMETRY ───────────────────────────────────────────────────────────────── ┐
│  {}  execution_trace.json           Agent Trace     ·  14.2 KB  [↓]       │
└───────────────────────────────────────────────────────────────────────────── ┘

┌─ GRAPHS ──────────────────────────────────────────────────────────────────── ┐
│  ⬡  api_graph.json                  API Architecture ·  3.2 KB  [↓]       │
│  ⬡  page_graph.json                 Page Structure  ·  1.8 KB  [↓]        │
│  ⬡  component_graph.json            Components      ·  4.1 KB  [↓]        │
│  ⬡  feature_graph.json              Features        ·  2.7 KB  [↓]        │
└───────────────────────────────────────────────────────────────────────────── ┘

┌─ INTEGRITY ─────────────────────────────────────────────────────────────────┐
│  Workspace Hash:    [sha256 full value]                          [⎘]       │
│  Bundle Hash:       [sha256 full value]                          [⎘]       │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Download UX:**
Each row has a persistent `[↓]` download button (not hidden on hover). Clicking triggers the file download. A toast confirms: "Downloading deployment_bundle.zip". The button briefly shows a `Loader` then `✓` before reverting.

**Hash values:**
Shown truncated (`4a3b...def9`) with a `[⎘]` copy button that copies the full hash. Hovering the truncated value shows the full hash in a tooltip.

---

## Screen 11 — Planning Report (`/projects/[id]/runs/[runId]/report`)

**Purpose:** Rule engine validation results. Critical for diagnosing failures.

**Layout:**
```
┌─ Status Banner ─────────────────────────────────────────────────────────────┐
│  ✓  Rule Validation: SUCCESS       Integrity: 92/100 · Duration: 1.8s      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─ Metrics Grid (2×4) ───────────────────────────────────────────────────────┐
│  [Features: 12] [Pages: 8] [APIs: 24] [Entities: 16]                      │
│  [Components: 18] [Dependencies: 47] [Errors: 0] [Warnings: 2]            │
└────────────────────────────────────────────────────────────────────────────┘

┌─ Rule Results ─────────────────────────────────────────────────────────────┐
│  [All] [Pass N] [Warn N] [Fail N]         [Search rules...]                │
│                                                                              │
│  ✓  NoCircularDependencies          PASS   0.12s                           │
│  ✓  AllAPIsHaveModels               PASS   0.09s                           │
│  ⚠  UnreferencedComponents          WARN   0.04s    [2 issues] [▼]        │
│  ✓  DatabaseRelationalIntegrity     PASS   0.31s                           │
└────────────────────────────────────────────────────────────────────────────┘

┌─ Issue Detail (expanded when a rule with issues is opened) ─────────────────┐
│  ⚠ UnreferencedComponents                                                  │
│  2 components are defined but not referenced by any page.                  │
│                                                                              │
│  • HeaderDropdown (defined in components, not used in any page)            │
│  • FooterSocial (defined in components, not used in any page)              │
│                                                                              │
│  Remediation: Add these to a page spec or remove from the component list.  │
│  [Edit Specification →]                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Failed run state:** Banner is red. `Errors: N` metric card is red. Failed rules are expanded by default. Remediation text for each failure is shown prominently.

---

## Screen 12 — Command Palette (global overlay)

**Purpose:** Universal navigation, search, and action interface.

**Trigger:** `⌘K` / `Ctrl+K` from any page.

**Layout:**
```
[Backdrop: --surface-app/70 backdrop-blur-sm]

┌─ Command Palette [fixed: 640px, centered] ──────────────────────────────────┐
│  [🔍  Type a command or search...]                                          │
│  ─────────────────────────────────────────────────────────────────────────  │
│  RECENT                                                                     │
│  ⬡  E-Commerce Platform                                            ↗  ⚡   │
│  ⬡  run_20240628_1  ·  E-Commerce Platform  ·  SUCCESS  ·  14.2s   ↗      │
│                                                                             │
│  QUICK ACTIONS                                                              │
│  ⚡  New Compilation                                              ⌘N       │
│  G   Go to Projects                                               G P      │
│  G   Go to Telemetry                                              G T      │
│  ⚙   Open Settings                                                ,        │
│                                                                             │
│  [When typing: live filtered results grouped by Projects / Runs / Files]   │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Result item structure:**
- Left icon (16px, type-specific)
- Primary label (text-body-md, text-primary)
- Secondary label (text-body-sm, text-tertiary, e.g., project name or timestamp)
- Right: contextual action buttons (Open | Run | Download) — appear on hover
- Right: keyboard shortcut badge

**Result group ordering (when typing):**
1. Projects (highest priority)
2. Runs
3. Actions
4. Settings

**Keyboard navigation:**
`↑↓` move selection, `Enter` to primary action, `Tab` to move to contextual action buttons, `Escape` to close.

---

## Screen 13 — Notification Center (popover)

**Trigger:** Bell icon in global rail.

**Layout:**
```
┌─ Notifications [fixed: 360px, right-aligned] ───────────────────────────────┐
│  Notifications                              [Mark all read]                 │
│  ─────────────────────────────────────────────────────────────────────────  │
│  UNREAD                                                                     │
│  ●  E-Commerce Platform compiled successfully          14m ago     [→]     │
│  ⚠  Blog Platform compilation failed                  1h ago      [→]     │
│  ─────────────────────────────────────────────────────────────────────────  │
│  EARLIER TODAY                                                              │
│  ●  Internal Dashboard compiled                        3h ago      [→]     │
│  ●  CRM System compiled                                5h ago      [→]     │
└─────────────────────────────────────────────────────────────────────────────┘
```

Unread items have a subtle `--surface-accent` background tint. The bell icon shows a badge count of unread items.

---

## Screen 14 — Settings (`/settings`)

**Layout:** Left-nav category layout. Persistent left navigation (120px) + main content area.

**Categories:**
- General (org name, description)
- Compiler (defaults, timeouts, retry behavior)
- API Keys (list, create, revoke)
- Notifications (toast, email, browser)
- Appearance (theme, density, sidebar state)
- Team (quick link to /team)
- Danger Zone (delete org, export data)

No exotic design needed. Correctness and clarity are the only requirements for settings.

---

---

# PHASE 5 — Implementation Plan

## Guiding Principles

Every milestone must satisfy three constraints:
1. **The application must be runnable** after every commit. No "big bang" migrations.
2. **All existing backend API integrations must remain functional** throughout the migration.
3. **Visual regressions must be minimal** — the application should look progressively better, never worse.

## The Dependency Graph

Some work must happen before other work can begin:

```
[M0: Foundation] ──→ [M1: Shell]
[M0: Foundation] ──→ [M2: Design System]
[M1: Shell] ──→ [M3: Core Pages]
[M2: Design System] ──→ [M3: Core Pages]
[M3: Core Pages] ──→ [M4: Advanced Features]
[M4: Advanced Features] ──→ [M5: Polish]
```

---

## Milestone 0 — Foundation (No Visible UI Changes)

**Scope:** Infrastructure changes only. No user-visible changes.

**Work items:**

1. **Consolidate Tailwind configuration**
   - Delete `tailwind.config.js` (keep `tailwind.config.ts`)
   - Extend the config with all design token values

2. **Install design system dependencies**
   - `cmdk` (command palette)
   - `@radix-ui/react-*` (accessible primitives: dialog, popover, dropdown-menu, tooltip, tabs)
   - `recharts` (charts for telemetry and benchmarks)
   - `@tanstack/react-virtual` (virtualization for large lists)
   - `next/font` integration for Inter and JetBrains Mono

3. **Create CSS token file** (`src/styles/tokens.css`)
   - All semantic tokens for dark and light mode
   - All spacing, radius, shadow, duration, easing tokens

4. **Import Google Fonts**
   - Configure `next/font/google` for Inter and JetBrains Mono
   - Replace Arial in `globals.css`

5. **Create `/src/components/ui/` atomic components**
   - `Button` (all variants)
   - `Input`, `Label`, `FormField`
   - `Badge`, `StatusBadge`
   - `Skeleton`
   - `Spinner`
   - `Tooltip`
   - `kbd` (keyboard shortcut display)

**Regression risk:** Zero — no UI renders have changed. Backend untouched.

---

## Milestone 1 — App Shell & Navigation

**Scope:** Replace the entire layout structure and navigation system.

**Work items:**

1. **New app shell layout** (`src/app/dashboard/layout.tsx`)
   - Implement 3-column CSS Grid shell (`global-rail` + `context-panel` + `main`)
   - Persist context panel state in `localStorage`
   - Add contextual right panel zone

2. **Global Rail** (`src/components/layout/GlobalRail.tsx`)
   - 8 icon buttons (Dashboard, Projects, Compiler, Runs, Telemetry, Team, Settings, User)
   - Active state detection using `usePathname()`
   - Notification bell with badge count

3. **Context Panel** (`src/components/layout/ContextPanel.tsx`)
   - Context-aware navigation tree
   - Three states: Global / Project / Run
   - Collapsible with animation

4. **Header Bar** (`src/components/layout/AppHeader.tsx`)
   - Breadcrumb navigation (dynamic, based on route)
   - Search trigger (`⌘K` label)
   - Notification bell
   - User avatar + dropdown

5. **Create all missing routes**
   - `/compiler` → new page
   - `/runs` → new page
   - `/projects` → new page
   - `/projects/[id]` → project overview page
   - `/telemetry` → new page

**Migration approach:**
- The existing `dashboard/layout.tsx` is replaced, not modified
- All existing page files under `dashboard/` remain untouched initially
- New routes wrap existing component logic to prevent regressions
- Test: all existing functionality continues to work in the new shell

**Regression risk:** Low — existing component logic is unchanged, only the shell and routing.

---

## Milestone 2 — Design System & Core Components

**Scope:** Apply the design system. Rebuild shared components.

**Work items:**

1. **Apply token CSS** to all existing components
   - Replace all `slate-*` Tailwind classes with `var(--...)` references
   - Replace `blue-500/600` with `var(--accent)` and `var(--accent-hover)`
   - Replace `emerald-*/red-*/amber-*` with semantic status tokens

2. **Rebuild common components**
   - `StatCard` (dashboard metrics)
   - `ProjectCard` (projects grid)
   - `RunRow` / `RunCard`
   - `PhaseBlock` (compiler trace — new component)
   - `StatusBadge` (consolidated, replaces inline JSX across all files)
   - `EmptyState` (shared component with `icon`, `title`, `body`, `cta` props)
   - `ErrorState` (shared component)
   - `SkeletonCard`, `SkeletonTable`, `SkeletonRow`

3. **Theme toggle** (dark/light)
   - Implement via `next-themes` (already installed)
   - Add toggle to Settings > Appearance
   - Light mode tokens already defined in CSS

**Migration approach:**
- Apply tokens file-by-file, starting with shared components
- Each file migration is independent and can be reviewed separately

**Regression risk:** Medium — visual changes are intentional and sweeping. Functionality unchanged.

---

## Milestone 3 — Core Pages Redesign

**Scope:** Redesign and reimplement the primary pages.

### M3.1 — Login Page

Replace the existing login page with the new design. Backend API call is identical — only the UI changes.

### M3.2 — Dashboard (`/`)

Replace the current `dashboard/page.tsx` with the new dashboard:
- Remove the SpecEditor and ExecutionStatusPanel from the dashboard
- Add: Health Strip, Active Runs section, Recent Projects grid, Build Activity Chart
- The right panel shows the Activity Feed (existing SSE logic migrated here)

**API preservation:** All existing `useProjects()` and `useSSE()` hooks continue to work. The dashboard simply renders differently.

### M3.3 — Compiler (`/compiler`)

New page at `/compiler`. Moves the SpecEditor and ExecutionStatusPanel here.
- Monaco editor is already built — wire to the new layout
- Right panel shows live compilation output (existing `ExecutionStatusPanel` logic, redesigned as `PhaseBlock` components)
- On completion: auto-navigate to the new run's detail page

### M3.4 — Projects (`/projects`)

New page showing all projects. Uses existing `useProjects()` hook.

### M3.5 — Project Overview (`/projects/[id]`)

New page — project-level landing. Shows last run summary, run history, spec summary.

### M3.6 — Run Overview (`/projects/[id]/runs/[runId]`)

Replaces the current `dashboard/project/[id]/page.tsx`. The tabbed interface is replaced by the vertical context panel navigation. Each "tab" becomes its own route.

**Migration approach:**
- The current tab content components (PlanningReportViewer, GraphInspector, ExecutionTimeline, DeploymentPanel, WorkspaceExplorer) are used as-is in the new routes
- They receive the same props as before
- Visual redesign is applied around them
- Horizontal tabs → vertical context panel navigation

**Regression risk:** Medium. Core functionality identical; routing changes may affect deep links.

---

## Milestone 4 — Advanced Features

**Scope:** Command palette, notifications, architecture graph improvements, workspace improvements.

### M4.1 — Command Palette

Install `cmdk`. Build `CommandPalette` component. Register universal shortcut handler (`useHotkeys`).

### M4.2 — Notification Center

Build `NotificationCenter` popover. Connect to SSE stream for real-time notifications.

### M4.3 — Architecture Graph Redesign

Rebuild `GraphInspector` as the full-page `ArchitectureGraph` screen:
- Node filtering panel
- Node detail right panel
- Graph type switching with animated transitions
- Export functionality
- Table view mode

### M4.4 — Workspace Explorer Improvements

- Multi-tab file viewer (tab bar above Monaco)
- File tree keyboard navigation
- File tree search
- File stats section

### M4.5 — Keyboard Shortcuts

Global `useHotkeys` system:
- Universal shortcuts
- Navigation shortcuts (G D, G P, etc.)
- Contextual shortcuts (per page)
- Shortcut reference modal (`?` key)

### M4.6 — Telemetry Page (`/telemetry`)

New page with aggregate metrics, charts, and the full run event table.

**Regression risk:** Low — all new functionality, no modification of existing features.

---

## Milestone 5 — Polish & Production Readiness

**Scope:** Accessibility hardening, responsive behavior, performance, and final visual polish.

### M5.1 — Accessibility Audit

- Audit all components against the ARIA requirements table from Phase 3
- Fix all missing `aria-label` attributes
- Implement proper focus management for all modals/dialogs
- Implement keyboard navigation for file tree and data tables
- Verify WCAG 2.1 AA color contrast ratios

### M5.2 — Responsive Behavior

- Implement mobile bottom tab bar (< 768px)
- Implement collapsible sidebar for tablet
- Fix all hardcoded height values (`h-[500px]`, `h-[600px]`)
- Test at all defined breakpoints

### M5.3 — Performance

- Implement virtualization for long lists (`@tanstack/react-virtual`)
- Lazy-load all heavy components (architecture graph, workspace Monaco instances)
- Verify `@tanstack/react-query` cache invalidation doesn't trigger unnecessary refetches

### M5.4 — Empty & Error States

- Audit every data-bearing section for missing empty states
- Implement all empty states from the Phase 4 spec
- Implement all error states (component-level, page-level, global banner)
- Implement the backend offline banner (replacing the current inline error)

### M5.5 — Final Visual Pass

- Typography audit across all pages
- Spacing consistency audit
- Animation timing review
- Dark/light mode verification

**Regression risk:** Low — all polish work. No functional changes.

---

## Implementation Timeline

| Milestone | Scope | Stability | Visible Changes |
|---|---|---|---|
| M0 — Foundation | Infra + deps | 🟢 Zero risk | None |
| M1 — Shell | Navigation | 🟡 Low risk | Navigation redesigned |
| M2 — Design System | Tokens + components | 🟡 Low risk | Color, type, spacing |
| M3 — Core Pages | Primary screens | 🟠 Medium risk | Major visual overhaul |
| M4 — Advanced | Command palette, etc | 🟡 Low risk | New features added |
| M5 — Polish | A11y, responsive, perf | 🟢 Low risk | Incremental polish |

---

## What Is Preserved

Across all milestones, the following are untouched:

| Preserved | How |
|---|---|
| All backend API endpoints | Frontend API calls remain identical |
| Authentication system (JWT + localStorage) | `api-client.ts` unchanged |
| React Query data layer | All hooks preserved as-is |
| SSE event streaming | `useSSE` hook unchanged |
| Monaco editor integrations | Component wrapped, not replaced |
| React Flow graph rendering | Component wrapped, not replaced |
| Compiler submission logic | `GenesisAPI.runCompiler()` unchanged |
| All environment variables | `NEXT_PUBLIC_API_URL` unchanged |
| Next.js routing (base) | Routes extended, not removed |

---

*End of Document*

*This specification governs all frontend work on Genesis Engine.*  
*Implementation begins at Milestone 0 upon approval.*  
*No design deviations without explicit design review.*
