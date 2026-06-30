# Current Milestone

Status: complete — Milestone 25 (Rich App Spec v2 and Approved Plan Compiler Mapping).

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

## Current Validation Baseline

From `frontend/`:

```powershell
npm.cmd run lint
npm.cmd run build
npm.cmd test
git diff --check
```

Expected baseline (M25): lint pass, build pass, **23 files / 239 tests pass**, diff --check pass (CRLF warnings only).
Frontend product code was not touched in M25.

Engine/backend files changed in M25 (4 modified files):
- `genesis_engine/models/spec.py` (added 13 optional rich fields to `ProjectSpecification`)
- `genesis_engine/models/ir.py` (added 6 optional rich fields to `GenesisIR`)
- `genesis_engine/core/planning_engine.py` (imported `GenesisEntity`; updated `_convert_spec_to_ir()`)
- `backend/app/api/genesis_controller.py` (updated plan→spec conversion to map all 13 rich fields)

## Stopping Point

Stop here until the user explicitly approves the next milestone.
