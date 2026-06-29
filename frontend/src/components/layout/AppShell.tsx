"use client";

import type { ReactNode } from "react";
import { AppHeader } from "./AppHeader";
import { ContextPanel } from "./ContextPanel";
import { GlobalRail } from "./GlobalRail";
import { RightPanel } from "./RightPanel";
import { ShellProvider, useShell } from "./ShellProvider";
import { CommandPalette } from "@/components/commands/CommandPalette";

function ShellGrid({ children }: { children: ReactNode }) {
  const { contextPanelExpanded, rightPanelExpanded } = useShell();

  return (
    <>
      <div
        className="grid h-screen overflow-hidden bg-background text-foreground"
        style={{
          gridTemplateColumns: `48px ${contextPanelExpanded ? "240px" : "0px"} minmax(0, 1fr) ${rightPanelExpanded ? "320px" : "0px"}`,
          gridTemplateRows: "52px minmax(0, 1fr)",
        }}
      >
        <GlobalRail />
        <div className="col-start-2 col-end-5 row-start-1 min-w-0">
          <AppHeader />
        </div>
        <div className="col-start-2 row-start-2 min-h-0">
          <ContextPanel />
        </div>
        <section className="col-start-3 row-start-2 min-h-0 min-w-0 overflow-y-auto bg-surface-app" aria-label="Main work surface">
          <div className="mx-auto w-full max-w-7xl p-6 md:p-8">
            {children}
          </div>
        </section>
        <div className="col-start-4 row-start-2 min-h-0">
          <RightPanel />
        </div>
      </div>
      <CommandPalette />
    </>
  );
}

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <ShellProvider>
      <ShellGrid>{children}</ShellGrid>
    </ShellProvider>
  );
}
