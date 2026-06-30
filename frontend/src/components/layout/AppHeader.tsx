"use client";

import { LogOut, PanelLeftClose, PanelLeftOpen, PanelRightClose, PanelRightOpen } from "lucide-react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Breadcrumbs } from "./Breadcrumbs";
import { useShell } from "./ShellProvider";
import { removeToken } from "@/app/dashboard/lib/api-client";

export function AppHeader() {
  const {
    contextPanelExpanded,
    rightPanelExpanded,
    toggleContextPanel,
    toggleRightPanel,
  } = useShell();
  const router = useRouter();

  const handleLogout = () => {
    removeToken();
    router.push("/login");
  };

  return (
    <header className="flex h-[52px] min-w-0 items-center justify-between border-b border-border bg-surface-base px-3">
      <div className="flex min-w-0 items-center gap-2">
        <Button
          type="button"
          variant="ghost"
          size="icon"
          onClick={toggleContextPanel}
          aria-label={contextPanelExpanded ? "Collapse context panel" : "Expand context panel"}
        >
          {contextPanelExpanded ? <PanelLeftClose className="h-4 w-4" aria-hidden="true" /> : <PanelLeftOpen className="h-4 w-4" aria-hidden="true" />}
        </Button>
        <Breadcrumbs />
      </div>

      <div className="flex shrink-0 items-center gap-2">
        <Button
          type="button"
          variant="ghost"
          size="icon"
          onClick={handleLogout}
          aria-label="Sign out"
        >
          <LogOut className="h-4 w-4" aria-hidden="true" />
        </Button>
        <Button
          type="button"
          variant="ghost"
          size="icon"
          onClick={toggleRightPanel}
          aria-label={rightPanelExpanded ? "Collapse right panel" : "Expand right panel"}
        >
          {rightPanelExpanded ? <PanelRightClose className="h-4 w-4" aria-hidden="true" /> : <PanelRightOpen className="h-4 w-4" aria-hidden="true" />}
        </Button>
      </div>
    </header>
  );
}
