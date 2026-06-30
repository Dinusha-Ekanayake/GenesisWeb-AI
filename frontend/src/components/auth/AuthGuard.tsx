"use client";

import { type ReactNode, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/app/dashboard/lib/api-client";

type AuthStatus = "checking" | "authenticated" | "unauthenticated";

export function AuthGuard({ children }: { children: ReactNode }) {
  const [status, setStatus] = useState<AuthStatus>("checking");
  const router = useRouter();

  useEffect(() => {
    if (getToken()) {
      setStatus("authenticated");
    } else {
      setStatus("unauthenticated");
      router.replace("/login");
    }
  }, [router]);

  if (status !== "authenticated") {
    return null;
  }

  return <>{children}</>;
}
