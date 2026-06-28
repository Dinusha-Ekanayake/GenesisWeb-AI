# Release Checklist (v1.0)

Before freezing the repository for a major release, ensure the following constraints hold true:
- [x] All Quality Gates pass successfully without bypassing.
- [x] OpenAPI schema fully syncs with TypeScript definitions (Contract Test passed).
- [x] No `asyncio.to_thread` leaks or synchronous disk blocks exist in the FastAPI controllers.
- [x] JWT Authentication is enforced correctly across all endpoints (including SSE).
- [x] Mutation tests correctly reject graph anomalies and tampered planning reports.
- [x] Benchmark reports indicate no degradation in Peak Memory or Processing Time compared to prior runs.
