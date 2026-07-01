from ...interfaces.plugin import GenerationPlugin
from ...models.outputs import FileArtifact
from ...rules.base import RuleContext
from typing import List
from .fastapi_generators.config_generator import generate_config_files
from .fastapi_generators.main_generator import generate_entity_backend
from .fastapi_generators.minimal_backend_generator import generate_minimal_backend


class FastApiPlugin(GenerationPlugin):
    @property
    def name(self): return "FastApiMinimalGenerator"
    @property
    def target_framework(self): return "fastapi"

    def generate(self, context: RuleContext) -> List[FileArtifact]:
        artifacts = generate_config_files()
        entities = context.database_graph.tables if context.database_graph else []
        if entities:
            artifacts.extend(generate_entity_backend(entities))
        else:
            artifacts.extend(generate_minimal_backend(context.api_graph))
        return artifacts
