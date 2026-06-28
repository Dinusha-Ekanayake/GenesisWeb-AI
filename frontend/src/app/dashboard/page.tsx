"use client";

import { useEffect, useState } from "react";
import { GenesisAPI } from "./lib/genesis-api";
import { ProjectData, ProjectSpecification } from "./types/genesis";
import { ArrowRight, Loader2, FolderKanban, PlayCircle, AlertTriangle, CheckCircle, Package } from "lucide-react";
import SpecEditor from "./components/SpecEditor";
import ExecutionStatusPanel from "./components/ExecutionStatusPanel";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useProjects, useSSE } from "./lib/hooks";
import { toast } from "sonner";

export default function DashboardHome() {
  const router = useRouter();
  const { data: projects = [], isLoading: loading, error, refetch } = useProjects();
  const [running, setRunning] = useState(false);
  const [activeProjectId, setActiveProjectId] = useState<string | null>(null);

  // Subscribe to global SSE for automatic invalidation
  useSSE("*");

  useEffect(() => {
    if (error && (error as any).status === 401) {
      router.push("/login");
    }
  }, [error, router]);

  const backendError = error && (error as any).status !== 401 ? (error as any).message || "Cannot connect to backend" : null;

  const handleRunCompiler = async (spec: ProjectSpecification) => {
    setRunning(true);
    setActiveProjectId(spec.project_id);
    try {
      await GenesisAPI.runCompiler(spec);
      await refetch();
    } catch (e: any) {
      toast.error(`Compiler Error: ${e.message}`);
    } finally {
      setRunning(false);
    }
  };

  const handleValidateSpec = async (spec: ProjectSpecification) => {
    try {
      await GenesisAPI.validateSpec(spec);
      toast.success("Spec is valid!");
    } catch (e: any) {
      toast.error(`Validation Error: ${e.message}`);
    }
  };

  // Compute stats
  const activeBuilds = projects.filter(p => p.status === "RUNNING").length;
  const failedBuilds = projects.filter(p => p.status === "FAILED").length;
  const deployed = projects.filter(p => p.deployment_manifest?.build_status === "COMPLETED").length;

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white">Dashboard</h1>
        <p className="text-slate-400 mt-1">Manage and monitor Genesis Engine compiler runs.</p>
      </div>

      {/* Backend offline banner */}
      {backendError && (
        <div className="flex items-center gap-3 bg-red-950/60 border border-red-500/40 text-red-300 px-5 py-3 rounded-lg text-sm">
          <span className="text-red-400 font-bold">⚠ Backend Offline:</span>
          <span>{backendError}</span>
          <span className="ml-auto text-red-400/70 text-xs font-mono">Run: uvicorn main:app --reload  (in /backend)</span>
        </div>
      )}

      {/* Section B: System Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: "Total Projects", val: projects.length, icon: <FolderKanban className="w-5 h-5 text-blue-400" /> },
          { label: "Active Builds", val: activeBuilds, icon: <PlayCircle className="w-5 h-5 text-emerald-400" /> },
          { label: "Failed Builds", val: failedBuilds, icon: <AlertTriangle className="w-5 h-5 text-red-400" /> },
          { label: "Deployed Bundles", val: deployed, icon: <Package className="w-5 h-5 text-purple-400" /> },
        ].map((stat, i) => (
          <div key={i} className="bg-slate-900 border border-slate-800 p-5 rounded-xl shadow-sm flex items-center gap-4">
            <div className="bg-slate-800/50 p-3 rounded-lg border border-slate-700/50">
              {stat.icon}
            </div>
            <div>
              <p className="text-sm font-medium text-slate-400">{stat.label}</p>
              <h3 className="text-2xl font-bold text-white mt-1">{loading ? "-" : stat.val}</h3>
            </div>
          </div>
        ))}
      </div>

      {/* Section A: Control Panel (Spec Editor) & Status Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 h-[500px]">
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-sm flex flex-col">
          <div className="px-6 py-4 border-b border-slate-800 bg-slate-900/50 flex items-center justify-between">
            <h2 className="text-base font-semibold text-white">Compiler Console</h2>
          </div>
          <div className="flex-1 p-6">
             <SpecEditor onRun={handleRunCompiler} onValidate={handleValidateSpec} loading={running} />
          </div>
        </div>

        {/* Execution Status Panel placed next to the Spec Editor */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-sm flex flex-col">
          <ExecutionStatusPanel projectId={activeProjectId} />
        </div>
      </div>

      {/* Section C: Active Workspaces Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-sm">
        <div className="px-6 py-4 border-b border-slate-800 bg-slate-900/50">
          <h2 className="text-base font-semibold text-white">Recent Workspaces</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-slate-400 uppercase bg-slate-900/80 border-b border-slate-800">
              <tr>
                <th className="px-6 py-4 font-medium">Project ID</th>
                <th className="px-6 py-4 font-medium">Status</th>
                <th className="px-6 py-4 font-medium">Integrity</th>
                <th className="px-6 py-4 font-medium">Last Updated</th>
                <th className="px-6 py-4 font-medium text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/50 text-slate-300">
              {loading && projects.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-slate-500">
                    <Loader2 className="w-5 h-5 animate-spin mx-auto mb-2" /> Loading workspaces...
                  </td>
                </tr>
              ) : projects.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-slate-500">
                    No compiled workspaces found.
                  </td>
                </tr>
              ) : (
                projects.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-800/30 transition-colors">
                    <td className="px-6 py-4 font-medium text-slate-200">
                      <Link href={`/dashboard/project/${p.id}`} className="hover:text-blue-400 transition-colors">
                        {p.id}
                      </Link>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-semibold border ${
                        p.status === "SUCCESS" ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" :
                        p.status === "FAILED" ? "bg-red-500/10 text-red-400 border-red-500/20" :
                        "bg-blue-500/10 text-blue-400 border-blue-500/20"
                      }`}>
                        {p.status === "SUCCESS" && <CheckCircle className="w-3.5 h-3.5" />}
                        {p.status === "FAILED" && <AlertTriangle className="w-3.5 h-3.5" />}
                        {p.status === "RUNNING" && <Loader2 className="w-3.5 h-3.5 animate-spin" />}
                        {p.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 font-mono">
                      {p.planning_report?.graph_integrity_score ?? "-"}
                    </td>
                    <td className="px-6 py-4 text-slate-500">
                      {new Date(p.created_at).toLocaleString()}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <Link href={`/dashboard/project/${p.id}`} className="inline-flex items-center justify-center text-sm font-medium text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 px-3 py-1.5 rounded-md transition-colors border border-slate-700">
                        View Details
                      </Link>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
