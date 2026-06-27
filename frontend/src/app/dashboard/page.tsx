"use client";

import { useEffect, useState } from "react";
import { GenesisAPI } from "./lib/genesis-api";
import { ProjectData, ProjectSpecification } from "./types/genesis";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowRight, Loader2, Activity } from "lucide-react";
import SpecEditor from "./components/SpecEditor";
import Link from "next/link";

export default function DashboardHome() {
  const [projects, setProjects] = useState<ProjectData[]>([]);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);

  const fetchProjects = async () => {
    try {
      const data = await GenesisAPI.getProjects();
      setProjects(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
    const interval = setInterval(fetchProjects, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleRunCompiler = async (spec: ProjectSpecification) => {
    setRunning(true);
    try {
      // For MVP, we use validate -> deploy manually or full run if backend supports it.
      // Since backend has /run that does full pipeline:
      await GenesisAPI.runCompiler(spec);
      await fetchProjects();
    } catch (e: any) {
      alert(`Compiler Error: ${e.message}`);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 min-h-screen dark:bg-slate-950">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">Genesis Control Plane</h1>
          <p className="text-slate-500 mt-2">Deterministic Compiler Dashboard</p>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400 rounded-full text-sm font-medium border border-blue-200 dark:border-blue-800">
          <Activity className="w-4 h-4 animate-pulse" /> System Online
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Projects List */}
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-xl font-semibold text-slate-800 dark:text-slate-200">Active Workspaces</h2>
          {loading ? (
            <div className="flex items-center gap-2 text-slate-500"><Loader2 className="animate-spin h-5 w-5"/> Loading...</div>
          ) : projects.length === 0 ? (
            <div className="p-8 text-center bg-slate-50 dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800">
              <p className="text-slate-500">No compiled workspaces found.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {projects.map((p) => (
                <Card key={p.id} className="hover:border-blue-300 dark:hover:border-blue-700 transition-colors bg-white dark:bg-slate-900 shadow-sm">
                  <CardHeader className="pb-3">
                    <div className="flex justify-between items-start">
                      <CardTitle className="truncate pr-4 text-slate-800 dark:text-slate-200">{p.title}</CardTitle>
                      <span className={`text-xs font-bold px-2 py-1 rounded-full flex-shrink-0 ${
                        p.status === "SUCCESS" ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-300" :
                        p.status === "FAILED" ? "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300" :
                        "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
                      }`}>
                        {p.status}
                      </span>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-slate-500 mb-4 font-mono">
                      {p.id}
                    </p>
                    <Link href={`/dashboard/project/${p.id}`} passHref>
                      <Button variant="outline" className="w-full justify-between hover:bg-slate-50 dark:hover:bg-slate-800">
                        Open Workspace <ArrowRight className="h-4 w-4" />
                      </Button>
                    </Link>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>

        {/* Right Column: Spec Editor */}
        <div className="lg:col-span-1 h-[600px]">
          <h2 className="text-xl font-semibold text-slate-800 dark:text-slate-200 mb-4">Compiler Console</h2>
          <SpecEditor onRun={handleRunCompiler} loading={running} />
        </div>
      </div>
    </div>
  );
}
