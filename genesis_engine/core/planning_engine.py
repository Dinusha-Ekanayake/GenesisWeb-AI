import time
from ..interfaces.modules import Planner
from ..models.spec import ProjectSpecification
from ..models.outputs import GenerationPlan, ArchitectureDecisionRecord, PlanningReport, RuleSeverity
from ..models.ir import GenesisIR, GenesisEntity
from ..utils.workspace_adapter import WorkspaceAdapter
from ..rules.registry import RuleRegistry
from ..rules.base import RuleContext
from ..rules.standards.db_rules import RequirePrimaryKeyRule
from ..rules.standards.api_rules import SecureMutationsRule
from ..rules.standards.cross_graph_rules import ApiToDatabaseMappingRule, OrphanPageRule
from ..utils.scoring import calculate_graph_integrity_score

from ..pipeline.planners.feature_planner import FeaturePlanner
from ..pipeline.planners.page_planner import PagePlanner
from ..pipeline.planners.component_planner import ComponentPlanner
from ..pipeline.planners.api_planner import ApiPlanner
from ..pipeline.planners.database_planner import DatabasePlanner
from ..pipeline.planners.dependency_planner import DependencyPlanner
from ..pipeline.planners.generation_builder import GenerationBuilder

class EventEmitter:
    def emit(self, event_name: str, payload: dict = None):
        print(f"[EVENT] {event_name}: {payload or {}}")

class PlanningEngine(Planner):
    def __init__(self, workspace_root: str):
        self.workspace_adapter = WorkspaceAdapter(workspace_root)
        self.events = EventEmitter()
        
        self.feature_planner = FeaturePlanner()
        self.page_planner = PagePlanner()
        self.component_planner = ComponentPlanner()
        self.api_planner = ApiPlanner()
        self.database_planner = DatabasePlanner()
        self.dependency_planner = DependencyPlanner()
        self.generation_builder = GenerationBuilder()
        
        self.rule_registry = RuleRegistry()
        self.rule_registry.register(RequirePrimaryKeyRule())
        self.rule_registry.register(SecureMutationsRule())
        self.rule_registry.register(ApiToDatabaseMappingRule())
        self.rule_registry.register(OrphanPageRule())
        
    def _convert_spec_to_ir(self, spec: ProjectSpecification) -> GenesisIR:
        entities = [
            GenesisEntity(name=e, attributes={}, relations=[])
            for e in spec.entities
        ]
        return GenesisIR(
            project_id=spec.project_id,
            entities=entities,
            roles=[],
            workflows=[],
            features=spec.pages,
            components=spec.components,
            api_routes=spec.api_routes,
            auth_requirements=spec.auth_requirements,
            roles_permissions=spec.roles_permissions,
            navigation_structure=spec.navigation_structure,
            app_type=spec.app_type,
            target_users=spec.target_users,
        )
        
    def validate_blueprint(self, spec: ProjectSpecification):
        """
        Pre-Generation Guarantee: Executes planning and Rule Engine validation
        but stops before GenerationBuilder and disk flush.
        """
        start_time = time.time()
        self.events.emit("PlanningStarted", {"project_id": spec.project_id})
        
        adr = ArchitectureDecisionRecord()
        
        ir = self._convert_spec_to_ir(spec)
        feature_graph = self.feature_planner.plan(ir, adr)
        page_graph = self.page_planner.plan(feature_graph, ir, adr)
        component_graph = self.component_planner.plan(page_graph, ir, adr)
        api_graph = self.api_planner.plan(feature_graph, page_graph, ir, adr)
        database_graph = self.database_planner.plan(ir, adr)
        dependency_graph = self.dependency_planner.plan(feature_graph, page_graph, api_graph, database_graph, adr)
        
        rule_context = RuleContext(
            feature_graph=feature_graph,
            page_graph=page_graph,
            component_graph=component_graph,
            api_graph=api_graph,
            database_graph=database_graph,
            dependency_graph=dependency_graph,
        )
        
        traces = self.rule_registry.evaluate_all(rule_context)
        
        errors = [t for t in traces if t.status == RuleSeverity.ERROR]
        warnings = [t for t in traces if t.status == RuleSeverity.WARNING]
        
        score = calculate_graph_integrity_score(traces)
        
        coverage = self.rule_registry.analyze_coverage([
            "FeatureGraph", "PageGraph", "ComponentGraph", "ApiGraph", "DatabaseGraph", "DependencyGraph"
        ])
        
        report = PlanningReport(
            total_features=len(feature_graph.features),
            total_pages=len(page_graph.pages),
            total_apis=len(api_graph.endpoints),
            total_entities=len(database_graph.tables),
            total_components=len(component_graph.components),
            dependency_count=len(dependency_graph.dependencies),
            planning_duration_ms=int((time.time() - start_time) * 1000),
            rule_validation_status="FAIL" if errors else "PASS",
            total_errors=len(errors),
            total_warnings=len(warnings),
            failed_rules=[],
            rule_trace=traces,
            graph_integrity_score=score,
            rule_coverage=coverage,
            graph_hashes={
                "FeatureGraph": feature_graph.compute_hash(),
                "PageGraph": page_graph.compute_hash(),
                "ComponentGraph": component_graph.compute_hash(),
                "ApiGraph": api_graph.compute_hash(),
                "DatabaseGraph": database_graph.compute_hash(),
                "DependencyGraph": dependency_graph.compute_hash(),
            }
        )
        
        if errors:
            error_details = "\n".join([f"- [{e.rule_id}] {e.affected_nodes} - {e._message}" for e in errors]) if hasattr(errors[0], '_message') else "\n".join([f"- [{e.rule_id}] {e.affected_nodes}" for e in errors])
            # wait, RuleExecutionTrace doesn't have a 'message' field. It only has rule_id, status, affected_nodes.
            # I should just print what we have, or maybe I should check the rules to see why they are failing.
            raise ValueError(f"Strict Mode Validation Failed: {len(errors)} ERROR(s) detected. Score: {score}\nDetails:\n" + "\n".join([f"- [{e.rule_id}] {e.affected_nodes}" for e in errors]))
            
        return report, feature_graph, page_graph, component_graph, api_graph, database_graph, dependency_graph, adr, ir

    def plan(self, spec: ProjectSpecification) -> GenerationPlan:
        report, feature_graph, page_graph, component_graph, api_graph, database_graph, dependency_graph, adr, ir = self.validate_blueprint(spec)
        
        generation_plan = self.generation_builder.build(
            feature_graph, page_graph, component_graph, 
            api_graph, database_graph, dependency_graph, adr
        )
        
        artifacts = {
            "genesis_ir.json": ir,
            "architecture_decisions.json": adr,
            "planning_report.json": report,
            "feature_graph.json": feature_graph,
            "page_graph.json": page_graph,
            "component_graph.json": component_graph,
            "api_graph.json": api_graph,
            "database_graph.json": database_graph,
            "dependency_graph.json": dependency_graph,
            "generation_plan.json": generation_plan
        }
        self.workspace_adapter.flush_transaction(spec.project_id, artifacts)
        
        return generation_plan
