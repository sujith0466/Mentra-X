import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { HelpCircle, ChevronDown, ChevronUp, CheckCircle2, AlertCircle } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { cn } from "@/utils/cn";

export interface ReasoningStep {
  step: number;
  title: string;
  detail: string;
  status?: "passed" | "flagged";
}

export interface ExplainabilityPanelProps {
  score: number;
  steps: ReasoningStep[];
  model?: string;
  className?: string;
}

export const ExplainabilityPanel: React.FC<ExplainabilityPanelProps> = ({
  score,
  steps,
  model = "AI Safety Multi-Agent Validator",
  className,
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <Card variant="default" className={cn("p-4 border-indigo-500/20 bg-slate-50 dark:bg-obsidian-900/60", className)}>
      <div
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center justify-between cursor-pointer select-none"
      >
        <div className="flex items-center space-x-2">
          <HelpCircle className="w-4 h-4 text-indigo-400" />
          <span className="text-sm font-semibold text-slate-900 dark:text-white">AI Explainability & Reasoning</span>
          <Badge variant="cyan" size="sm">{model}</Badge>
        </div>
        <div className="flex items-center space-x-3">
          <span className="text-xs font-mono text-emerald-400 font-bold">
            Confidence: {(score * 100).toFixed(1)}%
          </span>
          {isExpanded ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
        </div>
      </div>

      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden pt-4 mt-4 border-t border-slate-200 dark:border-obsidian-600 space-y-3"
          >
            {steps.map((st) => (
              <div key={st.step} className="flex items-start space-x-3 p-2.5 rounded-lg bg-white dark:bg-obsidian-800/80 border border-slate-200 dark:border-obsidian-600/50">
                {st.status === "flagged" ? (
                  <AlertCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                ) : (
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                )}
                <div>
                  <span className="text-xs font-semibold text-slate-900 dark:text-white block">Step {st.step}: {st.title}</span>
                  <p className="text-xs text-slate-400 mt-0.5 leading-relaxed">{st.detail}</p>
                </div>
              </div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </Card>
  );
};
