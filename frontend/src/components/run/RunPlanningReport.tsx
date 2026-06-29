"use client";

import Link from "next/link";
import { CheckCircle2, Info, XCircle } from "lucide-react";
import type { PlanningReport, RuleExecutionTrace } from "@/app/dashboard/types/genesis";
import type { RunViewModel } from "@/lib/genesis/view-models";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { LimitedState } from "@/components/routes/RouteScaffold";

// ── Local helpers ─────────────────────────────────────────────────────────────

function formatPlanningMs(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  return `${(ms / 1000).toFixed(2)}s`;
}

function RuleStatusBadge({ status }: { status: RuleExecutionTrace["status"] }) {
  if (status === "PASS") return <Badge variant="success">PASS</Badge>;
  if (status === "FAIL")
    return (
      <Badge variant="outline" className="border-[color:var(--error)] text-[color:var(--error)]">
        FAIL
      </Badge>
    );
  return (
    <Badge variant="outline" className="text-[color:var(--warning)]">
      WARN
    </Badge>
  );
}

// ── Sub-sections ──────────────────────────────────────────────────────────────

function StatusHeader({ report }: { report: PlanningReport }) {
  const isSuccess = report.rule_validation_status === "SUCCESS";
  return (
    <div className="flex flex-col gap-3 rounded-lg border border-border bg-surface-raised p-4 sm:flex-row sm:items-start sm:justify-between">
      <div className="flex items-center gap-3">
        {isSuccess ? (
          <CheckCircle2 className="h-5 w-5 shrink-0 text-success" aria-hidden="true" />
        ) : (
          <XCircle className="h-5 w-5 shrink-0 text-[color:var(--error)]" aria-hidden="true" />
        )}
        <div>
          <p className="font-semibold text-foreground">
            Rule Engine:{" "}
            <span className={isSuccess ? "text-success" : "text-[color:var(--error)]"}>
              {report.rule_validation_status}
            </span>
          </p>
          <p className="text-sm text-[color:var(--text-secondary)]">
            Integrity score:{" "}
            <code className="font-mono">{report.graph_integrity_score}</code> / 100
          </p>
        </div>
      </div>
      <div className="text-sm text-[color:var(--text-secondary)] sm:text-right">
        <p>
          Duration:{" "}
          <code className="font-mono text-xs">{formatPlanningMs(report.planning_duration_ms)}</code>
        </p>
        {(report.total_errors > 0 || report.total_warnings > 0) && (
          <p className="mt-1 flex flex-wrap gap-2 sm:justify-end">
            {report.total_errors > 0 && (
              <span className="text-[color:var(--error)]">
                {report.total_errors} error{report.total_errors !== 1 ? "s" : ""}
              </span>
            )}
            {report.total_warnings > 0 && (
              <span className="text-[color:var(--warning)]">
                {report.total_warnings} warning{report.total_warnings !== 1 ? "s" : ""}
              </span>
            )}
          </p>
        )}
      </div>
    </div>
  );
}

function MetricsGrid({ report }: { report: PlanningReport }) {
  const metrics = [
    { label: "Features", value: report.total_features },
    { label: "Pages", value: report.total_pages },
    { label: "APIs", value: report.total_apis },
    { label: "Entities", value: report.total_entities },
    { label: "Components", value: report.total_components },
    { label: "Dependencies", value: report.dependency_count },
    { label: "Errors", value: report.total_errors, isError: report.total_errors > 0 },
    { label: "Warnings", value: report.total_warnings, isWarn: report.total_warnings > 0 },
  ] as const;

  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
      {metrics.map((m) => (
        <div
          key={m.label}
          className="flex flex-col items-center justify-center rounded-md border border-border bg-surface-raised p-4 text-center"
        >
          <span
            className={`font-mono text-2xl font-bold tabular-nums ${
              "isError" in m && m.isError
                ? "text-[color:var(--error)]"
                : "isWarn" in m && m.isWarn
                ? "text-[color:var(--warning)]"
                : "text-foreground"
            }`}
          >
            {m.value}
          </span>
          <span className="mt-1 text-xs font-semibold uppercase tracking-wider text-[color:var(--text-tertiary)]">
            {m.label}
          </span>
        </div>
      ))}
    </div>
  );
}

function CoverageCard({ report }: { report: PlanningReport }) {
  if (!report.rule_coverage) return null;
  const cov = report.rule_coverage;
  const items = [
    { label: "API Coverage", value: cov.api_coverage },
    { label: "DB Coverage", value: cov.db_coverage },
    { label: "UI Coverage", value: cov.ui_coverage },
    { label: "Overall Score", value: cov.overall_score },
  ] as const;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Rule Coverage</CardTitle>
        <CardDescription>Coverage scores from the rule validation engine.</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          {items.map((item) => (
            <div
              key={item.label}
              className="flex flex-col items-center rounded-md border border-border bg-surface-base p-3 text-center"
            >
              <span className="font-mono text-xl font-bold text-foreground">{item.value}</span>
              <span className="mt-1 text-xs text-[color:var(--text-tertiary)]">{item.label}</span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

function FailedRulesSection({ rules }: { rules: string[] }) {
  if (rules.length === 0) return null;
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base text-[color:var(--error)]">
          <XCircle className="h-4 w-4" aria-hidden="true" />
          Failed Rules
        </CardTitle>
        <CardDescription>
          {rules.length} rule{rules.length !== 1 ? "s" : ""} failed validation.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ul className="space-y-2">
          {rules.map((rule, idx) => (
            <li
              key={idx}
              className="rounded-md border border-[color:var(--error)] bg-surface-raised px-3 py-2 font-mono text-xs text-[color:var(--error)]"
            >
              {rule}
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}

function AssumptionsSection({ assumptions }: { assumptions: string[] }) {
  if (assumptions.length === 0) return null;
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <Info className="h-4 w-4 text-[color:var(--text-tertiary)]" aria-hidden="true" />
          Planning Assumptions
        </CardTitle>
        <CardDescription>
          {assumptions.length} assumption{assumptions.length !== 1 ? "s" : ""} made during
          planning.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ul className="space-y-2">
          {assumptions.map((assumption, idx) => (
            <li
              key={idx}
              className="rounded-md border border-border bg-surface-raised px-3 py-2 text-sm text-[color:var(--text-secondary)]"
            >
              {assumption}
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}

function RuleTraceSection({ trace }: { trace: RuleExecutionTrace[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Rule Execution Trace</CardTitle>
        <CardDescription>
          {trace.length} rule{trace.length !== 1 ? "s" : ""} evaluated during the planning phase.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        {trace.length === 0 ? (
          <p className="text-sm text-[color:var(--text-secondary)]">No rule trace entries.</p>
        ) : (
          trace.map((entry, idx) => (
            <div key={idx} className="rounded-md border border-border bg-surface-raised p-3">
              <div className="flex flex-wrap items-start justify-between gap-2">
                <div className="min-w-0">
                  <p className="text-sm font-medium text-foreground">{entry.rule_name}</p>
                  <code className="text-xs text-[color:var(--text-tertiary)]">{entry.rule_id}</code>
                </div>
                <RuleStatusBadge status={entry.status} />
              </div>
              <p className="mt-2 text-sm text-[color:var(--text-secondary)]">{entry.message}</p>
              {entry.context != null &&
                typeof entry.context === "object" &&
                Object.keys(entry.context).length > 0 && (
                  <pre className="mt-2 overflow-x-auto rounded-md border border-border bg-surface-base p-2 font-mono text-xs text-[color:var(--text-secondary)]">
                    {JSON.stringify(entry.context, null, 2)}
                  </pre>
                )}
            </div>
          ))
        )}
      </CardContent>
    </Card>
  );
}

function GraphHashesSection({ report }: { report: PlanningReport }) {
  const entries = Object.entries(report.graph_hashes);
  if (entries.length === 0 && !report.workspace_hash) return null;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Graph Hashes</CardTitle>
        <CardDescription>Integrity hashes produced by the compiler pipeline.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-3 text-sm">
        {report.workspace_hash && (
          <div className="flex flex-col gap-0.5">
            <span className="text-xs font-semibold uppercase tracking-wider text-[color:var(--text-tertiary)]">
              Workspace Hash
            </span>
            <code className="break-all font-mono text-xs text-[color:var(--text-secondary)]">
              {report.workspace_hash}
            </code>
          </div>
        )}
        {entries.map(([key, hash]) => (
          <div key={key} className="flex flex-col gap-0.5">
            <span className="text-xs font-semibold uppercase tracking-wider text-[color:var(--text-tertiary)]">
              {key}
            </span>
            <code className="break-all font-mono text-xs text-[color:var(--text-secondary)]">
              {hash}
            </code>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

// ── Main export ───────────────────────────────────────────────────────────────

export function RunPlanningReport({ run }: { run: RunViewModel }) {
  if (!run.planningReport) {
    return (
      <LimitedState
        title="Planning report not available"
        description="The backend project record does not include a planning report. Compile a specification to generate one."
        action={
          <Link
            href="/compiler"
            className="inline-flex rounded-sm bg-accent px-3 py-2 text-sm font-medium text-accent-foreground hover:bg-accent-hover"
          >
            Open Compiler
          </Link>
        }
      />
    );
  }

  const { planningReport: report } = run;

  return (
    <div className="space-y-4">
      <StatusHeader report={report} />
      <MetricsGrid report={report} />
      <CoverageCard report={report} />
      <FailedRulesSection rules={report.failed_rules} />
      <AssumptionsSection assumptions={report.assumptions} />
      <RuleTraceSection trace={report.rule_trace} />
      <GraphHashesSection report={report} />
    </div>
  );
}
