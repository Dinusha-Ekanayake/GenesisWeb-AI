import sys
import os

# Add project root to python path to resolve modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from genesis_engine.models.spec import ProjectSpecification
from genesis_engine.core.planning_engine import PlanningEngine
from genesis_engine.core.generation_engine import GenerationEngine
from genesis_engine.plugins.implementations.fastapi_plugin import FastApiPlugin
from genesis_engine.plugins.implementations.nextjs_plugin import NextJsPlugin

def run():
    print("--- Genesis Engine: Phase 5 End-to-End Test ---")
    workspace_root = os.path.join(os.path.dirname(__file__), "workspace")
    
    os.makedirs(workspace_root, exist_ok=True)
    
    spec = ProjectSpecification(
        project_id="test_e2e_001",
        name="Test Shop",
        description="A full end-to-end compiler test",
        pages=["Dashboard", "Products", "Checkout"],
        components=["NavigationBar", "Footer"]
    )
    
    print(f"\n1. Initializing PlanningEngine (Workspace: {workspace_root})")
    planning_engine = PlanningEngine(workspace_root=workspace_root)
    
    print("\n2. Executing Strict Blueprint Validation (Phase 3 Rules)")
    try:
        report, feature_graph, page_graph, component_graph, api_graph, database_graph, dependency_graph, adr, ir = planning_engine.validate_blueprint(spec)
        print(f"   Validation Status: {report.rule_validation_status}")
        print(f"   Integrity Score: {report.graph_integrity_score}")
        print(f"   Errors: {report.total_errors}, Warnings: {report.total_warnings}")
    except Exception as e:
        print(f"\n[FATAL ERROR] PlanningEngine failed validation: {e}")
        return
        
    print("\n3. Generating Final Execution Plan")
    plan = planning_engine.plan(spec)
    print(f"   Generation Steps: {len(plan.steps)}")
    
    print("\n4. Initializing GenerationEngine")
    generation_engine = GenerationEngine(workspace_root=workspace_root)
    generation_engine.register_plugin(FastApiPlugin())
    generation_engine.register_plugin(NextJsPlugin())
    
    from genesis_engine.rules.base import RuleContext
    context = RuleContext(
        feature_graph=feature_graph,
        page_graph=page_graph,
        component_graph=component_graph,
        api_graph=api_graph,
        database_graph=database_graph,
        dependency_graph=dependency_graph,
        report=report
    )
    
    print("\n5. Executing Generation Plugins (Phase 4)")
    try:
        generation_engine.execute(plan, context, spec.project_id)
        print("   Generation completed successfully.")
    except Exception as e:
        print(f"\n[FATAL ERROR] GenerationEngine failed: {e}")
        return
        
    print("\n--- Test Completed Successfully! ---")
    print(f"Check outputs in {os.path.join(workspace_root, spec.project_id)}")

if __name__ == "__main__":
    run()
