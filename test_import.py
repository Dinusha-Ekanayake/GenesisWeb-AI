import sys
import traceback

sys.path.append("e:\\Projects\\GenesisWeb-AI")

try:
    from backend.app.api import genesis_controller
    print("SUCCESS")
except Exception as e:
    print("FAILED")
    traceback.print_exc()
