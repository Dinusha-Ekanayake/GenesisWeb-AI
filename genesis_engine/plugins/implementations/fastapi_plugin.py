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
    def _sa_type(raw: str) -> str:
        base = raw.rstrip("?")
        return {"string": "String", "integer": "Integer", "number": "Float", "boolean": "Boolean"}.get(base, "String")

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
sqlalchemy>=2.0.0
""",
        ))

        init_code = ""
        is_valid, err_msg = PythonValidator.validate(init_code, filename="backend/app/__init__.py")
        if not is_valid:
            raise ValueError(f"Generation Error (FastApiMinimalGenerator): {err_msg}")
        configs.append(FileArtifact(path="backend/app/__init__.py", content=init_code))

        configs.append(FileArtifact(
            path="backend/.env.example",
            content="""DATABASE_URL=sqlite:///./genesis_app.db
SECRET_KEY=your-secret-key-here
""",
        ))

        return configs

    def _generate_database_code(self) -> str:
        return "\n".join([
            "from sqlalchemy import create_engine",
            "from sqlalchemy.orm import sessionmaker, declarative_base",
            "",
            "",
            'DATABASE_URL = "sqlite:///./genesis_app.db"',
            'engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})',
            "SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)",
            "Base = declarative_base()",
            "",
            "",
            "def get_db():",
            "    db = SessionLocal()",
            "    try:",
            "        yield db",
            "    finally:",
            "        db.close()",
            "",
        ])

    def _generate_models_code(self, entities) -> str:
        lines = [
            "from sqlalchemy import Column, Integer, String, Float, Boolean",
            "from .database import Base",
            "",
            "",
        ]
        for table in entities:
            name = table.name
            plural = self._pluralize(name)
            columns = table.columns or {}
            lines += [f"class {name}(Base):", f'    __tablename__ = "{plural}"', ""]
            lines.append("    id = Column(Integer, primary_key=True, index=True)")
            if columns:
                for field_name, raw_type in columns.items():
                    sa_type = self._sa_type(raw_type)
                    nullable = raw_type.endswith("?")
                    lines.append(f"    {field_name} = Column({sa_type}, nullable={nullable})")
            else:
                lines.append("    name = Column(String, nullable=False)")
            lines.append("")
        return "\n".join(lines)

    def _generate_schemas_code(self, entities) -> str:
        lines = ["from pydantic import BaseModel, ConfigDict", "from typing import Optional", ""]
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

            # Response model — flat with from_attributes for SQLAlchemy ORM compatibility.
            # Must be flat (not inheriting {name}Base) to avoid Pydantic v2 required-after-optional
            # error when a required child field follows optional parent fields.
            response_fields = [
                "    model_config = ConfigDict(from_attributes=True)",
                "    id: int",
            ] + base_fields
            lines += ["", "", f"class {name}(BaseModel):"] + response_fields
            lines.append("")

        return "\n".join(lines)

    def _generate_router_code(self, table, plural: str) -> str:
        name = table.name
        lower = table.name.lower()
        model_alias = f"{name}Model"
        lines = [
            "from typing import List",
            "from fastapi import APIRouter, Depends, HTTPException",
            "from sqlalchemy.orm import Session",
            f"from ..schemas import {name}, {name}Create",
            "from ..database import get_db",
            f"from ..models import {name} as {model_alias}",
            "",
            "",
            f'router = APIRouter(prefix="/{plural}", tags=["{plural}"])',
            "",
            "",
            f'@router.get("/", response_model=List[{name}])',
            f"def list_{plural}(db: Session = Depends(get_db)):",
            f"    return db.query({model_alias}).all()",
            "",
            "",
            f'@router.get("/{{item_id}}", response_model={name})',
            f"def get_{lower}(item_id: int, db: Session = Depends(get_db)):",
            f"    record = db.query({model_alias}).filter({model_alias}.id == item_id).first()",
            "    if not record:",
            f'        raise HTTPException(status_code=404, detail="{lower} not found")',
            "    return record",
            "",
            "",
            f'@router.post("/", response_model={name}, status_code=201)',
            f"def create_{lower}(item: {name}Create, db: Session = Depends(get_db)):",
            f"    record = {model_alias}(**item.model_dump())",
            "    db.add(record)",
            "    db.commit()",
            "    db.refresh(record)",
            "    return record",
            "",
            "",
            f'@router.put("/{{item_id}}", response_model={name})',
            f"def update_{lower}(item_id: int, item: {name}Create, db: Session = Depends(get_db)):",
            f"    record = db.query({model_alias}).filter({model_alias}.id == item_id).first()",
            "    if not record:",
            f'        raise HTTPException(status_code=404, detail="{lower} not found")',
            "    for k, v in item.model_dump().items():",
            "        setattr(record, k, v)",
            "    db.commit()",
            "    db.refresh(record)",
            "    return record",
            "",
            "",
            f'@router.delete("/{{item_id}}", status_code=204)',
            f"def delete_{lower}(item_id: int, db: Session = Depends(get_db)):",
            f"    record = db.query({model_alias}).filter({model_alias}.id == item_id).first()",
            "    if not record:",
            f'        raise HTTPException(status_code=404, detail="{lower} not found")',
            "    db.delete(record)",
            "    db.commit()",
            "",
        ]
        return "\n".join(lines)

    def _generate_entity_main_code(self, plurals: List[str]) -> str:
        lines = [
            "from fastapi import FastAPI",
            "from .database import engine, Base",
            "from . import models",  # ensures ORM classes are registered in Base.metadata before create_all
        ]
        for plural in plurals:
            lines.append(f"from .routers.{plural} import router as {plural}_router")
        lines += [
            "",
            "",
            "Base.metadata.create_all(bind=engine)",
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

        database_code = self._generate_database_code()
        is_valid, err = PythonValidator.validate(database_code, "backend/app/database.py")
        if not is_valid:
            raise ValueError(f"Generation Error (FastApiMinimalGenerator): {err}")
        artifacts.append(FileArtifact(path="backend/app/database.py", content=database_code))

        models_code = self._generate_models_code(entities)
        is_valid, err = PythonValidator.validate(models_code, "backend/app/models.py")
        if not is_valid:
            raise ValueError(f"Generation Error (FastApiMinimalGenerator): {err}")
        artifacts.append(FileArtifact(path="backend/app/models.py", content=models_code))

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

    def generate(self, context: RuleContext) -> List[FileArtifact]:
        artifacts = self._generate_config_files()
        entities = context.database_graph.tables if context.database_graph else []
        if entities:
            artifacts.extend(self._generate_entity_backend(entities))
        else:
            artifacts.extend(self._generate_minimal_backend(context.api_graph))
        return artifacts
