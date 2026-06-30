# Current Milestone

Status: complete — Milestone 27 (Entity Field Inference and Rich Schema Generator).

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

## Current Validation Baseline

From `frontend/`:

```powershell
npm.cmd run lint
npm.cmd run build
npm.cmd test
git diff --check
```

Expected baseline (M27): lint pass, build pass, **23 files / 239 tests pass**, diff --check pass (CRLF warnings only).
Frontend product code was not touched in M27.

Engine/backend files changed in M27 (5 modified files):
- `genesis_engine/models/planning.py` — added `EntityFieldDef`, `EntityDefinition`; added `entity_definitions` to `ProposedApplicationPlan`
- `genesis_engine/models/spec.py` — added `entity_definitions: List[Dict[str, Any]]`
- `genesis_engine/core/planning_engine.py` — added field inference tables and `_infer_attributes()`; updated `_convert_spec_to_ir()` to populate entity attributes via inference or explicit definitions
- `genesis_engine/plugins/implementations/fastapi_plugin.py` — added `_py_type()` helper; rewrote `_generate_schemas_code()` for field-aware Pydantic schema generation
- `backend/app/api/genesis_controller.py` — pass `entity_definitions` from plan to spec

Scripts added in M27:
- `scripts/validate_m27.py` — M27 validation runner (36 checks; PASS)

## Stopping Point

Stop here until the user explicitly approves the next milestone.
