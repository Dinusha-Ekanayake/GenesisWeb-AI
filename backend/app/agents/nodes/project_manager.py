from ..state import ProjectState

def project_manager_node(state: ProjectState) -> dict:
    """
    The Project Manager orchestrates the workflow.
    It routes strictly based on events in the state.
    """
    events = state.get("events", [])
    print(f"[ProjectManager] Evaluating Events: {events}")
    
    if not events or "ProjectStarted" not in events:
        return {"events": ["ProjectStarted"], "status": "ANALYZING_REQUIREMENTS"}
        
    if "RequirementCompleted" not in events:
        return {"status": "ANALYZING_REQUIREMENTS"}
        
    if "RequirementCompleted" in events and "ValidationPassed" not in events and "ValidationFailed" not in events and "ValidationWarning" not in events:
        # Route to Genesis Compiler
        return {"status": "COMPILING"}
        
    if "ValidationWarning" in events and "ApprovalGranted" not in events:
        return {"status": "PENDING_APPROVAL"}
        
    if "ValidationFailed" in events:
        # Strict mode: Halt
        return {"status": "HALTED_DUE_TO_ERRORS"}
        
    if ("ValidationPassed" in events or "ApprovalGranted" in events) and "GenerationCompleted" not in events:
        # Route to Generator
        return {"status": "GENERATING_CODE"}
            
    return {"status": "WAITING"}
