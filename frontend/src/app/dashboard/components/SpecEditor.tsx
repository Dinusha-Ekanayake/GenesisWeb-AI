"use client";

import { useState } from "react";
import { ProjectSpecification } from "../types/genesis";
import { Play, CheckSquare, Loader2, AlertCircle } from "lucide-react";

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
    const spec = parseSpec();
    if (spec) await onRun(spec);
  };

  const handleValidate = async () => {
    const spec = parseSpec();
    if (spec && onValidate) await onValidate(spec);
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
          {onValidate && (
            <button 
              onClick={handleValidate} 
              disabled={loading}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded transition-colors disabled:opacity-50 border border-slate-700"
            >
              <CheckSquare className="w-3.5 h-3.5" /> Validate
            </button>
          )}
          <button 
            onClick={handleRun} 
            disabled={loading}
            className="flex items-center gap-1.5 px-4 py-1.5 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-500 rounded transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-sm shadow-blue-900/50"
          >
            {loading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Play className="w-3.5 h-3.5 fill-current" />}
            Run Compiler
          </button>
        </div>
      </div>

      {/* Editor Body */}
      <div className="flex-1 relative">
        <textarea
          value={jsonText}
          onChange={(e) => {
            setJsonText(e.target.value);
            if (error) setError(null);
          }}
          className="absolute inset-0 w-full h-full p-6 bg-slate-950 text-slate-300 font-mono text-sm leading-relaxed focus:outline-none resize-none selection:bg-blue-500/30"
          spellCheck={false}
          style={{ tabSize: 2 }}
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
