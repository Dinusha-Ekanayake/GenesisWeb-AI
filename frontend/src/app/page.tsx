export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gradient-to-b from-background to-slate-50 dark:to-slate-900">
      <h1 className="text-5xl font-extrabold tracking-tight mb-6">
        Welcome to <span className="text-primary">GenesisWeb AI</span>
      </h1>
      <p className="text-lg text-slate-600 dark:text-slate-300 max-w-2xl text-center mb-10">
        The ultimate Multi-Agent System that builds, designs, and orchestrates full-stack web applications from a simple prompt.
      </p>
      
      <div className="flex gap-4">
        <button className="px-6 py-3 bg-primary text-primary-foreground rounded-lg font-medium shadow-md hover:opacity-90 transition-opacity">
          Create New Project
        </button>
        <button className="px-6 py-3 bg-slate-200 dark:bg-slate-800 text-slate-900 dark:text-slate-100 rounded-lg font-medium shadow-sm hover:opacity-90 transition-opacity">
          View Dashboard
        </button>
      </div>
    </main>
  );
}
