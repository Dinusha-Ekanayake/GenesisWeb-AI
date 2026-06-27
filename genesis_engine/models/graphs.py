import hashlib
import json
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class GraphMetadata(BaseModel):
    graph_version: str = "1.0.0"
    planner_version: str = "1.0.0"
    specification_hash: str = ""
    engine_version: str = "1.0.0"

class GraphNodeMetadata(BaseModel):
    created_by: str
    derived_from: List[str] = Field(default_factory=list)
    depends_on: List[str] = Field(default_factory=list)

class GraphNode(BaseModel):
    id: str
    name: str
    metadata: GraphNodeMetadata

class DeterministicGraph(BaseModel):
    metadata: GraphMetadata = Field(default_factory=GraphMetadata)
    
    def compute_hash(self) -> str:
        data = self.model_dump()
        serialized = json.dumps(data, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

class FeatureNode(GraphNode):
    requirements: List[str]

class FeatureGraph(DeterministicGraph):
    features: List[FeatureNode]

class PageNode(GraphNode):
    route: str
    layout: Optional[str] = None
    components: List[str]

class PageGraph(DeterministicGraph):
    pages: List[PageNode]

class ComponentNode(GraphNode):
    props: Dict[str, Any]
    state: Dict[str, Any]
    children: List[str] = Field(default_factory=list)

class ComponentGraph(DeterministicGraph):
    components: List[ComponentNode]

class ApiEndpointNode(GraphNode):
    path: str
    method: str
    requires_auth: bool = False
    request_schema: Optional[str] = None
    response_schema: Optional[str] = None
    target_entity: Optional[str] = None

class ApiGraph(DeterministicGraph):
    endpoints: List[ApiEndpointNode]

class DatabaseTableNode(GraphNode):
    columns: Dict[str, str]
    relations: List[Dict[str, str]]
    primary_key: Optional[str] = None

class DatabaseGraph(DeterministicGraph):
    tables: List[DatabaseTableNode]

class DependencyNode(GraphNode):
    version: str

class DependencyGraph(DeterministicGraph):
    dependencies: List[DependencyNode]
