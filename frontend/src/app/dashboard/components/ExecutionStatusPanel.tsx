"use client";

import { useEffect, useRef, useMemo } from "react";
import { useProjectStatus, useProjectTelemetry } from "../lib/hooks";
import { CheckCircle2, Loader2, ServerCrash, Zap, Clock, TrendingUp, AlertTriangle } from "lucide-react";

interface ExecutionStatusPanelProps {
  projectId: string | null;
}

const PHASES = ["Planning", "Validation", "Generation", "Packaging"];

export default function ExecutionStatusPanel({ projectId }: ExecutionStatusPanelProps) {
  const { data: statusData } = useProjectStatus(projectId);
  const { data: traces = [] } = useProjectTelemetry(projectId);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [traces]);

  // Compute pipeline state
  const currentPhase = useMemo(() => {
    if (!traces || traces.length === 0) return "Planning";
    const lastTrace = traces[traces.length - 1];
    
    // Simple heuristic to map event names to phases
    const eventName = lastTrace.event.toLowerCase();
    if (eventName.includes("packag") || eventName.includes("deploy")) return "Packaging";
    if (eventName.includes("generat") || eventName.includes("build")) return "Generation";
    if (eventName.includes("validat")) return "Validation";
    return "Planning";
  }, [traces]);

  // Compute metrics
  const metrics = useMemo(() => {
    if (!traces || traces.length < 2) return null;
    
    const startTime = new Date(traces[0].timestamp).getTime();
    const endTime = new Date(traces[traces.length - 1].timestamp).getTime();
    const totalTimeMs = endTime - startTime;
    
    // Group traces by phase to find longest phase
    const phaseTimes: Record<string, { start: number, end: number }> = {};
    let currentP = "Planning";
    
    traces.forEach(trace => {
      const eventName = trace.event.toLowerCase();
      if (eventName.includes("packag") || eventName.includes("deploy")) currentP = "Packaging";
      else if (eventName.includes("generat") || eventName.includes("build")) currentP = "Generation";
      else if (eventName.includes("validat")) currentP = "Validation";
      
      const ts = new Date(trace.timestamp).getTime();
      if (!phaseTimes[currentP]) phaseTimes[currentP] = { start: ts, end: ts };
      else phaseTimes[currentP].end = ts;
    });

    let longestPhase = "";
    let maxDuration = 0;
    let totalPhaseDuration = 0;
    let phaseCount = 0;

    Object.entries(phaseTimes).forEach(([phase, times]) => {
      const duration = times.end - times.start;
      totalPhaseDuration += duration;
      phaseCount++;
      if (duration > maxDuration) {
        maxDuration = duration;
        longestPhase = phase;
      }
    });

    const formatMs = (ms: number) => (ms / 1000).toFixed(1) + "s";

    return {
      totalTime: formatMs(totalTimeMs),
      longestPhase: `${longestPhase} (${formatMs(maxDuration)})`,
      avgPhase: formatMs(phaseCount > 0 ? totalPhaseDuration / phaseCount : 0)
    };
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

  const status = statusData?.status || "RUNNING";
  const isComplete = status === "SUCCESS" || status === "FAILED";

  return (
    <div className="bg-slate-900 rounded-xl border border-slate-800 flex flex-col h-full shadow-sm overflow-hidden">
      
      {/* Header Pipeline */}
      <div className="border-b border-slate-800 bg-slate-900/50 p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-base font-semibold text-white flex items-center gap-2">
            {!isComplete && <Loader2 className="w-4 h-4 animate-spin text-blue-500" />}
            Compiler Pipeline
          </h3>
          <span className={`text-xs font-bold px-2.5 py-1 rounded-md border ${
            status === "SUCCESS" ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" :
            status === "FAILED" ? "bg-red-500/10 text-red-400 border-red-500/20" :
            "bg-blue-500/10 text-blue-400 border-blue-500/20"
          }`}>
            {status}
          </span>
        </div>

        {/* Phase Stepper */}
        <div className="flex items-center justify-between relative">
          <div className="absolute left-0 right-0 top-1/2 -translate-y-1/2 h-0.5 bg-slate-800 -z-10" />
          {PHASES.map((phase, idx) => {
            const isPast = PHASES.indexOf(currentPhase) > idx;
            const isCurrent = currentPhase === phase && !isComplete;
            const isErrorPhase = status === "FAILED" && currentPhase === phase;

            return (
              <div key={phase} className="flex flex-col items-center gap-2 bg-slate-900 px-2 z-10">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center border-2 transition-colors ${
                  isErrorPhase ? "bg-red-950 border-red-500 text-red-400" :
                  isPast || (isComplete && status === "SUCCESS") ? "bg-emerald-950 border-emerald-500 text-emerald-400" :
                  isCurrent ? "bg-blue-950 border-blue-500 text-blue-400 shadow-[0_0_15px_rgba(59,130,246,0.5)]" :
                  "bg-slate-900 border-slate-700 text-slate-600"
                }`}>
                  {isErrorPhase ? <AlertTriangle className="w-4 h-4" /> :
                   isPast || (isComplete && status === "SUCCESS") ? <CheckCircle2 className="w-4 h-4" /> :
                   isCurrent ? <Loader2 className="w-4 h-4 animate-spin" /> :
                   <span className="text-xs font-bold">{idx + 1}</span>}
                </div>
                <span className={`text-xs font-medium ${isCurrent || isPast ? "text-slate-300" : "text-slate-500"}`}>{phase}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Metrics Row */}
      {metrics && (
        <div className="grid grid-cols-3 divide-x divide-slate-800 border-b border-slate-800 bg-slate-900/30">
          <div className="p-3 text-center">
            <p className="text-[10px] uppercase tracking-wider text-slate-500 mb-1 flex items-center justify-center gap-1"><Clock className="w-3 h-3" /> Total Time</p>
            <p className="text-sm font-mono text-slate-300">{metrics.totalTime}</p>
          </div>
          <div className="p-3 text-center">
            <p className="text-[10px] uppercase tracking-wider text-slate-500 mb-1 flex items-center justify-center gap-1"><TrendingUp className="w-3 h-3" /> Longest Phase</p>
            <p className="text-sm font-mono text-slate-300">{metrics.longestPhase}</p>
          </div>
          <div className="p-3 text-center">
            <p className="text-[10px] uppercase tracking-wider text-slate-500 mb-1 flex items-center justify-center gap-1"><Zap className="w-3 h-3" /> Avg Phase</p>
            <p className="text-sm font-mono text-slate-300">{metrics.avgPhase}</p>
          </div>
        </div>
      )}
      
      {/* Timeline Body */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-6 scroll-smooth bg-slate-950/50"
      >
        <div className="relative border-l-2 border-slate-800 ml-3 space-y-8">
          {traces.length === 0 && !isComplete && (
            <div className="pl-8 text-sm text-slate-500 italic animate-pulse">Initializing compiler pipeline...</div>
          )}
          {traces.map((trace: any, idx: number) => {
            const isError = trace.event.toLowerCase().includes("fail") || trace.details?.status === "failed";
            return (
              <div key={idx} className="relative pl-8 animate-in slide-in-from-left-2 fade-in duration-300">
                <span className="absolute -left-[11px] bg-slate-950 top-0.5 rounded-full">
                  {isError ? (
                    <ServerCrash className="h-5 w-5 text-red-500 fill-red-500/10" />
                  ) : (
                    <CheckCircle2 className="h-5 w-5 text-blue-500 fill-blue-500/10 bg-slate-950" />
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
                    <div className="mt-3 bg-slate-900 rounded-md border border-slate-800 p-3 shadow-inner">
                      <pre className="text-xs font-mono text-slate-400 overflow-x-auto custom-scrollbar">
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
