from ...models.graphs import DependencyGraph, DependencyNode, GraphNodeMetadata
from ...models.outputs import ArchitectureDecisionRecord, ArchitectureDecision

class DependencyPlanner:
    def plan(self, feature_graph, page_graph, api_graph, database_graph, adr: ArchitectureDecisionRecord) -> DependencyGraph:
        dependencies = []
        
        if len(api_graph.endpoints) > 0:
            dependencies.append(DependencyNode(
                id="dep_fastapi",
                name="fastapi",
                version=">=0.100.0",
                metadata=GraphNodeMetadata(created_by="DependencyPlanner", derived_from=["ApiGraph"])
            ))
            
        if len(database_graph.tables) > 0:
            dependencies.append(DependencyNode(
                id="dep_sqlalchemy",
                name="sqlalchemy",
                version=">=2.0.0",
                metadata=GraphNodeMetadata(created_by="DependencyPlanner", derived_from=["DatabaseGraph"])
            ))
            
        return DependencyGraph(dependencies=dependencies)
