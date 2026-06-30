"use client";

import { useState } from "react";
import { Search } from "lucide-react";
import { RouteScaffold, LimitedState } from "@/components/routes/RouteScaffold";
import { useProjects } from "@/app/dashboard/lib/hooks";
import { buildSearchResults } from "./search-index";
import { SearchResultCard } from "./SearchResultCard";

function LoadingState() {
  return (
    <div className="flex items-center gap-2 py-8 text-sm text-[color:var(--text-secondary)]">
      <span>Loading projects…</span>
    </div>
  );
}

function ErrorState() {
  return (
    <div className="rounded-md border border-[color:var(--error)] bg-surface-base px-4 py-3 text-sm text-[color:var(--error)]">
      Cannot reach the backend. Project data is unavailable.
    </div>
  );
}

function EmptyQueryState() {
  return (
    <div className="rounded-md border border-border bg-surface-base px-5 py-6 space-y-2">
      <p className="text-sm font-medium text-foreground">What you can search</p>
      <ul className="space-y-1 text-sm text-[color:var(--text-secondary)]">
        <li>• Project names and IDs</li>
        <li>• Statuses (SUCCESS, FAILED, RUNNING…)</li>
        <li>• Specification names and descriptions</li>
      </ul>
    </div>
  );
}

export function GlobalSearchPage() {
  const [query, setQuery] = useState("");
  const { data: projects = [], isLoading, error } = useProjects();

  const results = buildSearchResults(projects, query);
  const hasQuery = query.trim().length > 0;

  return (
    <RouteScaffold
      eyebrow="Search"
      title="Search"
      description="Search projects and latest-known-run metadata."
    >
      <div className="space-y-4">
        {/* Search input */}
        <div className="relative">
          <Search
            className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[color:var(--text-tertiary)]"
            aria-hidden="true"
          />
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search projects, latest known runs, statuses…"
            className="w-full rounded-md border border-border bg-surface-base py-2.5 pl-9 pr-4 text-sm text-foreground placeholder:text-[color:var(--text-tertiary)] focus:outline-none focus:ring-1 focus:ring-accent"
            aria-label="Search"
          />
        </div>

        {/* Scope disclaimer — always visible */}
        <p className="text-xs text-[color:var(--text-tertiary)]">
          Search currently covers projects and latest-known-run metadata only. File contents, compilation traces, and full Run history are not indexed.
        </p>

        {/* Content states */}
        {isLoading ? (
          <LoadingState />
        ) : error ? (
          <ErrorState />
        ) : !hasQuery ? (
          <EmptyQueryState />
        ) : results.length === 0 ? (
          <LimitedState
            title="No results"
            description={`No projects or runs match "${query}". Try a different project name, ID, or status.`}
          />
        ) : (
          <ul className="space-y-2" aria-label="Search results">
            {results.map((r) => (
              <li key={r.projectId}>
                <SearchResultCard result={r} />
              </li>
            ))}
          </ul>
        )}
      </div>
    </RouteScaffold>
  );
}
