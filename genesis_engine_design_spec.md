# Genesis Engine — Enterprise Product Design Specification
### Version 1.0 | Principal Design Review

---

## Table of Contents

1. [Phase 1 — Ruthless Audit](#phase-1--ruthless-audit)
2. [Phase 2 — Product Vision](#phase-2--product-vision)
3. [Phase 3 — Complete UX Architecture](#phase-3--complete-ux-architecture)
4. [Phase 4 — Design System](#phase-4--design-system)
5. [Phase 5 — Enterprise Features](#phase-5--enterprise-features)

---

# Phase 1 — Ruthless Audit

## What Was Built vs. What Was Shipped

The team shipped a functional internal tool that **works** but doesn't **feel**. It passes tests. It does not pass scrutiny. Here is a systematic breakdown of every failure mode.

---

### 1.1 Layout

**Current State:**
- A rigid `flex h-screen` two-column layout: `w-64` fixed sidebar + `flex-1` main area.
- The main content is capped at `max-w-7xl mx-auto` — reasonable, but there is zero layout intelligence.
- The dashboard mixes three entirely different conceptual tasks into a single scrolling page: **creating a project** (SpecEditor), **monitoring a run** (ExecutionStatusPanel), and **browsing past projects** (table). These three are different jobs, different user intents, different mental models, crammed into one vertical scroll.
- The `h-[500px]` hardcoded height on the SpecEditor/ExecutionStatusPanel grid is brittle. It clips content on small screens and wastes space on large ones.

**Why This Prevents Enterprise Feel:**
GitHub, Linear, and Vercel do not combine creation with monitoring with browsing on the same page. These are distinct workflows. Mixing them creates cognitive overload and signals that no UX thinking occurred beyond "put it somewhere".

---

### 1.2 Navigation

**Current State:**
- The sidebar contains five links. Four of them (`Projects`, `Execution Logs`, `Deployment`, `Settings`) link to `/dashboard` — the same page. They are functionally dead.
- There is no active-state detection. The `Dashboard` link is hardcoded with `bg-blue-500/10 text-blue-400` regardless of the current route.
- No mobile navigation exists. The sidebar is `hidden md:flex` with zero fallback — on mobile, the entire navigation disappears.
- No breadcrumb system exists at the page level. On the Project Detail page, the only wayfinding is an `← Back to Workspaces` link.
- No workspace switcher. "Default Organization" is a static string.

**Why This Prevents Enterprise Feel:**
A navigation system with four dead links is not a navigation system. It's a placeholder that shipped. Products like Linear, Vercel, and Datadog treat their left nav as the primary orientation layer. Every item is real, leads somewhere distinct, and communicates context. Dead nav links immediately signal to a power user that this is a prototype.

---

### 1.3 Information Hierarchy

**Current State:**
- The dashboard `<h1>` reads `"Dashboard"`. This is the single most generic heading in software.
- The four stat cards (`Total Projects`, `Active Builds`, `Failed Builds`, `Deployed Bundles`) are the right concept, but have no trend indicators, no sparklines, no delta-from-previous, no click targets.
- The "Recent Workspaces" table shows `Project ID` (a raw slug like `demo_project_001`) as the primary display name. The project `name` from the spec is not surfaced.
- The `Integrity` column shows a raw number with no context. `85` out of what? Green/yellow/red?
- The Project Detail header displays `{statusData.id.replace(/_/g, " ")}` as the title — string manipulation as a substitute for actual project naming.

**Why This Prevents Enterprise Feel:**
Information hierarchy in enterprise tools is intentional: primary identifier (project name), secondary (ID/slug), tertiary (metadata). The current implementation inverts this — slugs are primary, names are missing. This is equivalent to GitHub showing commit hashes as branch names.

---

### 1.4 UX Flows

**Current State:**
- **Compiler trigger lives on the dashboard** — the same page as the project list. There is no project creation flow. You submit a JSON spec and a project materialises. There is no naming step, no description prompt, no template selection, no confirmation.
- **Navigation to a project** requires clicking "View Details" in a table row. The project ID in the same row is also a link. Two links to the same destination in the same row — redundant and confusing.
- After running the compiler, the user stays on the dashboard. They must manually find their project in the table. There is no automatic navigation to the new project.
- The Project Detail page has six tabs. The default is `Overview`. The Overview shows `Specification Summary` — this is backwards. The most important thing after a run is its **status, duration, and errors**. The spec is input data, not output.

**Why This Prevents Enterprise Feel:**
Enterprise tools have explicit workflow phases: Create → Configure → Run → Monitor → Inspect → Deploy. The current UX collapses all of these into one page with no phase transitions. It's a control panel, not a product.

---

### 1.5 Visual Hierarchy

**Current State:**
- The color palette is entirely `slate-*` with accent blue (`blue-500`, `blue-600`). This is the default Tailwind dark mode. It is competent but completely generic.
- Typography: `font-family: Arial, Helvetica, sans-serif` in `globals.css`. Arial. In 2026. For an enterprise engineering platform.
- Every card is the same: `bg-slate-900 border border-slate-800 rounded-xl p-5`. Identical elevation. No hierarchy of importance.
- The SpecEditor correctly uses `JetBrains Mono` inside Monaco — but the surrounding UI uses Arial. This creates a jarring font mismatch.
- Icon usage is inconsistent. `Box` is used as the logo. `Box` is a generic shape, not a brand.

**Why This Prevents Enterprise Feel:**
Tools like Vercel, Linear, and Datadog invest heavily in typographic hierarchy. Each level of information has a distinct visual weight. The current implementation is monochrome and flat — every element competes equally for attention.

---

### 1.6 Empty States

**Current State:**
- Empty project list: `"No compiled workspaces found."` — a single sentence in `text-slate-500`. No icon, no CTA, no explanation of what to do.
- ExecutionStatusPanel before a run: Has an icon (`Zap`) and a label — this is the best empty state in the app.
- Graph Inspector empty: A `Share2` icon and `"No graphs available. Has the compiler run yet?"` — a question mark in a UI state is a code smell; the system should know.
- Workspace Explorer empty: `"Select a file to preview"` — functional, acceptable for internal tools, insufficient for a product.

**Why This Prevents Enterprise Feel:**
Great empty states are **product marketing moments**. Linear's empty project list explains what projects do and provides a CTA. Vercel's empty deployments list explains the workflow. The current states are error-message-grade text.

---

### 1.7 Loading States

**Current State:**
- Global: A `Loader2 animate-spin` icon.
- SpecEditor skeleton: Five hardcoded `h-4 bg-slate-800 rounded` divs — not matching the actual editor layout.
- Project list loading: A centered spinner with `"Loading workspaces..."` inside a table `<td>`.
- No page-level loading skeleton. The entire dashboard loads synchronously from React Query. The transition from no data to data is abrupt.
- No optimistic updates.

**Why This Prevents Enterprise Feel:**
Skeleton loaders should mirror the exact layout they're loading. Spinners in table cells break the spatial contract of the table. Enterprise tools like Linear and GitHub show layout-accurate skeletons that don't cause layout shift.

---

### 1.8 Responsiveness

**Current State:**
- Sidebar: `hidden md:flex` with no mobile nav.
- Dashboard stat grid: `grid-cols-1 md:grid-cols-2 lg:grid-cols-4` — acceptable.
- Project detail tabs: `overflow-x-auto` — functional but no touch affordance.
- The `h-[500px]` grids are fixed — not responsive.
- WorkspaceExplorer: `h-[600px]` fixed — will clip on small screens.
- The application is **not usable on mobile**. This is not a requirement failure (it's a desktop tool), but the total absence of even a hamburger menu or drawer means the mobile experience is a blank sidebar with cut-off content.

**Why This Prevents Enterprise Feel:**
Enterprise tools that run on tablets (Datadog, AWS Console) use responsive sidebars, collapsible panels, and drawer navigation. This app renders a broken UI below `md`.

---

### 1.9 Discoverability

**Current State:**
- No command palette.
- No global search.
- No tooltips on any interactive element.
- Keyboard shortcuts exist in the SpecEditor (`Ctrl+S`, `Ctrl+Enter`) but are not documented anywhere visible in the UI — they appear as hidden `xl:inline` text.
- No onboarding flow.
- No contextual help or documentation links.
- The "Format" button in the SpecEditor is a plain text button with no icon and no tooltip. A new user would not know what it does without clicking it.

**Why This Prevents Enterprise Feel:**
Power user discoverability is a competitive advantage. The `⌘K` command palette is now table stakes for developer tools. Its absence is immediately felt.

---

### 1.10 Workflow Efficiency

**Current State:**
- To run a new compilation on an existing project, a user must: navigate to dashboard → scroll down → find the SpecEditor → manually type/paste the JSON → click Run. There is no "re-run" action on the Project Detail page.
- The project table shows the last N projects but there is no search, filter, or sort.
- Artifacts are listed as a static hardcoded array — all 8 files are always shown even if they don't exist for a given project.
- There is no "copy to clipboard" on Project IDs or hash values.
- Tab navigation on the Project Detail page loses scroll position when switching between tabs.

**Why This Prevents Enterprise Feel:**
Every extra click in a workflow is friction. Enterprise tools minimize friction through persistent state, re-run actions, bulk operations, and keyboard-first navigation.

---

### 1.11 Accessibility

**Current State:**
- `Skip to main content` link exists — good.
- `aria-live="polite"` on the status badge — good.
- `role="tablist"` and `role="tab"` on project detail tabs — good.
- **Problems:** No `aria-label` on icon-only buttons (the `Download` buttons in DeploymentPanel). No focus ring visible on most interactive elements (focus rings are `focus:outline-none` without a replacement). The Monaco editor instances are not in the natural tab order. The file tree in WorkspaceExplorer has no keyboard navigation.

**Why This Prevents Enterprise Feel:**
Enterprise procurement requires WCAG 2.1 AA compliance. The current implementation has good intent but incomplete execution. Focus management is broken on several interactive elements.

---

### 1.12 Developer Experience (Codebase)

**Current State:**
- `dashboard/layout.tsx` has hardcoded `hidden md:flex` — not configurable.
- All nav links in `layout.tsx` point to `/dashboard`. This is a TODO that shipped.
- `globals.css` defines exactly 4 CSS variables — essentially no design system.
- No shared component library beyond `button.tsx` and `card.tsx`, which appear unused.
- `tailwind.config.js` AND `tailwind.config.ts` both exist — duplicate config files.
- `PlanningReportViewer.tsx` receives a `report: PlanningReport` prop but the parent component (`project/[id]/page.tsx`) passes `projectId` — the component signature and the call-site are mismatched. This is a bug.
- API base URL hardcoded in multiple components (`DeploymentPanel.tsx` line 9, `hooks.ts` line 90) despite `api-client.ts` already defining a single `API_BASE` constant.

**Why This Prevents Enterprise Feel:**
Code quality is product quality. Dead nav links, API URL duplication, mismatched component interfaces, and duplicate config files indicate the frontend is in a prototype state.

---

### 1.13 Scalability

**Current State:**
- All dashboard data loads into a single component with no pagination.
- The `useSSE("*")` global wildcard subscription invalidates the entire project list on every SSE event — this does not scale beyond ~10 projects.
- There is no concept of workspaces, organizations, or teams.
- There is no role-based UI differentiation.
- No concept of project archiving, pinning, or categorization.

**Why This Prevents Enterprise Feel:**
Enterprise tools are designed for 100s of projects, multiple team members, and role differentiation. The current implementation will degrade at scale.

---

# Phase 2 — Product Vision

## 2.1 Product Philosophy

Genesis Engine is an **AI-powered application compiler**. It takes structured intent (a specification) and produces a complete, deployable application artifact through a multi-agent pipeline.

The product philosophy is:

> **"Show the machine thinking."**

Unlike tools that hide AI complexity behind a chat interface, Genesis Engine exposes the compilation pipeline as a **first-class, inspectable, observable process**. Users are engineers. They want to see the graph. They want to inspect the telemetry. They want to understand what the agents decided and why.

The product must feel like **Datadog met Linear met a code compiler**. Professional. Dense. Precise. Fast.

Three axioms:
1. **Transparency over abstraction** — Every AI decision is visible and inspectable.
2. **Flow over interruption** — Common workflows require zero friction. Rare actions require confirmation.
3. **Density over decoration** — Information density is a feature. Every pixel serves a purpose.

---

## 2.2 User Personas

### Persona 1: The Platform Engineer (Primary)
- **Role:** Senior engineer or tech lead, builds internal tooling.
- **Goal:** Quickly compile, inspect, and deploy specifications. Needs telemetry and graph inspection.
- **Pain point:** Slow feedback loops. Wants to see exactly what the agents did and catch errors in the planning phase.
- **Key workflows:** New compilation → Live monitoring → Graph inspection → Artifact download.

### Persona 2: The Engineering Manager (Secondary)
- **Role:** Manages a team of 5–15 engineers, needs to track build status.
- **Goal:** Dashboard-level overview. Which projects succeeded? Which failed? What's the trend?
- **Pain point:** Too much technical detail, needs summarised health metrics.
- **Key workflows:** Dashboard overview → Project list with status filters → Telemetry summary.

### Persona 3: The Security/Compliance Officer (Tertiary)
- **Role:** Verifies that compiled artifacts meet security requirements.
- **Goal:** Inspect cryptographic hashes, plugin versions, rule engine results.
- **Pain point:** No dedicated security view; data buried in deployment panels.
- **Key workflows:** Artifact integrity → Hash verification → Rule engine audit.

---

## 2.3 Primary Workflows

**Workflow A: New Project Compilation**
```
Command Palette (⌘K → "New Project")
  → Project Creation Modal (name, description, spec)
  → Compiler Console (real-time pipeline view)
  → Auto-navigate to Project Detail on completion
```

**Workflow B: Re-run / Iterate**
```
Project Detail Page
  → "Re-compile" button (top-right)
  → Edit Spec in right panel (Monaco, inline)
  → Re-run → Live status updates in the same panel
```

**Workflow C: Graph Inspection**
```
Project Detail → Graph Explorer tab
  → Select graph type (API / Page / Component / Feature)
  → React Flow canvas with filtering and node details
  → Export graph as PNG / JSON
```

**Workflow D: Artifact Download**
```
Project Detail → Artifacts tab
  → File list with size, checksum, type
  → Single-click download or bulk-select download
```

**Workflow E: Telemetry / Diagnostics**
```
Telemetry section (global or per-project)
  → Timeline of all compiler events
  → Filter by phase, status, duration
  → Click event → Expand details panel
```

---

## 2.4 Navigation Model

**Primary Navigation (Left Sidebar — 64px icon rail + 240px expanded)**

```
[Genesis Logo]
─────────────
⊞ Overview          /
⬡ Projects          /projects
⚙ Compiler          /compiler
⬡ Telemetry         /telemetry
⬡ Benchmarks        /benchmarks
─────────────
⬡ Security          /security
⬡ Team              /team
⬡ Settings          /settings
─────────────
[User Avatar]
[⌘K Search]
```

The sidebar has two states:
- **Collapsed (icon rail):** 64px width, icon + tooltip on hover.
- **Expanded:** 240px width, icon + label. Persisted in localStorage.

**Contextual Right Sidebar (Project Detail):**
Dockable panel for real-time compiler output, collapses to 0px when dismissed.

---

## 2.5 Workspace Model

A **Workspace** is a compiled project output. Each compilation creates one Workspace. A Workspace contains:
- Input specification
- All agent-generated graphs (API, Page, Component, Feature, DB)
- Compilation telemetry
- Deployment manifest
- Cryptographic hashes
- Generated source code (browsable via Workspace Explorer)

Workspaces are **immutable** once created. Re-compilation creates a new Workspace (new ID, preserving history).

---

## 2.6 Project Lifecycle

```
PENDING  →  PLANNING  →  VALIDATING  →  GENERATING  →  PACKAGING  →  SUCCESS
                                                                    ↘
                                                                    FAILED
```

The UI communicates lifecycle state through:
- Color-coded status badge (always visible)
- Phase stepper in Compiler Console
- Live SSE-driven timeline
- Completion notification (toast + browser notification)

---

# Phase 3 — Complete UX Architecture

## 3.1 Login Page

**Layout:** Full-screen centered card. Dark background with subtle gradient mesh. Product wordmark above the form.

**Sections:**
- **Hero area (top of card):** Genesis Engine logotype + tagline "AI-Powered Application Compiler"
- **Form area:** Username/email field, password field, "Remember me" toggle
- **CTA area:** Primary "Sign In" button, "Forgot password?" link
- **Footer:** Version badge, security certification badges (SOC 2, etc.)

**Design details:**
- Background: `#0A0D12` with a subtle radial gradient at center (`rgba(30,58,138,0.15)`)
- Card: Glassmorphism — `backdrop-blur-xl bg-white/5 border border-white/10`
- Logo: Custom SVG mark (hexagon lattice motif representing the graph/compilation concept)
- Error state: Inline error below the affected field, shakes animation on submit failure
- Success state: Button transforms to checkmark, then routes

**Keyboard shortcuts:** `Tab` between fields, `Enter` to submit, `Escape` to clear error.

**Responsive:** Single-column centered, works at 320px minimum width.

---

## 3.2 Dashboard Overview (`/`)

**Layout:** Three-zone layout.
- Top: Metric strip (full width)
- Middle: Activity feed (left 60%) + Build Queue (right 40%)
- Bottom: Recent Projects table (full width)

**Sections:**

**Zone A — Header Bar**
```
[Greeting: "Good morning, Dinusha"]   [⌘K Search]   [+ New Project]   [🔔]   [Avatar]
```

**Zone B — Metric Strip (4 cards horizontal)**
```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  TOTAL PROJECTS │  │  ACTIVE BUILDS  │  │  FAILED TODAY   │  │  DEPLOYED       │
│      47         │  │       3 ●       │  │      1  ⚠       │  │      12         │
│  ▲ 3 this week  │  │  Running now    │  │  Last: 2h ago   │  │  ▲ 5 this week  │
└─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘
```
Cards are clickable and filter the project table below.

**Zone C — Activity Feed (left panel)**
- SSE-driven live feed of compiler events across all projects
- Each entry: timestamp • project name (linked) • event description • phase badge
- "Clear" and "Pause" controls
- Filterable by project, phase, status

**Zone D — Build Queue (right panel)**
- Shows all RUNNING and PENDING builds in real-time
- Each item: project name, phase stepper (mini), elapsed time, "View Live" link
- Empty state: illustration + "No active builds. Start a new compilation."

**Zone E — Recent Projects Table**
- Columns: **Name** | **Status** | **Integrity Score** | **Phase** | **Duration** | **Updated** | **Actions**
- Status column: Color-coded pill (not just text)
- Integrity score: Colored progress bar (0-100) within the cell
- Actions: "Open" button + kebab menu (Re-run, Download, Archive, Delete)
- Table header: Sortable columns, filter dropdown, search input
- Pagination: 20 items per page, load-more button

**Keyboard shortcuts:**
- `N` → New Project
- `⌘K` → Command Palette
- `↑↓` → Navigate table rows (when table focused)
- `Enter` → Open selected project

**Responsive:** On tablet (768-1024px), Build Queue moves below Activity Feed. On mobile, collapses to a list of recent projects only.

---

## 3.3 Projects Page (`/projects`)

**Layout:** Two-zone: Filter sidebar (240px left) + Project grid/list (flex-1 right)

**Filter Sidebar:**
- Status filter: ALL / SUCCESS / FAILED / RUNNING / PENDING (checkboxes)
- Date range picker: Last 24h / 7 days / 30 days / Custom
- Tag filter (if implemented)
- Sort: Newest / Oldest / Name A-Z / Integrity Score

**Project Display (switchable: Grid / List view)**

**Grid View:**
```
┌─────────────────────────┐
│ [Status badge]          │
│                         │
│ Project Name            │
│ demo-ecommerce-app      │
│                         │
│ ████████████░░░ 84/100  │
│ Integrity score         │
│                         │
│ Phase: ●●●●○            │  <- mini stepper
│                         │
│ 2h ago  |  14.2s build  │
│                    [→]  │
└─────────────────────────┘
```

**List View:**
Full-width table with the same columns as the dashboard overview table but with richer filtering and batch selection.

**Toolbar:**
```
[□ Select All]  [Search projects...]  [Status ▾]  [Date ▾]  [Sort ▾]  [⊞ Grid] [☰ List]  [+ New Project]
```

**Batch Actions (appears when items selected):**
`[Archive Selected] [Download All Artifacts] [Delete Selected]`

**Empty State:**
Full-page illustration (stylised hexagonal lattice) + headline "No projects yet" + description + "Create your first project" CTA button.

---

## 3.4 Specifications Page (`/specifications`)

A dedicated library of saved specification templates.

**Layout:** Split panel — Template list (left 320px) + Template editor (right, full Monaco)

**Left Panel:**
- Search bar
- Template cards: name, description, page count, last modified
- "New Template" button
- Import JSON button

**Right Panel (Monaco editor, full height):**
- JSON schema validation (existing Genesis spec schema)
- Toolbar: Format | Validate | Save as Template | Run Compiler
- Breadcrumb: Specifications / [Template Name]

**Purpose:** Decouples spec authoring from compilation. Users can maintain a library of project templates and launch compilations from them.

---

## 3.5 Project Detail Page (`/projects/[id]`)

**Layout:** Three-zone horizontal split.
- **Left:** Fixed project header + vertical tab navigation (not horizontal — horizontal tabs don't scale to 6+ items)
- **Center:** Active tab content (scrollable)
- **Right:** Dockable Compiler Panel (collapsible, shows live status)

**Header (top of page, sticky):**
```
← Projects   /  ecommerce-storefront  /  [Overview]
─────────────────────────────────────────────────────────────────────
[Project Name: E-Commerce Storefront]          [● SUCCESS]  [Re-run ▸]
[ID: ecommerce_storefront_20240628]   [Created: Jun 28, 2026, 2:14 PM]
```

**Left Vertical Tab Rail:**
```
⊞ Overview
⌁ Compiler Trace    (with live dot if RUNNING)
⬡ Graph Explorer
📁 Workspace
📦 Artifacts
📊 Telemetry
📋 Planning Report
🔐 Security
```

**Tab: Overview**
- Build summary card: Status, duration, phases completed, errors/warnings count
- Spec summary: Name, description, pages (chips), components (chips), features (chips)
- Quick stats: Total APIs, Total Entities, Total DB tables, Integrity score (big number)
- Assumptions list (from planning report)

**Tab: Compiler Trace**
- Full visual pipeline stepper (4 phases) at top
- Metrics strip: Total time | Longest phase | Average phase | Agent count
- Timeline: Chronological event list, each event expandable to show `details` JSON
- Filter: by phase, by status (success/fail), by agent
- "Export Trace" button (JSON download)

**Tab: Graph Explorer**
- Graph type selector: API Graph | Page Graph | Component Graph | Feature Graph | DB Schema
- Mode toggle: Flow View (React Flow) | Tree View (JSON tree) | Table View (structured list)
- React Flow canvas with:
  - Node grouping by type
  - Minimap
  - Controls (zoom in/out, fit, lock)
  - Node click → right panel detail drawer
  - Edge labels showing dependency type
  - Search/filter nodes by name
- "Export as PNG" and "Export as JSON" buttons
- Fullscreen mode (`F` key)

**Tab: Workspace Explorer**
- VS Code-style split: File tree (240px left) + Monaco viewer (right)
- File tree: Icons by file type, expand/collapse directories
- Monaco viewer: Read-only, syntax highlighting, line numbers
- Tab bar above Monaco for multiple open files
- Copy file content button
- Search within file (`⌘F`)
- Breadcrumb path above viewer

**Tab: Artifacts**
- Categorised artifact list:
  - **Source** category: `deployment_bundle.zip`
  - **Metadata** category: `deployment_manifest.json`, `planning_report.json`
  - **Telemetry** category: `execution_trace.json`
  - **Graphs** category: `api_graph.json`, `page_graph.json`, `component_graph.json`, `feature_graph.json`
- Each artifact row: Icon | Filename | Category | Description | Size | SHA-256 (truncated, hover for full) | Download button
- Bulk download: "Download All as ZIP" button
- Hash display: truncated, click to copy full hash

**Tab: Telemetry**
- Time-series chart: Event rate over compilation duration (line chart)
- Phase breakdown: Stacked bar or Gantt-style timeline showing phase durations
- Event table: Same as Compiler Trace but with advanced filtering and sorting

**Tab: Planning Report**
- Status banner (SUCCESS/FAILED)
- Metrics grid (8 KPIs in 2×4 grid)
- Rule engine status: Table of all rules (pass/fail/warn), sortable, filterable
- Failed rules: Expanded card with rule name, description, and remediation suggestion
- Graph hashes: Table of all graph files with their SHA-256 hashes

**Tab: Security**
- Cryptographic integrity section: workspace hash, deployment hash (full, copyable)
- Plugin version manifest table: Plugin | Version | Hash | Status
- Rule engine coverage: API coverage | DB coverage | UI coverage | Overall (donut chart)
- Audit trail: Timestamps for each compilation phase

**Right Dockable Panel (Compiler Panel):**
- Visible when a compilation is RUNNING or just completed
- Shows: Phase stepper + live event feed (auto-scrolls)
- Collapsed state: 48px right edge strip with pulsing indicator
- Close button (persists collapsed state in localStorage)

**Breadcrumbs:** `Projects → [Project Name] → [Active Tab]`

**Keyboard shortcuts:**
- `1`–`8` → Switch to tab by number
- `R` → Re-run compiler
- `F` → Fullscreen graph (when on Graph tab)
- `D` → Download all artifacts
- `⌘F` → Search in workspace file (when on Workspace tab)
- `Escape` → Close expanded panels/modals

**Responsive:** On tablet, right panel becomes a bottom drawer. Vertical tabs become a horizontal scrollable tab bar. On mobile, content-only view with a hamburger to reach tabs.

---

## 3.6 Compiler Console (`/compiler`)

A dedicated page for **launching new compilations** — separate from project monitoring.

**Layout:** Two-panel split: Spec Editor (left 55%) | Live Output (right 45%)

**Left Panel — Spec Editor:**
- Toolbar: New | Open Template | Save as Template | Format | Validate | **Run Compiler ▸**
- Monaco editor (full height, JSON mode with schema validation)
- Status bar: Cursor position | JSON validity indicator | Last validated timestamp

**Right Panel — Live Output:**
- Shown in "idle" state before run: Empty state with "Submit a spec to begin compilation"
- During run:
  - Phase stepper at top (Planning → Validation → Generation → Packaging)
  - Live event feed (auto-scrolls)
  - Metrics strip (elapsed time, events received)
- After completion:
  - Success/Failure banner
  - "View Project →" button (navigates to new project's detail page)
  - "Download Artifacts" button
  - "Run Again" button

**Keyboard shortcuts:**
- `Ctrl+Enter` → Run Compiler
- `Ctrl+S` → Validate
- `Ctrl+Shift+F` → Format

---

## 3.7 Telemetry Page (`/telemetry`)

**Layout:** Full-width, data-dense, no sidebar panels.

**Sections:**

**Top Bar:**
```
[Time Range: Last 24h ▾]  [Project: All ▾]  [Phase: All ▾]  [Auto-refresh: 30s ▾]
```

**Metrics Strip (6 cards):**
Total Compilations | Success Rate | Average Duration | P95 Duration | Agent Errors | Total Events

**Chart Row (3 charts):**
- Build volume over time (bar chart, hourly buckets)
- Success vs Failure rate (line chart, dual axis)
- Phase duration distribution (box plot per phase)

**Event Table:**
- All compilation events across all projects
- Columns: Timestamp | Project | Phase | Event | Duration | Status | Details
- Row click → expand inline to show `details` JSON
- Filterable, sortable, paginated (50 per page)
- CSV export button

---

## 3.8 Benchmarks Page (`/benchmarks`)

**Layout:** Full-width, tabbed.

**Tab: Performance**
- Average compile time per project (bar chart)
- Phase duration breakdown over time (stacked area chart)
- Slowest compilations table: Project | Duration | Phase | Date

**Tab: Quality**
- Integrity score distribution (histogram)
- Rule pass/fail rates by rule name (bar chart)
- Trend: Integrity score over time (line chart)

**Tab: Comparisons**
- Select 2 projects → side-by-side comparison of key metrics
- Table: Metric | Project A | Project B | Delta

---

## 3.9 Security Page (`/security`)

**Layout:** Single column, card-based sections.

**Sections:**
- **Authentication Audit Log:** Table of login events (user, timestamp, IP, result)
- **API Access Log:** Table of API calls (endpoint, user, timestamp, response code)
- **Artifact Integrity:** All projects with their deployment hashes — flag any hash mismatches
- **Rule Engine Health:** Summary of rule coverage scores across all projects
- **Active Sessions:** List of current active tokens, with "Revoke" action

---

## 3.10 User Management Page (`/team`)

**Layout:** Two sections stacked.

**Section A — Members Table:**
- Columns: Avatar | Name | Username | Role | Last Active | Actions
- Roles: Admin | Engineer | Viewer
- Actions: Edit Role (dropdown) | Remove User

**Section B — Invitations:**
- Pending invite list (email, role, sent date, resend/revoke)
- "Invite Member" form: email input + role selector + "Send Invite" button

---

## 3.11 Settings Page (`/settings`)

**Layout:** Left nav (settings categories) + right content panel.

**Categories:**
- **General:** Workspace name, description, API URL configuration
- **Compiler:** Default spec template, retry behaviour, timeout settings
- **Notifications:** Toast preferences, email notifications, browser notifications
- **API Keys:** Create/revoke API keys for programmatic access
- **Appearance:** Theme (Light/Dark/System), sidebar state, density (Compact/Default/Comfortable)
- **Danger Zone:** Delete workspace, export all data

---

# Phase 4 — Design System

## 4.1 Typography

**Primary Typeface:** `Inter` (via Google Fonts)
- Reason: Used by Linear, Vercel, Notion, Figma. Exceptional legibility at small sizes. Best-in-class numerals.

**Monospace Typeface:** `JetBrains Mono` (via Google Fonts)
- Reason: Best monospace for code. Already used inside Monaco. Apply to all code, hashes, IDs, terminal output.

**Type Scale (in rem):**

| Token        | Size   | Weight | Line Height | Use Case |
|--------------|--------|--------|-------------|----------|
| `display-xl` | 3rem   | 700    | 1.1         | Page heroes |
| `display-lg` | 2.25rem| 700    | 1.15        | Section headings |
| `heading-xl` | 1.5rem | 600    | 1.25        | Card headers, h1 |
| `heading-lg` | 1.25rem| 600    | 1.3         | Panel headers |
| `heading-md` | 1rem   | 600    | 1.35        | Section titles |
| `heading-sm` | 0.875rem| 600   | 1.4         | Table headers |
| `body-lg`    | 1rem   | 400    | 1.6         | Primary body |
| `body-md`    | 0.875rem| 400   | 1.6         | Secondary body |
| `body-sm`    | 0.75rem | 400   | 1.5         | Captions, labels |
| `label-sm`   | 0.6875rem| 600  | 1.4         | Uppercase tracking labels |
| `code-md`    | 0.875rem| 400   | 1.6         | Inline code, IDs |
| `code-sm`    | 0.75rem | 400   | 1.5         | Hash values |

---

## 4.2 Color System

**Background scale (dark theme primary):**

| Token              | Hex       | Use |
|--------------------|-----------|-----|
| `bg-void`          | `#060810` | Page background |
| `bg-base`          | `#0C0F1A` | App shell |
| `bg-surface`       | `#111827` | Cards, panels |
| `bg-elevated`      | `#1A2033` | Dropdown, overlays |
| `bg-overlay`       | `#1F2A3C` | Modals, dialogs |
| `bg-hover`         | `#243147` | Hover states |
| `bg-selected`      | `#2A3A55` | Active/selected states |

**Border scale:**

| Token            | Hex                    | Use |
|------------------|------------------------|-----|
| `border-subtle`  | `rgba(255,255,255,0.04)` | Dividers, card borders |
| `border-default` | `rgba(255,255,255,0.08)` | Component borders |
| `border-strong`  | `rgba(255,255,255,0.14)` | Focused states |
| `border-accent`  | `rgba(109,137,255,0.4)` | Active focus ring |

**Text scale:**

| Token            | Value | Use |
|------------------|-------|-----|
| `text-primary`   | `#F0F4FF` | Headings, primary content |
| `text-secondary` | `#8B9AB5` | Labels, descriptions |
| `text-tertiary`  | `#4E5D7A` | Placeholders, timestamps |
| `text-disabled`  | `#2E3A4E` | Disabled state |

**Accent palette (Genesis Blue — primary brand):**

| Token              | Hex       | Use |
|--------------------|-----------|-----|
| `accent-blue-50`   | `#E8EDFF` | Light tint, backgrounds |
| `accent-blue-400`  | `#6D89FF` | Primary accent |
| `accent-blue-500`  | `#4F6EF7` | Buttons, links |
| `accent-blue-600`  | `#3A55E8` | Button hover |
| `accent-blue-900`  | `#111E4A` | Accent surface |

**Semantic palette:**

| Token         | Hex       | Use |
|---------------|-----------|-----|
| `success-400` | `#34D399` | Success states |
| `success-900` | `#052E16` | Success background |
| `warning-400` | `#FBBF24` | Warning states |
| `warning-900` | `#2D1E00` | Warning background |
| `error-400`   | `#F87171` | Error states |
| `error-900`   | `#2A0A0A` | Error background |
| `info-400`    | `#60A5FA` | Info states |

**Note on the accent choice:** The current `blue-500` (#3B82F6) is generic Tailwind blue. The new `accent-blue-400` (#6D89FF) is a slightly purple-shifted blue that reads as more premium and distinct. It's the same hue family used by Linear and Raycast.

---

## 4.3 Spacing System

Base unit: `4px` (0.25rem). All spacing values are multiples.

| Token  | Value    | Rem      | Use |
|--------|----------|----------|-----|
| `sp-0` | 0px      | 0        | Reset |
| `sp-1` | 4px      | 0.25rem  | Micro gaps |
| `sp-2` | 8px      | 0.5rem   | Icon-label gap |
| `sp-3` | 12px     | 0.75rem  | Inline spacing |
| `sp-4` | 16px     | 1rem     | Default padding |
| `sp-5` | 20px     | 1.25rem  | Card padding (compact) |
| `sp-6` | 24px     | 1.5rem   | Card padding (default) |
| `sp-8` | 32px     | 2rem     | Section spacing |
| `sp-10`| 40px     | 2.5rem   | Large section gaps |
| `sp-12`| 48px     | 3rem     | Page section spacing |
| `sp-16`| 64px     | 4rem     | Header height |
| `sp-20`| 80px     | 5rem     | Hero sections |

---

## 4.4 Elevation System

Not using `box-shadow` for depth. Using background-layer differentiation instead (more accurate in dark UIs):

| Level | Background    | Border                        | Blur   | Use |
|-------|---------------|-------------------------------|--------|-----|
| 0     | `bg-void`     | None                          | —      | Page background |
| 1     | `bg-surface`  | `border-subtle`               | —      | Cards, panels |
| 2     | `bg-elevated` | `border-default`              | —      | Dropdowns |
| 3     | `bg-overlay`  | `border-strong`               | 8px    | Modals |
| 4     | —             | `border-accent` + glow        | 24px   | Focused inputs, active panels |

Shadow tokens (supplementary, for floating elements):
- `shadow-sm`: `0 1px 3px rgba(0,0,0,0.5)`
- `shadow-md`: `0 4px 12px rgba(0,0,0,0.5)`
- `shadow-lg`: `0 8px 32px rgba(0,0,0,0.7)`
- `shadow-glow-blue`: `0 0 20px rgba(79,110,247,0.3)`

---

## 4.5 Cards

**Card Anatomy:**
```
┌──────────────────────────────────────┐  ← border-subtle
│  [Icon/Badge]  Card Title     [Menu] │  ← header zone, bg-surface, border-bottom
│────────────────────────────────────  │
│  Content area                        │  ← body zone
│                                      │
│  [Secondary action]   [Primary CTA]  │  ← footer zone (optional)
└──────────────────────────────────────┘
```

**Card Variants:**
- `card-default`: Elevation level 1, `rounded-xl`, `p-6`
- `card-compact`: Elevation level 1, `rounded-lg`, `p-4`
- `card-interactive`: `card-default` + `cursor-pointer` + hover transition (`bg-hover` on hover, `scale(1.002)`)
- `card-stat`: Compact, icon left, value large, label small, delta indicator
- `card-empty`: Dashed border (`border-dashed border-strong`), centered content, illustration slot

---

## 4.6 Tables

**Standard Table:**
```
┌────────────────────────────────────────────────────────────────┐
│  [□] Name ▴    Status     Score     Updated    Duration  [⋯]   │  ← header
├────────────────────────────────────────────────────────────────┤
│  [□] my-project  ● SUCCESS  ████ 84  2h ago    14.2s     [⋯]   │  ← row
│  [□] another     ○ RUNNING  ░░░░ –   running   elapsed   [⋯]   │
└────────────────────────────────────────────────────────────────┘
```

Rules:
- Header: `text-label-sm uppercase tracking-widest text-tertiary`, `border-bottom border-subtle`
- Row hover: `bg-hover` transition 100ms
- Selected row: `bg-selected border-l-2 border-accent`
- Actions column: Always right-aligned, reveal on row hover
- No visible row borders (vertical dividers create visual noise)
- Alternating row backgrounds are NOT used (adds noise, reduces scannability)

---

## 4.7 Forms

**Input:**
```css
background: bg-base
border: 1px solid border-default
border-radius: 8px
padding: 10px 14px
color: text-primary
font-size: body-md

focus:
  border-color: accent-blue-400
  box-shadow: 0 0 0 3px rgba(79,110,247,0.2)

error:
  border-color: error-400
  box-shadow: 0 0 0 3px rgba(248,113,113,0.2)
```

**Label:** `body-sm` weight 500, `text-secondary`, `mb-2` below label

**Helper text:** `body-sm text-tertiary`, displayed below input always (not only on error)

**Error text:** `body-sm text-error-400`, with icon, appears below helper text slot

**Form layout:** Labels above inputs, never inline (inline labels break when inputs are long).

**Select/Dropdown:** Matches input styling. Custom styled to match the design system — no browser-native dropdowns.

---

## 4.8 Dialogs / Modals

**Structure:**
- Backdrop: `bg-void/80 backdrop-blur-sm`
- Dialog card: Elevation level 3, `max-w-lg w-full`, `rounded-2xl`
- Header: Title (`heading-md`) + optional subtitle (`body-md text-secondary`) + close button
- Body: Scrollable if content exceeds 60vh
- Footer: Left-aligned secondary action + right-aligned primary action

**Variants:**
- `dialog-default`: Standard information/form dialog
- `dialog-destructive`: Red-tinted header, destructive primary button
- `dialog-confirm`: Two-action: Cancel + Confirm (no form content)

**Animation:**
- Enter: `scale(0.97) opacity(0)` → `scale(1) opacity(1)`, duration 150ms, easing `ease-out`
- Exit: Reverse, duration 100ms

---

## 4.9 Notifications / Toasts

Using `sonner` (already installed). Configuration:

```tsx
<Toaster
  theme="dark"
  position="bottom-right"
  richColors
  gap={8}
  toastOptions={{
    style: {
      background: 'var(--bg-elevated)',
      border: '1px solid var(--border-default)',
      color: 'var(--text-primary)',
      fontFamily: 'Inter, sans-serif',
    }
  }}
/>
```

**Toast types:**
- `success`: Green left border, check icon
- `error`: Red left border, X icon, persists for 8s (not 4s default)
- `warning`: Amber left border
- `info`: Blue left border
- `loading`: Spinner, no auto-dismiss, must be explicitly dismissed via `.dismiss(id)`

**System notifications (for long-running operations):**
Use `toast.promise()` pattern for compiler runs:
```
Compiling "my-project"...  →  Compilation succeeded  (or failed)
```

---

## 4.10 Progress Indicators

**Phase Stepper (horizontal):**
```
●─────●─────●─────○
Plan  Validate  Generate  Package
                ↑ current
```
- Past: Filled circle, accent-blue, checkmark icon
- Current: Animated pulse ring around filled circle
- Future: Empty circle, `border-default`
- Error: Red filled circle, X icon

**Progress Bar:**
- Height: 4px (`h-1`)
- Background: `bg-surface`
- Fill: Gradient (`accent-blue-400` → `accent-blue-600`)
- Indeterminate variant: Animated shimmer sweep

**Inline Loading (spinner):**
- 16px spinner for inline use (`w-4 h-4`)
- 24px for section loading
- 40px for full-page loading
- All use `animate-spin` at `0.75s linear infinite` (slightly slower than default, less aggressive)

**Skeleton loaders:**
- Match exact geometry of the content they replace
- `bg-surface` base + `bg-elevated` shimmer overlay
- Animation: `shimmer` keyframe (gradient slide left to right, 1.8s loop)

---

## 4.11 Badges / Status Pills

**Status badges:**
```
● SUCCESS    →  bg-success-900 text-success-400 border border-success-400/20
● RUNNING    →  bg-accent-blue-900 text-accent-blue-400 border border-accent-blue-400/20 (with pulse dot)
⚠ FAILED     →  bg-error-900 text-error-400 border border-error-400/20
○ PENDING    →  bg-surface text-tertiary border border-default
```

**Tag badges (for categorisation):**
- `px-2 py-0.5 rounded-md text-xs font-medium`
- Palette: 8 preset colors (blue, purple, green, amber, red, pink, cyan, slate)

**Count badges (notification counts):**
- `w-5 h-5 rounded-full bg-error-400 text-white text-xs font-bold` (red dot)
- Position: `absolute -top-1 -right-1` on icon buttons

---

## 4.12 Charts and Graphs

**Chart library recommendation:** `Recharts` (React-native, composable, good with dark themes)

**Chart style system:**
```ts
const chartTheme = {
  background: 'transparent',
  gridColor: 'rgba(255,255,255,0.06)',
  axisColor: 'var(--text-tertiary)',
  axisFont: { fontFamily: 'JetBrains Mono', fontSize: 11 },
  tooltip: {
    background: 'var(--bg-elevated)',
    border: '1px solid var(--border-default)',
    borderRadius: '8px',
  }
}
```

**Color sequences for data series:**
1. `#6D89FF` (Genesis Blue)
2. `#34D399` (Emerald)
3. `#FBBF24` (Amber)
4. `#F87171` (Red)
5. `#A78BFA` (Purple)
6. `#60A5FA` (Sky)

**Chart types used:**
- **Bar chart** (build volume)
- **Line chart** (trends, success rate)
- **Area chart** (filled, for cumulative metrics)
- **Pie/Donut chart** (coverage scores, phase breakdown)
- **Gantt/Timeline** (phase durations per build — custom React component)

---

## 4.13 Icons

**Library:** `lucide-react` (already installed). Consistent weight.

**Icon sizing:**
- `w-3 h-3` (12px): Inline text icons, badge icons
- `w-4 h-4` (16px): Button icons, list item icons
- `w-5 h-5` (20px): Navigation icons, card action icons
- `w-6 h-6` (24px): Feature icons, empty state icons
- `w-8 h-8` (32px): Section header icons
- `w-12 h-12` (48px): Illustration icons (empty states)

**Custom icons needed:**
- Genesis Engine logotype (SVG): Hexagonal lattice/node graph motif
- Phase icons: unique icons for Planning, Validation, Generation, Packaging

---

## 4.14 Animations and Transitions

**Principles:**
- Animations communicate meaning, not decoration.
- All transitions: `ease-out` curve (fast start, slow end — feels responsive).
- Max duration for UI transitions: 200ms. For page transitions: 300ms.
- Respect `prefers-reduced-motion` — all animations should degrade to instant when set.

**Transition tokens:**
```css
--transition-fast: 100ms ease-out;      /* hover states, focus rings */
--transition-default: 150ms ease-out;   /* color changes, border changes */
--transition-medium: 200ms ease-out;    /* layout shifts, panel resizes */
--transition-slow: 300ms ease-out;      /* page transitions, modals */
```

**Micro-animations:**
- Nav item hover: Background fades in, left indicator slides in (150ms)
- Button hover: Background shifts (100ms), subtle upward translate `translateY(-1px)` (150ms)
- Card hover (interactive): `translateY(-2px)` + shadow increase (150ms)
- Status badge (RUNNING): Pulsing dot — CSS `animate-pulse` at 2s period
- Phase stepper current step: Outer ring pulse animation (`scale(1) → scale(1.15) → scale(1)`, 2s loop)
- Live event entry: `slide-in-from-bottom-2 fade-in` (200ms, stagger 30ms per item)
- Toast entry: `slide-in-from-right-4` (200ms)
- Command palette entry: `scale(0.96) opacity(0) → scale(1) opacity(1)` (150ms)

**Framer Motion (already installed):** Use for:
- Page transitions (route changes)
- Modal enter/exit
- Command palette
- Dockable panel resize
- Number counter animation on stat cards (`useMotionValue` + `useSpring`)

---

## 4.15 Loading Skeletons

Every data-bearing section must have a skeleton that matches its exact layout geometry.

**Stat card skeleton:**
```
┌──────────────────────┐
│ ██████ (icon)        │  ← 32x32 rounded shimmer
│                      │
│ ████████████         │  ← 40% width, h-8 (big number)
│ ██████               │  ← 25% width, h-3 (label)
└──────────────────────┘
```

**Table skeleton:**
- Header row: 5 cells of varying widths (20%, 10%, 15%, 20%, 10%)
- 5 body rows each matching header cell widths
- All cells: `h-4 rounded bg-surface shimmer`

**Project detail header skeleton:**
- Title placeholder: `h-8 w-64 rounded`
- ID placeholder: `h-4 w-48 rounded`
- Status badge placeholder: `h-6 w-20 rounded-full`

**Skeleton animation (CSS):**
```css
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
.skeleton {
  background: linear-gradient(
    90deg,
    var(--bg-surface) 0%,
    var(--bg-elevated) 50%,
    var(--bg-surface) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.8s linear infinite;
}
```

---

## 4.16 Empty States

Every empty state must contain:
1. An **illustration** (icon-based, consistent with brand)
2. A **headline** (what is empty, not why)
3. A **body** (what can be done here, what value will appear)
4. A **CTA button** (primary action)

**Examples:**

**No projects:**
```
        [Hexagonal lattice icon, 64px, text-tertiary]
        No projects yet
        Launch your first compilation to see projects here.
        [+ New Project]
```

**No active builds:**
```
        [Play circle icon, 48px, text-tertiary]
        No active compilations
        All quiet. Start a new project to see live build activity.
        [Go to Compiler]
```

**No artifacts:**
```
        [Package icon, 48px, text-tertiary]
        Artifacts not generated
        Run the compiler to generate deployment artifacts.
        [Re-run Compiler]
```

**Graph not available (flow mode):**
```
        [Network icon, 48px, text-tertiary]
        Graph structure unresolvable
        This output could not be mapped to a visual graph.
        Switch to Tree View for raw inspection.
        [Switch to Tree View]
```

---

## 4.17 Error States

**Inline field error:**
```
[ Input value          ]
  ⚠ Field name is required.
```

**Component-level error (card):**
```
┌─────────────────────────────────────┐
│  ⚠  Failed to load data            │
│  Error: Cannot connect to backend   │
│  [Retry]   [Dismiss]               │
└─────────────────────────────────────┘
```

**Page-level error (full section):**
```
          ⊘
    Something went wrong
    We couldn't load this workspace.
    Error code: 404 / Workspace not found

    [← Back to Projects]   [Retry]
```

**Backend offline banner (global, top of page):**
```
┌──────────────────────────────────────────────────────────────────────┐
│  ⚠  Backend Offline  —  Cannot reach Genesis Engine API on :8000    │
│  Run: uvicorn main:app --reload (in /backend)           [Dismiss ✕]  │
└──────────────────────────────────────────────────────────────────────┘
```
This replaces the current inline error in the dashboard. It is positioned as a global banner below the top header, collapsible, persists across page navigation while the backend is down.

---

## 4.18 Success States

**Inline success (form submit):**
- Button transforms: `Loader → ✓ Saved` for 2 seconds, then reverts
- Optional: Green flash on the affected input's border

**Compilation success (toast + banner):**
- Toast: `✓ Compilation complete · ecommerce-app · 14.2s` with "View Project" action button
- Project Detail banner (replaces RUNNING state): `✓ Build succeeded in 14.2s`

**Download success:**
- Toast: `✓ Downloading deployment_bundle.zip`

---

# Phase 5 — Enterprise Features

## 5.1 Command Palette (`⌘K` / `Ctrl+K`)

The single most important power-user feature. Opens a floating modal centered on screen.

**Behaviour:**
- Opens with `⌘K` or `Ctrl+K` from any page
- Focus traps inside
- `Escape` to close
- Real-time fuzzy search over all commands and data

**Command categories:**
```
⬡  Navigation
      Go to Dashboard
      Go to Projects
      Go to Compiler
      Go to Telemetry
      Open Project: [name] ...   ← recent projects, dynamically populated

⚙  Actions
      New Project
      Run Compiler
      Download All Artifacts
      Re-run Last Project
      Export Telemetry

⬡  Quick Jump
      [Project Name] → Overview
      [Project Name] → Artifacts
      [Project Name] → Graph Explorer

⬡  Settings
      Toggle Theme
      Toggle Sidebar
      Open API Settings
```

**Implementation:** Custom React component using `cmdk` library (the gold standard, used by Vercel, Linear, shadcn/ui). Already compatible with TailwindCSS.

---

## 5.2 Global Search

Full-text search across:
- Project names and IDs
- Specification content
- Event types in telemetry
- Artifact names

Accessible from the header search bar or via `⌘K`. Results grouped by type (Projects, Events, Artifacts) with keyboard navigation.

---

## 5.3 Dockable Panels

**Compiler Live Panel (Project Detail):**
- Right-side panel, 400px default width
- Drag handle to resize (200px–600px)
- Collapse button: slides panel out, shows 48px activator strip
- Persists open/closed state and width in `localStorage`
- When panel is open: main content area shrinks fluidly

**Implementation:** CSS grid layout (`grid-template-columns: 1fr [panel-width]`) driven by a resize observer + draggable handle.

---

## 5.4 Multi-tab Workspace Explorer

Replace the single-file Monaco viewer with a proper tab bar:

```
[package.json ×] [App.tsx ×] [index.css ×] [+]
─────────────────────────────────────────────
[Monaco editor content for active tab]
```

- Click file in tree → opens in new tab
- Click existing tab → switches to it
- `×` to close
- Middle-click to close
- Tab overflow: `overflow-x-auto` with scroll arrows
- `⌘W` to close current tab
- `⌘Tab` to cycle through open tabs

---

## 5.5 Persistent Layouts

All layout preferences persisted to `localStorage`:
- Sidebar: expanded / collapsed
- Compiler panel: open / closed / width
- Dashboard: grid view / list view
- Table column widths (resizable columns for power users)
- Last active tab on Project Detail page

**Implementation:** Single `useLayoutPreferences` hook that reads/writes to a `layout_prefs` key in localStorage, with a `useEffect` to apply on mount.

---

## 5.6 Activity Feed

A global, persistent, SSE-driven stream of all compilation events visible from the dashboard. Features:
- Filter by project, phase, status
- Pause/resume live updates
- Clear button
- "Jump to project" on any event
- Timestamps in relative format (`2 minutes ago`) with tooltip showing absolute time

---

## 5.7 Notification System

**In-app notification center (bell icon in header):**
- Opens a right-aligned dropdown panel
- Sections: Unread (highlighted) / All
- Notification types:
  - Compilation complete (success/fail) with project link
  - Compilation started
  - Backend offline/online
- "Mark all read" button
- Badge count on bell icon

**Browser notifications (opt-in):**
- Request permission on first successful compilation
- Send `Notification` API push for: compilation success, compilation failure

**Toast notifications** (already spec'd in 4.9)

---

## 5.8 Build Queue Panel (Dashboard)

A real-time panel on the dashboard showing:
- All RUNNING compilations
- Each item: mini phase stepper + elapsed timer + project name
- "View Live" → navigates to Project Detail with Compiler Panel open
- "Cancel" action (if backend supports it)
- Empty state: `No active builds`

---

## 5.9 Live Logs Stream

Within the Compiler Trace tab and the Compiler Panel:
- Auto-scroll to bottom when new events arrive (with "scroll to top" button appearing)
- User can scroll up — auto-scroll pauses
- "Jump to bottom" sticky button appears when scrolled up (like Discord, Slack)
- Log entries are virtualised for performance (use `@tanstack/react-virtual`) — supports 10,000+ events without DOM bloat

---

## 5.10 Diagnostics Panel

Accessible from any component-level error state. Shows:
- Last API response details (status, headers, body)
- Active queries (React Query DevTools style, but embedded)
- SSE connection status + reconnect count
- Browser info
- Backend version (from health endpoint)

---

## 5.11 Resource Usage (Sidebar Footer)

A persistent indicator in the sidebar footer showing:
```
● Connected  |  API: 24ms  |  Events: 3/s
```
Clicking opens a detailed diagnostic panel.

---

## 5.12 Compiler Metrics Bar

Visible on any page that shows a project in RUNNING state:
```
[Planning ●●●●●] [Validating ●●●●○] [Generating ○○○○○] [Packaging ○○○○○]  |  Elapsed: 14.2s
```
This is a sticky notification bar below the main header (not a toast) while a compilation is active.

---

## 5.13 Timeline View (Gantt)

In the Telemetry tab and Benchmarks tab:
- A horizontal Gantt chart showing each compilation phase as a bar
- X-axis: time (seconds)
- Y-axis: phases
- Bars color-coded by phase
- Click bar → scrolls Trace tab to that phase's events
- Hover → tooltip with phase name, start time, duration

**Implementation:** Custom SVG component (Recharts doesn't have native Gantt). ~150 lines of code, re-usable.

---

## 5.14 Build History Timeline

On the Project Detail page, a mini timeline of all past compilations for the same project ID:
```
[Jun 28] ● Success 14.2s → [Jun 27] ⚠ Failed 8.1s → [Jun 26] ● Success 22.4s
```
Clicking any point navigates to that specific compilation's project detail.

---

## 5.15 Recent Projects (Sidebar)

The bottom section of the sidebar (below main nav) shows the last 5 opened projects:
```
─────────────
  RECENT
  ● ecommerce-app
  ⚠ blog-platform
  ● crm-system
─────────────
```
Persisted in localStorage. Clicking navigates directly.

---

## 5.16 Favourites / Pinning

Any project can be pinned:
- Pin icon on every project card and table row
- Pinned projects appear at the top of the project list, always
- Pinned projects appear in a "Favourites" section in the sidebar
- Persisted in localStorage (or backend user preferences when user system is expanded)

---

## 5.17 Keyboard-First Navigation

Full keyboard navigation map:

| Shortcut | Action |
|----------|--------|
| `⌘K` | Open Command Palette |
| `⌘/` | Toggle sidebar |
| `N` | New project (when not in input) |
| `G then D` | Go to Dashboard (vim-style) |
| `G then P` | Go to Projects |
| `G then C` | Go to Compiler |
| `G then T` | Go to Telemetry |
| `↑ ↓` | Navigate table rows |
| `Enter` | Open selected row |
| `R` | Re-run (on project detail) |
| `D` | Download artifacts (on project detail) |
| `1`–`8` | Switch project detail tabs |
| `F` | Fullscreen graph |
| `⌘F` | Find in file (workspace explorer) |
| `⌘W` | Close active file tab |
| `Escape` | Close modal/palette/panel |

Implement with a global `useHotkeys` hook that respects focus context (shortcuts are disabled when typing in inputs).

---

# Implementation Priority Order

When implementing incrementally, this is the recommended priority:

## Tier 1 — Foundation (Do First)
1. Design system tokens (CSS variables, typography, color palette)
2. Google Fonts integration (Inter + JetBrains Mono)
3. Sidebar: icon rail mode, active-state detection, all links functional with real routes
4. Command Palette (`cmdk`)

## Tier 2 — Core UX Fixes
5. Separate `/compiler` page (move SpecEditor off dashboard)
6. Dashboard redesign: metrics strip + activity feed + build queue + project table
7. Project Detail: vertical tab rail, project name as title (not slug), Overview tab redesign
8. Skeleton loaders for all data sections
9. Empty states for all sections

## Tier 3 — Power Features
10. Workspace Explorer: multi-tab file viewer
11. Dockable compiler panel
12. Global notification center
13. Telemetry page (full)
14. Timeline / Gantt chart

## Tier 4 — Enterprise Polish
15. Persistent layout preferences
16. Keyboard shortcuts system
17. Global search
18. Benchmarks page
19. Security page
20. User management page

---

> **This specification is the source of truth for the Genesis Engine frontend redesign.**
> No implementation decisions should deviate from this document without explicit design review.
> Backend architecture is preserved. All changes are frontend-only.
