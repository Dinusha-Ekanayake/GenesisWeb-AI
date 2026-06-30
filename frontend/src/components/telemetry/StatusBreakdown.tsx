import { StatusBadge } from "@/components/ui/status-badge";
import type { StatusCount } from "./telemetry-metrics";

interface StatusBreakdownProps {
  statusCounts: StatusCount[];
  total: number;
}

export function StatusBreakdown({ statusCounts, total }: StatusBreakdownProps) {
  return (
    <section aria-labelledby="status-breakdown-heading">
      <h2
        id="status-breakdown-heading"
        className="mb-3 text-sm font-semibold text-foreground"
      >
        Status Breakdown
      </h2>
      <div className="rounded-md border border-border bg-surface-base">
        {statusCounts.length === 0 ? (
          <p className="px-4 py-4 text-sm text-[color:var(--text-tertiary)]">
            No project data.
          </p>
        ) : (
          statusCounts.map(({ status, count }) => (
            <div
              key={status}
              className="flex items-center justify-between border-b border-border px-4 py-3 last:border-b-0"
            >
              <StatusBadge status={status} />
              <span className="font-mono text-sm tabular-nums text-foreground">
                {count}
              </span>
            </div>
          ))
        )}
      </div>
      <p className="mt-2 text-xs text-[color:var(--text-tertiary)]">
        {total} project{total !== 1 ? "s" : ""} total
      </p>
    </section>
  );
}
