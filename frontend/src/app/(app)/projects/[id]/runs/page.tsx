"use client";

import Link from "next/link";
import { Loader2 } from "lucide-react";
import { useProject } from "@/app/dashboard/lib/hooks";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/status-badge";
import { toProjectViewModel } from "@/lib/genesis/adapters";
import { LimitedState, RouteScaffold } from "@/components/routes/RouteScaffold";

export default function ProjectRunsPage({ params }: { params: { id: string } }) {
  const { data: project, isLoading, error } = useProject(params.id);

  return (
    <RouteScaffold
      eyebrow="Project"
      title="Runs"
      description="Run history is not available from the backend yet. This page exposes the latest known Run only."
    >
      {isLoading ? (
        <div className="flex min-h-64 items-center justify-center text-[color:var(--text-secondary)]">
          <Loader2 className="mr-2 h-4 w-4 animate-spin" aria-hidden="true" />
          Loading Runs...
        </div>
      ) : error || !project ? (
        <LimitedState title="Runs unavailable" description="The existing backend project endpoint did not return data." />
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {toProjectViewModel(project).runs.map((run) => (
            <Link key={run.id} href={`/projects/${params.id}/runs/${run.id}`} className="block">
              <Card className="transition-colors hover:border-border-accent hover:bg-surface-hover">
                <CardHeader>
                  <CardTitle>{run.projectName}</CardTitle>
                  <CardDescription>Source: {run.source}</CardDescription>
                </CardHeader>
                <CardContent className="flex items-center justify-between gap-3">
                  <span className="text-sm text-[color:var(--text-secondary)]">{run.createdAt || "Created date unavailable"}</span>
                  <StatusBadge status={run.status} />
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </RouteScaffold>
  );
}
