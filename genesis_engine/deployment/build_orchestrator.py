import os
import shutil
from pathlib import Path
from .packager import Packager

class BuildOrchestrator:
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.templates_dir = Path(__file__).parent / "templates"
        self.packager = Packager(workspace_root)
        
    def _validate_workspace(self, project_id: str) -> bool:
        project_dir = self.workspace_root / project_id
        if not project_dir.exists():
            raise FileNotFoundError(f"Project directory {project_dir} does not exist.")
            
        # Optional: Validate frontend and backend exist. But wait, if they aren't generated yet 
        # (e.g. an API only project), we shouldn't hard crash. However, since we are building a full-stack compiler:
        backend_dir = project_dir / "backend"
        frontend_dir = project_dir / "frontend"
        
        if not backend_dir.exists() and not frontend_dir.exists():
            raise ValueError(f"Project {project_id} has neither a frontend nor backend directory to build.")
            
        return True
        
    def _inject_templates(self, project_id: str):
        project_dir = self.workspace_root / project_id
        
        # Copy backend Dockerfile
        if (project_dir / "backend").exists():
            shutil.copy(self.templates_dir / "Dockerfile.backend", project_dir / "Dockerfile.backend")
            
        # Copy frontend Dockerfile
        if (project_dir / "frontend").exists():
            shutil.copy(self.templates_dir / "Dockerfile.frontend", project_dir / "Dockerfile.frontend")
            
        # Copy docker-compose (we can assume full stack for now based on Phase 9 requirements)
        shutil.copy(self.templates_dir / "docker-compose.yml", project_dir / "docker-compose.yml")
        
        print(f"[BuildOrchestrator] Injected deployment templates for {project_id}")

    def execute_build(self, project_id: str, planning_report: dict):
        print(f"\n--- [BuildOrchestrator] Starting Deployment Pipeline for {project_id} ---")
        
        # 1. Validate Workspace existence
        self._validate_workspace(project_id)
        
        # 2. Tamper Detection (Verify workspace hasn't been modified since generation)
        from ..utils.hash_utils import compute_deterministic_workspace_hash
        project_dir = self.workspace_root / project_id
        current_hash = compute_deterministic_workspace_hash(project_dir)
        expected_hash = planning_report.get("workspace_hash", "")
        
        if expected_hash and current_hash != expected_hash:
            raise RuntimeError(f"CompilerTamperError: Workspace integrity compromised! Expected {expected_hash}, got {current_hash}")
        
        # 3. Inject Docker Templates
        self._inject_templates(project_id)
        
        # 4. Deterministically Package Workspace
        manifest = self.packager.bundle(project_id, planning_report)
        
        print(f"--- [BuildOrchestrator] Deployment Bundle Ready: /dist/{project_id}/ ---")
        return manifest
