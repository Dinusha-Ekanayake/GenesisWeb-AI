from ...interfaces.plugin import GenerationPlugin
from ...models.outputs import FileArtifact
from ...rules.base import RuleContext
from typing import List

class NextJsPlugin(GenerationPlugin):
    @property
    def name(self): return "NextJsMinimalGenerator"
    @property
    def target_framework(self): return "nextjs"
    
    def generate(self, context: RuleContext) -> List[FileArtifact]:
        artifacts = []
        if not context.page_graph: return artifacts
        
        for page in context.page_graph.pages:
            clean_route = page.route.strip("/")
            path = f"frontend/app/{clean_route}/page.tsx" if clean_route else "frontend/app/page.tsx"
            
            comp_name = page.name.replace(" ", "")
            
            code = [
                f"export default function {comp_name}() {{",
                f"    return (",
                f"        <div>",
                f"            <h1>{page.name}</h1>",
                f"            <p>Generated deterministically by Genesis Engine.</p>",
                f"        </div>",
                f"    );",
                f"}}"
            ]
            
            artifacts.append(FileArtifact(
                path=path,
                content="\n".join(code)
            ))
            
        return artifacts
