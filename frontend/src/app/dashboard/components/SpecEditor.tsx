"use client";

import { useState, useRef, useEffect } from "react";
import { ProjectSpecification } from "../types/genesis";
import { Play, CheckSquare, Loader2, AlertCircle } from "lucide-react";
import dynamic from "next/dynamic";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), {
  ssr: false,
  loading: () => (
    <div className="absolute inset-0 w-full h-full p-6 bg-slate-950 flex flex-col gap-4 animate-pulse">
      <div className="h-4 bg-slate-800 rounded w-1/3"></div>
      <div className="h-4 bg-slate-800 rounded w-1/2"></div>
      <div className="h-4 bg-slate-800 rounded w-1/4"></div>
      <div className="h-4 bg-slate-800 rounded w-2/5"></div>
      <div className="h-4 bg-slate-800 rounded w-1/3"></div>
      <div className="absolute inset-0 flex items-center justify-center text-slate-600 font-mono text-sm">
        Loading Monaco Editor...
      </div>
    </div>
  )
});

interface SpecEditorProps {
  onRun: (spec: ProjectSpecification) => Promise<void>;
  onValidate?: (spec: ProjectSpecification) => Promise<void>;
  loading: boolean;
}

const DEFAULT_SPEC: ProjectSpecification = {
  project_id: "demo_project_001",
  name: "Demo Project",
  description: "A demonstration of the Genesis Engine Control Plane.",
  pages: ["Dashboard", "Settings"],
  components: ["Navbar", "DataTable"]
};

export default function SpecEditor({ onRun, onValidate, loading }: SpecEditorProps) {
  const [jsonText, setJsonText] = useState(JSON.stringify(DEFAULT_SPEC, null, 2));
  const [error, setError] = useState<string | null>(null);
  const editorRef = useRef<any>(null);

  const handleEditorDidMount = (editor: any, monaco: any) => {
    editorRef.current = editor;

    // JSON Schema validation
    monaco.languages.json.jsonDefaults.setDiagnosticsOptions({
      validate: true,
      schemas: [{
        uri: "http://myserver/project-schema.json",
        fileMatch: ["*"],
        schema: {
          type: "object",
          properties: {
            project_id: { type: "string" },
            name: { type: "string" },
            description: { type: "string" },
            pages: { type: "array", items: { type: "string" } },
            components: { type: "array", items: { type: "string" } }
          },
          required: ["project_id"]
        }
      }]
    });

    // Add Ctrl+S for Validate
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => {
      handleValidate();
    });

    // Add Ctrl+Enter for Run Compiler
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => {
      handleRun();
    });
    
    // Auto format on load
    setTimeout(() => {
      editor.getAction('editor.action.formatDocument')?.run();
    }, 500);
  };

  const parseSpec = (): ProjectSpecification | null => {
    try {
      const spec = JSON.parse(jsonText);
      setError(null);
      return spec;
    } catch (e: any) {
      setError(`Invalid JSON Syntax: ${e.message}`);
      return null;
    }
  };

  const handleRun = async () => {
    if (loading) return;
    const spec = parseSpec();
    if (spec) await onRun(spec);
  };

  const handleValidate = async () => {
    if (loading) return;
    const spec = parseSpec();
    if (spec && onValidate) await onValidate(spec);
  };

  const handleFormat = () => {
    if (editorRef.current) {
      editorRef.current.getAction('editor.action.formatDocument').run();
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-950 rounded-lg border border-slate-800 overflow-hidden relative group">
      
      {/* Editor Header / Toolbar */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-slate-800 bg-slate-900/80">
        <div className="flex items-center gap-2">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-red-500/20 border border-red-500/50"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500/20 border border-yellow-500/50"></div>
            <div className="w-3 h-3 rounded-full bg-emerald-500/20 border border-emerald-500/50"></div>
          </div>
          <span className="text-xs font-mono text-slate-500 ml-2">ProjectSpecification.json</span>
        </div>
        
        <div className="flex items-center gap-2">
          <button 
            onClick={handleFormat} 
            disabled={loading}
            className="px-3 py-1.5 text-xs font-medium text-slate-400 hover:text-white transition-colors disabled:opacity-50"
          >
            Format
          </button>
          {onValidate && (
            <button 
              onClick={handleValidate} 
              disabled={loading}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded transition-colors disabled:opacity-50 border border-slate-700 focus:outline-none focus:ring-2 focus:ring-slate-500"
            >
              <CheckSquare className="w-3.5 h-3.5" /> Validate <span className="hidden xl:inline opacity-50 ml-1">(Ctrl+S)</span>
            </button>
          )}
          <button 
            onClick={handleRun} 
            disabled={loading}
            className="flex items-center gap-1.5 px-4 py-1.5 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-500 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm shadow-blue-900/50 focus:outline-none focus:ring-2 focus:ring-blue-400"
          >
            {loading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Play className="w-3.5 h-3.5 fill-current" />}
            Run Compiler <span className="hidden xl:inline opacity-50 ml-1">(Ctrl+Enter)</span>
          </button>
        </div>
      </div>

      {/* Editor Body */}
      <div className="flex-1 relative bg-slate-950">
        <MonacoEditor
          height="100%"
          language="json"
          theme="vs-dark"
          value={jsonText}
          onChange={(val) => {
            setJsonText(val || "");
            if (error) setError(null);
          }}
          onMount={handleEditorDidMount}
          options={{
            minimap: { enabled: false },
            wordWrap: "on",
            readOnly: loading,
            formatOnPaste: true,
            tabSize: 2,
            fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
            fontSize: 13,
            padding: { top: 16 },
            scrollBeyondLastLine: false,
            smoothScrolling: true,
          }}
        />
        
        {error && (
          <div className="absolute bottom-4 left-4 right-4 bg-red-950/90 backdrop-blur border border-red-500/50 text-red-200 px-4 py-3 rounded-lg shadow-lg flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
            <div className="text-sm font-mono break-all">{error}</div>
          </div>
        )}
      </div>
    </div>
  );
}
