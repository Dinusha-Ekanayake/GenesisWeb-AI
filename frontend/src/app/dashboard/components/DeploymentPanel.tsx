"use client";

import { useProjectManifest } from "../lib/hooks";
import { Download, Package, CheckCircle2, FileJson, FileArchive, Loader2 } from "lucide-react";

export default function DeploymentPanel({ projectId }: { projectId: string }) {
  const { data: manifest, isLoading } = useProjectManifest(projectId);

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";

  const handleDownload = (filename: string) => {
    const url = `${API_BASE}/genesis/projects/${projectId}/artifacts/${filename}`;
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center p-12 bg-slate-900 rounded-lg border border-slate-800">
        <Loader2 className="w-8 h-8 animate-spin text-slate-500 mb-4" />
        <p className="text-slate-400">Loading artifacts...</p>
      </div>
    );
  }

  if (!manifest) {
    return (
      <div className="flex flex-col items-center justify-center p-12 bg-slate-900 rounded-lg border border-slate-800">
        <Package className="w-12 h-12 mb-4 text-slate-600" />
        <h3 className="text-lg font-semibold text-slate-300 mb-2">No Deployment Artifacts</h3>
        <p className="text-sm text-slate-500 mb-6 text-center max-w-md">
          The compiler has not generated deployment artifacts yet.
        </p>
      </div>
    );
  }

  const artifacts = [
    { name: "deployment_bundle.zip", type: "zip", size: "Compiled Bundle", icon: FileArchive },
    { name: "deployment_manifest.json", type: "json", size: "Build Metadata", icon: FileJson },
    { name: "execution_trace.json", type: "json", size: "Telemetry Logs", icon: FileJson },
    { name: "planning_report.json", type: "json", size: "Plan Validation", icon: FileJson },
    { name: "api_graph.json", type: "json", size: "Graph Data", icon: FileJson },
    { name: "page_graph.json", type: "json", size: "Graph Data", icon: FileJson },
    { name: "component_graph.json", type: "json", size: "Graph Data", icon: FileJson },
    { name: "feature_graph.json", type: "json", size: "Graph Data", icon: FileJson },
  ];

  return (
    <div className="space-y-6">
      <div className="bg-emerald-950/30 border border-emerald-900/50 rounded-lg p-6 flex items-center justify-between shadow-inner">
        <div className="flex items-center gap-4">
          <div className="bg-emerald-900/50 p-3 rounded-full border border-emerald-800">
            <CheckCircle2 className="w-6 h-6 text-emerald-400" />
          </div>
          <div>
            <h3 className="font-semibold text-emerald-300 text-lg">Deployment Bundle Ready</h3>
            <p className="text-sm text-emerald-500">Status: {manifest.build_status}</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-slate-950 rounded-lg border border-slate-800 p-6 flex flex-col h-full">
          <h4 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-6">Artifact Download Manager</h4>
          <div className="space-y-3 flex-1">
            {artifacts.map((file) => (
              <div key={file.name} className="flex items-center justify-between p-3 bg-slate-900 rounded-lg border border-slate-800 hover:border-slate-700 transition-colors group">
                <div className="flex items-center gap-3">
                  <file.icon className={`w-5 h-5 ${file.type === "zip" ? "text-amber-400" : "text-blue-400"}`} />
                  <div>
                    <p className="text-sm font-medium text-slate-200">{file.name}</p>
                    <p className="text-xs text-slate-500">{file.size}</p>
                  </div>
                </div>
                <button
                  onClick={() => handleDownload(file.name)}
                  className="p-2 bg-slate-800 text-slate-300 rounded hover:bg-blue-600 hover:text-white transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
                  title={`Download ${file.name}`}
                >
                  <Download className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        </div>

        <div className="flex flex-col gap-6">
          <div className="bg-slate-950 rounded-lg border border-slate-800 p-6">
            <h4 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-4">Cryptographic Hashes</h4>
            <div className="space-y-4">
              <div>
                <p className="text-xs text-slate-500 mb-1">Workspace SHA-256</p>
                <code className="text-xs font-mono bg-slate-900 px-2 py-1.5 rounded block break-all text-slate-300 border border-slate-800">
                  {manifest.workspace_hash || "N/A"}
                </code>
              </div>
              <div>
                <p className="text-xs text-slate-500 mb-1">Deployment Bundle SHA-256</p>
                <code className="text-xs font-mono bg-slate-900 px-2 py-1.5 rounded block break-all text-slate-300 border border-slate-800">
                  {manifest.deployment_hash}
                </code>
              </div>
            </div>
          </div>

          <div className="bg-slate-950 rounded-lg border border-slate-800 p-6 flex-1">
            <h4 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-4">Plugin Versions</h4>
            <ul className="space-y-3">
              {Object.entries(manifest.plugin_versions || {}).map(([plugin, version]) => (
                <li key={plugin} className="flex justify-between items-center text-sm border-b border-slate-800 pb-2 last:border-0 last:pb-0">
                  <span className="text-slate-300">{plugin}</span>
                  <span className="font-mono text-xs bg-slate-900 px-2 py-1 rounded text-slate-400 border border-slate-800">v{String(version)}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
