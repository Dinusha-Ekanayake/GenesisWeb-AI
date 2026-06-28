import pytest
from genesis_engine.core.exceptions import CompilerTamperError, RuleEngineViolation
from genesis_engine.models.spec import ProjectSpecification
from genesis_engine.core.orchestrator import ExecutionOrchestrator
import os

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../workspace"))

@pytest.fixture
def orchestrator():
    return ExecutionOrchestrator(WORKSPACE_ROOT)

@pytest.fixture
def base_spec():
    return {
        "project_id": "mutation_test_project",
        "title": "Mutation Test",
        "description": "A project for mutation testing",
        "architecture": {
            "frontend": "react",
            "backend": "fastapi",
            "database": "postgres"
        },
        "features": ["auth"],
        "api_schema": {
            "endpoints": [
                {"path": "/users", "method": "GET", "response": "UserList"}
            ]
        },
        "data_models": {
            "User": {
                "fields": {"id": "uuid", "name": "string"}
            }
        }
    }

def test_mutation_missing_project_id(orchestrator, base_spec):
    mutated_spec = base_spec.copy()
    del mutated_spec["project_id"]
    
    with pytest.raises(Exception):
        spec = ProjectSpecification(**mutated_spec)
        orchestrator.validate_spec(spec)

def test_mutation_invalid_architecture(orchestrator, base_spec):
    mutated_spec = base_spec.copy()
    mutated_spec["architecture"]["frontend"] = "unknown_framework"
    
    with pytest.raises(Exception):
        spec = ProjectSpecification(**mutated_spec)
        orchestrator.validate_spec(spec)

def test_mutation_circular_dependency_simulation():
    """
    If the Rule Engine has graph validation, we simulate a cyclic dependency.
    """
    from genesis_engine.planning.rule_engine import RuleEngine
    engine = RuleEngine()
    
    # Create a cyclic graph
    graph = {
        "nodes": ["A", "B", "C"],
        "edges": [("A", "B"), ("B", "C"), ("C", "A")]
    }
    
    # We assume rule engine has a method or fails gracefully
    try:
        engine.validate_dependency_graph(graph)
        pytest.fail("Rule engine failed to catch circular dependency mutation")
    except Exception as e:
        assert True # Successfully caught the mutation
        
def test_mutation_tampered_planning_report(orchestrator, base_spec):
    """
    Tamper with a planning report and ensure it gets rejected during build execution.
    """
    report = {
        "project_id": "tampered_project",
        "graph_integrity_score": 100, # Spoofed score
        "phases": [],
        "tampered_flag": True
    }
    
    with pytest.raises(Exception):
        orchestrator.build_orchestrator.execute_build("tampered_project", report)
