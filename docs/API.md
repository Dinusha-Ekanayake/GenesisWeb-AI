# API Reference

The Genesis Control Plane exposes a REST API via FastAPI. The exact types can be viewed via the Swagger UI (`/docs`) or OpenAPI schema (`/openapi.json`).

## Envelope Format
All Genesis endpoints respond with the standard envelope:
```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "timestamp": "2026-06-27T10:00:00.000Z",
  "request_id": "uuid"
}
```

## Core Endpoints
- `POST /api/v1/auth/token`: Retrieve a JWT.
- `POST /api/v1/genesis/generate`: Submits a ProjectSpecification and runs the full compiler pipeline.
- `GET /api/v1/genesis/projects`: Lists compiled workspaces.
- `GET /api/v1/genesis/projects/{id}`: Fetches specific project metadata.
- `GET /api/v1/genesis/events`: Streams compiler telemetry via Server-Sent Events (SSE). Must pass `token` as a query parameter.
- `GET /api/v1/genesis/projects/{id}/artifacts/{name}`: Downloads binary or large JSON artifacts.
