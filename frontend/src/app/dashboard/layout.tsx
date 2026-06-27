import React from "react";
import Link from "next/link";
import { 
  Box, 
  LayoutDashboard, 
  FolderOpen, 
  FileTerminal, 
  Settings, 
  Activity, 
  Database 
} from "lucide-react";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 font-sans overflow-hidden">
      
      {/* Sidebar */}
      <aside className="w-64 border-r border-slate-800 bg-slate-950 flex flex-col hidden md:flex">
        <div className="h-16 flex items-center px-6 border-b border-slate-800">
          <Box className="w-6 h-6 text-blue-500 mr-3" />
          <span className="font-bold text-lg tracking-tight">Genesis Engine</span>
        </div>
        
        <nav className="flex-1 px-4 py-6 space-y-2">
          <Link href="/dashboard" className="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md bg-blue-500/10 text-blue-400">
            <LayoutDashboard className="w-4 h-4" /> Dashboard
          </Link>
          <Link href="/dashboard" className="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md text-slate-400 hover:text-slate-100 hover:bg-slate-900 transition-colors">
            <FolderOpen className="w-4 h-4" /> Projects
          </Link>
          <Link href="/dashboard" className="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md text-slate-400 hover:text-slate-100 hover:bg-slate-900 transition-colors">
            <FileTerminal className="w-4 h-4" /> Execution Logs
          </Link>
          <Link href="/dashboard" className="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md text-slate-400 hover:text-slate-100 hover:bg-slate-900 transition-colors">
            <Database className="w-4 h-4" /> Deployment
          </Link>
        </nav>

        <div className="p-4 border-t border-slate-800">
          <Link href="/dashboard" className="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-md text-slate-400 hover:text-slate-100 hover:bg-slate-900 transition-colors">
            <Settings className="w-4 h-4" /> Settings
          </Link>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-screen overflow-hidden bg-slate-950">
        
        {/* Top Header */}
        <header className="h-16 border-b border-slate-800 bg-slate-950/50 backdrop-blur-md flex items-center justify-between px-8 z-10 sticky top-0">
          <div className="flex items-center gap-4 text-sm">
            <span className="text-slate-400 font-medium">Workspace:</span>
            <span className="text-slate-200">Default Organization</span>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-3 py-1.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-full text-xs font-semibold uppercase tracking-wide">
              <Activity className="w-3 h-3 animate-pulse" /> API Connected
            </div>
            <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center">
              <span className="text-xs font-bold text-slate-300">U</span>
            </div>
          </div>
        </header>
        
        {/* Scrollable Content */}
        <main className="flex-1 overflow-y-auto p-8 relative">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>

    </div>
  );
}
