import * as React from "react"
import { cn } from "@/lib/utils"

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "secondary" | "success" | "warning" | "error" | "outline"
}

const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(
  ({ className, variant = "default", ...props }, ref) => (
    <span
      ref={ref}
      className={cn(
        "inline-flex items-center gap-1.5 rounded-xs border px-2 py-0.5 text-xs font-semibold leading-none",
        {
          "border-border-accent bg-accent-subtle text-accent": variant === "default",
          "border-border bg-surface-raised text-[color:var(--text-secondary)]": variant === "secondary",
          "border-border-success bg-success-subtle text-success": variant === "success",
          "border-border-warning bg-warning-subtle text-warning": variant === "warning",
          "border-border-error bg-error-subtle text-error": variant === "error",
          "border-border bg-transparent text-[color:var(--text-secondary)]": variant === "outline",
        },
        className
      )}
      {...props}
    />
  )
)
Badge.displayName = "Badge"

export { Badge }
