"use client";

import { useState } from "react";
import Link from "next/link";
import { CheckCircle2, ExternalLink, XCircle } from "lucide-react";
import SpecEditor from "@/app/dashboard/components/SpecEditor";
import ExecutionStatusPanel from "@/app/dashboard/components/ExecutionStatusPanel";
import { GenesisAPI } from "@/app/dashboard/lib/genesis-api";
import { useSSE } from "@/app/dashboard/lib/hooks";
import { toast } from "sonner";
import type { DeploymentManifest, ProjectSpecification } from "@/app/dashboard/types/genesis";

type CompilationResult = {
  status: string;
  manifest: DeploymentManifest;
};

export function CompilerWorkspace() {
  const [running, setRunning] = useState(false);
  const [activeProjectId, setActiveProjectId] = useState<string | null>(null);
  const [compilationResult, setCompilationResult] = useState<CompilationResult | null>(null);
  const [compilationError, setCompilationError] = useState<string | null>(null);

  // Connect to live SSE events once a backend project ID is known.
  // activeProjectId is set from spec.project_id before awaiting runCompiler,
  // matching the legacy dashboard pattern so events stream during compilation.
  useSSE(activeProjectId);

  const handleCompile = async (spec: ProjectSpecification) => {
    setRunning(true);
    setCompilationResult(null);
    setCompilationError(null);
    setActiveProjectId(spec.project_id);
    try {
      const result = await GenesisAPI.runCompiler(spec);
      setCompilationResult(result);
    } catch (e: any) {
      const message = e.message || "Compilation failed";
      setCompilationError(message);
      toast.error(`Compiler Error: ${message}`);
    } finally {
      setRunning(false);
    }
  };

  const handleValidate = async (spec: ProjectSpecification) => {
    try {
      await GenesisAPI.validateSpec(spec);
      toast.success("Specification is valid.");
    } catch (e: any) {
      toast.error(`Validation Error: ${e.message}`);
    }
  };

  // Derive safe navigation target from the backend manifest, not from any frontend-invented ID.
  // The latest-known-run model maps project.id === run.id, so both segments use backendProjectId.
  const backendProjectId = compilationResult?.manifest?.project_id ?? null;

  return (
    <div className="flex flex-col gap-6">
      <header className="flex flex-col gap-1 border-b border-border pb-5">
        <p className="text-xs font-semibold uppercase text-[color:var(--text-tertiary)]">Compiler</p>
        <h1 className="mt-1 text-2xl font-semibold tracking-normal text-foreground">
          Compiler Workspace
        </h1>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-[color:var(--text-secondary)]">
          Write a specification, validate its structure, and compile it through the Genesis Engine
          pipeline. Status updates reflect live backend events.
        </p>
      </header>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2 lg:h-[540px]">
        {/* Left column: Specification Editor */}
        <SpecEditor onRun={handleCompile} onValidate={handleValidate} loading={running} />

        {/* Right column: Pipeline Status + Result */}
        <div className="flex min-h-0 flex-col gap-3">
          <div className="min-h-0 flex-1">
            <ExecutionStatusPanel projectId={activeProjectId} />
          </div>

          {compilationResult && backendProjectId && (
            <div className="flex items-center justify-between gap-3 rounded-lg border border-border bg-surface-raised px-4 py-3">
              <div className="flex items-center gap-2 text-sm text-success">
                <CheckCircle2 className="h-4 w-4 shrink-0" aria-hidden="true" />
                <span>
                  Compilation complete —{" "}
                  <code className="font-mono text-xs text-[color:var(--text-secondary)]">
                    {backendProjectId}
                  </code>
                </span>
              </div>
              <Link
                href={`/projects/${backendProjectId}/runs/${backendProjectId}`}
                className="inline-flex shrink-0 items-center gap-1.5 rounded-sm border border-border bg-surface-base px-3 py-1.5 text-xs font-medium text-foreground hover:bg-surface-hover"
              >
                View latest known Run
                <ExternalLink className="h-3 w-3" aria-hidden="true" />
              </Link>
            </div>
          )}

          {compilationError && !running && (
            <div className="flex items-start gap-2 rounded-lg border border-[color:var(--error)] bg-surface-raised px-4 py-3 text-sm text-[color:var(--error)]">
              <XCircle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
              <span>{compilationError}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
