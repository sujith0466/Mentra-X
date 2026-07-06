import React from "react";
import { Link, useLocation } from "react-router-dom";
import { Sparkles, Sun, Moon, MessageSquare, Menu, LogOut, ShieldCheck } from "lucide-react";
import { useAuthStore } from "@/store/useAuthStore";
import { useUIStore } from "@/store/useUIStore";
import { Badge } from "@/components/ui/Badge";

export const Navbar: React.FC = () => {
  const { user, logout } = useAuthStore();
  const { theme, toggleTheme, toggleSidebar, toggleChat } = useUIStore();
  const location = useLocation();

  return (
    <header className="sticky top-0 z-40 w-full h-16 enterprise-glass flex items-center justify-between px-6 transition-all">
      <div className="flex items-center space-x-4">
        <button
          onClick={toggleSidebar}
          className="lg:hidden text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white p-1 rounded-lg hover:bg-slate-100 dark:hover:bg-white/5 transition-colors"
        >
          <Menu className="w-5 h-5" />
        </button>
        <Link to="/" className="flex items-center space-x-2.5">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-primary-600 to-indigo-400 flex items-center justify-center shadow-lg shadow-indigo-500/25">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div className="flex flex-col">
            <span className="text-base font-bold tracking-tight text-slate-900 dark:text-white leading-none">
              Mentra X
            </span>
            <span className="text-[10px] font-medium text-indigo-600 dark:text-indigo-400 tracking-wider uppercase mt-0.5">
              Enterprise AI
            </span>
          </div>
        </Link>
        <div className="hidden md:flex items-center space-x-1 pl-6">
          <Badge variant="cyan" size="sm">
            <ShieldCheck className="w-3 h-3 mr-1" /> AI Safety Verification Active
          </Badge>
        </div>
      </div>

      <div className="flex items-center space-x-3">
        <button
          onClick={toggleChat}
          className="relative inline-flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-primary-500/10 border border-primary-500/20 text-indigo-700 dark:text-indigo-300 hover:bg-primary-500/20 hover:text-indigo-900 dark:hover:text-white transition-all text-xs font-medium"
        >
          <MessageSquare className="w-3.5 h-3.5 text-indigo-500 dark:text-indigo-400" />
          <span>Intelligent AI Tutor</span>
          <span className="absolute -top-1 -right-1 w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
        </button>

        <button
          onClick={toggleTheme}
          className="text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-white/5 transition-colors"
          title="Toggle Theme"
        >
          {theme === "dark" ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-700" />}
        </button>

        {user ? (
          <div className="flex items-center space-x-3 pl-3 border-l border-slate-200 dark:border-obsidian-600">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 rounded-full bg-indigo-600/20 dark:bg-indigo-600/30 border border-indigo-500/40 flex items-center justify-center text-xs font-semibold text-indigo-700 dark:text-indigo-200">
                {user.name.split(" ").map((n) => n[0]).join("")}
              </div>
              <div className="hidden sm:flex flex-col text-left">
                <span className="text-xs font-semibold text-slate-800 dark:text-slate-200 leading-none">
                  {user.name}
                </span>
                <span className="text-[10px] text-slate-500 dark:text-slate-400 capitalize mt-0.5">
                  {user.role}
                </span>
              </div>
            </div>
            <button
              onClick={logout}
              className="text-slate-400 hover:text-rose-600 dark:hover:text-rose-400 p-1.5 rounded-lg hover:bg-rose-500/10 transition-colors"
              title="Logout"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <div className="flex items-center space-x-2 pl-3">
            <Link
              to="/login"
              className="px-3 py-1.5 text-xs font-medium text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white transition-colors"
            >
              Log In
            </Link>
            <Link
              to="/register"
              className="px-3 py-1.5 text-xs font-medium rounded-lg bg-primary-600 text-white hover:bg-primary-500 transition-colors shadow-md shadow-indigo-500/20"
            >
              Register
            </Link>
          </div>
        )}
      </div>
    </header>
  );
};
