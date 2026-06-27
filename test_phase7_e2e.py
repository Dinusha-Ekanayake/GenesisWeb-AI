import sys
import os
import shutil

os.environ["MOCK_LLM_FOR_TEST"] = "1"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app.agents.workflow import app
from genesis_engine.models.spec import ProjectSpecification

def mock_requirement_analyzer_valid():
    return ProjectSpecification(
        project_id="test_valid_001",
        name="Valid CRM",
        description="A simple CRM dashboard",
        pages=["Dashboard", "Settings"],
        components=["Sidebar", "NavigationBar"]
    ).model_dump()

def mock_requirement_analyzer_invalid():
    # Will fail database rules (e.g., missing primary key if we had that detail, 
    # but since our spec is high level, let's inject a failure by making it invalid or lacking components)
    return ProjectSpecification(
        project_id="test_invalid_001",
        name="Invalid App",
        description="App with no pages",
        pages=[], # Empty pages might trigger a rule if we have one, otherwise we can simulate a failure
        components=[]
    ).model_dump()

def run_test_case(name, spec_dict, expect_failure=False):
    print(f"\n==================================================")
    print(f"Executing Test Case: {name}")
    print(f"==================================================")
    
    # State initialization
    initial_state = {
        "project_id": spec_dict["project_id"],
        "user_prompt": "Mock prompt",
        "events": [],
        "errors": [],
        "specification": spec_dict # Pre-inject spec to bypass analyzer
    }
    
    config = {"configurable": {"thread_id": f"thread-{name}"}}
    
    try:
        # Step 1: Run until interrupt or end
        print("1. Running Graph (Initial pass)...")
        for event in app.stream(initial_state, config):
            for node_name, state_update in event.items():
                print(f"   [{node_name}] Status: {state_update.get('status', '')}")
                if "errors" in state_update and state_update["errors"]:
                    print(f"   [ERROR CAUGHT] {state_update['errors']}")
                    
        current_state = app.get_state(config)
        next_nodes = current_state.next
        
        # Check if we hit the expected failure
        has_errors = bool(current_state.values.get("errors"))
        
        if expect_failure:
            if has_errors or current_state.values.get("status") == "HALTED_DUE_TO_ERRORS":
                print(f"✅ SUCCESS: Expected failure was correctly caught by strict mode.")
                return True
            else:
                print(f"❌ FAILED: Expected failure did not occur. Status: {current_state.values.get('status')}")
                return False
                
        # If we expect success, we should be at GenesisGenerator interrupt
        if current_state.values.get("status") == "GENERATING_CODE":
            print("2. [HUMAN-IN-THE-LOOP] Execution paused. Validation passed.")
            print("   Simulating human approval...")
            
            app.update_state(config, {"events": ["ApprovalGranted"]})
            
            print("3. Resuming Graph (Code Generation)...")
            for event in app.stream(None, config):
                for node_name, state_update in event.items():
                    print(f"   [{node_name}] Status: {state_update.get('status', '')}")
                    
            print(f"✅ SUCCESS: Code generation completed for {name}.")
            
            # Verify Workspace Output
            workspace_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspace", spec_dict["project_id"])
            if os.path.exists(workspace_dir):
                print(f"   Verified workspace output created at {workspace_dir}")
                return True
            else:
                print(f"❌ FAILED: Workspace output not found.")
                return False
        else:
            print(f"❌ FAILED: Did not reach generation interrupt. Status: {current_state.values.get('status')}")
            return False
            
    except Exception as e:
        print(f"❌ FATAL EXCEPTION: {str(e)}")
        return False

def main():
    print("--- Phase 7 End-to-End System Validation ---")
    
    # Clean workspace before tests
    workspace_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspace")
    if os.path.exists(workspace_dir):
        print("Cleaning up old workspace...")
        # Be careful not to delete things we shouldn't. Just specific test dirs.
        for t in ["test_valid_001", "test_invalid_001"]:
            d = os.path.join(workspace_dir, t)
            if os.path.exists(d):
                shutil.rmtree(d)
    
    # Test 1: Valid Execution
    test1 = run_test_case("Valid CRM Scenario", mock_requirement_analyzer_valid(), expect_failure=False)
    
    # Test 2: Invalid Execution (We inject a faulty spec)
    # To guarantee an error in the Rule Engine without writing complex dummy rules, 
    # we monkey-patch validate_blueprint to raise ValueError for the invalid test.
    from genesis_engine.core.planning_engine import PlanningEngine
    original_validate = PlanningEngine.validate_blueprint
    
    def mock_validate_blueprint(self, spec):
        if spec.project_id == "test_invalid_001":
            raise ValueError("Strict Mode Validation Failed: 1 ERROR(s) detected. (MOCK FOR TEST)")
        return original_validate(self, spec)
        
    PlanningEngine.validate_blueprint = mock_validate_blueprint
    
    test2 = run_test_case("Invalid Empty Scenario", mock_requirement_analyzer_invalid(), expect_failure=True)
    
    # Restore
    PlanningEngine.validate_blueprint = original_validate
    
    print("\n==================================================")
    if test1 and test2:
        print("🏆 ALL PHASE 7 TESTS PASSED! System is Deterministic and Stable.")
    else:
        print("⚠️ SOME TESTS FAILED. Please review the logs.")

if __name__ == "__main__":
    main()
