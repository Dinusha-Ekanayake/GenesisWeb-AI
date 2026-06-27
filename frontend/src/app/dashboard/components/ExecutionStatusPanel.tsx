"use client";

import { useEffect, useState } from "react";
import { GenesisAPI } from "../lib/genesis-api";
import { ExecutionTrace } from "../types/genesis";
import { CheckCircle2, Circle, Loader2, Play } from "lucide-react";

interface ExecutionStatusPanelProps {
  projectId: string | null;
}

export default function ExecutionStatusPanel({ projectId }: ExecutionStatusPanelProps) {
  const [status, setStatus] = useState<string>("IDLE");
  const [traces, setTraces] = useState<ExecutionTrace[]>([]);

  useEffect(() => {
    if (!projectId) {
      setStatus("IDLE");
      setTraces([]);
      return;
    }

    let isMounted = true;

    const pollStatus = async () => {
      try {
        const data = await GenesisAPI.getProjectStatus(projectId);
        if (isMounted) {
          setStatus(data.status);
          setTraces(data.traces);
        }
      } catch (e) {
        console.error("Polling failed:", e);
      }
    };

    pollStatus();
    const interval = setInterval(pollStatus, 2500);

    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, [projectId]);

  if (!projectId) {
    return (
      <div className="bg-slate-50 dark:bg-slate-900 rounded-lg p-6 border border-slate-200 dark:border-slate-800 text-center text-slate-500 flex flex-col items-center justify-center h-full">
        <Play className="w-8 h-8 mb-4 text-slate-300" />
        <p>Awaiting compiler execution...</p>
      </div>
    );
  }

  const isComplete = status === "SUCCESS" || status === "FAILED";

  return (
    <div className="bg-white dark:bg-slate-950 rounded-lg border border-slate-200 dark:border-slate-800 p-6 shadow-sm h-full flex flex-col">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">Live Execution Status</h3>
        <div className="flex items-center gap-2">
          {!isComplete && <Loader2 className="w-4 h-4 animate-spin text-blue-500" />}
          <span className={`text-xs font-bold px-2 py-1 rounded-full ${
            status === "SUCCESS" ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-300" :
            status === "FAILED" ? "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300" :
            "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300"
          }`}>
            {status}
          </span>
        </div>
      </div>
      
      <div className="relative border-l border-slate-200 dark:border-slate-700 ml-4 space-y-6 flex-1 overflow-y-auto pr-2">
        {traces.map((trace, idx) => (
          <div key={idx} className="relative pl-6">
            <span className="absolute -left-[1.3rem] bg-white dark:bg-slate-950 top-1">
              {trace.event.toLowerCase().includes("fail") || trace.details?.status === "failed" ? (
                <Circle className="h-5 w-5 text-red-500 fill-red-500/20" />
              ) : (
                <CheckCircle2 className="h-5 w-5 text-emerald-500 fill-emerald-500/20" />
              )}
            </span>
            <div className="flex flex-col">
              <span className="text-sm font-semibold text-slate-800 dark:text-slate-200">
                {trace.event.replace(/([A-Z])/g, ' $1').trim()}
              </span>
              <span className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                {new Date(trace.timestamp).toLocaleTimeString()}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
