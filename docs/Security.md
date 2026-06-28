# Security Architecture

## Authentication
Genesis Engine uses a stateless JWT (JSON Web Token) authentication strategy.
- Users are issued tokens via the `/api/v1/auth/token` endpoint.
- Tokens expire by default after 8 days.

## Authorization (RBAC)
Authorization is permission-based rather than role-based.
- `COMPILE`: Can trigger parsing, planning, validation, and generation.
- `DEPLOY`: Can trigger packaging and deployment.
- `READ_WORKSPACE`: Can view projects, load files, and inspect telemetry.
- `DOWNLOAD_ARTIFACTS`: Can download generated outputs and ZIP bundles.
- `MANAGE_PROJECTS`, `MANAGE_USERS`: Administrator capabilities.

## Path Traversal Protection
All filesystem access is strictly routed through `PathValidator` (`backend/app/security/path_validator.py`).
- Prevents loading hidden directories (unless explicitly authorized for certain APIs).
- Blocks access outside the designated `WORKSPACE_ROOT`.
- Filters oversized files and unapproved binaries.

## Event Loop Protection
All underlying blocking I/O is routed through `FileSystemService` which delegates to `asyncio.to_thread()`, preventing disk stalls from degrading concurrent API responsiveness.
