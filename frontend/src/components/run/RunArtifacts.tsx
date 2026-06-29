"use client";

import Link from "next/link";
import { CheckCircle2, Download, FileJson } from "lucide-react";
import type { DeploymentManifest } from "@/app/dashboard/types/genesis";
import type { ArtifactFileViewModel, RunViewModel } from "@/lib/genesis/view-models";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { LimitedState } from "@/components/routes/RouteScaffold";

// ── Helpers ───────────────────────────────────────────────────────────────────

function buildArtifactUrl(file: ArtifactFileViewModel): string {
  const base = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000/api/v1";
  return `${base}/genesis/projects/${file.backendProjectId}/artifacts/${encodeURIComponent(file.name)}`;
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

// ── Sub-sections ──────────────────────────────────────────────────────────────

function StatusBanner({ buildStatus }: { buildStatus: string }) {
  return (
    <div className="flex items-center gap-3 rounded-lg border border-border bg-surface-raised px-4 py-3">
      <CheckCircle2 className="h-5 w-5 shrink-0 text-success" aria-hidden="true" />
      <div>
        <p className="font-semibold text-foreground">Deployment Bundle Ready</p>
        <p className="text-sm text-[color:var(--text-secondary)]">
          Status:{" "}
          <code className="font-mono">{buildStatus}</code>
        </p>
      </div>
    </div>
  );
}

function HashesCard({
  workspaceHash,
  deploymentHash,
}: {
  workspaceHash?: string;
  deploymentHash?: string;
}) {
  if (!workspaceHash && !deploymentHash) return null;
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Cryptographic Hashes</CardTitle>
        <CardDescription>Integrity hashes for the compiled artifact bundle.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {workspaceHash && (
          <div>
            <p className="mb-1 text-xs font-semibold uppercase tracking-wider text-[color:var(--text-tertiary)]">
              Workspace SHA-256
            </p>
            <code className="block break-all rounded-md border border-border bg-surface-raised px-2 py-1.5 font-mono text-xs text-[color:var(--text-secondary)]">
              {workspaceHash}
            </code>
          </div>
        )}
        {deploymentHash && (
          <div>
            <p className="mb-1 text-xs font-semibold uppercase tracking-wider text-[color:var(--text-tertiary)]">
              Deployment Bundle SHA-256
            </p>
            <code className="block break-all rounded-md border border-border bg-surface-raised px-2 py-1.5 font-mono text-xs text-[color:var(--text-secondary)]">
              {deploymentHash}
            </code>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

function ManifestCard({ manifest }: { manifest: DeploymentManifest }) {
  const graphEntries = Object.entries(manifest.graph_hashes ?? {});
  const pluginEntries = Object.entries(manifest.plugin_versions ?? {});

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Manifest Metadata</CardTitle>
          <CardDescription>Build information from the deployment manifest.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3 text-sm">
          <div className="flex items-center justify-between gap-4">
            <span className="text-[color:var(--text-tertiary)]">Project ID</span>
            <code className="font-mono text-xs text-foreground">{manifest.project_id}</code>
          </div>
          <div className="flex items-center justify-between gap-4">
            <span className="text-[color:var(--text-tertiary)]">Rule Engine Score</span>
            <code className="font-mono text-xs text-foreground">{manifest.rule_engine_score}</code>
          </div>
          <div className="flex items-center justify-between gap-4">
            <span className="text-[color:var(--text-tertiary)]">Build Status</span>
            <code className="font-mono text-xs text-foreground">{manifest.build_status}</code>
          </div>
        </CardContent>
      </Card>

      {pluginEntries.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Plugin Versions</CardTitle>
            <CardDescription>{pluginEntries.length} plugin{pluginEntries.length !== 1 ? "s" : ""} recorded.</CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {pluginEntries.map(([plugin, version]) => (
                <li
                  key={plugin}
                  className="flex items-center justify-between border-b border-border pb-2 text-sm last:border-0 last:pb-0"
                >
                  <span className="text-foreground">{plugin}</span>
                  <code className="rounded border border-border bg-surface-raised px-1.5 py-0.5 font-mono text-xs text-[color:var(--text-secondary)]">
                    v{String(version)}
                  </code>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {graphEntries.length > 0 && (
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="text-base">Graph Hashes</CardTitle>
            <CardDescription>Integrity hashes for the compiled graph outputs.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {graphEntries.map(([key, hash]) => (
              <div key={key} className="flex flex-col gap-0.5">
                <span className="text-xs font-semibold uppercase tracking-wider text-[color:var(--text-tertiary)]">
                  {key}
                </span>
                <code className="break-all font-mono text-xs text-[color:var(--text-secondary)]">
                  {hash}
                </code>
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
}

function ArtifactFilesCard({ files }: { files: ArtifactFileViewModel[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Artifact Files</CardTitle>
        <CardDescription>
          {files.length === 0
            ? "No artifact files are listed in the backend project record."
            : `${files.length} file${files.length !== 1 ? "s" : ""} in the artifact bundle.`}
        </CardDescription>
      </CardHeader>
      {files.length > 0 && (
        <CardContent className="space-y-2">
          {files.map((file) => (
            <div
              key={file.path}
              className="flex items-center justify-between gap-3 rounded-md border border-border bg-surface-raised px-3 py-2"
            >
              <div className="flex min-w-0 items-center gap-2">
                <FileJson
                  className="h-4 w-4 shrink-0 text-[color:var(--text-tertiary)]"
                  aria-hidden="true"
                />
                <div className="min-w-0">
                  <p className="truncate font-mono text-sm text-foreground">{file.name}</p>
                  <p className="truncate text-xs text-[color:var(--text-tertiary)]">{file.path}</p>
                  {file.sizeBytes !== undefined && (
                    <p className="text-xs text-[color:var(--text-tertiary)]">
                      {formatBytes(file.sizeBytes)}
                    </p>
                  )}
                </div>
              </div>
              <a
                href={buildArtifactUrl(file)}
                download={file.name}
                aria-label={`Download ${file.name}`}
                className="shrink-0 rounded border border-border bg-surface-base p-1.5 text-[color:var(--text-secondary)] hover:bg-accent hover:text-accent-foreground"
              >
                <Download className="h-3.5 w-3.5" aria-hidden="true" />
              </a>
            </div>
          ))}
        </CardContent>
      )}
    </Card>
  );
}

// ── Main export ───────────────────────────────────────────────────────────────

export function RunArtifacts({ run }: { run: RunViewModel }) {
  if (!run.artifactBundle) {
    return (
      <LimitedState
        title="No artifact bundle available"
        description="The backend project record does not include a deployment manifest or artifact files. Compile a specification to generate artifacts."
        action={
          <Link
            href="/compiler"
            className="inline-flex rounded-sm bg-accent px-3 py-2 text-sm font-medium text-accent-foreground hover:bg-accent-hover"
          >
            Open Compiler
          </Link>
        }
      />
    );
  }

  const { manifest, files, workspaceHash, deploymentHash } = run.artifactBundle;

  return (
    <div className="space-y-4">
      {manifest?.build_status && <StatusBanner buildStatus={manifest.build_status} />}
      <HashesCard workspaceHash={workspaceHash} deploymentHash={deploymentHash} />
      {manifest && <ManifestCard manifest={manifest} />}
      <ArtifactFilesCard files={files} />
    </div>
  );
}
