import React from "react";
import { Outlet, Link } from "react-router-dom";
import { Sparkles, ArrowLeft } from "lucide-react";
import { Badge } from "@/components/ui/Badge";

export const AuthLayout: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-obsidian-900 text-slate-900 dark:text-slate-100 flex flex-col justify-center items-center p-4 relative overflow-hidden font-sans">
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-primary-600/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-ai-violet/10 rounded-full blur-3xl pointer-events-none" />

      <div className="absolute top-6 left-6">
        <Link
          to="/"
          className="inline-flex items-center space-x-2 text-xs font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors p-2 rounded-lg hover:bg-slate-200/60 dark:hover:bg-white/5"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Home</span>
        </Link>
      </div>

      <div className="w-full max-w-md z-10 flex flex-col items-center">
        <Link to="/" className="flex items-center space-x-3 mb-8">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-primary-600 to-indigo-400 flex items-center justify-center shadow-lg shadow-indigo-500/25">
            <Sparkles className="w-6 h-6 text-white animate-pulse" />
          </div>
          <div className="flex flex-col">
            <span className="text-xl font-bold tracking-tight text-slate-900 dark:text-white leading-none">Mentra X</span>
            <span className="text-xs font-medium text-indigo-600 dark:text-indigo-400 tracking-wider uppercase mt-0.5">Enterprise Portal</span>
          </div>
        </Link>

        <div className="w-full mb-6 flex justify-center">
          <Badge variant="cyan" size="md">
            🛡️ AI Safety Verified Protected Session
          </Badge>
        </div>

        <div className="w-full">
          <Outlet />
        </div>

        <p className="text-xs text-slate-500 mt-8 text-center">
          &copy; {new Date().getFullYear()} Mentra AI Student Platform. Enterprise Grade.
        </p>
      </div>
    </div>
  );
};
