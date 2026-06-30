"use client";

import Link from "next/link";
import { AlertTriangle, FolderKanban, Info, Loader2, Package, PlayCircle, Terminal } from "lucide-react";
import { useProjects } from "@/app/dashboard/lib/hooks";
import { toProjectViewModel } from "@/lib/genesis/adapters";
import type { ProjectData } from "@/app/dashboard/types/genesis";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/status-badge";
import { LimitedState, RouteScaffold } from "@/components/routes/RouteScaffold";

// ── Stats strip ───────────────────────────────────────────────────────────────

type StatTile = { label: string; value: number; icon: React.ElementType };

function deriveStats(projects: ProjectData[]): StatTile[] {
  return [
    { label: "Projects", value: projects.length, icon: FolderKanban },
    { label: "Active Builds", value: projects.filter((p) => p.status === "RUNNING").length, icon: PlayCircle },
    { label: "Failed", value: projects.filter((p) => p.status === "FAILED").length, icon: AlertTriangle },
    {
      label: "Deployed",
      value: projects.filter((p) => Boolean(p.deployment_manifest)).length,
      icon: Package,
    },
  ];
}

function StatsStrip({ projects }: { projects: ProjectData[] }) {
  const stats = deriveStats(projects);
  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
      {stats.map(({ label, value, icon: Icon }) => (
        <div
          key={label}
          className="flex items-center gap-3 rounded-lg border border-border bg-surface-raised px-4 py-3"
        >
          <Icon className="h-4 w-4 shrink-0 text-[color:var(--text-tertiary)]" aria-hidden="true" />
          <div>
            <p className="text-xs text-[color:var(--text-tertiary)]">{label}</p>
            <p className="font-mono text-xl font-bold tabular-nums text-foreground">{value}</p>
          </div>
        </div>
      ))}
    </div>
  );
}

// ── Recent projects ───────────────────────────────────────────────────────────

function RecentProjectsGrid({ projects }: { projects: ProjectData[] }) {
  const viewModels = projects.slice(0, 6).map(toProjectViewModel);

  return (
    <section>
      <div className="mb-3 flex items-center justify-between gap-4">
        <h2 className="text-sm font-semibold text-foreground">Recent Projects</h2>
        <Link
          href="/projects"
          className="text-xs text-[color:var(--text-secondary)] hover:text-foreground"
        >
          View all
        </Link>
      </div>

      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
        {viewModels.map((project) => {
          const run = project.lastRun;
          const href = run
            ? `/projects/${project.id}/runs/${run.id}`
            : `/projects/${project.id}`;
          return (
            <Link key={project.id} href={href} className="block">
              <Card className="h-full transition-colors hover:border-border-accent hover:bg-surface-hover">
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between gap-2">
                    <CardTitle className="text-base">{project.name}</CardTitle>
                    {run && <StatusBadge status={run.status} />}
                  </div>
                  <CardDescription>
                    <code className="font-mono text-xs">{project.backendProjectId}</code>
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-xs text-[color:var(--text-tertiary)]">Latest known Run</p>
                </CardContent>
              </Card>
            </Link>
          );
        })}
      </div>

      <div className="mt-4 flex items-start gap-2 rounded-md border border-border bg-surface-raised px-3 py-2 text-xs text-[color:var(--text-secondary)]">
        <Info className="mt-0.5 h-3.5 w-3.5 shrink-0 text-[color:var(--text-tertiary)]" aria-hidden="true" />
        <span>
          Each project currently exposes its latest known Run only. Real Run history requires a
          future backend endpoint.
        </span>
      </div>
    </section>
  );
}

// ── Header actions ────────────────────────────────────────────────────────────

function HeaderActions() {
  return (
    <div className="flex shrink-0 flex-wrap gap-2">
      <Link
        href="/compiler"
        className="inline-flex items-center gap-2 rounded-sm bg-accent px-4 py-2 text-sm font-medium text-accent-foreground hover:bg-accent-hover"
      >
        <Terminal className="h-4 w-4" aria-hidden="true" />
        Open Compiler
      </Link>
      <Link
        href="/projects"
        className="inline-flex items-center gap-2 rounded-sm border border-border bg-surface-raised px-4 py-2 text-sm font-medium text-foreground hover:bg-surface-hover"
      >
        <FolderKanban className="h-4 w-4" aria-hidden="true" />
        View Projects
      </Link>
    </div>
  );
}

// ── Main export ───────────────────────────────────────────────────────────────

export function ControlPlaneHome() {
  const { data: projects = [], isLoading, error } = useProjects();

  return (
    <RouteScaffold
      eyebrow="Platform"
      title="Genesis Engine"
      description="Specification Compiler Platform"
      actions={<HeaderActions />}
    >
      {isLoading ? (
        <div className="flex min-h-64 items-center justify-center text-[color:var(--text-secondary)]">
          <Loader2 className="mr-2 h-4 w-4 animate-spin" aria-hidden="true" />
          Loading projects...
        </div>
      ) : error ? (
        <div className="flex items-start gap-3 rounded-lg border border-[color:var(--error)] bg-surface-raised px-4 py-3 text-sm">
          <AlertTriangle
            className="mt-0.5 h-4 w-4 shrink-0 text-[color:var(--error)]"
            aria-hidden="true"
          />
          <span className="text-[color:var(--error)]">
            Cannot reach the backend.{" "}
            <span className="font-mono text-xs text-[color:var(--text-secondary)]">
              Ensure the Genesis backend is running on the configured API URL.
            </span>
          </span>
        </div>
      ) : projects.length === 0 ? (
        <LimitedState
          title="No projects yet"
          description="No backend project records are available. Compile a specification to create the first project."
          action={
            <Link
              href="/compiler"
              className="inline-flex rounded-sm bg-accent px-3 py-2 text-sm font-medium text-accent-foreground hover:bg-accent-hover"
            >
              Open Compiler
            </Link>
          }
        />
      ) : (
        <div className="space-y-8">
          <StatsStrip projects={projects} />
          <RecentProjectsGrid projects={projects} />
        </div>
      )}
    </RouteScaffold>
  );
}
