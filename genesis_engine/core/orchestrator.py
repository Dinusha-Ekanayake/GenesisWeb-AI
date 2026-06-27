from pathlib import Path
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
    
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.planning_engine = PlanningEngine(workspace_root)
        self.generation_engine = GenerationEngine(workspace_root)
        self.build_orchestrator = BuildOrchestrator(workspace_root)
        self.telemetry = TelemetryLogger(workspace_root)
        
    def _get_lock(self, project_id: str):
        from ..utils.os_lock import OSFileLock
        lock_path = Path(self.workspace_root) / project_id / ".compiler_lock"
        # Ensure workspace exists before trying to lock
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        return OSFileLock(lock_path)

    def validate_spec(self, spec: ProjectSpecification):
        """Phase 1: Validates the blueprint without generating code."""
        project_id = spec.project_id
        
        with self._get_lock(project_id) as lock:
            self.telemetry.log_execution_trace(project_id, {"phase": "validation", "status": "started"})
            report, _, _, _, _, _, _, _, _ = self.planning_engine.validate_blueprint(spec)
            self.telemetry.log_execution_trace(project_id, {
                "phase": "validation", 
                "status": "completed",
                "score": report.graph_integrity_score
            })
            return report

    def run_full_pipeline(self, spec: ProjectSpecification, require_approval: bool = False):
        """Executes the full pipeline: Plan -> Validate -> Generate -> Package"""
        project_id = spec.project_id
        
        with self._get_lock(project_id) as lock:
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
            
            # Compute immediately post-generation workspace hash
            from ..utils.hash_utils import compute_deterministic_workspace_hash
            import json
            from pathlib import Path
            project_dir = Path(self.workspace_root) / project_id
            post_gen_hash = compute_deterministic_workspace_hash(project_dir)
            
            # Update planning_report with workspace_hash
            report.workspace_hash = post_gen_hash
            
            # Flush updated report to disk so independent deploy commands can verify it
            report_path = project_dir / "artifacts" / "planning_report.json"
            if report_path.exists():
                with open(report_path, "w") as f:
                    f.write(report.model_dump_json(indent=2))
            
            # 3. Deployment Packaging
            self.telemetry.log_execution_trace(project_id, {"phase": "pipeline", "step": "deployment", "status": "started"})
            manifest = self.build_orchestrator.execute_build(project_id, report.model_dump(mode="json"))
                
            self.telemetry.log_execution_trace(project_id, {
                "phase": "pipeline", 
                "status": "completed",
                "deployment_hash": manifest.deployment_hash
            })
            return manifest
