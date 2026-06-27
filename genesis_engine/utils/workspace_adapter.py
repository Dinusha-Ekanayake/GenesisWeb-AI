import os
from pathlib import Path
from pydantic import BaseModel

class WorkspaceAdapter:
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)

    def flush_transaction(self, project_id: str, artifacts: dict[str, BaseModel]) -> None:
        """
        Performs a single transactional flush of all generated planning artifacts to disk.
        """
        project_dir = self.workspace_root / project_id / "artifacts"
        project_dir.mkdir(parents=True, exist_ok=True)

        for filename, model in artifacts.items():
            file_path = project_dir / filename
            with open(file_path, "w") as f:
                f.write(model.model_dump_json(indent=2))

    def write_code_artifacts(self, project_id: str, artifacts: list) -> None:
        """Writes physical code artifacts to the workspace."""
        project_dir = self.workspace_root / project_id
        
        for artifact in artifacts:
            file_path = project_dir / artifact.path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w") as f:
                f.write(artifact.content)
