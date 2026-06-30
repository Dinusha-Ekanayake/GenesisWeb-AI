import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { GlobalSearchPage } from "../src/components/search/GlobalSearchPage";
import type { ProjectData } from "../src/app/dashboard/types/genesis";

// ── Module mocks ──────────────────────────────────────────────────────────────

const mockUseProjects = vi.fn();
vi.mock("../src/app/dashboard/lib/hooks", () => ({
  useProjects: () => mockUseProjects(),
}));

// ── Test fixtures ─────────────────────────────────────────────────────────────

const PROJECT_ALPHA: ProjectData = {
  id: "project-alpha",
  title: "Alpha Project",
  status: "SUCCESS",
  created_at: "2026-06-30T10:00:00Z",
  spec: {
    project_id: "project-alpha",
    name: "Alpha Spec",
    description: "First test specification",
    pages: [],
    components: [],
  },
  deployment_manifest: {
    project_id: "project-alpha",
    graph_hashes: {},
    rule_engine_score: 95,
    plugin_versions: {},
    build_status: "COMPLETED",
    deployment_hash: "hash-1",
    workspace_hash: "ws-hash-1",
  },
};

const PROJECT_FAILED: ProjectData = {
  id: "project-beta",
  title: "Beta Project",
  status: "FAILED",
  created_at: "2026-06-30T09:00:00Z",
};

const PROJECT_WITH_REPORT: ProjectData = {
  id: "project-gamma",
  title: "Gamma Project",
  status: "SUCCESS",
  created_at: "2026-06-30T11:00:00Z",
  spec: {
    project_id: "project-gamma",
    name: "Gamma Spec",
    description: "Has planning report",
    pages: [],
    components: [],
  },
  planning_report: {
    rule_validation_status: "PASSED",
    integrity_score: 88,
    planning_duration_ms: 2000,
    features: 4,
    pages: 2,
    api_endpoints: 3,
    db_entities: 5,
    components: 6,
    dependencies: 1,
    errors: 0,
    warnings: 0,
    rule_results: [],
  },
};

// ── GlobalSearchPage tests ────────────────────────────────────────────────────

describe("GlobalSearchPage", () => {
  beforeEach(() => {
    mockUseProjects.mockReset();
  });

  // Structure
  it("renders Search heading", () => {
    mockUseProjects.mockReturnValue({ data: [], isLoading: false, error: null });
    render(<GlobalSearchPage />);
    expect(screen.getByRole("heading", { name: "Search" })).toBeInTheDocument();
  });

  it("renders a search input with accessible label", () => {
    mockUseProjects.mockReturnValue({ data: [], isLoading: false, error: null });
    render(<GlobalSearchPage />);
    expect(screen.getByLabelText("Search")).toBeInTheDocument();
  });

  it("search input placeholder mentions projects, runs, and statuses", () => {
    mockUseProjects.mockReturnValue({ data: [], isLoading: false, error: null });
    render(<GlobalSearchPage />);
    const input = screen.getByLabelText("Search");
    expect(input).toHaveAttribute("placeholder", expect.stringMatching(/projects/i));
    expect(input).toHaveAttribute("placeholder", expect.stringMatching(/runs/i));
    expect(input).toHaveAttribute("placeholder", expect.stringMatching(/status/i));
  });

  // Scope disclaimer — always present
  it("shows scope disclaimer that search covers metadata only", () => {
    mockUseProjects.mockReturnValue({ data: [], isLoading: false, error: null });
    render(<GlobalSearchPage />);
    expect(
      screen.getByText(/Search currently covers projects and latest-known-run metadata only/i)
    ).toBeInTheDocument();
  });

  it("scope disclaimer explicitly states file contents are not indexed", () => {
    mockUseProjects.mockReturnValue({ data: [], isLoading: false, error: null });
    render(<GlobalSearchPage />);
    expect(screen.getByText(/File contents.*not indexed/i)).toBeInTheDocument();
  });

  // Loading state
  it("shows loading state while projects load", () => {
    mockUseProjects.mockReturnValue({ data: [], isLoading: true, error: null });
    render(<GlobalSearchPage />);
    expect(screen.getByText(/Loading projects/i)).toBeInTheDocument();
  });

  it("does not show search results while loading", () => {
    mockUseProjects.mockReturnValue({ data: [], isLoading: true, error: null });
    render(<GlobalSearchPage />);
    expect(screen.queryByRole("list", { name: "Search results" })).not.toBeInTheDocument();
  });

  // Error state
  it("shows backend error message when useProjects fails", () => {
    mockUseProjects.mockReturnValue({
      data: [],
      isLoading: false,
      error: { message: "Network error" },
    });
    render(<GlobalSearchPage />);
    expect(screen.getByText(/Cannot reach the backend/i)).toBeInTheDocument();
  });

  // Empty query state
  it("shows explanatory state when query is empty", () => {
    mockUseProjects.mockReturnValue({ data: [PROJECT_ALPHA], isLoading: false, error: null });
    render(<GlobalSearchPage />);
    expect(screen.getByText(/Project names and IDs/i)).toBeInTheDocument();
  });

  it("shows what can be searched in empty query state", () => {
    mockUseProjects.mockReturnValue({ data: [PROJECT_ALPHA], isLoading: false, error: null });
    render(<GlobalSearchPage />);
    expect(screen.getByText(/Statuses/i)).toBeInTheDocument();
    expect(screen.getByText(/Specification names/i)).toBeInTheDocument();
  });

  // Results with real data
  it("shows project results matching the query", () => {
    mockUseProjects.mockReturnValue({
      data: [PROJECT_ALPHA],
      isLoading: false,
      error: null,
    });
    render(<GlobalSearchPage />);
    fireEvent.change(screen.getByLabelText("Search"), { target: { value: "alpha" } });
    expect(screen.getByText("Alpha Spec")).toBeInTheDocument();
  });

  it("shows backend project ID in result card", () => {
    mockUseProjects.mockReturnValue({ data: [PROJECT_ALPHA], isLoading: false, error: null });
    render(<GlobalSearchPage />);
    fireEvent.change(screen.getByLabelText("Search"), { target: { value: "alpha" } });
    expect(screen.getByText(/ID: project-alpha/)).toBeInTheDocument();
  });

  it("shows spec description in result card when present", () => {
    mockUseProjects.mockReturnValue({ data: [PROJECT_ALPHA], isLoading: false, error: null });
    render(<GlobalSearchPage />);
    fireEvent.change(screen.getByLabelText("Search"), { target: { value: "alpha" } });
    expect(screen.getByText("First test specification")).toBeInTheDocument();
  });

  // Filtering — by project name
  it("filters results by project name (case-insensitive)", () => {
    mockUseProjects.mockReturnValue({
      data: [PROJECT_ALPHA, PROJECT_FAILED],
      isLoading: false,
      error: null,
    });
    render(<GlobalSearchPage />);
    fireEvent.change(screen.getByLabelText("Search"), { target: { value: "Beta" } });
    expect(screen.getByText("Beta Project")).toBeInTheDocument();
    expect(screen.queryByText("Alpha Spec")).not.toBeInTheDocument();
  });

  // Filtering — by backend project ID
  it("filters results by backend project ID", () => {
    mockUseProjects.mockReturnValue({
      data: [PROJECT_ALPHA, PROJECT_FAILED],
      isLoading: false,
      error: null,
    });
    render(<GlobalSearchPage />);
    fireEvent.change(screen.getByLabelText("Search"), { target: { value: "project-alpha" } });
    expect(screen.getByText("Alpha Spec")).toBeInTheDocument();
    expect(screen.queryByText("Beta Project")).not.toBeInTheDocument();
  });

  // Filtering — by status
  it("filters results by status string", () => {
    mockUseProjects.mockReturnValue({
      data: [PROJECT_ALPHA, PROJECT_FAILED],
      isLoading: false,
      error: null,
    });
    render(<GlobalSearchPage />);
    fireEvent.change(screen.getByLabelText("Search"), { target: { value: "failed" } });
    expect(screen.getByText("Beta Project")).toBeInTheDocument();
    expect(screen.queryByText("Alpha Spec")).not.toBeInTheDocument();
  });

  // Result links use backendProjectId
  it("View Run link uses backendProjectId as both project and run segment", () => {
    mockUseProjects.mockReturnValue({ data: [PROJECT_ALPHA], isLoading: false, error: null });
    render(<GlobalSearchPage />);
    fireEvent.change(screen.getByLabelText("Search"), { target: { value: "alpha" } });
    const viewRunLink = screen.getByRole("link", {
      name: /View Run for Alpha Spec/i,
    });
    expect(viewRunLink).toHaveAttribute(
      "href",
      "/projects/project-alpha/runs/project-alpha"
    );
  });

  // Surface links use backendProjectId
  it("Artifacts surface link uses backendProjectId when manifest present", () => {
    mockUseProjects.mockReturnValue({ data: [PROJECT_ALPHA], isLoading: false, error: null });
    render(<GlobalSearchPage />);
    fireEvent.change(screen.getByLabelText("Search"), { target: { value: "alpha" } });
    const artifactsLink = screen.getByRole("link", { name: "Artifacts" });
    expect(artifactsLink).toHaveAttribute(
      "href",
      "/projects/project-alpha/runs/project-alpha/artifacts"
    );
  });

  it("Planning Report surface link uses backendProjectId when planning_report present", () => {
    mockUseProjects.mockReturnValue({
      data: [PROJECT_WITH_REPORT],
      isLoading: false,
      error: null,
    });
    render(<GlobalSearchPage />);
    fireEvent.change(screen.getByLabelText("Search"), { target: { value: "gamma" } });
    const reportLink = screen.getByRole("link", { name: "Planning Report" });
    expect(reportLink).toHaveAttribute(
      "href",
      "/projects/project-gamma/runs/project-gamma/report"
    );
  });

  it("does not show surface links for capabilities not present", () => {
    mockUseProjects.mockReturnValue({ data: [PROJECT_FAILED], isLoading: false, error: null });
    render(<GlobalSearchPage />);
    fireEvent.change(screen.getByLabelText("Search"), { target: { value: "beta" } });
    // PROJECT_FAILED has no manifest, no planning_report, no architecture, no trace
    expect(screen.queryByRole("link", { name: "Planning Report" })).not.toBeInTheDocument();
    expect(screen.queryByRole("link", { name: "Architecture" })).not.toBeInTheDocument();
    expect(screen.queryByRole("link", { name: "Artifacts" })).not.toBeInTheDocument();
  });

  // No results
  it("shows no-results state when query matches nothing", () => {
    mockUseProjects.mockReturnValue({ data: [PROJECT_ALPHA], isLoading: false, error: null });
    render(<GlobalSearchPage />);
    fireEvent.change(screen.getByLabelText("Search"), { target: { value: "zzznomatch" } });
    expect(screen.getByText(/No results/i)).toBeInTheDocument();
    expect(screen.queryByText("Alpha Spec")).not.toBeInTheDocument();
  });

  // No fake data
  it("does not show fake or invented results when projects list is empty", () => {
    mockUseProjects.mockReturnValue({ data: [], isLoading: false, error: null });
    render(<GlobalSearchPage />);
    fireEvent.change(screen.getByLabelText("Search"), { target: { value: "demo" } });
    expect(screen.queryByText(/demo_project/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/fake/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/run #\d/i)).not.toBeInTheDocument();
  });

  it("does not claim to search file contents or full Run history", () => {
    mockUseProjects.mockReturnValue({ data: [PROJECT_ALPHA], isLoading: false, error: null });
    render(<GlobalSearchPage />);
    // The disclaimer explicitly says what is NOT searchable
    expect(screen.getByText(/File contents.*not indexed/i)).toBeInTheDocument();
    expect(screen.queryByText(/searching.*files/i)).not.toBeInTheDocument();
  });
});
