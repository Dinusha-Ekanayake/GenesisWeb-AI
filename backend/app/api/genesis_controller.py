import os
import sys
import json
from pathlib import Path

# Ensure the root Genesis Engine directory is on the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from fastapi import APIRouter, HTTPException, Depends
from genesis_engine.core.orchestrator import ExecutionOrchestrator
from genesis_engine.models.spec import ProjectSpecification

router = APIRouter(prefix="/genesis", tags=["Genesis Control Plane"])

# Initialize a singleton orchestrator for the API
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../workspace"))
orchestrator = ExecutionOrchestrator(WORKSPACE_ROOT)

@router.post("/parse")
def parse_prompt(prompt: str):
    # Optional LLM adapter hook. Currently stubbed to enforce deterministic compiler only.
    return {"status": "Not Implemented", "message": "Use direct spec submission for now."}

@router.post("/plan")
def plan_spec(spec: ProjectSpecification):
    try:
        report = orchestrator.validate_spec(spec)
        return {"status": "SUCCESS", "report": report}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/validate")
def validate_spec(spec: ProjectSpecification):
    try:
        report = orchestrator.validate_spec(spec)
        return {"status": "SUCCESS", "score": report.graph_integrity_score}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/generate")
def generate_project(spec: ProjectSpecification):
    try:
        manifest = orchestrator.run_full_pipeline(spec)
        return {"status": "SUCCESS", "manifest": manifest}
    except RuntimeError as re:
        raise HTTPException(status_code=423, detail=str(re)) # Locked
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/deploy/{project_id}")
def deploy_project(project_id: str):
    try:
        report_path = Path(WORKSPACE_ROOT) / project_id / "artifacts" / "planning_report.json"
        if not report_path.exists():
            raise HTTPException(status_code=404, detail="Planning report not found. Compile first.")
            
        with open(report_path, "r") as f:
            report = json.load(f)
            
        manifest = orchestrator.build_orchestrator.execute_build(project_id, report)
        return {"status": "SUCCESS", "manifest": manifest}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
