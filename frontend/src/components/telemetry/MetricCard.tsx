interface MetricCardProps {
  label: string;
  value: string | number;
  note?: string;
}

export function MetricCard({ label, value, note }: MetricCardProps) {
  return (
    <div className="rounded-md border border-border bg-surface-base px-4 py-4">
      <p className="text-xs font-medium uppercase tracking-wider text-[color:var(--text-tertiary)]">
        {label}
      </p>
      <p className="mt-2 font-mono text-2xl font-bold tabular-nums">{value}</p>
      {note && (
        <p className="mt-1 text-xs text-[color:var(--text-tertiary)]">{note}</p>
      )}
    </div>
  );
}
