import os
import zipfile
import hashlib
import json
from pathlib import Path
from ..models.outputs import DeploymentManifest
from ..utils.hash_utils import compute_deterministic_workspace_hash

class Packager:
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)

    def _hash_file(self, filepath: Path) -> str:
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
        
    def _create_deterministic_zip(self, source_dir: Path, output_zip: Path):
        """Creates a zip archive with normalized timestamps to ensure deterministic hashing."""
        # Fixed timestamp: 1980-01-01 00:00:00 (Minimum valid DOS timestamp for ZIP)
        fixed_time = (1980, 1, 1, 0, 0, 0)
        
        all_files = []
        for root, _, files in os.walk(source_dir):
            for f in files:
                all_files.append(Path(root) / f)
                
        # Sort lexically to ensure order of addition to zip is deterministic
        all_files.sort()
        
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filepath in all_files:
                rel_path = filepath.relative_to(source_dir).as_posix()
                
                # Create ZipInfo with fixed timestamp
                zinfo = zipfile.ZipInfo(filename=rel_path, date_time=fixed_time)
                zinfo.compress_type = zipfile.ZIP_DEFLATED
                
                # Normalize line endings to ensure deterministic file content across OS
                with open(filepath, 'rb') as f:
                    content = f.read()
                    
                # Normalize CRLF -> LF for text files, heuristically assuming mostly text 
                # (Or strictly for all files for strict determinism, which is fine for our compiler)
                content = content.replace(b'\r\n', b'\n')
                
                zipf.writestr(zinfo, content)

    def bundle(self, project_id: str, planning_report: dict) -> DeploymentManifest:
        project_dir = self.workspace_root / project_id
        dist_dir = self.workspace_root.parent / "dist" / project_id
        dist_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Compute Deterministic Workspace Hash
        workspace_hash = compute_deterministic_workspace_hash(project_dir)
        
        bundle_path = dist_dir / "deployment_bundle"
        zip_file = Path(f"{bundle_path}.zip")
        
        # 2. Create Deterministic Zip
        self._create_deterministic_zip(project_dir, zip_file)
        
        # 3. Compute deployment hash
        deployment_hash = self._hash_file(zip_file)
        
        # 4. Prepare Manifest
        manifest = DeploymentManifest(
            project_id=project_id,
            graph_hashes=planning_report.get("graph_hashes", {}),
            rule_engine_score=planning_report.get("graph_integrity_score", 0),
            plugin_versions={
                "FastApiMinimalGenerator": "1.0",
                "NextJsMinimalGenerator": "1.0"
            },
            build_status="SUCCESS",
            deployment_hash=deployment_hash,
            workspace_hash=workspace_hash
        )
        
        # Save Manifest
        manifest_path = dist_dir / "deployment_manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest.model_dump(mode="json"), f, indent=4)
            
        print(f"[Packager] Packaged {project_id} -> {zip_file}")
        print(f"[Packager] Workspace SHA-256: {workspace_hash}")
        print(f"[Packager] Deployment SHA-256: {deployment_hash}")
        
        return manifest
