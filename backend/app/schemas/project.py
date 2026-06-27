from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime

# Central single source of truth that all agents consume.
class ProjectSpecification(BaseModel):
    project_name: Optional[str] = None
    description: Optional[str] = None
    pages: List[str] = []
    components: List[str] = []
    theme: Dict[str, Any] = {}
    authentication: Dict[str, Any] = {}
    database: Dict[str, Any] = {}
    backend: Dict[str, Any] = {}
    frontend: Dict[str, Any] = {}
    deployment: Dict[str, Any] = {}

class ProjectBase(BaseModel):
    title: str = Field(..., description="The title of the project")
    user_prompt: str = Field(..., description="The raw natural language prompt from the user")

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: uuid.UUID
    status: str
    requirements: Optional[ProjectSpecification] = None
    architecture: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
