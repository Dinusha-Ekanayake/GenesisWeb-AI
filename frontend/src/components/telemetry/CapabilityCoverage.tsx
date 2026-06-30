interface CoverageRowProps {
  label: string;
  count: number;
  total: number;
}

function CoverageRow({ label, count, total }: CoverageRowProps) {
  return (
    <div className="flex items-center justify-between border-b border-border px-4 py-3 last:border-b-0">
      <span className="text-sm text-foreground">{label}</span>
      <span className="font-mono text-sm tabular-nums text-[color:var(--text-secondary)]">
        {count} / {total}
      </span>
    </div>
  );
}

interface CapabilityCoverageProps {
  total: number;
  planningReportCount: number;
  architectureGraphCount: number;
  artifactManifestCount: number;
  compilationTraceCount: number;
}

export function CapabilityCoverage({
  total,
  planningReportCount,
  architectureGraphCount,
  artifactManifestCount,
  compilationTraceCount,
}: CapabilityCoverageProps) {
  return (
    <section aria-labelledby="capability-coverage-heading">
      <h2
        id="capability-coverage-heading"
        className="mb-3 text-sm font-semibold text-foreground"
      >
        Run Surface Availability
      </h2>
      <div className="rounded-md border border-border bg-surface-base">
        <CoverageRow label="Planning Report" count={planningReportCount} total={total} />
        <CoverageRow
          label="Architecture Graphs"
          count={architectureGraphCount}
          total={total}
        />
        <CoverageRow
          label="Artifact Manifest"
          count={artifactManifestCount}
          total={total}
        />
        <CoverageRow
          label="Compiler Trace"
          count={compilationTraceCount}
          total={total}
        />
      </div>
      <p className="mt-2 text-xs text-[color:var(--text-tertiary)]">
        Latest-known-run surfaces available across all projects.
      </p>
    </section>
  );
}
