import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

from genesis_engine.models.spec import ProjectSpecification
from genesis_engine.core.planning_engine import PlanningEngine
from genesis_engine.core.generation_engine import GenerationEngine
from genesis_engine.plugins.implementations.fastapi_plugin import FastApiPlugin
from genesis_engine.plugins.implementations.nextjs_plugin import NextJsPlugin
from genesis_engine.rules.base import RuleContext
from ...core.workspace import WorkspaceManager
from ..state import ProjectState

def genesis_generator_node(state: ProjectState) -> dict:
    project_id = state.get("project_id", "")
    print(f"[GenesisGenerator] Generating code for Project {project_id}...")
    
    spec_dict = state.get("specification")
    if not spec_dict:
        return {"errors": ["GenesisGenerator failed: No ProjectSpecification found."]}
        
    spec = ProjectSpecification(**spec_dict)
    
    workspace_root = str(WorkspaceManager.get_workspace_root()) if hasattr(WorkspaceManager, 'get_workspace_root') else os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")), "workspace")
    
    # We must rebuild the graphs via PlanningEngine.validate_blueprint 
    # since we cannot store full Python objects in the SQLite memory easily without serialization overhead.
    planning_engine = PlanningEngine(workspace_root=workspace_root)
    
    try:
        report, feature_graph, page_graph, component_graph, api_graph, database_graph, dependency_graph, adr, ir = planning_engine.validate_blueprint(spec)
        plan = planning_engine.plan(spec)
        
        generation_engine = GenerationEngine(workspace_root=workspace_root)
        generation_engine.register_plugin(FastApiPlugin())
        generation_engine.register_plugin(NextJsPlugin())
        
        context = RuleContext(
            feature_graph=feature_graph,
            page_graph=page_graph,
            component_graph=component_graph,
            api_graph=api_graph,
            database_graph=database_graph,
            dependency_graph=dependency_graph,
            report=report
        )
        
        generation_engine.execute(plan, context, spec.project_id)
        
        return {
            "events": ["GenerationCompleted"],
            "status": "GENERATION_COMPLETE"
        }
        
    except Exception as e:
        return {"errors": [f"GenesisGenerator failed: {str(e)}"]}
