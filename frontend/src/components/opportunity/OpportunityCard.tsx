import React, { useState } from "react";
import {
  Sparkles,
  MapPin,
  Calendar,
  DollarSign,
  ArrowRight,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  ChevronDown,
  ChevronUp,
  Bookmark
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";

export interface MatchExplanation {
  factor: string;
  impact: string;
  detail: string;
  score_delta: number;
}

export interface OpportunityItem {
  opportunity_id: string;
  title: string;
  organization: string;
  category: string;
  location: string;
  stipend_or_reward: string;
  deadline: string;
  required_skills: string[];
  description: string;
  external_url: string;
}

export interface MatchedOpportunity {
  opportunity: OpportunityItem;
  match_percentage: number;
  readiness_level: string;
  explanations: MatchExplanation[];
  lifecycle_status: string;
}

interface OpportunityCardProps {
  item: MatchedOpportunity;
  onStatusChange: (opportunityId: string, newStatus: string) => void;
  onInspectSkillGap?: (opportunityId: string) => void;
}

export const OpportunityCard: React.FC<OpportunityCardProps> = ({
  item,
  onStatusChange,
  onInspectSkillGap
}) => {
  const [showExplainability, setShowExplainability] = useState(false);
  const { opportunity, match_percentage, readiness_level, explanations, lifecycle_status } = item;

  const getCategoryBadgeVariant = (cat: string) => {
    switch (cat) {
      case "INTERNSHIP":
        return "indigo";
      case "HACKATHON":
        return "purple";
      case "JOB":
        return "cyan";
      case "SCHOLARSHIP":
        return "success";
      default:
        return "default";
    }
  };

  const getMatchBadgeVariant = (pct: number) => {
    if (pct >= 85) return "success";
    if (pct >= 70) return "indigo";
    return "warning";
  };

  return (
    <Card className="p-6 transition-all duration-200 hover:shadow-md border border-slate-200 dark:border-obsidian-600 bg-white dark:bg-obsidian-800">
      <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
        {/* Left column: Title, organization, badges */}
        <div className="space-y-2">
          <div className="flex flex-wrap items-center gap-2">
            <Badge variant={getCategoryBadgeVariant(opportunity.category)} size="sm">
              {opportunity.category}
            </Badge>
            <Badge variant={getMatchBadgeVariant(match_percentage)} size="sm">
              <Sparkles className="w-3.5 h-3.5 mr-1" />
              {match_percentage.toFixed(1)}% Match
            </Badge>
            <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-obsidian-700 text-slate-700 dark:text-slate-300">
              {readiness_level.replace("_", " ")}
            </span>
          </div>

          <h3 className="text-lg font-bold text-slate-900 dark:text-white leading-snug">
            {opportunity.title}
          </h3>
          <div className="text-sm font-semibold text-indigo-600 dark:text-indigo-400">
            {opportunity.organization}
          </div>

          <p className="text-xs text-slate-600 dark:text-slate-300 max-w-2xl leading-relaxed">
            {opportunity.description}
          </p>

          <div className="flex flex-wrap items-center gap-4 pt-2 text-xs text-slate-500 dark:text-slate-400">
            <span className="flex items-center">
              <MapPin className="w-3.5 h-3.5 mr-1 text-slate-400" />
              {opportunity.location}
            </span>
            <span className="flex items-center">
              <DollarSign className="w-3.5 h-3.5 mr-1 text-emerald-500" />
              {opportunity.stipend_or_reward}
            </span>
            <span className="flex items-center">
              <Calendar className="w-3.5 h-3.5 mr-1 text-amber-500" />
              Deadline: {opportunity.deadline}
            </span>
          </div>
        </div>

        {/* Right column: Actions */}
        <div className="flex flex-col sm:flex-row md:flex-col gap-2 shrink-0">
          <Button
            size="sm"
            variant="primary"
            rightIcon={<ArrowRight className="w-3.5 h-3.5" />}
            onClick={() => window.open(opportunity.external_url || "#", "_blank")}
          >
            Apply Now
          </Button>

          <Button
            size="sm"
            variant="outline"
            leftIcon={<Bookmark className="w-3.5 h-3.5" />}
            onClick={() => onStatusChange(opportunity.opportunity_id, "SAVED")}
          >
            {lifecycle_status === "SAVED" ? "Saved" : "Save Opportunity"}
          </Button>

          <Button
            size="sm"
            variant="secondary"
            onClick={() => setShowExplainability(!showExplainability)}
            leftIcon={<HelpCircle className="w-3.5 h-3.5" />}
          >
            Why Recommended?
          </Button>
        </div>
      </div>

      {/* Required skills chips */}
      <div className="mt-4 pt-3 border-t border-slate-100 dark:border-obsidian-700 flex flex-wrap items-center gap-1.5">
        <span className="text-xs font-semibold text-slate-400 mr-1">Prerequisites:</span>
        {opportunity.required_skills.map((skill) => (
          <span
            key={skill}
            className="px-2 py-0.5 text-[11px] font-medium rounded-md bg-slate-100 dark:bg-obsidian-700 text-slate-700 dark:text-slate-300"
          >
            {skill}
          </span>
        ))}
      </div>

      {/* Match Explainability Drawer Section */}
      {showExplainability && (
        <div className="mt-4 p-4 rounded-xl bg-slate-50 dark:bg-obsidian-900/70 border border-indigo-500/20 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
              AI Match Explainability Breakdown
            </span>
            {onInspectSkillGap && (
              <button
                onClick={() => onInspectSkillGap(opportunity.opportunity_id)}
                className="text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:underline"
              >
                Inspect Skill Gap Bridge →
              </button>
            )}
          </div>

          <div className="space-y-2">
            {explanations.map((exp, idx) => (
              <div
                key={idx}
                className="flex items-start justify-between text-xs p-2 rounded-lg bg-white dark:bg-obsidian-800 border border-slate-200 dark:border-obsidian-700"
              >
                <div className="flex items-start space-x-2">
                  {exp.impact === "POSITIVE" ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  ) : (
                    <AlertCircle className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
                  )}
                  <div>
                    <span className="font-semibold text-slate-900 dark:text-white block">
                      {exp.factor}
                    </span>
                    <span className="text-slate-600 dark:text-slate-300">
                      {exp.detail}
                    </span>
                  </div>
                </div>
                <span
                  className={`font-bold ml-2 shrink-0 ${
                    exp.score_delta >= 0 ? "text-emerald-600 dark:text-emerald-400" : "text-rose-500"
                  }`}
                >
                  {exp.score_delta >= 0 ? `+${exp.score_delta}%` : `${exp.score_delta}%`}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </Card>
  );
};
