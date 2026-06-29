"use client";

import { useCallback, useRef, useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Search } from "lucide-react";
import { cn } from "@/lib/utils";
import { useShell } from "@/components/layout/ShellProvider";
import { COMMANDS, type Command } from "./commands";
import { useKeyboardShortcuts } from "./useKeyboardShortcuts";

export function CommandPalette() {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();
  const { toggleContextPanel, toggleRightPanel } = useShell();

  const openPalette = useCallback(() => {
    setIsOpen(true);
    setQuery("");
    setSelectedIndex(0);
  }, []);

  const closePalette = useCallback(() => {
    setIsOpen(false);
    setQuery("");
    setSelectedIndex(0);
  }, []);

  const executeCommand = useCallback(
    (cmd: Command) => {
      closePalette();
      if (cmd.action.type === "navigate") {
        router.push(cmd.action.href);
      } else {
        if (cmd.action.action === "toggleContextPanel") toggleContextPanel();
        else toggleRightPanel();
      }
    },
    [closePalette, router, toggleContextPanel, toggleRightPanel]
  );

  useKeyboardShortcuts({
    isOpen,
    onOpen: openPalette,
    onClose: closePalette,
    paletteInputRef: inputRef,
    toggleContextPanel,
    toggleRightPanel,
    onNavigate: (href) => router.push(href),
  });

  const filtered = COMMANDS.filter(
    (cmd) => query === "" || cmd.label.toLowerCase().includes(query.toLowerCase())
  );

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  // Reset selection when filter changes
  useEffect(() => {
    setSelectedIndex(0);
  }, [query]);

  // Arrow key navigation inside the palette
  useEffect(() => {
    if (!isOpen) return;
    function onPaletteKey(e: KeyboardEvent) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        setSelectedIndex((i) => Math.min(i + 1, filtered.length - 1));
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        setSelectedIndex((i) => Math.max(i - 1, 0));
      } else if (e.key === "Enter" && filtered[selectedIndex]) {
        e.preventDefault();
        executeCommand(filtered[selectedIndex]);
      }
    }
    document.addEventListener("keydown", onPaletteKey);
    return () => document.removeEventListener("keydown", onPaletteKey);
  }, [isOpen, filtered, selectedIndex, executeCommand]);

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label="Command palette"
      className="fixed inset-0 z-50 flex items-start justify-center pt-[20vh]"
      onClick={closePalette}
    >
      <div
        className="relative w-full max-w-lg rounded-md border border-border bg-surface-base shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Search input */}
        <div className="flex items-center border-b border-border px-3">
          <Search className="h-4 w-4 shrink-0 text-[color:var(--text-tertiary)]" aria-hidden="true" />
          <input
            ref={inputRef}
            type="text"
            placeholder="Type a command or search…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-transparent px-3 py-3.5 text-sm text-foreground placeholder:text-[color:var(--text-tertiary)] focus:outline-none"
            aria-label="Search commands"
            aria-autocomplete="list"
            aria-controls="command-palette-list"
          />
        </div>

        {/* Command list */}
        <ul
          id="command-palette-list"
          role="listbox"
          aria-label="Commands"
          className="max-h-72 overflow-y-auto py-1"
        >
          {filtered.length === 0 && (
            <li className="px-4 py-6 text-center text-sm text-[color:var(--text-tertiary)]">
              No commands found.
            </li>
          )}
          {filtered.map((cmd, i) => (
            <li
              key={cmd.id}
              role="option"
              aria-selected={i === selectedIndex}
              className={cn(
                "flex cursor-pointer items-center justify-between px-4 py-2 text-sm",
                i === selectedIndex
                  ? "bg-surface-hover text-foreground"
                  : "text-[color:var(--text-secondary)]"
              )}
              onClick={() => executeCommand(cmd)}
              onMouseEnter={() => setSelectedIndex(i)}
            >
              <span>{cmd.label}</span>
              {cmd.shortcut && (
                <kbd className="ml-4 shrink-0 rounded border border-border bg-surface-raised px-1.5 py-0.5 font-mono text-xs text-[color:var(--text-tertiary)]">
                  {cmd.shortcut}
                </kbd>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
