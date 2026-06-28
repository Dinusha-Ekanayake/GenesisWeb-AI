"""
Genesis Engine – Compiler Benchmark Suite
==========================================
Measures compilation performance across all pipeline stages and produces
a machine-readable JSON benchmark report.

Stages measured:
  - Planning & Validation (Rule Engine)
  - Code Generation
  - Packaging (ZIP + Hash)
  - Peak Memory (via tracemalloc)
  - Total Compilation Time
  - Artifact Size (workspace + zip)

Usage:
  python scripts/benchmark.py [--output benchmark_report.json]

Exit codes:
  0 = Benchmark completed successfully
  1 = Benchmark error
"""

import sys
import os
import json
import time
import shutil
import tracemalloc
import argparse
from pathlib import Path
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(ROOT_DIR))

WORKSPACE_ROOT = ROOT_DIR / "workspace"
BENCHMARK_PROJECT_ID = "__benchmark_run__"

BENCHMARK_SPEC = {
    "project_id": BENCHMARK_PROJECT_ID,
    "title": "Benchmark Project",
    "description": "A performance benchmark project for the Genesis Engine.",
    "architecture": {
        "frontend": "react",
        "backend": "fastapi",
        "database": "postgres"
    },
    "features": ["auth", "crud"],
    "api_schema": {
        "endpoints": [
            {"path": "/users", "method": "GET", "response": "UserList"},
            {"path": "/users/{id}", "method": "GET", "response": "User"},
            {"path": "/users", "method": "POST", "response": "User"},
        ]
    },
    "data_models": {
        "User": {
            "fields": {"id": "uuid", "name": "string", "email": "string"}
        }
    }
}


def get_dir_size_bytes(path: Path) -> int:
    """Return total size in bytes of all files under path."""
    total = 0
    for p in path.rglob("*"):
        if p.is_file():
            try:
                total += p.stat().st_size
            except OSError:
                pass
    return total


def run_benchmark(output_path: str = None) -> dict:
    from genesis_engine.core.orchestrator import ExecutionOrchestrator
    from genesis_engine.models.spec import ProjectSpecification

    project_dir = WORKSPACE_ROOT / BENCHMARK_PROJECT_ID

    # Clean any previous benchmark run
    if project_dir.exists():
        shutil.rmtree(project_dir)

    orchestrator = ExecutionOrchestrator(str(WORKSPACE_ROOT))
    spec = ProjectSpecification(**BENCHMARK_SPEC)

    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "project_id": BENCHMARK_PROJECT_ID,
        "stages": {},
        "artifacts": {},
        "peak_memory_mb": None,
        "total_time_s": None,
        "passed": False,
        "errors": []
    }

    # ── Stage 1: Planning & Validation ────────────────────────────────────────
    tracemalloc.start()
    overall_start = time.perf_counter()

    try:
        t0 = time.perf_counter()
        report, f_graph, p_graph, c_graph, a_graph, db_graph, dep_graph, adr, ir = (
            orchestrator.planning_engine.validate_blueprint(spec)
        )
        results["stages"]["planning_validation"] = {
            "duration_s": round(time.perf_counter() - t0, 4),
            "graph_integrity_score": report.graph_integrity_score,
            "total_errors": report.total_errors,
            "total_warnings": report.total_warnings,
        }
    except Exception as e:
        results["errors"].append(f"Planning stage failed: {e}")
        return _finalize(results, overall_start, tracemalloc, output_path)

    # ── Stage 2: Code Generation ────────────────────────────────────────────
    try:
        from genesis_engine.rules.base import RuleContext
        from genesis_engine.plugins.implementations.fastapi_plugin import FastApiPlugin
        from genesis_engine.plugins.implementations.nextjs_plugin import NextJsPlugin

        generation_plan = orchestrator.planning_engine.generation_builder.build(
            f_graph, p_graph, c_graph, a_graph, db_graph, dep_graph, adr
        )
        rule_context = RuleContext(
            feature_graph=f_graph,
            page_graph=p_graph,
            component_graph=c_graph,
            api_graph=a_graph,
            database_graph=db_graph,
            dependency_graph=dep_graph,
        )
        orchestrator.generation_engine.register_plugin(FastApiPlugin())
        orchestrator.generation_engine.register_plugin(NextJsPlugin())

        t0 = time.perf_counter()
        orchestrator.generation_engine.execute(generation_plan, rule_context, BENCHMARK_PROJECT_ID)
        results["stages"]["code_generation"] = {
            "duration_s": round(time.perf_counter() - t0, 4),
        }
    except Exception as e:
        results["errors"].append(f"Generation stage failed: {e}")
        return _finalize(results, overall_start, tracemalloc, output_path)

    # ── Stage 3: Packaging ──────────────────────────────────────────────────
    try:
        from genesis_engine.utils.hash_utils import compute_deterministic_workspace_hash

        post_gen_hash = compute_deterministic_workspace_hash(project_dir)
        report.workspace_hash = post_gen_hash

        t0 = time.perf_counter()
        manifest = orchestrator.build_orchestrator.execute_build(
            BENCHMARK_PROJECT_ID, report.model_dump(mode="json")
        )
        results["stages"]["packaging"] = {
            "duration_s": round(time.perf_counter() - t0, 4),
            "deployment_hash": manifest.deployment_hash,
        }
    except Exception as e:
        results["errors"].append(f"Packaging stage failed: {e}")
        return _finalize(results, overall_start, tracemalloc, output_path)

    # ── Artifact Sizes ──────────────────────────────────────────────────────
    workspace_size = get_dir_size_bytes(project_dir)
    zip_path = project_dir / "exports" / "deployment_bundle.zip"
    zip_size = zip_path.stat().st_size if zip_path.exists() else 0

    results["artifacts"] = {
        "workspace_size_bytes": workspace_size,
        "workspace_size_kb": round(workspace_size / 1024, 2),
        "zip_size_bytes": zip_size,
        "zip_size_kb": round(zip_size / 1024, 2),
    }
    results["passed"] = True

    return _finalize(results, overall_start, tracemalloc, output_path)


def _finalize(results: dict, overall_start: float, tm, output_path: str) -> dict:
    _, peak = tm.get_traced_memory()
    tm.stop()

    results["total_time_s"] = round(time.perf_counter() - overall_start, 4)
    results["peak_memory_mb"] = round(peak / 1024 / 1024, 2)

    print(json.dumps(results, indent=2))

    if output_path:
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n[Benchmark] Report saved to: {output_path}")

    return results


def main():
    parser = argparse.ArgumentParser(description="Genesis Engine Benchmark Suite")
    parser.add_argument("--output", default=None, help="Path to write JSON benchmark report")
    args = parser.parse_args()

    print("=" * 60)
    print("Genesis Engine Compiler Benchmark Suite")
    print("=" * 60)

    results = run_benchmark(output_path=args.output)

    print("\n" + "=" * 60)
    if results["passed"]:
        print(f"BENCHMARK PASSED — Total: {results['total_time_s']}s | Peak Memory: {results['peak_memory_mb']} MB")
        sys.exit(0)
    else:
        print(f"BENCHMARK FAILED — Errors: {results['errors']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
