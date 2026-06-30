"use client";

import { AlertTriangle, Loader2 } from "lucide-react";
import Link from "next/link";
import { useProjects } from "@/app/dashboard/lib/hooks";
import { LimitedState, RouteScaffold } from "@/components/routes/RouteScaffold";
import { CapabilityCoverage } from "./CapabilityCoverage";
import { MetricCard } from "./MetricCard";
import { RecentRunTelemetry } from "./RecentRunTelemetry";
import { StatusBreakdown } from "./StatusBreakdown";
import { deriveTelemetryMetrics, formatDurationMs } from "./telemetry-metrics";

export function TelemetryPage() {
  const { data: projects = [], isLoading, error } = useProjects();
  const metrics = deriveTelemetryMetrics(projects);

  return (
    <RouteScaffold
      eyebrow="Operations"
      title="Telemetry"
      description="Project and latest-known-run observability summary."
    >
      <div className="space-y-8">
        <p className="text-xs text-[color:var(--text-tertiary)]">
          Telemetry currently summarizes project and latest-known-run metadata only. No live
          telemetry pipeline, time-series data, or analytics backend exists.
        </p>

        {isLoading ? (
          <div className="flex items-center gap-2 py-8 text-sm text-[color:var(--text-secondary)]">
            <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
            <span>Loading telemetry data…</span>
          </div>
        ) : error ? (
          <div className="flex items-start gap-3 rounded-lg border border-[color:var(--error)] bg-surface-raised px-4 py-3">
            <AlertTriangle
              className="mt-0.5 h-4 w-4 shrink-0 text-[color:var(--error)]"
              aria-hidden="true"
            />
            <span className="text-sm text-[color:var(--error)]">
              Cannot reach the backend. Telemetry data is unavailable.
            </span>
          </div>
        ) : projects.length === 0 ? (
          <LimitedState
            title="No telemetry data"
            description="No backend project records are available. Compile a specification to generate project data."
            action={
              <Link
                href="/compiler"
                className="inline-flex items-center rounded-sm bg-accent px-3 py-2 text-sm font-medium text-accent-foreground hover:bg-accent/90"
              >
                Open Compiler
              </Link>
            }
          />
        ) : (
          <>
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
              <MetricCard label="Total Projects" value={metrics.totalProjects} />
              <MetricCard
                label="Planning Reports"
                value={metrics.planningReportCount}
                note={`of ${metrics.totalProjects} projects`}
              />
              <MetricCard
                label="Artifact Manifests"
                value={metrics.artifactManifestCount}
                note={`of ${metrics.totalProjects} projects`}
              />
              <MetricCard
                label="Avg Planning Duration"
                value={
                  metrics.avgPlanningDurationMs != null
                    ? formatDurationMs(metrics.avgPlanningDurationMs)
                    : "—"
                }
                note={
                  metrics.avgPlanningDurationMs != null
                    ? "from available reports"
                    : "no planning reports"
                }
              />
            </div>

            <div className="grid gap-6 md:grid-cols-2">
              <StatusBreakdown
                statusCounts={metrics.statusCounts}
                total={metrics.totalProjects}
              />
              <CapabilityCoverage
                total={metrics.totalProjects}
                planningReportCount={metrics.planningReportCount}
                architectureGraphCount={metrics.architectureGraphCount}
                artifactManifestCount={metrics.artifactManifestCount}
                compilationTraceCount={metrics.compilationTraceCount}
              />
            </div>

            <RecentRunTelemetry projects={projects} />
          </>
        )}
      </div>
    </RouteScaffold>
  );
}
