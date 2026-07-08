import React from "react";
import { Outlet, Link } from "react-router-dom";
import { GraduationCap, ArrowLeft } from "lucide-react";
import { motion } from "framer-motion";

export const AuthLayout: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-indigo-50/40 to-slate-100 dark:from-obsidian-950 dark:via-indigo-950/20 dark:to-obsidian-900 text-slate-900 dark:text-slate-100 flex flex-col justify-center items-center p-4 relative overflow-hidden font-sans">
      {/* Decorative blobs */}
      <div className="absolute -top-56 -left-56 w-[28rem] h-[28rem] bg-indigo-500/10 dark:bg-indigo-500/8 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-56 -right-56 w-[28rem] h-[28rem] bg-violet-500/10 dark:bg-violet-500/8 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[32rem] h-[32rem] bg-cyan-400/5 rounded-full blur-3xl pointer-events-none" />

      {/* Back to Home */}
      <div className="absolute top-6 left-6 z-10">
        <Link
          to="/"
          className="inline-flex items-center gap-2 text-xs font-medium text-slate-500 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors p-2 rounded-lg hover:bg-white/60 dark:hover:bg-white/5"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Home</span>
        </Link>
      </div>

      <div className="w-full max-w-md z-10 flex flex-col items-center">
        {/* Brand mark */}
        <motion.div
          initial={{ opacity: 0, y: -16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: "easeOut" }}
        >
          <Link to="/" className="flex items-center gap-3 mb-8 group">
            <div className="w-11 h-11 rounded-2xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/30 group-hover:shadow-indigo-500/50 transition-shadow">
              <GraduationCap className="w-6 h-6 text-white" />
            </div>
            <div className="flex flex-col">
              <span className="text-xl font-extrabold tracking-tight text-slate-900 dark:text-white leading-none">
                Mentra X
              </span>
              <span className="text-[11px] font-semibold text-indigo-600 dark:text-indigo-400 tracking-widest uppercase mt-0.5">
                AI Learning Platform
              </span>
            </div>
          </Link>
        </motion.div>

        {/* Card outlet */}
        <motion.div
          className="w-full"
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1, ease: "easeOut" }}
        >
          <Outlet />
        </motion.div>

        <motion.p
          className="text-xs text-slate-400 dark:text-slate-500 mt-8 text-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.4 }}
        >
          &copy; {new Date().getFullYear()} Mentra AI Student Platform. All rights reserved.
        </motion.p>
      </div>
    </div>
  );
};
