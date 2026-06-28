import os
import sys
import time
import json
import psutil
import datetime
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from genesis_engine.core.orchestrator import ExecutionOrchestrator
from genesis_engine.models.spec import ProjectSpecification

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../workspace"))
BENCHMARKS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../benchmarks/history"))

def run_benchmark():
    os.makedirs(BENCHMARKS_DIR, exist_ok=True)
    
    spec_data = {
        "project_id": f"benchmark_{int(time.time())}",
        "title": "Benchmark Project",
        "description": "Standard benchmark workload",
        "architecture": {
            "frontend": "react",
            "backend": "fastapi",
            "database": "postgres"
        },
        "features": ["auth", "payments"],
        "api_schema": {
            "endpoints": [
                {"path": "/users", "method": "GET", "response": "UserList"},
                {"path": "/payments", "method": "POST", "response": "PaymentStatus"}
            ]
        },
        "data_models": {
            "User": {"fields": {"id": "uuid", "name": "string"}},
            "Payment": {"fields": {"id": "uuid", "amount": "float"}}
        }
    }
    
    spec = ProjectSpecification(**spec_data)
    orchestrator = ExecutionOrchestrator(WORKSPACE_ROOT)
    
    process = psutil.Process(os.getpid())
    start_cpu = process.cpu_times()
    start_time = time.perf_counter()
    peak_memory = 0
    
    # We will simulate the capture by wrapping the orchestrator run
    # In a real deep integration, we'd hook into telemetry. For this script, we do an overall measure.
    
    # Track metrics
    t0 = time.perf_counter()
    report = orchestrator.validate_spec(spec)
    t1 = time.perf_counter()
    planning_time = t1 - t0
    peak_memory = max(peak_memory, process.memory_info().rss)
    
    t0 = time.perf_counter()
    manifest = orchestrator.build_orchestrator.execute_build(spec.project_id, report.model_dump())
    t2 = time.perf_counter()
    generation_time = t2 - t0
    peak_memory = max(peak_memory, process.memory_info().rss)
    
    end_time = time.perf_counter()
    end_cpu = process.cpu_times()
    
    total_time = end_time - start_time
    cpu_time = (end_cpu.user - start_cpu.user) + (end_cpu.system - start_cpu.system)
    
    # Count generated LOC and files
    project_dir = Path(WORKSPACE_ROOT) / spec.project_id
    generated_file_count = 0
    generated_loc = 0
    
    for f in project_dir.rglob("*"):
        if f.is_file():
            generated_file_count += 1
            try:
                with open(f, "r", encoding="utf-8") as file:
                    generated_loc += len(file.readlines())
            except Exception:
                pass
                
    bundle_size = 0
    bundle_path = project_dir / "exports" / "deployment_bundle.zip"
    if bundle_path.exists():
        bundle_size = bundle_path.stat().st_size
    
    metrics = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "project_id": spec.project_id,
        "metrics": {
            "planning_time_s": planning_time,
            "generation_time_s": generation_time,
            "total_compilation_time_s": total_time,
            "peak_memory_mb": peak_memory / (1024 * 1024),
            "cpu_time_s": cpu_time,
            "generated_file_count": generated_file_count,
            "generated_loc": generated_loc,
            "bundle_size_bytes": bundle_size
        }
    }
    
    report_file = os.path.join(BENCHMARKS_DIR, f"benchmark_{metrics['project_id']}.json")
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        
    print(f"Benchmark completed successfully. Report saved to {report_file}")
    print(json.dumps(metrics["metrics"], indent=2))

if __name__ == "__main__":
    run_benchmark()
