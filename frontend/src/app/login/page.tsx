"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Lock, Loader2 } from "lucide-react";
import { loginWithCredentials } from "@/lib/auth/login";
import { setToken } from "@/app/dashboard/lib/api-client";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const token = await loginWithCredentials(username, password);
      setToken(token);
      router.push("/dashboard");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Login failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-surface-base flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-surface-raised border border-border rounded-xl p-8 shadow-2xl">
        <div className="flex flex-col items-center mb-8">
          <div className="w-12 h-12 bg-accent/20 text-accent rounded-xl flex items-center justify-center mb-4">
            <Lock className="w-6 h-6" />
          </div>
          <h1 className="text-2xl font-bold text-foreground tracking-tight">Genesis Engine</h1>
          <p className="text-sm mt-1 text-[color:var(--text-secondary)]">Control Plane Authentication</p>
        </div>

        {error && (
          <div
            role="alert"
            className="mb-6 p-3 rounded-md text-sm text-center bg-[color:var(--error)]/10 border border-[color:var(--error)]/20 text-[color:var(--error)]"
          >
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-foreground mb-1">
              Username
            </label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-surface-base border border-border rounded-md px-4 py-2.5 text-foreground placeholder:text-[color:var(--text-tertiary)] focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-colors"
              placeholder="e.g. developer"
              required
              autoComplete="username"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-foreground mb-1">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-surface-base border border-border rounded-md px-4 py-2.5 text-foreground placeholder:text-[color:var(--text-tertiary)] focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-colors"
              placeholder="••••••••"
              required
              autoComplete="current-password"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-accent hover:bg-accent/90 text-accent-foreground font-medium py-2.5 rounded-md transition-colors flex items-center justify-center mt-2 disabled:opacity-50"
          >
            {loading ? <Loader2 className="w-5 h-5 animate-spin" aria-hidden="true" /> : "Sign In"}
          </button>
        </form>

        <div className="mt-8 text-center text-xs text-[color:var(--text-tertiary)]">
          Secure Control Plane &bull; v1.0.0
        </div>
      </div>
    </div>
  );
}
