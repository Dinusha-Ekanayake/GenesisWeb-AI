# Release Checklist (v1.0)

Before freezing the repository for a major release, ensure the following constraints hold true:

- [x] All Quality Gates pass successfully without bypassing (`scripts/quality_gate.py`).
- [x] Contract verification passes (`scripts/verify_contracts.py`). Verifies all frontend API calls map to real backend endpoints.
- [x] No `asyncio.to_thread` calls in FastAPI controllers. Threading is owned by `CompilerService`.
- [x] No synchronous filesystem operations (`open`, `mkdir`, `iterdir`) in FastAPI controllers or LangGraph nodes.
- [x] JWT Authentication is enforced correctly across all endpoints (including SSE token-param auth).
- [x] Mutation tests correctly reject graph anomalies and tampered planning reports (`backend/tests/test_mutations.py`).
- [x] Benchmark suite runs and produces a JSON report (`scripts/benchmark.py`).
- [x] No production code contains `MOCK_*` environment-variable testing branches.
- [x] No dead facades, `NotImplementedError`, or `pass`-only stubs in production modules.
- [x] Determinism regression test passes (`scripts/test_determinism.py`).
