#!/usr/bin/env python3
"""
Genesis Engine -- Generated App Quality Benchmark (M18)
=======================================================
Runs validate + generate for 3 increasingly complex specs and reports results.
Uses only Python stdlib -- no external dependencies required.

Usage:
    python scripts/benchmark_genesis.py
    python scripts/benchmark_genesis.py --backend-url http://127.0.0.1:8000
    python scripts/benchmark_genesis.py --skip-generate   # validate only, no workspace mutations
"""

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BENCHMARK_SPECS = [
    {
        "id": "A",
        "label": "Simple -- Personal Portfolio",
        "spec": {
            "project_id": "benchmark_portfolio_001",
            "name": "Personal Portfolio",
            "description": (
                "A personal portfolio website with Home, About, Projects, Blog, and Contact pages. "
                "Includes a responsive navbar, project cards with thumbnails and descriptions, "
                "blog preview cards with date and excerpt, a contact form with name/email/message "
                "fields, and a footer."
            ),
            "pages": ["Home", "About", "Projects", "Blog", "Contact"],
            "components": ["Navbar", "ProjectCard", "BlogPreviewCard", "ContactForm", "Footer"],
        },
    },
    {
        "id": "B",
        "label": "Medium -- Task Management Dashboard",
        "spec": {
            "project_id": "benchmark_tasks_001",
            "name": "Task Management Dashboard",
            "description": (
                "A task management dashboard with login page, dashboard overview with summary stats, "
                "projects page with project list, task board with Kanban columns (Todo, In Progress, Done), "
                "task detail page, team members page with member cards, and settings page. "
                "Includes reusable Card, Table, Form, StatusBadge, TaskCard, Sidebar, and Navbar components."
            ),
            "pages": ["Login", "Dashboard", "Projects", "TaskBoard", "TaskDetail", "TeamMembers", "Settings"],
            "components": ["Navbar", "Sidebar", "Card", "Table", "Form", "StatusBadge", "TaskCard"],
        },
    },
    {
        "id": "C",
        "label": "Advanced -- SaaS CRM Application",
        "spec": {
            "project_id": "benchmark_crm_001",
            "name": "SaaS CRM Application",
            "description": (
                "A small SaaS CRM application with authentication screens (login, register), "
                "dashboard analytics with KPI cards and chart placeholders, customer list with search and filters, "
                "customer detail page with contact info and activity history, deals pipeline with stage columns, "
                "activities timeline, team management page, settings page, and a reusable layout shell. "
                "Includes Form, Table, Chart placeholder, DealCard, ActivityCard, CustomerCard, StatusBadge, "
                "Navbar, and LayoutShell components. Backend includes REST API routes for customers, deals, "
                "and activities."
            ),
            "pages": [
                "Login", "Register", "Dashboard", "CustomerList", "CustomerDetail",
                "DealsPipeline", "ActivitiesTimeline", "TeamManagement", "Settings",
            ],
            "components": [
                "LayoutShell", "Navbar", "Form", "Table", "Chart",
                "DealCard", "ActivityCard", "CustomerCard", "StatusBadge",
            ],
        },
    },
]


def http(method, url, *, headers=None, data=None, timeout=180):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, (json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            return exc.code, json.loads(raw)
        except Exception:
            return exc.code, {"detail": raw}
    except (urllib.error.URLError, OSError, TimeoutError) as exc:
        return None, str(exc)


def workspace_tree(root: Path, indent: int = 0) -> list[str]:
    lines = []
    try:
        entries = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name))
    except PermissionError:
        return [f"{'  ' * indent}[permission denied]"]
    for entry in entries:
        prefix = "  " * indent
        if entry.is_dir():
            lines.append(f"{prefix}{entry.name}/")
            lines.extend(workspace_tree(entry, indent + 1))
        else:
            size = entry.stat().st_size
            lines.append(f"{prefix}{entry.name}  ({size} bytes)")
    return lines


def read_file_head(path: Path, lines: int = 30) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        return "\n".join(text.splitlines()[:lines])
    except Exception as exc:
        return f"[read error: {exc}]"


def main():
    parser = argparse.ArgumentParser(description="Genesis Engine benchmark -- M18")
    parser.add_argument("--backend-url", default="http://127.0.0.1:8000", metavar="URL")
    parser.add_argument("--api-prefix", default="/api/v1", metavar="PATH")
    parser.add_argument("--username", default="developer")
    parser.add_argument("--password", default="devpassword")
    parser.add_argument(
        "--skip-generate",
        action="store_true",
        help="Run validate only; skip generate (no workspace mutations)",
    )
    parser.add_argument(
        "--spec",
        choices=["A", "B", "C", "all"],
        default="all",
        help="Which benchmark spec to run (default: all)",
    )
    args = parser.parse_args()

    base = args.backend_url.rstrip("/")
    api = f"{base}{args.api_prefix}"
    workspace_root = Path(__file__).parent.parent / "workspace"

    print()
    print("Genesis Engine -- Generated App Quality Benchmark")
    print("=" * 60)
    print(f"  Backend : {base}")
    print(f"  Mode    : {'validate-only' if args.skip_generate else 'validate + generate'}")
    print()

    # Auth
    form = urllib.parse.urlencode({"username": args.username, "password": args.password}).encode()
    status, body = http(
        "POST",
        f"{api}/auth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=form,
        timeout=15,
    )
    if status != 200 or not isinstance(body, dict) or "access_token" not in body:
        print(f"[FAIL] Auth failed: HTTP {status}")
        sys.exit(1)
    token = body["access_token"]
    auth = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    print(f"[AUTH] Token acquired for user '{args.username}'")
    print()

    specs_to_run = (
        BENCHMARK_SPECS
        if args.spec == "all"
        else [s for s in BENCHMARK_SPECS if s["id"] == args.spec]
    )

    results = {}

    for bench in specs_to_run:
        bid = bench["id"]
        spec = bench["spec"]
        pid = spec["project_id"]

        print("=" * 60)
        print(f"BENCHMARK {bid}: {bench['label']}")
        print(f"  project_id : {pid}")
        print(f"  pages      : {spec['pages']}")
        print(f"  components : {spec['components']}")
        print()

        body_bytes = json.dumps(spec).encode()

        # Validate
        print(f"  Validating...")
        t0 = time.time()
        status, body = http("POST", f"{api}/genesis/validate", headers=auth, data=body_bytes, timeout=60)
        t1 = time.time()

        if status == 200 and isinstance(body, dict):
            score = (body.get("data") or {}).get("score", "?")
            print(f"  [PASS] POST /genesis/validate  score={score}  ({t1-t0:.1f}s)")
            results[bid] = {"validate": "PASS", "score": score}
        else:
            detail = (body.get("detail") if isinstance(body, dict) else str(body))[:300]
            print(f"  [FAIL] POST /genesis/validate  HTTP {status}: {detail}")
            results[bid] = {"validate": "FAIL", "score": None}

        if args.skip_generate or results[bid]["validate"] != "PASS":
            print()
            continue

        # Generate
        print(f"  Generating (may take 30-120s)...")
        t0 = time.time()
        status, body = http("POST", f"{api}/genesis/generate", headers=auth, data=body_bytes, timeout=300)
        t1 = time.time()

        if status == 200 and isinstance(body, dict):
            data = body.get("data") or {}
            manifest = data.get("manifest") or {}
            ret_pid = manifest.get("project_id", pid)
            rule_score = manifest.get("rule_engine_score", "?")
            build_status = manifest.get("build_status", "?")
            graph_count = len(manifest.get("graph_hashes") or {})
            plugins = list((manifest.get("plugin_versions") or {}).keys())
            print(f"  [PASS] POST /genesis/generate  ({t1-t0:.1f}s)")
            print(f"    project_id       : {ret_pid}")
            print(f"    build_status     : {build_status}")
            print(f"    rule_engine_score: {rule_score}")
            print(f"    graphs           : {graph_count}")
            print(f"    plugins          : {plugins}")
            results[bid]["generate"] = "PASS"
            results[bid]["manifest"] = manifest
        else:
            detail = (body.get("detail") if isinstance(body, dict) else str(body))[:300]
            print(f"  [FAIL] POST /genesis/generate  HTTP {status}: {detail}")
            results[bid]["generate"] = "FAIL"
            print()
            continue

        # Workspace inspection
        ws_path = workspace_root / pid
        print()
        if ws_path.exists():
            tree_lines = workspace_tree(ws_path)
            total_files = sum(1 for p in ws_path.rglob("*") if p.is_file())
            print(f"  Workspace: {ws_path}  ({total_files} files)")
            print()
            for line in tree_lines:
                print(f"    {line}")
            results[bid]["workspace_path"] = str(ws_path)
            results[bid]["file_count"] = total_files
        else:
            print(f"  [WARN] Workspace path not found: {ws_path}")
            results[bid]["workspace_path"] = None
            results[bid]["file_count"] = 0

        print()

    # Summary table
    print()
    print("=" * 60)
    print("SUMMARY")
    print()
    for bid, r in results.items():
        bench = next(b for b in BENCHMARK_SPECS if b["id"] == bid)
        validate = r.get("validate", "-")
        generate = r.get("generate", "-") if not args.skip_generate else "skipped"
        score = r.get("score", "-")
        files = r.get("file_count", "-")
        print(f"  Benchmark {bid} ({bench['spec']['project_id']})")
        print(f"    validate : {validate}  (score={score})")
        print(f"    generate : {generate}")
        print(f"    files    : {files}")
        print()

    # Print key file contents for inspection
    if not args.skip_generate:
        print("=" * 60)
        print("FILE CONTENT SAMPLES")
        print()
        for bench in specs_to_run:
            bid = bench["id"]
            pid = bench["spec"]["project_id"]
            ws_path = workspace_root / pid
            if not ws_path.exists():
                continue
            print(f"--- Benchmark {bid}: {pid} ---")
            for rel in [
                "spec.json",
                "frontend/app",
                "backend/app/main.py",
                "backend/app/routes",
            ]:
                target = ws_path / rel
                if target.is_file():
                    print(f"\n  [{rel}]")
                    print(read_file_head(target, 40))
                elif target.is_dir():
                    sub_files = sorted(target.rglob("*"))
                    print(f"\n  [{rel}/] contains:")
                    for sf in sub_files[:20]:
                        if sf.is_file():
                            size = sf.stat().st_size
                            print(f"    {sf.relative_to(ws_path)}  ({size} bytes)")
            print()

    all_passed = all(
        r.get("validate") == "PASS" and (args.skip_generate or r.get("generate") == "PASS")
        for r in results.values()
    )
    print("=" * 60)
    print(f"RESULT: {'PASS' if all_passed else 'PARTIAL / FAIL'}")
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
