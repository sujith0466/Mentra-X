import React from "react";
import { Zap, CheckCircle2, AlertTriangle, ArrowRight, Clock, TrendingUp } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";

export interface SkillGapData {
  opportunity_id: string;
  current_skills: string[];
  missing_skills: string[];
  learning_path_steps: string[];
  estimated_readiness_days: number;
  current_match_pct: number;
  expected_match_after_remediation_pct: number;
}

interface SkillGapCardProps {
  data: SkillGapData;
  opportunityTitle: string;
}

export const SkillGapCard: React.FC<SkillGapCardProps> = ({ data, opportunityTitle }) => {
  const isFullyQualified = data.missing_skills.length === 0;

  return (
    <Card className="p-6 bg-gradient-to-br from-indigo-500/5 via-transparent to-purple-500/5 border-indigo-500/20">
      <div className="flex items-center justify-between mb-4">
        <div>
          <div className="flex items-center space-x-2">
            <Zap className="w-5 h-5 text-amber-500" />
            <h3 className="text-lg font-bold text-slate-900 dark:text-white">
              Skill Gap &amp; Readiness Bridge
            </h3>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            Targeted remediation path for <span className="font-semibold">{opportunityTitle}</span>
          </p>
        </div>

        <Badge variant={isFullyQualified ? "success" : "warning"} size="sm">
          {isFullyQualified ? "100% Core Prereqs Met" : `${data.estimated_readiness_days} Day Bridge`}
        </Badge>
      </div>

      {/* Skills Comparison Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-4">
        <div className="p-3.5 rounded-xl bg-white dark:bg-obsidian-800 border border-slate-200 dark:border-obsidian-700">
          <div className="text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider mb-2 flex items-center">
            <CheckCircle2 className="w-3.5 h-3.5 mr-1" />
            Verified Current Skills
          </div>
          <div className="flex flex-wrap gap-1.5">
            {data.current_skills.map((s) => (
              <span
                key={s}
                className="px-2 py-0.5 text-xs font-medium rounded-md bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border border-emerald-500/20"
              >
                {s}
              </span>
            ))}
          </div>
        </div>

        <div className="p-3.5 rounded-xl bg-white dark:bg-obsidian-800 border border-slate-200 dark:border-obsidian-700">
          <div className="text-xs font-bold text-amber-600 dark:text-amber-400 uppercase tracking-wider mb-2 flex items-center">
            <AlertTriangle className="w-3.5 h-3.5 mr-1" />
            Missing Prerequisite Skills
          </div>
          <div className="flex flex-wrap gap-1.5">
            {data.missing_skills.length > 0 ? (
              data.missing_skills.map((s) => (
                <span
                  key={s}
                  className="px-2 py-0.5 text-xs font-medium rounded-md bg-amber-500/10 text-amber-700 dark:text-amber-300 border border-amber-500/20"
                >
                  {s}
                </span>
              ))
            ) : (
              <span className="text-xs text-slate-500 dark:text-slate-400 italic">
                No missing prerequisite skills detected.
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Readiness Bridge Projection */}
      <div className="p-4 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center space-x-6">
          <div>
            <div className="text-[10px] font-bold uppercase text-slate-400">
              Current Match
            </div>
            <div className="text-xl font-extrabold text-slate-900 dark:text-white">
              {data.current_match_pct.toFixed(1)}%
            </div>
          </div>

          <ArrowRight className="w-5 h-5 text-indigo-500" />

          <div>
            <div className="text-[10px] font-bold uppercase text-indigo-600 dark:text-indigo-400 flex items-center">
              <TrendingUp className="w-3 h-3 mr-1" />
              Projected Match
            </div>
            <div className="text-xl font-extrabold text-emerald-600 dark:text-emerald-400">
              {data.expected_match_after_remediation_pct.toFixed(1)}%
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <span className="inline-flex items-center text-xs font-semibold text-slate-600 dark:text-slate-300">
            <Clock className="w-3.5 h-3.5 mr-1 text-indigo-500" />
            Est. Bridge Time: {data.estimated_readiness_days} days
          </span>
          <Button size="sm" variant="primary">
            Start Learning Bridge
          </Button>
        </div>
      </div>

      {/* Recommended Learning Path Steps */}
      <div className="mt-4 space-y-2">
        <div className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
          Targeted Remediation Roadmap
        </div>
        {data.learning_path_steps.map((step, index) => (
          <div
            key={index}
            className="text-xs p-2.5 rounded-lg bg-white dark:bg-obsidian-800 border border-slate-200 dark:border-obsidian-700 flex items-center justify-between"
          >
            <span className="text-slate-700 dark:text-slate-300 font-medium">
              Step {index + 1}: {step}
            </span>
            <span className="text-[11px] font-semibold text-indigo-600 dark:text-indigo-400">
              AI Guided
            </span>
          </div>
        ))}
      </div>
    </Card>
  );
};
