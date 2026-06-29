import Link from "next/link";
import { FolderKanban, Terminal } from "lucide-react";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-surface-app px-6 py-12">
      <div className="w-full max-w-lg space-y-8 text-center">
        <div className="space-y-3">
          <p className="text-xs font-semibold uppercase tracking-widest text-[color:var(--text-tertiary)]">
            Genesis Engine
          </p>
          <h1 className="text-4xl font-semibold tracking-tight text-foreground">
            Specification Compiler
          </h1>
          <p className="text-base text-[color:var(--text-secondary)]">
            Compile structured specifications into full-stack deployable applications.
          </p>
        </div>

        <div className="flex flex-col items-center gap-3 sm:flex-row sm:justify-center">
          <Link
            href="/compiler"
            className="inline-flex items-center gap-2 rounded-sm bg-accent px-5 py-2.5 text-sm font-medium text-accent-foreground hover:bg-accent-hover"
          >
            <Terminal className="h-4 w-4" aria-hidden="true" />
            Open Compiler
          </Link>
          <Link
            href="/projects"
            className="inline-flex items-center gap-2 rounded-sm border border-border bg-surface-base px-5 py-2.5 text-sm font-medium text-foreground hover:bg-surface-hover"
          >
            <FolderKanban className="h-4 w-4" aria-hidden="true" />
            View Projects
          </Link>
        </div>
      </div>
    </main>
  );
}
