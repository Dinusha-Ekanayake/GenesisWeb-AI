"use client";

import React, { useState, useMemo } from "react";
import { useProjectGraphs } from "../lib/hooks";
import { ChevronDown, ChevronRight, Share2, Loader2, Maximize2, Network, FolderTree } from "lucide-react";
import dynamic from "next/dynamic";
import { Background, Controls, MiniMap } from "@xyflow/react";
import '@xyflow/react/dist/style.css';

// Lazy load React Flow to keep initial bundle small
const ReactFlow = dynamic(() => import("@xyflow/react").then(mod => mod.ReactFlow), { 
  ssr: false,
  loading: () => <div className="flex h-[500px] items-center justify-center bg-slate-900 border border-slate-800 rounded-lg"><Loader2 className="w-8 h-8 animate-spin text-slate-500" /></div>
});

// A simple recursive component for Mode A: Tree View
const JsonTreeViewer = React.memo(({ data, name = "root" }: { data: any, name?: string }) => {
  const [expanded, setExpanded] = useState(true);

  if (data === null) return <span className="text-slate-500">null</span>;
  if (typeof data !== "object") return <span className="text-emerald-400">{String(data)}</span>;

  const isArray = Array.isArray(data);
  const keys = Object.keys(data);

  if (keys.length === 0) return <span className="text-slate-500">{isArray ? "[]" : "{}"}</span>;

  return (
    <div className="font-mono text-sm ml-4">
      <div 
        className="flex items-center cursor-pointer hover:text-blue-400 text-slate-300"
        onClick={() => setExpanded(!expanded)}
      >
        {expanded ? <ChevronDown className="w-3 h-3 mr-1" /> : <ChevronRight className="w-3 h-3 mr-1" />}
        <span className="text-blue-300 mr-2">{name}:</span>
        {!expanded && <span className="text-slate-500">{isArray ? "[...]" : "{...}"}</span>}
      </div>
      {expanded && (
        <div className="border-l border-slate-800 ml-1.5 pl-3 mt-1">
          {keys.map((key) => (
            <div key={key} className="my-1">
              {typeof data[key] === "object" && data[key] !== null ? (
                <JsonTreeViewer data={data[key]} name={key} />
              ) : (
                <div className="flex ml-4">
                  <span className="text-blue-300 mr-2">{key}:</span>
                  <span className={typeof data[key] === "string" ? "text-amber-300" : "text-emerald-400"}>
                    {typeof data[key] === "string" ? `"${data[key]}"` : String(data[key])}
                  </span>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
});
JsonTreeViewer.displayName = "JsonTreeViewer";

export default function GraphInspector({ projectId }: { projectId: string }) {
  const { data: rawGraphs, isLoading, error } = useProjectGraphs(projectId);
  const graphs = rawGraphs as Record<string, any> | undefined;
  const [activeGraph, setActiveGraph] = useState<string | null>(null);
  const [mode, setMode] = useState<"tree" | "flow">("flow");

  const flowData = useMemo(() => {
    if (!activeGraph || !graphs || !graphs[activeGraph]) return { nodes: [], edges: [] };
    
    const graphData = graphs[activeGraph];
    const nodes: any[] = [];
    const edges: any[] = [];

    // Simple heuristic to extract nodes and edges from Genesis JSON
    // Looks for arrays of objects that might represent entities (e.g., endpoints, pages, components)
    let yOffset = 0;
    
    const processItems = (items: any[]) => {
      items.forEach((item, index) => {
        if (!item.id && !item.name) return;
        
        const nodeId = item.id || item.name;
        nodes.push({
          id: nodeId,
          position: { x: (index % 3) * 250, y: Math.floor(index / 3) * 150 },
          data: { label: <div className="p-2 font-mono text-xs">{item.name || item.id}</div> },
          style: { background: '#1e293b', color: '#f8fafc', border: '1px solid #334155', borderRadius: '8px' }
        });

        // Dependencies
        if (item.metadata?.depends_on) {
          item.metadata.depends_on.forEach((dep: string) => {
            edges.push({
              id: `e-${nodeId}-${dep}`,
              source: dep,
              target: nodeId,
              animated: true,
              style: { stroke: '#64748b' }
            });
          });
        }
      });
    };

    if (graphData.endpoints) processItems(graphData.endpoints);
    else if (graphData.pages) processItems(graphData.pages);
    else if (graphData.components) processItems(graphData.components);
    else if (graphData.features) processItems(graphData.features);
    else if (graphData.tables) processItems(graphData.tables);

    return { nodes, edges };
  }, [graphs, activeGraph]);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center p-12 bg-slate-900 rounded-lg border border-slate-800">
        <Loader2 className="w-8 h-8 animate-spin text-slate-500 mb-4" />
        <p className="text-slate-400">Loading dependency graphs...</p>
      </div>
    );
  }

  if (error || !graphs || Object.keys(graphs).length === 0) {
    return (
      <div className="text-slate-500 p-8 text-center bg-slate-900 rounded-lg border border-slate-800">
        <Share2 className="w-8 h-8 mx-auto mb-4 text-slate-600" />
        <p>No graphs available. Has the compiler run yet?</p>
      </div>
    );
  }

  const graphNames = Object.keys(graphs);
  if (!activeGraph && graphNames.length > 0) setActiveGraph(graphNames[0]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex space-x-2 overflow-x-auto pb-2 custom-scrollbar">
          {graphNames.map(name => (
            <button
              key={name}
              onClick={() => setActiveGraph(name)}
              className={`px-4 py-2 text-sm font-medium rounded-md whitespace-nowrap transition-colors ${
                activeGraph === name 
                  ? "bg-blue-600 text-white" 
                  : "bg-slate-800 text-slate-300 hover:bg-slate-700"
              }`}
            >
              {name.replace(/_/g, ' ').replace('.json', '')}
            </button>
          ))}
        </div>

        <div className="flex items-center bg-slate-800 rounded-md p-1 border border-slate-700 ml-4">
          <button
            onClick={() => setMode("flow")}
            className={`px-3 py-1.5 rounded text-xs font-semibold flex items-center gap-1.5 ${mode === "flow" ? "bg-slate-700 text-white shadow-sm" : "text-slate-400 hover:text-slate-300"}`}
          >
            <Network className="w-3.5 h-3.5" /> Flow
          </button>
          <button
            onClick={() => setMode("tree")}
            className={`px-3 py-1.5 rounded text-xs font-semibold flex items-center gap-1.5 ${mode === "tree" ? "bg-slate-700 text-white shadow-sm" : "text-slate-400 hover:text-slate-300"}`}
          >
            <FolderTree className="w-3.5 h-3.5" /> Tree
          </button>
        </div>
      </div>

      <div className="bg-slate-950 rounded-xl border border-slate-800 overflow-hidden shadow-inner h-[600px] relative">
        {mode === "tree" ? (
          <div className="absolute inset-0 p-6 overflow-auto custom-scrollbar">
            <JsonTreeViewer data={graphs[activeGraph || ""]} />
          </div>
        ) : (
          <div className="absolute inset-0">
            {flowData.nodes.length > 0 ? (
              <ReactFlow 
                nodes={flowData.nodes} 
                edges={flowData.edges}
                fitView
                className="bg-slate-950"
              >
                <Background color="#334155" gap={16} />
                <Controls className="bg-slate-800 border-slate-700 fill-slate-300" />
                <MiniMap style={{ backgroundColor: '#0f172a' }} nodeColor="#334155" maskColor="rgba(15, 23, 42, 0.7)" />
              </ReactFlow>
            ) : (
              <div className="flex items-center justify-center h-full text-slate-500">
                This graph could not be mapped to Flow nodes. Switch to Tree mode.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
