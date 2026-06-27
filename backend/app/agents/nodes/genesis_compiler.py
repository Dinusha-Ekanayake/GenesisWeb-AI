import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from genesis_engine.models.spec import ProjectSpecification
from genesis_engine.core.planning_engine import PlanningEngine
from ...core.workspace import WorkspaceManager
from ..state import ProjectState

def genesis_compiler_node(state: ProjectState) -> dict:
    project_id = state.get("project_id", "")
    print(f"[GenesisCompiler] Validating ProjectSpecification for {project_id}...")
    
    spec_dict = state.get("specification")
    if not spec_dict:
        return {"errors": ["GenesisCompiler failed: No ProjectSpecification found in state."]}
    
    spec = ProjectSpecification(**spec_dict)
    
    workspace_root = str(WorkspaceManager.get_workspace_root()) if hasattr(WorkspaceManager, 'get_workspace_root') else os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")), "workspace")
    
    planning_engine = PlanningEngine(workspace_root=workspace_root)
    
    try:
        report, _, _, _, _, _, _, _, _ = planning_engine.validate_blueprint(spec)
        
        # Check warnings
        if report.total_warnings > 0:
            return {
                "planning_report": report.model_dump(),
                "events": ["ValidationWarning"],
                "status": "VALIDATION_WARNING"
            }
            
        return {
            "planning_report": report.model_dump(),
            "events": ["ValidationPassed"],
            "status": "VALIDATION_PASSED"
        }
        
    except ValueError as e:
        print(f"[GenesisCompiler] Strict Mode Exception Caught: {str(e)}")
        # Rule Engine emitted ERROR
        return {
            "errors": [f"Strict Validation Failed: {str(e)}"],
            "events": ["ValidationFailed"],
            "status": "VALIDATION_FAILED"
        }
    except Exception as e:
        return {"errors": [f"GenesisCompiler unexpected failure: {str(e)}"]}
