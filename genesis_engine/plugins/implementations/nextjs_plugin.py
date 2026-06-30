from ...interfaces.plugin import GenerationPlugin
from ...models.outputs import FileArtifact
from ...rules.base import RuleContext
from ..validators.tsx_validator import TsxValidator
from typing import List

class NextJsPlugin(GenerationPlugin):
    @property
    def name(self): return "NextJsMinimalGenerator"
    @property
    def target_framework(self): return "nextjs"
    
    def generate(self, context: RuleContext) -> List[FileArtifact]:
        artifacts = []

        # Pages → frontend/app/{route}/page.tsx
        if context.page_graph:
            for page in context.page_graph.pages:
                clean_route = page.route.strip("/")
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

        # Spec-declared components → frontend/components/{Name}.tsx
        if context.component_graph:
            spec_components = [
                c for c in context.component_graph.components
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
