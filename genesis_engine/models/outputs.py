from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class ArchitectureDecision(BaseModel):
    decision: str
    reason: str
    source: str
    affected_graphs: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ArchitectureDecisionRecord(BaseModel):
    decisions: List[ArchitectureDecision] = Field(default_factory=list)

class GenerationStep(BaseModel):
    id: str
    description: str
    target_plugin: str
    dependencies: List[str] = Field(default_factory=list)
    execution_priority: int
    estimated_outputs: List[str] = Field(default_factory=list)
    target_workspace_path: str

class GenerationPlan(BaseModel):
    steps: List[GenerationStep]

class ValidationError(BaseModel):
    code: str
    message: str
    node_id: str

class ValidationReport(BaseModel):
    is_valid: bool
    errors: List[ValidationError]
    warnings: List[str]

class RuleSeverity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"

class RuleCategory(str, Enum):
    DATABASE = "DATABASE"
    API = "API"
    UI = "UI"
    CROSS_GRAPH = "CROSS_GRAPH"

class RuleResult(BaseModel):
    rule_id: str
    severity: RuleSeverity
    message: str
    affected_nodes: List[str] = Field(default_factory=list)

class RuleExecutionTrace(BaseModel):
    rule_id: str
    status: RuleSeverity
    affected_nodes: List[str]
    execution_time_ms: int

class RuleCoverageReport(BaseModel):
    missing_graph_rules: List[str] = Field(default_factory=list)
    untriggered_rules: List[str] = Field(default_factory=list)

class PlannerMetrics(BaseModel):
    execution_time_ms: int = 0
    nodes_generated: int = 0
    validation_errors: int = 0
    warnings: int = 0

class PlanningReport(BaseModel):
    total_features: int = 0
    total_pages: int = 0
    total_apis: int = 0
    total_entities: int = 0
    total_components: int = 0
    dependency_count: int = 0
    planning_duration_ms: int = 0
    
    rule_validation_status: str = "PENDING"
    total_errors: int = 0
    total_warnings: int = 0
    failed_rules: List[RuleResult] = Field(default_factory=list)
    rule_trace: List[RuleExecutionTrace] = Field(default_factory=list)
    graph_integrity_score: int = 100
    rule_coverage: Optional[RuleCoverageReport] = None
    
    graph_hashes: Dict[str, str] = Field(default_factory=dict)
    workspace_hash: str = ""
    assumptions: List[str] = Field(default_factory=list)

class FileArtifact(BaseModel):
    path: str
    content: str

class DeploymentManifest(BaseModel):
    project_id: str
    generation_timestamp: datetime = Field(default_factory=datetime.utcnow)
    graph_hashes: Dict[str, str] = Field(default_factory=dict)
    rule_engine_score: int
    plugin_versions: Dict[str, str] = Field(default_factory=dict)
    build_status: str
    deployment_hash: str
    workspace_hash: str = ""
