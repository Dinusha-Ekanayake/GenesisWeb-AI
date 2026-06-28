"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import { Toaster } from "sonner";
import { ErrorBoundary } from "react-error-boundary";
import { useState, ReactNode } from "react";

function ErrorFallback({ error, resetErrorBoundary }: any) {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-slate-950 text-slate-100 p-8">
      <div className="bg-red-950/30 border border-red-900/50 rounded-xl p-8 max-w-2xl w-full">
        <h2 className="text-2xl font-bold text-red-500 mb-4">Something went wrong</h2>
        <pre className="text-sm text-red-300 font-mono bg-red-950/50 p-4 rounded-lg overflow-x-auto mb-6">
          {error.message}
        </pre>
        <button
          onClick={resetErrorBoundary}
          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md font-medium transition-colors"
        >
          Try again
        </button>
      </div>
    </div>
  );
}

export function Providers({ children }: { children: ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 5000,
        refetchOnWindowFocus: false,
        retry: 2,
      },
    },
  }));

  return (
    <ErrorBoundary FallbackComponent={ErrorFallback}>
      <QueryClientProvider client={queryClient}>
        <NextThemesProvider attribute="class" defaultTheme="system" enableSystem>
          {children}
          <Toaster theme="system" richColors position="bottom-right" />
        </NextThemesProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}
