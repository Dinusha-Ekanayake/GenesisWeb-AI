#!/usr/bin/env python3
"""
M34 Validation -- Generated App UI Styling Foundation
======================================================
Validates that NextJsPlugin generates entity pages with CSS class-based
styling: container layout, styled form, styled table, styled buttons,
empty state, and a globals.css design system.

Sections:
  1.  Genesis backend health
  2.  Authentication
  3.  Generate styled_crud_app_001 via propose+approve-and-generate
  4.  File tree: lib/api.ts, lib/types.ts, .env.example, entity pages
  5.  globals.css styling content checks
  6.  customers/page.tsx className checks
  7.  customers/page.tsx CRUD behavior preserved (M32 baseline)
  8.  Frontend npm install
  9.  Frontend npm run build
  10. Generated backend py_compile
  11. Backward compat: simple_no_entities_001

Usage:
    python scripts/validate_m34.py
    python scripts/validate_m34.py --backend-url http://127.0.0.1:8000
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

STYLED_PROJECT_ID = "styled_crud_app_001"
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

    gen_payload = json.dumps({
        "plan": proposed_plan,
        "approval": {
            "approved": True,
            "approved_by": "m34_validation",
            "notes": "M34 automated validation.",
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
    parser = argparse.ArgumentParser(description="M34 styled UI validation")
    parser.add_argument("--backend-url", default="http://127.0.0.1:8000", metavar="URL")
    parser.add_argument("--api-prefix", default="/api/v1", metavar="PATH")
    parser.add_argument("--username", default="developer")
    parser.add_argument("--password", default="devpassword")
    args = parser.parse_args()

    base = args.backend_url.rstrip("/")
    api = f"{base}{args.api_prefix}"
    workspace_root = Path(__file__).parent.parent / "workspace"
    project_ws = workspace_root / STYLED_PROJECT_ID
    frontend_dir = project_ws / "frontend"
    backend_dir = project_ws / "backend"

    print()
    print("M34 Validation -- Generated App UI Styling Foundation")
    print("=" * 60)
    print(f"  Backend : {base}")
    print(f"  Project : {STYLED_PROJECT_ID}")
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
    # 3. Generate styled_crud_app_001
    # ------------------------------------------------------------------
    print(f"\n3. Generate {STYLED_PROJECT_ID}")
    print(f'  Prompt: "{CRM_PROMPT}"')

    plan = _generate_project(api, auth, STYLED_PROJECT_ID, CRM_PROMPT, workspace_root)
    if plan is None:
        print("  Generation failed — skipping file-tree and content checks.")

    # ------------------------------------------------------------------
    # 4. File tree
    # ------------------------------------------------------------------
    print("\n4. File Tree Verification")

    required_files = [
        ("frontend/lib/api.ts",       frontend_dir / "lib" / "api.ts"),
        ("frontend/lib/types.ts",     frontend_dir / "lib" / "types.ts"),
        ("frontend/.env.example",     frontend_dir / ".env.example"),
        ("frontend/app/layout.tsx",   frontend_dir / "app" / "layout.tsx"),
        ("frontend/app/globals.css",  frontend_dir / "app" / "globals.css"),
        ("frontend/package.json",     frontend_dir / "package.json"),
        ("backend/app/database.py",   backend_dir / "app" / "database.py"),
        ("backend/app/models.py",     backend_dir / "app" / "models.py"),
        ("backend/app/schemas.py",    backend_dir / "app" / "schemas.py"),
        ("backend/app/main.py",       backend_dir / "app" / "main.py"),
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
    # 5. globals.css styling content checks
    # ------------------------------------------------------------------
    print("\n5. globals.css Styling Content")
    globals_css = frontend_dir / "app" / "globals.css"
    if globals_css.exists():
        css = globals_css.read_text(encoding="utf-8", errors="replace")

        if "@tailwind base" in css:
            _pass("globals.css retains @tailwind base")
        else:
            _fail("globals.css retains @tailwind base", "not found")

        for selector in [".page-container", ".page-title", ".entity-form",
                          ".form-input", ".btn", ".btn-primary", ".btn-secondary",
                          ".btn-danger", ".data-table", ".empty-state", ".error-banner"]:
            if selector in css:
                _pass(f"globals.css defines {selector}")
            else:
                _fail(f"globals.css defines {selector}", "not found")

        if "font-family" in css:
            _pass("globals.css sets font-family on body")
        else:
            _fail("globals.css sets font-family on body", "not found")

        if "background" in css:
            _pass("globals.css sets background color")
        else:
            _fail("globals.css sets background color", "not found")

        if "border-collapse" in css:
            _pass("globals.css has table border-collapse")
        else:
            _fail("globals.css has table border-collapse", "not found")

        if "flex-wrap" in css or "display: flex" in css:
            _pass("globals.css uses flex layout for form")
        else:
            _fail("globals.css uses flex layout for form", "not found")
    else:
        _fail("globals.css exists for content check", "MISSING")

    # ------------------------------------------------------------------
    # 6. customers/page.tsx className checks (M34 new)
    # ------------------------------------------------------------------
    print("\n6. customers/page.tsx className Checks")
    customers_page = frontend_dir / "app" / "customers" / "page.tsx"
    if customers_page.exists():
        content = customers_page.read_text(encoding="utf-8")

        # Check for className presence (class may be combined with other modifiers)
        for needle, label in [
            ('className="page-container"', "page-container wrapper"),
            ('className="page-title"',     "page-title heading"),
            ('className="entity-form"',    "entity-form form"),
            ('className="form-input"',     "form-input on inputs"),
            ('className="btn btn-primary"', "btn-primary submit button"),
        ]:
            if needle in content:
                _pass(f"customers/page.tsx has {label}")
            else:
                _fail(f"customers/page.tsx has {label}", f"{needle!r} not found")

        # These class names may appear alongside modifiers like btn-sm
        for cls_name, label in [
            ("btn-secondary", "btn-secondary cancel/edit button"),
            ("btn-danger",    "btn-danger delete button"),
        ]:
            if cls_name in content:
                _pass(f"customers/page.tsx has {label}")
            else:
                _fail(f"customers/page.tsx has {label}", f"class {cls_name!r} not found")

        for needle, label in [
            ('className="data-table"',    "data-table table"),
            ('className="table-actions"', "table-actions wrapper"),
            ('className="empty-state"',   "empty-state paragraph"),
            ('className="error-banner"',  "error-banner paragraph"),
        ]:
            if needle in content:
                _pass(f"customers/page.tsx has {label}")
            else:
                _fail(f"customers/page.tsx has {label}", f"{needle!r} not found")

        # Empty state text content
        if "No customers yet" in content or "empty-state" in content:
            _pass("customers/page.tsx has empty state message")
        else:
            _fail("customers/page.tsx has empty state message", "empty-state content not found")

        # No raw inline style for error (replaced by className)
        if 'style={{ color: "red" }}' not in content and 'style={{color:"red"}}' not in content:
            _pass('customers/page.tsx error uses className not inline style')
        else:
            _fail('customers/page.tsx error uses className not inline style',
                  'style={{ color: "red" }} still present')
    else:
        _fail("customers/page.tsx exists for className check", "MISSING")

    # ------------------------------------------------------------------
    # 7. CRUD behavior preserved (M32 baseline checks)
    # ------------------------------------------------------------------
    print("\n7. CRUD Behavior Preserved (M32 baseline)")
    if customers_page.exists():
        content = customers_page.read_text(encoding="utf-8")

        for symbol in ['"use client"', "useEffect", "useState", "listItems",
                        "createItem", "updateItem", "deleteItem",
                        "editingId", "handleDelete"]:
            if symbol in content:
                _pass(f"customers/page.tsx has {symbol!r}")
            else:
                _fail(f"customers/page.tsx has {symbol!r}", "not found")

        if "useState<CustomerCreate>" in content:
            _pass("customers/page.tsx uses useState<CustomerCreate>")
        else:
            _fail("customers/page.tsx uses useState<CustomerCreate>", "not found")

        if "[form, setForm]" in content:
            _pass("customers/page.tsx uses [form, setForm]")
        else:
            _fail("customers/page.tsx uses [form, setForm]", "not found")

        if "form)" in content:
            _pass("customers/page.tsx passes form directly to createItem")
        else:
            _fail("customers/page.tsx passes form directly to createItem", "not found")

        for field in ["name", "email", "phone", "company", "status"]:
            if f'placeholder="{field}"' in content or f'name="{field}"' in content:
                _pass(f"customers/page.tsx has input for field {field!r}")
            else:
                _fail(f"customers/page.tsx has input for field {field!r}",
                      "no placeholder/name attribute found")

        if "setEditingId(item.id)" in content:
            _pass("customers/page.tsx Edit sets editingId")
        else:
            _fail("customers/page.tsx Edit sets editingId", "not found")

        if "Edit" in content and "Delete" in content and "Cancel" in content:
            _pass("customers/page.tsx has Edit, Delete, Cancel actions")
        else:
            _fail("customers/page.tsx has Edit, Delete, Cancel actions", "one or more missing")

        if "as unknown as" not in content:
            _pass("customers/page.tsx has no 'as unknown as' assertion")
        else:
            _fail("customers/page.tsx has no 'as unknown as' assertion", "still present")

        if "../../lib/api" in content and "../../lib/types" in content:
            _pass("customers/page.tsx imports from lib paths")
        else:
            _fail("customers/page.tsx imports from lib paths", "missing import(s)")
    else:
        _fail("customers/page.tsx exists for CRUD check", "MISSING")

    # ------------------------------------------------------------------
    # 8. Frontend npm install
    # ------------------------------------------------------------------
    print("\n8. Frontend npm install")
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
    print("\n9. Frontend npm run build")
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
    print("\n10. Generated Backend py_compile")
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

    no_ent_css = no_ent_ws / "frontend" / "app" / "globals.css"
    if no_ent_css.exists():
        css_content = no_ent_css.read_text(encoding="utf-8")
        if ".page-container" in css_content:
            _pass("simple_no_entities_001: globals.css has styling (no-entity path)")
        else:
            _fail("simple_no_entities_001: globals.css has styling", ".page-container not found")
    else:
        _fail("simple_no_entities_001: frontend/app/globals.css exists", "MISSING")

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
        print("RESULT: PASS  (all M34 checks passed)")
        sys.exit(0)


if __name__ == "__main__":
    main()
