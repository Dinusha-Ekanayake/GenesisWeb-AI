"use client";

import { ProjectData } from "../types/genesis";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowRight, Clock, ShieldCheck } from "lucide-react";
import Link from "next/link";

interface ProjectCardProps {
  project: ProjectData;
}

export default function ProjectCard({ project }: ProjectCardProps) {
  const isSuccess = project.status === "SUCCESS";
  const isFailed = project.status === "FAILED";

  const integrityScore = project.planning_report?.graph_integrity_score ?? "N/A";

  return (
    <Card className="hover:border-blue-300 dark:hover:border-blue-700 transition-colors bg-white dark:bg-slate-900 shadow-sm">
      <CardHeader className="pb-3">
        <div className="flex justify-between items-start">
          <CardTitle className="truncate pr-4 text-slate-800 dark:text-slate-200">
            {project.title}
          </CardTitle>
          <span className={`text-xs font-bold px-2 py-1 rounded-full flex-shrink-0 ${
            isSuccess ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-300" :
            isFailed ? "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300" :
            "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
          }`}>
            {project.status}
          </span>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-2 mb-4">
          <div className="flex items-center text-sm text-slate-500">
            <Clock className="w-4 h-4 mr-2" />
            <span>{new Date(project.created_at).toLocaleString()}</span>
          </div>
          <div className="flex items-center text-sm text-slate-500">
            <ShieldCheck className="w-4 h-4 mr-2" />
            <span>Integrity Score: {integrityScore}</span>
          </div>
        </div>
        <Link href={`/dashboard/project/${project.id}`} passHref>
          <Button variant="outline" className="w-full justify-between hover:bg-slate-50 dark:hover:bg-slate-800">
            Open Workspace <ArrowRight className="h-4 w-4" />
          </Button>
        </Link>
      </CardContent>
    </Card>
  );
}
