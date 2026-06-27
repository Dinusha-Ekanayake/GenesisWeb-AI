"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Plus, ArrowRight, Loader2 } from "lucide-react";

interface Project {
  id: string;
  title: string;
  status: string;
  created_at: string;
}

export default function DashboardPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [isCreating, setIsCreating] = useState(false);
  const [prompt, setPrompt] = useState("");

  const fetchProjects = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/v1/projects/");
      if (res.ok) {
        const data = await res.json();
        setProjects(data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleCreate = async () => {
    if (!prompt) return;
    setIsCreating(true);
    try {
      const res = await fetch("http://localhost:8000/api/v1/projects/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: "New Generation",
          user_prompt: prompt
        })
      });
      if (res.ok) {
        setPrompt("");
        fetchProjects();
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div className="p-8 max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-slate-500 mt-2">Manage your AI-generated projects.</p>
        </div>
      </div>

      {/* Quick Create Section */}
      <Card className="mb-8 border-primary/20 shadow-sm bg-primary/5">
        <CardHeader>
          <CardTitle>Create New Project</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col md:flex-row gap-4">
            <input 
              type="text" 
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="E.g., I need a modern online bookstore with Stripe..." 
              className="flex-1 rounded-md border border-slate-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary dark:bg-slate-800 dark:border-slate-700"
            />
            <Button onClick={handleCreate} disabled={isCreating || !prompt}>
              {isCreating ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Plus className="mr-2 h-4 w-4" />}
              Generate Website
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Projects Grid */}
      <h2 className="text-xl font-semibold mb-4">Recent Projects</h2>
      {loading ? (
        <div className="flex items-center gap-2 text-slate-500"><Loader2 className="animate-spin h-5 w-5"/> Loading...</div>
      ) : projects.length === 0 ? (
        <p className="text-slate-500">No projects found. Create one above!</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((p) => (
            <Card key={p.id} className="hover:shadow-md transition-shadow">
              <CardHeader className="pb-3">
                <div className="flex justify-between items-start">
                  <CardTitle className="truncate pr-4">{p.title}</CardTitle>
                  <span className="text-xs font-medium px-2 py-1 bg-slate-100 dark:bg-slate-800 rounded-full flex-shrink-0">
                    {p.status}
                  </span>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-slate-500 mb-4 truncate">
                  Created: {new Date(p.created_at).toLocaleDateString()}
                </p>
                <Button variant="outline" className="w-full justify-between">
                  View Workflow <ArrowRight className="h-4 w-4" />
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
