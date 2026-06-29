"use client";

import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from "react";

type ShellState = {
  contextPanelExpanded: boolean;
  rightPanelExpanded: boolean;
  toggleContextPanel: () => void;
  toggleRightPanel: () => void;
  setContextPanelExpanded: (expanded: boolean) => void;
  setRightPanelExpanded: (expanded: boolean) => void;
};

const ShellContext = createContext<ShellState | null>(null);

const CONTEXT_PANEL_KEY = "genesis:shell:context-panel-expanded";
const RIGHT_PANEL_KEY = "genesis:shell:right-panel-expanded";

function readStoredBoolean(key: string, fallback: boolean) {
  if (typeof window === "undefined") return fallback;
  const value = window.localStorage.getItem(key);
  if (value === "true") return true;
  if (value === "false") return false;
  return fallback;
}

export function ShellProvider({ children }: { children: ReactNode }) {
  const [mounted, setMounted] = useState(false);
  const [contextPanelExpanded, setContextPanelExpanded] = useState(true);
  const [rightPanelExpanded, setRightPanelExpanded] = useState(false);

  useEffect(() => {
    setContextPanelExpanded(readStoredBoolean(CONTEXT_PANEL_KEY, true));
    setRightPanelExpanded(readStoredBoolean(RIGHT_PANEL_KEY, false));
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!mounted) return;
    window.localStorage.setItem(CONTEXT_PANEL_KEY, String(contextPanelExpanded));
  }, [contextPanelExpanded, mounted]);

  useEffect(() => {
    if (!mounted) return;
    window.localStorage.setItem(RIGHT_PANEL_KEY, String(rightPanelExpanded));
  }, [rightPanelExpanded, mounted]);

  const value = useMemo<ShellState>(() => ({
    contextPanelExpanded,
    rightPanelExpanded,
    toggleContextPanel: () => setContextPanelExpanded((expanded) => !expanded),
    toggleRightPanel: () => setRightPanelExpanded((expanded) => !expanded),
    setContextPanelExpanded,
    setRightPanelExpanded,
  }), [contextPanelExpanded, rightPanelExpanded]);

  return (
    <ShellContext.Provider value={value}>
      {children}
    </ShellContext.Provider>
  );
}

export function useShell() {
  const context = useContext(ShellContext);
  if (!context) {
    throw new Error("useShell must be used within ShellProvider");
  }
  return context;
}
