"use client";

import { Activity, Info } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { useShell } from "./ShellProvider";

export function RightPanel() {
  const { rightPanelExpanded } = useShell();

  return (
    <aside
      className={cn(
        "min-h-0 overflow-hidden border-l border-border bg-surface-base transition-opacity duration-default",
        rightPanelExpanded ? "opacity-100" : "pointer-events-none opacity-0"
      )}
      aria-label="Inspector panel"
      aria-hidden={!rightPanelExpanded}
    >
      <div className="flex h-full flex-col">
        <div className="border-b border-border px-4 py-4">
          <div className="flex items-center justify-between gap-3">
            <h2 className="text-sm font-semibold text-foreground">Inspector</h2>
            <Badge variant="outline">Foundation</Badge>
          </div>
        </div>

        <div className="space-y-4 overflow-y-auto p-4">
          <div className="flex items-start gap-3 rounded-md border border-border bg-surface-raised p-3">
            <Info className="mt-0.5 h-4 w-4 shrink-0 text-[color:var(--text-tertiary)]" aria-hidden="true" />
            <p className="text-sm leading-6 text-[color:var(--text-secondary)]">
              Run details, traces, and artifact inspection will attach here during later milestones.
            </p>
          </div>

          <div className="flex items-center gap-2 text-sm text-[color:var(--text-secondary)]">
            <Activity className="h-4 w-4 text-success" aria-hidden="true" />
            <span>Shell layout active</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
