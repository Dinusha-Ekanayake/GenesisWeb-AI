"use client";

import Link from "next/link";
import { Loader2 } from "lucide-react";
import { useProjects } from "@/app/dashboard/lib/hooks";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/status-badge";
import { toRunSummaryViewModel } from "@/lib/genesis/adapters";
import { LimitedState, RouteScaffold } from "@/components/routes/RouteScaffold";

export default function RunsPage() {
  const { data: projects = [], isLoading, error } = useProjects();
  const runs = projects.map(toRunSummaryViewModel);

  return (
    <RouteScaffold
      eyebrow="Organization"
      title="Runs"
      description="Current backend project records represented as latest known Runs. Explicit Run history is not available yet."
    >
      {isLoading ? (
        <div className="flex min-h-64 items-center justify-center text-[color:var(--text-secondary)]">
          <Loader2 className="mr-2 h-4 w-4 animate-spin" aria-hidden="true" />
          Loading Runs...
        </div>
      ) : error ? (
        <LimitedState title="Runs unavailable" description="The existing backend projects endpoint did not return data." />
      ) : runs.length === 0 ? (
        <LimitedState title="No Runs yet" description="No backend project records are available to map into latest known Runs." />
      ) : (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {runs.map((run) => (
            <Link key={run.id} href={`/projects/${run.backendProjectId}/runs/${run.id}`} className="block">
              <Card className="h-full transition-colors hover:border-border-accent hover:bg-surface-hover">
                <CardHeader>
                  <CardTitle>{run.projectName}</CardTitle>
                  <CardDescription>{run.source}</CardDescription>
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
