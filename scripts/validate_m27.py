#!/usr/bin/env python3
"""
M27 Validation -- Entity Field Inference and Rich Schema Generator
==================================================================
Verifies that Genesis generates field-aware Pydantic schemas from inferred
entity field definitions, rather than the M26 name-only placeholder.

Checks:
  - Rich CRM project (rich_fields_crm_001): CustomerBase has name/email/phone/company/status
  - DealBase has title/value/stage/customer_id
  - ActivityBase has title/type/due_date/completed
  - UserBase has name/email/role
  - TeamBase has name/description
  - NoteBase has title/content
  - All generated Python files pass py_compile
  - Old entity-name-only format (old_entity_format_001) still generates and compiles
  - No-entities backward compat (simple_no_entities_001) still works

Usage:
    python scripts/validate_m27.py
    python scripts/validate_m27.py --backend-url http://127.0.0.1:8000
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

RICH_CRM_PROJECT_ID = "rich_fields_crm_001"
OLD_FORMAT_PROJECT_ID = "old_entity_format_001"
NO_ENTITIES_PROJECT_ID = "simple_no_entities_001"

RICH_CRM_PROMPT = (
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


def py_compile_check(path: Path) -> bool:
    try:
        source = path.read_text(encoding="utf-8")
        ast.parse(source)
        return True
    except SyntaxError as e:
        print(f"      SyntaxError at line {e.lineno}: {e.msg}")
        return False


def _schemas_check(schemas_path: Path, entity_name: str, expected_fields: list) -> None:
    """Verify that {entity_name}Base class contains all expected_fields in schemas.py."""
    content = schemas_path.read_text(encoding="utf-8")
    class_marker = f"class {entity_name}Base"
    if class_marker not in content:
        _fail(f"{entity_name}Base class exists in schemas.py")
        return
    _pass(f"{entity_name}Base class exists in schemas.py")

    # Extract the class body (lines after class header until next class or EOF)
    lines = content.splitlines()
    in_class = False
    class_lines = []
    for line in lines:
        if line.startswith(class_marker):
            in_class = True
            continue
        if in_class:
            if line.startswith("class ") and not line.startswith("    "):
                break
            class_lines.append(line)

    class_body = "\n".join(class_lines)
    for field in expected_fields:
        if field in class_body:
            _pass(f"{entity_name}Base.{field} present")
        else:
            _fail(f"{entity_name}Base.{field} present", f"not found in class body")


def _generate_project(api, auth, project_id, prompt, preferences, workspace_root) -> dict:
    """Propose and approve-and-generate a project. Returns proposed_plan or None on failure."""
    ws = workspace_root / project_id
    if ws.exists():
        shutil.rmtree(ws, ignore_errors=True)
        print(f"  Cleaned prior workspace: {ws}")

    propose_payload = json.dumps({
        "prompt": prompt,
        "project_id": project_id,
        "preferences": preferences,
    }).encode()

    status, body = http("POST", f"{api}/genesis/propose", headers=auth, data=propose_payload, timeout=60)
    if status != 200 or not (isinstance(body, dict) and body.get("success")):
        _fail(f"POST /genesis/propose ({project_id})", f"HTTP {status}: {_detail(body)}")
        return None

    data = body.get("data") or {}
    proposed_plan = data.get("plan")
    if not proposed_plan:
        _fail(f"proposed_plan extracted ({project_id})")
        return None

    method = proposed_plan.get("generation_method", "?")
    entities = proposed_plan.get("entities", [])
    _pass(f"POST /genesis/propose ({project_id})", f"method={method}  entities={len(entities)}: {entities[:6]}")

    gen_payload = json.dumps({
        "plan": proposed_plan,
        "approval": {
            "approved": True,
            "approved_by": "m27_validation",
            "notes": "M27 automated validation.",
        },
    }).encode()

    print(f"  Generating (may take 30-120s)...")
    status, body = http("POST", f"{api}/genesis/approve-and-generate", headers=auth, data=gen_payload, timeout=180)
    if status == 200 and isinstance(body, dict) and body.get("success"):
        resp_data = body.get("data") or {}
        manifest = resp_data.get("manifest") or {}
        build_status = manifest.get("build_status", "?") if isinstance(manifest, dict) else "?"
        _pass(f"POST /genesis/approve-and-generate ({project_id})", f"build_status={build_status}")
        if build_status != "SUCCESS":
            _fail(f"build_status==SUCCESS ({project_id})", f"got {build_status}")
    else:
        _fail(f"POST /genesis/approve-and-generate ({project_id})", f"HTTP {status}: {_detail(body)}")
        return None

    return proposed_plan


def main() -> None:
    parser = argparse.ArgumentParser(description="M27 rich schema generator validation")
    parser.add_argument("--backend-url", default="http://127.0.0.1:8000", metavar="URL")
    parser.add_argument("--api-prefix", default="/api/v1", metavar="PATH")
    parser.add_argument("--username", default="developer")
    parser.add_argument("--password", default="devpassword")
    args = parser.parse_args()

    base = args.backend_url.rstrip("/")
    api = f"{base}{args.api_prefix}"
    workspace_root = Path(__file__).parent.parent / "workspace"

    print()
    print("M27 Validation -- Entity Field Inference and Rich Schema Generator")
    print("=" * 68)
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
    # 3. Generate rich CRM project
    # ------------------------------------------------------------------
    print(f"\n3. Rich CRM Generation ({RICH_CRM_PROJECT_ID})")
    print(f'  Prompt: "{RICH_CRM_PROMPT[:80]}..."')

    _generate_project(
        api, auth,
        RICH_CRM_PROJECT_ID, RICH_CRM_PROMPT,
        {"frontend": "nextjs", "backend": "fastapi", "database": "postgresql"},
        workspace_root,
    )

    # ------------------------------------------------------------------
    # 4. File tree verification
    # ------------------------------------------------------------------
    print(f"\n4. File Tree Verification  ({RICH_CRM_PROJECT_ID})")
    project_ws = workspace_root / RICH_CRM_PROJECT_ID
    backend_app = project_ws / "backend" / "app"

    required_files = [
        ("backend/app/schemas.py",   backend_app / "schemas.py"),
        ("backend/app/storage.py",   backend_app / "storage.py"),
        ("backend/app/main.py",      backend_app / "main.py"),
        ("backend/app/routers/__init__.py", backend_app / "routers" / "__init__.py"),
    ]
    for label, path in required_files:
        if path.exists():
            _pass(f"{label} exists")
        else:
            _fail(f"{label} exists", "MISSING")

    routers_dir = backend_app / "routers"
    entity_routers = [f for f in routers_dir.glob("*.py") if f.name != "__init__.py"] \
        if routers_dir.exists() else []
    if entity_routers:
        names = ", ".join(sorted(f.name for f in entity_routers))
        _pass("entity router files", f"{len(entity_routers)}: {names}")
    else:
        _fail("entity router files", "none found")

    # ------------------------------------------------------------------
    # 5. py_compile all generated backend Python files
    # ------------------------------------------------------------------
    print(f"\n5. py_compile — Generated Backend")
    py_files = sorted((project_ws / "backend").rglob("*.py")) \
        if (project_ws / "backend").exists() else []
    if not py_files:
        _fail("backend Python files found", "none")
    else:
        for py_file in py_files:
            rel = py_file.relative_to(project_ws)
            if py_compile_check(py_file):
                _pass(f"py_compile {rel}")
            else:
                _fail(f"py_compile {rel}")

    # ------------------------------------------------------------------
    # 6. Schema content checks
    # ------------------------------------------------------------------
    print(f"\n6. Schema Content Checks")
    schemas_path = backend_app / "schemas.py"
    if not schemas_path.exists():
        _fail("schemas.py exists for content checks")
    else:
        _schemas_check(schemas_path, "Customer", ["name", "email", "phone", "company", "status"])
        _schemas_check(schemas_path, "Deal",     ["title", "value", "stage", "customer_id"])
        _schemas_check(schemas_path, "Activity", ["title", "type", "due_date", "completed"])
        _schemas_check(schemas_path, "User",     ["name", "email", "role"])
        _schemas_check(schemas_path, "Team",     ["name", "description"])
        _schemas_check(schemas_path, "Note",     ["title", "content"])

        # Verify Optional import is present (needed for optional fields)
        content = schemas_path.read_text(encoding="utf-8")
        if "Optional" in content:
            _pass("schemas.py imports Optional")
        else:
            _fail("schemas.py imports Optional")

        # Verify response model is flat (Customer(BaseModel), not Customer(CustomerBase))
        if "class Customer(BaseModel):" in content:
            _pass("Customer response model is flat (Pydantic v2 safe)")
        else:
            _fail("Customer response model is flat", "Customer(BaseModel) not found")

        # Verify id field in response model
        if "    id: int" in content:
            _pass("Response model has id: int field")
        else:
            _fail("Response model has id: int field")

    # ------------------------------------------------------------------
    # 7. Old entity-name-only format (backward compat with direct /generate)
    # ------------------------------------------------------------------
    print(f"\n7. Old Entity-Name-Only Format ({OLD_FORMAT_PROJECT_ID})")

    old_ws = workspace_root / OLD_FORMAT_PROJECT_ID
    if old_ws.exists():
        shutil.rmtree(old_ws, ignore_errors=True)

    old_spec = {
        "project_id": OLD_FORMAT_PROJECT_ID,
        "name": "Old Entity Format",
        "description": "Test old entity list support — entities as strings only.",
        "pages": ["Customers"],
        "components": ["Navbar"],
        "entities": ["Customer"],
    }
    status, body = http(
        "POST", f"{api}/genesis/generate",
        headers=auth, data=json.dumps(old_spec).encode(), timeout=120,
    )
    if status == 200 and isinstance(body, dict) and body.get("success"):
        resp_data = body.get("data") or {}
        manifest = resp_data.get("manifest") or {}
        build_status = manifest.get("build_status", "?") if isinstance(manifest, dict) else "?"
        _pass("POST /genesis/generate (old format)", f"build_status={build_status}")
    else:
        _fail("POST /genesis/generate (old format)", f"HTTP {status}: {_detail(body)}")

    old_schemas = workspace_root / OLD_FORMAT_PROJECT_ID / "backend" / "app" / "schemas.py"
    if old_schemas.exists():
        if py_compile_check(old_schemas):
            _pass("old_entity_format_001 schemas.py py_compile")
        else:
            _fail("old_entity_format_001 schemas.py py_compile")

        content = old_schemas.read_text(encoding="utf-8")
        if "class CustomerBase(BaseModel):" in content:
            _pass("old_entity_format_001: CustomerBase generated via inference")
        else:
            _fail("old_entity_format_001: CustomerBase generated via inference")

        # Default inference gives name + description fields
        if "name" in content:
            _pass("old_entity_format_001: name field inferred")
        else:
            _fail("old_entity_format_001: name field inferred")
    else:
        _fail("old_entity_format_001 schemas.py exists", "MISSING")

    # ------------------------------------------------------------------
    # 8. No-entities backward compat (simple spec)
    # ------------------------------------------------------------------
    print(f"\n8. No-Entities Backward Compat ({NO_ENTITIES_PROJECT_ID})")

    no_ent_ws = workspace_root / NO_ENTITIES_PROJECT_ID
    if no_ent_ws.exists():
        shutil.rmtree(no_ent_ws, ignore_errors=True)

    no_ent_spec = {
        "project_id": NO_ENTITIES_PROJECT_ID,
        "name": "Simple No Entities",
        "description": "Backward compat: no entities, page-derived stubs only.",
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
        _pass("POST /genesis/generate (no entities)", f"build_status={build_status}")
    else:
        _fail("POST /genesis/generate (no entities)", f"HTTP {status}: {_detail(body)}")

    no_ent_main = workspace_root / NO_ENTITIES_PROJECT_ID / "backend" / "app" / "main.py"
    if no_ent_main.exists():
        if py_compile_check(no_ent_main):
            _pass("simple_no_entities_001 backend/app/main.py py_compile")
        else:
            _fail("simple_no_entities_001 backend/app/main.py py_compile")
    else:
        _fail("simple_no_entities_001 backend/app/main.py exists", "MISSING")

    no_ent_routers = workspace_root / NO_ENTITIES_PROJECT_ID / "backend" / "app" / "routers"
    if not no_ent_routers.exists():
        _pass("simple_no_entities_001: no routers/ directory (correct)")
    else:
        _fail("simple_no_entities_001: routers/ should not exist for no-entity spec")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print()
    print("=" * 68)
    if _failures:
        print(f"RESULT: FAIL  ({len(_failures)} failure(s))")
        for f in _failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("RESULT: PASS  (all M27 checks passed)")
        sys.exit(0)


if __name__ == "__main__":
    main()
