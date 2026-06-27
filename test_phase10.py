import os
import sys
import json
import subprocess
from pathlib import Path

# Fix pythonpath
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_phase10():
    print("--- Phase 10 Control Plane Test ---")
    
    spec_path = "test_spec_phase10.json"
    spec_data = {
        "project_id": "test_phase10_001",
        "name": "Phase 10 API",
        "description": "Testing the Phase 10 CLI Control Plane",
        "pages": ["Dashboard"],
        "components": ["Header", "Footer"]
    }
    
    with open(spec_path, "w") as f:
        json.dump(spec_data, f)
        
    try:
        # 1. Test CLI Validate
        print("\n[Test 1] CLI Validation Execution")
        result_val = subprocess.run([sys.executable, "genesis_engine/cli/main.py", "validate", spec_path], capture_output=True, text=True)
        print(result_val.stdout)
        if result_val.returncode != 0:
            print(f"[ERROR] CLI Validate Failed: {result_val.stderr}")
            return
            
        # 2. Test CLI Run (Full Pipeline)
        print("\n[Test 2] CLI Run Execution")
        result_run = subprocess.run([sys.executable, "genesis_engine/cli/main.py", "run", spec_path], capture_output=True, text=True)
        print(result_run.stdout)
        if result_run.returncode != 0:
            print(f"[ERROR] CLI Run Failed: {result_run.stderr}")
            return
            
        # 3. Test Telemetry Output
        print("\n[Test 3] Telemetry Validation")
        trace_file = Path(f"workspace/test_phase10_001/execution_trace.json")
        if not trace_file.exists():
            print("[ERROR] Telemetry trace file missing!")
            return
            
        with open(trace_file, "r") as f:
            trace = json.load(f)
            events = trace.get("events", [])
            print(f"   Found {len(events)} telemetry events.")
            if len(events) < 4:
                print("[ERROR] Not enough telemetry events logged.")
                return
                
        print("\n[SUCCESS] All Phase 10 Control Plane tests passed successfully!")
        
    finally:
        if os.path.exists(spec_path):
            os.remove(spec_path)

if __name__ == "__main__":
    test_phase10()
