"use client";

import Link from "next/link";
import { Loader2 } from "lucide-react";
import { useProjects } from "@/app/dashboard/lib/hooks";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/status-badge";
import { toProjectViewModel } from "@/lib/genesis/adapters";
import { LimitedState, RouteScaffold } from "@/components/routes/RouteScaffold";

export default function ProjectsPage() {
  const { data: projects = [], isLoading, error } = useProjects();
  const viewModels = projects.map(toProjectViewModel);

  return (
    <RouteScaffold
      eyebrow="Organization"
      title="Projects"
      description="Backend projects mapped into the target Project model. Each project currently exposes its latest known Run only."
    >
      {isLoading ? (
        <div className="flex min-h-64 items-center justify-center text-[color:var(--text-secondary)]">
          <Loader2 className="mr-2 h-4 w-4 animate-spin" aria-hidden="true" />
          Loading projects...
        </div>
      ) : error ? (
        <LimitedState title="Projects unavailable" description="The existing backend projects endpoint did not return data." />
      ) : viewModels.length === 0 ? (
        <LimitedState title="No projects yet" description="No backend project records are available to map into Genesis Projects." />
      ) : (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {viewModels.map((project) => (
            <Link key={project.id} href={`/projects/${project.id}`} className="block">
              <Card className="h-full transition-colors hover:border-border-accent hover:bg-surface-hover">
                <CardHeader>
                  <CardTitle>{project.name}</CardTitle>
                  <CardDescription>{project.description || `Backend project ${project.backendProjectId}`}</CardDescription>
                </CardHeader>
                <CardContent className="flex items-center justify-between gap-3">
                  <span className="text-sm text-[color:var(--text-secondary)]">{project.runs.length} latest known Run</span>
                  {project.lastRun ? <StatusBadge status={project.lastRun.status} /> : null}
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </RouteScaffold>
  );
}
