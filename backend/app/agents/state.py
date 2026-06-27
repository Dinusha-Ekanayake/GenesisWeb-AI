from typing import TypedDict, Annotated, List, Dict, Any, Optional
import operator

class ProjectState(TypedDict):
    project_id: str
    user_prompt: str
    
    # Event-Based Workflow Array
    # e.g., ["ProjectStarted", "RequirementCompleted", "ValidationPassed"]
    events: Annotated[List[str], operator.add]
    
    # Single Source of Truth
    specification: Optional[Dict[str, Any]]
    
    # Artifact tracking (mapping filename/path to metadata)
    artifacts: Annotated[Dict[str, Any], operator.ior]
    
    # Genesis Engine Outputs
    planning_report: Optional[Dict[str, Any]]
    
    # Workflow control
    status: str
    errors: Annotated[List[str], operator.add]
    
    # For human-in-the-loop approvals
    approval_status: Optional[str]
