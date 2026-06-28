# Testing Guide

## Quality Gates (CLI Only – Not Runtime)

The Genesis Engine enforces strict quality gates through CI/CD pipelines and manual developer
workflows. These scripts are **strictly decoupled** from the runtime compiler.
The runtime compiler pipeline must NEVER execute any of these scripts.

### Available Scripts

| Script | Purpose |
|--------|---------|
| `scripts/quality_gate.py` | Orchestrates all quality checks (linting, type-checking, tests). |
| `scripts/verify_contracts.py` | Verifies frontend API calls map to real backend OpenAPI endpoints. |
| `scripts/benchmark.py` | Measures compiler stage performance, memory, and artifact sizes. |
| `scripts/test_determinism.py` | Proves the compiler produces identical output across two independent runs. |

## Coverage Requirements

| Layer | Required |
|-------|---------|
| Backend | 90% |
| Frontend | 80% |
| Core Compiler | 95% |
| Rule Engine | 100% |

## Test Frameworks

1. **Pytest (Backend):** Covers PathValidator, PubSub event bus, compiler orchestration, and mutation rejection.
   - `backend/tests/test_phase11_2.py`
   - `backend/tests/test_mutations.py`

2. **Vitest + React Testing Library (Frontend):** Covers dashboard components in isolation.
   - `frontend/tests/` — component and API client unit tests.

3. **Playwright (End-to-End):** Covers the integrated user workflow (login → compile → inspect → download).
   - `frontend/e2e/workflow.spec.ts`

## Contract Testing

`scripts/verify_contracts.py` parses the FastAPI OpenAPI schema and the frontend `genesis-api.ts`
to detect orphaned API calls (frontend calls a path with no backend match) or removed endpoints.
This script is invoked by `quality_gate.py` and must pass before any release packaging.

## Benchmarking

`scripts/benchmark.py` runs the full compiler pipeline against a benchmark specification and
produces a JSON report (`benchmark_report.json`) with per-stage timing, peak memory (via
`tracemalloc`), workspace size, and deployment zip size. This script is used to detect
performance regressions between releases.

## Mutation Testing

`backend/tests/test_mutations.py` intentionally injects structural corruptions
(missing project IDs, invalid architectures, circular dependencies, tampered planning reports)
and asserts the compiler correctly rejects each mutation.
