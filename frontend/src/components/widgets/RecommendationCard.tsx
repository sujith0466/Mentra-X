import React from "react";
import { Sparkles, ArrowRight, Bookmark } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { cn } from "@/utils/cn";

export interface RecommendationCardProps {
  title: string;
  description: string;
  category: string;
  priority?: "high" | "medium" | "low";
  actionLabel?: string;
  onAction?: () => void;
  className?: string;
}

export const RecommendationCard: React.FC<RecommendationCardProps> = ({
  title,
  description,
  category,
  priority = "medium",
  actionLabel = "Start Learning",
  onAction,
  className,
}) => {
  const priorityBadges = {
    high: { label: "High Priority", variant: "danger" as const },
    medium: { label: "Recommended", variant: "primary" as const },
    low: { label: "Optional", variant: "default" as const },
  };

  return (
    <Card variant="interactive" className={cn("flex flex-col justify-between p-5", className)}>
      <div>
        <div className="flex items-center justify-between mb-3">
          <Badge variant="purple" size="sm">
            <Sparkles className="w-3 h-3 mr-1 text-ai-violet" /> {category}
          </Badge>
          <Badge variant={priorityBadges[priority].variant} size="sm">
            {priorityBadges[priority].label}
          </Badge>
        </div>
        <h4 className="font-bold text-white text-base leading-snug">{title}</h4>
        <p className="text-xs text-slate-400 mt-1.5 line-clamp-2 leading-relaxed">{description}</p>
      </div>

      <div className="flex items-center justify-between pt-4 mt-4 border-t border-obsidian-600/50">
        <button className="text-slate-500 hover:text-slate-300 transition-colors p-1" title="Save for later">
          <Bookmark className="w-4 h-4" />
        </button>
        <Button size="sm" variant="outline" onClick={onAction} rightIcon={<ArrowRight className="w-3.5 h-3.5" />}>
          {actionLabel}
        </Button>
      </div>
    </Card>
  );
};
