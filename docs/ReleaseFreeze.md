# Genesis Engine v1.0 Release Freeze

## Current Version
**Version:** 1.0.0
**Git Tag Recommendation:** `v1.0.0-phase11-final`

## Frozen Folder Structure
The repository structure is now considered stable and frozen for Phase 11.
- `/backend`: FastAPI control plane and security services.
- `/frontend`: Next.js dashboard UI.
- `/genesis_engine`: Core compiler (Planning, Generation, Deployment).
- `/scripts`: Quality Gates and Testing utilities.

## Frozen APIs
All endpoints in `/genesis` are now frozen. Any breaking changes require a `/v2/` namespace.
**Note:** All endpoints (except SSE `/events` which uses token query parameters) are secured via JWT RBAC.

## Frozen Dependency Versions
- Python: `3.12+`
- FastAPI: `0.110.0`
- LangGraph: `0.0.30`
- React: `18.2.0`
- Next.js: `14.1.0`
- ReactFlow: `12.0.0`

## Frozen Compiler Architecture
The deterministic compiler pipeline is finalized:
1. **Planning Engine**
2. **Generation Engine**
3. **Build Orchestrator**

*The compiler is entirely separated from CI/CD tooling. Quality gates are strictly CLI/Developer utilities.*

## Known Limitations
- Heavy file I/O operations inside the compiler are synchronous (though running in isolated threads) by design to maintain strict determinism.
- The `users.json` repository is static and intended to be replaced with a database implementation in Phase 12.

## Technical Debt
- Need robust database backing for long-term project/workspace persistence.
- E2E tests are implemented but could use greater assertion depth for generated ZIP structure.

## Deferred Features
- Multi-user collaboration.
- External Git repository integrations.
- Advanced cloud deployment targets (AWS/GCP).

## Phase 12 Starting Assumptions
Phase 12 will focus on Project & Workspace Management. The fundamental compiler architecture will NOT be altered in Phase 12. Phase 12 will inherit the strict RBAC models introduced in Phase 11.3/11.4.
