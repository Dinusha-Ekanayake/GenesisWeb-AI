#!/usr/bin/env python3
"""
M32 Validation -- Multi-Field Entity Forms
==========================================
Validates that NextJsPlugin generates entity pages with per-field form inputs
covering all non-id entity fields, using typed form state instead of a
single-field string.

Sections:
  1.  Genesis backend health
  2.  Authentication
  3.  Generate multi_field_crud_001 via propose+approve-and-generate
  4.  File tree: lib/api.ts, lib/types.ts, .env.example, entity pages
  5.  Content: api.ts exports (unchanged from M30)
  6.  Content: types.ts interfaces (unchanged from M30)
  7.  Content: entity page multi-field form checks
  8.  Frontend npm install
  9.  Frontend npm run build
  10. Generated backend py_compile
  11. Backward compat: simple_no_entities_001

Usage:
    python scripts/validate_m32.py
    python scripts/validate_m32.py --backend-url http://127.0.0.1:8000
"""

import argparse
import ast
import json
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

MULTI_FIELD_PROJECT_ID = "multi_field_crud_001"
NO_ENTITIES_PROJECT_ID = "simple_no_entities_001"

CRM_PROMPT = (
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


def _find_npm() -> str:
    for candidate in ("npm.cmd", "npm"):
        found = shutil.which(candidate)
        if found:
            return found
    return "npm"


def _run_npm(args: list, cwd: Path, timeout: int = 360) -> tuple:
    npm = _find_npm()
    try:
        result = subprocess.run(
            [npm] + args,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"timeout after {timeout}s"
    except FileNotFoundError as exc:
        return -2, "", str(exc)


def _generate_project(api, auth, project_id, prompt, workspace_root):
    ws = workspace_root / project_id
    if ws.exists():
        shutil.rmtree(ws, ignore_errors=True)
        print(f"  Cleaned prior workspace: {ws}")

    propose_payload = json.dumps({
        "prompt": prompt,
        "project_id": project_id,
        "preferences": {"frontend": "nextjs", "backend": "fastapi", "database": "postgresql"},
    }).encode()

    status, body = http("POST", f"{api}/genesis/propose", headers=auth,
                        data=propose_payload, timeout=60)
    if status != 200 or not (isinstance(body, dict) and body.get("success")):
        _fail(f"POST /genesis/propose ({project_id})", f"HTTP {status}: {_detail(body)}")
        return None

    data = body.get("data") or {}
    proposed_plan = data.get("plan")
    entities = (proposed_plan or {}).get("entities", [])
    method = (proposed_plan or {}).get("generation_method", "?")
    _pass(f"POST /genesis/propose ({project_id})", f"method={method}  entities={len(entities)}: {entities[:6]}")

    if not entities:
        print("  WARNING: plan has no entities — entity frontend path will NOT be exercised")

    gen_payload = json.dumps({
        "plan": proposed_plan,
        "approval": {
            "approved": True,
            "approved_by": "m32_validation",
            "notes": "M32 automated validation.",
        },
    }).encode()

    print("  Generating (may take 30-120s)...")
    status, body = http("POST", f"{api}/genesis/approve-and-generate", headers=auth,
                        data=gen_payload, timeout=180)
    if status == 200 and isinstance(body, dict) and body.get("success"):
        resp_data = body.get("data") or {}
        manifest = resp_data.get("manifest") or {}
        build_status = manifest.get("build_status", "?") if isinstance(manifest, dict) else "?"
        _pass(f"POST /genesis/approve-and-generate ({project_id})", f"build_status={build_status}")
        if build_status != "SUCCESS":
            _fail(f"build_status==SUCCESS ({project_id})", f"got {build_status}")
            return None
    else:
        _fail(f"POST /genesis/approve-and-generate ({project_id})", f"HTTP {status}: {_detail(body)}")
        return None

    return proposed_plan


def main() -> None:
    parser = argparse.ArgumentParser(description="M32 multi-field form validation")
    parser.add_argument("--backend-url", default="http://127.0.0.1:8000", metavar="URL")
    parser.add_argument("--api-prefix", default="/api/v1", metavar="PATH")
    parser.add_argument("--username", default="developer")
    parser.add_argument("--password", default="devpassword")
    args = parser.parse_args()

    base = args.backend_url.rstrip("/")
    api = f"{base}{args.api_prefix}"
    workspace_root = Path(__file__).parent.parent / "workspace"
    project_ws = workspace_root / MULTI_FIELD_PROJECT_ID
    frontend_dir = project_ws / "frontend"
    backend_dir = project_ws / "backend"

    print()
    print("M32 Validation -- Multi-Field Entity Forms")
    print("=" * 60)
    print(f"  Backend : {base}")
    print(f"  Project : {MULTI_FIELD_PROJECT_ID}")
    print()

    # ------------------------------------------------------------------
    # 1. Genesis backend health
    # ------------------------------------------------------------------
    print("1. Genesis Backend Health")
    status, body = http("GET", f"{base}/health")
    if status is None:
        _fail("GET /health", str(body))
        print()
        print("  Genesis backend unreachable. Start with:")
        print("    cd backend && python -m uvicorn main:app --port 8000")
        sys.exit(1)
    elif status == 200:
        _pass("GET /health")
    else:
        _fail("GET /health", f"HTTP {status}")

    # ------------------------------------------------------------------
    # 2. Authentication
    # ------------------------------------------------------------------
    print("\n2. Authentication")
    form_data = urllib.parse.urlencode({"username": args.username, "password": args.password}).encode()
    status, body = http(
        "POST", f"{api}/auth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=form_data,
    )
    if status == 200 and isinstance(body, dict) and "access_token" in body:
        token: str = body["access_token"]
        _pass(f"POST /auth/token (user: {args.username})")
    else:
        _fail("POST /auth/token", f"HTTP {status}: {_detail(body)}")
        sys.exit(1)

    auth = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # ------------------------------------------------------------------
    # 3. Generate multi_field_crud_001
    # ------------------------------------------------------------------
    print(f"\n3. Generate {MULTI_FIELD_PROJECT_ID}")
    print(f'  Prompt: "{CRM_PROMPT}"')

    plan = _generate_project(api, auth, MULTI_FIELD_PROJECT_ID, CRM_PROMPT, workspace_root)
    if plan is None:
        print("  Generation failed — skipping file-tree and content checks.")

    # ------------------------------------------------------------------
    # 4. File tree
    # ------------------------------------------------------------------
    print(f"\n4. File Tree Verification")

    required_files = [
        ("frontend/lib/api.ts",        frontend_dir / "lib" / "api.ts"),
        ("frontend/lib/types.ts",      frontend_dir / "lib" / "types.ts"),
        ("frontend/.env.example",      frontend_dir / ".env.example"),
        ("frontend/app/layout.tsx",    frontend_dir / "app" / "layout.tsx"),
        ("frontend/package.json",      frontend_dir / "package.json"),
        ("backend/app/database.py",    backend_dir / "app" / "database.py"),
        ("backend/app/models.py",      backend_dir / "app" / "models.py"),
        ("backend/app/schemas.py",     backend_dir / "app" / "schemas.py"),
        ("backend/app/main.py",        backend_dir / "app" / "main.py"),
    ]
    for label, path in required_files:
        if path.exists():
            _pass(f"{label} exists")
        else:
            _fail(f"{label} exists", "MISSING")

    entity_pages_dir = frontend_dir / "app"
    entity_page_files = []
    if entity_pages_dir.exists():
        entity_page_files = [
            d / "page.tsx"
            for d in entity_pages_dir.iterdir()
            if d.is_dir() and (d / "page.tsx").exists()
        ]
    if entity_page_files:
        names = ", ".join(sorted(p.parent.name for p in entity_page_files))
        _pass("entity page files", f"{len(entity_page_files)}: {names}")
    else:
        _fail("entity page files", "no app/{route}/page.tsx files found")

    for entity_plural in ["customers", "deals", "activities"]:
        page_path = frontend_dir / "app" / entity_plural / "page.tsx"
        if page_path.exists():
            _pass(f"frontend/app/{entity_plural}/page.tsx exists")
        else:
            _fail(f"frontend/app/{entity_plural}/page.tsx exists", "MISSING")

    # ------------------------------------------------------------------
    # 5. api.ts content checks (unchanged from M30)
    # ------------------------------------------------------------------
    print(f"\n5. api.ts Content")
    api_ts = frontend_dir / "lib" / "api.ts"
    if api_ts.exists():
        content = api_ts.read_text(encoding="utf-8")
        for symbol in ["API_BASE_URL", "listItems", "getItem", "createItem", "updateItem", "deleteItem"]:
            if symbol in content:
                _pass(f"api.ts exports {symbol!r}")
            else:
                _fail(f"api.ts exports {symbol!r}", "not found")
        if "8010" in content:
            _pass("api.ts default port is 8010")
        else:
            _fail("api.ts default port is 8010", "8010 not found")
    else:
        _fail("api.ts exists for content check", "MISSING")

    # ------------------------------------------------------------------
    # 6. types.ts content checks (unchanged from M30)
    # ------------------------------------------------------------------
    print(f"\n6. types.ts Content")
    types_ts = frontend_dir / "lib" / "types.ts"
    if types_ts.exists():
        content = types_ts.read_text(encoding="utf-8")
        for iface in ["Customer", "Deal", "Activity"]:
            if f"export interface {iface}" in content:
                _pass(f"types.ts exports interface {iface}")
            else:
                _fail(f"types.ts exports interface {iface}", "not found")
            if f"export type {iface}Create" in content:
                _pass(f"types.ts exports type {iface}Create")
            else:
                _fail(f"types.ts exports type {iface}Create", "not found")
        if "id: number" in content:
            _pass("types.ts includes id: number field")
        else:
            _fail("types.ts includes id: number field", "not found")
        if "Omit<" in content:
            _pass("types.ts uses Omit<> for Create types")
        else:
            _fail("types.ts uses Omit<> for Create types", "not found")
    else:
        _fail("types.ts exists for content check", "MISSING")

    # ------------------------------------------------------------------
    # 7. Entity page multi-field form checks
    # ------------------------------------------------------------------
    print(f"\n7. Entity Page Multi-Field Form Content")
    customers_page = frontend_dir / "app" / "customers" / "page.tsx"
    if customers_page.exists():
        content = customers_page.read_text(encoding="utf-8")

        # M31 baseline: CRUD behavior still present
        for symbol in ['"use client"', "useEffect", "useState", "listItems", "createItem",
                        "updateItem", "deleteItem", "editingId", "handleDelete"]:
            if symbol in content:
                _pass(f"customers/page.tsx has {symbol!r}")
            else:
                _fail(f"customers/page.tsx has {symbol!r}", "not found")

        # M32 new: typed form state object (not single fieldValue)
        if "useState<CustomerCreate>" in content:
            _pass("customers/page.tsx uses useState<CustomerCreate> for form state")
        else:
            _fail("customers/page.tsx uses useState<CustomerCreate> for form state", "not found")

        if "[form, setForm]" in content:
            _pass("customers/page.tsx uses [form, setForm] state destructuring")
        else:
            _fail("customers/page.tsx uses [form, setForm] state destructuring", "not found")

        # M32: form passed directly to API calls (no 'as unknown as' for create/update)
        if "createItem" in content and "form)" in content:
            _pass("customers/page.tsx passes form directly to createItem")
        else:
            _fail("customers/page.tsx passes form directly to createItem", "not found or still using assertion")

        if "updateItem" in content and ", form)" in content:
            _pass("customers/page.tsx passes form directly to updateItem")
        else:
            _fail("customers/page.tsx passes form directly to updateItem", "not found")

        # M32: multiple field inputs (Customer has name, email, phone, company, status)
        for field in ["name", "email", "phone", "company", "status"]:
            # Check for input with placeholder or name attribute matching the field
            if f'placeholder="{field}"' in content or f'name="{field}"' in content:
                _pass(f"customers/page.tsx has input for field {field!r}")
            else:
                _fail(f"customers/page.tsx has input for field {field!r}", "no placeholder/name attribute found")

        # M32: setForm with spread for onChange
        if "setForm({...form," in content or "setForm({ ...form," in content:
            _pass("customers/page.tsx uses setForm spread for field updates")
        else:
            _fail("customers/page.tsx uses setForm spread for field updates", "not found")

        # M32: no longer uses old single-field state names
        if "fieldValue" not in content and "editingValue" not in content:
            _pass("customers/page.tsx removed single-field state (fieldValue/editingValue)")
        else:
            _fail("customers/page.tsx removed single-field state",
                  "fieldValue or editingValue still present")

        # M32: no 'as unknown as' assertion (form is fully typed)
        if "as unknown as" not in content:
            _pass("customers/page.tsx has no 'as unknown as' assertion")
        else:
            _fail("customers/page.tsx has no 'as unknown as' assertion",
                  "'as unknown as' still present — form may not be fully typed")

        # Edit still works: setEditingId and setForm for pre-population
        if "setEditingId(item.id)" in content:
            _pass("customers/page.tsx Edit sets editingId from item")
        else:
            _fail("customers/page.tsx Edit sets editingId from item", "not found")

        if "setForm({" in content and "item.name" in content:
            _pass("customers/page.tsx Edit pre-populates form from item")
        else:
            _fail("customers/page.tsx Edit pre-populates form from item", "setForm with item fields not found")

        if "../../lib/api" in content:
            _pass("customers/page.tsx imports from ../../lib/api")
        else:
            _fail("customers/page.tsx imports from ../../lib/api", "not found")

        if "../../lib/types" in content:
            _pass("customers/page.tsx imports from ../../lib/types")
        else:
            _fail("customers/page.tsx imports from ../../lib/types", "not found")
    else:
        _fail("customers/page.tsx exists for content check", "MISSING")

    # ------------------------------------------------------------------
    # 8. Frontend npm install
    # ------------------------------------------------------------------
    print(f"\n8. Frontend npm install")
    npm_exe = _find_npm()
    if not frontend_dir.exists():
        _fail("frontend dir exists for npm install", "MISSING — skipping npm steps")
    else:
        print(f"  Running npm install in {frontend_dir}  (may take 2-5 minutes)...")
        rc, stdout, stderr = _run_npm(["install"], frontend_dir, timeout=360)
        if rc == 0:
            _pass("npm install", "exit code 0")
        else:
            _fail("npm install", f"exit code {rc}")
            last_lines = (stderr or stdout or "").strip().splitlines()[-20:]
            for line in last_lines:
                print(f"    {line}")

    # ------------------------------------------------------------------
    # 9. Frontend npm run build
    # ------------------------------------------------------------------
    print(f"\n9. Frontend npm run build")
    if not frontend_dir.exists():
        _fail("frontend dir exists for npm build", "MISSING")
    elif npm_exe and (frontend_dir / "node_modules").exists():
        print(f"  Running npm run build in {frontend_dir}  (may take 1-3 minutes)...")
        rc, stdout, stderr = _run_npm(["run", "build"], frontend_dir, timeout=360)
        if rc == 0:
            _pass("npm run build", "exit code 0")
        else:
            _fail("npm run build", f"exit code {rc}")
            all_output = (stdout + "\n" + stderr).strip().splitlines()
            last_lines = all_output[-30:]
            print("    --- build output (last 30 lines) ---")
            for line in last_lines:
                print(f"    {line}")
    else:
        reason = "npm not found" if not npm_exe else "node_modules missing (npm install failed)"
        _fail("npm run build", f"skipped: {reason}")

    # ------------------------------------------------------------------
    # 10. Generated backend py_compile
    # ------------------------------------------------------------------
    print(f"\n10. Generated Backend py_compile")
    if backend_dir.exists():
        py_files = sorted(backend_dir.rglob("*.py"))
        if py_files:
            for py_file in py_files:
                rel = py_file.relative_to(project_ws)
                if py_compile_check(py_file):
                    _pass(f"py_compile {rel}")
                else:
                    _fail(f"py_compile {rel}")
        else:
            _fail("backend Python files found", "none")
    else:
        _fail("backend dir exists for py_compile", "MISSING")

    # ------------------------------------------------------------------
    # 11. Backward compat: simple_no_entities_001
    # ------------------------------------------------------------------
    print(f"\n11. Backward Compat ({NO_ENTITIES_PROJECT_ID})")

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

    no_ent_api_ts = no_ent_ws / "frontend" / "lib" / "api.ts"
    if not no_ent_api_ts.exists():
        _pass("simple_no_entities_001: lib/api.ts absent (correct — no entities)")
    else:
        _fail("simple_no_entities_001: lib/api.ts absent", "generated for no-entity spec")

    no_ent_env = no_ent_ws / "frontend" / ".env.example"
    if no_ent_env.exists():
        _pass("simple_no_entities_001: frontend/.env.example exists")
    else:
        _fail("simple_no_entities_001: frontend/.env.example exists", "MISSING")

    no_ent_home = no_ent_ws / "frontend" / "app" / "home" / "page.tsx"
    if no_ent_home.exists():
        _pass("simple_no_entities_001: frontend/app/home/page.tsx exists (page-graph still works)")
    else:
        _fail("simple_no_entities_001: frontend/app/home/page.tsx exists", "MISSING")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print()
    print("=" * 60)
    if _failures:
        print(f"RESULT: FAIL  ({len(_failures)} failure(s))")
        for f in _failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("RESULT: PASS  (all M32 checks passed)")
        sys.exit(0)


if __name__ == "__main__":
    main()
