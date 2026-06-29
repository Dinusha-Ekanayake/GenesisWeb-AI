import { AlertTriangle, CheckCircle2, Clock, Loader2, Package, Shield, Zap } from "lucide-react"
import { cn } from "@/lib/utils"

type Status =
  | "NO_RUNS"
  | "QUEUED"
  | "PENDING"
  | "PLANNING"
  | "VALIDATING"
  | "VALIDATION"
  | "GENERATING"
  | "GENERATION"
  | "PACKAGING"
  | "RUNNING"
  | "SUCCESS"
  | "FAILED"
  | string

interface StatusBadgeProps {
  status: Status
  className?: string
  pulse?: boolean
}

const STATUS_CONFIG: Record<string, { label: string; className: string; icon: typeof Clock; active?: boolean }> = {
  NO_RUNS: { label: "No Runs", className: "border-border bg-surface-raised text-[color:var(--text-tertiary)]", icon: Clock },
  QUEUED: { label: "Queued", className: "border-border-warning bg-warning-subtle text-warning", icon: Clock },
  PENDING: { label: "Pending", className: "border-border-warning bg-warning-subtle text-warning", icon: Clock },
  PLANNING: { label: "Planning", className: "border-border-accent bg-accent-subtle text-accent", icon: Zap, active: true },
  VALIDATING: { label: "Validating", className: "border-border-accent bg-accent-subtle text-accent", icon: Shield, active: true },
  VALIDATION: { label: "Validating", className: "border-border-accent bg-accent-subtle text-accent", icon: Shield, active: true },
  GENERATING: { label: "Generating", className: "border-border-accent bg-accent-subtle text-accent", icon: Loader2, active: true },
  GENERATION: { label: "Generating", className: "border-border-accent bg-accent-subtle text-accent", icon: Loader2, active: true },
  PACKAGING: { label: "Packaging", className: "border-border-accent bg-accent-subtle text-accent", icon: Package, active: true },
  RUNNING: { label: "Running", className: "border-border-accent bg-accent-subtle text-accent", icon: Loader2, active: true },
  SUCCESS: { label: "Success", className: "border-border-success bg-success-subtle text-success", icon: CheckCircle2 },
  FAILED: { label: "Failed", className: "border-border-error bg-error-subtle text-error", icon: AlertTriangle },
}

export function StatusBadge({ status, className, pulse = true }: StatusBadgeProps) {
  const normalized = String(status || "PENDING").toUpperCase()
  const config = STATUS_CONFIG[normalized] || {
    label: normalized.replace(/_/g, " ").toLowerCase().replace(/\b\w/g, (c) => c.toUpperCase()),
    className: "border-border bg-surface-raised text-[color:var(--text-secondary)]",
    icon: Clock,
  }
  const Icon = config.icon
  const isActive = pulse && config.active

  return (
    <span
      aria-label={`Status: ${config.label}`}
      className={cn(
        "inline-flex items-center gap-1.5 rounded-xs border px-2.5 py-1 text-xs font-bold uppercase tracking-wider",
        config.className,
        className
      )}
    >
      <span className="relative inline-flex h-3.5 w-3.5 items-center justify-center">
        {isActive ? <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-current opacity-30" /> : null}
        <Icon className={cn("h-3.5 w-3.5", config.icon === Loader2 && "animate-spin")} aria-hidden="true" />
      </span>
      {config.label}
    </span>
  )
}
