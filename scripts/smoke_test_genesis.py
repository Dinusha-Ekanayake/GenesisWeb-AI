#!/usr/bin/env python3
"""
Genesis Engine -- Authenticated Smoke Test
==========================================
Verifies that the backend API, auth, and key endpoints work together
after frontend auth hardening (M13-M15).

Uses only Python stdlib -- no external dependencies required.

Default mode (read-only, no workspace mutations):
    python scripts/smoke_test_genesis.py

With explicit credentials:
    python scripts/smoke_test_genesis.py --username developer --password devpassword

Generate mode (creates workspace/smoke_test_001, may call LLM):
    python scripts/smoke_test_genesis.py --generate

Custom backend:
    python scripts/smoke_test_genesis.py --backend-url http://127.0.0.1:8000 --api-prefix /api/v1

Exit codes:
    0  all automated checks passed
    1  one or more automated checks failed
"""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request


# ---------------------------------------------------------------------------
# Result tracking
# ---------------------------------------------------------------------------

_failures: list[str] = []


def _pass(label: str, detail: str = "") -> None:
    suffix = f"  -- {detail}" if detail else ""
    print(f"  [PASS] {label}{suffix}")


def _fail(label: str, detail: str = "") -> None:
    suffix = f"  -- {detail}" if detail else ""
    print(f"  [FAIL] {label}{suffix}")
    _failures.append(label)


def _skip(label: str, detail: str = "") -> None:
    suffix = f"  -- {detail}" if detail else ""
    print(f"  [SKIP] {label}{suffix}")


# ---------------------------------------------------------------------------
# HTTP helper (stdlib only)
# ---------------------------------------------------------------------------

def http(
    method: str,
    url: str,
    *,
    headers: dict | None = None,
    data: bytes | None = None,
    timeout: int = 15,
) -> tuple[int | None, object]:
    """
    Make an HTTP request.
    Returns (status_code, parsed_json_body).
    Returns (None, error_string) if the server is unreachable.
    """
    req = urllib.request.Request(
        url,
        data=data,
        headers=headers or {},
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, (json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            return exc.code, json.loads(raw)
        except Exception:
            return exc.code, {"detail": raw}
    except (urllib.error.URLError, OSError, TimeoutError) as exc:
        return None, str(exc)


def _detail(body: object) -> str:
    """Extract a short error string from an API response body."""
    if isinstance(body, dict):
        return str(body.get("detail") or body)
    return str(body)[:200]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Genesis Engine authenticated smoke test",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--backend-url",
        default="http://127.0.0.1:8000",
        metavar="URL",
        help="Backend base URL (default: http://127.0.0.1:8000)",
    )
    parser.add_argument(
        "--api-prefix",
        default="/api/v1",
        metavar="PATH",
        help="API path prefix (default: /api/v1)",
    )
    parser.add_argument(
        "--username",
        default="developer",
        help="Login username (default: developer)",
    )
    parser.add_argument(
        "--password",
        default="devpassword",
        help="Login password (default: devpassword)",
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help=(
            "Enable compile endpoints: POST /genesis/validate and POST /genesis/generate. "
            "Creates workspace/smoke_test_001. May invoke LLM if OPENAI_API_KEY is set."
        ),
    )
    args = parser.parse_args()

    base = args.backend_url.rstrip("/")
    api = f"{base}{args.api_prefix}"

    print()
    print("Genesis Engine -- Authenticated Smoke Test")
    print("=" * 52)
    print(f"  Backend : {base}")
    print(f"  API     : {api}")
    print(f"  User    : {args.username}")
    print(f"  Mode    : {'generate (mutations enabled)' if args.generate else 'read-only'}")
    print()

    # -------------------------------------------------------------------------
    # 1. Backend health
    # -------------------------------------------------------------------------
    print("1. Backend Health")
    status, body = http("GET", f"{base}/health")
    if status is None:
        _fail("GET /health", body)  # type: ignore[arg-type]
        print()
        print("  Backend is unreachable. Start it first:")
        print()
        print("    # Activate the project venv, then:")
        print("    cd backend")
        print("    uvicorn main:app --reload --port 8000")
        print()
        sys.exit(1)
    elif status == 200:
        _pass("GET /health", str(body.get("status", "ok")))  # type: ignore[union-attr]
    else:
        _fail("GET /health", f"HTTP {status}")

    # -------------------------------------------------------------------------
    # 2. Authentication
    # -------------------------------------------------------------------------
    print("\n2. Authentication")
    form = urllib.parse.urlencode(
        {"username": args.username, "password": args.password}
    ).encode()
    status, body = http(
        "POST",
        f"{api}/auth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=form,
    )
    if status == 200 and isinstance(body, dict) and "access_token" in body:
        token: str = body["access_token"]
        _pass(f"POST /auth/token  (user: {args.username})", "token acquired")
    elif status == 401:
        _fail(f"POST /auth/token  (user: {args.username})", "invalid credentials")
        print()
        print("  Check --username / --password.")
        print("  Built-in accounts: developer/devpassword, admin/admin, viewer/viewpassword")
        sys.exit(1)
    else:
        _fail("POST /auth/token", f"HTTP {status}: {_detail(body)}")
        sys.exit(1)

    auth = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # -------------------------------------------------------------------------
    # 3. Project list
    # -------------------------------------------------------------------------
    print("\n3. Project List")
    status, body = http("GET", f"{api}/genesis/projects", headers=auth)
    if status == 200 and isinstance(body, dict):
        projects: list = body.get("data") if isinstance(body.get("data"), list) else []
        _pass("GET /genesis/projects", f"{len(projects)} project(s) in workspace")
    else:
        projects = []
        _fail("GET /genesis/projects", f"HTTP {status}: {_detail(body)}")

    # -------------------------------------------------------------------------
    # 4. Per-project detail (first project only)
    # -------------------------------------------------------------------------
    print("\n4. Project Detail")
    if projects:
        pid: str = projects[0].get("id", "")
        pid_label = pid or "<unknown-id>"

        status, body = http(
            "GET", f"{api}/genesis/projects/{pid}", headers=auth
        )
        if status == 200:
            _pass(f"GET /genesis/projects/{pid_label}")
        else:
            _fail(f"GET /genesis/projects/{pid_label}", f"HTTP {status}: {_detail(body)}")

        status, body = http(
            "GET", f"{api}/genesis/projects/{pid}/workspace", headers=auth
        )
        if status == 200:
            tree = body.get("data") or [] if isinstance(body, dict) else []  # type: ignore[union-attr]
            _pass(
                f"GET /genesis/projects/{pid_label}/workspace",
                f"{len(tree)} item(s)",
            )
        elif status == 404:
            _skip(
                f"GET /genesis/projects/{pid_label}/workspace",
                "not found (project may be incomplete)",
            )
        else:
            _fail(
                f"GET /genesis/projects/{pid_label}/workspace",
                f"HTTP {status}: {_detail(body)}",
            )

        status, body = http(
            "GET", f"{api}/genesis/projects/{pid}/manifest", headers=auth
        )
        if status == 200:
            manifest_data = body.get("data") if isinstance(body, dict) else None  # type: ignore[union-attr]
            _pass(
                f"GET /genesis/projects/{pid_label}/manifest",
                "manifest present" if manifest_data else "null (not yet compiled)",
            )
        elif status == 404:
            _skip(f"GET /genesis/projects/{pid_label}/manifest", "not found")
        else:
            _fail(
                f"GET /genesis/projects/{pid_label}/manifest",
                f"HTTP {status}: {_detail(body)}",
            )

        status, body = http(
            "GET", f"{api}/genesis/projects/{pid}/graphs", headers=auth
        )
        if status == 200:
            graphs = body.get("data") or {} if isinstance(body, dict) else {}  # type: ignore[union-attr]
            _pass(
                f"GET /genesis/projects/{pid_label}/graphs",
                f"{len(graphs)} graph(s)",
            )
        elif status == 404:
            _skip(f"GET /genesis/projects/{pid_label}/graphs", "not found")
        else:
            _fail(
                f"GET /genesis/projects/{pid_label}/graphs",
                f"HTTP {status}: {_detail(body)}",
            )
    else:
        _skip(
            "Per-project checks",
            "no projects in workspace -- run with --generate to create one",
        )

    # -------------------------------------------------------------------------
    # 5. Compile endpoints (opt-in with --generate)
    # -------------------------------------------------------------------------
    print("\n5. Compile Endpoints")
    if args.generate:
        smoke_spec = {
            "project_id": "smoke_test_001",
            "name": "Smoke Test",
            "description": "Minimal spec for Genesis Engine smoke testing.",
            "pages": ["Dashboard"],
            "components": ["Navbar"],
        }
        body_bytes = json.dumps(smoke_spec).encode()

        status, body = http(
            "POST",
            f"{api}/genesis/validate",
            headers=auth,
            data=body_bytes,
            timeout=60,
        )
        if status == 200:
            score = (body.get("data") or {}).get("score", "?") if isinstance(body, dict) else "?"  # type: ignore[union-attr]
            _pass("POST /genesis/validate", f"integrity score={score}")
        else:
            _fail("POST /genesis/validate", f"HTTP {status}: {_detail(body)}")

        print(
            "  Generating project 'smoke_test_001' "
            "-- this may take 30-120 seconds..."
        )
        status, body = http(
            "POST",
            f"{api}/genesis/generate",
            headers=auth,
            data=body_bytes,
            timeout=180,
        )
        if status == 200:
            manifest = (body.get("data") or {}).get("manifest") or {} if isinstance(body, dict) else {}  # type: ignore[union-attr]
            proj_id = manifest.get("project_id", smoke_spec["project_id"])
            _pass("POST /genesis/generate", f"project_id={proj_id}")
        else:
            _fail("POST /genesis/generate", f"HTTP {status}: {_detail(body)}")
    else:
        _skip("POST /genesis/validate", "pass --generate to test compilation")
        _skip("POST /genesis/generate", "pass --generate to test compilation")

    # -------------------------------------------------------------------------
    # 6. Frontend manual checklist
    # -------------------------------------------------------------------------
    frontend_url = "http://localhost:3000"
    print(f"\n6. Frontend Manual Checklist  (start: cd frontend && npm run dev)")
    print()
    routes = [
        ("/login",     "Public  -- login form, no token required"),
        ("/dashboard", "Guard   -- Genesis Engine control plane"),
        ("/compiler",  "Guard   -- Monaco spec editor + compile button"),
        ("/projects",  "Guard   -- project list from backend"),
        ("/runs",      "Guard   -- runs list from backend"),
        ("/search",    "Guard   -- search over project metadata"),
        ("/settings",  "Guard   -- local preferences, logout button"),
        ("/telemetry", "Guard   -- project metadata summary"),
    ]
    for route, note in routes:
        print(f"  [ ] {frontend_url}{route:<15}  {note}")

    print()
    print("  Auth flow verification:")
    print(f"  [ ] Open {frontend_url}/projects without a token"
          "  =>  redirected to /login")
    print(f"  [ ] Login with {args.username} / {args.password}"
          "  =>  redirected to /dashboard")
    print(f"  [ ] Click Sign Out in header"
          "  =>  token removed, redirected to /login")
    print(f"  [ ] Clear token in DevTools and reload /projects"
          "  =>  AuthGuard redirects to /login")
    print(f"  [ ] Set an invalid token and reload /projects"
          "  =>  API returns 401, token cleared, redirected to /login")

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    print()
    print("=" * 52)
    if _failures:
        print(
            f"RESULT: FAIL  "
            f"({len(_failures)} check(s) failed: {', '.join(_failures)})"
        )
        sys.exit(1)
    else:
        print("RESULT: PASS  (all automated checks passed)")
        sys.exit(0)


if __name__ == "__main__":
    main()
