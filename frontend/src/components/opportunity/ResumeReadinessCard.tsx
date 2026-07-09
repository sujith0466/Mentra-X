import React from "react";
import { FileText, CheckCircle2, AlertCircle, Sparkles, ArrowRight } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Link } from "react-router-dom";

export interface ResumeReadinessData {
  opportunity_id: string;
  ats_score: number;
  matched_keywords: string[];
  missing_keywords: string[];
  suggested_improvements: string[];
  missing_projects_note: string;
}

interface ResumeReadinessCardProps {
  data: ResumeReadinessData;
}

export const ResumeReadinessCard: React.FC<ResumeReadinessCardProps> = ({ data }) => {
  return (
    <Card className="p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <FileText className="w-5 h-5 text-indigo-500" />
          <h3 className="text-lg font-bold text-slate-900 dark:text-white">
            Resume ATS Alignment &amp; Keyword Analysis
          </h3>
        </div>
        <Badge variant={data.ats_score >= 80 ? "success" : "warning"} size="sm">
          ATS Index: {data.ats_score.toFixed(0)} / 100
        </Badge>
      </div>

      {/* Keywords breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-4">
        <div className="p-3.5 rounded-xl bg-slate-50 dark:bg-obsidian-900/50 border border-slate-200 dark:border-obsidian-700">
          <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400 block mb-2">
            Matched Keywords ({data.matched_keywords.length})
          </span>
          <div className="flex flex-wrap gap-1.5">
            {data.matched_keywords.map((kw) => (
              <span
                key={kw}
                className="px-2 py-0.5 text-xs font-medium rounded-md bg-emerald-500/10 text-emerald-700 dark:text-emerald-300"
              >
                {kw}
              </span>
            ))}
          </div>
        </div>

        <div className="p-3.5 rounded-xl bg-slate-50 dark:bg-obsidian-900/50 border border-slate-200 dark:border-obsidian-700">
          <span className="text-xs font-bold text-rose-600 dark:text-rose-400 block mb-2">
            Missing Target Keywords ({data.missing_keywords.length})
          </span>
          <div className="flex flex-wrap gap-1.5">
            {data.missing_keywords.length > 0 ? (
              data.missing_keywords.map((kw) => (
                <span
                  key={kw}
                  className="px-2 py-0.5 text-xs font-medium rounded-md bg-rose-500/10 text-rose-700 dark:text-rose-300"
                >
                  {kw}
                </span>
              ))
            ) : (
              <span className="text-xs text-slate-500 dark:text-slate-400 italic">
                No missing target keywords.
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Projects Gap Note */}
      <div className="p-3.5 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-xs text-slate-700 dark:text-slate-300 mb-4 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Sparkles className="w-4 h-4 text-indigo-500 shrink-0" />
          <span>{data.missing_projects_note}</span>
        </div>
        <Link to="/student/projects">
          <Button size="sm" variant="outline">
            Open Studio
          </Button>
        </Link>
      </div>

      {/* Actionable Suggestions List */}
      <div className="space-y-2">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
          AI Resume Enhancements
        </span>
        {data.suggested_improvements.map((tip, idx) => (
          <div
            key={idx}
            className="flex items-start space-x-2 text-xs p-2.5 rounded-lg bg-white dark:bg-obsidian-800 border border-slate-200 dark:border-obsidian-700"
          >
            <CheckCircle2 className="w-3.5 h-3.5 text-indigo-500 shrink-0 mt-0.5" />
            <span className="text-slate-700 dark:text-slate-300 leading-relaxed">
              {tip}
            </span>
          </div>
        ))}
      </div>

      <div className="mt-4 flex justify-end">
        <Link to="/student/career/resume">
          <Button size="sm" variant="primary" rightIcon={<ArrowRight className="w-3.5 h-3.5" />}>
            Optimize Resume Studio
          </Button>
        </Link>
      </div>
    </Card>
  );
};
