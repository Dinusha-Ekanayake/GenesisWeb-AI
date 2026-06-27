"use client";

import { ExecutionTrace } from "../types/genesis";
import { CheckCircle2, Circle, Clock } from "lucide-react";

interface ExecutionTimelineProps {
  traces: ExecutionTrace[];
}

export default function ExecutionTimeline({ traces }: ExecutionTimelineProps) {
  if (!traces || traces.length === 0) {
    return (
      <div className="text-slate-500 flex flex-col items-center justify-center p-12 bg-slate-50 dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800">
        <Clock className="w-8 h-8 mb-4 text-slate-400" />
        <p>No execution trace available for this project.</p>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-slate-950 rounded-lg border border-slate-200 dark:border-slate-800 p-6 shadow-sm">
      <h3 className="text-lg font-semibold mb-6 text-slate-900 dark:text-slate-100">Compiler Execution Timeline</h3>
      <div className="relative border-l border-slate-200 dark:border-slate-700 ml-4 space-y-8">
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
                {new Date(trace.timestamp).toLocaleString()}
              </span>
              {trace.details && (
                <div className="mt-2 bg-slate-50 dark:bg-slate-900 rounded border border-slate-200 dark:border-slate-800 p-3">
                  <pre className="text-xs font-mono text-slate-600 dark:text-slate-400 overflow-x-auto whitespace-pre-wrap">
                    {JSON.stringify(trace.details, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
