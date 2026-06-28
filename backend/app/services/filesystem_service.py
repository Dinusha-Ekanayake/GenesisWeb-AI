import json
import asyncio
from pathlib import Path
from typing import Any, List, Dict, Optional

class FileSystemService:
    """
    Dedicated asynchronous filesystem service wrapping blocking IO calls.
    Ensures the FastAPI event loop is never blocked by OS I/O operations.
    """
    
    @staticmethod
    async def read_json(path: Path) -> Any:
        def _read():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return await asyncio.to_thread(_read)
        
    @staticmethod
    async def write_json(path: Path, data: Any, indent: int = 2) -> None:
        def _write():
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=indent)
        return await asyncio.to_thread(_write)

    @staticmethod
    async def read_text(path: Path) -> str:
        def _read():
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return await asyncio.to_thread(_read)
        
    @staticmethod
    async def list_directory(path: Path) -> List[Path]:
        def _list():
            return list(path.iterdir())
        return await asyncio.to_thread(_list)

    @staticmethod
    async def exists(path: Path) -> bool:
        def _exists():
            return path.exists()
        return await asyncio.to_thread(_exists)

    @staticmethod
    async def is_file(path: Path) -> bool:
        def _is_file():
            return path.is_file()
        return await asyncio.to_thread(_is_file)

    @staticmethod
    async def is_dir(path: Path) -> bool:
        def _is_dir():
            return path.is_dir()
        return await asyncio.to_thread(_is_dir)
        
    @staticmethod
    async def get_ctime(path: Path) -> float:
        def _ctime():
            return path.stat().st_ctime
        return await asyncio.to_thread(_ctime)
        
    @staticmethod
    async def mkdir(path: Path, parents: bool = False, exist_ok: bool = False) -> None:
        def _mkdir():
            path.mkdir(parents=parents, exist_ok=exist_ok)
        return await asyncio.to_thread(_mkdir)
        
    @staticmethod
    async def build_project_tree(project_dir: Path, forbidden_names: set) -> List[Dict[str, Any]]:
        def _build_tree(dir_path: Path):
            tree = []
            for p in dir_path.iterdir():
                if p.name in forbidden_names:
                    continue
                if p.name.startswith('.') and p.name not in {".env", ".git", ".compiler_lock", ".pytest_cache", ".next"}:
                    pass 
                    
                item = {
                    "name": p.name,
                    "path": str(p.relative_to(project_dir)).replace("\\", "/"),
                    "is_dir": p.is_dir()
                }
                if p.is_dir():
                    item["children"] = _build_tree(p)
                tree.append(item)
            return sorted(tree, key=lambda x: (not x["is_dir"], x["name"]))
            
        return await asyncio.to_thread(_build_tree, project_dir)
