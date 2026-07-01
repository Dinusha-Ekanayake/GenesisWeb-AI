from ...interfaces.plugin import GenerationPlugin
from ...models.outputs import FileArtifact
from ...rules.base import RuleContext
from ..validators.tsx_validator import TsxValidator
from typing import List
from .nextjs_generators.config_generator import generate_config_files
from .nextjs_generators.api_client_generator import generate_api_lib_code
from .nextjs_generators.types_generator import generate_types_code, pluralize
from .nextjs_generators.entity_page_generator import generate_entity_page_code
from .nextjs_generators.static_page_generator import generate_static_pages
from .nextjs_generators.component_generator import generate_components


class NextJsPlugin(GenerationPlugin):
    @property
    def name(self): return "NextJsMinimalGenerator"
    @property
    def target_framework(self): return "nextjs"

    def generate(self, context: RuleContext) -> List[FileArtifact]:
        artifacts = generate_config_files()

        entities = context.database_graph.tables if context.database_graph else []
        entity_routes: set = set()

        if entities:
            artifacts.append(FileArtifact(
                path="frontend/lib/types.ts",
                content=generate_types_code(entities),
            ))
            artifacts.append(FileArtifact(
                path="frontend/lib/api.ts",
                content=generate_api_lib_code(),
            ))
            for table in entities:
                plural = pluralize(table.name)
                entity_routes.add(plural)
                path = f"frontend/app/{plural}/page.tsx"
                page_code = generate_entity_page_code(table, plural)
                is_valid, err_msg = TsxValidator.validate(page_code, filename=path)
                if not is_valid:
                    raise ValueError(f"Generation Error (NextJsMinimalGenerator): {err_msg}")
                artifacts.append(FileArtifact(path=path, content=page_code))

        artifacts.extend(generate_static_pages(context.page_graph, entity_routes))
        artifacts.extend(generate_components(context.component_graph))

        return artifacts
