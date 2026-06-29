import * as React from "react"
import { cn } from "@/lib/utils"

function Skeleton({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "rounded-sm bg-[linear-gradient(90deg,var(--surface-raised)_0%,var(--surface-overlay)_50%,var(--surface-raised)_100%)] bg-[length:200%_100%] animate-[skeleton-shimmer_1.6s_var(--ease-in-out)_infinite]",
        className
      )}
      aria-hidden="true"
      {...props}
    />
  )
}

function SkeletonText({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <Skeleton className={cn("h-4 w-full", className)} {...props} />
}

export { Skeleton, SkeletonText }
