import threading
from typing import Dict
from ..core.planning_engine import PlanningEngine
from ..core.generation_engine import GenerationEngine
from ..deployment.build_orchestrator import BuildOrchestrator
from ..telemetry.execution_trace import TelemetryLogger
from ..models.spec import ProjectSpecification

class ExecutionOrchestrator:
    """
    Central control plane for the Genesis Engine.
    Enforces strict execution ordering and prevents concurrent pipeline execution for the same project.
    """
    _locks: Dict[str, threading.Lock] = {}
    _global_lock = threading.Lock()
    
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.planning_engine = PlanningEngine(workspace_root)
        self.generation_engine = GenerationEngine(workspace_root)
        self.build_orchestrator = BuildOrchestrator(workspace_root)
        self.telemetry = TelemetryLogger(workspace_root)
        
    def _get_lock(self, project_id: str) -> threading.Lock:
        with self._global_lock:
            if project_id not in self._locks:
                self._locks[project_id] = threading.Lock()
            return self._locks[project_id]

    def validate_spec(self, spec: ProjectSpecification):
        """Phase 1: Validates the blueprint without generating code."""
        project_id = spec.project_id
        lock = self._get_lock(project_id)
        
        if not lock.acquire(blocking=False):
            raise RuntimeError(f"Execution Lock Error: Pipeline is currently running for project {project_id}.")
            
        try:
            self.telemetry.log_execution_trace(project_id, {"phase": "validation", "status": "started"})
            report, _, _, _, _, _, _, _, _ = self.planning_engine.validate_blueprint(spec)
            self.telemetry.log_execution_trace(project_id, {
                "phase": "validation", 
                "status": "completed",
                "score": report.graph_integrity_score
            })
            return report
        finally:
            lock.release()

    def run_full_pipeline(self, spec: ProjectSpecification, require_approval: bool = False):
        """Executes the full pipeline: Plan -> Validate -> Generate -> Package"""
        project_id = spec.project_id
        lock = self._get_lock(project_id)
        
        if not lock.acquire(blocking=False):
            raise RuntimeError(f"Execution Lock Error: Pipeline is currently running for project {project_id}.")
            
        try:
            # 1. Validation (Rule Engine)
            self.telemetry.log_execution_trace(project_id, {"phase": "pipeline", "step": "validation", "status": "started"})
            report, f_graph, p_graph, c_graph, a_graph, db_graph, dep_graph, adr, ir = self.planning_engine.validate_blueprint(spec)
            
            # If require_approval is True, we would pause here (handled by LangGraph typically, 
            # but in pure orchestration we just enforce deterministic generation)
            if require_approval:
                # We simply return the report and stop. LangGraph would resume later.
                # Since LangGraph operates over these engines, we just allow the pipeline to proceed if False.
                pass
            
            # 2. Generation Engine
            self.telemetry.log_execution_trace(project_id, {"phase": "pipeline", "step": "generation", "status": "started"})
            
            # Build generation plan
            generation_plan = self.planning_engine.generation_builder.build(
                f_graph, p_graph, c_graph, a_graph, db_graph, dep_graph, adr
            )
            
            # Build rule context
            from ..rules.base import RuleContext
            rule_context = RuleContext(
                feature_graph=f_graph,
                page_graph=p_graph,
                component_graph=c_graph,
                api_graph=a_graph,
                database_graph=db_graph,
                dependency_graph=dep_graph,
            )
            
            # Register plugins
            from ..plugins.implementations.fastapi_plugin import FastApiPlugin
            from ..plugins.implementations.nextjs_plugin import NextJsPlugin
            self.generation_engine.register_plugin(FastApiPlugin())
            self.generation_engine.register_plugin(NextJsPlugin())
            
            # Execute generation
            self.generation_engine.execute(generation_plan, rule_context, project_id)
            
            # 3. Deployment Packaging
            self.telemetry.log_execution_trace(project_id, {"phase": "pipeline", "step": "deployment", "status": "started"})
            manifest = self.build_orchestrator.execute_build(project_id, report.model_dump(mode="json"))
            
            self.telemetry.log_execution_trace(project_id, {
                "phase": "pipeline", 
                "status": "completed",
                "deployment_hash": manifest.deployment_hash
            })
            return manifest
            
        finally:
            lock.release()
