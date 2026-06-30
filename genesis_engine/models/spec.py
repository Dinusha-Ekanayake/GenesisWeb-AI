from pydantic import BaseModel, Field
from typing import Dict, Any, List

class ProjectSpecification(BaseModel):
    # --- Core identity ---
    project_id: str
    name: str
    description: str

    # --- UI surface ---
    pages: List[str] = Field(default_factory=list)
    components: List[str] = Field(default_factory=list)

    # --- Rich plan fields (optional; populated by approve-and-generate, ignored by direct /generate) ---
    entities: List[str] = Field(default_factory=list)
    entity_definitions: List[Dict[str, Any]] = Field(default_factory=list)
    api_routes: List[str] = Field(default_factory=list)
    auth_requirements: List[str] = Field(default_factory=list)
    roles_permissions: List[str] = Field(default_factory=list)
    navigation_structure: List[str] = Field(default_factory=list)
    tools_libraries: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    deployment_target: str = ""
    app_type: str = ""
    target_users: str = ""
    architecture_summary: str = ""

    # Full technology stack snapshot from the approved plan (nested dict; informational for future planners)
    technology_stack: Dict[str, Any] = Field(default_factory=dict)

    # --- Framework/infra dicts (set by both direct /generate and approve-and-generate) ---
    theme: Dict[str, Any] = Field(default_factory=dict)
    authentication: Dict[str, Any] = Field(default_factory=dict)
    database: Dict[str, Any] = Field(default_factory=dict)
    backend: Dict[str, Any] = Field(default_factory=dict)
    frontend: Dict[str, Any] = Field(default_factory=dict)
    deployment: Dict[str, Any] = Field(default_factory=dict)
