"use client";

import { useEffect, useState } from "react";
import { GenesisAPI } from "../../lib/genesis-api";
import { ProjectData } from "../../types/genesis";
import { ArrowLeft, Loader2, Play } from "lucide-react";
import Link from "next/link";
import PlanningReportViewer from "../../components/PlanningReportViewer";
import GraphInspector from "../../components/GraphInspector";
import ExecutionTimeline from "../../components/ExecutionTimeline";
import DeploymentPanel from "../../components/DeploymentPanel";

export default function ProjectDetail({ params }: { params: { id: string } }) {
  const [project, setProject] = useState<ProjectData | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"overview" | "planning" | "graphs" | "trace" | "deployment">("overview");

  const fetchProject = async () => {
    try {
      const data = await GenesisAPI.getProject(params.id);
      setProject(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProject();
  }, [params.id]);

  const handleDeploy = async () => {
    try {
      await GenesisAPI.deployProject(params.id);
      await fetchProject();
    } catch (e: any) {
      alert(`Deployment Error: ${e.message}`);
    }
  };

  if (loading) {
    return <div className="p-12 flex justify-center"><Loader2 className="w-8 h-8 animate-spin text-slate-400" /></div>;
  }

  if (!project) {
    return <div className="p-12 text-center text-slate-500">Workspace not found.</div>;
  }

  const tabs = [
    { id: "overview", label: "Overview" },
    { id: "planning", label: "Planning Report" },
    { id: "graphs", label: "Graph Inspector" },
    { id: "trace", label: "Execution Trace" },
    { id: "deployment", label: "Deployment Bundle" }
  ] as const;

  return (
    <div className="p-8 max-w-6xl mx-auto min-h-screen dark:bg-slate-950">
      <div className="mb-8">
        <Link href="/dashboard" className="inline-flex items-center text-sm text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 mb-4 transition-colors">
          <ArrowLeft className="w-4 h-4 mr-1" /> Back to Dashboard
        </Link>
        <div className="flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">{project.title}</h1>
            <p className="text-slate-500 mt-2 font-mono text-sm">{project.id}</p>
          </div>
          <span className={`text-sm font-bold px-3 py-1 rounded-full ${
            project.status === "SUCCESS" ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-300" :
            project.status === "FAILED" ? "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300" :
            "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
          }`}>
            {project.status}
          </span>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex space-x-1 border-b border-slate-200 dark:border-slate-800 mb-8 overflow-x-auto">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors whitespace-nowrap ${
              activeTab === tab.id 
                ? "border-blue-500 text-blue-600 dark:text-blue-400" 
                : "border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300 dark:text-slate-400 dark:hover:text-slate-300"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="pb-24">
        {activeTab === "overview" && (
          <div className="space-y-6">
            <div className="bg-white dark:bg-slate-900 p-6 rounded-lg border border-slate-200 dark:border-slate-800">
              <h3 className="text-lg font-semibold mb-4 text-slate-800 dark:text-slate-200">Specification Summary</h3>
              {project.spec ? (
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-slate-500 block mb-1">Name</span>
                    <span className="font-medium text-slate-900 dark:text-slate-100">{project.spec.name}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block mb-1">Description</span>
                    <span className="text-slate-700 dark:text-slate-300">{project.spec.description}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block mb-1">Pages ({project.spec.pages.length})</span>
                    <span className="text-slate-700 dark:text-slate-300">{project.spec.pages.join(", ")}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block mb-1">Components ({project.spec.components.length})</span>
                    <span className="text-slate-700 dark:text-slate-300">{project.spec.components.join(", ")}</span>
                  </div>
                </div>
              ) : (
                <p className="text-slate-500">No specification found.</p>
              )}
            </div>
          </div>
        )}

        {activeTab === "planning" && (
          project.planning_report ? (
            <PlanningReportViewer report={project.planning_report} />
          ) : (
            <div className="text-center p-12 bg-slate-50 dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 text-slate-500">
              Planning report not available yet.
            </div>
          )
        )}

        {activeTab === "graphs" && (
          <GraphInspector graphHashes={project.planning_report?.graph_hashes} />
        )}

        {activeTab === "trace" && (
          <ExecutionTimeline traces={project.execution_trace || []} />
        )}

        {activeTab === "deployment" && (
          <DeploymentPanel 
            manifest={project.deployment_manifest} 
            onDeploy={handleDeploy} 
            loading={false} 
          />
        )}
      </div>
    </div>
  );
}
