# Genesis Engine
## Complete Product UX Architecture Specification
### Version 2.0 — Ground-Up Redesign

> *"Software is the collective hallucination of an engineering team. Genesis makes it a precise compilation."*

**Document Status:** Design Review Draft  
**Audience:** Senior Frontend Engineers, Designers, Product Managers  
**Scope:** Complete product redesign from first principles. No implementation code.

---

# Part I: Reference Analysis

Before designing Genesis, we must understand *why* the reference products feel the way they do — not what they look like, but what mental models they create and what interaction philosophies they embody.

## Why Linear Works

Linear's genius is not its dark theme or its fast animations. It's the **speed contract**. Linear treats every interaction as if bandwidth is zero and latency is instantaneous. Every action updates the UI before the server confirms it. The interface never waits for the network. This creates a product that feels *light* — like writing in a notebook rather than submitting a form.

The second insight: **the left sidebar is a workspace map, not a navigation menu**. You're not navigating between pages — you're moving within a spatial hierarchy (Workspace → Team → Project → Issue). The sidebar collapses into a rail but never disappears. You are always located somewhere in the hierarchy.

The third insight: Linear's **keyboard shortcuts are the real product**. The mouse is optional. Every action has a chord. The product rewards investment.

**What Genesis can learn:** The feeling of speed, the spatial navigation model, the keyboard-first philosophy.

## Why Vercel Works

Vercel's dashboard is not a project list. It's a **deployment feed**. The most recent deployment is always visible. The "Visit" button is always one click away. Status (building / ready / error) is the primary visual element on every card.

Vercel understands that its users care about **one thing above all**: "Is my deployment live and healthy?" Every design decision routes toward answering that question faster.

The second insight: Vercel's **build logs** are a canonical piece of product design. A simple scrolling terminal-style log that tells you exactly what happened. No abstractions. No charts. Just the raw truth of the build.

**What Genesis can learn:** Make the *output state* (is the artifact ready?) the visual hero. Not the input, not the configuration — the output.

## Why GitHub Works

GitHub's mental model is the **repository as the source of truth**. Every page is a view into the repo. The breadcrumb is the navigation (`owner / repo / path`). Navigation isn't menu-driven — it's path-driven.

GitHub's second great insight is **context-preserving tabs**. When you're on a PR, the tabs (Conversation / Commits / Files Changed / Checks) don't navigate you away — they show different views of the *same* object. You never lose context.

The third insight: GitHub's **code view** (file tree + syntax-highlighted code) is so well-executed that it became the industry standard for workspace browsing. The mental model is a local IDE mapped to a web interface.

**What Genesis can learn:** The breadcrumb-as-navigation model. The context-preserving tab pattern. The file-tree-plus-viewer pattern for workspace exploration.

## Why Cursor Works

Cursor's core insight is that the **AI is a colleague, not a tool**. The AI panel sits alongside the code editor as a collaborator with its own state, its own context awareness, and its own communication style. The AI is not invoked — it participates.

The second insight: **context is everything**. Cursor's AI knows what file you're in, what function you've selected, what error you're seeing. The AI's input field is always context-aware. It doesn't ask you to explain where you are.

**What Genesis can learn:** The agents in Genesis's compiler should be visible as *participants*, not processes. The compilation trace should feel like watching a team of agents deliberate, not watching a progress bar fill.

## Why Railway Works

Railway's primary innovation is the **service graph as the dashboard**. Instead of a list of services, you see them as connected nodes on a canvas. The visual layout communicates *relationships* — which service depends on which database, which service calls which API.

Railway understands that modern applications are not lists of components. They are graphs. And graphs should be visualized as graphs.

**What Genesis can learn:** The Architecture Graph in Genesis is not a secondary feature in a tab. It is the primary visual output of the compilation. It should feel like Railway's service graph — a living diagram of what was built.

## Why Datadog Works

Datadog's insight is **density as a feature**. A senior engineer opening a Datadog dashboard wants to see everything at once — metrics, traces, logs, alerts. The dashboard is not a landing page. It is a control room.

Datadog is also the canonical example of **time as the primary axis**. Every piece of data is placed in time. The global time picker is not a filter — it is the lens through which all data is viewed.

**What Genesis can learn:** The telemetry experience should be dense and time-aware. Compilation events have timestamps; those timestamps should be the primary organizing principle.

## Why Figma Works

Figma's insight is the **canvas as the primary work surface**. The product doesn't have pages — it has canvases. You pan and zoom. You can see everything at once or zoom into a single component.

The second insight: **the sidebar is a layer list**. What you see on the canvas is mirrored in the layer panel. Clicking in either updates the other. They are synchronized views of the same data.

**What Genesis can learn:** The Architecture Graph should work like a Figma canvas. You pan, zoom, select nodes. The node list on the left mirrors what's on the canvas. Clicking a node in the list highlights it on the canvas.

## Why Raycast Works

Raycast's insight is that **the command interface should be the primary interface**. The launcher replaces the dock, Spotlight, and dozens of utilities. It is the answer to the question "where do I start?"

The design insight: Raycast's result list has **three zones** — the result, the preview, and the action set. Every result shows you what it is, shows you a preview of it, and shows you what you can do with it. The result is never just a label.

**What Genesis can learn:** The Command Palette in Genesis is not a navigation shortcut. It's a primary interface. It should show projects with previews, actions, and contextual options. It should be fast enough to be preferred over clicking.

## Why Warp Works

Warp's insight is that **the terminal's unit of interaction is the block, not the line**. A command and its output form a single, selectable, shareable unit. This transforms the terminal from a stream of text into a structured document.

The second insight: Warp's AI integration doesn't replace the terminal — it annotates it. The AI knows your shell history. It can explain any block, suggest follow-up commands, and fix errors in context.

**What Genesis can learn:** Compilation logs should be **blocks**, not lines. Each phase of the compiler is a block with a header (phase name, duration, status) and a body (events). Blocks are collapsible. Blocks are copyable. Blocks have actions.

---

# Part II: Product Vision

## The Central Thesis

Genesis Engine is not a code generator. It is a **specification compiler**.

A compiler takes source code and transforms it into a binary. No one who understands compilers thinks of `gcc` as a "code writer". The input is a precise specification; the output is a deterministic artifact.

Genesis does the same thing at a higher level of abstraction. You write a specification describing what an application should *be*. Genesis compiles that specification — through a pipeline of AI agents that plan, validate, architect, generate, and package — into a deployable application artifact.

This is the mental model the product must communicate from the first second:

> **You write specs. Genesis compiles them.**

Not "you chat with AI". Not "you describe your app and we'll do our best". Not "AI-powered code generation". A specification compiler.

This framing has profound consequences for the product design:

1. **Specifications are inputs, not conversations.** They are structured, versioned, and reusable.
2. **Compilation is a process, not a chat.** It has phases, can fail, and produces deterministic outputs.
3. **Artifacts are outputs, not suggestions.** They are signed, hashed, and downloadable.
4. **The compiler is observable.** Like `make` with verbose output, you can see every step.

## Product Tagline

> **Genesis Engine — Compile your vision into production-grade software.**

## The Three Pillars

**Precision:** Every compilation is deterministic, verifiable, and traceable. You can inspect every decision made by every agent. No black boxes.

**Velocity:** A specification that took days to manually implement compiles in minutes. The interface never slows you down.

**Trust:** Cryptographic artifact integrity, rule engine validation, and full compilation audit trails. Safe for enterprise procurement.

---

# Part III: Information Architecture

## The Object Model

Every piece of data in Genesis maps to one of five object types. The UI is built around these objects — not around pages.

```
Organization
└── Project (one logical application concept)
    └── Run (one compilation attempt)
        ├── Specification (the input to the run)
        ├── Planning Report (phase 1 output)
        ├── Architecture (graphs: API, Page, Component, Feature, DB)
        ├── Compilation Trace (chronological agent event log)
        └── Artifact Bundle (the deployable output)
            ├── Source Archive (.zip)
            ├── Deployment Manifest (.json)
            └── Graph Files (.json × N)
```

### Object Descriptions

**Organization:** The tenant. All projects belong to an organization. An organization has members, roles, and settings.

**Project:** A logical grouping. "E-Commerce Platform", "Internal Dashboard", "API Gateway". A project has many Runs over time. It does *not* contain code — it contains the history of attempts to compile its specification.

**Run:** The atomic unit of work in Genesis. A Run has a status (PENDING → PLANNING → VALIDATING → GENERATING → PACKAGING → SUCCESS | FAILED), a duration, and all associated outputs. When an engineer says "the last build failed", they are talking about a Run.

**Specification:** The input to a Run. A structured JSON document describing pages, components, features, and APIs. Specifications are versioned and can be saved as templates.

**Architecture:** The AI-generated structural design of the application. Not source code — a *blueprint*. Expressed as graphs (how APIs connect to pages, how components depend on each other, how DB entities relate). This is the most valuable and intellectually interesting output of Genesis.

**Compilation Trace:** The audit log of what every agent did. Every decision, every step, every duration. The trace is the proof that the compilation was correct.

**Artifact Bundle:** The deployable output. A cryptographically signed archive containing all generated source code, plus metadata (manifest, hashes, plugin versions).

## Navigation Hierarchy

```
Level 0 — Global
  /                     → Organization Dashboard (overview of all projects)
  /projects             → All Projects (list/grid view)
  /runs                 → Global Run Feed (all compilations, all time)
  /telemetry            → Organization-level telemetry
  /team                 → Team & User Management
  /settings             → Organization Settings

Level 1 — Project
  /projects/[id]        → Project Overview
  /projects/[id]/runs   → All Runs for this Project
  /projects/[id]/spec   → Specification Library (saved specs for this project)
  /projects/[id]/settings → Project Settings

Level 2 — Run
  /projects/[id]/runs/[runId]                    → Run Overview
  /projects/[id]/runs/[runId]/compiler           → Live Compiler (or Trace if complete)
  /projects/[id]/runs/[runId]/architecture       → Architecture Graph
  /projects/[id]/runs/[runId]/workspace          → Generated Code Explorer
  /projects/[id]/runs/[runId]/artifacts          → Artifact Manager
  /projects/[id]/runs/[runId]/report             → Planning Report

Special Routes
  /compiler             → New Run (spec editor + live output)
  /search               → Global Search
```

## Information Priority (Per Screen)

Every screen has a primary, secondary, and tertiary information layer. This prevents cognitive overload.

| Screen | Primary | Secondary | Tertiary |
|--------|---------|-----------|----------|
| Org Dashboard | Active runs + recent project health | Project stats strip | Activity feed |
| Projects | Project name + last run status | Run count + success rate | Last modified |
| Run Overview | Status + duration + error count | Phase breakdown | Spec summary |
| Compiler (live) | Current phase + live events | Phase stepper | Elapsed time |
| Architecture | Graph canvas (primary visual) | Node type filter | Node details panel |
| Workspace | File tree + code viewer | File metadata | Language stats |
| Artifacts | File list with download | Hash values | File sizes |

---

# Part IV: Navigation Architecture

## The Three-Layer Navigation Model

Genesis uses a **three-layer navigation model** inspired by Linear's workspace hierarchy and GitHub's breadcrumb navigation.

### Layer 1: The Global Rail (48px, always visible)

The leftmost element of the interface. Never expands. Contains only icons. This is the "escape hatch" — always gets you back to global context.

```
┌────┐
│ G  │  ← Genesis logotype / org switcher
├────┤
│ ⊞  │  ← Dashboard (home)
│ ⬡  │  ← Projects
│ ⚡  │  ← Compiler (new run)
│ ⬡  │  ← Global Runs Feed
│ ~  │  ← Telemetry
├────┤
│    │  (spacer, flex-1)
├────┤
│ ⬡  │  ← Team
│ ⚙  │  ← Settings
│ 🔔 │  ← Notifications
│ /  │  ← User avatar (click → profile/logout)
└────┘
```

The active item in the rail has a left-side indicator (2px vertical bar, accent color). There is no background highlight — only the indicator. This is cleaner than background fills and communicates "position" rather than "selection".

**Design Rationale:** A permanent 48px rail means the user is never more than one click from any global destination, regardless of how deep they've navigated. This solves the "lost in a project" problem that plagues most dashboard apps.

### Layer 2: The Context Panel (240px, collapsible)

This is not a "sidebar". It is a **context navigator** — it shows the navigation tree relevant to the current global rail selection.

When "Projects" is active in the rail:
```
┌──────────────────────────────┐
│  Projects                    │
│  [+ New Project]  [⊞ Grid]  │
├──────────────────────────────┤
│  PINNED                      │
│  ● E-Commerce Platform       │
│  ● Internal Dashboard        │
├──────────────────────────────┤
│  ALL PROJECTS                │
│  ○ Blog Platform             │
│  ○ API Gateway               │
│  ○ CRM System                │
├──────────────────────────────┤
│  [Search projects...]        │
└──────────────────────────────┘
```

When a specific project is active, the context panel transforms into the **project navigator**:
```
┌──────────────────────────────┐
│  ← Projects                  │
│  E-Commerce Platform   ●     │  ← status dot
├──────────────────────────────┤
│  ⊞ Overview                  │
│  ⚡ Compiler                  │  ← "Start New Run"
│  ⬡ Runs (47)                 │
│  📋 Specifications            │
├──────────────────────────────┤
│  RECENT RUNS                 │
│  ● run_2024628_1            │  ← SUCCESS
│  ⚠ run_2024627_3            │  ← FAILED
│  ● run_2024626_2            │  ← SUCCESS
├──────────────────────────────┤
│  ⚙ Project Settings          │
└──────────────────────────────┘
```

When a specific run is active, the context panel transforms into the **run navigator**:
```
┌──────────────────────────────┐
│  ← E-Commerce Platform       │
│  run_20240628_1       ●      │  ← status
├──────────────────────────────┤
│  ⊞ Overview                  │
│  ⚡ Compiler / Trace         │  ← live indicator if running
│  ⬡ Architecture              │
│  📁 Workspace                │
│  📦 Artifacts                │
│  📋 Planning Report          │
└──────────────────────────────┘
```

**Design Rationale:** The context panel is not a fixed list of links — it is a *view of the current object's children and siblings*. This mirrors Linear's left panel and creates a sense of spatial navigation rather than page navigation. You always know where you are in the hierarchy because the panel shows your current position and what's around it.

**Collapse behavior:** The context panel collapses to 0px (fully hidden) on user command (`⌘\` or clicking a collapse button on the panel edge). The main work surface expands to fill the space. This is different from icon-rail mode (which is the global rail — always visible).

### Layer 3: The Header Breadcrumb

The top header bar contains the breadcrumb as the primary navigation element.

```
[G]  Organization  /  E-Commerce Platform  /  run_20240628_1  /  Architecture
```

Each segment is clickable and navigates to that level. The final segment (current location) is displayed in `text-primary` weight 600; parent segments are in `text-secondary` weight 400. Separators are `/` characters in `text-tertiary`.

**The header is 52px tall.** Not 64px. Not 56px. 52px. This saves 12px of screen real estate and makes the interface feel denser and more professional. The density signals "tool", not "website".

---

# Part V: Global Layout System

## The App Shell

The application uses a **three-column CSS Grid layout** at the shell level. This is not a flex layout with sidebars. It is a grid with named areas that allows precise, fluid layout control.

```css
.app-shell {
  display: grid;
  grid-template-columns: 48px [context-width] 1fr [right-panel-width];
  grid-template-rows: 52px 1fr;
  grid-template-areas:
    "rail context  header header"
    "rail context  main   right-panel";
  height: 100vh;
  overflow: hidden;
}
```

Where:
- `[context-width]` is a CSS custom property: `0px` (collapsed) or `240px` (expanded)
- `[right-panel-width]` is a CSS custom property: `0px` to `420px` (user-controlled)
- Both are animated with `transition: grid-template-columns 200ms ease-out`

**Why CSS Grid instead of flexbox for the shell?**

Flexbox creates a one-dimensional layout. When the right panel collapses, the `flex-1` main area grows — but this growth is not smooth because flexbox transitions don't animate `flex-basis` cleanly in all browsers. CSS Grid with named template areas allows *both* the context panel and right panel to resize independently while the main area fills the remaining space. The animation is handled by transitioning the grid column widths, which browsers animate natively and correctly.

## The Four Zones

### Zone 1: Global Rail (48px × 100vh)

Fixed. Never scrolls. Never hides (on desktop). Contains only icon buttons. The rail is the one constant in the entire interface — it is the user's anchor.

**Colors:** Background is `--surface-void` (#07090F) — slightly darker than the context panel and main area. This makes the rail visually recede while remaining distinct.

### Zone 2: Context Panel (0–240px × 100vh minus header)

Scrollable (internally). Position: below the header. Contains the context-aware navigation tree.

The context panel has a **subtle right border** (`1px solid rgba(255,255,255,0.06)`) — barely visible, but enough to define the boundary between the panel and the main surface.

### Zone 3: Header Bar (100% × 52px)

Spans the full width above the main area and right panel (not above the rail or context panel). Contains:
- **Left:** Breadcrumb navigation
- **Center:** Page title (only shown on pages with long content, otherwise blank)
- **Right:** Search trigger (`⌘K` label) + Notification bell + Status indicator + User avatar

The header has `backdrop-filter: blur(20px)` and a bottom border. It appears to float above scrollable content — as the page scrolls, the header stays fixed.

### Zone 4: Main Work Surface (flex-1)

This is where all page content renders. It is a scrollable region. Each page controls its own internal layout.

### Zone 5: Contextual Right Panel (0–420px)

The **most important architectural decision in this redesign.**

In the current Genesis implementation, the Compiler Output and the Spec Editor live on the *same page*. In the new design, the right panel is a **persistent, dockable context panel** that shows information relevant to the current main view.

The right panel is:
- **Persistent:** It doesn't disappear when you navigate. It transitions its content.
- **Dockable:** The user can resize it by dragging its left edge. Width is persisted.
- **Collapsible:** Collapse to 0px with `⌘P` or a collapse button. Main area expands.
- **Context-aware:** Its content changes based on the main view:

| Main View | Right Panel Content |
|-----------|---------------------|
| Dashboard | Activity Feed / Live Runs |
| Projects list | Recent Activity |
| Run Overview | Compiler Status (if running) or Run Summary |
| Compiler | Live Agent Output (always) |
| Architecture | Selected Node Details |
| Workspace | File Metadata + Actions |
| Artifacts | Selected File Details |

**Design Rationale:** This solves the fundamental problem with the current design — the SpecEditor and ExecutionStatusPanel exist as peers on the dashboard, making the dashboard schizophrenic. In the new model, the Spec Editor is a dedicated page (`/compiler`), and the live output is always in the right panel. The main surface is for authoring. The right panel is for observing. These are different jobs, and they now live in different zones.

## Layout Density Modes

Users can choose between three density modes (persisted in user preferences):

**Comfortable:** `padding: 24px`, `row-gap: 20px`, `font-size: base (14px)`. Default for new users.

**Default:** `padding: 16px`, `row-gap: 16px`, `font-size: 13px`. Standard mode.

**Compact:** `padding: 12px`, `row-gap: 12px`, `font-size: 12px`. Maximum information density. Used by power users.

All spacing tokens scale proportionally between modes using a `--density-scale` CSS custom property.

---

# Part VI: Project Lifecycle

## States and Transitions

A Run moves through a defined state machine:

```
                        ┌─────────────────────────────────────────────┐
                        ↓                                             │
IDLE → [submit spec] → QUEUED → PLANNING → VALIDATING → GENERATING → PACKAGING → SUCCESS
                                     │            │           │                 ↗
                                     └────────────┴───────────┴──→ FAILED ────┘
                                                                (can retry)
```

**QUEUED:** The run has been submitted but the compiler hasn't started yet. Shows a queue position indicator if the system is under load.

**PLANNING:** Phase 1. The planner agent analyzes the spec, expands features, resolves dependencies, and produces the graph blueprint. This is the fastest phase (typically 2–8 seconds).

**VALIDATING:** Phase 2. The rule engine validates the planned architecture against a set of integrity rules. Checks for circular dependencies, missing API definitions, schema violations. Can fail here — produces a Planning Report with failed rules.

**GENERATING:** Phase 3. The generation agents produce code for each component, page, API endpoint, and database schema. The longest phase (10–60 seconds depending on spec complexity).

**PACKAGING:** Phase 4. The artifacts are assembled, hashed, and bundled. The deployment manifest is created. (2–5 seconds).

**SUCCESS:** All phases completed without errors. Artifact bundle is available for download.

**FAILED:** One or more phases encountered an unrecoverable error. A Failed run still produces a partial Planning Report and Compilation Trace that can be inspected for debugging.

## Visual State Communication

Status is communicated through **three channels simultaneously** — never just one:

1. **Color:** The accent color associated with the status
2. **Icon:** A distinct icon shape (not just color changes)
3. **Motion:** RUNNING has animation; SUCCESS is static; FAILED is static

| Status | Color | Icon | Motion |
|--------|-------|------|--------|
| QUEUED | `--warning` (amber) | Clock icon | Static |
| PLANNING | `--accent` (iris blue) | Brain icon | Rotating pulse |
| VALIDATING | `--accent` (iris blue) | Shield icon | Slow pulse |
| GENERATING | `--accent` (iris blue) | Code icon | Fast pulse |
| PACKAGING | `--accent` (iris blue) | Package icon | Slow pulse |
| SUCCESS | `--success` (emerald) | Check circle | Static |
| FAILED | `--error` (red) | X circle | Static |

The animation for active phases uses a **dual-ring pulse** (inner ring solid, outer ring expanding and fading) — the same visual language used by medical monitoring equipment. It communicates "ongoing, healthy activity" without being distracting.

---

# Part VII: User Journeys

## Journey 1: First-Time User

```
Land on Login page
  → Authenticate
  → Land on Dashboard (first time — empty state with onboarding prompt)
  → Click "Compile your first spec" (empty state CTA)
  → Opens /compiler with a pre-loaded example specification
  → User can edit the spec
  → Click "Compile" (⌘Enter)
  → Right panel shows live agent output
  → After completion: Toast "Compilation successful. 14.2s."
  → Auto-navigate to Run Overview for the new run
  → User explores Architecture tab, Workspace tab, Artifacts tab
  → User clicks "New Run" to iterate
```

**Key Insight:** The empty dashboard does not ask the user "what would you like to do?" It tells them: "You don't have any projects yet. Let's compile your first spec." The CTA takes them directly to the Compiler with an example loaded — lowering the activation energy to zero.

## Journey 2: Returning Engineer — Daily Use

```
⌘K → type "e-commerce" → select project → press Enter
  → Lands on Project Overview (last opened project)
  → Sees last run status at a glance
  → Clicks "New Run" (or presses R)
  → /compiler opens in context of this project
  → Spec is pre-loaded from last successful run (editable)
  → Makes changes
  → ⌘Enter to compile
  → Right panel shows live output (user can continue browsing other projects)
  → 14 minutes later: Browser notification "Compilation complete"
  → Returns to run detail
```

**Key Insight:** The returning engineer's primary path is via Command Palette, not the sidebar. They think in project names and actions, not in menu items. The spec is pre-loaded from last run — they iterate, not restart.

## Journey 3: Engineering Manager — Status Check

```
Open Genesis
  → Dashboard shows project health strip and active runs
  → 3 projects have runs in progress
  → 1 project has a FAILED run (highlighted with error color)
  → Manager clicks the failed project
  → Project Overview shows failure reason at the top
  → One click to "Planning Report" to see which rules failed
  → Copies error summary to Slack
```

**Key Insight:** The manager never needs to go deeper than the Planning Report. The failure reason must be visible within 2 clicks from the dashboard.

## Journey 4: Security Audit

```
Navigate to /runs (global run feed)
  → Filter by date range (last 30 days)
  → Export run list as CSV
  → Open specific run
  → Go to Artifacts tab
  → Copy SHA-256 hash of deployment bundle
  → Check plugin versions table
  → Export Planning Report (rule coverage scores)
```

**Key Insight:** The security officer needs data in a format they can take elsewhere. Every hash is copyable with one click. Every table is exportable.

---

# Part VIII: Every Screen

## Screen 1: Login (`/login`)

**Purpose:** Authentication gate. Must communicate the product's premium quality before the user enters.

**Layout:**
- Full viewport. Dark background.
- Centered card, max-width 420px.
- Above the card: Genesis logotype (wordmark + icon mark). This is the first impression of the brand.

**Background Design:**
Not a plain dark background. A subtle, mathematically-generated **hexagonal grid** pattern (SVG background, very low opacity ~4%) over the dark void. This communicates the "graph/compilation" concept without being decorative. The same visual language as the Architecture Graph — establishing continuity between the brand and the product.

**Card Content (top to bottom):**
1. Genesis icon mark (32px, centered)
2. Product name "Genesis Engine" (heading-lg, centered)
3. Subtitle "Specification Compiler Platform" (body-sm, text-secondary, centered)
4. Divider (8px spacer + 1px border)
5. Username label + input
6. Password label + input + "Show/hide" toggle
7. "Remember this device" checkbox
8. "Sign In →" primary button (full width)
9. Forgot password link (text-only, text-secondary)
10. Version badge + legal links (bottom of card, very small)

**Error State:**
On failed login, the card shakes (translateX shake animation, 300ms). An inline error message appears between the password field and the button — not a toast, not a modal. The specific field that caused the failure gets an error border if identifiable (e.g., wrong password → password field gets error ring).

**Why no SSO/OAuth buttons for v1:** Keeping the login page clean and focused. SSO can be added as a secondary link ("Sign in with SSO →") that opens a separate flow.

**Keyboard:** Tab order is Username → Password → Remember → Submit. Enter in either field submits the form.

---

## Screen 2: Organization Dashboard (`/`)

**Purpose:** The control room. Show what's happening across the entire organization right now, and what happened recently.

**This is not a welcome page. This is not a project list. This is an operational view.**

**Layout (CSS Grid):**
```
┌──────────────────────────────────────────────────────────────────────────┐
│  HEADER: [Breadcrumb: Organization]    [⌘K]  [🔔]  [Avatar]             │
├──────────────────────────────────────────────────────────────────────────┤
│                                              │                           │
│  ┌─ Health Strip (5 stats) ───────────────┐  │   RIGHT PANEL:            │
│  └─────────────────────────────────────────┘  │   Activity Feed           │
│                                              │   (SSE-driven, live)      │
│  ┌─ Active Runs ──────────────────────────┐  │                           │
│  │  (Showing runs in PLANNING/GENERATING/ │  │   ─────────────────────   │
│  │   PACKAGING state, live update)        │  │   RECENT EVENTS           │
│  └─────────────────────────────────────────┘  │   14:02 ecommerce DONE   │
│                                              │   13:58 blog-api FAILED   │
│  ┌─ Recent Projects ──────────────────────┐  │   13:41 crm STARTED      │
│  │  (Last 5 touched projects, cards)      │  │   ...                     │
│  └─────────────────────────────────────────┘  │                           │
│                                              │                           │
│  ┌─ Build History Chart ──────────────────┐  │                           │
│  │  (Bar chart, last 30 days)             │  │                           │
│  └─────────────────────────────────────────┘  │                           │
└──────────────────────────────────────────────────────────────────────────┘
```

**Health Strip (5 stat cards, horizontal):**
- Total Projects | Active Compilations | Success Rate (7d) | Avg Compile Time (7d) | Artifacts Generated
- Each card: Large number (heading-xl), label (label-sm), delta vs. previous period (body-sm with ▲/▼ colored indicator)
- Cards are clickable: clicking "Active Compilations" filters the main view to show only active runs

**Active Runs Section:**
This section is only visible when there are active runs. It appears at the top of the content area, above Recent Projects, making it impossible to miss.

Each active run shows as a **horizontal card** (full width):
```
┌────────────────────────────────────────────────────────────────────────┐
│ [●●●○○ phase stepper] │ E-Commerce Platform  ·  run_20240628_1        │
│ ██████████████░░░ GENERATING                      Elapsed: 14.2s  [→] │
└────────────────────────────────────────────────────────────────────────┘
```

The progress bar fills based on a time estimate for each phase (not real progress — a heuristic based on spec complexity). This is honest "progress theater" — it communicates activity without false precision.

**Recent Projects Section:**
5 most recently touched projects. Each is a card (not a table row). Cards show:
- Project name (heading-sm)
- Last run status (status badge)
- Last run time (relative: "2 hours ago")
- Success rate sparkline (7 data points, the last 7 runs)
- "Open" button (visible on hover)

**Build History Chart:**
A bar chart (Recharts, custom styled) showing compilation count per day for the last 30 days. Bars are stacked: green = SUCCESS, red = FAILED. Clicking a bar filters the global runs feed to that day.

**Right Panel — Activity Feed:**
Live SSE-driven event stream. Shows the last 50 events across all projects. Each event:
- Timestamp (relative, tooltip shows absolute)
- Project name (linked)
- Event type (badge)
- Brief description

New events animate in from the top with `slide-in-from-top-1 fade-in` (150ms). The feed doesn't scroll automatically — new events push old ones down. A "New events" pill appears at the top if the user has scrolled down.

---

## Screen 3: Projects (`/projects`)

**Purpose:** Browse, search, and manage all projects.

**Layout:**
```
┌─ Toolbar ──────────────────────────────────────────────────────────────┐
│  [All] [Success] [Failed] [Running]   [Search...]   [Sort▾] [⊞] [☰]  [+ New] │
└────────────────────────────────────────────────────────────────────────┘
┌─ Content (Grid or List based on toggle) ───────────────────────────────┐
│  [Project cards or table rows]                                          │
└────────────────────────────────────────────────────────────────────────┘
```

**Grid View (default for ≤20 projects):**
3-column grid (4 on large screens). Each project card:
```
┌───────────────────────────────────────┐
│ [●] SUCCESS                   [★] [⋯] │
│                                        │
│  E-Commerce Platform                   │
│  47 runs  ·  Last: 2h ago             │
│                                        │
│  ████████████████░░  92%   ← success  │
│  rate (7d)                             │
│                                        │
│  Pages: 12  APIs: 24  Components: 18  │
│                     (last run stats)   │
└───────────────────────────────────────┘
```

The card background uses a subtle left-border color accent matching the last run status. SUCCESS = thin emerald left border. FAILED = thin red left border. RUNNING = animated iris gradient left border.

**List View (default for >20 projects):**
A full-width table. Columns: Name | Last Run Status | Last Run Time | Total Runs | 7d Success Rate | Actions.

The table header is sticky. Clicking a column header sorts. The sort direction is indicated by a `▴`/`▼` icon.

**Batch Actions:**
Checkboxes appear on hover of each row/card. When items are selected, a **floating action bar** appears at the bottom of the screen (like iOS's multi-select toolbar):
```
[□ 3 selected]  [Archive]  [Export]  [Delete]  [✕ Deselect all]
```

**Context Menu (right-click on project card or row):**
- Open
- Open in new tab
- ─────────
- New Run
- Copy project ID
- ─────────
- Pin to sidebar
- Archive
- ─────────
- Delete (destructive, confirmation required)

---

## Screen 4: Compiler (`/compiler`)

**Purpose:** The creation tool. Where new compilations are initiated.

**This screen is designed around a single user intention: "I have a specification and I want to compile it."**

**Layout:**
```
┌─ Header ──────────────────────────────────────────────────────────────┐
│  Organization / Compiler              [Select Project ▾]  [Templates ▾] │
├───────────────────────────────────────────────────────────────────────┤
│                                        │                              │
│  EDITOR ZONE                          │  RIGHT PANEL:                │
│  ┌─ tab bar: [spec.json] [+] ────────┐│  COMPILER OUTPUT             │
│  │                                   ││                               │
│  │  Monaco Editor                    ││  (When idle: empty state)    │
│  │  (full height)                    ││  "Submit a spec to begin"    │
│  │                                   ││                               │
│  │                                   ││  (When running: live feed)   │
│  │                                   ││  Phase stepper + events      │
│  │                                   ││                               │
│  │                                   ││  (When complete: summary)    │
│  └─────────────────────────────────  ││  Result + "View Run →" CTA   │
│                                        │                              │
│  ┌─ status bar ─────────────────────┐  │                              │
│  │ ✓ Valid JSON  ·  5 fields  ·  ln 1 col 1  [Format] [Validate]    [▶ Compile ⌘↵] │
│  └───────────────────────────────────┘                               │
└───────────────────────────────────────────────────────────────────────┘
```

**Editor Zone:**
- Monaco Editor, full height, `json` language mode with Genesis JSON Schema validation
- Tab bar above the editor: allows multiple spec tabs to be open simultaneously (for comparison)
- The editor toolbar is *at the bottom* of the editor (status bar), not the top. This puts the most-used action ("Compile") at the bottom-right — closest to the primary content, lowest click distance.

**Status bar (editor bottom):**
- Left zone: JSON validity indicator (`✓ Valid JSON` / `⚠ N errors`), field count, cursor position
- Right zone: Format button | Validate button | **Compile button** (primary, iris background, `⌘Enter` shortcut labeled)

**Template Picker:**
A dropdown in the header ("Templates ▾") shows saved specification templates. Selecting a template loads it into the editor. The user can then edit and compile. This replaces the default spec — no hardcoded `DEFAULT_SPEC` in the component.

**Project Selector:**
A dropdown ("Select Project ▾") in the header allows the user to associate this run with a project, or create a new project. This solves the current UX problem where compilation and project creation are conflated.

**Right Panel — Compiler Output:**
Three states:

**Idle state:**
```
        ⚡
  Ready to Compile

  Edit your specification in the editor,
  then press ⌘↵ to compile.

  [Load Example Spec]
```

**Running state:**
```
  [Phase Stepper: ●●○○]
  GENERATING  ·  Elapsed 14.2s

  ─────────────────────────────────
  PLANNING PHASE                 ✓
  ─────────────────────────────────
  [collapsed block, expandable]

  ─────────────────────────────────
  VALIDATION PHASE               ✓
  ─────────────────────────────────
  [collapsed block]

  ─────────────────────────────────
  GENERATION PHASE               ●  ← spinning
  ─────────────────────────────────
  → Generating: UserAuthController
  → Generating: ProductCatalogService
  → Generating: CheckoutPage
  [auto-scrolling, last 3 visible]
```

**Complete state:**
```
  ✓ Compilation Successful

  Duration: 14.2s  ·  47 events
  Integrity: 92/100

  ─────────────────────────────────
  [View Run Details →]
  [Download Artifacts]
  [New Compilation]
  ─────────────────────────────────
```

**Phase blocks** are the Warp-inspired innovation. Each phase is a **collapsible block** — a header row showing phase name, status, and duration; plus an expandable body showing all events from that phase. The user can expand any completed phase to inspect it. By default, completed phases are collapsed; the active phase is expanded.

---

## Screen 5: Run Overview (`/projects/[id]/runs/[runId]`)

**Purpose:** The master view of a single compilation run. The first thing an engineer sees after a compilation completes.

**Layout:**
```
┌─ Run Header ──────────────────────────────────────────────────────────┐
│  E-Commerce Platform / run_20240628_1                    [● SUCCESS]  │
│  Jun 28, 2026, 2:14 PM  ·  14.2s  ·  4 phases  ·  47 events         │
│  [View Compiler Trace]  [View Architecture]  [Download Artifacts]     │
└────────────────────────────────────────────────────────────────────────┘
┌─ Metrics Strip ────────────────────────────────────────────────────────┐
│  [Integrity 92]  [Features 12]  [Pages 8]  [APIs 24]  [Entities 16]  │
└────────────────────────────────────────────────────────────────────────┘
┌─ Two column grid ──────────────────────────────────────────────────────┐
│  ┌─ Phase Timeline ─────────────────┐  ┌─ Spec Summary ─────────────┐ │
│  │  Planning    2.1s  ✓             │  │  Project: E-Commerce        │ │
│  │  Validation  1.8s  ✓             │  │  Pages: Dashboard, Cart...  │ │
│  │  Generation  9.4s  ✓             │  │  APIs: /products, /orders.. │ │
│  │  Packaging   0.9s  ✓             │  │  [View Full Spec]           │ │
│  └──────────────────────────────────┘  └─────────────────────────────┘ │
│                                                                        │
│  ┌─ Architecture Preview ─────────────────────────────────────────────┐ │
│  │  [Mini React Flow canvas, non-interactive, shows the graph]        │ │
│  │  [View Full Architecture →]                                         │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

**Run Header:**
The status badge is the *largest* element in the header. It is not a small pill on the right side. It is a prominent badge with a large icon and the status text. This is because status is the most important fact about a run.

The three quick action buttons are secondary: View Compiler Trace, View Architecture, Download Artifacts. These are the three most common actions after viewing the overview.

**Phase Timeline:**
A vertical list of phases with their durations. Each phase has:
- Phase icon (specific to the phase type)
- Phase name
- Duration (formatted: `9.4s`)
- Status indicator
- Click → navigates to Compiler Trace tab, scrolled to that phase's block

**Architecture Preview:**
A non-interactive (no pan/zoom) thumbnail view of the architecture graph. Shows the graph at a small scale to give the engineer a sense of the complexity of what was built. Clicking anywhere on it navigates to the full Architecture screen.

**Why a preview?** Because the Architecture is the most intellectually interesting output, and showing even a small version of it on the overview dramatically increases the likelihood that the engineer will click through to explore it. It teases the product's depth.

---

## Screen 6: Compiler Trace (`/projects/[id]/runs/[runId]/compiler`)

**Purpose:** The full, inspectable audit trail of the compilation. The "build logs" equivalent.

**Layout (full-width, no right panel by default):**
```
┌─ Toolbar ─────────────────────────────────────────────────────────────┐
│  [All Phases ▾] [All Status ▾] [Search events...]  [Export JSON]  [⊞] │
└────────────────────────────────────────────────────────────────────────┘
┌─ Phase Stepper (horizontal, sticky) ──────────────────────────────────┐
│  ✓ Planning 2.1s  ·  ✓ Validation 1.8s  ·  ✓ Generation 9.4s  ·  ✓ Packaging 0.9s │
└────────────────────────────────────────────────────────────────────────┘
┌─ Event Blocks (scrollable) ────────────────────────────────────────────┐
│                                                                        │
│  ┌─ PLANNING PHASE  ·  2.1s  ·  ✓ 12 events ─────────────────── [▼] ┐ │
│  │  14:02:01.012  →  SpecAnalysisStarted                              │ │
│  │  14:02:01.245  →  FeatureExpansion: 12 features resolved           │ │
│  │  14:02:01.891  →  DependencyGraph: 47 edges computed               │ │
│  │  14:02:02.104  →  PlanningComplete  [expand details]               │ │
│  └──────────────────────────────────────────────────────────────────── ┘ │
│                                                                        │
│  ┌─ VALIDATION PHASE  ·  1.8s  ·  ✓ 8 events ─────────────────── [▼] ┐ │
│  │  ...                                                               │ │
│  └──────────────────────────────────────────────────────────────────── ┘ │
│                                                                        │
│  ┌─ GENERATION PHASE  ·  9.4s  ·  ✓ 24 events ─────────────────── [▼] ┐ │
│  │  ...                                                               │ │
│  └──────────────────────────────────────────────────────────────────── ┘ │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

**Phase Blocks (Warp-inspired):**
Each phase is a collapsible block. The block header is a full-width bar with:
- Left: Phase name (label-sm uppercase) + status icon
- Center: Duration (code-sm)
- Right: Event count + collapse toggle

When expanded, the block body shows all events in that phase as timeline entries:
- Timestamp (code-sm, `HH:mm:ss.mmm`)
- Arrow (`→`) separator
- Event name (body-sm, weight 500)
- If the event has `details`, a `[+]` expand toggle appears inline

Clicking `[+]` expands the event inline to show its `details` object as a formatted JSON block (syntax-highlighted, not raw).

**For RUNNING compilations:**
The latest phase block is expanded and pinned at the bottom of the viewport. New events animate in at the bottom. A "Scroll to bottom" pill appears if the user scrolls up.

**Gantt Timeline toggle (`⊞` button):**
Switches the view from event blocks to a horizontal Gantt timeline:
```
         0s    2s    4s    6s    8s    10s   12s   14s
Plan     [███]
Validate      [███]
Generate            [████████████████]
Package                               [█]
```

Each bar is clickable, scrolling back to that phase's block view.

---

## Screen 7: Architecture Graph (`/projects/[id]/runs/[runId]/architecture`)

**Purpose:** The primary intellectual output of Genesis. A visual, explorable diagram of the compiled application's structure.

**This screen is the most ambitious in the product. It must feel like a professional diagramming tool, not a debug view.**

**Layout:**
```
┌─ Toolbar ─────────────────────────────────────────────────────────────┐
│  Graph: [API ▾]  Mode: [● Canvas] [○ Table]  [Fit] [+] [-]  [Export▾] │
└────────────────────────────────────────────────────────────────────────┘
┌─ Left Mini Panel (240px) ──┐ ┌─ Canvas (flex-1) ──────────────────────┐
│  FILTER / LEGEND          │ │                                         │
│                            │ │  (React Flow canvas)                   │
│  ○ API Endpoints (24)      │ │                                         │
│  ○ Pages (8)              │ │  [drag, pan, zoom]                     │
│  ○ Components (18)         │ │  [click node → right panel opens]      │
│  ○ DB Entities (6)         │ │                                         │
│                            │ │  [Minimap bottom-right]                │
│  ─────────────────         │ │                                         │
│  NODE LIST                 │ │                                         │
│  > ProductController       │ │                                         │
│    CartService             │ │                                         │
│    UserAuthAPI             │ │                                         │
│    [...]                   │ │                                         │
└────────────────────────────┘ └─────────────────────────────────────────┘
                                Right panel (when node selected):
                                ┌─ Node: ProductController ─────────────┐
                                │  Type: API Endpoint                   │
                                │  Method: GET /api/products             │
                                │  Dependencies: [ProductRepo, CacheLayer]│
                                │  Used by: [ProductPage, SearchPage]    │
                                │  Hash: sha256:abc...                   │
                                └───────────────────────────────────────┘
```

**Canvas Behavior:**
- Pan: Click and drag background
- Zoom: Scroll wheel, or `+`/`-` keys
- Select: Click a node
- Multi-select: Shift-click or drag-select box
- Fit view: `F` key or "Fit" button
- `Escape`: Deselect all

**Node Types and Visual Language:**
Each node type has a distinct shape and color:
- **API Endpoints:** Rounded rectangle, iris border
- **Pages:** Rectangle with folded top-right corner, slate border
- **Components:** Hexagon, emerald border
- **DB Entities:** Cylinder shape (if SVG-based node), amber border
- **Features:** Circle, purple border

Node size scales with the number of connections (degree centrality). More connected nodes are larger, helping identify architectural hubs.

**Edge Types:**
- **Dependency:** Arrow pointing from dependent to dependency (solid line)
- **Usage:** Arrow pointing from user to used component (dashed line)
- **Data flow:** Thick arrow (animated when the run is RUNNING)

**Node Detail Panel (right panel):**
When a node is selected, the right panel slides open with:
- Node name (heading-md)
- Node type badge
- Full API path or route (if applicable)
- Dependencies list (clickable, clicking highlights the connected node on canvas)
- "Used by" list (clickable)
- Hash value (copyable)
- Source file path (if in workspace)

**Graph Selector (API / Page / Component / Feature / DB):**
Different graphs are different *views* of the architecture, not different graphs. Switching graph type morphs the canvas — nodes that exist in both views transition smoothly.

**Export options:**
- PNG (current viewport)
- PNG (full graph, scaled)
- JSON (raw graph data)
- SVG (vector, scalable)

---

## Screen 8: Workspace Explorer (`/projects/[id]/runs/[runId]/workspace`)

**Purpose:** Browse the generated source code. The IDE experience without leaving the browser.

**Layout:**
```
┌─ File Tree (240px) ──┐ ┌─ Tab Bar ───────────────────────────────────┐
│  [Search files...]   │ │ [package.json ×] [App.tsx ×] [styles.css ×]│
│                       │ ├─────────────────────────────────────────────┤
│  ▶ src/              │ │  [Monaco Editor — active tab content]       │
│    ▶ components/     │ │                                             │
│    ▶ pages/          │ │                                             │
│    ▶ api/            │ │                                             │
│    ▼ styles/         │ │                                             │
│      globals.css     │ │                                             │
│      theme.css       │ │                                             │
│  ▶ public/           │ │                                             │
│  package.json ←      │ │                                             │
│  tsconfig.json       │ └─────────────────────────────────────────────┘
│                       │ ┌─ Status Bar ────────────────────────────────┐
│  STATS               │ │ TypeScript  ·  ln 24, col 8  ·  [Copy]  [↗] │
│  47 files  ·  12 dirs│ └─────────────────────────────────────────────┘
└───────────────────────┘
```

**File Tree:**
- Click file → opens in new tab
- Click directory → expand/collapse (animated, 150ms)
- File icons by type (TypeScript, JSON, CSS, Markdown, etc.)
- Search within file tree: filters visible files by name
- Right-click file → context menu: Open, Copy path, Copy content, View raw

**Tab Bar:**
- Multiple open files as tabs (same as VS Code)
- Tabs overflow: scroll with scroll wheel, left/right arrow buttons appear
- `⌘W` closes active tab
- Middle-click closes tab
- Drag tabs to reorder (optional, Tier 4)

**Monaco Editor:**
- Read-only (this is generated code — do not allow editing)
- Theme matches the overall design system (custom dark theme, not `vs-dark`)
- Minimap: enabled on large screens, disabled on small
- `⌘F` → Find in file
- Bottom status bar: language mode, cursor position, copy button, "Open raw" link

**File Stats Panel (optional, collapsible from file tree footer):**
Total files, total directories, language breakdown (small donut chart: TypeScript 62%, CSS 18%, JSON 12%, Other 8%)

---

## Screen 9: Artifact Manager (`/projects/[id]/runs/[runId]/artifacts`)

**Purpose:** Download and verify the compilation outputs.

**Layout:**
```
┌─ Header ───────────────────────────────────────────────────────────────┐
│  Artifacts  ·  run_20240628_1  ·  ✓ SUCCESS                           │
│  [Download All as ZIP ↓]                                               │
└────────────────────────────────────────────────────────────────────────┘
┌─ Artifact List ────────────────────────────────────────────────────────┐
│                                                                        │
│  SOURCE                                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │ 📦  deployment_bundle.zip                         12.4 MB  [↓]    ││
│  │     Compiled source bundle  ·  SHA256: abc...def  [copy]           ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                        │
│  METADATA                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │ {} deployment_manifest.json                        2.1 KB  [↓]    ││
│  │ {} planning_report.json                            8.4 KB  [↓]    ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                        │
│  TELEMETRY                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │ {} execution_trace.json                           14.2 KB  [↓]    ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                        │
│  GRAPHS                                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │ ⬡  api_graph.json                                  3.2 KB  [↓]    ││
│  │ ⬡  page_graph.json                                 1.8 KB  [↓]    ││
│  │ ⬡  component_graph.json                            4.1 KB  [↓]    ││
│  │ ⬡  feature_graph.json                              2.7 KB  [↓]    ││
│  └─────────────────────────────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────────────────────┘
┌─ Integrity Section ────────────────────────────────────────────────────┐
│  Workspace Hash (SHA-256):                                             │
│  [long hash]                                              [Copy ⎘]    │
│                                                                        │
│  Deployment Bundle Hash (SHA-256):                                     │
│  [long hash]                                              [Copy ⎘]    │
└────────────────────────────────────────────────────────────────────────┘
```

**Key Design Decisions:**
- Artifacts are **categorised** — not a flat list. The categories make it clear what each artifact type is for.
- Hash values are shown **next to each artifact** (truncated) with a one-click copy. Full hash visible on hover.
- Download button is visible on each row — no hover reveal. Artifacts are downloaded frequently. Making users hover to see the button creates unnecessary friction.
- "Download All as ZIP" is a prominent action in the header.

---

## Screen 10: Planning Report (`/projects/[id]/runs/[runId]/report`)

**Purpose:** The rule engine validation results. Most important for debugging failed runs.

**Layout:**
```
┌─ Status Banner ────────────────────────────────────────────────────────┐
│  ✓ Rule Validation: SUCCESS  ·  Integrity: 92/100  ·  Duration: 1.8s  │
└────────────────────────────────────────────────────────────────────────┘
┌─ Metrics Grid (2×4) ────────────────────────────────────────────────────┐
│  [Features: 12] [Pages: 8] [APIs: 24] [Entities: 16]                  │
│  [Components: 18] [Dependencies: 47] [Errors: 0] [Warnings: 2]        │
└────────────────────────────────────────────────────────────────────────┘
┌─ Rule Results Table ────────────────────────────────────────────────────┐
│  [All] [Pass] [Fail] [Warn]      [Search rules...]                     │
│                                                                        │
│  ✓  NoCircularDependencies              passed  0.12s                  │
│  ✓  AllAPIsHaveModels                   passed  0.09s                  │
│  ⚠  UnreferencedComponents              warn    0.04s   [2 issues]     │
│  ✓  DatabaseRelationalIntegrity         passed  0.31s                  │
└────────────────────────────────────────────────────────────────────────┘
┌─ Issues Detail (only shown if warnings or errors exist) ───────────────┐
│  ⚠ UnreferencedComponents                                              │
│  HeaderDropdown is defined but not referenced by any page.            │
│  FooterSocial is defined but not referenced by any page.              │
│                                                                        │
│  Suggested remediation: Add these components to a page specification   │
│  or remove them from the component list.                              │
└────────────────────────────────────────────────────────────────────────┘
```

**Key Design Decision:**
The rule results are a **table**, not a list. Tables support sorting and filtering. A senior engineer who sees "2 warnings" wants to click the `Warn` filter and see only those rules. The table supports this.

Each failed/warned rule is expandable inline to show:
- Rule description (what does this rule check for)
- Failing elements (which specific components/APIs triggered the failure)
- Remediation suggestion

The **remediation suggestion** is new — currently the UI just shows the raw rule name. Adding a human-readable explanation of how to fix it dramatically reduces time-to-resolution.

---

## Screen 11: Global Runs Feed (`/runs`)

**Purpose:** A global view of all compilations, across all projects, with filtering and time-based browsing.

**Layout:**
```
┌─ Filters ──────────────────────────────────────────────────────────────┐
│  [Project: All ▾]  [Status: All ▾]  [Last 7 days ▾]   [Export CSV]   │
└────────────────────────────────────────────────────────────────────────┘
┌─ Run List ─────────────────────────────────────────────────────────────┐
│  TODAY                                                                 │
│  14:02  ●  E-Commerce Platform  ·  run_20240628_1  ·  14.2s  [→]     │
│  13:41  ⚠  Blog Platform       ·  run_20240628_2  ·  8.1s   [→]     │
│                                                                        │
│  YESTERDAY                                                             │
│  22:15  ●  Internal Dashboard  ·  run_20240627_1  ·  22.4s  [→]     │
│  ...                                                                   │
└────────────────────────────────────────────────────────────────────────┘
```

Runs are grouped by **date** (Today / Yesterday / This Week / Earlier). Within each group they are chronological (newest first).

Each run row: Timestamp | Status icon | Project name | Run ID | Duration | "Open →" button.

Clicking a row navigates to that run's Overview. Clicking the project name navigates to the Project Overview.

---

## Screen 12: Telemetry (`/telemetry`)

**Purpose:** Aggregate metrics across all compilations, with time-based analysis.

**Subsections:**
- **Overview:** Key metrics strip + build volume chart + success rate chart
- **Performance:** Phase duration analysis, P50/P90/P99 durations, slowest runs table
- **Quality:** Integrity score distribution, rule pass rates, warning trends
- **Comparisons:** Select two runs → side-by-side metrics comparison

---

## Screen 13: Team Management (`/team`)

Standard team management. Members table with roles. Invite flow. Active sessions. Nothing exotic.

---

## Screen 14: Settings (`/settings`)

Left-nav category layout. Categories: General | Compiler | API Keys | Notifications | Appearance | Danger Zone.

---

# Part IX: Relationships Between Screens

```
Login
  └── Dashboard (/)
        ├── Projects (/projects)
        │     └── Project Overview (/projects/[id])
        │           ├── Compiler (/compiler?project=[id])
        │           ├── Runs (/projects/[id]/runs)
        │           │     └── Run Overview (/projects/[id]/runs/[runId])
        │           │           ├── Compiler Trace (/...runs/[runId]/compiler)
        │           │           ├── Architecture   (/...runs/[runId]/architecture)
        │           │           ├── Workspace      (/...runs/[runId]/workspace)
        │           │           ├── Artifacts      (/...runs/[runId]/artifacts)
        │           │           └── Planning Report(/...runs/[runId]/report)
        │           └── Specs (/projects/[id]/spec)
        ├── Compiler (/compiler)
        ├── Global Runs (/runs)
        ├── Telemetry (/telemetry)
        ├── Team (/team)
        └── Settings (/settings)
```

**Key cross-screen relationships:**

- Dashboard active run card → Run Overview (most common navigation)
- Run Overview header → Compiler Trace / Architecture / Artifacts (primary actions)
- Architecture node click → Node detail panel (in-page relationship)
- Architecture node "View Source" → Workspace Explorer, scrolled to file (cross-screen jump)
- Compilation complete → Auto-navigate to Run Overview (programmatic navigation)
- Planning Report failed rule → Compiler Trace (jump to validation phase block)
- Command Palette → any screen (direct navigation)

---

# Part X: The Command Palette

**Philosophy:** The Command Palette is the product's power interface. It is not a "search". It is the fastest path to any object or action in the system.

## Visual Design

Opens as a **centered floating panel** over a backdrop blur. Width: 640px. Max height: 60vh (internally scrollable).

```
┌────────────────────────────────────────────────────┐
│  🔍  Type to search or run a command...            │
│                                                    │
│  RECENT                                            │
│  ⬡  E-Commerce Platform                 ↗         │
│  ⚡  New Run on E-Commerce Platform               │
│  ⬡  run_20240628_1 · SUCCESS · 14.2s   ↗         │
│                                                    │
│  ─────────────────────────────────────────────── │
│                                                    │
│  QUICK ACTIONS                                    │
│  ⚡  New Compilation           ⌘N                 │
│  ⬡  Go to Dashboard           G D                │
│  ⬡  Go to Projects            G P                │
│  ⬡  Open Telemetry            G T                │
│  ⚙  Open Settings             ,                  │
└────────────────────────────────────────────────────┘
```

When typing:
```
┌────────────────────────────────────────────────────┐
│  🔍  ecomm                                         │
│                                                    │
│  PROJECTS                                          │
│  ⬡  E-Commerce Platform         open ↗  run ⚡   │
│  ⬡  E-Commerce Admin            open ↗  run ⚡   │
│                                                    │
│  RUNS                                              │
│  ●  run_20240628_1  E-Commerce Platform  14.2s ↗  │
│  ⚠  run_20240627_3  E-Commerce Platform  8.1s  ↗  │
│                                                    │
│  ARTIFACTS                                         │
│  📦  deployment_bundle.zip  E-Commerce Platform ↓  │
└────────────────────────────────────────────────────┘
```

## Command Categories

**Navigation commands:**
- Go to Dashboard
- Go to Projects  
- Go to Compiler
- Go to Telemetry
- Go to [Project Name]
- Go to [Run ID]

**Action commands:**
- New Compilation → opens /compiler
- New Project → opens new project modal
- Re-run Last Compilation
- Download Artifacts for [current run]
- Export Compilation Trace

**Settings commands:**
- Toggle Sidebar
- Toggle Theme
- Toggle Dense Mode
- Open API Settings

**Search results (live):**
- Projects (by name, ID)
- Runs (by ID, status, date)
- Artifacts (by filename)

## Implementation

Use `cmdk` library. Each result item has:
- Icon (leftmost, 16px)
- Primary label
- Secondary label (e.g., project name, timestamp)
- Right-side actions (appear on hover: Open | Run | Download, depending on type)
- Keyboard indicator (kbd style)

Keyboard navigation: `↑↓` to move, `Enter` to select, `Escape` to close. `Tab` moves to the right-side actions for the selected item.

---

# Part XI: Search Experience

Global search is accessible via:
- `⌘K` (opens Command Palette, which includes search)
- Dedicated search icon in the header rail
- Direct URL: `/search?q=...`

Search results page (`/search?q=ecommerce`) shows a full-page results view grouped by object type:
- Projects (max 3, expandable)
- Runs (max 5, expandable)
- Artifacts (max 5, expandable)

Each result is a card (not a list item) — the additional height allows showing contextual preview information.

---

# Part XII: Notifications

## Notification Architecture

Three-tier notification system:

**Tier 1: Toasts** — Ephemeral, bottom-right, 4–8 seconds.
- Compilation started
- Compilation complete (success/fail)
- Download started
- Action confirmation

**Tier 2: In-App Notification Center** — Persistent, in header.
- All compilation completions
- Failed runs (higher priority)
- System messages (backend offline, etc.)
- Cleared manually or on read

**Tier 3: Browser Notifications** — Opt-in.
- Only for: compilation complete (success or fail)
- Shows project name and result
- Clicking the notification brings the app to focus and navigates to the run

## Notification Center Panel

Clicking the bell icon in the global rail opens a **right-aligned dropdown panel** (not a full page):
```
┌─ Notifications ─────────────────────────────────────────────┐
│  [Mark all read]                    [Clear all]              │
├──────────────────────────────────────────────────────────────┤
│  UNREAD                                                       │
│  ● E-Commerce Platform compiled successfully    14m ago  [→] │
│  ⚠ Blog Platform compilation failed            1h ago   [→] │
├──────────────────────────────────────────────────────────────┤
│  EARLIER                                                      │
│  ● Internal Dashboard compiled                  2h ago  [→] │
│  ● E-Commerce Platform compiled                 4h ago  [→] │
└──────────────────────────────────────────────────────────────┘
```

Unread notifications have a subtle background highlight. The badge count on the bell is the count of unread notifications.

---

# Part XIII: Context Menus

Every interactive object in Genesis has a **right-click context menu** with contextually relevant actions.

**Project card right-click:**
```
  Open
  Open in new tab
  ─────────────────────
  New Run
  Duplicate project
  ─────────────────────
  Pin to sidebar
  Rename
  ─────────────────────
  Archive
  Delete...            ← ellipsis = confirmation dialog
```

**Run row right-click:**
```
  Open
  Open in new tab
  ─────────────────────
  View Architecture
  View Compiler Trace
  ─────────────────────
  Download Artifacts
  Copy Run ID
  ─────────────────────
  Re-run with same spec
  ─────────────────────
  Delete Run
```

**Artifact row right-click:**
```
  Download
  Copy filename
  Copy SHA-256 hash
  ─────────────────────
  View in Workspace Explorer (if source archive)
```

**Architecture node right-click:**
```
  View Details
  ─────────────────────
  Highlight dependencies
  Highlight usages
  Isolate node (hide all unrelated)
  ─────────────────────
  Copy node ID
  Copy node data as JSON
```

**File tree item right-click:**
```
  Open
  Open in new tab
  ─────────────────────
  Copy path
  Copy content
  ─────────────────────
  View raw
```

Context menus use a consistent visual style:
- Background: `--surface-elevated`
- Border: `--border-default`
- Items: 32px min height, 14px font
- Separator: 1px `--border-subtle`, 4px vertical margin
- Destructive items: `--error-400` text color
- Keyboard shortcuts shown right-aligned in `--text-tertiary`
- `border-radius: 8px`
- `box-shadow: --shadow-lg`
- Appear with `scale(0.97) opacity(0) → scale(1) opacity(1)` in 120ms

---

# Part XIV: Loading States

## Philosophy

Loading states must be **spatially honest**. Every loading state must occupy the same geometry as the content it will replace. No spinners in the center of an empty screen unless the entire screen's content is loading.

## Loading State Types

### Type 1: Page Skeleton
Used when an entire page's data is loading (first navigation to a page).

Each page has a custom skeleton that mirrors its exact layout:

**Dashboard skeleton:**
- 5 stat cards: rectangles with rounded shimmer
- Active runs section: 2 full-width bar placeholders
- Recent projects: 5 card-sized rectangles in a grid
- Build chart: A flat rectangle

**Run Overview skeleton:**
- Header: Wide title bar + narrow status badge
- Phase timeline: 4 rows of varying widths
- Spec summary: Two columns of label/value pairs

### Type 2: Table Row Skeleton
When a table is loading, show 5 skeleton rows. Each skeleton row has cells matching the actual column widths.

```
[░░░░░░░░░░░░░] [░░░░] [░░░░░] [░░░░░░] [░░░░] [░░░]
[░░░░░░░░░░] [░░░░] [░░░░░░░] [░░░░░] [░░░░] [░░░]
```

### Type 3: Inline Loading
Used when an action has been triggered but data is loading within an existing layout:

- Button loading: Button's label is replaced with a 16px spinner. Button width does not change (prevents layout shift). Button is disabled.
- Card loading: Card's content area shows a 20px spinner centered in the content zone.

### Type 4: Progressive Loading
For the Architecture Graph: The canvas shows immediately (empty) with a loading spinner in the center. As graph data arrives, nodes animate onto the canvas one by one (stagger 20ms). This feels like the graph is being built, which matches the narrative of compilation.

## Skeleton Animation

```css
@keyframes skeleton-shimmer {
  0% { background-position: -400px 0; }
  100% { background-position: 400px 0; }
}

.skeleton-block {
  background: linear-gradient(
    90deg,
    var(--surface-base) 0%,
    var(--surface-elevated) 50%,
    var(--surface-base) 100%
  );
  background-size: 800px 100%;
  animation: skeleton-shimmer 1.6s ease-in-out infinite;
  border-radius: var(--radius-sm);
}
```

---

# Part XV: Empty States

## Philosophy

An empty state is an **opportunity**, not an error. It tells the user what *will* be here, not just that nothing is here.

Every empty state has four required elements:
1. Illustration (icon-based, on-brand)
2. Headline (what is empty — noun, not sentence)
3. Body (why it's empty, what will appear here)
4. CTA (the action that makes it not empty)

## Specific Empty States

**No Projects:**
```
        ⬡ (hexagonal network icon, 64px, iris tint)

      Your first project awaits

   Genesis compiles your specification into a
   production-ready application. Start by
   describing what you want to build.

      [Compile Your First Spec →]
      
   or  [View Example Spec]
```

**No Active Runs (on Dashboard active runs section):**
— This section is simply hidden when there are no active runs. No empty state needed; its absence communicates "nothing is running right now".

**No Runs for a Project:**
```
        ⚡ (lightning bolt icon, 48px, text-tertiary)

       No runs yet

   This project has never been compiled.
   Submit a specification to start.

      [New Run →]
```

**Architecture Graph — No Nodes:**
```
        ⬡ (graph icon, 48px, text-tertiary)

    Graph unavailable

   The compilation didn't produce a
   resolvable architecture graph.
   Check the Planning Report for validation errors.

      [View Planning Report]    [Switch to Tree View]
```

**Workspace — No File Selected:**
```
        📁 (folder icon, 48px, text-tertiary)

    Select a file

   Click any file in the tree to view
   its generated source code here.
```
No CTA — the action is inherent (click the file tree).

**Artifacts — No Artifacts:**
```
        📦 (package icon, 48px, text-tertiary)

    Artifacts not generated

   The compilation hasn't completed successfully.
   Artifacts are only available for successful runs.

      [View Compiler Trace]
```

**Notification Center — No Notifications:**
```
        🔔 (bell icon, 32px, text-tertiary)

    All caught up

   No notifications.
```
Short, simple. No CTA — there's nothing to do.

---

# Part XVI: Error UX

## Error Taxonomy

**Level 1: Validation Errors (inline)**
- Appear below the specific field that caused the error
- Show immediately on blur (not on submit)
- `⚠ Field name is required.` or `⚠ Invalid JSON at line 4`
- Clear as soon as the field is corrected

**Level 2: API Errors (component-level)**
- Affect a specific card or section, not the whole page
- Show within the affected component's space
- Include a Retry button
```
┌──────────────────────────────────────────┐
│  Failed to load runs                      │
│  Error: Request timed out (408)           │
│  [Retry] [Dismiss]                       │
└──────────────────────────────────────────┘
```

**Level 3: Route-Level Errors (page-level)**
- When navigating to a resource that doesn't exist or can't be accessed
- Full-page error state, centered
```
           ⊘
    Workspace not found

    We couldn't find a workspace with ID
    "run_20240628_99". It may have been
    deleted or you may not have access.

    Error: 404 NOT_FOUND

    [← Back to Projects]    [Search for it]
```

**Level 4: System Errors (global banner)**
- Backend offline
- Authentication expired
- Network connectivity lost

System errors appear as a **full-width banner directly below the header** (not the top of the screen — above the header is reserved for nothing). They are dismissible but will reappear if the condition persists.

```
┌──────────────────────────────────────────────────────────────────────┐
│  ⚠  API Offline  ·  Cannot connect to Genesis Engine on port 8000    │
│  Start the backend: uvicorn main:app --reload              [✕ Close] │
└──────────────────────────────────────────────────────────────────────┘
```

**Level 5: Fatal Application Error (full-screen)**
- React Error Boundary triggered by an unhandled JS error
- Shows a dignified error card, not a blank screen
```
        ⊘
    Something went wrong

    An unexpected error occurred in Genesis Engine.
    This has been automatically reported.

    Error: TypeError — Cannot read property 'id' of undefined

    [Reload Application]    [Go to Dashboard]    [Copy Error Details]
```

The "Copy Error Details" button copies a structured error report (error message, stack trace, current URL, timestamp) for sharing with support.

---

# Part XVII: Responsive Strategy

## Breakpoint Philosophy

Genesis Engine is a **desktop-primary product**. Its users are software engineers working on workstations and laptops. The minimum supported viewport is 1280px wide.

However, the product must be **usable** (not necessarily optimal) at 768px (tablet) for occasional use. Below 768px, a "reduced experience" mode is shown that removes panels and simplifies navigation.

**Breakpoints:**

| Breakpoint | Name | Width | Behaviour |
|------------|------|-------|-----------|
| SM | Tablet | 768px | Context panel collapses. Right panel becomes a bottom drawer. |
| MD | Small Laptop | 1024px | Full layout, right panel collapses by default. |
| LG | Standard | 1280px | Full layout, right panel open by default. |
| XL | Large | 1440px | Full layout, wider content zones. |
| 2XL | Wide | 1920px | Maximum content width capped at 1800px. |

**At 768px (SM — Tablet):**
- Global rail: moves to bottom (iOS-style tab bar with 5 primary icons)
- Context panel: removed (accessible via hamburger → drawer)
- Right panel: removed (accessible via FAB or swipe gesture)
- Main content: full width
- Tables: horizontal scroll

**At <768px (Mobile — Not Officially Supported):**
A graceful degradation banner: "Genesis Engine is optimized for desktop use. Some features may not work as expected." The product remains usable for read operations (viewing projects, runs, reports) but authoring (Compiler) is limited.

---

# Part XVIII: Accessibility

## Target Compliance Level: WCAG 2.1 AA

## Focus Management

All interactive elements must have a visible focus ring. The focus ring style:
```css
:focus-visible {
  outline: 2px solid var(--accent-iris);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}
```

**Note:** Use `:focus-visible` (not `:focus`). This shows the focus ring for keyboard navigation but not for mouse clicks — the standard modern approach.

The focus must be **trapped** within:
- Modals/Dialogs
- Command Palette
- Dropdown menus (when open)

When a modal opens, focus moves to the first interactive element inside it. When it closes, focus returns to the element that triggered it.

## ARIA Patterns

All interactive components must implement correct ARIA:

| Component | ARIA Pattern |
|-----------|-------------|
| Tabs | `role="tablist"`, `role="tab"`, `aria-selected`, `aria-controls` |
| Command Palette | `role="combobox"`, `aria-haspopup="listbox"`, `aria-expanded` |
| Context Menu | `role="menu"`, `role="menuitem"` |
| Status badges | `aria-label="Status: Success"` |
| Live compiler feed | `aria-live="polite"` on the event feed container |
| Phase stepper | `role="list"`, each phase is `role="listitem"` with `aria-current` |
| File tree | `role="tree"`, `role="treeitem"`, `aria-expanded` |
| Notifications badge | `aria-label="3 unread notifications"` |

## Screen Reader Considerations

- All icon-only buttons (download, copy, close) must have `aria-label`
- Dynamic status changes (run status changing from RUNNING to SUCCESS) must be announced via `aria-live="polite"` on a status region
- The file tree's expand/collapse actions must announce the state change
- The command palette input has `aria-autocomplete="list"` and `aria-activedescendant` pointing to the selected result

## Color and Contrast

All text elements must meet WCAG AA contrast ratio:
- Normal text (< 18px): minimum 4.5:1
- Large text (≥ 18px bold or ≥ 24px): minimum 3:1
- UI components (buttons, inputs, icons): minimum 3:1

The `--text-tertiary` color in the design system must be verified to meet 4.5:1 against `--surface-base`. If it doesn't, it must be lightened.

Status colors (success green, error red, warning amber) must never be the *only* means of conveying information. Always pair color with an icon.

## Motion and Animation

All animations must respect `prefers-reduced-motion`:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

Exception: The live event feed's auto-scroll behaviour is not animation — it is scroll position manipulation and must remain functional even with reduced motion.

---

# Part XIX: Design Tokens

## Token Structure

Design tokens use CSS custom properties in `:root`. They are organized in three layers:

**Layer 1: Primitive tokens** — Raw values. Never used directly in components.
```css
:root {
  --primitive-blue-400: hsl(232, 80%, 65%);
  --primitive-gray-900: hsl(220, 20%, 8%);
  /* etc. */
}
```

**Layer 2: Semantic tokens** — Named for their use. These are what components reference.
```css
:root {
  --accent: var(--primitive-blue-400);
  --surface-base: var(--primitive-gray-900);
  /* etc. */
}
```

**Layer 3: Component tokens** — Specific to a component. Override semantic tokens.
```css
.btn-primary {
  --btn-bg: var(--accent);
  --btn-text: var(--text-on-accent);
}
```

## Complete Semantic Token Set

### Surface Tokens
```
--surface-void:      hsl(225, 25%, 4%)     /* #07090F — page background */
--surface-base:      hsl(225, 22%, 8%)     /* #0C1018 — app shell */
--surface-raised:    hsl(225, 20%, 11%)    /* #111827 — cards, panels */
--surface-overlay:   hsl(225, 18%, 14%)    /* #171F2D — dropdowns */
--surface-elevated:  hsl(225, 16%, 18%)    /* #1E2A3A — modals */
--surface-hover:     hsl(225, 16%, 22%)    /* #253040 — hover states */
--surface-selected:  hsl(225, 30%, 25%)    /* #243A5A — selected states */
```

### Border Tokens
```
--border-subtle:     rgba(255, 255, 255, 0.05)
--border-default:    rgba(255, 255, 255, 0.09)
--border-strong:     rgba(255, 255, 255, 0.15)
--border-accent:     rgba(109, 130, 255, 0.50)
--border-error:      rgba(248, 113, 113, 0.50)
```

### Text Tokens
```
--text-primary:      hsl(220, 30%, 96%)    /* #EDF0FA */
--text-secondary:    hsl(220, 15%, 65%)    /* #95A3BE */
--text-tertiary:     hsl(220, 12%, 45%)    /* #60718A */
--text-disabled:     hsl(220, 10%, 30%)    /* #404D5E */
--text-on-accent:    hsl(0, 0%, 100%)      /* #FFFFFF */
--text-link:         hsl(232, 90%, 72%)    /* #7B95FF */
```

### Accent Tokens (Iris Blue — primary brand)
```
--accent:            hsl(232, 80%, 62%)    /* #4F6EF7 */
--accent-subtle:     hsl(232, 80%, 62%, 0.12)
--accent-hover:      hsl(232, 80%, 68%)    /* #6882F8 */
--accent-active:     hsl(232, 80%, 55%)    /* #3A55E0 */
--accent-surface:    hsl(232, 60%, 12%)    /* #101A3D */
```

### Semantic Status Tokens
```
--success:           hsl(158, 64%, 52%)    /* #34C483 */
--success-subtle:    hsl(158, 64%, 52%, 0.12)
--success-surface:   hsl(158, 50%, 8%)     /* #071A10 */

--warning:           hsl(42, 95%, 58%)     /* #F5BE24 */
--warning-subtle:    hsl(42, 95%, 58%, 0.12)
--warning-surface:   hsl(42, 60%, 8%)      /* #1F1600 */

--error:             hsl(0, 90%, 67%)      /* #F75252 */
--error-subtle:      hsl(0, 90%, 67%, 0.12)
--error-surface:     hsl(0, 50%, 8%)       /* #1F0707 */
```

### Radius Tokens
```
--radius-xs:   4px
--radius-sm:   6px
--radius-md:   8px
--radius-lg:   12px
--radius-xl:   16px
--radius-2xl:  24px
--radius-full: 9999px
```

### Shadow Tokens
```
--shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.4);
--shadow-sm: 0 2px 6px rgba(0, 0, 0, 0.5);
--shadow-md: 0 4px 16px rgba(0, 0, 0, 0.6);
--shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.7);
--shadow-glow-accent: 0 0 24px rgba(79, 110, 247, 0.25);
--shadow-glow-success: 0 0 24px rgba(52, 196, 131, 0.20);
```

---

# Part XX: Typography System

## Type Scale

```
--font-primary:  'Inter', -apple-system, BlinkMacSystemFont, sans-serif
--font-mono:     'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace
```

| Token | Size | Weight | Line-Height | Letter-Spacing | Use |
|-------|------|--------|-------------|----------------|-----|
| `--text-3xl` | 30px / 1.875rem | 700 | 1.1 | -0.03em | Hero headings |
| `--text-2xl` | 24px / 1.5rem | 600 | 1.15 | -0.02em | Page titles |
| `--text-xl` | 20px / 1.25rem | 600 | 1.25 | -0.015em | Section headers |
| `--text-lg` | 18px / 1.125rem | 500 | 1.3 | -0.01em | Card headers |
| `--text-base` | 14px / 0.875rem | 400 | 1.5 | 0 | Primary body |
| `--text-sm` | 13px / 0.8125rem | 400 | 1.5 | 0 | Secondary body |
| `--text-xs` | 12px / 0.75rem | 400 | 1.4 | 0 | Captions |
| `--text-2xs` | 11px / 0.6875rem | 500 | 1.4 | 0.03em | Uppercase labels |
| `--text-code-sm` | 12px / 0.75rem | 400 | 1.5 | 0 | Code, hashes |
| `--text-code-base` | 13px / 0.8125rem | 400 | 1.5 | 0 | Editor |

**Uppercase labels** (`--text-2xs`, 500 weight, 0.03em tracking): Used for section headings in the sidebar (`RECENT RUNS`, `ALL PROJECTS`), table headers, and category headers in artifacts. NEVER used for interactive elements.

**Monospace font** (`--font-mono`): Used for:
- All code in Monaco editors
- Run IDs (`run_20240628_1`)
- Hash values (`sha256:abc...def`)
- Timestamps in log views
- File paths in workspace explorer
- Terminal-style output in compiler trace
- Any value that must be compared character-by-character

---

# Part XXI: Spacing System

## The 4px Base Grid

All spacing derives from a 4px base. All values are multiples of 4.

```
--space-0:   0px
--space-1:   4px    (0.25rem) — tight inline gaps
--space-2:   8px    (0.5rem)  — icon-to-label gap
--space-3:   12px   (0.75rem) — compact padding
--space-4:   16px   (1rem)    — standard padding
--space-5:   20px   (1.25rem) — comfortable padding
--space-6:   24px   (1.5rem)  — card padding
--space-8:   32px   (2rem)    — section spacing
--space-10:  40px   (2.5rem)  — large gaps
--space-12:  48px   (3rem)    — page section gaps
--space-16:  64px   (4rem)    — major section spacing
--space-20:  80px   (5rem)    — hero spacing
```

## Component Spacing Rules

**Buttons:**
- Small: `padding: 6px 12px` — `--space-1-half --space-3`
- Default: `padding: 8px 16px` — `--space-2 --space-4`
- Large: `padding: 10px 20px` — `--space-2-half --space-5`

**Cards:**
- Compact: `padding: 16px` — `--space-4`
- Default: `padding: 20px 24px` — `--space-5 --space-6`
- Generous: `padding: 24px 32px` — `--space-6 --space-8`

**Table cells:**
- Default: `padding: 12px 16px` — `--space-3 --space-4`
- Compact: `padding: 8px 12px` — `--space-2 --space-3`

**Form inputs:**
- Default: `padding: 8px 12px` — `--space-2 --space-3`

---

# Part XXII: Elevation System

## Philosophy

In dark UIs, elevation is expressed through **lightness**, not shadows. Higher elevation = lighter background. This is how macOS dark mode works. This is how Linear and Vercel work.

Shadows are used *additionally* for floating elements (dropdowns, modals, tooltips) — but background lightness is the primary elevation signal.

```
Level 0 (void):    --surface-void     hsl(225, 25%, 4%)
Level 1 (base):    --surface-base     hsl(225, 22%, 8%)
Level 2 (raised):  --surface-raised   hsl(225, 20%, 11%)
Level 3 (overlay): --surface-overlay  hsl(225, 18%, 14%)
Level 4 (elevated):--surface-elevated hsl(225, 16%, 18%)
```

The lightness increases as elevation increases. The jump between levels is deliberately small (2–3% lightness) — enough to feel like a layer, not enough to draw attention.

## Elevation Mapping

| Element | Elevation Level | Additional Shadow |
|---------|----------------|-------------------|
| Page background | 0 | None |
| Main content area | 1 | None |
| Cards, panels | 2 | `--shadow-sm` |
| Dropdowns, popovers | 3 | `--shadow-md` |
| Modals, command palette | 4 | `--shadow-lg` |
| Tooltips | 4 | `--shadow-sm` |
| Context menus | 4 | `--shadow-lg` |

---

# Part XXIII: Color System

## Design Rationale

The current Genesis palette is `slate-*` — the default Tailwind dark mode. It is recognizable as Tailwind. This is a problem. The product must feel like itself, not like a Tailwind template.

The new Genesis palette is **Void Black** — a blue-shifted dark background that is cooler and more technical than neutral gray. The difference is subtle but immediately felt. Compared to `slate-950` (#020617), the new `--surface-void` (#07090F) has more blue in it, giving the entire interface a slightly "electric" quality.

The accent color shifts from `blue-500` (#3B82F6) to **Iris** (`#4F6EF7`) — a slightly purple-shifted blue. This is important: `#3B82F6` is universally recognized as Tailwind blue. `#4F6EF7` is distinct — more indigo, less generic, more "intelligent". Linear uses a similar hue. Raycast uses a similar hue.

## Color Hierarchy

**80% of the interface** should be in the surface and text tokens — backgrounds and text. The interface should feel almost monochrome.

**15% of the interface** should be in accent (iris blue) — used for: primary buttons, active nav indicators, links, focus rings, active status badges, the phase stepper's active step.

**5% of the interface** should be in semantic colors (success/warning/error) — used strictly for status communication, never for decoration.

## Light Mode Consideration

The product is **dark mode only in v1**. Light mode will be added in v2. Design rationale: the user base (software engineers) strongly prefers dark mode; implementing a good light mode requires a full second token set and is a significant investment. Ship dark first, ship it perfectly.

---

# Part XXIV: Component Hierarchy

## Atomic Components (lowest level)

These are the primitive building blocks. They are unstyled in terms of layout but fully styled in terms of visual appearance.

- `Button` (variants: primary, secondary, ghost, destructive; sizes: sm, md, lg)
- `Input` (variants: default, error, disabled; types: text, password, search)
- `Select` (custom styled dropdown)
- `Checkbox`
- `Toggle`
- `Badge` (status badges, count badges, tag badges)
- `Icon` (Lucide icons wrapped in a sizing utility)
- `Kbd` (keyboard shortcut display)
- `Tooltip`
- `Spinner`
- `Skeleton`

## Molecular Components (composed from atomics)

- `StatCard` = Icon + Metric + Label + Delta
- `StatusBadge` = Icon + Text (variant based on status enum)
- `ProjectCard` = Card + StatusBadge + SparkLine + ActionMenu
- `RunRow` = TableRow + StatusBadge + Duration + ActionMenu
- `PhaseBlock` = Header (PhaseName + Duration + Status) + EventList (collapsible)
- `ArtifactRow` = FileIcon + Filename + Filesize + HashDisplay + DownloadButton
- `NavItem` = Icon + Label + ActiveIndicator + Count (optional)
- `Breadcrumb` = BreadcrumbItem[] (each clickable except last)
- `CommandItem` = Icon + Label + SecondaryLabel + ActionButtons + KbdHint

## Organism Components (composed from molecular)

- `AppShell` = GlobalRail + ContextPanel + Header + MainArea + RightPanel
- `ContextPanel` = Header + NavSection[] + ProjectTree (when project active)
- `CommandPalette` = Input + CategorySection[] (full-screen overlay)
- `NotificationCenter` = TriggerButton + Dropdown (NotificationItem[])
- `ArchitectureGraph` = FilterPanel + ReactFlowCanvas + NodeDetailPanel
- `WorkspaceExplorer` = FileTree + TabBar + MonacoViewer + StatusBar
- `CompilerOutput` = PhaseBlock[] (scrollable)
- `RunHeader` = BreadcrumbRow + StatusBadge + MetaRow + ActionRow
- `PlanningReport` = StatusBanner + MetricsGrid + RuleTable + IssueDetail

---

# Part XXV: Page Hierarchy

## Visual Weight Hierarchy Per Page

Every page must have exactly one primary visual element. The eye should naturally land on it first.

| Page | Primary Visual | Secondary | Tertiary |
|------|---------------|-----------|----------|
| Dashboard | Active Run cards | Health stats | Project grid |
| Projects | Project cards/table | Toolbar | Pagination |
| Compiler | Monaco editor | Compile button | Right panel output |
| Run Overview | Status badge | Phase timeline | Spec summary |
| Compiler Trace | Phase blocks | Phase stepper | Toolbar |
| Architecture | Graph canvas | Node list | Node detail |
| Workspace | Monaco viewer | File tree | Status bar |
| Artifacts | Artifact list | Hash section | Download all |
| Planning Report | Status banner | Rule table | Issue detail |

---

# Part XXVI: Animation Philosophy

## The Contract

The animation system must satisfy a contract with the user: **animations communicate state changes, never decorate**.

If removing an animation makes the interface harder to understand, the animation is functional. If removing it has no impact on comprehension, it should be removed.

## The Four Categories of Animation

**Category 1: Transition animations** — Communicate spatial relationships.
- Page transitions: new page slides in from the right, old page slides out to the left (only if navigation has a clear direction). Uses Framer Motion `AnimatePresence`.
- Panel open/close: right panel slides in from right (200ms `ease-out`). Context panel slides in from left (200ms `ease-out`).
- Dropdown/menu: `scale(0.95) + opacity(0) → scale(1) + opacity(1)` (120ms `ease-out`)

**Category 2: State animations** — Communicate property changes.
- Status badge change (RUNNING → SUCCESS): Crossfade between the two states (300ms)
- Number counter (stat cards): Animate from 0 to the value using spring physics (400ms, stiffness 100)
- Progress bar fill: Width transition (300ms `ease-out`)

**Category 3: Attention animations** — Guide focus to important changes.
- New event in compiler feed: `slide-in-from-bottom-4 + fade-in` (150ms)
- New notification: Bell icon bounces once (keyframe, 300ms)
- Error state appearance: Shake animation on affected component (300ms)
- New run in dashboard: `slide-in-from-top-2 + fade-in` (200ms)

**Category 4: Operational animations** — Communicate ongoing work.
- Active run status indicator: Dual-ring pulse (2s loop, infinite while RUNNING)
- Skeleton shimmer: Gradient sweep (1.6s loop)
- Spinner: 360° rotation (0.8s linear, infinite)

## Motion Guidelines

**Duration rules:**
- Hover effects: 100ms
- UI state changes (color, border): 150ms
- Component enter/exit: 200ms
- Page transitions: 300ms
- Nothing exceeds 400ms (with the exception of spring-based number animations)

**Easing rules:**
- Entering elements: `cubic-bezier(0.0, 0.0, 0.2, 1)` (`ease-out`) — fast start, slow end
- Exiting elements: `cubic-bezier(0.4, 0.0, 1, 1)` (`ease-in`) — slow start, fast end
- State changes: `cubic-bezier(0.4, 0.0, 0.2, 1)` (`ease-in-out`) — smooth through

**Spring physics** (Framer Motion):
- Standard spring: `{ stiffness: 300, damping: 30 }`
- Bouncy spring (notification bell): `{ stiffness: 600, damping: 20 }`
- Gentle spring (number counter): `{ stiffness: 100, damping: 20 }`

---

# Part XXVII: Keyboard Shortcut System

## Design Philosophy

Keyboard shortcuts in Genesis have three tiers:

**Tier 1: Universal** — Work from any page, any context.
- `⌘K` / `Ctrl+K`: Command Palette
- `⌘/` / `Ctrl+/`: Toggle context panel
- `⌘P` / `Ctrl+P`: Toggle right panel
- `Escape`: Close modal / palette / dropdown / panel

**Tier 2: Navigation** — Work from any page (not when typing in an input).
- `G then D`: Go to Dashboard
- `G then P`: Go to Projects
- `G then C`: Go to Compiler
- `G then R`: Go to Runs
- `G then T`: Go to Telemetry
- `N`: New (context-aware: new project on Projects page, new run on Project page)

**Tier 3: Contextual** — Only active on specific pages.

*On Run Overview / any Run page:*
- `1`: Overview
- `2`: Compiler Trace
- `3`: Architecture
- `4`: Workspace
- `5`: Artifacts
- `6`: Planning Report
- `R`: Re-run with same spec
- `D`: Download artifacts

*On Compiler page:*
- `⌘Enter` / `Ctrl+Enter`: Run compiler
- `⌘S` / `Ctrl+S`: Validate spec
- `⌘Shift+F` / `Ctrl+Shift+F`: Format JSON

*On Architecture Graph:*
- `F`: Fit view
- `+` / `-`: Zoom in / out
- `Escape`: Deselect all nodes

*On Workspace Explorer:*
- `⌘F` / `Ctrl+F`: Find in file
- `⌘W` / `Ctrl+W`: Close current tab

## Shortcut Discoverability

Keyboard shortcuts are discovered through three channels:
1. **Tooltips:** Every button with a shortcut shows the shortcut in the tooltip (`⌘K`)
2. **Command Palette:** All commands show their shortcut on the right
3. **Help modal:** `?` key (when not in an input) opens a shortcut reference modal

---

# Part XXVIII: Design Rationale Summary

## The Ten Most Important Decisions

**1. The object model is `Run`, not `Project`.**
The current product treats the workspace as the primary object. In the redesign, a `Run` (compilation attempt) is the primary object. This is because engineers care about *what was compiled, when, and whether it succeeded* — not about abstract project containers.

**2. The right panel is a persistent context zone, not a feature.**
Moving the compiler output from a dashboard widget to a persistent right panel fundamentally changes how the product feels. The dashboard is now a command center. The right panel is a viewport into current activity. These are different jobs; they now live in different zones.

**3. Navigation is spatial (hierarchy), not categorical (pages).**
The context panel changes its content based on your position in the object hierarchy. You're not navigating to pages — you're moving through a space. This is the Linear insight applied to Genesis.

**4. Phase blocks are the unit of the compiler trace.**
The Warp-inspired "block" model transforms the compilation log from a stream of text into a structured, navigable document. Each phase is a collapsed block. You can expand any phase. This makes the trace inspectable without being overwhelming.

**5. The Architecture Graph is a first-class view.**
In the current product, the graph is tab #3 on the project detail page. In the redesign, it has its own dedicated URL, its own toolbar, its own panel, and an architectural preview on the Run Overview. The graph is the most intellectually interesting output of Genesis; the product should treat it that way.

**6. The compiler page is separate from the dashboard.**
Mixing spec authoring, live monitoring, and project browsing on one page destroys all three experiences. The compiler lives at `/compiler`. The dashboard shows health metrics. The right panel shows live activity from anywhere.

**7. Iris blue replaces Tailwind blue.**
`#3B82F6` (Tailwind's `blue-500`) is recognized in milliseconds as "this was made with Tailwind". `#4F6EF7` (Iris) is distinct, slightly more indigo, slightly more premium. This single change makes the product look less like a template.

**8. Arial is eliminated entirely.**
`font-family: Arial, Helvetica, sans-serif` in `globals.css` is the loudest signal that this is a student project, not an enterprise product. Inter replaces it. JetBrains Mono replaces it in code contexts.

**9. Empty states include remediation CTAs.**
The current empty states are apologetic ("No graphs available. Has the compiler run yet?"). The new empty states are actionable ("Architecture unavailable. View Planning Report to see why."). They guide the user to the next step.

**10. The product is dark-only in v1.**
Rather than ship a mediocre light mode alongside a mediocre dark mode, we ship a perfect dark mode. The dark mode is the product's personality. It can be extended to light in v2 once the token system is proven.

---

*End of Product UX Architecture Specification v2.0*

*This document governs all frontend implementation decisions for Genesis Engine.*  
*No implementation should begin without reference to this document.*  
*All deviations require explicit design review.*
