import asyncio
from genesis_engine.core.orchestrator import ExecutionOrchestrator
from genesis_engine.models.spec import ProjectSpecification


class CompilerService:
    """
    Service layer that mediates between the async FastAPI controller and the
    synchronous deterministic compiler pipeline.

    The compiler pipeline (PlanningEngine → GenerationEngine → BuildOrchestrator)
    is inherently synchronous to preserve deterministic batch execution. This service
    wraps that pipeline in asyncio.to_thread so controllers remain purely async
    without embedding threading concerns directly.
    """

    def __init__(self, orchestrator: ExecutionOrchestrator):
        self._orchestrator = orchestrator

    async def run_pipeline(self, spec: ProjectSpecification):
        """Execute the full compilation pipeline asynchronously."""
        return await asyncio.to_thread(self._orchestrator.run_full_pipeline, spec)

    async def run_deploy(self, project_id: str, planning_report: dict):
        """Execute the deployment packaging pipeline asynchronously."""
        return await asyncio.to_thread(
            self._orchestrator.build_orchestrator.execute_build,
            project_id,
            planning_report,
        )

    async def validate(self, spec: ProjectSpecification):
        """Validate a spec without generating code, asynchronously."""
        return await asyncio.to_thread(self._orchestrator.validate_spec, spec)
