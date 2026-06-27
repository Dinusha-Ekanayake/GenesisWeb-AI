import sys
import os

os.environ["MOCK_LLM_FOR_TEST"] = "1"

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app.agents.workflow import app

def run():
    print("--- LangGraph Orchestration: Phase 6 E2E Test ---")
    
    # State initialization
    initial_state = {
        "project_id": "langgraph_test_001",
        "user_prompt": "Build a simple CRM dashboard with a customer list page and a settings page. Include a sidebar component.",
        "events": [],
        "errors": []
    }
    
    config = {"configurable": {"thread_id": "thread-1"}}
    
    print("1. Starting Workflow...")
    try:
        for event in app.stream(initial_state, config):
            for node_name, state_update in event.items():
                print(f"[{node_name}] Events: {state_update.get('events', [])} | Status: {state_update.get('status', '')}")
                if "errors" in state_update and state_update["errors"]:
                    print(f"[FATAL ERROR] {state_update['errors']}")
    except Exception as e:
        print(f"Execution Error: {e}")
                
    current_state = app.get_state(config)
    next_node = current_state.next
    
    if "GenesisGenerator" in next_node:
        print("\n2. [HUMAN IN THE LOOP] Execution paused before Generation.")
        print("   Rule Engine Validation Passed or warnings acknowledged.")
        print("   Simulating Human Approval...")
        
        # We manually update state to trigger the edge logic. 
        # But actually GenesisGenerator is just the next node. If we continue with stream(None), it will execute it.
        # But ProjectManager routes based on events, so we need to inject ApprovalGranted just in case it loops back.
        app.update_state(config, {"events": ["ApprovalGranted"]})
        
        print("\n3. Resuming Workflow for Generation...")
        for event in app.stream(None, config):
            for node_name, state_update in event.items():
                print(f"[{node_name}] Events: {state_update.get('events', [])} | Status: {state_update.get('status', '')}")
                
    print("\n--- Test Completed ---")

if __name__ == "__main__":
    run()
