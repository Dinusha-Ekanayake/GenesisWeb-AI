const SHORTCUTS = [
  { keys: "Ctrl / Cmd + K", description: "Open command palette" },
  { keys: "Escape", description: "Close command palette" },
  { keys: "G D", description: "Open Dashboard" },
  { keys: "G C", description: "Open Compiler" },
  { keys: "G P", description: "Open Projects" },
  { keys: "G R", description: "Open Runs" },
  { keys: "Ctrl + \\", description: "Toggle context panel" },
  { keys: "Ctrl + P", description: "Toggle right panel" },
];

export function ShortcutReferenceCard() {
  return (
    <section aria-labelledby="shortcuts-heading">
      <div className="rounded-md border border-border bg-surface-base p-5 space-y-4">
        <h2 id="shortcuts-heading" className="text-sm font-semibold text-foreground">
          Keyboard Shortcuts
        </h2>
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border">
              <th className="pb-2 pr-8 text-left text-xs font-medium text-[color:var(--text-tertiary)]">
                Shortcut
              </th>
              <th className="pb-2 text-left text-xs font-medium text-[color:var(--text-tertiary)]">
                Action
              </th>
            </tr>
          </thead>
          <tbody>
            {SHORTCUTS.map((s) => (
              <tr key={s.keys} className="border-b border-border last:border-0">
                <td className="py-2 pr-8">
                  <kbd className="font-mono text-xs text-foreground">{s.keys}</kbd>
                </td>
                <td className="py-2 text-sm text-[color:var(--text-secondary)]">
                  {s.description}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
