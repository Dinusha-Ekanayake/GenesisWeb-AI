"use client";

import React, { useState, useCallback, useMemo } from "react";
import { useProjectWorkspace, useProjectFile } from "../lib/hooks";
import { ChevronRight, ChevronDown, File, Folder, Loader2 } from "lucide-react";
import dynamic from "next/dynamic";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

const getLanguageFromPath = (path: string) => {
  if (path.endsWith(".json")) return "json";
  if (path.endsWith(".ts") || path.endsWith(".tsx")) return "typescript";
  if (path.endsWith(".js") || path.endsWith(".jsx")) return "javascript";
  if (path.endsWith(".py")) return "python";
  if (path.endsWith(".md")) return "markdown";
  if (path.endsWith(".css")) return "css";
  if (path.endsWith(".html")) return "html";
  return "plaintext";
};

const FileTree = React.memo(({ items, onSelect, selectedPath, level = 0 }: any) => {
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});

  const toggleDir = useCallback((path: string) => {
    setExpanded(prev => ({ ...prev, [path]: !prev[path] }));
  }, []);

  return (
    <div className="w-full">
      {items.map((item: any) => (
        <div key={item.path}>
          <div 
            className={`flex items-center gap-1.5 px-2 py-1.5 cursor-pointer text-sm font-mono ${
              selectedPath === item.path 
                ? "bg-blue-600/20 text-blue-400" 
                : "text-slate-300 hover:bg-slate-800"
            }`}
            style={{ paddingLeft: `${level * 12 + 8}px` }}
            onClick={() => item.is_dir ? toggleDir(item.path) : onSelect(item.path)}
          >
            {item.is_dir ? (
              <>
                {expanded[item.path] ? <ChevronDown className="w-4 h-4 text-slate-500" /> : <ChevronRight className="w-4 h-4 text-slate-500" />}
                <Folder className="w-4 h-4 text-blue-400 fill-blue-400/20" />
              </>
            ) : (
              <>
                <div className="w-4" /> {/* spacing to align with folders */}
                <File className="w-4 h-4 text-slate-400" />
              </>
            )}
            <span className="truncate">{item.name}</span>
          </div>
          {item.is_dir && expanded[item.path] && item.children && (
            <FileTree 
              items={item.children} 
              onSelect={onSelect} 
              selectedPath={selectedPath} 
              level={level + 1} 
            />
          )}
        </div>
      ))}
    </div>
  );
});
FileTree.displayName = "FileTree";

const FileViewer = React.memo(({ projectId, path }: { projectId: string, path: string }) => {
  const { data, isLoading, error } = useProjectFile(projectId, path);

  if (isLoading) {
    return <div className="flex items-center justify-center h-full text-slate-500"><Loader2 className="w-6 h-6 animate-spin" /></div>;
  }

  if (error || !data) {
    const isBinary = (error as any)?.status === 415;
    const isTooLarge = (error as any)?.status === 403 && (error as any)?.message?.includes("too large");
    return <div className="flex items-center justify-center h-full text-slate-400 font-mono text-sm">
      {isBinary ? "Cannot preview binary file (Unsupported Media Type)" : 
       isTooLarge ? "File too large for preview" : 
       "Failed to load file content"}
    </div>;
  }

  return (
    <div className="h-full w-full">
      <MonacoEditor
        height="100%"
        language={getLanguageFromPath(path)}
        theme="vs-dark"
        value={data.content}
        options={{
          readOnly: true,
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          padding: { top: 16 },
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 13,
        }}
      />
    </div>
  );
});
FileViewer.displayName = "FileViewer";

export default function WorkspaceExplorer({ projectId }: { projectId: string }) {
  const { data: tree, isLoading, error } = useProjectWorkspace(projectId);
  const [selectedPath, setSelectedPath] = useState<string | null>(null);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96 text-slate-500">
        <Loader2 className="w-8 h-8 animate-spin mb-4 text-blue-500" />
        <p>Loading file tree...</p>
      </div>
    );
  }

  if (error || !tree) {
    return <div className="text-red-400 p-8 text-center bg-slate-900 rounded-lg">Error loading workspace</div>;
  }

  return (
    <div className="flex h-[600px] bg-slate-950 border border-slate-800 rounded-xl overflow-hidden shadow-inner">
      {/* File Tree Sidebar */}
      <div className="w-64 border-r border-slate-800 bg-slate-900 overflow-y-auto custom-scrollbar flex-shrink-0 pt-2 pb-4">
        <FileTree items={tree} onSelect={setSelectedPath} selectedPath={selectedPath} />
      </div>

      {/* Code Editor Preview */}
      <div className="flex-1 relative bg-[#1e1e1e]">
        {selectedPath ? (
          <>
            <div className="absolute top-0 left-0 right-0 h-10 border-b border-slate-800 bg-slate-900/80 flex items-center px-4 z-10">
              <span className="text-xs font-mono text-slate-400">{selectedPath}</span>
            </div>
            <div className="pt-10 h-full">
              <FileViewer projectId={projectId} path={selectedPath} />
            </div>
          </>
        ) : (
          <div className="flex items-center justify-center h-full text-slate-600 font-mono text-sm">
            Select a file to preview
          </div>
        )}
      </div>
    </div>
  );
}
