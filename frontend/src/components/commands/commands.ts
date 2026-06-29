export type CommandAction =
  | { type: "navigate"; href: string }
  | { type: "shell"; action: "toggleContextPanel" | "toggleRightPanel" };

export interface Command {
  id: string;
  label: string;
  group: "Navigate" | "Shell";
  shortcut?: string;
  action: CommandAction;
}

export const COMMANDS: Command[] = [
  {
    id: "nav-dashboard",
    label: "Open Dashboard",
    group: "Navigate",
    shortcut: "G D",
    action: { type: "navigate", href: "/dashboard" },
  },
  {
    id: "nav-compiler",
    label: "Open Compiler",
    group: "Navigate",
    shortcut: "G C",
    action: { type: "navigate", href: "/compiler" },
  },
  {
    id: "nav-projects",
    label: "Open Projects",
    group: "Navigate",
    shortcut: "G P",
    action: { type: "navigate", href: "/projects" },
  },
  {
    id: "nav-runs",
    label: "Open Runs",
    group: "Navigate",
    shortcut: "G R",
    action: { type: "navigate", href: "/runs" },
  },
  {
    id: "nav-telemetry",
    label: "Open Telemetry",
    group: "Navigate",
    action: { type: "navigate", href: "/telemetry" },
  },
  {
    id: "nav-team",
    label: "Open Team",
    group: "Navigate",
    action: { type: "navigate", href: "/team" },
  },
  {
    id: "nav-settings",
    label: "Open Settings",
    group: "Navigate",
    action: { type: "navigate", href: "/settings" },
  },
  {
    id: "nav-search",
    label: "Open Search",
    group: "Navigate",
    action: { type: "navigate", href: "/search" },
  },
  {
    id: "shell-context",
    label: "Toggle Context Panel",
    group: "Shell",
    shortcut: "Ctrl \\",
    action: { type: "shell", action: "toggleContextPanel" },
  },
  {
    id: "shell-right",
    label: "Toggle Right Panel",
    group: "Shell",
    shortcut: "Ctrl P",
    action: { type: "shell", action: "toggleRightPanel" },
  },
];
