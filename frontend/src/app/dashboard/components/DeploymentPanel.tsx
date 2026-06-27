"use client";

import { DeploymentManifest } from "../types/genesis";
import { Download, Package, CheckCircle2 } from "lucide-react";
import { Button } from "@/components/ui/button";

interface DeploymentPanelProps {
  manifest?: DeploymentManifest;
  onDeploy: () => Promise<void>;
  loading: boolean;
}

export default function DeploymentPanel({ manifest, onDeploy, loading }: DeploymentPanelProps) {
  if (!manifest) {
    return (
      <div className="flex flex-col items-center justify-center p-12 bg-slate-50 dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800">
        <Package className="w-12 h-12 mb-4 text-slate-300" />
        <h3 className="text-lg font-semibold text-slate-700 dark:text-slate-300 mb-2">Ready for Deployment</h3>
        <p className="text-sm text-slate-500 mb-6 text-center max-w-md">
          The compiler has successfully generated the workspace. You can now package and deploy it.
        </p>
        <Button onClick={onDeploy} disabled={loading} className="bg-blue-600 hover:bg-blue-700 text-white">
          {loading ? "Packaging Workspace..." : "Package & Deploy"}
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900 rounded-lg p-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="bg-emerald-100 dark:bg-emerald-900 p-3 rounded-full">
            <CheckCircle2 className="w-6 h-6 text-emerald-600 dark:text-emerald-400" />
          </div>
          <div>
            <h3 className="font-semibold text-emerald-900 dark:text-emerald-300 text-lg">Deployment Bundle Ready</h3>
            <p className="text-sm text-emerald-700 dark:text-emerald-400/80">Status: {manifest.build_status}</p>
          </div>
        </div>
        <Button variant="outline" className="border-emerald-200 hover:bg-emerald-100 text-emerald-700 dark:border-emerald-800 dark:hover:bg-emerald-900 dark:text-emerald-300" onClick={() => alert("Downloading bundle... (Backend streaming not yet implemented)")}>
          <Download className="w-4 h-4 mr-2" />
          Download ZIP
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-slate-950 rounded-lg border border-slate-200 dark:border-slate-800 p-6">
          <h4 className="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-4">Cryptographic Hashes</h4>
          <div className="space-y-4">
            <div>
              <p className="text-xs text-slate-500 mb-1">Workspace SHA-256</p>
              <code className="text-xs font-mono bg-slate-100 dark:bg-slate-900 px-2 py-1 rounded block break-all text-slate-700 dark:text-slate-300">
                {manifest.workspace_hash || "N/A"}
              </code>
            </div>
            <div>
              <p className="text-xs text-slate-500 mb-1">Deployment Bundle SHA-256</p>
              <code className="text-xs font-mono bg-slate-100 dark:bg-slate-900 px-2 py-1 rounded block break-all text-slate-700 dark:text-slate-300">
                {manifest.deployment_hash}
              </code>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-slate-950 rounded-lg border border-slate-200 dark:border-slate-800 p-6">
          <h4 className="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-4">Plugin Versions</h4>
          <ul className="space-y-2">
            {Object.entries(manifest.plugin_versions).map(([plugin, version]) => (
              <li key={plugin} className="flex justify-between items-center text-sm">
                <span className="text-slate-700 dark:text-slate-300">{plugin}</span>
                <span className="font-mono text-xs bg-slate-100 dark:bg-slate-900 px-2 py-1 rounded text-slate-500">v{version}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
