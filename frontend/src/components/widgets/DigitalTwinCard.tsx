import React from "react";
import { BrainCircuit, Activity, Zap, Flame, Award } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { cn } from "@/utils/cn";

export interface DigitalTwinCardProps {
  twinId?: string;
  studentName: string;
  healthScore: number;
  knowledgeMastery: number;
  studyVelocity: number;
  streakDays: number;
  status?: "healthy" | "needs_attention" | "syncing";
  className?: string;
}

export const DigitalTwinCard: React.FC<DigitalTwinCardProps> = ({
  twinId = "twin_alpha_99",
  studentName,
  healthScore,
  knowledgeMastery,
  studyVelocity,
  streakDays,
  status = "healthy",
  className,
}) => {
  const statusColors = {
    healthy: "text-emerald-400 border-emerald-500/30 bg-emerald-500/10",
    needs_attention: "text-amber-400 border-amber-500/30 bg-amber-500/10",
    syncing: "text-cyan-400 border-cyan-500/30 bg-cyan-500/10",
  };

  return (
    <Card variant="glow" className={cn("relative overflow-hidden p-6", className)}>
      <div className="flex items-center justify-between pb-4 border-b border-obsidian-600 mb-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-primary-600 to-ai-violet flex items-center justify-center shadow-lg shadow-indigo-500/30">
            <BrainCircuit className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h4 className="font-bold text-white leading-none">{studentName}&apos;s Digital Twin</h4>
              <Badge variant="purple" size="sm">Active</Badge>
            </div>
            <span className="text-xs font-mono text-indigo-400 mt-1 block">ID: {twinId}</span>
          </div>
        </div>
        <div className={cn("px-2.5 py-1 rounded-full text-xs font-semibold border flex items-center space-x-1", statusColors[status])}>
          <Activity className="w-3.5 h-3.5 animate-pulse" />
          <span className="capitalize">{status.replace("_", " ")}</span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <div className="p-3 rounded-lg bg-obsidian-900 border border-obsidian-600/60 flex flex-col">
          <span className="text-xs text-slate-400 flex items-center gap-1">
            <Activity className="w-3.5 h-3.5 text-indigo-400" /> Health Score
          </span>
          <span className="text-xl font-bold text-white mt-1">{healthScore}/100</span>
        </div>
        <div className="p-3 rounded-lg bg-obsidian-900 border border-obsidian-600/60 flex flex-col">
          <span className="text-xs text-slate-400 flex items-center gap-1">
            <Award className="w-3.5 h-3.5 text-ai-violet" /> Mastery
          </span>
          <span className="text-xl font-bold text-white mt-1">{knowledgeMastery}%</span>
        </div>
        <div className="p-3 rounded-lg bg-obsidian-900 border border-obsidian-600/60 flex flex-col">
          <span className="text-xs text-slate-400 flex items-center gap-1">
            <Zap className="w-3.5 h-3.5 text-amber-400" /> Velocity
          </span>
          <span className="text-xl font-bold text-white mt-1">{studyVelocity}x</span>
        </div>
        <div className="p-3 rounded-lg bg-obsidian-900 border border-obsidian-600/60 flex flex-col">
          <span className="text-xs text-slate-400 flex items-center gap-1">
            <Flame className="w-3.5 h-3.5 text-rose-400" /> Streak
          </span>
          <span className="text-xl font-bold text-white mt-1">{streakDays} Days</span>
        </div>
      </div>
    </Card>
  );
};
