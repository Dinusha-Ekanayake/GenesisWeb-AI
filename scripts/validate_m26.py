#!/usr/bin/env python3
"""
M26 Validation -- FastAPI Entity, Schema, and CRUD Generator
============================================================
Generates a CRM project with entities and verifies:
  - schemas.py, database.py, models.py, routers/__init__.py
  - Per-entity router files (customers.py, deals.py, etc.)
  - updated main.py with router includes + /health
  - All generated backend Python files pass py_compile

Updated in M29: storage.py replaced by database.py + models.py (SQLAlchemy).

Usage:
    python scripts/validate_m26.py
    python scripts/validate_m26.py --backend-url http://127.0.0.1:8000
"""

import argparse
import ast
import json
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

PROJECT_ID = "crm_crud_001"

CRM_PROMPT = (
    "Build a CRM system for a sales team with customers, deals, activities, "
    "users, teams, and notes management."
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


def py_compile_check(path: Path) -> bool:
    try:
        source = path.read_text(encoding="utf-8")
        ast.parse(source)
        return True
    except SyntaxError as e:
        print(f"      SyntaxError at line {e.lineno}: {e.msg}")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="M26 CRUD generator validation")
    parser.add_argument("--backend-url", default="http://127.0.0.1:8000", metavar="URL")
    parser.add_argument("--api-prefix", default="/api/v1", metavar="PATH")
    parser.add_argument("--username", default="developer")
    parser.add_argument("--password", default="devpassword")
    args = parser.parse_args()

    base = args.backend_url.rstrip("/")
    api = f"{base}{args.api_prefix}"
    workspace_root = Path(__file__).parent.parent / "workspace"
    project_ws = workspace_root / PROJECT_ID

    print()
    print("M26 Validation -- FastAPI Entity, Schema, and CRUD Generator")
    print("=" * 62)
    print(f"  Backend   : {base}")
    print(f"  Project   : {PROJECT_ID}")
    print(f"  Prompt    : {CRM_PROMPT[:70]}...")
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
        print("    uvicorn backend.app.main:app --reload --port 8000")
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
    # 3. Propose CRM plan
    # ------------------------------------------------------------------
    print("\n3. Planning Proposal (CRM with entities)")
    print(f'  Prompt: "{CRM_PROMPT[:80]}..."')

    if project_ws.exists():
        shutil.rmtree(project_ws, ignore_errors=True)
        print(f"  Cleaned prior workspace: {project_ws}")

    propose_payload = json.dumps({
        "prompt": CRM_PROMPT,
        "project_id": PROJECT_ID,
        "preferences": {"frontend": "nextjs", "backend": "fastapi", "database": "postgresql"},
    }).encode()

    status, body = http("POST", f"{api}/genesis/propose", headers=auth, data=propose_payload, timeout=60)
    proposed_plan = None
    if status == 200 and isinstance(body, dict) and body.get("success"):
        data = body.get("data") or {}
        proposed_plan = data.get("plan")
        method = (proposed_plan or {}).get("generation_method", "?")
        pages = len((proposed_plan or {}).get("pages", []))
        entities = (proposed_plan or {}).get("entities", [])
        _pass("POST /genesis/propose", f"method={method}  pages={pages}  entities={len(entities)}")
        if not entities:
            print("  WARNING: plan has no entities -- entity-path will NOT be exercised")
    else:
        _fail("POST /genesis/propose", f"HTTP {status}: {_detail(body)}")
        print("  Cannot continue. Aborting.")
        sys.exit(1)

    if proposed_plan is None:
        _fail("proposed_plan extracted from response")
        sys.exit(1)

    # ------------------------------------------------------------------
    # 4. Approve and generate
    # ------------------------------------------------------------------
    print(f"\n4. Approve-and-Generate (project: {PROJECT_ID})")
    print("  This may take 30-120 seconds...")

    gen_payload = json.dumps({
        "plan": proposed_plan,
        "approval": {
            "approved": True,
            "approved_by": "m26_validation",
            "notes": "M26 automated validation.",
        },
    }).encode()

    status, body = http("POST", f"{api}/genesis/approve-and-generate", headers=auth, data=gen_payload, timeout=180)
    if status == 200 and isinstance(body, dict) and body.get("success"):
        data = body.get("data") or {}
        manifest = data.get("manifest") or {}
        build_status = manifest.get("build_status", "?") if isinstance(manifest, dict) else "?"
        _pass("POST /genesis/approve-and-generate", f"build_status={build_status}")
        if build_status != "SUCCESS":
            _fail("build_status == SUCCESS", f"got {build_status}")
    else:
        _fail("POST /genesis/approve-and-generate", f"HTTP {status}: {_detail(body)}")
        print("  Cannot verify file tree. Aborting.")
        sys.exit(1)

    # ------------------------------------------------------------------
    # 5. File tree verification
    # ------------------------------------------------------------------
    print(f"\n5. File Tree Verification  ({project_ws / 'backend'})")

    backend_app = project_ws / "backend" / "app"

    required_files = [
        ("backend/requirements.txt",       project_ws / "backend" / "requirements.txt"),
        ("backend/app/__init__.py",         backend_app / "__init__.py"),
        ("backend/app/database.py",         backend_app / "database.py"),
        ("backend/app/models.py",           backend_app / "models.py"),
        ("backend/app/schemas.py",          backend_app / "schemas.py"),
        ("backend/app/main.py",             backend_app / "main.py"),
        ("backend/app/routers/__init__.py", backend_app / "routers" / "__init__.py"),
    ]

    for label, path in required_files:
        if path.exists():
            _pass(f"{label} exists")
        else:
            _fail(f"{label} exists", "MISSING")

    # Check per-entity router files
    routers_dir = backend_app / "routers"
    router_files = list(routers_dir.glob("*.py")) if routers_dir.exists() else []
    entity_routers = [f for f in router_files if f.name != "__init__.py"]
    if entity_routers:
        names = ", ".join(sorted(f.name for f in entity_routers))
        _pass(f"entity router files exist", f"{len(entity_routers)} file(s): {names}")
    else:
        _fail("entity router files exist", "no per-entity router .py files found in routers/")

    # Check main.py references include_router
    main_path = backend_app / "main.py"
    if main_path.exists():
        main_content = main_path.read_text(encoding="utf-8")
        if "include_router" in main_content:
            _pass("main.py contains include_router calls")
        else:
            _fail("main.py contains include_router calls", "include_router not found")
        if 'prefix="/api/v1"' in main_content:
            _pass('main.py include_router calls use prefix="/api/v1"')
        else:
            _fail('main.py include_router calls use prefix="/api/v1"', 'prefix="/api/v1" not found')
        if '"/health"' in main_content or "'/health'" in main_content:
            _pass("main.py contains /health endpoint")
        else:
            _fail("main.py contains /health endpoint")

    # ------------------------------------------------------------------
    # 6. py_compile all generated backend Python files
    # ------------------------------------------------------------------
    print(f"\n6. py_compile — All Generated Backend Python Files")

    py_files = list((project_ws / "backend").rglob("*.py")) if (project_ws / "backend").exists() else []
    if not py_files:
        _fail("backend Python files found", "no .py files under backend/")
    else:
        for py_file in sorted(py_files):
            rel = py_file.relative_to(project_ws)
            if py_compile_check(py_file):
                _pass(f"py_compile {rel}")
            else:
                _fail(f"py_compile {rel}")

    # ------------------------------------------------------------------
    # 7. Content spot checks
    # ------------------------------------------------------------------
    print(f"\n7. Content Spot Checks")

    schemas_path = backend_app / "schemas.py"
    if schemas_path.exists():
        schemas_content = schemas_path.read_text(encoding="utf-8")
        if "BaseModel" in schemas_content:
            _pass("schemas.py imports BaseModel")
        else:
            _fail("schemas.py imports BaseModel")
        class_count = schemas_content.count("class ")
        _pass(f"schemas.py class count", f"{class_count} class definition(s)")

    # M29: storage.py replaced by database.py + models.py (SQLAlchemy persistence)
    database_path = backend_app / "database.py"
    if database_path.exists():
        db_content = database_path.read_text(encoding="utf-8")
        if "get_db" in db_content and "engine" in db_content and "Base" in db_content:
            _pass("database.py has get_db, engine, Base")
        else:
            _fail("database.py has get_db, engine, Base")
        if "sqlalchemy" in db_content:
            _pass("database.py imports sqlalchemy")
        else:
            _fail("database.py imports sqlalchemy")

    models_path = backend_app / "models.py"
    if models_path.exists():
        models_content = models_path.read_text(encoding="utf-8")
        if "Column" in models_content and "Base" in models_content:
            _pass("models.py has Column and Base")
        else:
            _fail("models.py has Column and Base")

    req_path = project_ws / "backend" / "requirements.txt"
    if req_path.exists():
        req_content = req_path.read_text(encoding="utf-8")
        if "sqlalchemy" in req_content.lower():
            _pass("requirements.txt includes sqlalchemy")
        else:
            _fail("requirements.txt includes sqlalchemy")

    if entity_routers:
        sample = entity_routers[0]
        router_content = sample.read_text(encoding="utf-8")
        if "APIRouter" in router_content:
            _pass(f"{sample.name} uses APIRouter")
        else:
            _fail(f"{sample.name} uses APIRouter")
        for method in ["get", "post", "put", "delete"]:
            if f"@router.{method}" in router_content:
                _pass(f"{sample.name} has @router.{method}")
            else:
                _fail(f"{sample.name} has @router.{method}")

    # ------------------------------------------------------------------
    # 8. Frontend build check (optional — verify npm artifacts exist)
    # ------------------------------------------------------------------
    print(f"\n8. Frontend Artifact Check")
    frontend_dir = project_ws / "frontend"
    pkg_json = frontend_dir / "package.json"
    if pkg_json.exists():
        _pass("frontend/package.json exists")
    else:
        _fail("frontend/package.json exists", "MISSING")

    tsx_files = list(frontend_dir.rglob("*.tsx")) if frontend_dir.exists() else []
    if tsx_files:
        _pass(f"frontend .tsx files", f"{len(tsx_files)} file(s)")
    else:
        _fail("frontend .tsx files", "none found")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print()
    print("=" * 62)
    if _failures:
        print(f"RESULT: FAIL  ({len(_failures)} failure(s))")
        for f in _failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("RESULT: PASS  (all M26 checks passed)")
        sys.exit(0)


if __name__ == "__main__":
    main()
