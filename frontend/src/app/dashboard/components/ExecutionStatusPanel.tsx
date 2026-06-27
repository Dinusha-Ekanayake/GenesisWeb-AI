"use client";

import { useEffect, useState, useRef } from "react";
import { GenesisAPI } from "../lib/genesis-api";
import { ExecutionTrace } from "../types/genesis";
import { CheckCircle2, Circle, Loader2, ServerCrash, Zap } from "lucide-react";

interface ExecutionStatusPanelProps {
  projectId: string | null;
}

export default function ExecutionStatusPanel({ projectId }: ExecutionStatusPanelProps) {
  const [status, setStatus] = useState<string>("IDLE");
  const [traces, setTraces] = useState<ExecutionTrace[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

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
    const interval = setInterval(pollStatus, 2000);

    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, [projectId]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [traces]);

  if (!projectId) {
    return (
      <div className="bg-slate-900 rounded-xl border border-slate-800 p-8 text-center text-slate-500 flex flex-col items-center justify-center h-full shadow-sm">
        <div className="w-16 h-16 rounded-full bg-slate-800/50 flex items-center justify-center mb-4 border border-slate-700/50">
          <Zap className="w-6 h-6 text-slate-400" />
        </div>
        <h3 className="text-lg font-medium text-slate-300 mb-2">Awaiting Execution</h3>
        <p className="text-sm max-w-[250px]">Submit a specification to monitor the Genesis Engine pipeline live.</p>
      </div>
    );
  }

  const isComplete = status === "SUCCESS" || status === "FAILED";

  return (
    <div className="bg-slate-900 rounded-xl border border-slate-800 flex flex-col h-full shadow-sm overflow-hidden">
      
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-900/50">
        <h3 className="text-base font-semibold text-white flex items-center gap-2">
          {!isComplete && <Loader2 className="w-4 h-4 animate-spin text-blue-500" />}
          Live Telemetry
        </h3>
        <span className={`text-xs font-bold px-2.5 py-1 rounded-md border ${
          status === "SUCCESS" ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" :
          status === "FAILED" ? "bg-red-500/10 text-red-400 border-red-500/20" :
          "bg-blue-500/10 text-blue-400 border-blue-500/20"
        }`}>
          {status}
        </span>
      </div>
      
      {/* Timeline Body */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-6 scroll-smooth"
      >
        <div className="relative border-l-2 border-slate-800 ml-3 space-y-8">
          {traces.length === 0 && !isComplete && (
            <div className="pl-8 text-sm text-slate-500 italic animate-pulse">Initializing compiler pipeline...</div>
          )}
          {traces.map((trace, idx) => {
            const isError = trace.event.toLowerCase().includes("fail") || trace.details?.status === "failed";
            return (
              <div key={idx} className="relative pl-8 animate-in slide-in-from-left-2 fade-in duration-300">
                <span className="absolute -left-[11px] bg-slate-900 top-0.5">
                  {isError ? (
                    <ServerCrash className="h-5 w-5 text-red-500 fill-red-500/10" />
                  ) : (
                    <CheckCircle2 className="h-5 w-5 text-blue-500 fill-blue-500/10" />
                  )}
                </span>
                <div className="flex flex-col">
                  <span className={`text-sm font-semibold ${isError ? "text-red-400" : "text-slate-200"}`}>
                    {trace.event.replace(/([A-Z])/g, ' $1').trim()}
                  </span>
                  <span className="text-xs text-slate-500 font-mono mt-1">
                    {new Date(trace.timestamp).toLocaleTimeString([], { hour12: false, fractionalSecondDigits: 3 })}
                  </span>
                  
                  {trace.details && Object.keys(trace.details).length > 0 && (
                    <div className="mt-3 bg-slate-950 rounded-md border border-slate-800 p-3 shadow-inner">
                      <pre className="text-xs font-mono text-slate-400 overflow-x-auto">
                        {JSON.stringify(trace.details, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
