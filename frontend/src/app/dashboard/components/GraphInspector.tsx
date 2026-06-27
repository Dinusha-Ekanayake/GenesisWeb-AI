"use client";

import { useState } from "react";
import { ChevronDown, ChevronRight, Share2 } from "lucide-react";

interface GraphInspectorProps {
  graphHashes?: Record<string, string>;
  // Ideally we would pass the actual graph JSON here, 
  // but since MVP specifies showing hashes and structured data, 
  // we'll display the hashes for now.
}

export default function GraphInspector({ graphHashes }: GraphInspectorProps) {
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});

  const toggle = (key: string) => {
    setExpanded(prev => ({ ...prev, [key]: !prev[key] }));
  };

  if (!graphHashes || Object.keys(graphHashes).length === 0) {
    return (
      <div className="text-slate-500 p-8 text-center bg-slate-50 dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800">
        <Share2 className="w-8 h-8 mx-auto mb-4 text-slate-400" />
        <p>No graphs generated yet. Run the compiler first.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {Object.entries(graphHashes).map(([graphName, hash]) => (
        <div key={graphName} className="bg-white dark:bg-slate-950 rounded-lg border border-slate-200 dark:border-slate-800 overflow-hidden shadow-sm">
          <button 
            onClick={() => toggle(graphName)}
            className="w-full flex items-center justify-between px-6 py-4 hover:bg-slate-50 dark:hover:bg-slate-900 transition-colors"
          >
            <div className="flex items-center gap-3">
              {expanded[graphName] ? <ChevronDown className="w-5 h-5 text-slate-400" /> : <ChevronRight className="w-5 h-5 text-slate-400" />}
              <h3 className="font-semibold text-slate-800 dark:text-slate-200">{graphName}</h3>
            </div>
            <span className="text-xs font-mono bg-slate-100 dark:bg-slate-800 px-3 py-1 rounded text-slate-500 truncate max-w-[200px]">
              {hash}
            </span>
          </button>
          
          {expanded[graphName] && (
            <div className="px-6 py-4 border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50">
              <p className="text-sm text-slate-500 mb-2">Deterministic SHA-256 Hash:</p>
              <code className="text-xs bg-slate-200 dark:bg-slate-800 px-2 py-1 rounded break-all text-slate-700 dark:text-slate-300">
                {hash}
              </code>
              <div className="mt-4 p-4 border border-slate-200 dark:border-slate-700 rounded bg-white dark:bg-slate-950 flex items-center justify-center text-slate-400 text-sm">
                [Full Graph JSON Visualization Pending API Endpoint Integration]
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
