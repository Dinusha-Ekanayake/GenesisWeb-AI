from ...models.outputs import GenerationPlan, GenerationStep, ArchitectureDecisionRecord, ArchitectureDecision

class GenerationBuilder:
    def build(self, feature_graph, page_graph, component_graph, api_graph, database_graph, dependency_graph, adr: ArchitectureDecisionRecord) -> GenerationPlan:
        steps = []
        
        # Build DAG steps based on graphs
        steps.append(GenerationStep(
            id="gen_database",
            description="Generate SQLAlchemy Models",
            target_plugin="FastApiSqlAlchemyPlugin",
            dependencies=[],
            execution_priority=1,
            estimated_outputs=["models.py"],
            target_workspace_path="backend/app/models"
        ))
        
        steps.append(GenerationStep(
            id="gen_api",
            description="Generate FastAPI Endpoints",
            target_plugin="FastApiPlugin",
            dependencies=["gen_database"],
            execution_priority=2,
            estimated_outputs=["endpoints.py"],
            target_workspace_path="backend/app/api"
        ))
        
        steps.append(GenerationStep(
            id="gen_components",
            description="Generate React Macro Components",
            target_plugin="NextJsAppRouterPlugin",
            dependencies=["gen_api"],
            execution_priority=3,
            estimated_outputs=["components.tsx"],
            target_workspace_path="frontend/src/components"
        ))
        
        adr.decisions.append(ArchitectureDecision(
            decision="Constructed GenerationPlan DAG",
            reason="Ensures backend is generated before frontend consumes it",
            source="GenerationBuilder",
            affected_graphs=[]
        ))
        
        return GenerationPlan(steps=steps)
