"use client";

import { useEffect, useState } from "react";
import { GenesisAPI } from "../lib/genesis-api";
import { ProjectData } from "../types/genesis";
import ProjectCard from "./ProjectCard";
import { Loader2 } from "lucide-react";

export default function ProjectList({ refreshTrigger }: { refreshTrigger: number }) {
  const [projects, setProjects] = useState<ProjectData[]>([]);
  const [loading, setLoading] = useState(true);

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
  }, [refreshTrigger]);

  if (loading) {
    return <div className="flex items-center gap-2 text-slate-500"><Loader2 className="animate-spin h-5 w-5"/> Loading...</div>;
  }

  if (projects.length === 0) {
    return (
      <div className="p-8 text-center bg-slate-50 dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800">
        <p className="text-slate-500">No compiled workspaces found.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {projects.map((p) => (
        <ProjectCard key={p.id} project={p} />
      ))}
    </div>
  );
}
