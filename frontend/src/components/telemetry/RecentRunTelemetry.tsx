import Link from "next/link";
import type { ProjectData } from "@/app/dashboard/types/genesis";
import { toRunViewModel } from "@/lib/genesis/adapters";
import { StatusBadge } from "@/components/ui/status-badge";
import { formatDurationMs } from "./telemetry-metrics";

interface RecentRunTelemetryProps {
  projects: ProjectData[];
}

export function RecentRunTelemetry({ projects }: RecentRunTelemetryProps) {
  const recent = projects.slice(0, 8);

  return (
    <section aria-labelledby="recent-runs-heading">
      <h2
        id="recent-runs-heading"
        className="mb-3 text-sm font-semibold text-foreground"
      >
        Latest Known Runs
      </h2>
      <div className="rounded-md border border-border bg-surface-base">
        {recent.map((project) => {
          const run = toRunViewModel(project);
          const href = `/projects/${run.backendProjectId}/runs/${run.id}`;
          const duration = project.planning_report?.planning_duration_ms;

          return (
            <div
              key={project.id}
              className="flex items-center justify-between gap-4 border-b border-border px-4 py-3 last:border-b-0"
            >
              <div className="min-w-0 flex-1">
                <Link
                  href={href}
                  className="truncate text-sm font-medium text-foreground hover:text-accent"
                >
                  {run.projectName}
                </Link>
                <p className="font-mono text-xs text-[color:var(--text-tertiary)]">
                  {run.backendProjectId}
                </p>
              </div>
              <div className="flex shrink-0 items-center gap-3">
                {duration != null && (
                  <span className="font-mono text-xs text-[color:var(--text-secondary)]">
                    {formatDurationMs(duration)}
                  </span>
                )}
                <StatusBadge status={run.status} />
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
