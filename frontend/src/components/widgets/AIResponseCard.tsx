import React, { useState } from "react";
import { Sparkles, Copy, Check, ThumbsUp, ThumbsDown } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { SafetyBadge, EnkryptAction } from "@/components/widgets/SafetyBadge";
import { cn } from "@/utils/cn";

export interface AIResponseCardProps {
  title?: string;
  content: string;
  safetyStatus?: EnkryptAction | string;
  confidenceScore?: number;
  modelName?: string;
  onFeedback?: (isPositive: boolean) => void;
  className?: string;
}

export const AIResponseCard: React.FC<AIResponseCardProps> = ({
  title = "Intelligent AI Tutor",
  content,
  safetyStatus = "APPROVE",
  confidenceScore,
  modelName = "Adaptive Intelligence v2.5",
  onFeedback,
  className,
}) => {
  const [copied, setCopied] = useState(false);
  const [feedbackGiven, setFeedbackGiven] = useState<"up" | "down" | null>(null);

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleThumb = (dir: "up" | "down") => {
    setFeedbackGiven(dir);
    if (onFeedback) onFeedback(dir === "up");
  };

  return (
    <Card
      variant="glass"
      className={cn("relative overflow-hidden border-indigo-500/30 transition-all", className)}
    >
      <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 rounded-full blur-2xl pointer-events-none" />
      
      <div className="flex items-center justify-between pb-4 border-b border-white/10 mb-4">
        <div className="flex items-center space-x-2">
          <div className="p-1.5 rounded-lg bg-primary-500/20 text-primary-500">
            <Sparkles className="w-4 h-4 animate-pulse" />
          </div>
          <span className="font-semibold text-sm text-white">{title}</span>
          <span className="text-[10px] text-slate-500 font-mono px-1.5 py-0.5 rounded bg-white/5 border border-white/10">
            {modelName}
          </span>
        </div>
        <div className="flex items-center space-x-2">
          {safetyStatus && <SafetyBadge status={safetyStatus} score={confidenceScore} />}
        </div>
      </div>

      <div className="prose prose-invert max-w-none text-sm text-slate-200 leading-relaxed font-sans whitespace-pre-wrap">
        {content}
      </div>

      <div className="flex items-center justify-between pt-4 border-t border-white/10 mt-4 text-xs text-slate-400">
        <div className="flex items-center space-x-2">
          <span>Was this explanation helpful?</span>
          <button
            onClick={() => handleThumb("up")}
            className={cn(
              "p-1 rounded hover:bg-white/10 transition-colors",
              feedbackGiven === "up" && "text-emerald-400 bg-emerald-500/10"
            )}
            title="Helpful"
          >
            <ThumbsUp className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => handleThumb("down")}
            className={cn(
              "p-1 rounded hover:bg-white/10 transition-colors",
              feedbackGiven === "down" && "text-rose-400 bg-rose-500/10"
            )}
            title="Not Helpful"
          >
            <ThumbsDown className="w-3.5 h-3.5" />
          </button>
        </div>

        <button
          onClick={handleCopy}
          className="inline-flex items-center space-x-1 px-2 py-1 rounded bg-white/5 hover:bg-white/10 text-slate-300 hover:text-white transition-colors"
        >
          {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
          <span>{copied ? "Copied" : "Copy Code"}</span>
        </button>
      </div>
    </Card>
  );
};
