"use client";

import { cn } from "@/lib/utils";
import { useShell } from "@/components/layout/ShellProvider";

function ToggleRow({
  label,
  active,
  onToggle,
  ariaLabel,
}: {
  label: string;
  active: boolean;
  onToggle: () => void;
  ariaLabel: string;
}) {
  return (
    <div className="flex items-center justify-between py-3 border-b border-border last:border-0">
      <div>
        <p className="text-sm text-foreground">{label}</p>
        <p className="text-xs text-[color:var(--text-tertiary)]">
          {active ? "Expanded" : "Collapsed"}
        </p>
      </div>
      <button
        type="button"
        onClick={onToggle}
        aria-pressed={active}
        aria-label={ariaLabel}
        className={cn(
          "rounded-sm border px-3 py-1.5 text-xs font-medium transition-colors duration-default",
          active
            ? "border-accent bg-accent-subtle text-accent hover:bg-accent-subtle"
            : "border-border bg-surface-raised text-foreground hover:bg-surface-hover"
        )}
      >
        {active ? "Collapse" : "Expand"}
      </button>
    </div>
  );
}

export function ShellPreferencesCard() {
  const {
    contextPanelExpanded,
    rightPanelExpanded,
    toggleContextPanel,
    toggleRightPanel,
    setContextPanelExpanded,
    setRightPanelExpanded,
  } = useShell();

  function resetDefaults() {
    setContextPanelExpanded(true);
    setRightPanelExpanded(false);
  }

  return (
    <section aria-labelledby="shell-prefs-heading">
      <div className="rounded-md border border-border bg-surface-base p-5 space-y-4">
        <div className="flex items-center justify-between">
          <h2 id="shell-prefs-heading" className="text-sm font-semibold text-foreground">
            Shell Preferences
          </h2>
          <button
            type="button"
            onClick={resetDefaults}
            aria-label="Reset shell preferences to defaults"
            className="text-xs text-[color:var(--text-tertiary)] hover:text-foreground transition-colors duration-default"
          >
            Reset to defaults
          </button>
        </div>
        <div className="divide-y divide-border">
          <ToggleRow
            label="Context Panel"
            active={contextPanelExpanded}
            onToggle={toggleContextPanel}
            ariaLabel="Toggle Context Panel"
          />
          <ToggleRow
            label="Right Panel"
            active={rightPanelExpanded}
            onToggle={toggleRightPanel}
            ariaLabel="Toggle Right Panel"
          />
        </div>
      </div>
    </section>
  );
}
