import os
from pathlib import Path

# In a real app, this might come from a config/env variable
BASE_WORKSPACE_DIR = Path(os.getenv("WORKSPACE_DIR", "./workspace")).resolve()

class WorkspaceManager:
    @staticmethod
    def create_project_workspace(project_id: str) -> Path:
        """
        Creates the physical directory structure for a new project.
        workspace/
          {project_id}/
            specification/
            artifacts/
            frontend/
            backend/
            docs/
            logs/
            exports/
        """
        project_dir = BASE_WORKSPACE_DIR / project_id
        
        folders = [
            "specification",
            "artifacts",
            "frontend",
            "backend",
            "docs",
            "logs",
            "exports"
        ]
        
        for folder in folders:
            # parents=True ensures parent directories are created
            # exist_ok=True prevents errors if it already exists
            (project_dir / folder).mkdir(parents=True, exist_ok=True)
            
        return project_dir

    @staticmethod
    def get_project_dir(project_id: str) -> Path:
        return BASE_WORKSPACE_DIR / project_id
