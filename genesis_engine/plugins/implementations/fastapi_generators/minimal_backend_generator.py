from typing import List
from ....models.outputs import FileArtifact
from ...validators.python_validator import PythonValidator


def generate_minimal_backend(api_graph) -> List[FileArtifact]:
    if not api_graph:
        return []
    code = ["from fastapi import FastAPI\n\napp = FastAPI()\n"]
    seen: set = set()
    for endpoint in api_graph.endpoints:
        method = endpoint.method.lower()
        path_part = (
            endpoint.path.replace("/api/v1", "")
            .replace("/", "_").replace("{", "").replace("}", "")
            .strip("_")
        )
        base = f"{method}_{path_part}" if path_part else method
        func_name, n = base, 1
        while func_name in seen:
            func_name, n = f"{base}_{n}", n + 1
        seen.add(func_name)
        code.append(f"@app.{method}('{endpoint.path}')")
        code.append(f"def {func_name}():")
        code.append(f"    return {{'message': '{endpoint.name} generated deterministically'}}")
        code.append("")
    final_code = "\n".join(code)
    is_valid, err_msg = PythonValidator.validate(final_code, filename="backend/app/main.py")
    if not is_valid:
        raise ValueError(f"Generation Error (FastApiMinimalGenerator): {err_msg}")
    return [FileArtifact(path="backend/app/main.py", content=final_code)]
