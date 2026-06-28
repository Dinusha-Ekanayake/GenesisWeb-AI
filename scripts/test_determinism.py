import sys
import os
import hashlib
from pathlib import Path
import shutil

# Ensure genesis engine is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from genesis_engine.core.orchestrator import ExecutionOrchestrator
from genesis_engine.models.spec import ProjectSpecification

def hash_file(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def main():
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../workspace"))
    orchestrator = ExecutionOrchestrator(workspace_root)
    
    spec_data = {
        "project_id": "determinism_test",
        "description": "A determinism test project",
        "requirements": ["Feature A", "Feature B"],
        "architecture": {
            "frontend_framework": "React",
            "backend_framework": "FastAPI",
            "database": "PostgreSQL"
        }
    }
    spec = ProjectSpecification(**spec_data)
    
    # Run 1
    print("Running compilation 1...")
    manifest1 = orchestrator.run_full_pipeline(spec)
    hash_workspace1 = manifest1.deployment_hash
    hash_zip1 = hash_file(Path(workspace_root) / "determinism_test" / "exports" / "deployment_bundle.zip")
    
    # Clean up workspace completely for a fresh run
    shutil.rmtree(Path(workspace_root) / "determinism_test")
    
    # Run 2
    print("Running compilation 2...")
    manifest2 = orchestrator.run_full_pipeline(spec)
    hash_workspace2 = manifest2.deployment_hash
    hash_zip2 = hash_file(Path(workspace_root) / "determinism_test" / "exports" / "deployment_bundle.zip")
    
    print(f"Run 1 Workspace: {hash_workspace1} | Zip: {hash_zip1}")
    print(f"Run 2 Workspace: {hash_workspace2} | Zip: {hash_zip2}")
    
    if hash_workspace1 != hash_workspace2:
        print("FAIL: Workspace hashes differ!")
        sys.exit(1)
        
    if hash_zip1 != hash_zip2:
        print("FAIL: Zip hashes differ!")
        sys.exit(1)
        
    print("PASS: Determinism verified.")

if __name__ == "__main__":
    main()
