import os
import shutil
import hashlib
import json
from pathlib import Path
from ..models.outputs import DeploymentManifest

class Packager:
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)

    def _hash_file(self, filepath: Path) -> str:
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def bundle(self, project_id: str, planning_report: dict) -> DeploymentManifest:
        project_dir = self.workspace_root / project_id
        dist_dir = self.workspace_root.parent / "dist" / project_id
        dist_dir.mkdir(parents=True, exist_ok=True)
        
        bundle_path = dist_dir / "deployment_bundle"
        
        # Zip the project directory
        # shutil.make_archive adds the .zip extension automatically
        shutil.make_archive(str(bundle_path), 'zip', str(project_dir))
        zip_file = Path(f"{bundle_path}.zip")
        
        # Compute deterministic SHA256 of the zip
        deployment_hash = self._hash_file(zip_file)
        
        # Prepare Manifest
        manifest = DeploymentManifest(
            project_id=project_id,
            graph_hashes=planning_report.get("graph_hashes", {}),
            rule_engine_score=planning_report.get("graph_integrity_score", 0),
            plugin_versions={
                "FastApiMinimalGenerator": "1.0",
                "NextJsMinimalGenerator": "1.0"
            },
            build_status="SUCCESS",
            deployment_hash=deployment_hash
        )
        
        # Save Manifest
        manifest_path = dist_dir / "deployment_manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest.model_dump(mode="json"), f, indent=4)
            
        print(f"[Packager] Packaged {project_id} -> {zip_file}")
        print(f"[Packager] Deployment SHA-256: {deployment_hash}")
        
        return manifest
