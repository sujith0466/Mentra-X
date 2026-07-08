import React from "react";
import { motion } from "framer-motion";
import { cn } from "@/utils/cn";

export interface ConfidenceMeterProps {
  score: number; // 0 to 1
  label?: string;
  size?: "sm" | "md" | "lg";
  className?: string;
}

export const ConfidenceMeter: React.FC<ConfidenceMeterProps> = ({
  score,
  label = "Composite Confidence",
  size = "md",
  className,
}) => {
  const percentage = Math.min(Math.max(Math.round(score * 100), 0), 100);

  const getStatusColor = (val: number) => {
    if (val >= 90) return { bg: "bg-emerald-500", text: "text-emerald-400", border: "border-emerald-500/30" };
    if (val >= 70) return { bg: "bg-amber-500", text: "text-amber-400", border: "border-amber-500/30" };
    return { bg: "bg-rose-500", text: "text-rose-400", border: "border-rose-500/30" };
  };

  const status = getStatusColor(percentage);

  return (
    <div className={cn("w-full flex flex-col space-y-1.5", className)}>
      <div className="flex items-center justify-between text-xs font-semibold">
        <span className="text-slate-600 dark:text-slate-300">{label}</span>
        <span className={cn("font-mono", status.text)}>{percentage}%</span>
      </div>
      <div className="w-full h-2 rounded-full bg-slate-50 dark:bg-obsidian-900 border border-slate-200 dark:border-obsidian-600 overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          className={cn("h-full rounded-full transition-all", status.bg)}
        />
      </div>
    </div>
  );
};
