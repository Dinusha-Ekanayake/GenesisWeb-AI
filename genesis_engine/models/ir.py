from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class GenesisEntity(BaseModel):
    name: str
    attributes: Dict[str, str]
    relations: List[Dict[str, str]] = Field(default_factory=list)

class GenesisRole(BaseModel):
    name: str
    permissions: List[str]

class GenesisWorkflow(BaseModel):
    name: str
    steps: List[str]

class GenesisIR(BaseModel):
    project_id: str
    entities: List[GenesisEntity] = Field(default_factory=list)
    roles: List[GenesisRole] = Field(default_factory=list)
    workflows: List[GenesisWorkflow] = Field(default_factory=list)
    features: List[str] = Field(default_factory=list)
    components: List[str] = Field(default_factory=list)
    # Rich fields carried forward from approved plan (unused by current planners; available for M26+)
    api_routes: List[str] = Field(default_factory=list)
    auth_requirements: List[str] = Field(default_factory=list)
    roles_permissions: List[str] = Field(default_factory=list)
    navigation_structure: List[str] = Field(default_factory=list)
    app_type: str = ""
    target_users: str = ""
