export interface ProjectSpecification {
  project_id: string;
  name: string;
  description: string;
  pages: string[];
  components: string[];
}

export interface RuleExecutionTrace {
  rule_id: string;
  rule_name: string;
  status: "PASS" | "FAIL" | "WARN";
  message: string;
  context?: any;
}

export interface RuleCoverageReport {
  api_coverage: number;
  db_coverage: number;
  ui_coverage: number;
  overall_score: number;
}

export interface PlanningReport {
  total_features: number;
  total_pages: number;
  total_apis: number;
  total_entities: number;
  total_components: number;
  dependency_count: number;
  planning_duration_ms: number;
  rule_validation_status: "SUCCESS" | "FAILED";
  total_errors: number;
  total_warnings: number;
  failed_rules: string[];
  rule_trace: RuleExecutionTrace[];
  graph_integrity_score: number;
  rule_coverage?: RuleCoverageReport;
  graph_hashes: Record<string, string>;
  workspace_hash: string;
  assumptions: string[];
}

export interface DeploymentManifest {
  project_id: string;
  graph_hashes: Record<string, string>;
  rule_engine_score: number;
  plugin_versions: Record<string, string>;
  build_status: string;
  deployment_hash: string;
  workspace_hash: string;
}

export interface ExecutionTrace {
  timestamp: string;
  event: string;
  details: any;
}

export interface ProjectData {
  id: string;
  title: string;
  status: string;
  created_at: string;
  spec?: ProjectSpecification;
  planning_report?: PlanningReport;
  deployment_manifest?: DeploymentManifest;
  execution_trace?: ExecutionTrace[];
}
