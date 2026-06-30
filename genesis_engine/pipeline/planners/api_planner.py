from ...models.ir import GenesisIR
from ...models.graphs import FeatureGraph, PageGraph, ApiGraph, ApiEndpointNode, GraphNodeMetadata
from ...models.outputs import ArchitectureDecisionRecord, ArchitectureDecision

_VALID_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}
_MUTATION_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
_API_PREFIX = "/api/v1"


def _pluralize(name: str) -> str:
    lower = name.lower()
    if lower.endswith("y") and len(lower) > 1 and lower[-2] not in "aeiou":
        return lower[:-1] + "ies"
    if lower.endswith("s") or lower.endswith("x") or lower.endswith("z"):
        return lower + "es"
    return lower + "s"


class ApiPlanner:
    def _entity_crud_endpoints(self, entities, adr) -> list:
        """Generate 5 CRUD endpoints per entity from ir.entities."""
        endpoints = []
        for entity in entities:
            plural = _pluralize(entity.name)
            col_path = f"{_API_PREFIX}/{plural}"
            item_path = f"{_API_PREFIX}/{plural}/{{item_id}}"

            crud = [
                ("GET",    col_path,  False),
                ("POST",   col_path,  True),
                ("GET",    item_path, False),
                ("PUT",    item_path, True),
                ("DELETE", item_path, True),
            ]

            for method, path, requires_auth in crud:
                suffix = ".item" if "{item_id}" in path else ""
                node_id = f"api.{method.lower()}.{plural}{suffix}"
                endpoints.append(ApiEndpointNode(
                    id=node_id,
                    name=f"{method} {entity.name}",
                    path=path,
                    method=method,
                    requires_auth=requires_auth,
                    target_entity=entity.name,
                    metadata=GraphNodeMetadata(
                        created_by="ApiPlanner",
                        derived_from=[f"ir.entity.{entity.name.lower()}"],
                        depends_on=[f"database.{entity.name.lower()}"],
                    ),
                ))

            adr.decisions.append(ArchitectureDecision(
                decision=f"Generated 5 CRUD endpoints for entity {entity.name} at {col_path}",
                reason="Entity-driven REST API from IR entities",
                source=f"ir.entity.{entity.name.lower()}",
                affected_graphs=["ApiGraph"],
            ))

        return endpoints

    def _api_routes_endpoints(self, api_routes, adr) -> list:
        """Parse approved ir.api_routes strings into endpoint nodes."""
        endpoints = []
        for route_str in api_routes:
            parts = route_str.strip().split(None, 1)
            if len(parts) != 2:
                continue
            method, path = parts[0].upper(), parts[1]
            if method not in _VALID_METHODS:
                continue
            if not path.startswith(_API_PREFIX):
                path = _API_PREFIX + ("" if path.startswith("/") else "/") + path
            path = path.replace("{id}", "{item_id}")
            node_id = f"api.{method.lower()}.{path.replace('/', '.').strip('.')}"
            endpoints.append(ApiEndpointNode(
                id=node_id,
                name=f"{method} {path}",
                path=path,
                method=method,
                requires_auth=(method in _MUTATION_METHODS),
                metadata=GraphNodeMetadata(
                    created_by="ApiPlanner",
                    derived_from=["ir.api_routes"],
                    depends_on=[],
                ),
            ))
            adr.decisions.append(ArchitectureDecision(
                decision=f"Parsed route {method} {path} from approved plan",
                reason="Plan-driven API from ir.api_routes",
                source="ir.api_routes",
                affected_graphs=["ApiGraph"],
            ))
        return endpoints

    def _page_derived_endpoints(self, feature_graph, adr) -> list:
        """Fallback: generate GET+POST stubs from feature/page names."""
        endpoints = []
        for feature in feature_graph.features:
            base_path = f"{_API_PREFIX}/{feature.name.lower().replace(' ', '_')}"
            for method in ["GET", "POST"]:
                node_id = f"api.{method.lower()}.{feature.name.lower().replace(' ', '_')}"
                endpoints.append(ApiEndpointNode(
                    id=node_id,
                    name=f"{method} {feature.name}",
                    path=base_path,
                    method=method,
                    requires_auth=(method in ["POST", "PUT", "DELETE"]),
                    metadata=GraphNodeMetadata(
                        created_by="ApiPlanner",
                        derived_from=[feature.id],
                        depends_on=[feature.id],
                    ),
                ))
                adr.decisions.append(ArchitectureDecision(
                    decision=f"Generated {method} endpoint for {feature.name}",
                    reason="Standard REST architecture",
                    source=feature.id,
                    affected_graphs=["ApiGraph"],
                ))
        return endpoints

    def plan(self, feature_graph: FeatureGraph, _page_graph: PageGraph, ir: GenesisIR, adr: ArchitectureDecisionRecord) -> ApiGraph:
        if ir.entities:
            endpoints = self._entity_crud_endpoints(ir.entities, adr)
        elif ir.api_routes:
            endpoints = self._api_routes_endpoints(ir.api_routes, adr)
        else:
            endpoints = self._page_derived_endpoints(feature_graph, adr)

        paths_methods = [(e.path, e.method) for e in endpoints]
        if len(paths_methods) != len(set(paths_methods)):
            raise ValueError("ApiPlanner Validation Error: Conflicting API routes detected.")

        return ApiGraph(endpoints=endpoints)
