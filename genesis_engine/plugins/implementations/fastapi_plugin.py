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

    def _generate_config_files(self) -> List[FileArtifact]:
        configs = []

        configs.append(FileArtifact(
            path="backend/requirements.txt",
            content="""fastapi>=0.110.0
uvicorn[standard]>=0.29.0
pydantic>=2.0.0
""",
        ))

        init_code = ""
        is_valid, err_msg = PythonValidator.validate(init_code, filename="backend/app/__init__.py")
        if not is_valid:
            raise ValueError(f"Generation Error (FastApiMinimalGenerator): {err_msg}")
        configs.append(FileArtifact(path="backend/app/__init__.py", content=init_code))

        configs.append(FileArtifact(
            path="backend/.env.example",
            content="""DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key-here
""",
        ))

        return configs

    def generate(self, context: RuleContext) -> List[FileArtifact]:
        artifacts = self._generate_config_files()
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
