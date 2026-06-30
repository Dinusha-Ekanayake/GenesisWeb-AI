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

    @staticmethod
    def _py_type(raw: str):
        """Map internal type string (with optional '?' suffix) to (python_type, is_optional)."""
        optional = raw.endswith("?")
        base = raw.rstrip("?")
        py = {"string": "str", "integer": "int", "number": "float", "boolean": "bool"}.get(base, "str")
        return py, optional

    @staticmethod
    def _pluralize(name: str) -> str:
        lower = name.lower()
        if lower.endswith('y') and len(lower) > 1 and lower[-2] not in 'aeiou':
            return lower[:-1] + 'ies'
        if lower.endswith('s') or lower.endswith('x') or lower.endswith('z'):
            return lower + 'es'
        return lower + 's'

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

    def _generate_schemas_code(self, entities) -> str:
        lines = ["from pydantic import BaseModel", "from typing import Optional", ""]
        for table in entities:
            name = table.name
            columns = table.columns or {}

            # Required fields before optional (Pydantic v2 ordering rule)
            required_cols = [(k, v) for k, v in columns.items() if not v.endswith("?")]
            optional_cols = [(k, v) for k, v in columns.items() if v.endswith("?")]
            ordered = required_cols + optional_cols

            def _field_decls(cols):
                if not cols:
                    return ['    name: str = ""']
                out = []
                for field_name, raw_type in cols:
                    py_type, optional = self._py_type(raw_type)
                    if optional:
                        out.append(f"    {field_name}: Optional[{py_type}] = None")
                    else:
                        out.append(f"    {field_name}: {py_type}")
                return out

            base_fields = _field_decls(ordered)

            # Base model — all domain fields
            lines += ["", f"class {name}Base(BaseModel):"] + base_fields

            # Create model — inherits Base (used for POST/PUT request bodies)
            lines += ["", "", f"class {name}Create({name}Base):", "    pass"]

            # Response model — flat (avoids Pydantic v2 required-after-optional error
            # that occurs when a required child field follows optional parent fields)
            response_fields = ["    id: int"] + base_fields
            lines += ["", "", f"class {name}(BaseModel):"] + response_fields
            lines.append("")

        return "\n".join(lines)

    def _generate_storage_code(self, entities) -> str:
        lines = [
            "from typing import Dict, Any",
            "",
            "",
            "_stores: Dict[str, Dict[int, Any]] = {",
        ]
        for t in entities:
            lines.append(f'    "{t.name.lower()}": {{}},')
        lines += [
            "}",
            "",
            "_counters: Dict[str, int] = {",
        ]
        for t in entities:
            lines.append(f'    "{t.name.lower()}": 0,')
        lines += [
            "}",
            "",
            "",
            "def get_store(entity: str) -> Dict[int, Any]:",
            "    return _stores[entity]",
            "",
            "",
            "def next_id(entity: str) -> int:",
            "    _counters[entity] += 1",
            "    return _counters[entity]",
            "",
        ]
        return "\n".join(lines)

    def _generate_router_code(self, table, plural: str) -> str:
        name = table.name
        lower = table.name.lower()
        lines = [
            "from typing import List",
            "from fastapi import APIRouter, HTTPException",
            f"from ..schemas import {name}, {name}Create",
            "from ..storage import get_store, next_id",
            "",
            "",
            f'router = APIRouter(prefix="/{plural}", tags=["{plural}"])',
            "",
            "",
            f'@router.get("/", response_model=List[{name}])',
            f"def list_{plural}():",
            f'    return list(get_store("{lower}").values())',
            "",
            "",
            f'@router.get("/{{item_id}}", response_model={name})',
            f"def get_{lower}(item_id: int):",
            f'    store = get_store("{lower}")',
            "    if item_id not in store:",
            f'        raise HTTPException(status_code=404, detail="{lower} not found")',
            "    return store[item_id]",
            "",
            "",
            f'@router.post("/", response_model={name}, status_code=201)',
            f"def create_{lower}(item: {name}Create):",
            f'    store = get_store("{lower}")',
            f'    new_id = next_id("{lower}")',
            f"    record = {name}(id=new_id, **item.model_dump())",
            "    store[new_id] = record",
            "    return record",
            "",
            "",
            f'@router.put("/{{item_id}}", response_model={name})',
            f"def update_{lower}(item_id: int, item: {name}Create):",
            f'    store = get_store("{lower}")',
            "    if item_id not in store:",
            f'        raise HTTPException(status_code=404, detail="{lower} not found")',
            f"    record = {name}(id=item_id, **item.model_dump())",
            "    store[item_id] = record",
            "    return record",
            "",
            "",
            f'@router.delete("/{{item_id}}", status_code=204)',
            f"def delete_{lower}(item_id: int):",
            f'    store = get_store("{lower}")',
            "    if item_id not in store:",
            f'        raise HTTPException(status_code=404, detail="{lower} not found")',
            "    del store[item_id]",
            "",
        ]
        return "\n".join(lines)

    def _generate_entity_main_code(self, plurals: List[str]) -> str:
        lines = ["from fastapi import FastAPI"]
        for plural in plurals:
            lines.append(f"from .routers.{plural} import router as {plural}_router")
        lines += [
            "",
            "",
            'app = FastAPI(title="Genesis App")',
            "",
        ]
        for plural in plurals:
            lines.append(f'app.include_router({plural}_router, prefix="/api/v1")')
        lines += [
            "",
            "",
            '@app.get("/health")',
            "def health():",
            '    return {"status": "ok"}',
            "",
        ]
        return "\n".join(lines)

    def _generate_entity_backend(self, entities) -> List[FileArtifact]:
        artifacts = []
        plurals = [self._pluralize(t.name) for t in entities]

        schemas_code = self._generate_schemas_code(entities)
        is_valid, err = PythonValidator.validate(schemas_code, "backend/app/schemas.py")
        if not is_valid:
            raise ValueError(f"Generation Error (FastApiMinimalGenerator): {err}")
        artifacts.append(FileArtifact(path="backend/app/schemas.py", content=schemas_code))

        storage_code = self._generate_storage_code(entities)
        is_valid, err = PythonValidator.validate(storage_code, "backend/app/storage.py")
        if not is_valid:
            raise ValueError(f"Generation Error (FastApiMinimalGenerator): {err}")
        artifacts.append(FileArtifact(path="backend/app/storage.py", content=storage_code))

        artifacts.append(FileArtifact(path="backend/app/routers/__init__.py", content=""))

        for table, plural in zip(entities, plurals):
            router_code = self._generate_router_code(table, plural)
            is_valid, err = PythonValidator.validate(router_code, f"backend/app/routers/{plural}.py")
            if not is_valid:
                raise ValueError(f"Generation Error (FastApiMinimalGenerator): {err}")
            artifacts.append(FileArtifact(path=f"backend/app/routers/{plural}.py", content=router_code))

        main_code = self._generate_entity_main_code(plurals)
        is_valid, err = PythonValidator.validate(main_code, "backend/app/main.py")
        if not is_valid:
            raise ValueError(f"Generation Error (FastApiMinimalGenerator): {err}")
        artifacts.append(FileArtifact(path="backend/app/main.py", content=main_code))

        return artifacts

    def _generate_minimal_backend(self, api_graph) -> List[FileArtifact]:
        if not api_graph:
            return []
        code = ["from fastapi import FastAPI\n\napp = FastAPI()\n"]
        for endpoint in api_graph.endpoints:
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
        return [FileArtifact(path="backend/app/main.py", content=final_code)]

    def generate(self, context: RuleContext) -> List[FileArtifact]:
        artifacts = self._generate_config_files()
        entities = context.database_graph.tables if context.database_graph else []
        if entities:
            artifacts.extend(self._generate_entity_backend(entities))
        else:
            artifacts.extend(self._generate_minimal_backend(context.api_graph))
        return artifacts
