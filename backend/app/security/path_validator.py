import os
import re
from pathlib import Path
from backend.app.core.exceptions import WorkspaceSecurityError

class PathValidator:
    MAX_PREVIEW_SIZE_MB = 2.0
    
    # Common hidden folders/files to reject
    FORBIDDEN_NAMES = {
        ".env", ".git", ".compiler_lock", "__pycache__", 
        ".pytest_cache", ".next", "node_modules"
    }

    @staticmethod
    def validate_project_id(project_id: str) -> str:
        if not project_id:
            raise WorkspaceSecurityError("Project ID cannot be empty")
        if not re.match(r"^[a-zA-Z0-9_-]+$", project_id):
            raise WorkspaceSecurityError(f"Invalid project ID format: {project_id}")
        return project_id

    @staticmethod
    def validate_artifact_name(name: str) -> str:
        if not name:
            raise WorkspaceSecurityError("Artifact name cannot be empty")
        if not re.match(r"^[a-zA-Z0-9_.-]+$", name):
            raise WorkspaceSecurityError(f"Invalid artifact name format: {name}")
        return name

    @staticmethod
    def resolve_and_validate_path(base_dir: str | Path, requested_path: str | Path, 
                                  allow_hidden: bool = False, is_preview: bool = False) -> Path:
        base_dir_resolved = Path(base_dir).resolve()
        
        # Resolve symlinks and absolute path
        full_path = Path(base_dir_resolved / requested_path).resolve()
        
        # 1. Path Traversal check
        try:
            full_path.relative_to(base_dir_resolved)
        except ValueError:
            raise WorkspaceSecurityError("Path traversal attempt detected. Path escapes workspace.")
            
        if not full_path.exists():
            return full_path  # Let the caller handle FileNotFoundError if needed
            
        # 2. Symlink escape check
        requested_p = Path(base_dir_resolved) / requested_path
        if requested_p.is_symlink():
            if base_dir_resolved not in full_path.parents and base_dir_resolved != full_path:
                raise WorkspaceSecurityError("Symlink escapes workspace boundary.")

        # 3. Hidden File Protection
        if not allow_hidden:
            for part in full_path.relative_to(base_dir_resolved).parts:
                if part.startswith('.') and part not in {".env", ".git", ".compiler_lock", ".pytest_cache", ".next"}:
                    # Reject all dotfiles/directories
                    raise WorkspaceSecurityError(f"Access to hidden file/directory forbidden: {part}")
                if part in PathValidator.FORBIDDEN_NAMES:
                    raise WorkspaceSecurityError(f"Access to forbidden directory or file: {part}")

        # 4. Preview specific checks (Binary + Size)
        if is_preview and full_path.is_file():
            size_mb = full_path.stat().st_size / (1024 * 1024)
            if size_mb > PathValidator.MAX_PREVIEW_SIZE_MB:
                raise WorkspaceSecurityError(f"File too large for preview ({size_mb:.1f} MB > {PathValidator.MAX_PREVIEW_SIZE_MB} MB).")
                
            # Binary check
            if PathValidator._is_binary(full_path):
                raise WorkspaceSecurityError("Cannot preview binary files. Unsupported Media Type.", is_binary=True)
                
        return full_path

    @staticmethod
    def _is_binary(file_path: Path) -> bool:
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                if b'\0' in chunk:
                    return True
                chunk.decode('utf-8')
                return False
        except UnicodeDecodeError:
            return True
        except Exception:
            return False
