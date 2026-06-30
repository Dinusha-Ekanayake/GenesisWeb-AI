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
