# Current Milestone

Status: complete — Milestone 34 (Generated App UI Styling Foundation).

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
- M5.2: Planning Report Surface
- M5.3: Architecture Graph Surface
- M5.4: Workspace Surface
- M5.5: Artifacts Surface
- M5.6: Run Detail Visual QA and Consistency Pass
- M6: Dashboard / Product Home Redesign
- M7: Command Palette and Keyboard Shortcuts
- M8: Search Route / Global Search Surface
- M9: Settings / Preferences Surface
- M10: Telemetry Surface
- M11: Final Route QA and Production Readiness Pass
- M12: Backend-Connected Manual Smoke Test Support
- M13: Login / Auth UX Integration
- M14: Auth Guard / Unauthorized Redirect
- M15: Auth Expiry / 401 Handling
- M16: Authenticated End-to-End Smoke Test Runner
- M17: Real Compiler Generate Smoke Test
- M18: Generated App Quality Benchmark
- M19: Genesis Engine Product Direction Reset and Target Architecture Plan
- M20: Persist Manifest, Architecture Graphs, and Planning Report
- M21: Separate Pages and Components in Compiler IR
- M22: Planning-First Architecture and Tech Stack Proposal
- M23: Approval-Gated Plan Validation and Generate Flow
- M24: Generated App Package Configs and Build-Ready Skeleton
- M25: Rich App Spec v2 and Approved Plan Compiler Mapping
- M26: FastAPI Entity, Schema, and CRUD Generator Foundation
- M27: Entity Field Inference and Rich Schema Generator
- M28: Planned API Route Consumption and API Graph Alignment
- M29: SQLAlchemy Model and SQLite Persistence Foundation
- M30: Frontend API Integration Foundation
- M31: Full CRUD Frontend UI Foundation
- M32: Multi-Field Entity Forms
- M33: Generator Architecture Refactor
- M34: Generated App UI Styling Foundation

## Current Validation Baseline

From `frontend/`:

```powershell
npm.cmd run lint
npm.cmd run build
npm.cmd test
git diff --check
```

Expected baseline (M34): lint pass, build pass, **23 files / 239 tests pass**, diff --check pass (CRLF warnings only).
Platform frontend product code was not touched in M34.

Engine files changed in M34 (2 modified, 1 new script):
- `genesis_engine/plugins/implementations/nextjs_generators/config_generator.py` — globals.css extended with full CSS design system
- `genesis_engine/plugins/implementations/nextjs_generators/entity_page_generator.py` — className on all structural JSX elements, empty-state paragraph, error-banner class
- `scripts/validate_m34.py` (new) — 11-section M34 validation runner

Engine files changed in M33 (17 files — 2 modified, 15 new):
- `genesis_engine/plugins/implementations/nextjs_plugin.py` — rewritten as 48-line thin orchestrator; all logic extracted to `nextjs_generators/` subpackage.
- `genesis_engine/plugins/implementations/fastapi_plugin.py` — rewritten as 24-line thin orchestrator; all logic extracted to `fastapi_generators/` subpackage.
- `genesis_engine/plugins/implementations/nextjs_generators/__init__.py` (new)
- `genesis_engine/plugins/implementations/nextjs_generators/config_generator.py` (new)
- `genesis_engine/plugins/implementations/nextjs_generators/api_client_generator.py` (new)
- `genesis_engine/plugins/implementations/nextjs_generators/types_generator.py` (new)
- `genesis_engine/plugins/implementations/nextjs_generators/entity_page_generator.py` (new)
- `genesis_engine/plugins/implementations/nextjs_generators/static_page_generator.py` (new)
- `genesis_engine/plugins/implementations/nextjs_generators/component_generator.py` (new)
- `genesis_engine/plugins/implementations/fastapi_generators/__init__.py` (new)
- `genesis_engine/plugins/implementations/fastapi_generators/config_generator.py` (new)
- `genesis_engine/plugins/implementations/fastapi_generators/database_generator.py` (new)
- `genesis_engine/plugins/implementations/fastapi_generators/models_generator.py` (new)
- `genesis_engine/plugins/implementations/fastapi_generators/schemas_generator.py` (new)
- `genesis_engine/plugins/implementations/fastapi_generators/router_generator.py` (new)
- `genesis_engine/plugins/implementations/fastapi_generators/main_generator.py` (new)
- `genesis_engine/plugins/implementations/fastapi_generators/minimal_backend_generator.py` (new)

No scripts changed in M33 — regressions from M26–M32 served as the full validation suite.

**Generated frontend structure (entity apps, M32):**
- `frontend/lib/api.ts` — generic CRUD client (unchanged from M30)
- `frontend/lib/types.ts` — one `interface {Name}` + `type {Name}Create = Omit<{Name}, "id">` per entity (unchanged from M30)
- `frontend/app/{plural}/page.tsx` — `"use client"` page per entity with list table, typed multi-field form (one input per non-id field), inline edit (all fields pre-populated), and delete
- `frontend/.env.example` — `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8010` (unchanged from M30)

## Stopping Point

Stop here until the user explicitly approves the next milestone.

## Prior Milestone Engine Changes (M31)

Engine/frontend files changed in M31 (1 modified file):
- `genesis_engine/plugins/implementations/nextjs_plugin.py` — `_generate_entity_page_code()` rewritten: added `updateItem`/`deleteItem` imports; added `editingId`/`editingValue` state; rewrote `handleSubmit` to branch on edit vs create; added `handleDelete`; updated form to dual-mode input with Save/Cancel; added Edit/Delete buttons per table row with `<th>actions</th>` column.

Scripts created in M31:
- `scripts/validate_m31.py` (new) — 11-section CRUD validation runner.

## Prior Milestone Engine Changes (M30)

Engine/frontend files changed in M30 (1 rewritten file):
- `genesis_engine/plugins/implementations/nextjs_plugin.py` — added `_pluralize()`, `_ts_type()` helpers; added `_generate_api_lib_code()` (generic typed fetch functions); added `_generate_types_code(entities)` (TypeScript interfaces per entity); added `_generate_entity_page_code(table, plural)` (`"use client"` pages with `useEffect`/`useState` list + create form); extended `_generate_config_files()` with `frontend/.env.example`; updated `generate()` to dispatch on `context.database_graph.tables` for entity vs no-entity path; entity routes take priority over page-graph routes (collision dedup).

Scripts created in M30:
- `scripts/validate_m30.py` (new) — 44-check validation runner.

## Prior Milestone Engine Changes (M29)

Engine/backend files changed in M29 (1 rewritten file):
- `genesis_engine/plugins/implementations/fastapi_plugin.py` — replaced in-memory `storage.py` generation with real SQLAlchemy + SQLite persistence: added `_sa_type()`, `_generate_database_code()` (engine/SessionLocal/Base/get_db), `_generate_models_code()` (one SQLAlchemy model per entity); updated `_generate_schemas_code()` for `ConfigDict(from_attributes=True)`; rewrote `_generate_router_code()` for SQLAlchemy `Session = Depends(get_db)` CRUD; updated `_generate_entity_main_code()` to call `Base.metadata.create_all(bind=engine)`; deleted `_generate_storage_code()`.

Scripts changed in M29:
- `scripts/validate_m29.py` (new) — 45-check validation runner: file tree, py_compile, content checks, live CRUD on port 8010, restart-persistence check, `genesis_app.db` existence check.
- `scripts/validate_m26.py`, `scripts/validate_m27.py` (modified) — required-file/content checks updated to verify `database.py`/`models.py` instead of `storage.py`.

## Prior Milestone Engine Changes (M28)

Engine/backend files changed in M28 (2 modified files):
- `genesis_engine/pipeline/planners/api_planner.py` — rewrote `plan()` with three-priority dispatch: entity CRUD (5 routes/entity) → api_routes parse → page-derived fallback; added `_pluralize()`, `_entity_crud_endpoints()`, `_api_routes_endpoints()`, `_page_derived_endpoints()`
- `genesis_engine/plugins/implementations/fastapi_plugin.py` — fixed `_generate_minimal_backend()` function name derivation (path-based identifiers, not `endpoint.name`) to avoid invalid Python identifiers from parsed api_routes

Scripts added in M28:
- `scripts/validate_m28.py` — M28 validation runner (covers entity CRUD alignment, backward compat, api_routes parse; all checks PASS)

## Prior Milestone Engine Changes (M27)

Engine/backend files changed in M27 (5 modified files):
- `genesis_engine/models/planning.py` — added `EntityFieldDef`, `EntityDefinition`; added `entity_definitions` to `ProposedApplicationPlan`
- `genesis_engine/models/spec.py` — added `entity_definitions: List[Dict[str, Any]]`
- `genesis_engine/core/planning_engine.py` — added field inference tables and `_infer_attributes()`; updated `_convert_spec_to_ir()` to populate entity attributes via inference or explicit definitions
- `genesis_engine/plugins/implementations/fastapi_plugin.py` — added `_py_type()` helper; rewrote `_generate_schemas_code()` for field-aware Pydantic schema generation
- `backend/app/api/genesis_controller.py` — pass `entity_definitions` from plan to spec
