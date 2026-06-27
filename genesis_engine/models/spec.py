from pydantic import BaseModel, Field
from typing import Dict, Any, List

class ProjectSpecification(BaseModel):
    project_id: str
    name: str
    description: str
    pages: List[str] = Field(default_factory=list)
    components: List[str] = Field(default_factory=list)
    theme: Dict[str, Any] = Field(default_factory=dict)
    authentication: Dict[str, Any] = Field(default_factory=dict)
    database: Dict[str, Any] = Field(default_factory=dict)
    backend: Dict[str, Any] = Field(default_factory=dict)
    frontend: Dict[str, Any] = Field(default_factory=dict)
    deployment: Dict[str, Any] = Field(default_factory=dict)
