from ...interfaces.plugin import GenerationPlugin
from ...models.outputs import FileArtifact
from ...rules.base import RuleContext
from ..validators.python_validator import PythonValidator
from typing import List

class FastApiPlugin(GenerationPlugin):
    @property
    def name(self): return "FastApiMinimalGenerator"
    @property
    def target_framework(self): return "fastapi"
    
    def generate(self, context: RuleContext) -> List[FileArtifact]:
        artifacts = []
        if not context.api_graph: return artifacts
        
        code = ["from fastapi import FastAPI\n\napp = FastAPI()\n"]
        
        for endpoint in context.api_graph.endpoints:
            func_name = endpoint.name.lower().replace(" ", "_")
            method = endpoint.method.lower()
            code.append(f"@app.{method}('{endpoint.path}')")
            code.append(f"def {func_name}():")
            code.append(f"    return {{'message': '{endpoint.name} generated deterministically'}}")
            code.append("")
            
        final_code = "\n".join(code)
        
        is_valid, err_msg = PythonValidator.validate(final_code, filename="backend/app/main.py")
        if not is_valid:
            raise ValueError(f"Generation Error (FastApiMinimalGenerator): {err_msg}")
            
        artifacts.append(FileArtifact(
            path="backend/app/main.py",
            content=final_code
        ))
        
        return artifacts
