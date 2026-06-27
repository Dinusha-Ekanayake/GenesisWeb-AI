import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

class TelemetryLogger:
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        
    def log_execution_trace(self, project_id: str, trace_data: Dict[str, Any]):
        project_dir = self.workspace_root / project_id
        project_dir.mkdir(parents=True, exist_ok=True)
        
        trace_file = project_dir / "execution_trace.json"
        
        # Append logic or fresh write
        existing_trace = {}
        if trace_file.exists():
            try:
                with open(trace_file, "r") as f:
                    existing_trace = json.load(f)
            except Exception:
                pass
                
        events = existing_trace.get("events", [])
        
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "timestamp_ms": int(time.time() * 1000),
            **trace_data
        }
        events.append(event)
        
        full_trace = {
            "project_id": project_id,
            "last_updated": datetime.utcnow().isoformat(),
            "events": events
        }
        
        with open(trace_file, "w") as f:
            json.dump(full_trace, f, indent=4)
