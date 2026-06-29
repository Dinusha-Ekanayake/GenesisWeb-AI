import { type RefObject, useEffect, useRef, useState } from "react";

interface UseKeyboardShortcutsOptions {
  isOpen: boolean;
  onOpen: () => void;
  onClose: () => void;
  paletteInputRef: RefObject<HTMLInputElement | null>;
  toggleContextPanel: () => void;
  toggleRightPanel: () => void;
  onNavigate: (href: string) => void;
}

function isNonPaletteInput(paletteInput: HTMLInputElement | null): boolean {
  const el = document.activeElement as HTMLElement | null;
  if (!el) return false;
  const tag = el.tagName;
  return (tag === "INPUT" || tag === "TEXTAREA" || el.isContentEditable) && el !== paletteInput;
}

const SEQUENCE_MAP: Record<string, string> = {
  d: "/dashboard",
  c: "/compiler",
  p: "/projects",
  r: "/runs",
};

export function useKeyboardShortcuts({
  isOpen,
  onOpen,
  onClose,
  paletteInputRef,
  toggleContextPanel,
  toggleRightPanel,
  onNavigate,
}: UseKeyboardShortcutsOptions): void {
  const [awaitingSequence, setAwaitingSequence] = useState(false);
  const sequenceTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      // Escape always closes the palette
      if (e.key === "Escape" && isOpen) {
        e.preventDefault();
        onClose();
        return;
      }

      const inInput = isNonPaletteInput(paletteInputRef.current);

      // Ctrl+K / Cmd+K — toggle palette (blocked if a non-palette input is focused)
      if ((e.ctrlKey || e.metaKey) && e.key === "k") {
        if (inInput) return;
        e.preventDefault();
        isOpen ? onClose() : onOpen();
        return;
      }

      if (inInput) return;

      // Ctrl+\ — toggle context panel
      if (e.ctrlKey && e.key === "\\") {
        e.preventDefault();
        toggleContextPanel();
        return;
      }

      // Ctrl+P — toggle right panel
      if (e.ctrlKey && e.key === "p") {
        e.preventDefault();
        toggleRightPanel();
        return;
      }

      // G — begin sequence (only when palette is closed)
      if (!isOpen && !e.ctrlKey && !e.metaKey && !e.altKey && e.key === "g") {
        e.preventDefault();
        if (sequenceTimer.current) clearTimeout(sequenceTimer.current);
        setAwaitingSequence(true);
        sequenceTimer.current = setTimeout(() => setAwaitingSequence(false), 1000);
        return;
      }

      // Second key of G-sequence
      if (awaitingSequence && !e.ctrlKey && !e.metaKey && !e.altKey) {
        if (sequenceTimer.current) clearTimeout(sequenceTimer.current);
        setAwaitingSequence(false);
        const href = SEQUENCE_MAP[e.key.toLowerCase()];
        if (href) {
          e.preventDefault();
          onNavigate(href);
        }
      }
    }

    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, [isOpen, awaitingSequence, onOpen, onClose, paletteInputRef, toggleContextPanel, toggleRightPanel, onNavigate]);

  useEffect(() => {
    return () => {
      if (sequenceTimer.current) clearTimeout(sequenceTimer.current);
    };
  }, []);
}
