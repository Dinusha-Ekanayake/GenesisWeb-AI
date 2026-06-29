import type { LucideIcon } from "lucide-react";
import type { RunViewModel } from "@/lib/genesis/view-models";
import Link from "next/link";
import {
  Code2,
  FileText,
  FolderOpen,
  GitBranch,
  Hash,
  Info,
  Package,
  Terminal,
} from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { StatusBadge } from "@/components/ui/status-badge";

function formatDuration(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  return `${(ms / 1000).toFixed(1)}s`;
}

// ── Summary Card ──────────────────────────────────────────────────────────────

function RunSummaryCard({ run }: { run: RunViewModel }) {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-start justify-between gap-3">
          <CardTitle>{run.projectName}</CardTitle>
          <StatusBadge status={run.status} />
        </div>
        <CardDescription>
          Latest known Run — backend project{" "}
          <code className="font-mono text-xs">{run.backendProjectId}</code>.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="space-y-0.5">
            <p className="text-xs font-semibold uppercase tracking-wider text-[color:var(--text-tertiary)]">
              Created
            </p>
            <p className="text-[color:var(--text-secondary)]">
              {run.createdAt ? new Date(run.createdAt).toLocaleString() : "Unavailable"}
            </p>
          </div>
          <div className="space-y-0.5">
            <p className="text-xs font-semibold uppercase tracking-wider text-[color:var(--text-tertiary)]">
              Duration
            </p>
            <p className="font-mono text-[color:var(--text-secondary)]">
              {run.durationMs != null ? formatDuration(run.durationMs) : "Unavailable"}
            </p>
          </div>
        </div>
        <div className="flex items-start gap-2 rounded-md border border-border bg-surface-raised px-3 py-2 text-xs text-[color:var(--text-secondary)]">
          <Info
            className="mt-0.5 h-3.5 w-3.5 shrink-0 text-[color:var(--text-tertiary)]"
            aria-hidden="true"
          />
          <span>
            Source: <code className="font-mono">{run.source}</code>. The backend currently
            exposes each project as its latest known Run. Real Run history requires a future
            backend endpoint.
          </span>
        </div>
      </CardContent>
    </Card>
  );
}

// ── Backend Identity Card ─────────────────────────────────────────────────────

function BackendIdentityCard({ run }: { run: RunViewModel }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <Hash
            className="h-4 w-4 text-[color:var(--text-tertiary)]"
            aria-hidden="true"
          />
          Backend Identity
        </CardTitle>
        <CardDescription>
          Backend API calls must use these IDs — not the URL run segment.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-3 text-sm">
        <div className="space-y-0.5">
          <p className="text-xs font-semibold uppercase tracking-wider text-[color:var(--text-tertiary)]">
            Project ID
          </p>
          <code className="block break-all font-mono text-xs text-[color:var(--text-secondary)]">
            {run.backendProjectId}
          </code>
        </div>
        <div className="space-y-0.5">
          <p className="text-xs font-semibold uppercase tracking-wider text-[color:var(--text-tertiary)]">
            Workspace ID
          </p>
          <code className="block font-mono text-xs text-[color:var(--text-secondary)]">
            {run.backendWorkspaceId ?? "Unavailable"}
          </code>
        </div>
        <div className="space-y-0.5">
          <p className="text-xs font-semibold uppercase tracking-wider text-[color:var(--text-tertiary)]">
            Run ID
          </p>
          <code className="block break-all font-mono text-xs text-[color:var(--text-secondary)]">
            {run.id}
          </code>
        </div>
      </CardContent>
    </Card>
  );
}

// ── Specification Card ────────────────────────────────────────────────────────

function SpecificationCard({ run }: { run: RunViewModel }) {
  if (!run.specification) {
    return (
      <div className="flex items-center gap-2 rounded-lg border border-border bg-surface-raised px-4 py-3 text-sm text-[color:var(--text-secondary)]">
        <Code2
          className="h-4 w-4 shrink-0 text-[color:var(--text-tertiary)]"
          aria-hidden="true"
        />
        <span>Specification not included in the backend response for this project.</span>
      </div>
    );
  }

  const { specification: spec } = run;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <Code2
            className="h-4 w-4 text-[color:var(--text-tertiary)]"
            aria-hidden="true"
          />
          Specification
        </CardTitle>
        {spec.description && <CardDescription>{spec.description}</CardDescription>}
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-4 text-sm sm:grid-cols-4">
          <div className="space-y-0.5">
            <p className="text-xs font-semibold uppercase tracking-wider text-[color:var(--text-tertiary)]">
              Spec ID
            </p>
            <code className="block break-all font-mono text-xs text-[color:var(--text-secondary)]">
              {spec.project_id}
            </code>
          </div>
          <div className="space-y-0.5">
            <p className="text-xs font-semibold uppercase tracking-wider text-[color:var(--text-tertiary)]">
              Name
            </p>
            <p className="text-[color:var(--text-secondary)]">{spec.name || "Unnamed"}</p>
          </div>
          <div className="space-y-0.5">
            <p className="text-xs font-semibold uppercase tracking-wider text-[color:var(--text-tertiary)]">
              Pages
            </p>
            <p className="font-mono text-[color:var(--text-secondary)]">
              {spec.pages?.length ?? 0}
            </p>
          </div>
          <div className="space-y-0.5">
            <p className="text-xs font-semibold uppercase tracking-wider text-[color:var(--text-tertiary)]">
              Components
            </p>
            <p className="font-mono text-[color:var(--text-secondary)]">
              {spec.components?.length ?? 0}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

// ── Surface Cards ─────────────────────────────────────────────────────────────

type SurfaceDef = {
  key: string;
  label: string;
  description: string;
  icon: LucideIcon;
  path: string;
  isAvailable: (run: RunViewModel) => boolean;
};

const SURFACES: SurfaceDef[] = [
  {
    key: "compiler",
    label: "Compiler",
    description: "Stored compilation trace from this Run.",
    icon: Terminal,
    path: "compiler",
    isAvailable: (run) => run.capabilities.hasCompilationTrace,
  },
  {
    key: "report",
    label: "Planning Report",
    description: "Rule trace, feature analysis, and integrity score.",
    icon: FileText,
    path: "report",
    isAvailable: (run) => run.capabilities.hasPlanningReport,
  },
  {
    key: "architecture",
    label: "Architecture",
    description: "System graphs and structural analysis.",
    icon: GitBranch,
    path: "architecture",
    isAvailable: (run) => run.capabilities.hasArchitectureGraphs,
  },
  {
    key: "workspace",
    label: "Workspace",
    description: "Generated source files and workspace structure.",
    icon: FolderOpen,
    path: "workspace",
    isAvailable: (run) => run.capabilities.hasWorkspaceFiles,
  },
  {
    key: "artifacts",
    label: "Artifacts",
    description: "Deployment bundle, hashes, and output files.",
    icon: Package,
    path: "artifacts",
    isAvailable: (run) => run.capabilities.hasArtifactManifest,
  },
];

function SurfaceCard({ surface, run }: { surface: SurfaceDef; run: RunViewModel }) {
  const available = surface.isAvailable(run);
  const Icon = surface.icon;
  const href = `/projects/${run.backendProjectId}/runs/${run.id}/${surface.path}`;

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-2">
          <CardTitle className="flex items-center gap-2 text-base">
            <Icon
              className="h-4 w-4 text-[color:var(--text-tertiary)]"
              aria-hidden="true"
            />
            {surface.label}
          </CardTitle>
          <Badge variant={available ? "success" : "outline"}>
            {available ? "Available" : "Unavailable"}
          </Badge>
        </div>
        <CardDescription>{surface.description}</CardDescription>
      </CardHeader>
      <CardContent>
        <Link
          href={href}
          aria-label={`Open ${surface.label}`}
          className="inline-flex items-center rounded-sm border border-border bg-surface-base px-3 py-1.5 text-xs font-medium text-foreground hover:bg-surface-hover"
        >
          Open
        </Link>
      </CardContent>
    </Card>
  );
}

// ── Main Export ───────────────────────────────────────────────────────────────

export type RunOverviewProps = {
  run: RunViewModel;
};

export function RunOverview({ run }: RunOverviewProps) {
  return (
    <div className="space-y-6">
      <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_280px]">
        <RunSummaryCard run={run} />
        <BackendIdentityCard run={run} />
      </div>

      <SpecificationCard run={run} />

      <section>
        <h2 className="mb-3 text-sm font-semibold text-foreground">Run Surfaces</h2>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {SURFACES.map((surface) => (
            <SurfaceCard key={surface.key} surface={surface} run={run} />
          ))}
        </div>
      </section>
    </div>
  );
}
