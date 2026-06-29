"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Box, FolderKanban, PlayCircle, ScrollText, Settings, TerminalSquare } from "lucide-react";
import { cn } from "@/lib/utils";

const navItems = [
  { label: "Projects", href: "/projects", icon: FolderKanban, enabled: true },
  { label: "Runs", href: "/runs", icon: PlayCircle, enabled: true },
  { label: "Compiler", href: "/compiler", icon: TerminalSquare, enabled: true },
  { label: "Telemetry", href: "/telemetry", icon: ScrollText, enabled: true },
];

function isActivePath(pathname: string, href: string) {
  return pathname === href || pathname.startsWith(`${href}/`);
}

export function GlobalRail() {
  const pathname = usePathname();

  return (
    <aside className="row-span-2 flex h-screen w-12 flex-col items-center border-r border-border bg-surface-base" aria-label="Global navigation">
      <Link href="/projects" className="flex h-[52px] w-full items-center justify-center border-b border-border text-accent" aria-label="Genesis Projects">
        <Box className="h-5 w-5" aria-hidden="true" />
      </Link>

      <nav className="flex flex-1 flex-col items-center gap-1 py-3">
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = item.enabled && isActivePath(pathname, item.href);
          const className = cn(
            "flex h-9 w-9 items-center justify-center rounded-sm border border-transparent text-[color:var(--text-tertiary)] transition-colors duration-default",
            active && "border-border-accent bg-accent-subtle text-accent",
            item.enabled && !active && "hover:bg-surface-hover hover:text-foreground",
            !item.enabled && "cursor-not-allowed opacity-40"
          );

          return item.enabled ? (
            <Link key={item.label} href={item.href} className={className} aria-label={item.label} aria-current={active ? "page" : undefined}>
              <Icon className="h-4 w-4" aria-hidden="true" />
            </Link>
          ) : (
            <button key={item.label} type="button" className={className} aria-label={`${item.label} future navigation`} disabled>
              <Icon className="h-4 w-4" aria-hidden="true" />
            </button>
          );
        })}
      </nav>

      <div className="border-t border-border py-3">
        <Link href="/settings" className={cn(
          "flex h-9 w-9 items-center justify-center rounded-sm border border-transparent text-[color:var(--text-tertiary)] transition-colors duration-default hover:bg-surface-hover hover:text-foreground",
          isActivePath(pathname, "/settings") && "border-border-accent bg-accent-subtle text-accent"
        )} aria-label="Settings" aria-current={isActivePath(pathname, "/settings") ? "page" : undefined}>
          <Settings className="h-4 w-4" aria-hidden="true" />
        </Link>
      </div>
    </aside>
  );
}
