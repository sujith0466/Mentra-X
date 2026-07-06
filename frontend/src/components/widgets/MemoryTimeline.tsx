import React from "react";
import { Database, Clock, ArrowRight } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { cn } from "@/utils/cn";

export interface MemoryEvent {
  id: string | number;
  timestamp: string;
  concept: string;
  retrievalScore: number;
  summary: string;
}

export interface MemoryTimelineProps {
  events: MemoryEvent[];
  title?: string;
  className?: string;
}

export const MemoryTimeline: React.FC<MemoryTimelineProps> = ({
  events,
  title = "Qdrant Vector Memory Log",
  className,
}) => {
  return (
    <Card variant="default" className={cn("p-6", className)}>
      <div className="flex items-center justify-between pb-4 border-b border-obsidian-600 mb-6">
        <div className="flex items-center space-x-2.5">
          <Database className="w-5 h-5 text-indigo-400" />
          <h3 className="font-semibold text-white">{title}</h3>
        </div>
        <Badge variant="cyan" size="sm">Semantic Index</Badge>
      </div>

      <div className="relative border-l border-obsidian-600 ml-3 space-y-6">
        {events.map((ev, idx) => (
          <div key={ev.id || idx} className="relative pl-6 group">
            <span className="absolute -left-1.5 top-1 w-3 h-3 rounded-full bg-primary-500 ring-4 ring-obsidian-900 group-hover:scale-125 transition-transform" />
            <div className="flex items-center justify-between">
              <span className="text-sm font-semibold text-white">{ev.concept}</span>
              <div className="flex items-center space-x-2">
                <Badge variant="primary" size="sm">
                  Score: {(ev.retrievalScore * 100).toFixed(0)}%
                </Badge>
                <span className="text-xs text-slate-500 flex items-center gap-1 font-mono">
                  <Clock className="w-3 h-3" /> {ev.timestamp}
                </span>
              </div>
            </div>
            <p className="text-xs text-slate-400 mt-1 leading-relaxed">{ev.summary}</p>
          </div>
        ))}
      </div>
    </Card>
  );
};
