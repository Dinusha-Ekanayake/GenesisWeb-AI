import argparse
import sys
import json
import os
from pathlib import Path

# Adjust path for execution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from genesis_engine.core.orchestrator import ExecutionOrchestrator
from genesis_engine.models.spec import ProjectSpecification

def main():
    parser = argparse.ArgumentParser(description="Genesis Engine CLI - Deterministic Software Compiler")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run the full compilation pipeline")
    run_parser.add_argument("spec", help="Path to ProjectSpecification JSON file")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate a specification (Rule Engine only)")
    validate_parser.add_argument("spec", help="Path to ProjectSpecification JSON file")
    
    # Deploy command (just packages an already built workspace for CLI usage)
    # Actually, in our orchestrator, `run` does deployment too. But we can expose explicit deploy.
    deploy_parser = subparsers.add_parser("deploy", help="Deploy/Package an existing workspace")
    deploy_parser.add_argument("project_id", help="The Project ID to deploy")
    
    args = parser.parse_args()
    
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "workspace"))
    orchestrator = ExecutionOrchestrator(workspace_root)
    
    if args.command in ["run", "validate"]:
        if not os.path.exists(args.spec):
            print(f"[ERROR] Specification file not found: {args.spec}")
            sys.exit(1)
            
        with open(args.spec, "r") as f:
            spec_data = json.load(f)
            
        try:
            spec = ProjectSpecification(**spec_data)
        except Exception as e:
            print(f"[ERROR] Error parsing specification: {e}")
            sys.exit(1)
            
        if args.command == "validate":
            print(f"--- Validating Specification for {spec.project_id} ---")
            try:
                report = orchestrator.validate_spec(spec)
                print(f"[SUCCESS] Validation Passed! Integrity Score: {report.graph_integrity_score}")
            except Exception as e:
                print(f"[ERROR] Validation Failed:\n{e}")
                sys.exit(1)
                
        elif args.command == "run":
            print(f"--- Compiling Project {spec.project_id} ---")
            try:
                manifest = orchestrator.run_full_pipeline(spec)
                print(f"[SUCCESS] Compilation & Deployment Successful!")
                print(f"   Bundle Hash: {manifest.deployment_hash}")
            except Exception as e:
                print(f"[ERROR] Compilation Failed:\n{e}")
                sys.exit(1)
                
    elif args.command == "deploy":
        print(f"--- Packaging Deployment for {args.project_id} ---")
        try:
            # Note: A real manual deploy would need the planning report. 
            # The orchestrator's run_full_pipeline does this automatically.
            # For standalone CLI deploy, we fetch the planning_report from the workspace.
            report_path = Path(workspace_root) / args.project_id / "artifacts" / "planning_report.json"
            if not report_path.exists():
                print("[ERROR] planning_report.json not found. You must run the compiler first.")
                sys.exit(1)
            
            with open(report_path, "r") as f:
                report = json.load(f)
                
            manifest = orchestrator.build_orchestrator.execute_build(args.project_id, report)
            print(f"[SUCCESS] Deployment Bundled!")
            print(f"   Bundle Hash: {manifest.deployment_hash}")
        except Exception as e:
            print(f"[ERROR] Deployment Failed:\n{e}")
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
