import * as React from "react"
import { cn } from "@/lib/utils"

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  invalid?: boolean
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type = "text", invalid = false, ...props }, ref) => (
    <input
      ref={ref}
      type={type}
      aria-invalid={invalid || props["aria-invalid"]}
      className={cn(
        "flex h-10 w-full rounded-sm border bg-surface-base px-3 py-2 text-sm text-foreground shadow-xs transition-colors duration-default ease-out placeholder:text-[color:var(--text-tertiary)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:cursor-not-allowed disabled:opacity-50",
        invalid ? "border-border-error" : "border-border",
        className
      )}
      {...props}
    />
  )
)
Input.displayName = "Input"

export { Input }
