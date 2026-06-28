# Testing Guide

## Quality Gates
The Genesis Engine enforces strict quality gates through CI/CD pipelines and manual developer workflows.
The script `scripts/quality_gate.py` is executed via CLI for validation and is **strictly decoupled** from the runtime compiler.

## Minimum Coverage Requirements
- **Backend:** 90%
- **Frontend:** 80%
- **Core Compiler:** 95%
- **Rule Engine:** 100%

## Frameworks
1. **Pytest (Backend)**: Covers the compiler logic, path validators, and orchestrators.
2. **Vitest + React Testing Library (Frontend)**: Covers the React dashboard components and isolated hooks.
3. **Playwright (End-to-End)**: Covers the integrated workflow from specification definition, UI compilation, and artifact downloading.

## Mutation Testing
We execute intentional negative tests in `test_mutations.py` to prove that the Planning Engine correctly traps and blocks tampered ASTs, circular graphs, and malformed dependencies.
