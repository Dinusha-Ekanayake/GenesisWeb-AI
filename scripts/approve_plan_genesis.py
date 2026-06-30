#!/usr/bin/env python3
"""
Genesis Engine -- Approval-Gated Generate Smoke Test (M23)
==========================================================
Tests the full planning-first generation loop:
  1. POST /genesis/propose  (get a plan)
  2. POST /genesis/approve-and-generate  (approved path)
  3. POST /genesis/approve-and-generate  (rejected: not approved)
  4. POST /genesis/approve-and-generate  (rejected: unsupported stack)

Uses only Python stdlib -- no external dependencies required.

Usage:
    python scripts/approve_plan_genesis.py
    python scripts/approve_plan_genesis.py --backend-url http://127.0.0.1:8000
    python scripts/approve_plan_genesis.py --skip-generate   # propose only, skip generation

Exit codes:
    0  all checks passed
    1  one or more checks failed
"""

import argparse
import json
import sys
import shutil
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request

# Test project IDs
PROJECT_ID_POSITIVE  = "approved_plan_001"
PROJECT_ID_REJECT    = "approved_plan_reject_001"
PROJECT_ID_BADSTACK  = "approved_plan_stack_001"

EXAMPLE_PROMPT = (
    "Create a photography portfolio website with gallery, albums, "
    "services, testimonials, and contact form."
)

_failures: list = []


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


def http(method, url, *, headers=None, data=None, timeout=120):
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
        return str(body.get("detail") or body)[:300]
    return str(body)[:300]


def workspace_exists(workspace_root: Path, project_id: str) -> bool:
    return (workspace_root / project_id).exists()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Genesis Engine approval-gated generate smoke test (M23)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--backend-url", default="http://127.0.0.1:8000", metavar="URL")
    parser.add_argument("--api-prefix", default="/api/v1", metavar="PATH")
    parser.add_argument("--username", default="developer")
    parser.add_argument("--password", default="devpassword")
    parser.add_argument(
        "--skip-generate",
        action="store_true",
        help="Run propose only; skip approve-and-generate (no workspace mutations).",
    )
    args = parser.parse_args()

    base = args.backend_url.rstrip("/")
    api = f"{base}{args.api_prefix}"
    workspace_root = Path(__file__).parent.parent / "workspace"

    print()
    print("Genesis Engine -- Approval-Gated Generate Smoke Test (M23)")
    print("=" * 62)
    print(f"  Backend : {base}")
    print(f"  Mode    : {'propose-only' if args.skip_generate else 'full (propose + approve-and-generate)'}")
    print()

    # ------------------------------------------------------------------
    # 1. Health
    # ------------------------------------------------------------------
    print("1. Backend Health")
    status, body = http("GET", f"{base}/health")
    if status is None:
        _fail("GET /health", str(body))
        print()
        print("  Backend is unreachable. Start it:")
        print("    cd backend && uvicorn main:app --reload --port 8000")
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
    # 3. Propose
    # ------------------------------------------------------------------
    print("\n3. Planning Proposal")
    print(f'  Prompt: "{EXAMPLE_PROMPT[:80]}..."')

    propose_payload = json.dumps({
        "prompt": EXAMPLE_PROMPT,
        "project_id": PROJECT_ID_POSITIVE,
        "preferences": {"frontend": "nextjs", "backend": "fastapi", "database": "postgresql"},
    }).encode()

    status, body = http("POST", f"{api}/genesis/propose", headers=auth, data=propose_payload, timeout=60)

    proposed_plan = None
    if status == 200 and isinstance(body, dict) and body.get("success"):
        data = body.get("data") or {}
        proposed_plan = data.get("plan")
        requires_approval = data.get("requires_approval_before_generation", False)
        method = (proposed_plan or {}).get("generation_method", "?")
        pages = len((proposed_plan or {}).get("pages", []))
        _pass("POST /genesis/propose", f"method={method} pages={pages} requires_approval={requires_approval}")
        if not requires_approval:
            _fail("propose: requires_approval_before_generation flag", "expected True")
    else:
        _fail("POST /genesis/propose", f"HTTP {status}: {_detail(body)}")

    if args.skip_generate:
        _skip("approve-and-generate tests", "--skip-generate passed")
        print()
        print("=" * 62)
        if _failures:
            print(f"RESULT: FAIL  ({len(_failures)} failure(s): {', '.join(_failures)})")
            sys.exit(1)
        print("RESULT: PASS")
        sys.exit(0)

    if proposed_plan is None:
        print("  Cannot continue without a proposed plan. Aborting.")
        sys.exit(1)

    # ------------------------------------------------------------------
    # 4. Positive path: approve and generate
    # ------------------------------------------------------------------
    print(f"\n4. Positive Path — approve-and-generate (project: {PROJECT_ID_POSITIVE})")

    # Clean any prior run
    prior = workspace_root / PROJECT_ID_POSITIVE
    if prior.exists():
        shutil.rmtree(prior, ignore_errors=True)
        print(f"  Cleared prior workspace: {prior}")

    approved_payload = json.dumps({
        "plan": proposed_plan,
        "approval": {
            "approved": True,
            "approved_by": "smoke_test",
            "notes": "M23 automated smoke test approval.",
        },
    }).encode()

    print("  Generating (may take 30-120s)...")
    status, body = http(
        "POST", f"{api}/genesis/approve-and-generate",
        headers=auth, data=approved_payload, timeout=180,
    )

    if status == 200 and isinstance(body, dict) and body.get("success"):
        data = body.get("data") or {}
        ret_pid = data.get("project_id", "?")
        manifest = data.get("manifest") or {}
        summary = data.get("approved_plan_summary") or {}
        build_status = manifest.get("build_status", "?") if isinstance(manifest, dict) else "?"
        _pass(
            "POST /genesis/approve-and-generate",
            f"project_id={ret_pid} build_status={build_status}",
        )
        print(f"    Approved plan summary:")
        print(f"      name    : {summary.get('name', '?')}")
        print(f"      app_type: {summary.get('app_type', '?')}")
        print(f"      pages   : {summary.get('pages', [])}")
        print(f"      stack   : {summary.get('technology_stack', {})}")
        print(f"      approval: {summary.get('approval_status', '?')}")
    else:
        _fail("POST /genesis/approve-and-generate", f"HTTP {status}: {_detail(body)}")

    # Verify workspace structure
    print(f"\n  Workspace verification ({PROJECT_ID_POSITIVE}):")
    ws = workspace_root / PROJECT_ID_POSITIVE

    spec_path = ws / "spec.json"
    if spec_path.exists():
        _pass(f"workspace/{PROJECT_ID_POSITIVE}/spec.json exists")
    else:
        _fail(f"workspace/{PROJECT_ID_POSITIVE}/spec.json", "missing")

    approved_plan_path = ws / "artifacts" / "approved_plan.json"
    if approved_plan_path.exists():
        try:
            with open(approved_plan_path, encoding="utf-8") as f:
                ap = json.load(f)
            approval_status = ap.get("approval_status", "?")
            approved_by = ap.get("approved_by", "?")
            _pass(
                f"workspace/{PROJECT_ID_POSITIVE}/artifacts/approved_plan.json",
                f"approval_status={approval_status} approved_by={approved_by}",
            )
        except Exception as e:
            _fail(f"workspace/{PROJECT_ID_POSITIVE}/artifacts/approved_plan.json", f"read error: {e}")
    else:
        _fail(f"workspace/{PROJECT_ID_POSITIVE}/artifacts/approved_plan.json", "missing")

    for artifact in ("planning_report.json", "deployment_manifest.json", "architecture_graphs.json"):
        path = ws / "artifacts" / artifact
        if path.exists():
            _pass(f"workspace/{PROJECT_ID_POSITIVE}/artifacts/{artifact}")
        else:
            _fail(f"workspace/{PROJECT_ID_POSITIVE}/artifacts/{artifact}", "missing")

    # Verify pages vs components separation
    print(f"\n  File tree verification:")
    frontend_app = ws / "frontend" / "app"
    frontend_components = ws / "frontend" / "components"

    if frontend_app.exists():
        page_files = [p.name for p in frontend_app.rglob("page.tsx")]
        _pass(f"frontend/app/ — {len(page_files)} page file(s): {page_files}")
    else:
        _fail("frontend/app/", "directory missing")

    if frontend_components.exists():
        comp_files = [p.name for p in frontend_components.glob("*.tsx")]
        _pass(f"frontend/components/ — {len(comp_files)} component file(s): {comp_files}")
    else:
        # components/ may be absent if spec has no components — not a failure
        comp_count = len(proposed_plan.get("components", []))
        if comp_count > 0:
            _fail("frontend/components/", f"directory missing but {comp_count} components expected")
        else:
            _skip("frontend/components/", "no components in spec")

    # ------------------------------------------------------------------
    # 5. Negative path: not approved
    # ------------------------------------------------------------------
    print(f"\n5. Negative Path — rejected (not approved)")

    reject_payload = json.dumps({
        "plan": proposed_plan,
        "approval": {
            "approved": False,
            "notes": "Not yet reviewed.",
        },
    }).encode()

    # Confirm no workspace exists before the call
    reject_ws_before = workspace_exists(workspace_root, PROJECT_ID_REJECT)

    # Temporarily override project_id in plan to avoid touching positive project
    reject_plan = dict(proposed_plan)
    reject_plan["project_id"] = PROJECT_ID_REJECT
    reject_payload = json.dumps({
        "plan": reject_plan,
        "approval": {"approved": False},
    }).encode()

    status, body = http(
        "POST", f"{api}/genesis/approve-and-generate",
        headers=auth, data=reject_payload, timeout=30,
    )

    if status == 400:
        detail = _detail(body)
        _pass("rejection returns HTTP 400", detail[:80])
    else:
        _fail("rejection should return HTTP 400", f"got HTTP {status}: {_detail(body)}")

    if workspace_exists(workspace_root, PROJECT_ID_REJECT):
        _fail(f"no workspace created for rejected project", f"workspace/{PROJECT_ID_REJECT} was created")
    else:
        _pass(f"no workspace created for rejected project")

    # ------------------------------------------------------------------
    # 6. Unsupported stack path
    # ------------------------------------------------------------------
    print(f"\n6. Negative Path — unsupported stack (frontend=vite, backend=express)")

    bad_stack_plan = dict(proposed_plan)
    bad_stack_plan["project_id"] = PROJECT_ID_BADSTACK
    bad_stack_plan["technology_stack"] = {
        "frontend": {
            "framework": "vite",
            "language": "typescript",
            "router": "react_router",
            "styling": "css_modules",
            "component_library": None,
        },
        "backend": {
            "framework": "express",
            "language": "typescript",
            "api_style": "rest",
            "orm": None,
        },
        "database": {"engine": "postgresql", "hosting": "docker_local_or_managed"},
        "ai": {"enabled": False, "framework": None, "orchestration": None, "model_provider": None, "vector_store": None},
        "auth": {"provider": "custom_jwt", "strategy": "email_password"},
        "deployment": {"containerization": "docker", "frontend_host": "vercel", "backend_host": "render_or_aws", "database_host": "managed_postgresql"},
        "testing": {"frontend": "vitest", "backend": "jest", "e2e": "playwright"},
    }

    bad_stack_payload = json.dumps({
        "plan": bad_stack_plan,
        "approval": {"approved": True, "approved_by": "smoke_test"},
    }).encode()

    status, body = http(
        "POST", f"{api}/genesis/approve-and-generate",
        headers=auth, data=bad_stack_payload, timeout=30,
    )

    if status == 422:
        detail = _detail(body)
        _pass("unsupported stack returns HTTP 422", detail[:100])
    else:
        _fail("unsupported stack should return HTTP 422", f"got HTTP {status}: {_detail(body)}")

    if workspace_exists(workspace_root, PROJECT_ID_BADSTACK):
        _fail(f"no workspace created for bad-stack project", f"workspace/{PROJECT_ID_BADSTACK} was created")
    else:
        _pass(f"no workspace created for bad-stack project")

    # ------------------------------------------------------------------
    # 7. Verify existing /genesis/generate still works
    # ------------------------------------------------------------------
    print(f"\n7. Existing /genesis/generate still works")

    smoke_spec = {
        "project_id": "m23_compat_check",
        "name": "M23 Compat Check",
        "description": "Verify existing generate endpoint unaffected.",
        "pages": ["Home", "About"],
        "components": ["Navbar"],
    }

    prior_compat = workspace_root / "m23_compat_check"
    if prior_compat.exists():
        shutil.rmtree(prior_compat, ignore_errors=True)

    status, body = http(
        "POST", f"{api}/genesis/generate",
        headers=auth,
        data=json.dumps(smoke_spec).encode(),
        timeout=120,
    )
    if status == 200 and isinstance(body, dict) and body.get("success"):
        manifest = (body.get("data") or {}).get("manifest") or {}
        build_status = manifest.get("build_status", "?") if isinstance(manifest, dict) else "?"
        _pass("POST /genesis/generate (existing endpoint)", f"build_status={build_status}")
    else:
        _fail("POST /genesis/generate (existing endpoint)", f"HTTP {status}: {_detail(body)}")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print()
    print("=" * 62)
    if _failures:
        print(f"RESULT: FAIL  ({len(_failures)} failure(s): {', '.join(_failures)})")
        sys.exit(1)
    else:
        print("RESULT: PASS  (all checks passed)")
        sys.exit(0)


if __name__ == "__main__":
    main()
