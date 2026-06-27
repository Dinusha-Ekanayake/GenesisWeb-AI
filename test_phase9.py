import os
import sys

os.environ["MOCK_LLM_FOR_TEST"] = "1"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from genesis_engine.deployment.build_orchestrator import BuildOrchestrator
from genesis_engine.deployment.hooks import DeploymentHooks

def test_phase9():
    print("--- Phase 9 Deployment & Packaging Test ---")
    
    workspace_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspace")
    project_id = "test_valid_001"
    
    # Check if the Phase 7 test generated the workspace we need
    if not os.path.exists(os.path.join(workspace_root, project_id)):
        print(f"❌ Error: Workspace for {project_id} does not exist.")
        print("Please run `python test_phase7_e2e.py` first to generate the artifacts.")
        return
        
    # Mock backend and frontend folders if they are missing
    backend_dir = os.path.join(workspace_root, project_id, "backend")
    frontend_dir = os.path.join(workspace_root, project_id, "frontend")
    os.makedirs(backend_dir, exist_ok=True)
    os.makedirs(frontend_dir, exist_ok=True)
    
    with open(os.path.join(backend_dir, "requirements.txt"), "w") as f:
        f.write("fastapi\nuvicorn\n")
        
    orchestrator = BuildOrchestrator(workspace_root=workspace_root)
    
    # Mock planning report
    mock_report = {
        "graph_hashes": {"FeatureGraph": "abcd123"},
        "graph_integrity_score": 100
    }
    
    try:
        manifest = orchestrator.execute_build(project_id, mock_report)
        print("\n✅ Deployment Build Completed Successfully!")
        print(f"   Project ID: {manifest.project_id}")
        print(f"   Deployment Hash: {manifest.deployment_hash}")
        
        # Test hooks
        DeploymentHooks.push_to_github(manifest.project_id, "dummy/path")
        DeploymentHooks.push_to_docker_registry(manifest.project_id, "dummy/path")
        DeploymentHooks.trigger_live_deployment(manifest.project_id, manifest.deployment_hash)
        
    except Exception as e:
        print(f"❌ Build Failed: {e}")

if __name__ == "__main__":
    test_phase9()
