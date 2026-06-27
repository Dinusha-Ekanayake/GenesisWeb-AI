from ...models.ir import GenesisIR
from ...models.graphs import FeatureGraph, PageGraph, PageNode, GraphNodeMetadata
from ...models.outputs import ArchitectureDecisionRecord, ArchitectureDecision

class PagePlanner:
    def plan(self, feature_graph: FeatureGraph, ir: GenesisIR, adr: ArchitectureDecisionRecord) -> PageGraph:
        pages = []
        for feature in feature_graph.features:
            # Deterministic mapping: simple feature to page route logic
            route = f"/{feature.name.lower().replace(' ', '-')}"
            node_id = f"page.{route.replace('/', '').replace('-', '_')}"
            
            metadata = GraphNodeMetadata(
                created_by="PagePlanner",
                derived_from=[feature.id],
                depends_on=[feature.id]
            )
            
            pages.append(PageNode(
                id=node_id,
                name=f"{feature.name} Page",
                route=route,
                layout="DashboardLayout",
                components=[],
                metadata=metadata
            ))
            
            adr.decisions.append(ArchitectureDecision(
                decision=f"Created page for {feature.name}",
                reason="Feature requires user interface",
                source=feature.id,
                affected_graphs=["PageGraph"]
            ))
            
        # Lightweight Structural Validation: Duplicate routes
        routes = [p.route for p in pages]
        if len(routes) != len(set(routes)):
            raise ValueError("PagePlanner Validation Error: Duplicate routes detected.")
            
        return PageGraph(pages=pages)
