import type { ReactNode } from "react";
import { EmptyState } from "@/components/ui/empty-state";
import { Badge } from "@/components/ui/badge";

type RouteScaffoldProps = {
  eyebrow?: string;
  title: string;
  description?: string;
  children?: ReactNode;
  actions?: ReactNode;
};

type LimitedStateProps = {
  title: string;
  description: string;
  action?: ReactNode;
};

export function RouteScaffold({ eyebrow, title, description, children, actions }: RouteScaffoldProps) {
  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-4 border-b border-border pb-5 md:flex-row md:items-end md:justify-between">
        <div className="min-w-0">
          {eyebrow ? <p className="text-xs font-semibold uppercase text-[color:var(--text-tertiary)]">{eyebrow}</p> : null}
          <h1 className="mt-1 text-2xl font-semibold tracking-normal text-foreground">{title}</h1>
          {description ? <p className="mt-2 max-w-3xl text-sm leading-6 text-[color:var(--text-secondary)]">{description}</p> : null}
        </div>
        {actions ? <div className="flex shrink-0 items-center gap-2">{actions}</div> : null}
      </header>
      {children}
    </div>
  );
}

export function LimitedState({ title, description, action }: LimitedStateProps) {
  return (
    <EmptyState
      title={title}
      description={description}
      action={action}
      className="min-h-64 bg-surface-base"
    />
  );
}

export function CapabilityBadge({ enabled, label }: { enabled: boolean; label: string }) {
  return (
    <Badge variant={enabled ? "success" : "outline"}>
      {label}
    </Badge>
  );
}
