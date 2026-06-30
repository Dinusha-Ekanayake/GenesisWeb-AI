import json
import os
import sys
import asyncio
import uuid
from pathlib import Path
from datetime import datetime
from functools import wraps

# Ensure the root Genesis Engine directory is on the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import StreamingResponse, FileResponse
from backend.app.security.path_validator import PathValidator
from backend.app.core.exceptions import (
    GenesisException, WorkspaceSecurityError, WorkspaceNotFoundError, 
    ArtifactNotFoundError, GraphNotFoundError, CompilerTamperError
)
from backend.app.services.filesystem_service import FileSystemService
from genesis_engine.telemetry.events import TelemetryEventBus
from backend.app.security.auth import RequirePermission, Permission

router = APIRouter(prefix="/genesis", tags=["Genesis Control Plane"])

# Workspace root
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../workspace"))

_orchestrator = None
_compiler_service = None

def _get_orchestrator():
    global _orchestrator
    if _orchestrator is None:
        try:
            from genesis_engine.core.orchestrator import ExecutionOrchestrator
            _orchestrator = ExecutionOrchestrator(WORKSPACE_ROOT)
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Genesis Engine not available: {e}")
    return _orchestrator

def _get_compiler_service():
    global _compiler_service
    if _compiler_service is None:
        try:
            from backend.app.services.compiler_service import CompilerService
            _compiler_service = CompilerService(_get_orchestrator())
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Compiler service not available: {e}")
    return _compiler_service

def _get_spec_class():
    try:
        from genesis_engine.models.spec import ProjectSpecification
        return ProjectSpecification
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Genesis Engine models not available: {e}")

def api_response(data=None, error=None, success=True):
    return {
        "success": success,
        "data": data if data is not None else {},
        "error": error,
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": str(uuid.uuid4())
    }

def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        except WorkspaceSecurityError as e:
            if getattr(e, 'is_binary', False):
                raise HTTPException(status_code=415, detail=str(e))
            raise HTTPException(status_code=403, detail=str(e))
        except (WorkspaceNotFoundError, ArtifactNotFoundError, GraphNotFoundError) as e:
            raise HTTPException(status_code=404, detail=str(e))
        except CompilerTamperError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return wrapper

# Stacks supported by the current minimal generator plugins.
# Reject approve-and-generate requests for any other stack with a clear error.
SUPPORTED_FRONTEND_FRAMEWORKS = {"nextjs"}
SUPPORTED_BACKEND_FRAMEWORKS = {"fastapi"}


@router.post("/approve-and-generate", dependencies=[Depends(RequirePermission(Permission.COMPILE))])
@handle_exceptions
async def approve_and_generate(body: dict):
    """
    Approval-gated generation endpoint. Accepts an approved ProposedApplicationPlan and
    an explicit approval object. Validates approval, validates the plan, checks stack
    compatibility, converts to ProjectSpecification, runs the compiler pipeline, and
    persists the approved plan alongside all other artifacts.

    Rejected (no workspace created) when:
    - approval.approved is not True
    - plan fields are invalid (empty pages, missing project_id/name)
    - technology_stack specifies an unsupported framework
    """
    from genesis_engine.models.planning import ProposedApplicationPlan
    from genesis_engine.models.spec import ProjectSpecification

    # 1. Parse top-level inputs
    approval = body.get("approval", {})
    plan_dict = body.get("plan", {})

    if not isinstance(approval, dict):
        raise HTTPException(status_code=422, detail="Field 'approval' must be an object.")
    if not isinstance(plan_dict, dict):
        raise HTTPException(status_code=422, detail="Field 'plan' must be an object.")

    # 2. Validate approval FIRST — no filesystem work until this passes
    if not approval.get("approved", False):
        raise HTTPException(
            status_code=400,
            detail=(
                "Generation rejected: approval.approved must be true. "
                "Review the proposed plan, make any edits, then resubmit with approved=true."
            ),
        )

    # 3. Parse and validate plan structure
    try:
        plan = ProposedApplicationPlan(**plan_dict)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid plan: {e}")

    project_id = PathValidator.validate_project_id(plan.project_id)

    if not plan.name.strip():
        raise HTTPException(status_code=422, detail="Plan validation failed: 'name' must not be empty.")

    if not plan.pages:
        raise HTTPException(
            status_code=422,
            detail="Plan validation failed: 'pages' must not be empty. At least one page is required for generation.",
        )

    # 4. Validate stack compatibility — reject unsupported stacks before touching filesystem
    fe_framework = plan.technology_stack.frontend.framework.lower()
    be_framework = plan.technology_stack.backend.framework.lower()

    stack_errors = []
    if fe_framework not in SUPPORTED_FRONTEND_FRAMEWORKS:
        stack_errors.append(
            f"frontend.framework='{plan.technology_stack.frontend.framework}' is not supported. "
            f"Supported: {sorted(SUPPORTED_FRONTEND_FRAMEWORKS)}."
        )
    if be_framework not in SUPPORTED_BACKEND_FRAMEWORKS:
        stack_errors.append(
            f"backend.framework='{plan.technology_stack.backend.framework}' is not supported. "
            f"Supported: {sorted(SUPPORTED_BACKEND_FRAMEWORKS)}."
        )
    if stack_errors:
        raise HTTPException(
            status_code=422,
            detail=(
                "Unsupported technology stack in approved plan. "
                + " ".join(stack_errors)
                + " Change the plan's technology_stack before generation, "
                "or wait for additional generator support."
            ),
        )

    # 5. Convert ProposedApplicationPlan → ProjectSpecification (v2: carries all rich plan fields)
    spec = ProjectSpecification(
        project_id=plan.project_id,
        name=plan.name,
        description=plan.description,
        pages=plan.pages,
        components=plan.components,
        # Rich plan fields — persisted to spec.json and carried into GenesisIR
        entities=plan.entities,
        entity_definitions=[ed.model_dump() for ed in plan.entity_definitions],
        api_routes=plan.api_routes,
        auth_requirements=plan.auth_requirements,
        roles_permissions=plan.roles_permissions,
        navigation_structure=plan.navigation_structure,
        technology_stack=plan.technology_stack.model_dump(),
        tools_libraries=plan.tools_libraries,
        deployment_target=plan.deployment_target,
        app_type=plan.app_type,
        target_users=plan.target_users,
        architecture_summary=plan.architecture_summary,
        assumptions=plan.assumptions,
        warnings=plan.warnings,
        # Framework/infra dicts (unchanged from M23)
        theme={},
        authentication={
            "provider": plan.technology_stack.auth.provider,
            "strategy": plan.technology_stack.auth.strategy,
        },
        database={
            "engine": plan.technology_stack.database.engine,
            "hosting": plan.technology_stack.database.hosting,
        },
        backend={
            "framework": plan.technology_stack.backend.framework,
            "language": plan.technology_stack.backend.language,
            "orm": plan.technology_stack.backend.orm,
        },
        frontend={
            "framework": plan.technology_stack.frontend.framework,
            "language": plan.technology_stack.frontend.language,
            "styling": plan.technology_stack.frontend.styling,
        },
        deployment={
            "target": plan.deployment_target,
            "containerization": plan.technology_stack.deployment.containerization,
        },
    )

    # 6. Create workspace and write spec — first filesystem writes
    project_dir = PathValidator.resolve_and_validate_path(WORKSPACE_ROOT, project_id)
    await FileSystemService.mkdir(project_dir, parents=True, exist_ok=True)
    await FileSystemService.write_json(project_dir / "spec.json", spec.model_dump())

    # 7. Run compiler pipeline (validate → generate → build)
    compiler = _get_compiler_service()
    manifest = await compiler.run_pipeline(spec)

    # 8. Persist the approved plan to artifacts/ AFTER the pipeline completes.
    #    The tamper-detection hash check inside execute_build() is already done at this point.
    artifacts_dir = project_dir / "artifacts"
    await FileSystemService.mkdir(artifacts_dir, parents=True, exist_ok=True)
    approved_plan_data = plan.model_dump()
    approved_plan_data["approval_status"] = "APPROVED"
    approved_plan_data["approved_by"] = approval.get("approved_by", "user")
    approved_plan_data["approval_notes"] = approval.get("notes", "")
    await FileSystemService.write_json(artifacts_dir / "approved_plan.json", approved_plan_data)

    # 9. Build response
    approved_plan_summary = {
        "project_id": plan.project_id,
        "name": plan.name,
        "app_type": plan.app_type,
        "pages": plan.pages,
        "components": plan.components,
        "entities": plan.entities,
        "technology_stack": {
            "frontend": plan.technology_stack.frontend.framework,
            "backend": plan.technology_stack.backend.framework,
            "database": plan.technology_stack.database.engine,
        },
        "generation_method": plan.generation_method,
        "approval_status": "APPROVED",
        "approved_by": approval.get("approved_by", "user"),
    }

    return api_response({
        "status": "SUCCESS",
        "project_id": project_id,
        "manifest": manifest,
        "approved_plan_summary": approved_plan_summary,
    })


@router.post("/propose", dependencies=[Depends(RequirePermission(Permission.COMPILE))])
@handle_exceptions
async def propose_plan(body: dict):
    """
    Planning-only endpoint. Accepts a natural language prompt and optional
    technology preferences; returns a ProposedApplicationPlan.
    No workspace files are written. No code is generated.
    The plan requires explicit approval before generation can proceed.
    """
    prompt = body.get("prompt", "").strip()
    if not prompt:
        raise HTTPException(status_code=422, detail="Field 'prompt' is required and must not be empty.")

    preferences = body.get("preferences", {})
    if not isinstance(preferences, dict):
        preferences = {}

    project_id = body.get("project_id") or f"plan_{uuid.uuid4().hex[:8]}"

    from backend.app.services.planning_service import PlanningService
    service = PlanningService()
    plan = await asyncio.to_thread(service.propose, prompt=prompt, preferences=preferences, project_id=project_id)

    return api_response({
        "plan": plan.model_dump(),
        "editable": True,
        "requires_approval_before_generation": True,
    })


@router.post("/parse", dependencies=[Depends(RequirePermission(Permission.COMPILE))])
@handle_exceptions
async def parse_prompt(prompt: str):
    return api_response({"status": "Not Implemented", "message": "Use direct spec submission for now."})

@router.post("/plan", dependencies=[Depends(RequirePermission(Permission.COMPILE))])
@handle_exceptions
async def plan_spec(body: dict):
    ProjectSpecification = _get_spec_class()
    orchestrator = _get_orchestrator()
    spec = ProjectSpecification(**body)
    PathValidator.validate_project_id(spec.project_id)
    report = orchestrator.validate_spec(spec)
    return api_response({"status": "SUCCESS", "report": report})

@router.post("/validate", dependencies=[Depends(RequirePermission(Permission.VALIDATE))])
@handle_exceptions
async def validate_spec(body: dict):
    ProjectSpecification = _get_spec_class()
    orchestrator = _get_orchestrator()
    spec = ProjectSpecification(**body)
    PathValidator.validate_project_id(spec.project_id)
    report = orchestrator.validate_spec(spec)
    return api_response({"status": "SUCCESS", "score": report.graph_integrity_score})

@router.post("/generate", dependencies=[Depends(RequirePermission(Permission.COMPILE))])
@handle_exceptions
async def generate_project(body: dict):
    ProjectSpecification = _get_spec_class()
    compiler = _get_compiler_service()
    
    spec = ProjectSpecification(**body)
    project_id = PathValidator.validate_project_id(spec.project_id)
    
    project_dir = PathValidator.resolve_and_validate_path(WORKSPACE_ROOT, project_id)
    await FileSystemService.mkdir(project_dir, parents=True, exist_ok=True)
    
    await FileSystemService.write_json(project_dir / "spec.json", body)
        
    manifest = await compiler.run_pipeline(spec)
    return api_response({"status": "SUCCESS", "manifest": manifest})

@router.post("/deploy/{project_id}", dependencies=[Depends(RequirePermission(Permission.DEPLOY))])
@handle_exceptions
async def deploy_project(project_id: str):
    compiler = _get_compiler_service()
    
    valid_id = PathValidator.validate_project_id(project_id)
    report_path = PathValidator.resolve_and_validate_path(WORKSPACE_ROOT, f"{valid_id}/artifacts/planning_report.json")
    
    if not await FileSystemService.exists(report_path):
        raise HTTPException(status_code=404, detail="Planning report not found. Compile first.")
        
    report = await FileSystemService.read_json(report_path)
        
    manifest = await compiler.run_deploy(valid_id, report)
    return api_response({"status": "SUCCESS", "manifest": manifest})

async def _get_project_data_from_disk(project_id: str):
    try:
        valid_id = PathValidator.validate_project_id(project_id)
        project_dir = PathValidator.resolve_and_validate_path(WORKSPACE_ROOT, valid_id, allow_hidden=True)
    except Exception:
        return None
        
    if not await FileSystemService.exists(project_dir):
        return None
        
    status = "IDLE"
    created_at = None
    
    trace_file = project_dir / "execution_trace.json"
    traces = []
    if await FileSystemService.exists(trace_file):
        try:
            trace_data = await FileSystemService.read_json(trace_file)
            events = trace_data.get("events", [])
            
            for e in events:
                traces.append({
                    "timestamp": e.get("timestamp", ""),
                    "event": f"{e.get('phase', '')} {e.get('step', '')} {e.get('status', '')}".strip(),
                    "details": e
                })
            
            if events:
                last_event = events[-1]
                if last_event.get("phase") == "pipeline" and last_event.get("status") == "completed":
                    status = "SUCCESS"
                elif "fail" in str(last_event).lower():
                    status = "FAILED"
                else:
                    status = "RUNNING"
                    
                created_at = events[0].get("timestamp")
        except Exception:
            pass
            
    if not created_at:
        import datetime
        ctime = await FileSystemService.get_ctime(project_dir)
        created_at = datetime.datetime.fromtimestamp(ctime, datetime.timezone.utc).isoformat()
            
    report = None
    report_file = project_dir / "artifacts" / "planning_report.json"
    if await FileSystemService.exists(report_file):
        try:
            report = await FileSystemService.read_json(report_file)
        except Exception:
            pass
            
    manifest = None
    manifest_file = project_dir / "artifacts" / "deployment_manifest.json"
    if await FileSystemService.exists(manifest_file):
        try:
            manifest = await FileSystemService.read_json(manifest_file)
        except Exception:
            pass

    spec = None
    spec_file = project_dir / "spec.json"
    if await FileSystemService.exists(spec_file):
        try:
            spec = await FileSystemService.read_json(spec_file)
        except Exception:
            pass

    return {
        "id": project_id,
        "title": project_id.replace("_", " ").title(),
        "status": status,
        "created_at": created_at,
        "spec": spec,
        "planning_report": report,
        "deployment_manifest": manifest,
        "execution_trace": traces
    }

@router.get("/projects", dependencies=[Depends(RequirePermission(Permission.READ_WORKSPACE))])
@handle_exceptions
async def list_projects():
    projects = []
    root = Path(WORKSPACE_ROOT)
    if not await FileSystemService.exists(root):
        return api_response(projects)
        
    dirs = await FileSystemService.list_directory(root)
    for d in dirs:
        if await FileSystemService.is_dir(d):
            try:
                PathValidator.validate_project_id(d.name)
                data = await _get_project_data_from_disk(d.name)
                if data:
                    projects.append(data)
            except WorkspaceSecurityError:
                continue
    projects.sort(key=lambda x: x["created_at"], reverse=True)
    return api_response(projects)

@router.get("/projects/{project_id}", dependencies=[Depends(RequirePermission(Permission.READ_WORKSPACE))])
@handle_exceptions
async def get_project(project_id: str):
    data = await _get_project_data_from_disk(project_id)
    if not data:
        raise WorkspaceNotFoundError("Project not found in workspace")
    return api_response(data)

from backend.app.security.auth import get_user_repository, Permission
from backend.app.security.jwt_service import JWTService

@router.get("/events")
async def sse_events(
    request: Request, 
    project_id: str = "*", 
    token: str = None,
    user_repo = Depends(get_user_repository)
):
    # Manually authenticate because EventSource cannot send headers
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
        
    payload = JWTService.decode_token(token)
    if not payload or not payload.get("sub"):
        raise HTTPException(status_code=401, detail="Invalid token")
        
    user = user_repo.get_user(payload.get("sub"))
    if not user or Permission.READ_WORKSPACE not in user.permissions:
        raise HTTPException(status_code=403, detail="Forbidden")
    async def event_generator():
        try:
            if project_id != "*":
                PathValidator.validate_project_id(project_id)
        except WorkspaceSecurityError:
            yield "data: {\"error\": \"Invalid project_id\"}\n\n"
            return
            
        loop = asyncio.get_running_loop()
        subscriber = TelemetryEventBus.subscribe(project_id, queue_size=50)
        
        try:
            while True:
                if await request.is_disconnected():
                    break
                    
                # Heartbeat
                try:
                    event = await loop.run_in_executor(None, subscriber.get, True, 20.0)
                    yield f"data: {json.dumps(event)}\n\n"
                except asyncio.TimeoutError:
                    yield f"data: {json.dumps({'event_id': str(uuid.uuid4()), 'project_id': project_id, 'phase': 'Heartbeat', 'timestamp': datetime.utcnow().isoformat()})}\n\n"
                except Exception:
                    pass
        finally:
            TelemetryEventBus.unsubscribe(project_id, subscriber)
            
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/projects/{project_id}/status", dependencies=[Depends(RequirePermission(Permission.READ_WORKSPACE))])
@handle_exceptions
async def get_project_status(project_id: str):
    data = await _get_project_data_from_disk(project_id)
    if not data:
        raise WorkspaceNotFoundError("Project not found")
    return api_response({
        "id": data["id"],
        "status": data["status"],
        "created_at": data["created_at"]
    })

@router.get("/projects/{project_id}/telemetry", dependencies=[Depends(RequirePermission(Permission.READ_WORKSPACE))])
@handle_exceptions
async def get_project_telemetry(project_id: str):
    data = await _get_project_data_from_disk(project_id)
    if not data:
        raise WorkspaceNotFoundError("Project not found")
    return api_response(data.get("execution_trace", []))

@router.get("/projects/{project_id}/manifest", dependencies=[Depends(RequirePermission(Permission.READ_WORKSPACE))])
@handle_exceptions
async def get_project_manifest(project_id: str):
    data = await _get_project_data_from_disk(project_id)
    if not data:
        raise WorkspaceNotFoundError("Project not found")
    return api_response(data.get("deployment_manifest"))

@router.get("/projects/{project_id}/graphs", dependencies=[Depends(RequirePermission(Permission.READ_WORKSPACE))])
@handle_exceptions
async def get_project_graphs(project_id: str):
    valid_id = PathValidator.validate_project_id(project_id)
    artifacts_dir = PathValidator.resolve_and_validate_path(WORKSPACE_ROOT, f"{valid_id}/artifacts", allow_hidden=True)
    if not await FileSystemService.exists(artifacts_dir):
        return api_response({})
        
    graphs = {}
    files = await FileSystemService.list_directory(artifacts_dir)
    for f in files:
        if f.name.endswith("_graph.json"):
            try:
                graphs[f.stem] = await FileSystemService.read_json(f)
            except Exception:
                pass
    return api_response(graphs)

@router.get("/projects/{project_id}/workspace", dependencies=[Depends(RequirePermission(Permission.READ_WORKSPACE))])
@handle_exceptions
async def get_project_workspace(project_id: str):
    valid_id = PathValidator.validate_project_id(project_id)
    project_dir = PathValidator.resolve_and_validate_path(WORKSPACE_ROOT, valid_id, allow_hidden=True)
    
    if not await FileSystemService.exists(project_dir):
        raise WorkspaceNotFoundError("Project not found")
        
    tree = await FileSystemService.build_project_tree(project_dir, PathValidator.FORBIDDEN_NAMES)
    return api_response(tree)

@router.get("/projects/{project_id}/file", dependencies=[Depends(RequirePermission(Permission.READ_WORKSPACE))])
@handle_exceptions
async def get_project_file(project_id: str, path: str):
    valid_id = PathValidator.validate_project_id(project_id)
    file_path = PathValidator.resolve_and_validate_path(WORKSPACE_ROOT, f"{valid_id}/{path}", is_preview=True)
        
    try:
        content = await FileSystemService.read_text(file_path)
        return api_response({"content": content})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cannot read file: {e}")

@router.get("/projects/{project_id}/artifacts/{artifact_name}", dependencies=[Depends(RequirePermission(Permission.DOWNLOAD_ARTIFACTS))])
async def download_artifact(project_id: str, artifact_name: str):
    try:
        valid_id = PathValidator.validate_project_id(project_id)
        valid_artifact = PathValidator.validate_artifact_name(artifact_name)
        
        if valid_artifact == "deployment_bundle.zip":
            file_path = PathValidator.resolve_and_validate_path(WORKSPACE_ROOT, f"{valid_id}/exports/{valid_artifact}")
        else:
            file_path = PathValidator.resolve_and_validate_path(WORKSPACE_ROOT, f"{valid_id}/artifacts/{valid_artifact}")
            
        if not await FileSystemService.is_file(file_path):
            raise ArtifactNotFoundError("Artifact not found")
            
        return FileResponse(
            path=file_path,
            filename=valid_artifact,
            media_type="application/octet-stream" if valid_artifact.endswith(".zip") else "application/json"
        )
    except WorkspaceSecurityError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except (ArtifactNotFoundError, FileNotFoundError):
        raise HTTPException(status_code=404, detail="Artifact not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
