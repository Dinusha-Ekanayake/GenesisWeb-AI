from typing import List
from ....models.outputs import FileArtifact
from ...validators.tsx_validator import TsxValidator


def generate_components(component_graph) -> List[FileArtifact]:
    if not component_graph:
        return []
    artifacts = []
    spec_components = [
        c for c in component_graph.components
        if c.metadata.created_by == "SpecComponent"
    ]
    for comp in spec_components:
        path = f"frontend/components/{comp.name}.tsx"
        code = "\n".join([
            f"export default function {comp.name}() {{",
            f"    return (",
            f"        <div>",
            f"            <span>{comp.name}</span>",
            f"        </div>",
            f"    );",
            f"}}",
        ])
        is_valid, err_msg = TsxValidator.validate(code, filename=path)
        if not is_valid:
            raise ValueError(f"Generation Error (NextJsMinimalGenerator): {err_msg}")
        artifacts.append(FileArtifact(path=path, content=code))
    return artifacts
