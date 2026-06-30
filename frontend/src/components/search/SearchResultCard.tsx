import Link from "next/link";
import { FolderKanban } from "lucide-react";
import { StatusBadge } from "@/components/ui/status-badge";
import type { SearchResult } from "./search-index";

interface SearchResultCardProps {
  result: SearchResult;
}

export function SearchResultCard({ result }: SearchResultCardProps) {
  const runHref = `/projects/${result.projectId}/runs/${result.runId}`;

  return (
    <div className="rounded-md border border-border bg-surface-base p-4 space-y-3">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <Link
            href={runHref}
            className="text-sm font-medium text-foreground hover:text-accent"
          >
            {result.projectName}
          </Link>
          {result.specName && result.specName !== result.projectName && (
            <p className="mt-0.5 text-xs text-[color:var(--text-tertiary)]">{result.specName}</p>
          )}
        </div>
        <StatusBadge status={result.status} />
      </div>

      <p className="font-mono text-xs text-[color:var(--text-tertiary)]">
        ID: {result.projectId}
      </p>

      {result.specDescription && (
        <p className="text-xs leading-5 text-[color:var(--text-secondary)]">
          {result.specDescription}
        </p>
      )}

      <div className="flex flex-wrap gap-2">
        <Link
          href={runHref}
          aria-label={`View Run for ${result.projectName}`}
          className="inline-flex items-center gap-1.5 rounded-sm border border-border bg-surface-raised px-2.5 py-1 text-xs font-medium text-foreground hover:bg-surface-hover"
        >
          <FolderKanban className="h-3 w-3" aria-hidden="true" />
          View Run
        </Link>
        {result.surfaceLinks.map((s) => (
          <Link
            key={s.href}
            href={s.href}
            className="inline-flex items-center rounded-sm border border-border bg-surface-raised px-2.5 py-1 text-xs text-[color:var(--text-secondary)] hover:bg-surface-hover hover:text-foreground"
          >
            {s.label}
          </Link>
        ))}
      </div>
    </div>
  );
}
