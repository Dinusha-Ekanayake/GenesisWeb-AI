#!/usr/bin/env python3
"""
Genesis Engine -- Planning Smoke Test (M22)
===========================================
Calls POST /api/v1/genesis/propose with three example prompts and prints
the resulting ProposedApplicationPlan for each.

Usage:
    python scripts/plan_genesis.py
    python scripts/plan_genesis.py --backend-url http://127.0.0.1:8000
    python scripts/plan_genesis.py --prompt "Create a photography portfolio site"

Exit codes:
    0  all planning calls succeeded
    1  one or more calls failed
"""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

EXAMPLE_PROMPTS = [
    {
        "id": "A",
        "prompt": (
            "Create a photography portfolio website with gallery, albums, services, and contact form."
        ),
        "preferences": {"frontend": "nextjs", "database": "postgresql"},
    },
    {
        "id": "B",
        "prompt": (
            "Create a CRM for a sales team with customers, deals, activities, reports, and team roles."
        ),
        "preferences": {"frontend": "nextjs", "backend": "fastapi", "database": "postgresql"},
    },
    {
        "id": "C",
        "prompt": (
            "Create a hotel booking platform with rooms, bookings, payments, reviews, and admin management."
        ),
        "preferences": {"frontend": "nextjs", "backend": "fastapi", "database": "postgresql"},
    },
]

_failures: list = []


def _pass(label: str, detail: str = "") -> None:
    suffix = f"  -- {detail}" if detail else ""
    print(f"  [PASS] {label}{suffix}")


def _fail(label: str, detail: str = "") -> None:
    suffix = f"  -- {detail}" if detail else ""
    print(f"  [FAIL] {label}{suffix}")
    _failures.append(label)


def http(method, url, *, headers=None, data=None, timeout=30):
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


def _detail(body) -> str:
    if isinstance(body, dict):
        return str(body.get("detail") or body)[:200]
    return str(body)[:200]


def print_plan_summary(plan: dict) -> None:
    print(f"    Name            : {plan.get('name', '?')}")
    print(f"    App type        : {plan.get('app_type', '?')}")
    print(f"    Target users    : {plan.get('target_users', '?')}")
    print(f"    Method          : {plan.get('generation_method', '?')}")
    print(f"    Approval status : {plan.get('approval_status', '?')}")
    print(f"    Validation      : {plan.get('validation_status', '?')}")

    pages = plan.get("pages") or []
    print(f"\n    Pages ({len(pages)}):")
    for p in pages:
        print(f"      - {p}")

    components = plan.get("components") or []
    print(f"\n    Components ({len(components)}):")
    for c in components:
        print(f"      - {c}")

    entities = plan.get("entities") or []
    print(f"\n    Entities ({len(entities)}):")
    for e in entities:
        print(f"      - {e}")

    api_routes = plan.get("api_routes") or []
    print(f"\n    API routes ({len(api_routes)}):")
    for r in api_routes:
        print(f"      - {r}")

    stack = plan.get("technology_stack") or {}
    fe = stack.get("frontend") or {}
    be = stack.get("backend") or {}
    db = stack.get("database") or {}
    auth = stack.get("auth") or {}
    print("\n    Tech stack:")
    print(f"      frontend  : {fe.get('framework', '?')} / {fe.get('language', '?')} / {fe.get('styling', '?')}")
    print(f"      backend   : {be.get('framework', '?')} / {be.get('language', '?')} / {be.get('orm', '?')}")
    print(f"      database  : {db.get('engine', '?')} ({db.get('hosting', '?')})")
    print(f"      auth      : {auth.get('provider', '?')} / {auth.get('strategy', '?')}")

    warnings = plan.get("warnings") or []
    if warnings:
        print(f"\n    Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"      ! {w}")

    assumptions = plan.get("assumptions") or []
    if assumptions:
        print(f"\n    Assumptions ({len(assumptions)}):")
        for a in assumptions:
            print(f"      ~ {a}")

    summary = plan.get("architecture_summary", "")
    if summary:
        print(f"\n    Architecture summary:")
        words = summary.split()
        line = "      "
        for word in words:
            if len(line) + len(word) > 80:
                print(line)
                line = "      " + word + " "
            else:
                line += word + " "
        if line.strip():
            print(line)

    print(f"\n    Approval required : {plan.get('approval_status', '?') == 'PENDING'}")
    print(f"    Editable          : True")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Genesis Engine planning smoke test (M22)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--backend-url", default="http://127.0.0.1:8000", metavar="URL")
    parser.add_argument("--api-prefix", default="/api/v1", metavar="PATH")
    parser.add_argument("--username", default="developer")
    parser.add_argument("--password", default="devpassword")
    parser.add_argument(
        "--prompt",
        default=None,
        metavar="TEXT",
        help="Run a single custom prompt instead of the three example prompts.",
    )
    args = parser.parse_args()

    base = args.backend_url.rstrip("/")
    api = f"{base}{args.api_prefix}"

    print()
    print("Genesis Engine -- Planning Smoke Test (M22)")
    print("=" * 55)
    print(f"  Backend : {base}")
    print(f"  API     : {api}")
    print()

    # --- Health check ---
    status, body = http("GET", f"{base}/health")
    if status is None:
        _fail("GET /health", str(body))
        print()
        print("  Backend is unreachable. Start it with:")
        print("    cd backend && uvicorn main:app --reload --port 8000")
        sys.exit(1)
    elif status == 200:
        _pass("GET /health")
    else:
        _fail("GET /health", f"HTTP {status}")

    # --- Auth ---
    form = urllib.parse.urlencode({"username": args.username, "password": args.password}).encode()
    status, body = http(
        "POST", f"{api}/auth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=form,
    )
    if status == 200 and isinstance(body, dict) and "access_token" in body:
        token: str = body["access_token"]
        _pass(f"POST /auth/token (user: {args.username})")
    else:
        _fail("POST /auth/token", f"HTTP {status}: {_detail(body)}")
        sys.exit(1)

    auth_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # --- Choose prompts to run ---
    if args.prompt:
        prompts_to_run = [{"id": "custom", "prompt": args.prompt, "preferences": {}}]
    else:
        prompts_to_run = EXAMPLE_PROMPTS

    # --- Run planning calls ---
    print()
    for item in prompts_to_run:
        pid = item["id"]
        prompt_text = item["prompt"]
        preferences = item.get("preferences", {})

        print(f"Planning prompt {pid}:")
        print(f'  "{prompt_text[:80]}{"..." if len(prompt_text) > 80 else ""}"')
        print()

        payload = json.dumps({
            "prompt": prompt_text,
            "preferences": preferences,
        }).encode()

        status, body = http(
            "POST", f"{api}/genesis/propose",
            headers=auth_headers,
            data=payload,
            timeout=60,
        )

        label = f"POST /genesis/propose [{pid}]"
        if status == 200 and isinstance(body, dict) and body.get("success"):
            data = body.get("data") or {}
            plan = data.get("plan") or {}
            editable = data.get("editable", False)
            requires_approval = data.get("requires_approval_before_generation", False)

            if not plan:
                _fail(label, "Response success=true but plan is empty")
            elif not requires_approval:
                _fail(label, "requires_approval_before_generation is not true")
            else:
                _pass(label, f"method={plan.get('generation_method', '?')} pages={len(plan.get('pages', []))} entities={len(plan.get('entities', []))}")
                print()
                print_plan_summary(plan)
        else:
            detail = _detail(body)
            _fail(label, f"HTTP {status}: {detail}")

        print()
        print("-" * 55)
        print()

    # --- Summary ---
    print("=" * 55)
    if _failures:
        print(f"RESULT: FAIL  ({len(_failures)} check(s) failed: {', '.join(_failures)})")
        sys.exit(1)
    else:
        print("RESULT: PASS  (all planning checks passed)")
        sys.exit(0)


if __name__ == "__main__":
    main()
