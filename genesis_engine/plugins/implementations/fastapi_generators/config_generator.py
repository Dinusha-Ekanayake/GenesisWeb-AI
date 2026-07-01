from typing import List
from ....models.outputs import FileArtifact
from ...validators.python_validator import PythonValidator


def generate_config_files() -> List[FileArtifact]:
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
