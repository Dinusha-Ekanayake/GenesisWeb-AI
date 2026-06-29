"use client";

import { useState } from "react";
import Link from "next/link";
import { ChevronDown, ChevronRight, File, Folder, Loader2 } from "lucide-react";
import { useProjectFile, useProjectWorkspace } from "@/app/dashboard/lib/hooks";
import type { RunViewModel } from "@/lib/genesis/view-models";
import { LimitedState } from "@/components/routes/RouteScaffold";

// ── Types ─────────────────────────────────────────────────────────────────────

type WorkspaceItem = {
  name: string;
  path: string;
  is_dir: boolean;
  children?: WorkspaceItem[];
};

// ── FileTreeNode ──────────────────────────────────────────────────────────────

function FileTreeNode({
  item,
  selectedPath,
  onSelect,
  depth = 0,
}: {
  item: WorkspaceItem;
  selectedPath: string | null;
  onSelect: (path: string) => void;
  depth?: number;
}) {
  const [open, setOpen] = useState(false);
  const indent = depth * 12 + 8;

  if (item.is_dir) {
    return (
      <div>
        <button
          onClick={() => setOpen((prev) => !prev)}
          aria-expanded={open}
          style={{ paddingLeft: `${indent}px` }}
          className="flex w-full items-center gap-1.5 py-1.5 pr-3 text-left text-sm font-mono text-foreground hover:bg-surface-hover"
        >
          {open ? (
            <ChevronDown className="h-3.5 w-3.5 shrink-0 text-[color:var(--text-tertiary)]" aria-hidden="true" />
          ) : (
            <ChevronRight className="h-3.5 w-3.5 shrink-0 text-[color:var(--text-tertiary)]" aria-hidden="true" />
          )}
          <Folder className="h-3.5 w-3.5 shrink-0 text-accent" aria-hidden="true" />
          <span className="truncate">{item.name}</span>
        </button>
        {open && item.children && item.children.length > 0 && (
          <div>
            {item.children.map((child) => (
              <FileTreeNode
                key={child.path}
                item={child}
                selectedPath={selectedPath}
                onSelect={onSelect}
                depth={depth + 1}
              />
            ))}
          </div>
        )}
      </div>
    );
  }

  const isSelected = selectedPath === item.path;
  return (
    <button
      onClick={() => onSelect(item.path)}
      aria-pressed={isSelected}
      style={{ paddingLeft: `${indent + 14}px` }}
      className={`flex w-full items-center gap-1.5 py-1.5 pr-3 text-left text-sm font-mono ${
        isSelected
          ? "bg-accent/20 text-accent"
          : "text-[color:var(--text-secondary)] hover:bg-surface-hover hover:text-foreground"
      }`}
    >
      <File className="h-3.5 w-3.5 shrink-0 text-[color:var(--text-tertiary)]" aria-hidden="true" />
      <span className="truncate">{item.name}</span>
    </button>
  );
}

// ── FileViewer ────────────────────────────────────────────────────────────────

function FileViewer({
  backendProjectId,
  path,
}: {
  backendProjectId: string;
  path: string;
}) {
  const { data, isLoading, error } = useProjectFile(backendProjectId, path);

  if (isLoading) {
    return (
      <div className="flex h-full items-center justify-center text-[color:var(--text-secondary)]">
        <Loader2 className="mr-2 h-4 w-4 animate-spin" aria-hidden="true" />
        Loading file...
      </div>
    );
  }

  if (error || !data) {
    const isBinary = (error as any)?.status === 415;
    const isTooLarge = (error as any)?.status === 403;
    return (
      <div className="flex h-full items-center justify-center p-4 text-center text-sm text-[color:var(--text-secondary)]">
        {isBinary
          ? "Cannot preview binary file."
          : isTooLarge
          ? "File too large to preview."
          : "Failed to load file content."}
      </div>
    );
  }

  return (
    <pre
      className="h-full overflow-auto p-4 font-mono text-xs leading-relaxed text-[color:var(--text-secondary)]"
      aria-label={`File content: ${path}`}
    >
      {data.content}
    </pre>
  );
}

// ── Main export ───────────────────────────────────────────────────────────────

export function RunWorkspace({ run }: { run: RunViewModel }) {
  const [selectedPath, setSelectedPath] = useState<string | null>(null);
  const { data: tree, isLoading, error } = useProjectWorkspace(run.backendProjectId);

  if (isLoading) {
    return (
      <div className="flex min-h-64 items-center justify-center text-[color:var(--text-secondary)]">
        <Loader2 className="mr-2 h-4 w-4 animate-spin" aria-hidden="true" />
        Loading workspace...
      </div>
    );
  }

  const items = Array.isArray(tree) ? (tree as WorkspaceItem[]) : [];

  if (error || items.length === 0) {
    return (
      <LimitedState
        title="Workspace files unavailable"
        description="The workspace endpoint returned no file tree for this project. Compile a specification to generate workspace output."
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

  return (
    <div className="flex h-[600px] overflow-hidden rounded-lg border border-border bg-surface-base">
      {/* File tree sidebar */}
      <div
        className="w-60 shrink-0 overflow-y-auto border-r border-border bg-surface-raised py-2"
        aria-label="Workspace file tree"
      >
        <p className="mb-1 px-3 pb-1 text-xs font-semibold uppercase tracking-wider text-[color:var(--text-tertiary)] border-b border-border">
          <code className="font-mono">{run.backendProjectId}</code>
        </p>
        {items.map((item) => (
          <FileTreeNode
            key={item.path}
            item={item}
            selectedPath={selectedPath}
            onSelect={setSelectedPath}
          />
        ))}
      </div>

      {/* File content panel */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {selectedPath ? (
          <>
            <div className="flex items-center border-b border-border bg-surface-raised px-3 py-2">
              <code className="truncate text-xs text-[color:var(--text-secondary)]">
                {selectedPath}
              </code>
            </div>
            <div className="flex-1 overflow-hidden bg-surface-base">
              <FileViewer backendProjectId={run.backendProjectId} path={selectedPath} />
            </div>
          </>
        ) : (
          <div className="flex h-full items-center justify-center text-sm text-[color:var(--text-tertiary)]">
            Select a file to preview its content.
          </div>
        )}
      </div>
    </div>
  );
}
