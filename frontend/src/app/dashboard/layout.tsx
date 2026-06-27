import Link from "next/link";
import { LayoutDashboard, FolderKanban, Settings } from "lucide-react";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col md:flex-row bg-slate-50 dark:bg-slate-950">
      {/* Sidebar */}
      <aside className="w-full md:w-64 border-r border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 flex-shrink-0">
        <div className="p-6">
          <h2 className="text-2xl font-bold text-primary">GenesisWeb</h2>
        </div>
        <nav className="flex flex-col gap-2 px-4">
          <Link href="/dashboard" className="flex items-center gap-3 rounded-lg px-3 py-2 text-slate-900 dark:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
            <LayoutDashboard size={20} />
            Dashboard
          </Link>
          <Link href="/dashboard/projects" className="flex items-center gap-3 rounded-lg px-3 py-2 text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
            <FolderKanban size={20} />
            Projects
          </Link>
          <Link href="/dashboard/settings" className="flex items-center gap-3 rounded-lg px-3 py-2 text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
            <Settings size={20} />
            Settings
          </Link>
        </nav>
      </aside>
      
      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        {children}
      </main>
    </div>
  );
}
