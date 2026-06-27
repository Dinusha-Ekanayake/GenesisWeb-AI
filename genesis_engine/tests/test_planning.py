import pytest
from genesis_engine.models.spec import ProjectSpecification
from genesis_engine.core.planning_engine import PlanningEngine
from genesis_engine.models.outputs import GenerationPlan

def test_deterministic_planning_pipeline(tmp_path):
    # tmp_path is a built-in pytest fixture for temporary directories
    
    spec = ProjectSpecification(
        project_id="test_uuid_123",
        name="Test Ecommerce",
        description="A deterministic test spec",
        pages=["Dashboard", "Products"],
        components=["AuthModal"]
    )
    
    engine = PlanningEngine(workspace_root=str(tmp_path))
    
    # Run the deterministic plan
    generation_plan = engine.plan(spec)
    
    assert isinstance(generation_plan, GenerationPlan)
    assert len(generation_plan.steps) == 3 # DB, API, Components
    assert generation_plan.steps[0].id == "gen_database"
    
    # Check that disk flush occurred correctly
    artifacts_dir = tmp_path / "test_uuid_123" / "artifacts"
    assert artifacts_dir.exists()
    
    # Verify graph files were written
    expected_files = [
        "genesis_ir.json",
        "architecture_decisions.json",
        "feature_graph.json",
        "page_graph.json",
        "component_graph.json",
        "api_graph.json",
        "database_graph.json",
        "dependency_graph.json",
        "generation_plan.json"
    ]
    
    for f in expected_files:
        assert (artifacts_dir / f).exists(), f"File {f} is missing."

def test_page_planner_duplicate_validation():
    from genesis_engine.models.ir import GenesisIR
    from genesis_engine.models.graphs import FeatureGraph, FeatureNode, GraphNodeMetadata
    from genesis_engine.pipeline.planners.page_planner import PagePlanner
    from genesis_engine.models.outputs import ArchitectureDecisionRecord
    
    planner = PagePlanner()
    ir = GenesisIR(project_id="test")
    adr = ArchitectureDecisionRecord()
    
    # Intentionally create duplicate features to trigger structural validation
    feature_graph = FeatureGraph(features=[
        FeatureNode(id="f1", name="Home", requirements=[], metadata=GraphNodeMetadata(created_by="test")),
        FeatureNode(id="f2", name="Home", requirements=[], metadata=GraphNodeMetadata(created_by="test"))
    ])
    
    with pytest.raises(ValueError, match="Duplicate routes detected"):
        planner.plan(feature_graph, ir, adr)
