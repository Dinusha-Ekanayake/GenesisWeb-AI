"use client";

import { PlanningReport } from "../types/genesis";
import { CheckCircle2, AlertCircle, XCircle } from "lucide-react";

interface PlanningReportViewerProps {
  report: PlanningReport;
}

export default function PlanningReportViewer({ report }: PlanningReportViewerProps) {
  if (!report) return null;

  const isSuccess = report.rule_validation_status === "SUCCESS";

  return (
    <div className="space-y-6">
      {/* Status Banner */}
      <div className={`p-4 rounded-lg flex items-center justify-between border ${isSuccess ? 'bg-emerald-50 border-emerald-200 text-emerald-900 dark:bg-emerald-950/30 dark:border-emerald-900 dark:text-emerald-300' : 'bg-red-50 border-red-200 text-red-900 dark:bg-red-950/30 dark:border-red-900 dark:text-red-300'}`}>
        <div className="flex items-center gap-3">
          {isSuccess ? <CheckCircle2 className="w-6 h-6" /> : <XCircle className="w-6 h-6" />}
          <div>
            <h3 className="font-semibold text-lg">Rule Engine Validation: {report.rule_validation_status}</h3>
            <p className="text-sm opacity-80">Integrity Score: {report.graph_integrity_score} / 100</p>
          </div>
        </div>
        <div className="text-right text-sm font-medium">
          <p>Duration: {report.planning_duration_ms}ms</p>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: "Total Features", val: report.total_features },
          { label: "Total Pages", val: report.total_pages },
          { label: "Total APIs", val: report.total_apis },
          { label: "Total Entities", val: report.total_entities },
          { label: "Total Components", val: report.total_components },
          { label: "Dependency Count", val: report.dependency_count },
          { label: "Total Errors", val: report.total_errors, isBad: report.total_errors > 0 },
          { label: "Total Warnings", val: report.total_warnings, isBad: report.total_warnings > 0 },
        ].map((m, i) => (
          <div key={i} className={`bg-white dark:bg-slate-900 p-4 rounded-lg border border-slate-200 dark:border-slate-800 flex flex-col justify-center items-center ${m.isBad ? 'text-red-500' : ''}`}>
            <span className="text-3xl font-bold">{m.val}</span>
            <span className="text-xs text-slate-500 uppercase tracking-wide mt-1">{m.label}</span>
          </div>
        ))}
      </div>

      {/* Failed Rules */}
      {report.failed_rules && report.failed_rules.length > 0 && (
        <div className="bg-white dark:bg-slate-900 rounded-lg border border-red-200 dark:border-red-900/50 p-6">
          <h3 className="text-lg font-semibold text-red-600 dark:text-red-400 mb-4 flex items-center gap-2">
            <AlertCircle className="w-5 h-5" /> Failed Compiler Rules
          </h3>
          <ul className="list-disc pl-6 space-y-2">
            {report.failed_rules.map((rule, idx) => (
              <li key={idx} className="text-sm text-slate-700 dark:text-slate-300 font-mono bg-slate-50 dark:bg-slate-950 p-2 rounded border border-slate-100 dark:border-slate-800">
                {rule}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Rule Trace Raw Data */}
      <div className="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950">
          <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200">Execution Trace (JSON)</h3>
        </div>
        <div className="p-6 overflow-auto max-h-[400px]">
          <pre className="text-xs font-mono text-slate-600 dark:text-slate-400">
            {JSON.stringify(report.rule_trace, null, 2)}
          </pre>
        </div>
      </div>
    </div>
  );
}
