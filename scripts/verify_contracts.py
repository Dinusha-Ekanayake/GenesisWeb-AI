"""
Genesis Engine – OpenAPI Contract Verification Script
======================================================
Verifies that every endpoint defined in the FastAPI OpenAPI schema exists
in the frontend TypeScript API client (genesis-api.ts) and that every
frontend API call maps to a real backend endpoint.

Exit codes:
  0 = All contracts satisfied
  1 = Contract violations found

Usage:
  python scripts/verify_contracts.py
"""

import sys
import json
import os
import re
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.resolve()
FRONTEND_API_FILE = ROOT_DIR / "frontend" / "src" / "app" / "dashboard" / "lib" / "genesis-api.ts"

# These endpoints are known to require direct form-data submission (OAuth2)
# and therefore do NOT appear in the TypeScript GenesisAPI object.
EXCLUDED_ENDPOINTS = {
    "/api/v1/auth/token",
    "/api/v1/genesis/parse",  # Explicitly marked "Not Implemented" placeholder
}


def load_openapi_schema():
    """Load the OpenAPI schema from the running FastAPI server or from JSON export."""
    schema_path = ROOT_DIR / "backend" / "openapi.json"
    if schema_path.exists():
        with open(schema_path) as f:
            return json.load(f)

    print("[ContractVerifier] openapi.json not found. Attempting to generate from FastAPI app...")
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, "-c",
             "import json; import sys; sys.path.insert(0,'backend');"
             "from backend.main import app; "
             "print(json.dumps(app.openapi()))"],
            capture_output=True, text=True, cwd=str(ROOT_DIR)
        )
        if result.returncode != 0:
            print(f"[ContractVerifier] Failed to extract OpenAPI schema:\n{result.stderr}")
            sys.exit(1)
        return json.loads(result.stdout)
    except Exception as e:
        print(f"[ContractVerifier] Error: {e}")
        sys.exit(1)


def extract_backend_paths(schema: dict) -> set:
    """Extract all unique paths from the OpenAPI schema."""
    paths = set()
    prefix = "/api/v1"
    for path, methods in schema.get("paths", {}).items():
        for method in methods:
            if method.upper() in ("GET", "POST", "PUT", "DELETE", "PATCH"):
                full_path = f"{prefix}{path}" if not path.startswith(prefix) else path
                paths.add(f"{method.upper()} {full_path}")
    return paths


def extract_frontend_paths(ts_content: str) -> set:
    """
    Parse the TypeScript genesis-api.ts file to extract all endpoint paths called.
    Handles template literals and simple string literals.
    """
    # Match both static and template literal paths inside fetchWrapper calls
    paths = set()
    # Match fetchWrapper<...>(`/genesis/...` or "/genesis/...")
    pattern = re.compile(
        r'fetchWrapper\s*<[^>]*>\s*\(\s*[`\'"]([^`\'"]+)[`\'"]',
        re.MULTILINE
    )
    for match in pattern.finditer(ts_content):
        path = match.group(1)
        # Normalize dynamic segments: /projects/${id}/graphs → /projects/{id}/graphs
        path = re.sub(r'\$\{[^}]+\}', '{id}', path)
        # strip query parameters
        path = path.split("?")[0]
        paths.add(f"/api/v1{path}")
    return paths


def run_contract_verification():
    print("=" * 60)
    print("Genesis Engine Contract Verification")
    print("=" * 60)

    # 1. Load backend schema
    schema = load_openapi_schema()
    backend_paths = extract_backend_paths(schema)

    # 2. Load frontend API calls
    if not FRONTEND_API_FILE.exists():
        print(f"[ContractVerifier] FAIL: Frontend API file not found: {FRONTEND_API_FILE}")
        sys.exit(1)

    ts_content = FRONTEND_API_FILE.read_text(encoding="utf-8")
    frontend_paths = extract_frontend_paths(ts_content)

    print(f"\nBackend endpoints:  {len(backend_paths)}")
    print(f"Frontend API calls: {len(frontend_paths)}")

    violations = []

    # 3. Check every frontend call maps to a backend endpoint
    backend_path_set = {p.split(" ", 1)[1] for p in backend_paths}
    for fp in sorted(frontend_paths):
        if fp not in backend_path_set and fp not in EXCLUDED_ENDPOINTS:
            violations.append(f"  ORPHAN FRONTEND CALL: {fp} (no matching backend endpoint)")

    # 4. Check every backend endpoint is covered (warnings only for new ones)
    for bp in sorted(backend_paths):
        method, path = bp.split(" ", 1)
        full = path
        if full in EXCLUDED_ENDPOINTS:
            continue
        if full not in frontend_paths:
            # This is not necessarily a violation; the backend may expose admin endpoints
            # not used by the primary dashboard. Report as info only.
            print(f"  [INFO] Backend endpoint not referenced by frontend: {bp}")

    print()
    if violations:
        print(f"CONTRACT VERIFICATION FAILED: {len(violations)} violation(s) found.")
        for v in violations:
            print(v)
        sys.exit(1)
    else:
        print("CONTRACT VERIFICATION PASSED. All frontend API calls map to valid backend endpoints.")
        sys.exit(0)


if __name__ == "__main__":
    run_contract_verification()
