import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { RunPlanningReport } from "../src/components/run/RunPlanningReport";
import { RunRouteScaffold } from "../src/components/routes/RunRouteScaffold";
import type { RunViewModel } from "../src/lib/genesis/view-models";
import type { PlanningReport } from "../src/app/dashboard/types/genesis";

// ── Module mocks ──────────────────────────────────────────────────────────────

const mockUseProject = vi.fn();
vi.mock("../src/app/dashboard/lib/hooks", () => ({
  useProject: (...args: any[]) => mockUseProject(...args),
}));

// ── Test fixtures ─────────────────────────────────────────────────────────────

const PLANNING_REPORT: PlanningReport = {
  total_features: 12,
  total_pages: 4,
  total_apis: 8,
  total_entities: 3,
  total_components: 10,
  dependency_count: 5,
  planning_duration_ms: 1500,
  rule_validation_status: "SUCCESS",
  total_errors: 0,
  total_warnings: 2,
  failed_rules: [],
  rule_trace: [
    {
      rule_id: "rule-001",
      rule_name: "API Coverage Check",
      status: "PASS",
      message: "All APIs are properly documented.",
    },
    {
      rule_id: "rule-002",
      rule_name: "Entity Validation",
      status: "WARN",
      message: "Some entities lack descriptions.",
    },
  ],
  graph_integrity_score: 95,
  rule_coverage: {
    api_coverage: 85,
    db_coverage: 90,
    ui_coverage: 78,
    overall_score: 84,
  },
  graph_hashes: { endpoints: "abc123", pages: "def456" },
  workspace_hash: "ws-hash-xyz",
  assumptions: ["All users are authenticated", "Database is PostgreSQL"],
};

const RUN_WITH_REPORT: RunViewModel = {
  id: "project-1",
  backendProjectId: "project-1",
  source: "backend-project-as-latest-run",
  projectId: "project-1",
  projectName: "Test Project",
  status: "SUCCESS",
  capabilities: {
    hasExplicitRunHistory: false,
    hasPlanningReport: true,
    hasArchitectureGraphs: false,
    hasWorkspaceFiles: false,
    hasArtifactManifest: false,
    hasCompilationTrace: false,
  },
  planningReport: PLANNING_REPORT,
};

const RUN_WITHOUT_REPORT: RunViewModel = {
  id: "project-1",
  backendProjectId: "project-1",
  source: "backend-project-as-latest-run",
  projectId: "project-1",
  projectName: "Test Project",
  status: "UNKNOWN",
  capabilities: {
    hasExplicitRunHistory: false,
    hasPlanningReport: false,
    hasArchitectureGraphs: false,
    hasWorkspaceFiles: false,
    hasArtifactManifest: false,
    hasCompilationTrace: false,
  },
};

// ── RunPlanningReport — pure component tests ──────────────────────────────────

describe("RunPlanningReport", () => {
  it("shows unavailable state when report is absent", () => {
    render(<RunPlanningReport run={RUN_WITHOUT_REPORT} />);

    expect(screen.getByText(/Planning report not available/i)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Open Compiler/i })).toHaveAttribute(
      "href",
      "/compiler"
    );
  });

  it("renders rule validation status", () => {
    render(<RunPlanningReport run={RUN_WITH_REPORT} />);

    expect(screen.getByText(/Rule Engine/i)).toBeInTheDocument();
    expect(screen.getByText("SUCCESS")).toBeInTheDocument();
  });

  it("renders graph integrity score", () => {
    render(<RunPlanningReport run={RUN_WITH_REPORT} />);

    expect(screen.getByText(/Integrity score/i)).toBeInTheDocument();
    expect(screen.getByText("95")).toBeInTheDocument();
  });

  it("renders planning duration in formatted form", () => {
    render(<RunPlanningReport run={RUN_WITH_REPORT} />);

    // 1500ms → "1.50s"
    expect(screen.getByText("1.50s")).toBeInTheDocument();
  });

  it("shows all 8 metric tiles with backend-sourced values", () => {
    render(<RunPlanningReport run={RUN_WITH_REPORT} />);

    expect(screen.getByText("Features")).toBeInTheDocument();
    expect(screen.getByText("Pages")).toBeInTheDocument();
    expect(screen.getByText("APIs")).toBeInTheDocument();
    expect(screen.getByText("Entities")).toBeInTheDocument();
    expect(screen.getByText("Components")).toBeInTheDocument();
    expect(screen.getByText("Dependencies")).toBeInTheDocument();
    expect(screen.getByText("Errors")).toBeInTheDocument();
    expect(screen.getByText("Warnings")).toBeInTheDocument();
    // Spot-check values: features=12, pages=4, apis=8, components=10
    expect(screen.getByText("12")).toBeInTheDocument();
    expect(screen.getByText("10")).toBeInTheDocument();
  });

  it("renders rule coverage section when rule_coverage is present", () => {
    render(<RunPlanningReport run={RUN_WITH_REPORT} />);

    expect(screen.getByText("Rule Coverage")).toBeInTheDocument();
    expect(screen.getByText("API Coverage")).toBeInTheDocument();
    expect(screen.getByText("85")).toBeInTheDocument(); // api_coverage
    expect(screen.getByText("Overall Score")).toBeInTheDocument();
  });

  it("hides rule coverage section when rule_coverage is absent", () => {
    const runWithoutCoverage: RunViewModel = {
      ...RUN_WITH_REPORT,
      planningReport: { ...PLANNING_REPORT, rule_coverage: undefined },
    };

    render(<RunPlanningReport run={runWithoutCoverage} />);

    expect(screen.queryByText("Rule Coverage")).not.toBeInTheDocument();
    expect(screen.queryByText("API Coverage")).not.toBeInTheDocument();
  });

  it("renders planning assumptions when present", () => {
    render(<RunPlanningReport run={RUN_WITH_REPORT} />);

    expect(screen.getByText("Planning Assumptions")).toBeInTheDocument();
    expect(screen.getByText("All users are authenticated")).toBeInTheDocument();
    expect(screen.getByText("Database is PostgreSQL")).toBeInTheDocument();
  });

  it("hides assumptions section when the array is empty", () => {
    const runWithoutAssumptions: RunViewModel = {
      ...RUN_WITH_REPORT,
      planningReport: { ...PLANNING_REPORT, assumptions: [] },
    };

    render(<RunPlanningReport run={runWithoutAssumptions} />);

    expect(screen.queryByText("Planning Assumptions")).not.toBeInTheDocument();
  });

  it("renders rule trace section with rule names, IDs, and status badges", () => {
    render(<RunPlanningReport run={RUN_WITH_REPORT} />);

    expect(screen.getByText("Rule Execution Trace")).toBeInTheDocument();
    expect(screen.getByText("API Coverage Check")).toBeInTheDocument();
    expect(screen.getByText("rule-001")).toBeInTheDocument();
    expect(screen.getByText("Entity Validation")).toBeInTheDocument();
    expect(screen.getByText("rule-002")).toBeInTheDocument();
    // Status badges
    expect(screen.getByText("PASS")).toBeInTheDocument();
    expect(screen.getByText("WARN")).toBeInTheDocument();
  });

  it("renders trace entry messages", () => {
    render(<RunPlanningReport run={RUN_WITH_REPORT} />);

    expect(screen.getByText("All APIs are properly documented.")).toBeInTheDocument();
    expect(screen.getByText("Some entities lack descriptions.")).toBeInTheDocument();
  });

  it("renders graph hashes and workspace hash", () => {
    render(<RunPlanningReport run={RUN_WITH_REPORT} />);

    expect(screen.getByText("Graph Hashes")).toBeInTheDocument();
    expect(screen.getByText("ws-hash-xyz")).toBeInTheDocument();
    expect(screen.getByText("abc123")).toBeInTheDocument();
    expect(screen.getByText("def456")).toBeInTheDocument();
  });

  it("does not show Failed Rules section when all rules pass", () => {
    render(<RunPlanningReport run={RUN_WITH_REPORT} />);

    // PLANNING_REPORT.failed_rules is empty
    expect(screen.queryByText("Failed Rules")).not.toBeInTheDocument();
  });

  it("shows Failed Rules section with rule names when failures exist", () => {
    const runWithFailures: RunViewModel = {
      ...RUN_WITH_REPORT,
      planningReport: {
        ...PLANNING_REPORT,
        rule_validation_status: "FAILED",
        total_errors: 2,
        failed_rules: ["API_COVERAGE_FAIL", "ENTITY_MISSING_FIELD"],
      },
    };

    render(<RunPlanningReport run={runWithFailures} />);

    expect(screen.getByText("Failed Rules")).toBeInTheDocument();
    expect(screen.getByText("API_COVERAGE_FAIL")).toBeInTheDocument();
    expect(screen.getByText("ENTITY_MISSING_FIELD")).toBeInTheDocument();
  });

  it("shows FAILED status badge in rule trace when a rule failed", () => {
    const runWithFailedRule: RunViewModel = {
      ...RUN_WITH_REPORT,
      planningReport: {
        ...PLANNING_REPORT,
        rule_trace: [
          {
            rule_id: "rule-003",
            rule_name: "DB Schema Check",
            status: "FAIL",
            message: "Missing required entity relationships.",
          },
        ],
      },
    };

    render(<RunPlanningReport run={runWithFailedRule} />);

    expect(screen.getByText("FAIL")).toBeInTheDocument();
    expect(screen.getByText("Missing required entity relationships.")).toBeInTheDocument();
  });

  it("does not render any report data when planningReport is absent", () => {
    render(<RunPlanningReport run={RUN_WITHOUT_REPORT} />);

    // No metric labels should appear — only the unavailable state
    expect(screen.queryByText("Features")).not.toBeInTheDocument();
    expect(screen.queryByText("Rule Execution Trace")).not.toBeInTheDocument();
    expect(screen.queryByText("Graph Hashes")).not.toBeInTheDocument();
    expect(screen.queryByText("Planning Assumptions")).not.toBeInTheDocument();
  });

  it("shows empty trace message when rule_trace array is empty", () => {
    const runWithEmptyTrace: RunViewModel = {
      ...RUN_WITH_REPORT,
      planningReport: { ...PLANNING_REPORT, rule_trace: [] },
    };

    render(<RunPlanningReport run={runWithEmptyTrace} />);

    expect(screen.getByText("Rule Execution Trace")).toBeInTheDocument();
    expect(screen.getByText("No rule trace entries.")).toBeInTheDocument();
  });
});

// ── RunRouteScaffold — report surface integration ─────────────────────────────

describe("RunRouteScaffold report surface", () => {
  beforeEach(() => {
    mockUseProject.mockReset();
  });

  it("renders planning report content when project has a planning report", () => {
    mockUseProject.mockReturnValue({
      data: {
        id: "project-1",
        title: "Test Project",
        status: "SUCCESS",
        created_at: "2026-06-29T10:00:00Z",
        planning_report: PLANNING_REPORT,
      },
      isLoading: false,
      error: null,
    });

    render(<RunRouteScaffold projectId="project-1" runId="project-1" surface="report" />);

    expect(screen.getByText(/Rule Engine/i)).toBeInTheDocument();
    expect(screen.getByText("SUCCESS")).toBeInTheDocument();
    expect(screen.getByText("Rule Execution Trace")).toBeInTheDocument();
  });

  it("shows unavailable state when project has no planning report", () => {
    mockUseProject.mockReturnValue({
      data: {
        id: "project-1",
        title: "Test Project",
        status: "UNKNOWN",
        created_at: "2026-06-29T10:00:00Z",
      },
      isLoading: false,
      error: null,
    });

    render(<RunRouteScaffold projectId="project-1" runId="project-1" surface="report" />);

    expect(screen.getByText(/Planning report not available/i)).toBeInTheDocument();
    expect(screen.queryByText("Rule Engine")).not.toBeInTheDocument();
  });
});
