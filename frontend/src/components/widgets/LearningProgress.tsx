import React from "react";
import { motion } from "framer-motion";
import { BookOpen, CheckCircle } from "lucide-react";
import { cn } from "@/utils/cn";

export interface LearningProgressProps {
  courseTitle: string;
  completedModules: number;
  totalModules: number;
  estimatedTimeLeft?: string;
  className?: string;
}

export const LearningProgress: React.FC<LearningProgressProps> = ({
  courseTitle,
  completedModules,
  totalModules,
  estimatedTimeLeft = "2 hrs remaining",
  className,
}) => {
  const percentage = totalModules > 0 ? Math.round((completedModules / totalModules) * 100) : 0;

  return (
    <div className={cn("p-4 rounded-xl bg-white dark:bg-obsidian-800 border border-slate-200 dark:border-obsidian-600 space-y-3", className)}>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <BookOpen className="w-4 h-4 text-primary-500" />
          <span className="text-sm font-bold text-slate-900 dark:text-white truncate max-w-[200px] sm:max-w-xs">{courseTitle}</span>
        </div>
        <span className="text-xs font-mono text-indigo-400 font-bold">{percentage}%</span>
      </div>

      <div className="w-full h-2 rounded-full bg-slate-50 dark:bg-obsidian-900 border border-slate-200 dark:border-obsidian-600 overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.5, ease: "easeOut" }}
          className="h-full rounded-full bg-gradient-to-r from-primary-600 to-ai-violet"
        />
      </div>

      <div className="flex items-center justify-between text-xs text-slate-400 pt-1">
        <span className="flex items-center gap-1">
          <CheckCircle className="w-3.5 h-3.5 text-emerald-400" /> {completedModules} of {totalModules} modules
        </span>
        <span>{estimatedTimeLeft}</span>
      </div>
    </div>
  );
};
