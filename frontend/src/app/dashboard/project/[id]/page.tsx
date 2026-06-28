"use client";

import { useState } from "react";
import { useProjectStatus, useProject, useProjectTelemetry } from "../../lib/hooks";
import { ArrowLeft, Loader2, Calendar, FileText, CheckCircle2, AlertTriangle, PlayCircle } from "lucide-react";
import Link from "next/link";
import PlanningReportViewer from "../../components/PlanningReportViewer";
import GraphInspector from "../../components/GraphInspector";
import ExecutionTimeline from "../../components/ExecutionTimeline";
import DeploymentPanel from "../../components/DeploymentPanel";
import WorkspaceExplorer from "../../components/WorkspaceExplorer";
import { useSSE } from "../../lib/hooks";

export default function ProjectDetail({ params }: { params: { id: string } }) {
  const { data: statusData, isLoading: statusLoading, error: statusError } = useProjectStatus(params.id);
  const { data: project } = useProject(params.id);
  const [activeTab, setActiveTab] = useState<"overview" | "planning" | "graphs" | "trace" | "deployment" | "workspace">("overview");

  // Hook handles live SSE updates
  useSSE(params.id);

  if (statusLoading) {
    return (
      <div className="flex flex-col items-center justify-center h-96 text-slate-500">
        <Loader2 className="w-8 h-8 animate-spin mb-4 text-blue-500" />
        <p>Loading Workspace Status...</p>
      </div>
    );
  }

  if (statusError || !statusData) {
    return (
      <div className="flex flex-col items-center justify-center h-96 text-slate-500 bg-slate-900 border border-slate-800 rounded-xl">
        <FileText className="w-12 h-12 mb-4 text-slate-700" />
        <p>Workspace not found.</p>
        <Link href="/dashboard" className="text-blue-400 mt-4 hover:underline">Return to Dashboard</Link>
      </div>
    );
  }

  const tabs = [
    { id: "overview", label: "Overview" },
    { id: "workspace", label: "Workspace Explorer" },
    { id: "planning", label: "Planning Report" },
    { id: "graphs", label: "Graph Inspector" },
    { id: "trace", label: "Execution Trace" },
    { id: "deployment", label: "Deployment Bundle" }
  ] as const;

  return (
    <div className="max-w-7xl mx-auto space-y-6 animate-in fade-in duration-500">
      
      {/* Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 flex flex-col md:flex-row justify-between items-start md:items-end gap-6 shadow-sm">
        <div className="space-y-4">
          <Link href="/dashboard" className="inline-flex items-center text-xs font-medium text-slate-500 hover:text-slate-300 transition-colors focus-visible:ring-2 focus-visible:ring-blue-500 rounded outline-none">
            <ArrowLeft className="w-4 h-4 mr-1" /> Back to Workspaces
          </Link>
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white">{statusData.id.replace("_", " ").title()}</h1>
            <div className="flex flex-wrap items-center gap-4 mt-3 text-sm text-slate-400">
              <span className="flex items-center font-mono bg-slate-800 px-2 py-1 rounded text-slate-300">
                <FileText className="w-3.5 h-3.5 mr-1.5 opacity-70" /> {statusData.id}
              </span>
              <span className="flex items-center">
                <Calendar className="w-3.5 h-3.5 mr-1.5 opacity-70" /> {new Date(statusData.created_at).toLocaleString()}
              </span>
            </div>
          </div>
        </div>
        
        <span className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-md text-sm font-bold border shadow-sm ${
          statusData.status === "SUCCESS" ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" :
          statusData.status === "FAILED" ? "bg-red-500/10 text-red-400 border-red-500/20" :
          "bg-blue-500/10 text-blue-400 border-blue-500/20"
        }`} aria-live="polite">
          {statusData.status === "SUCCESS" && <CheckCircle2 className="w-4 h-4" />}
          {statusData.status === "FAILED" && <AlertTriangle className="w-4 h-4" />}
          {statusData.status === "RUNNING" && <PlayCircle className="w-4 h-4 animate-pulse" />}
          {statusData.status}
        </span>
      </div>

      {/* Tabs Layout */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl shadow-sm overflow-hidden min-h-[600px] flex flex-col">
        <div className="flex overflow-x-auto border-b border-slate-800 bg-slate-900/50" role="tablist" aria-label="Project Sections">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              role="tab"
              aria-selected={activeTab === tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-6 py-4 text-sm font-semibold transition-colors whitespace-nowrap border-b-2 outline-none focus-visible:bg-slate-800/50 ${
                activeTab === tab.id 
                  ? "border-blue-500 text-blue-400 bg-blue-500/5" 
                  : "border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        <div className="flex-1 overflow-auto bg-slate-950 p-6 md:p-8">
          {activeTab === "overview" && (
            <div className="space-y-6">
              <h3 className="text-lg font-semibold text-white mb-6">Specification Summary</h3>
              {project?.spec ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div className="space-y-6">
                    <div>
                      <p className="text-sm font-medium text-slate-500 mb-1">Project Name</p>
                      <p className="text-slate-200">{project.spec.name}</p>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-slate-500 mb-1">Description</p>
                      <p className="text-slate-300 leading-relaxed bg-slate-800/50 p-4 rounded-lg border border-slate-800">{project.spec.description}</p>
                    </div>
                  </div>
                  <div className="space-y-6">
                    <div>
                      <p className="text-sm font-medium text-slate-500 mb-2">Pages Defined</p>
                      <div className="flex flex-wrap gap-2">
                        {project.spec.pages.map((p: string) => (
                          <span key={p} className="px-3 py-1 bg-slate-800 border border-slate-700 rounded-full text-xs text-slate-300 font-medium">{p}</span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-slate-500 mb-2">Components Defined</p>
                      <div className="flex flex-wrap gap-2">
                        {project.spec.components.map((c: string) => (
                          <span key={c} className="px-3 py-1 bg-slate-800 border border-slate-700 rounded-full text-xs text-slate-300 font-medium">{c}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-center p-12 border border-dashed border-slate-700 rounded-lg text-slate-500">
                  No specification payload captured.
                </div>
              )}
            </div>
          )}

          {activeTab === "workspace" && (
            <WorkspaceExplorer projectId={params.id} />
          )}

          {activeTab === "planning" && (
            <PlanningReportViewer projectId={params.id} />
          )}

          {activeTab === "graphs" && (
            <GraphInspector projectId={params.id} />
          )}

          {activeTab === "trace" && (
            <ExecutionTimeline projectId={params.id} />
          )}

          {activeTab === "deployment" && (
            <DeploymentPanel projectId={params.id} />
          )}
        </div>
      </div>
    </div>
  );
}
