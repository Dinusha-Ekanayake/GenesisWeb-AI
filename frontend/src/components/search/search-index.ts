import type { ProjectData } from "@/app/dashboard/types/genesis";
import { toRunViewModel } from "@/lib/genesis/adapters";
import type { RunCapabilities } from "@/lib/genesis/view-models";

export interface SurfaceLink {
  label: string;
  href: string;
}

export interface SearchResult {
  projectId: string;
  runId: string;
  projectName: string;
  status: string;
  specName?: string;
  specDescription?: string;
  surfaceLinks: SurfaceLink[];
}

function deriveSurfaceLinks(projectId: string, caps: RunCapabilities): SurfaceLink[] {
  const base = `/projects/${projectId}/runs/${projectId}`;
  const candidates: Array<{ label: string; href: string; available: boolean }> = [
    { label: "Planning Report", href: `${base}/report`, available: caps.hasPlanningReport },
    { label: "Architecture", href: `${base}/architecture`, available: caps.hasArchitectureGraphs },
    { label: "Workspace", href: `${base}/workspace`, available: caps.hasWorkspaceFiles },
    { label: "Artifacts", href: `${base}/artifacts`, available: caps.hasArtifactManifest },
    { label: "Compiler Trace", href: `${base}/compiler`, available: caps.hasCompilationTrace },
  ];
  return candidates.filter((c) => c.available).map(({ label, href }) => ({ label, href }));
}

export function buildSearchResults(projects: ProjectData[], query: string): SearchResult[] {
  const q = query.toLowerCase().trim();

  const all: SearchResult[] = projects.map((project) => {
    const run = toRunViewModel(project);
    return {
      projectId: project.id,
      runId: project.id,
      projectName: run.projectName,
      status: run.status,
      specName: project.spec?.name?.trim() || undefined,
      specDescription: project.spec?.description?.trim() || undefined,
      surfaceLinks: deriveSurfaceLinks(project.id, run.capabilities),
    };
  });

  if (!q) return all;

  return all.filter(
    (r) =>
      r.projectName.toLowerCase().includes(q) ||
      r.projectId.toLowerCase().includes(q) ||
      r.status.toLowerCase().includes(q) ||
      (r.specName?.toLowerCase().includes(q) ?? false) ||
      (r.specDescription?.toLowerCase().includes(q) ?? false)
  );
}
