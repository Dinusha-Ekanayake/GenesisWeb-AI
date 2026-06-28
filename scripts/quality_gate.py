import os
import sys
import subprocess
from pathlib import Path

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

def run_step(name: str, cmd: list, cwd: str) -> bool:
    print(f"\n[{name}] Running...")
    try:
        # Use shell=True for npm on Windows
        shell = True if "npm" in cmd[0] else False
        result = subprocess.run(cmd, cwd=cwd, text=True, shell=shell)
        if result.returncode != 0:
            print(f"[{name}] FAILED (Exit Code: {result.returncode})")
            return False
        print(f"[{name}] SUCCESS")
        return True
    except Exception as e:
        print(f"[{name}] FAILED: {e}")
        return False

def main():
    print("=======================================")
    print("Genesis Engine v1.0 Quality Gate")
    print("=======================================")
    
    steps = [
        {"name": "Backend Linter (Ruff)", "cmd": ["ruff", "check", "app", "tests", "scripts"], "cwd": BACKEND_DIR},
        {"name": "Backend Type Check (MyPy)", "cmd": ["mypy", "app"], "cwd": BACKEND_DIR},
        {"name": "Backend Tests & Coverage", "cmd": ["pytest", "tests/", "--cov=app", "--cov-fail-under=90"], "cwd": BACKEND_DIR},
        {"name": "Frontend Linter", "cmd": ["npm", "run", "lint"], "cwd": FRONTEND_DIR},
        {"name": "Frontend Type Check", "cmd": ["npm", "run", "tsc"], "cwd": FRONTEND_DIR},
        {"name": "Frontend Unit Tests (Vitest)", "cmd": ["npm", "run", "test", "--", "--run", "--coverage", "--coverage.statements=80"], "cwd": FRONTEND_DIR},
        {"name": "Frontend E2E Tests (Playwright)", "cmd": ["npm", "run", "test:e2e"], "cwd": FRONTEND_DIR},
        {"name": "Contract Verification", "cmd": ["python", "scripts/verify_contracts.py"], "cwd": BACKEND_DIR},
    ]
    
    all_passed = True
    for step in steps:
        if not run_step(step["name"], step["cmd"], step["cwd"]):
            all_passed = False
            break
            
    print("\n=======================================")
    if all_passed:
        print("QUALITY GATE: PASSED. Ready for Packaging.")
        sys.exit(0)
    else:
        print("QUALITY GATE: FAILED. Packaging Blocked.")
        sys.exit(1)

if __name__ == "__main__":
    main()
