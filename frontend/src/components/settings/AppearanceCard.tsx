"use client";

import { useTheme } from "next-themes";
import { cn } from "@/lib/utils";

const THEME_OPTIONS = [
  { value: "system", label: "System" },
  { value: "light", label: "Light" },
  { value: "dark", label: "Dark" },
] as const;

export function AppearanceCard() {
  const { theme, setTheme } = useTheme();

  return (
    <section aria-labelledby="appearance-heading">
      <div className="rounded-md border border-border bg-surface-base p-5 space-y-4">
        <h2 id="appearance-heading" className="text-sm font-semibold text-foreground">
          Appearance
        </h2>
        <div>
          <p className="mb-3 text-xs text-[color:var(--text-secondary)]">Color theme</p>
          <div className="flex gap-2">
            {THEME_OPTIONS.map((opt) => (
              <button
                key={opt.value}
                type="button"
                onClick={() => setTheme(opt.value)}
                aria-pressed={theme === opt.value}
                className={cn(
                  "rounded-sm border px-4 py-2 text-sm font-medium transition-colors duration-default",
                  theme === opt.value
                    ? "border-accent bg-accent text-accent-foreground"
                    : "border-border bg-surface-raised text-foreground hover:bg-surface-hover"
                )}
              >
                {opt.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
