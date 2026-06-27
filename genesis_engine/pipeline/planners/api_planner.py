from ...models.ir import GenesisIR
from ...models.graphs import FeatureGraph, PageGraph, ApiGraph, ApiEndpointNode, GraphNodeMetadata
from ...models.outputs import ArchitectureDecisionRecord, ArchitectureDecision

class ApiPlanner:
    def plan(self, feature_graph: FeatureGraph, page_graph: PageGraph, ir: GenesisIR, adr: ArchitectureDecisionRecord) -> ApiGraph:
        endpoints = []
        
        # For each feature, create a RESTful endpoint mapping
        for feature in feature_graph.features:
            base_path = f"/api/v1/{feature.name.lower().replace(' ', '_')}"
            
            methods = ["GET", "POST"]
            for method in methods:
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
                        depends_on=[feature.id]
                    )
                ))
                
                adr.decisions.append(ArchitectureDecision(
                    decision=f"Generated {method} endpoint for {feature.name}",
                    reason="Standard REST architecture",
                    source=feature.id,
                    affected_graphs=["ApiGraph"]
                ))
                
        # Structural validation: Conflict paths
        paths_methods = [(e.path, e.method) for e in endpoints]
        if len(paths_methods) != len(set(paths_methods)):
            raise ValueError("ApiPlanner Validation Error: Conflicting API routes detected.")
            
        return ApiGraph(endpoints=endpoints)
