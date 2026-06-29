"use client";

import Link from "next/link";
import { CheckCircle2, Loader2, ServerCrash } from "lucide-react";
import { useProject } from "@/app/dashboard/lib/hooks";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/status-badge";
import { toRunViewModel } from "@/lib/genesis/adapters";
import type { RunViewModel } from "@/lib/genesis/view-models";
import { CapabilityBadge, LimitedState, RouteScaffold } from "./RouteScaffold";

type RunSurface = "overview" | "compiler" | "architecture" | "workspace" | "artifacts" | "report";

type RunRouteScaffoldProps = {
  projectId: string;
  runId: string;
  surface: RunSurface;
};

const surfaceCopy: Record<RunSurface, { title: string; description: string }> = {
  overview: {
    title: "Run Overview",
    description: "A Run is currently represented by the latest known backend project/workspace record.",
  },
  compiler: {
    title: "Compiler",
    description: "Compiler route shell only. The existing dashboard compiler remains the active implementation.",
  },
  architecture: {
    title: "Architecture",
    description: "Architecture route shell for graph and system inspection surfaces.",
  },
  workspace: {
    title: "Workspace",
    description: "Workspace route shell for generated files and source inspection.",
  },
  artifacts: {
    title: "Artifacts",
    description: "Artifact bundle route shell for deployment outputs.",
  },
  report: {
    title: "Planning Report",
    description: "Planning report route shell backed by available backend project data.",
  },
};

function LoadingState() {
  return (
    <div className="flex min-h-64 items-center justify-center text-[color:var(--text-secondary)]">
      <Loader2 className="mr-2 h-4 w-4 animate-spin" aria-hidden="true" />
      Loading run context...
    </div>
  );
}

function CapabilitySummary({ run }: { run: RunViewModel }) {
  return (
    <div className="flex flex-wrap gap-2">
      <CapabilityBadge enabled={run.capabilities.hasPlanningReport} label="Planning report" />
      <CapabilityBadge enabled={run.capabilities.hasArchitectureGraphs} label="Architecture" />
      <CapabilityBadge enabled={run.capabilities.hasWorkspaceFiles} label="Workspace" />
      <CapabilityBadge enabled={run.capabilities.hasArtifactManifest} label="Artifacts" />
      <CapabilityBadge enabled={run.capabilities.hasCompilationTrace} label="Trace" />
    </div>
  );
}

function Overview({ run }: { run: RunViewModel }) {
  const links = [
    ["Compiler", "compiler"],
    ["Architecture", "architecture"],
    ["Workspace", "workspace"],
    ["Artifacts", "artifacts"],
    ["Report", "report"],
  ];

  return (
    <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_320px]">
      <Card>
        <CardHeader>
          <CardTitle>{run.projectName}</CardTitle>
          <CardDescription>Latest known Run mapped from backend project `{run.backendProjectId}`.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex flex-wrap items-center gap-3">
            <StatusBadge status={run.status} />
            <span className="text-sm text-[color:var(--text-secondary)]">{run.createdAt || "Created date unavailable"}</span>
          </div>
          <CapabilitySummary run={run} />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Run Surfaces</CardTitle>
          <CardDescription>Route shells only; backend calls still use backend project/workspace IDs.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-2">
          {links.map(([label, path]) => (
            <Link key={path} href={`/projects/${run.backendProjectId}/runs/${run.id}/${path}`} className="block rounded-sm border border-border px-3 py-2 text-sm text-[color:var(--text-secondary)] hover:bg-surface-hover hover:text-foreground">
              {label}
            </Link>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}

function SurfaceContent({ run, surface }: { run: RunViewModel; surface: RunSurface }) {
  if (surface === "overview") return <Overview run={run} />;

  if (surface === "compiler") {
    const hasTrace =
      run.capabilities.hasCompilationTrace &&
      run.compilationTrace &&
      run.compilationTrace.length > 0;

    if (hasTrace) {
      return (
        <div className="space-y-4">
          <div className="flex flex-col gap-2 rounded-lg border border-border bg-surface-raised px-4 py-3 sm:flex-row sm:items-center sm:justify-between">
            <p className="text-sm text-[color:var(--text-secondary)]">
              Read-only compilation trace from{" "}
              <code className="font-mono text-xs">{run.backendProjectId}</code>.
              Backend calls use this project ID, not the URL run ID.
            </p>
            <Link
              href="/compiler"
              className="mt-2 inline-flex shrink-0 items-center gap-1.5 rounded-sm border border-border bg-surface-base px-3 py-1.5 text-xs font-medium text-foreground hover:bg-surface-hover sm:mt-0"
            >
              New compilation
            </Link>
          </div>
          <div className="relative ml-3 space-y-6 border-l-2 border-border">
            {run.compilationTrace!.map((trace, idx) => {
              const isError =
                trace.event.toLowerCase().includes("fail") ||
                (trace.details &&
                  typeof trace.details === "object" &&
                  trace.details.status === "failed");
              return (
                <div key={idx} className="relative pl-8">
                  <span className="absolute -left-[11px] top-0.5 rounded-full bg-surface-base">
                    {isError ? (
                      <ServerCrash className="h-5 w-5 text-[color:var(--error)]" aria-hidden="true" />
                    ) : (
                      <CheckCircle2 className="h-5 w-5 text-accent" aria-hidden="true" />
                    )}
                  </span>
                  <p
                    className={`text-sm font-semibold ${
                      isError ? "text-[color:var(--error)]" : "text-foreground"
                    }`}
                  >
                    {trace.event.replace(/([A-Z])/g, " $1").trim()}
                  </p>
                  <p className="mt-1 font-mono text-xs text-[color:var(--text-secondary)]">
                    {new Date(trace.timestamp).toLocaleTimeString([], {
                      hour12: false,
                      fractionalSecondDigits: 3,
                    })}
                  </p>
                  {trace.details &&
                    typeof trace.details === "object" &&
                    Object.keys(trace.details).length > 0 && (
                      <pre className="mt-2 overflow-x-auto rounded-md border border-border bg-surface-raised p-3 font-mono text-xs text-[color:var(--text-secondary)]">
                        {JSON.stringify(trace.details, null, 2)}
                      </pre>
                    )}
                </div>
              );
            })}
          </div>
        </div>
      );
    }

    return (
      <LimitedState
        title="No compilation trace available"
        description="The current backend project record does not include a stored compilation trace. Start a new compilation from the Compiler workspace."
        action={
          <Link
            href="/compiler"
            className="inline-flex rounded-sm bg-accent px-3 py-2 text-sm font-medium text-accent-foreground hover:bg-accent-hover"
          >
            Open Compiler
          </Link>
        }
      />
    );
  }

  if (surface === "architecture") {
    if (!run.capabilities.hasArchitectureGraphs) {
      return <LimitedState title="No architecture graphs available" description="The current backend project record does not include graph data for this latest known Run." />;
    }
    return (
      <Card>
        <CardHeader>
          <CardTitle>Available Graph Groups</CardTitle>
          <CardDescription>Architecture rendering is deferred; this shell exposes available graph keys only.</CardDescription>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-2">
          {Object.keys(run.architectureGraphs || {}).map((key) => <CapabilityBadge key={key} enabled label={key} />)}
        </CardContent>
      </Card>
    );
  }

  if (surface === "workspace") {
    return (
      <LimitedState
        title={run.capabilities.hasWorkspaceFiles ? "Workspace browser deferred" : "Workspace files unavailable"}
        description="The route exists, but workspace browsing remains in the legacy project detail screen until the workspace milestone is approved."
        action={<Link href={`/dashboard/project/${run.backendProjectId}`} className="inline-flex rounded-sm bg-accent px-3 py-2 text-sm font-medium text-accent-foreground hover:bg-accent-hover">Open legacy workspace</Link>}
      />
    );
  }

  if (surface === "artifacts") {
    if (!run.artifactBundle) {
      return <LimitedState title="No artifact bundle available" description="The current backend project record does not include artifact manifest or file data." />;
    }
    return (
      <Card>
        <CardHeader>
          <CardTitle>Artifact Bundle</CardTitle>
          <CardDescription>Download behavior remains on existing backend project artifact endpoints.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-2 text-sm text-[color:var(--text-secondary)]">
          <p>Workspace hash: <code>{run.artifactBundle.workspaceHash || "Unavailable"}</code></p>
          <p>Deployment hash: <code>{run.artifactBundle.deploymentHash || "Unavailable"}</code></p>
          <p>Files: {run.artifactBundle.files.length}</p>
        </CardContent>
      </Card>
    );
  }

  if (!run.planningReport) {
    return <LimitedState title="No planning report available" description="The current backend project record does not include a planning report." />;
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Planning Report Summary</CardTitle>
        <CardDescription>Detailed report rendering is deferred to a later product milestone.</CardDescription>
      </CardHeader>
      <CardContent className="grid gap-3 text-sm text-[color:var(--text-secondary)] sm:grid-cols-2 lg:grid-cols-4">
        <p>Features: {run.planningReport.total_features}</p>
        <p>Pages: {run.planningReport.total_pages}</p>
        <p>APIs: {run.planningReport.total_apis}</p>
        <p>Integrity: {run.planningReport.graph_integrity_score}</p>
      </CardContent>
    </Card>
  );
}

export function RunRouteScaffold({ projectId, runId, surface }: RunRouteScaffoldProps) {
  const { data: project, isLoading, error } = useProject(projectId);
  const copy = surfaceCopy[surface];

  if (isLoading) {
    return (
      <RouteScaffold title={copy.title} description={copy.description} eyebrow="Run">
        <LoadingState />
      </RouteScaffold>
    );
  }

  if (error || !project) {
    return (
      <RouteScaffold title={copy.title} description={copy.description} eyebrow="Run">
        <LimitedState title="Project not available" description="This route can only show Run context when the existing backend project endpoint returns data." />
      </RouteScaffold>
    );
  }

  const run = toRunViewModel(project);

  if (run.id !== runId) {
    return (
      <RouteScaffold title={copy.title} description={copy.description} eyebrow="Run">
        <LimitedState
          title="Run history is not available yet"
          description="The backend currently exposes each project as its latest known Run only. This Run ID does not match the latest backend project record."
          action={<Link href={`/projects/${projectId}/runs/${run.id}`} className="inline-flex rounded-sm bg-accent px-3 py-2 text-sm font-medium text-accent-foreground hover:bg-accent-hover">Open latest known Run</Link>}
        />
      </RouteScaffold>
    );
  }

  return (
    <RouteScaffold
      eyebrow="Run"
      title={copy.title}
      description={copy.description}
      actions={<StatusBadge status={run.status} />}
    >
      <SurfaceContent run={run} surface={surface} />
    </RouteScaffold>
  );
}
