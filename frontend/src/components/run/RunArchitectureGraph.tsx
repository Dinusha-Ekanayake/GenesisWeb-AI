"use client";

import { useState } from "react";
import Link from "next/link";
import { Network } from "lucide-react";
import type { RunViewModel } from "@/lib/genesis/view-models";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { LimitedState } from "@/components/routes/RouteScaffold";

// ── Helpers ───────────────────────────────────────────────────────────────────

function formatGraphName(key: string): string {
  return key.replace(/_/g, " ").replace(/\.json$/, "");
}

const KNOWN_COLLECTIONS = ["endpoints", "pages", "components", "features", "tables"] as const;

function deriveGraphStats(graphData: unknown): Record<string, number> | null {
  if (!graphData || typeof graphData !== "object" || Array.isArray(graphData)) return null;
  const data = graphData as Record<string, unknown>;
  const stats: Record<string, number> = {};
  for (const collection of KNOWN_COLLECTIONS) {
    if (Array.isArray(data[collection])) {
      stats[collection] = (data[collection] as unknown[]).length;
    }
  }
  return Object.keys(stats).length > 0 ? stats : null;
}

// ── Sub-components ────────────────────────────────────────────────────────────

function GraphPanel({ graphName, graphData }: { graphName: string; graphData: unknown }) {
  const stats = deriveGraphStats(graphData);

  return (
    <div className="space-y-4">
      {stats && (
        <div
          className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5"
          aria-label="Graph collection counts"
        >
          {Object.entries(stats).map(([collection, count]) => (
            <div
              key={collection}
              className="flex flex-col items-center justify-center rounded-md border border-border bg-surface-raised p-3 text-center"
            >
              <span className="font-mono text-xl font-bold tabular-nums text-foreground">
                {count}
              </span>
              <span className="mt-1 text-xs font-semibold uppercase tracking-wider text-[color:var(--text-tertiary)]">
                {collection}
              </span>
            </div>
          ))}
        </div>
      )}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm font-semibold capitalize">
            {formatGraphName(graphName)}
          </CardTitle>
          <CardDescription>Raw graph data from the compiler pipeline.</CardDescription>
        </CardHeader>
        <CardContent>
          <pre
            className="max-h-[480px] overflow-y-auto overflow-x-auto rounded-md border border-border bg-surface-base p-3 font-mono text-xs text-[color:var(--text-secondary)]"
            aria-label={`${graphName} graph data`}
          >
            {JSON.stringify(graphData, null, 2)}
          </pre>
        </CardContent>
      </Card>
    </div>
  );
}

// ── Main export ───────────────────────────────────────────────────────────────

export function RunArchitectureGraph({ run }: { run: RunViewModel }) {
  const graphEntries = Object.entries(run.architectureGraphs ?? {});

  // useState must precede early returns to satisfy Rules of Hooks
  const [activeGraph, setActiveGraph] = useState<string | null>(
    graphEntries[0]?.[0] ?? null
  );

  if (!run.capabilities.hasArchitectureGraphs || graphEntries.length === 0) {
    return (
      <LimitedState
        title="No architecture graphs available"
        description="The backend project record does not include architecture graph data. Compile a specification to generate graphs."
        action={
          <Link
            href="/compiler"
            className="inline-flex rounded-sm bg-accent px-3 py-2 text-sm font-medium text-accent-foreground hover:bg-accent-hover"
          >
            Open Compiler
          </Link>
        }
      />
    );
  }

  const resolvedActive = activeGraph ?? graphEntries[0][0];
  const activeGraphData = (run.architectureGraphs ?? {})[resolvedActive];

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-2">
        <Network className="h-4 w-4 shrink-0 text-[color:var(--text-tertiary)]" aria-hidden="true" />
        {graphEntries.map(([name]) => (
          <button
            key={name}
            onClick={() => setActiveGraph(name)}
            aria-pressed={resolvedActive === name}
            className={`whitespace-nowrap rounded-sm px-3 py-1.5 text-xs font-semibold transition-colors ${
              resolvedActive === name
                ? "bg-accent text-accent-foreground"
                : "border border-border bg-surface-raised text-foreground hover:bg-surface-hover"
            }`}
          >
            {formatGraphName(name)}
          </button>
        ))}
        <span className="ml-auto text-xs text-[color:var(--text-tertiary)]">
          {graphEntries.length} graph{graphEntries.length !== 1 ? "s" : ""} available
        </span>
      </div>

      <GraphPanel graphName={resolvedActive} graphData={activeGraphData} />
    </div>
  );
}
