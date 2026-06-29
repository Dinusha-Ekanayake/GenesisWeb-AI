"use client";

import Link from "next/link";
import { Loader2 } from "lucide-react";
import { useProject } from "@/app/dashboard/lib/hooks";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/status-badge";
import { toProjectViewModel } from "@/lib/genesis/adapters";
import { CapabilityBadge, LimitedState, RouteScaffold } from "@/components/routes/RouteScaffold";

export default function ProjectRoutePage({ params }: { params: { id: string } }) {
  const { data: project, isLoading, error } = useProject(params.id);

  if (isLoading) {
    return (
      <RouteScaffold title="Project" description="Loading project context." eyebrow="Project">
        <div className="flex min-h-64 items-center justify-center text-[color:var(--text-secondary)]">
          <Loader2 className="mr-2 h-4 w-4 animate-spin" aria-hidden="true" />
          Loading project...
        </div>
      </RouteScaffold>
    );
  }

  if (error || !project) {
    return (
      <RouteScaffold title="Project unavailable" description="This route depends on the existing backend project endpoint." eyebrow="Project">
        <LimitedState title="Project unavailable" description="The backend project record could not be loaded." />
      </RouteScaffold>
    );
  }

  const viewModel = toProjectViewModel(project);
  const run = viewModel.lastRun;

  return (
    <RouteScaffold
      eyebrow="Project"
      title={viewModel.name}
      description={viewModel.description || "Project route shell backed by an existing backend project record."}
      actions={run ? <StatusBadge status={run.status} /> : null}
    >
      {run ? (
        <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_320px]">
          <Card>
            <CardHeader>
              <CardTitle>Latest Known Run</CardTitle>
              <CardDescription>Current backend data exposes this project as one latest known Run.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex flex-wrap gap-2">
                <CapabilityBadge enabled={run.capabilities.hasPlanningReport} label="Planning report" />
                <CapabilityBadge enabled={run.capabilities.hasArchitectureGraphs} label="Architecture" />
                <CapabilityBadge enabled={run.capabilities.hasWorkspaceFiles} label="Workspace" />
                <CapabilityBadge enabled={run.capabilities.hasArtifactManifest} label="Artifacts" />
              </div>
              <Link href={`/projects/${viewModel.id}/runs/${run.id}`} className="inline-flex rounded-sm bg-accent px-3 py-2 text-sm font-medium text-accent-foreground hover:bg-accent-hover">
                Open latest Run
              </Link>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Backend Identity</CardTitle>
              <CardDescription>Use these IDs for backend calls until real Run endpoints exist.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-2 text-sm text-[color:var(--text-secondary)]">
              <p>Project ID: <code>{viewModel.backendProjectId}</code></p>
              <p>Workspace ID: <code>{run.backendWorkspaceId || "Unavailable"}</code></p>
            </CardContent>
          </Card>
        </div>
      ) : (
        <LimitedState title="No Run context available" description="The backend project record could not be mapped to a latest known Run." />
      )}
    </RouteScaffold>
  );
}
