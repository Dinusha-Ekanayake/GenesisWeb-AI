#!/usr/bin/env python3
"""
M28 Validation -- Planned API Route Consumption and API Graph Alignment
=======================================================================
Verifies that ApiPlanner generates entity CRUD endpoints (not page-placeholder
routes) when ir.entities exist, parses ir.api_routes when entities are absent,
and falls back to page-derived endpoints for simple no-entity specs.

Priority (must hold after M28):
  1. ir.entities present  → 5 CRUD endpoints per entity at /api/v1/{plural}
  2. ir.api_routes present → parse and normalize route strings
  3. otherwise            → page-derived GET+POST stubs (backward compat)

Usage:
    python scripts/validate_m28.py
    python scripts/validate_m28.py --backend-url http://127.0.0.1:8000
"""

import argparse
import json
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ALIGN_PROJECT_ID = "api_graph_alignment_001"
NO_ENTITIES_PROJECT_ID = "simple_no_entities_001"
ROUTES_PROJECT_ID = "api_routes_parse_001"

ALIGN_PROMPT = (
    "Create a CRM for a sales team with customers, deals, activities, "
    "reports, team roles, and settings."
)

_failures: list = []


def _pass(label: str, detail: str = "") -> None:
    suffix = f"  -- {detail}" if detail else ""
    print(f"  [PASS] {label}{suffix}")


def _fail(label: str, detail: str = "") -> None:
    suffix = f"  -- {detail}" if detail else ""
    print(f"  [FAIL] {label}{suffix}")
    _failures.append(label)


def http(method, url, *, headers=None, data=None, timeout=180):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
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


def _detail(body) -> str:
    if isinstance(body, dict):
        return str(body.get("detail") or body)[:400]
    return str(body)[:400]


def _pluralize(name: str) -> str:
    lower = name.lower()
    if lower.endswith("y") and len(lower) > 1 and lower[-2] not in "aeiou":
        return lower[:-1] + "ies"
    if lower.endswith("s") or lower.endswith("x") or lower.endswith("z"):
        return lower + "es"
    return lower + "s"


def _generate_via_propose(api, auth, project_id, prompt, preferences, workspace_root):
    """Propose and approve-and-generate. Returns proposed_plan dict or None."""
    ws = workspace_root / project_id
    if ws.exists():
        shutil.rmtree(ws, ignore_errors=True)
        print(f"  Cleaned prior workspace: {ws}")

    propose_payload = json.dumps({
        "prompt": prompt,
        "project_id": project_id,
        "preferences": preferences,
    }).encode()

    status, body = http("POST", f"{api}/genesis/propose", headers=auth,
                        data=propose_payload, timeout=60)
    if status != 200 or not (isinstance(body, dict) and body.get("success")):
        _fail(f"POST /genesis/propose ({project_id})", f"HTTP {status}: {_detail(body)}")
        return None

    data = body.get("data") or {}
    plan = data.get("plan")
    if not plan:
        _fail(f"proposed_plan extracted ({project_id})")
        return None

    entities = plan.get("entities", [])
    gen_method = plan.get("generation_method", "?")
    _pass(f"POST /genesis/propose ({project_id})",
          f"method={gen_method}  entities={len(entities)}: {entities}")

    gen_payload = json.dumps({
        "plan": plan,
        "approval": {
            "approved": True,
            "approved_by": "m28_validation",
            "notes": "M28 automated validation.",
        },
    }).encode()

    print(f"  Generating (may take 30-120s)...")
    status, body = http("POST", f"{api}/genesis/approve-and-generate", headers=auth,
                        data=gen_payload, timeout=180)
    if status == 200 and isinstance(body, dict) and body.get("success"):
        resp_data = body.get("data") or {}
        manifest = resp_data.get("manifest") or {}
        build_status = manifest.get("build_status", "?") if isinstance(manifest, dict) else "?"
        _pass(f"POST /genesis/approve-and-generate ({project_id})", f"build_status={build_status}")
        if build_status != "SUCCESS":
            _fail(f"build_status==SUCCESS ({project_id})", f"got {build_status}")
    else:
        _fail(f"POST /genesis/approve-and-generate ({project_id})",
              f"HTTP {status}: {_detail(body)}")
        return None

    return plan


def _load_api_graph(workspace_root, project_id):
    path = workspace_root / project_id / "artifacts" / "api_graph.json"
    if not path.exists():
        _fail(f"api_graph.json exists ({project_id})", f"NOT FOUND: {path}")
        return None
    _pass(f"api_graph.json exists ({project_id})")
    return json.loads(path.read_text(encoding="utf-8"))


def _check_entity_crud(api_graph, entities) -> None:
    endpoints = api_graph.get("endpoints", [])
    by_pm = {(e["path"], e["method"]): e for e in endpoints}

    for entity_name in entities:
        plural = _pluralize(entity_name)
        col = f"/api/v1/{plural}"
        item = f"/api/v1/{plural}/{{item_id}}"

        crud_spec = [
            ("GET",    col,  False),
            ("POST",   col,  True),
            ("GET",    item, False),
            ("PUT",    item, True),
            ("DELETE", item, True),
        ]

        for method, path, expect_auth in crud_spec:
            key = (path, method)
            if key not in by_pm:
                _fail(f"entity route {method} {path}", "MISSING")
                continue
            ep = by_pm[key]
            _pass(f"entity route {method} {path}")

            if ep.get("target_entity") == entity_name:
                _pass(f"  target_entity={entity_name!r} @ {method} {path}")
            else:
                _fail(f"  target_entity={entity_name!r} @ {method} {path}",
                      f"got {ep.get('target_entity')!r}")

            if ep.get("requires_auth") == expect_auth:
                _pass(f"  requires_auth={expect_auth} @ {method} {path}")
            else:
                _fail(f"  requires_auth={expect_auth} @ {method} {path}",
                      f"got {ep.get('requires_auth')!r}")


def _check_no_page_placeholders(api_graph, entities) -> None:
    entity_plurals = {_pluralize(e) for e in entities}
    for ep in api_graph.get("endpoints", []):
        path = ep.get("path", "")
        segment = path.removeprefix("/api/v1/").split("/")[0]
        if segment and "{" not in segment and segment not in entity_plurals:
            _fail(f"page-placeholder route {ep['method']} {path}",
                  f"segment '{segment}' not in entity set {sorted(entity_plurals)}")


def _check_endpoint_count(api_graph, entities) -> None:
    expected = len(entities) * 5
    actual = len(api_graph.get("endpoints", []))
    if actual == expected:
        _pass(f"endpoint count = {actual}  ({len(entities)} entities × 5)")
    else:
        _fail(f"endpoint count = {expected}", f"got {actual}")


def main() -> None:
    parser = argparse.ArgumentParser(description="M28 API graph alignment validation")
    parser.add_argument("--backend-url", default="http://127.0.0.1:8000", metavar="URL")
    parser.add_argument("--api-prefix", default="/api/v1", metavar="PATH")
    parser.add_argument("--username", default="developer")
    parser.add_argument("--password", default="devpassword")
    args = parser.parse_args()

    base = args.backend_url.rstrip("/")
    api = f"{base}{args.api_prefix}"
    workspace_root = Path(__file__).parent.parent / "workspace"

    print()
    print("M28 Validation -- Planned API Route Consumption and API Graph Alignment")
    print("=" * 72)
    print(f"  Backend : {base}")
    print()

    # ------------------------------------------------------------------
    # 1. Health
    # ------------------------------------------------------------------
    print("1. Backend Health")
    status, body = http("GET", f"{base}/health")
    if status is None:
        _fail("GET /health", str(body))
        print()
        print("  Backend unreachable. Start with:")
        print("    cd backend && python -m uvicorn main:app --port 8000")
        sys.exit(1)
    elif status == 200:
        _pass("GET /health")
    else:
        _fail("GET /health", f"HTTP {status}")

    # ------------------------------------------------------------------
    # 2. Auth
    # ------------------------------------------------------------------
    print("\n2. Authentication")
    form = urllib.parse.urlencode({"username": args.username, "password": args.password}).encode()
    status, body = http(
        "POST", f"{api}/auth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=form,
    )
    if status == 200 and isinstance(body, dict) and "access_token" in body:
        token: str = body["access_token"]
        _pass(f"POST /auth/token (user: {args.username})")
    else:
        _fail("POST /auth/token", f"HTTP {status}: {_detail(body)}")
        sys.exit(1)

    auth = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # ------------------------------------------------------------------
    # 3. Generate CRM project with entities
    # ------------------------------------------------------------------
    print(f"\n3. Entity CRUD Alignment  ({ALIGN_PROJECT_ID})")
    print(f'  Prompt: "{ALIGN_PROMPT}"')

    proposed_plan = _generate_via_propose(
        api, auth,
        ALIGN_PROJECT_ID, ALIGN_PROMPT,
        {"frontend": "nextjs", "backend": "fastapi", "database": "postgresql"},
        workspace_root,
    )
    entities = proposed_plan.get("entities", []) if proposed_plan else []

    # ------------------------------------------------------------------
    # 4. api_graph.json inspection — entity CRUD alignment
    # ------------------------------------------------------------------
    print(f"\n4. api_graph.json Inspection  ({ALIGN_PROJECT_ID})")
    api_graph = _load_api_graph(workspace_root, ALIGN_PROJECT_ID)
    if api_graph is None:
        _fail("api_graph.json loadable — skipping entity CRUD checks")
    elif not entities:
        _fail("entities list non-empty — cannot verify CRUD routes")
    else:
        print(f"  Entities: {entities}")
        _check_endpoint_count(api_graph, entities)
        _check_entity_crud(api_graph, entities)
        _check_no_page_placeholders(api_graph, entities)

    # ------------------------------------------------------------------
    # 5. Backward compat: simple spec → page-derived fallback
    # ------------------------------------------------------------------
    print(f"\n5. Backward Compat — Page-Derived Fallback  ({NO_ENTITIES_PROJECT_ID})")

    no_ent_ws = workspace_root / NO_ENTITIES_PROJECT_ID
    if no_ent_ws.exists():
        shutil.rmtree(no_ent_ws, ignore_errors=True)

    no_ent_spec = {
        "project_id": NO_ENTITIES_PROJECT_ID,
        "name": "Simple No Entities",
        "description": "Backward compat test: no entities, page-derived stubs only.",
        "pages": ["Home", "About"],
        "components": ["Navbar"],
    }
    status, body = http(
        "POST", f"{api}/genesis/generate",
        headers=auth, data=json.dumps(no_ent_spec).encode(), timeout=120,
    )
    if status == 200 and isinstance(body, dict) and body.get("success"):
        resp_data = body.get("data") or {}
        manifest = resp_data.get("manifest") or {}
        build_status = manifest.get("build_status", "?") if isinstance(manifest, dict) else "?"
        _pass(f"POST /genesis/generate ({NO_ENTITIES_PROJECT_ID})", f"build_status={build_status}")
    else:
        _fail(f"POST /genesis/generate ({NO_ENTITIES_PROJECT_ID})",
              f"HTTP {status}: {_detail(body)}")

    no_ent_graph = _load_api_graph(workspace_root, NO_ENTITIES_PROJECT_ID)
    if no_ent_graph is not None:
        endpoints = no_ent_graph.get("endpoints", [])
        # Expect GET+POST per page → 4 endpoints for ["Home", "About"]
        if endpoints:
            _pass(f"page-derived endpoints present", f"count={len(endpoints)}")
        else:
            _fail("page-derived endpoints present", "empty")

        with_target = [e for e in endpoints if e.get("target_entity")]
        if not with_target:
            _pass("no target_entity on page-derived endpoints")
        else:
            _fail("no target_entity on page-derived endpoints",
                  f"unexpected: {[e['path'] for e in with_target]}")

        item_routes = [e for e in endpoints if "{item_id}" in e.get("path", "")]
        if not item_routes:
            _pass("no {item_id} routes in page-derived fallback")
        else:
            _fail("no {item_id} routes in page-derived fallback",
                  f"found: {[e['path'] for e in item_routes]}")

        paths = {e["path"] for e in endpoints}
        for page in ["Home", "About"]:
            expected_path = f"/api/v1/{page.lower()}"
            if expected_path in paths:
                _pass(f"page-derived route present: {expected_path}")
            else:
                _fail(f"page-derived route present: {expected_path}",
                      f"actual paths: {sorted(paths)}")

    # ------------------------------------------------------------------
    # 6. API routes parse: api_routes set, no entities → parse path
    # ------------------------------------------------------------------
    print(f"\n6. API Routes Parse  ({ROUTES_PROJECT_ID})")

    routes_ws = workspace_root / ROUTES_PROJECT_ID
    if routes_ws.exists():
        shutil.rmtree(routes_ws, ignore_errors=True)

    routes_spec = {
        "project_id": ROUTES_PROJECT_ID,
        "name": "API Routes Parse Test",
        "description": "Test api_routes parse path: no entities, api_routes provided.",
        "pages": ["Items"],
        "components": ["Navbar"],
        "api_routes": [
            "GET /items",
            "POST /items",
            "GET /items/{id}",
            "PUT /items/{id}",
            "DELETE /items/{id}",
        ],
    }
    status, body = http(
        "POST", f"{api}/genesis/generate",
        headers=auth, data=json.dumps(routes_spec).encode(), timeout=120,
    )
    if status == 200 and isinstance(body, dict) and body.get("success"):
        resp_data = body.get("data") or {}
        manifest = resp_data.get("manifest") or {}
        build_status = manifest.get("build_status", "?") if isinstance(manifest, dict) else "?"
        _pass(f"POST /genesis/generate ({ROUTES_PROJECT_ID})", f"build_status={build_status}")
    else:
        _fail(f"POST /genesis/generate ({ROUTES_PROJECT_ID})",
              f"HTTP {status}: {_detail(body)}")

    routes_graph = _load_api_graph(workspace_root, ROUTES_PROJECT_ID)
    if routes_graph is not None:
        by_pm = {(e["path"], e["method"]): e for e in routes_graph.get("endpoints", [])}
        expected_parsed = [
            ("GET",    "/api/v1/items",           False),
            ("POST",   "/api/v1/items",           True),
            ("GET",    "/api/v1/items/{item_id}", False),
            ("PUT",    "/api/v1/items/{item_id}", True),
            ("DELETE", "/api/v1/items/{item_id}", True),
        ]
        for method, path, expect_auth in expected_parsed:
            if (path, method) in by_pm:
                ep = by_pm[(path, method)]
                _pass(f"parsed route {method} {path}")
                if ep.get("requires_auth") == expect_auth:
                    _pass(f"  requires_auth={expect_auth} @ {method} {path}")
                else:
                    _fail(f"  requires_auth={expect_auth} @ {method} {path}",
                          f"got {ep.get('requires_auth')!r}")
            else:
                _fail(f"parsed route {method} {path}", "MISSING from api_graph")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print()
    print("=" * 72)
    if _failures:
        print(f"RESULT: FAIL  ({len(_failures)} failure(s))")
        for f in _failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("RESULT: PASS  (all M28 checks passed)")
        sys.exit(0)


if __name__ == "__main__":
    main()
