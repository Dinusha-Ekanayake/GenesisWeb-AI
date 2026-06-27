"use client";

import { useState } from "react";
import { GenesisAPI } from "./lib/genesis-api";
import { ProjectSpecification } from "./types/genesis";
import { Activity } from "lucide-react";
import SpecEditor from "./components/SpecEditor";
import ProjectList from "./components/ProjectList";
import ExecutionStatusPanel from "./components/ExecutionStatusPanel";

export default function DashboardHome() {
  const [running, setRunning] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [activeProjectId, setActiveProjectId] = useState<string | null>(null);

  const handleRunCompiler = async (spec: ProjectSpecification) => {
    setRunning(true);
    setActiveProjectId(spec.project_id);
    try {
      await GenesisAPI.runCompiler(spec);
      setRefreshTrigger(prev => prev + 1);
    } catch (e: any) {
      alert(`Compiler Error: ${e.message}`);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 min-h-screen dark:bg-slate-950">
      <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">Genesis Control Plane</h1>
          <p className="text-slate-500 mt-2">Deterministic Compiler Dashboard</p>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-400 rounded-full text-sm font-medium border border-emerald-200 dark:border-emerald-800 shadow-sm">
          <Activity className="w-4 h-4 animate-pulse" /> System Online
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Spec Editor & Status Panel */}
        <div className="lg:col-span-1 flex flex-col gap-8 h-[800px]">
          <div className="flex-1">
            <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-200 mb-4 uppercase tracking-wide text-sm">Compiler Console</h2>
            <SpecEditor onRun={handleRunCompiler} loading={running} />
          </div>
          <div className="flex-1">
            <ExecutionStatusPanel projectId={activeProjectId} />
          </div>
        </div>

        {/* Right Column: Projects List */}
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-200 mb-4 uppercase tracking-wide text-sm">Active Workspaces</h2>
          <ProjectList refreshTrigger={refreshTrigger} />
        </div>
      </div>
    </div>
  );
}
