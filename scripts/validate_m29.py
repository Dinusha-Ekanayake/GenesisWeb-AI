#!/usr/bin/env python3
"""
M29 Validation -- SQLAlchemy Model and SQLite Persistence Foundation
====================================================================
Validates that FastApiPlugin generates SQLAlchemy-backed CRUD endpoints
instead of in-memory storage, and that data persists across server restarts.

Sections:
  1.  Genesis backend health
  2.  Authentication
  3.  Generate sqlite_persistence_001 via propose+approve-and-generate
  4.  File tree: database.py, models.py, schemas.py, routers/, main.py
  5.  py_compile all generated backend Python files
  6.  Content: sqlalchemy in requirements.txt
  7.  Content: database.py symbols (get_db, engine, Base, genesis_app.db)
  8.  Content: models.py symbols (Base, Column, Integer, String)
  9.  Content: schemas.py has from_attributes=True
  10. Content: router uses Session, Depends, get_db, db.query, db.commit
  11. Content: main.py calls Base.metadata.create_all
  12. storage.py absent
  13. Live: start generated backend on port 8010, POST customer, verify response
  14. Live: stop, restart, GET customer -- verify persistence
  15. File: genesis_app.db exists after live test

Usage:
    python scripts/validate_m29.py
    python scripts/validate_m29.py --backend-url http://127.0.0.1:8000
"""

import argparse
import ast
import json
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

PERSIST_PROJECT_ID = "sqlite_persistence_001"
PERSIST_PROMPT = (
    "Create a CRM for a sales team with customers, deals, activities, "
    "reports, team roles, and settings."
)
GENERATED_PORT = 8010

_failures: list = []


def _pass(label: str, detail: str = "") -> None:
    suffix = f"  -- {detail}" if detail else ""
    print(f"  [PASS] {label}{suffix}")


def _fail(label: str, detail: str = "") -> None:
    suffix = f"  -- {detail}" if detail else ""
    print(f"  [FAIL] {label}{suffix}")
    _failures.append(label)


def http(method, url, *, headers=None, data=None, timeout=30):
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


def _start_generated_backend(backend_dir: Path) -> subprocess.Popen:
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--port", str(GENERATED_PORT)],
        cwd=str(backend_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _wait_for_server(base_url: str, timeout_s: int = 30) -> bool:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            status, _ = http("GET", f"{base_url}/health", timeout=3)
            if status == 200:
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def _stop_proc(proc: subprocess.Popen) -> None:
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=8)
        except subprocess.TimeoutExpired:
            proc.kill()


def main() -> None:
    parser = argparse.ArgumentParser(description="M29 SQLite persistence validation")
    parser.add_argument("--backend-url", default="http://127.0.0.1:8000", metavar="URL")
    parser.add_argument("--api-prefix", default="/api/v1", metavar="PATH")
    parser.add_argument("--username", default="developer")
    parser.add_argument("--password", default="devpassword")
    args = parser.parse_args()

    base = args.backend_url.rstrip("/")
    api = f"{base}{args.api_prefix}"
    workspace_root = Path(__file__).parent.parent / "workspace"
    project_ws = workspace_root / PERSIST_PROJECT_ID
    backend_dir = project_ws / "backend"
    backend_app = backend_dir / "app"
    generated_base = f"http://127.0.0.1:{GENERATED_PORT}"

    print()
    print("M29 Validation -- SQLAlchemy Model and SQLite Persistence Foundation")
    print("=" * 70)
    print(f"  Genesis backend  : {base}")
    print(f"  Generated backend: {generated_base}  (started by this script)")
    print(f"  Project ID       : {PERSIST_PROJECT_ID}")
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
    # 3. Generate sqlite_persistence_001
    # ------------------------------------------------------------------
    print(f"\n3. Generate {PERSIST_PROJECT_ID}")
    print(f'  Prompt: "{PERSIST_PROMPT}"')

    if project_ws.exists():
        shutil.rmtree(project_ws, ignore_errors=True)
        print(f"  Cleaned prior workspace: {project_ws}")

    propose_payload = json.dumps({
        "prompt": PERSIST_PROMPT,
        "project_id": PERSIST_PROJECT_ID,
        "preferences": {"frontend": "nextjs", "backend": "fastapi", "database": "postgresql"},
    }).encode()

    status, body = http("POST", f"{api}/genesis/propose", headers=auth,
                        data=propose_payload, timeout=60)
    if status != 200 or not (isinstance(body, dict) and body.get("success")):
        _fail(f"POST /genesis/propose ({PERSIST_PROJECT_ID})", f"HTTP {status}: {_detail(body)}")
        sys.exit(1)

    data = body.get("data") or {}
    proposed_plan = data.get("plan")
    entities = (proposed_plan or {}).get("entities", [])
    gen_method = (proposed_plan or {}).get("generation_method", "?")
    _pass("POST /genesis/propose", f"method={gen_method}  entities={len(entities)}: {entities}")

    if not entities:
        print("  WARNING: plan has no entities — SQLAlchemy path will NOT be exercised")

    gen_payload = json.dumps({
        "plan": proposed_plan,
        "approval": {
            "approved": True,
            "approved_by": "m29_validation",
            "notes": "M29 automated validation.",
        },
    }).encode()

    print("  Generating (may take 30-120s)...")
    status, body = http("POST", f"{api}/genesis/approve-and-generate", headers=auth,
                        data=gen_payload, timeout=180)
    if status == 200 and isinstance(body, dict) and body.get("success"):
        resp_data = body.get("data") or {}
        manifest = resp_data.get("manifest") or {}
        build_status = manifest.get("build_status", "?") if isinstance(manifest, dict) else "?"
        _pass("POST /genesis/approve-and-generate", f"build_status={build_status}")
        if build_status != "SUCCESS":
            _fail("build_status==SUCCESS", f"got {build_status}")
    else:
        _fail("POST /genesis/approve-and-generate", f"HTTP {status}: {_detail(body)}")
        sys.exit(1)

    # ------------------------------------------------------------------
    # 4. File tree
    # ------------------------------------------------------------------
    print(f"\n4. File Tree Verification")

    required_files = [
        ("backend/requirements.txt",          backend_dir / "requirements.txt"),
        ("backend/app/__init__.py",            backend_app / "__init__.py"),
        ("backend/app/database.py",            backend_app / "database.py"),
        ("backend/app/models.py",              backend_app / "models.py"),
        ("backend/app/schemas.py",             backend_app / "schemas.py"),
        ("backend/app/main.py",                backend_app / "main.py"),
        ("backend/app/routers/__init__.py",    backend_app / "routers" / "__init__.py"),
    ]
    for label, path in required_files:
        if path.exists():
            _pass(f"{label} exists")
        else:
            _fail(f"{label} exists", "MISSING")

    storage_path = backend_app / "storage.py"
    if not storage_path.exists():
        _pass("backend/app/storage.py absent (removed in M29)")
    else:
        _fail("backend/app/storage.py absent", "still present — M29 should have removed it")

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
    print(f"\n5. py_compile — All Generated Backend Python Files")
    py_files = sorted(backend_dir.rglob("*.py")) if backend_dir.exists() else []
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
    # 6. requirements.txt includes sqlalchemy
    # ------------------------------------------------------------------
    print(f"\n6. requirements.txt")
    req_path = backend_dir / "requirements.txt"
    if req_path.exists():
        req_content = req_path.read_text(encoding="utf-8")
        if "sqlalchemy" in req_content.lower():
            _pass("requirements.txt includes sqlalchemy")
        else:
            _fail("requirements.txt includes sqlalchemy", "not found")
    else:
        _fail("requirements.txt exists", "MISSING")

    # ------------------------------------------------------------------
    # 7. database.py content
    # ------------------------------------------------------------------
    print(f"\n7. database.py Content")
    db_path = backend_app / "database.py"
    if db_path.exists():
        db_content = db_path.read_text(encoding="utf-8")
        for symbol in ["get_db", "engine", "Base", "SessionLocal", "genesis_app.db"]:
            if symbol in db_content:
                _pass(f"database.py has {symbol!r}")
            else:
                _fail(f"database.py has {symbol!r}", "not found")
        if "check_same_thread" in db_content:
            _pass("database.py has check_same_thread=False (required for SQLite + FastAPI)")
        else:
            _fail("database.py has check_same_thread=False", "not found — SQLite cross-thread access will fail")
    else:
        _fail("database.py exists for content check", "MISSING")

    # ------------------------------------------------------------------
    # 8. models.py content
    # ------------------------------------------------------------------
    print(f"\n8. models.py Content")
    models_path = backend_app / "models.py"
    if models_path.exists():
        models_content = models_path.read_text(encoding="utf-8")
        for symbol in ["Base", "Column", "Integer", "String"]:
            if symbol in models_content:
                _pass(f"models.py has {symbol!r}")
            else:
                _fail(f"models.py has {symbol!r}", "not found")
        if "primary_key=True" in models_content:
            _pass("models.py has primary_key=True on id column")
        else:
            _fail("models.py has primary_key=True on id column")
        if "__tablename__" in models_content:
            _pass("models.py has __tablename__")
        else:
            _fail("models.py has __tablename__")
    else:
        _fail("models.py exists for content check", "MISSING")

    # ------------------------------------------------------------------
    # 9. schemas.py has from_attributes=True
    # ------------------------------------------------------------------
    print(f"\n9. schemas.py Content")
    schemas_path = backend_app / "schemas.py"
    if schemas_path.exists():
        schemas_content = schemas_path.read_text(encoding="utf-8")
        if "from_attributes=True" in schemas_content:
            _pass("schemas.py has from_attributes=True (Pydantic v2 ORM compat)")
        else:
            _fail("schemas.py has from_attributes=True",
                  "missing — FastAPI cannot serialize SQLAlchemy ORM objects without this")
        if "ConfigDict" in schemas_content:
            _pass("schemas.py imports ConfigDict")
        else:
            _fail("schemas.py imports ConfigDict")
        if "BaseModel" in schemas_content:
            _pass("schemas.py imports BaseModel")
        else:
            _fail("schemas.py imports BaseModel")
    else:
        _fail("schemas.py exists for content check", "MISSING")

    # ------------------------------------------------------------------
    # 10. Router content: SQLAlchemy patterns present, storage.py patterns absent
    # ------------------------------------------------------------------
    print(f"\n10. Router Content")
    if entity_routers:
        sample = entity_routers[0]
        router_content = sample.read_text(encoding="utf-8")
        for symbol in ["Session", "Depends", "get_db", "db.query", "db.commit"]:
            if symbol in router_content:
                _pass(f"{sample.name} has {symbol!r}")
            else:
                _fail(f"{sample.name} has {symbol!r}", "not found")
        if "get_store" in router_content or "next_id" in router_content:
            _fail(f"{sample.name}: storage.py patterns absent",
                  "get_store/next_id still present — router not updated")
        else:
            _pass(f"{sample.name}: storage.py patterns absent")
        if "db.refresh" in router_content:
            _pass(f"{sample.name} has db.refresh (returns ORM-populated id after create)")
        else:
            _fail(f"{sample.name} has db.refresh", "not found — id may not be populated on create")
    else:
        _fail("entity router files exist for content check", "none found")

    # ------------------------------------------------------------------
    # 11. main.py calls Base.metadata.create_all
    # ------------------------------------------------------------------
    print(f"\n11. main.py Content")
    main_path = backend_app / "main.py"
    if main_path.exists():
        main_content = main_path.read_text(encoding="utf-8")
        if "create_all" in main_content:
            _pass("main.py has Base.metadata.create_all() (tables created on startup)")
        else:
            _fail("main.py has Base.metadata.create_all()",
                  "tables will not be created — backend starts but CRUD will fail")
        if "from . import models" in main_content or "from .models" in main_content:
            _pass("main.py imports models module (ORM registered before create_all)")
        else:
            _fail("main.py imports models module",
                  "ORM classes may not be registered in Base.metadata when create_all runs")
        if "include_router" in main_content:
            _pass("main.py has include_router calls")
        else:
            _fail("main.py has include_router calls")
        if '"/health"' in main_content or "'/health'" in main_content:
            _pass("main.py has /health endpoint")
        else:
            _fail("main.py has /health endpoint")
    else:
        _fail("main.py exists for content check", "MISSING")

    # ------------------------------------------------------------------
    # 12. storage.py absent (already checked in section 4, shown here for clarity)
    # ------------------------------------------------------------------
    print(f"\n12. storage.py Absent")
    if not storage_path.exists():
        _pass("backend/app/storage.py absent")
    else:
        _fail("backend/app/storage.py absent", "storage.py still generated — M29 removes it")

    # ------------------------------------------------------------------
    # 13-15. Live server tests
    # ------------------------------------------------------------------
    if not backend_dir.exists():
        _fail("backend_dir exists for live test", "MISSING — skipping live tests")
        _summarize()
        return

    proc1 = None
    proc2 = None
    customer_id = None

    try:
        # Section 13: start, POST customer
        print(f"\n13. Live Server — POST Customer  (port {GENERATED_PORT})")
        proc1 = _start_generated_backend(backend_dir)
        print(f"  Started generated backend (PID {proc1.pid})...")

        if not _wait_for_server(generated_base, timeout_s=30):
            stderr_bytes = b""
            try:
                proc1.wait(timeout=1)
                stderr_bytes = proc1.stderr.read(4000)
            except Exception:
                pass
            _fail("generated backend /health responds within 30s", "startup timeout")
            if stderr_bytes:
                print(f"    stderr: {stderr_bytes.decode('utf-8', errors='replace')[:600]}")
        else:
            _pass("generated backend started — /health responds")

            customer_payload = json.dumps({
                "name": "Acme Corp",
                "email": "hello@acme.com",
                "phone": "0712345678",
                "company": "Acme",
                "status": "Lead",
            }).encode()

            status, body = http(
                "POST", f"{generated_base}/api/v1/customers/",
                headers={"Content-Type": "application/json"},
                data=customer_payload,
                timeout=10,
            )
            if status == 201 and isinstance(body, dict):
                _pass("POST /api/v1/customers", f"HTTP {status}")
                customer_id = body.get("id")
                if customer_id is not None:
                    _pass("response has id", f"id={customer_id}")
                else:
                    _fail("response has id", f"body={body}")
                for field in ["name", "email", "phone", "company", "status"]:
                    if field in body:
                        _pass(f"response has field {field!r}", f"value={body[field]!r}")
                    else:
                        _fail(f"response has field {field!r}", "not in response")
            else:
                _fail("POST /api/v1/customers", f"HTTP {status}: {_detail(body)}")

        # Stop server 1
        _stop_proc(proc1)
        proc1 = None
        print("  Stopped server (first instance)")
        time.sleep(1.5)  # allow OS to release the port

        # Section 14: restart, GET — verify persistence
        print(f"\n14. Persistence — Restart and GET Customer")
        proc2 = _start_generated_backend(backend_dir)
        print(f"  Restarted generated backend (PID {proc2.pid})...")

        if not _wait_for_server(generated_base, timeout_s=30):
            _fail("restarted backend /health responds within 30s", "startup timeout")
        else:
            _pass("restarted backend started — /health responds")

            get_id = customer_id if customer_id is not None else 1
            status, body = http(
                "GET", f"{generated_base}/api/v1/customers/{get_id}",
                timeout=10,
            )
            if status == 200 and isinstance(body, dict):
                _pass(f"GET /api/v1/customers/{get_id} after restart", f"HTTP {status}")
                if body.get("name") == "Acme Corp":
                    _pass("persisted record: name == 'Acme Corp'")
                else:
                    _fail("persisted record: name == 'Acme Corp'", f"got {body.get('name')!r}")
                if body.get("email") == "hello@acme.com":
                    _pass("persisted record: email == 'hello@acme.com'")
                else:
                    _fail("persisted record: email == 'hello@acme.com'", f"got {body.get('email')!r}")
            else:
                _fail(f"GET /api/v1/customers/{get_id} after restart",
                      f"HTTP {status}: {_detail(body)}")

        # Section 15: genesis_app.db file
        print(f"\n15. SQLite Database File")
        db_file = backend_dir / "genesis_app.db"
        if db_file.exists():
            size = db_file.stat().st_size
            _pass("genesis_app.db exists", f"size={size} bytes at {db_file}")
        else:
            _fail("genesis_app.db exists", f"NOT FOUND at {db_file}")

    finally:
        _stop_proc(proc1)
        _stop_proc(proc2)

    _summarize()


def _summarize() -> None:
    print()
    print("=" * 70)
    if _failures:
        print(f"RESULT: FAIL  ({len(_failures)} failure(s))")
        for f in _failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("RESULT: PASS  (all M29 checks passed)")
        sys.exit(0)


if __name__ == "__main__":
    main()
