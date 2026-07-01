from typing import List
from ....models.outputs import FileArtifact
from ...validators.tsx_validator import TsxValidator


def generate_static_pages(page_graph, entity_routes: set) -> List[FileArtifact]:
    if not page_graph:
        return []
    artifacts = []
    for page in page_graph.pages:
        clean_route = page.route.strip("/")
        if clean_route in entity_routes:
            continue
        path = f"frontend/app/{clean_route}/page.tsx" if clean_route else "frontend/app/page.tsx"
        comp_name = page.name.replace(" ", "")
        code = "\n".join([
            f"export default function {comp_name}() {{",
            f"    return (",
            f"        <div>",
            f"            <h1>{page.name}</h1>",
            f"            <p>Generated deterministically by Genesis Engine.</p>",
            f"        </div>",
            f"    );",
            f"}}",
        ])
        is_valid, err_msg = TsxValidator.validate(code, filename=path)
        if not is_valid:
            raise ValueError(f"Generation Error (NextJsMinimalGenerator): {err_msg}")
        artifacts.append(FileArtifact(path=path, content=code))
    return artifacts
