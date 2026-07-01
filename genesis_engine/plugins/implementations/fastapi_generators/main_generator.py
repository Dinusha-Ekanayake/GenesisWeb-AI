from typing import List
from ....models.outputs import FileArtifact
from ...validators.python_validator import PythonValidator
from .schemas_generator import generate_schemas_code
from .database_generator import generate_database_code
from .models_generator import generate_models_code, pluralize
from .router_generator import generate_router_code


def generate_entity_main_code(plurals: List[str]) -> str:
    lines = [
        "from fastapi import FastAPI",
        "from .database import engine, Base",
        "from . import models",
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


def generate_entity_backend(entities) -> List[FileArtifact]:
    artifacts = []
    plurals = [pluralize(t.name) for t in entities]

    schemas_code = generate_schemas_code(entities)
    is_valid, err = PythonValidator.validate(schemas_code, "backend/app/schemas.py")
    if not is_valid:
        raise ValueError(f"Generation Error (FastApiMinimalGenerator): {err}")
    artifacts.append(FileArtifact(path="backend/app/schemas.py", content=schemas_code))

    database_code = generate_database_code()
    is_valid, err = PythonValidator.validate(database_code, "backend/app/database.py")
    if not is_valid:
        raise ValueError(f"Generation Error (FastApiMinimalGenerator): {err}")
    artifacts.append(FileArtifact(path="backend/app/database.py", content=database_code))

    models_code = generate_models_code(entities)
    is_valid, err = PythonValidator.validate(models_code, "backend/app/models.py")
    if not is_valid:
        raise ValueError(f"Generation Error (FastApiMinimalGenerator): {err}")
    artifacts.append(FileArtifact(path="backend/app/models.py", content=models_code))

    artifacts.append(FileArtifact(path="backend/app/routers/__init__.py", content=""))

    for table, plural in zip(entities, plurals):
        router_code = generate_router_code(table, plural)
        is_valid, err = PythonValidator.validate(router_code, f"backend/app/routers/{plural}.py")
        if not is_valid:
            raise ValueError(f"Generation Error (FastApiMinimalGenerator): {err}")
        artifacts.append(FileArtifact(path=f"backend/app/routers/{plural}.py", content=router_code))

    main_code = generate_entity_main_code(plurals)
    is_valid, err = PythonValidator.validate(main_code, "backend/app/main.py")
    if not is_valid:
        raise ValueError(f"Generation Error (FastApiMinimalGenerator): {err}")
    artifacts.append(FileArtifact(path="backend/app/main.py", content=main_code))

    return artifacts
