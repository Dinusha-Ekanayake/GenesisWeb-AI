"use client";

import { useState } from "react";
import { ProjectSpecification } from "../types/genesis";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";

interface SpecEditorProps {
  onRun: (spec: ProjectSpecification) => Promise<void>;
  loading: boolean;
}

const DEFAULT_SPEC: ProjectSpecification = {
  project_id: "demo_project_001",
  name: "Demo Project",
  description: "A demonstration of the Genesis Engine Control Plane.",
  pages: ["Dashboard", "Settings"],
  components: ["Navbar", "DataTable"]
};

export default function SpecEditor({ onRun, loading }: SpecEditorProps) {
  const [jsonText, setJsonText] = useState(JSON.stringify(DEFAULT_SPEC, null, 2));
  const [error, setError] = useState<string | null>(null);

  const handleRun = async () => {
    setError(null);
    try {
      const spec = JSON.parse(jsonText);
      await onRun(spec);
    } catch (e: any) {
      setError(`Invalid JSON: ${e.message}`);
    }
  };

  return (
    <div className="bg-slate-900 rounded-lg border border-slate-700 overflow-hidden flex flex-col h-full shadow-md">
      <div className="bg-slate-800 px-4 py-2 border-b border-slate-700 flex justify-between items-center">
        <span className="text-sm font-medium text-slate-300 font-mono">ProjectSpecification.json</span>
        <Button onClick={handleRun} disabled={loading} size="sm" className="bg-blue-600 hover:bg-blue-700 text-white font-semibold">
          {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
          Run Genesis Compiler
        </Button>
      </div>
      <div className="flex-1 p-4 relative">
        <textarea
          value={jsonText}
          onChange={(e) => setJsonText(e.target.value)}
          className="w-full h-full min-h-[300px] bg-slate-950 text-emerald-400 p-4 font-mono text-sm rounded focus:outline-none focus:ring-1 focus:ring-blue-500 resize-none"
          spellCheck={false}
        />
        {error && (
          <div className="absolute bottom-4 left-4 right-4 bg-red-900/90 border border-red-500 text-red-200 px-4 py-2 rounded text-sm">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}
