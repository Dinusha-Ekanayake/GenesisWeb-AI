import os
import hashlib
from pathlib import Path

def compute_deterministic_workspace_hash(workspace_dir: str | Path, exclude_dirs: list[str] = None) -> str:
    """
    Computes a strictly deterministic SHA-256 hash of a workspace directory.
    - Lexically sorts all files
    - Reads in binary mode
    - Normalizes CRLF (\r\n) to LF (\n) in-memory before hashing
    """
    workspace_dir = Path(workspace_dir)
    if exclude_dirs is None:
        exclude_dirs = [".git", "node_modules", "__pycache__"]
        
    hasher = hashlib.sha256()
    
    # 1. Collect all files and sort them lexically
    all_files = []
    for root, dirs, files in os.walk(workspace_dir):
        # Filter excluded directories in-place
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            # Skip the lock file and execution trace to prevent hash recursion/drift
            if file in [".compiler_lock", "execution_trace.json"]:
                continue
            all_files.append(Path(root) / file)
            
    all_files.sort() # Critical: Lexical sort
    
    # 2. Process each file
    for filepath in all_files:
        # Hash the relative path so folder renames affect the hash
        rel_path = filepath.relative_to(workspace_dir).as_posix()
        hasher.update(rel_path.encode('utf-8'))
        
        with open(filepath, 'rb') as f:
            content = f.read()
            # Normalize line endings
            content = content.replace(b'\r\n', b'\n')
            hasher.update(content)
            
    return hasher.hexdigest()
