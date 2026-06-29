"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ChevronRight, FolderKanban, GitBranch, PlayCircle, Search, Settings, TerminalSquare, Users } from "lucide-react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { useShell } from "./ShellProvider";

const contextItems = [
  { label: "Projects", href: "/projects", icon: FolderKanban, enabled: true },
  { label: "Runs", href: "/runs", icon: PlayCircle, enabled: true },
  { label: "Compiler", href: "/compiler", icon: TerminalSquare, enabled: true },
  { label: "Telemetry", href: "/telemetry", icon: GitBranch, enabled: true },
  { label: "Search", href: "/search", icon: Search, enabled: true },
  { label: "Team", href: "/team", icon: Users, enabled: true },
  { label: "Settings", href: "/settings", icon: Settings, enabled: true },
];

function isActivePath(pathname: string, href: string) {
  return pathname === href || pathname.startsWith(`${href}/`);
}

export function ContextPanel() {
  const pathname = usePathname();
  const { contextPanelExpanded } = useShell();

  return (
    <aside
      className={cn(
        "min-h-0 overflow-hidden border-r border-border bg-surface-base transition-opacity duration-default",
        contextPanelExpanded ? "opacity-100" : "pointer-events-none opacity-0"
      )}
      aria-label="Context navigation"
      aria-hidden={!contextPanelExpanded}
    >
      <div className="flex h-full flex-col">
        <div className="border-b border-border px-4 py-4">
          <p className="text-xs font-semibold uppercase text-[color:var(--text-tertiary)]">Organization</p>
          <h2 className="mt-1 truncate text-sm font-semibold text-foreground">Default Organization</h2>
        </div>

        <nav className="flex-1 space-y-1 overflow-y-auto px-2 py-3">
          {contextItems.map((item) => {
            const Icon = item.icon;
            const active = item.enabled && isActivePath(pathname, item.href);
            const className = cn(
              "flex w-full items-center gap-2 rounded-sm px-2.5 py-2 text-sm font-medium transition-colors duration-default",
              active && "bg-accent-subtle text-accent",
              item.enabled && !active && "text-[color:var(--text-secondary)] hover:bg-surface-hover hover:text-foreground",
              !item.enabled && "cursor-not-allowed text-[color:var(--text-disabled)]"
            );

            const content = (
              <>
                <Icon className="h-4 w-4 shrink-0" aria-hidden="true" />
                <span className="min-w-0 flex-1 truncate">{item.label}</span>
                {item.enabled ? <ChevronRight className="h-3.5 w-3.5 shrink-0 opacity-50" aria-hidden="true" /> : <Badge variant="outline">Soon</Badge>}
              </>
            );

            return item.enabled ? (
              <Link key={item.label} href={item.href} className={className} aria-current={active ? "page" : undefined}>
                {content}
              </Link>
            ) : (
              <button key={item.label} type="button" className={className} disabled>
                {content}
              </button>
            );
          })}
        </nav>
      </div>
    </aside>
  );
}
