import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { TelemetryPage } from "../src/components/telemetry/TelemetryPage";
import type { ProjectData } from "../src/app/dashboard/types/genesis";

// ── Module mock ────────────────────────────────────────────────────────────────

const useProjectsMock = vi.fn();

vi.mock("../src/app/dashboard/lib/hooks", () => ({
  useProjects: () => useProjectsMock(),
}));

// ── Fixtures ───────────────────────────────────────────────────────────────────

const PROJECT_SUCCESS: ProjectData = {
  id: "project-alpha",
  title: "Alpha Project",
  status: "SUCCESS",
  created_at: "2026-06-29T10:00:00Z",
  deployment_manifest: {
    project_id: "project-alpha",
    graph_hashes: {},
    rule_engine_score: 90,
    plugin_versions: {},
    build_status: "SUCCESS",
    deployment_hash: "dh-alpha",
    workspace_hash: "wh-alpha",
  },
};

const PROJECT_FAILED: ProjectData = {
  id: "project-beta",
  title: "Beta Project",
  status: "FAILED",
  created_at: "2026-06-28T10:00:00Z",
};

const PROJECT_WITH_REPORT: ProjectData = {
  id: "project-gamma",
  title: "Gamma Project",
  status: "SUCCESS",
  created_at: "2026-06-27T10:00:00Z",
  planning_report: {
    total_features: 4,
    total_pages: 2,
    total_apis: 3,
    total_entities: 5,
    total_components: 6,
    dependency_count: 1,
    planning_duration_ms: 2000,
    rule_validation_status: "SUCCESS",
    total_errors: 0,
    total_warnings: 0,
    failed_rules: [],
    rule_trace: [],
    graph_integrity_score: 88,
    graph_hashes: {},
    workspace_hash: "wh-gamma",
    assumptions: [],
  },
};

// ── TelemetryPage tests ────────────────────────────────────────────────────────

describe("TelemetryPage", () => {
  beforeEach(() => {
    useProjectsMock.mockReset();
  });

  // ── Structure ────────────────────────────────────────────────────────────────

  it("renders Telemetry heading", () => {
    useProjectsMock.mockReturnValue({ data: [], isLoading: false, error: null });
    render(<TelemetryPage />);
    expect(screen.getByRole("heading", { name: "Telemetry" })).toBeInTheDocument();
  });

  it("shows metadata-only scope note", () => {
    useProjectsMock.mockReturnValue({ data: [], isLoading: false, error: null });
    render(<TelemetryPage />);
    expect(screen.getByText(/metadata only/i)).toBeInTheDocument();
  });

  it("shows no live telemetry pipeline note", () => {
    useProjectsMock.mockReturnValue({ data: [], isLoading: false, error: null });
    render(<TelemetryPage />);
    expect(screen.getByText(/no live telemetry pipeline/i)).toBeInTheDocument();
  });

  // ── Loading state ────────────────────────────────────────────────────────────

  it("shows loading spinner while fetching", () => {
    useProjectsMock.mockReturnValue({ data: [], isLoading: true, error: null });
    render(<TelemetryPage />);
    expect(screen.getByText(/loading telemetry data/i)).toBeInTheDocument();
  });

  it("hides metric cards while loading", () => {
    useProjectsMock.mockReturnValue({ data: [], isLoading: true, error: null });
    render(<TelemetryPage />);
    expect(screen.queryByText("Total Projects")).not.toBeInTheDocument();
  });

  // ── Error state ──────────────────────────────────────────────────────────────

  it("shows error message when backend is unavailable", () => {
    useProjectsMock.mockReturnValue({
      data: [],
      isLoading: false,
      error: new Error("Network error"),
    });
    render(<TelemetryPage />);
    expect(screen.getByText(/cannot reach the backend/i)).toBeInTheDocument();
  });

  // ── Empty state ──────────────────────────────────────────────────────────────

  it("shows empty state when no projects exist", () => {
    useProjectsMock.mockReturnValue({ data: [], isLoading: false, error: null });
    render(<TelemetryPage />);
    expect(screen.getByText(/no telemetry data/i)).toBeInTheDocument();
  });

  // ── Metric strip ─────────────────────────────────────────────────────────────

  it("shows Total Projects metric label", () => {
    useProjectsMock.mockReturnValue({
      data: [PROJECT_SUCCESS, PROJECT_FAILED, PROJECT_WITH_REPORT],
      isLoading: false,
      error: null,
    });
    render(<TelemetryPage />);
    expect(screen.getByText("Total Projects")).toBeInTheDocument();
  });

  it("shows correct total project count", () => {
    useProjectsMock.mockReturnValue({
      data: [PROJECT_SUCCESS, PROJECT_FAILED, PROJECT_WITH_REPORT],
      isLoading: false,
      error: null,
    });
    render(<TelemetryPage />);
    expect(screen.getByText("3")).toBeInTheDocument();
  });

  it("shows Avg Planning Duration metric label", () => {
    useProjectsMock.mockReturnValue({
      data: [PROJECT_WITH_REPORT],
      isLoading: false,
      error: null,
    });
    render(<TelemetryPage />);
    expect(screen.getByText("Avg Planning Duration")).toBeInTheDocument();
  });

  it("shows formatted average planning duration when reports are available", () => {
    useProjectsMock.mockReturnValue({
      data: [PROJECT_WITH_REPORT],
      isLoading: false,
      error: null,
    });
    render(<TelemetryPage />);
    expect(screen.getAllByText("2.0s").length).toBeGreaterThanOrEqual(1);
  });

  it("shows dash for average planning duration when no reports exist", () => {
    useProjectsMock.mockReturnValue({
      data: [PROJECT_FAILED],
      isLoading: false,
      error: null,
    });
    render(<TelemetryPage />);
    expect(screen.getByText("—")).toBeInTheDocument();
  });

  // ── Status breakdown ─────────────────────────────────────────────────────────

  it("shows Status Breakdown section heading", () => {
    useProjectsMock.mockReturnValue({
      data: [PROJECT_SUCCESS, PROJECT_FAILED],
      isLoading: false,
      error: null,
    });
    render(<TelemetryPage />);
    expect(screen.getByRole("heading", { name: "Status Breakdown" })).toBeInTheDocument();
  });

  it("shows success and failed status badges in breakdown", () => {
    useProjectsMock.mockReturnValue({
      data: [PROJECT_SUCCESS, PROJECT_FAILED],
      isLoading: false,
      error: null,
    });
    render(<TelemetryPage />);
    expect(screen.getAllByLabelText(/status: success/i).length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByLabelText(/status: failed/i).length).toBeGreaterThanOrEqual(1);
  });

  // ── Capability coverage ──────────────────────────────────────────────────────

  it("shows Run Surface Availability section heading", () => {
    useProjectsMock.mockReturnValue({
      data: [PROJECT_SUCCESS],
      isLoading: false,
      error: null,
    });
    render(<TelemetryPage />);
    expect(
      screen.getByRole("heading", { name: "Run Surface Availability" })
    ).toBeInTheDocument();
  });

  it("shows planning report coverage count", () => {
    useProjectsMock.mockReturnValue({
      data: [PROJECT_WITH_REPORT],
      isLoading: false,
      error: null,
    });
    render(<TelemetryPage />);
    expect(screen.getByText("Planning Report")).toBeInTheDocument();
    expect(screen.getByText("1 / 1")).toBeInTheDocument();
  });

  it("shows artifact manifest coverage count", () => {
    useProjectsMock.mockReturnValue({
      data: [PROJECT_SUCCESS],
      isLoading: false,
      error: null,
    });
    render(<TelemetryPage />);
    expect(screen.getByText("Artifact Manifest")).toBeInTheDocument();
    expect(screen.getByText("1 / 1")).toBeInTheDocument();
  });

  // ── Recent runs ──────────────────────────────────────────────────────────────

  it("shows Latest Known Runs section heading", () => {
    useProjectsMock.mockReturnValue({
      data: [PROJECT_SUCCESS],
      isLoading: false,
      error: null,
    });
    render(<TelemetryPage />);
    expect(screen.getByRole("heading", { name: "Latest Known Runs" })).toBeInTheDocument();
  });

  it("shows project name as a link in recent runs", () => {
    useProjectsMock.mockReturnValue({
      data: [PROJECT_SUCCESS],
      isLoading: false,
      error: null,
    });
    render(<TelemetryPage />);
    expect(screen.getByRole("link", { name: "Alpha Project" })).toBeInTheDocument();
  });

  it("recent run links use backendProjectId in href", () => {
    useProjectsMock.mockReturnValue({
      data: [PROJECT_SUCCESS],
      isLoading: false,
      error: null,
    });
    render(<TelemetryPage />);
    const link = screen.getByRole("link", { name: "Alpha Project" });
    expect(link).toHaveAttribute(
      "href",
      "/projects/project-alpha/runs/project-alpha"
    );
  });

  it("shows backendProjectId below project name in recent runs", () => {
    useProjectsMock.mockReturnValue({
      data: [PROJECT_SUCCESS],
      isLoading: false,
      error: null,
    });
    render(<TelemetryPage />);
    expect(screen.getByText("project-alpha")).toBeInTheDocument();
  });

  // ── Honesty guards ───────────────────────────────────────────────────────────

  it("does not claim real-time or live metrics", () => {
    useProjectsMock.mockReturnValue({
      data: [PROJECT_SUCCESS],
      isLoading: false,
      error: null,
    });
    render(<TelemetryPage />);
    expect(screen.queryByText(/real-time/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/live metrics/i)).not.toBeInTheDocument();
  });

  it("does not show fake time-series or chart elements", () => {
    useProjectsMock.mockReturnValue({
      data: [PROJECT_SUCCESS],
      isLoading: false,
      error: null,
    });
    render(<TelemetryPage />);
    expect(screen.queryByText(/time series/i)).not.toBeInTheDocument();
    expect(screen.queryByRole("img", { name: /chart/i })).not.toBeInTheDocument();
  });
});
