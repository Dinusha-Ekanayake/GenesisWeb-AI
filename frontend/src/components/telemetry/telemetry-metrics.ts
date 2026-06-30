import type { ProjectData } from "@/app/dashboard/types/genesis";
import { toRunCapabilities } from "@/lib/genesis/capabilities";

export interface StatusCount {
  status: string;
  count: number;
}

export interface TelemetryMetrics {
  totalProjects: number;
  statusCounts: StatusCount[];
  avgPlanningDurationMs: number | null;
  planningReportCount: number;
  architectureGraphCount: number;
  artifactManifestCount: number;
  compilationTraceCount: number;
}

export function deriveTelemetryMetrics(projects: ProjectData[]): TelemetryMetrics {
  const total = projects.length;

  const statusMap: Record<string, number> = {};
  for (const p of projects) {
    const s = String(p.status || "UNKNOWN").toUpperCase();
    statusMap[s] = (statusMap[s] ?? 0) + 1;
  }
  const statusCounts: StatusCount[] = Object.entries(statusMap)
    .map(([status, count]) => ({ status, count }))
    .sort((a, b) => b.count - a.count);

  let planningReportCount = 0;
  let architectureGraphCount = 0;
  let artifactManifestCount = 0;
  let compilationTraceCount = 0;

  const durations: number[] = [];

  for (const p of projects) {
    const caps = toRunCapabilities(p);
    if (caps.hasPlanningReport) planningReportCount++;
    if (caps.hasArchitectureGraphs) architectureGraphCount++;
    if (caps.hasArtifactManifest) artifactManifestCount++;
    if (caps.hasCompilationTrace) compilationTraceCount++;

    const dur = p.planning_report?.planning_duration_ms;
    if (typeof dur === "number" && dur > 0) {
      durations.push(dur);
    }
  }

  const avgPlanningDurationMs =
    durations.length > 0
      ? Math.round(durations.reduce((s, d) => s + d, 0) / durations.length)
      : null;

  return {
    totalProjects: total,
    statusCounts,
    avgPlanningDurationMs,
    planningReportCount,
    architectureGraphCount,
    artifactManifestCount,
    compilationTraceCount,
  };
}

export function formatDurationMs(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  return `${(ms / 1000).toFixed(1)}s`;
}
