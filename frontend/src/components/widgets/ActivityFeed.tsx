import React from "react";
import { Activity, Clock, User, ShieldAlert } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { cn } from "@/utils/cn";

export interface ActivityItem {
  id: string | number;
  user: string;
  action: string;
  timestamp: string;
  type?: "normal" | "security" | "ai";
}

export interface ActivityFeedProps {
  items: ActivityItem[];
  title?: string;
  className?: string;
}

export const ActivityFeed: React.FC<ActivityFeedProps> = ({
  items,
  title = "Real-Time System Activity Feed",
  className,
}) => {
  return (
    <Card variant="default" className={cn("p-5 space-y-4", className)}>
      <div className="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-obsidian-600">
        <div className="flex items-center space-x-2">
          <Activity className="w-4 h-4 text-emerald-400 animate-pulse" />
          <h4 className="font-semibold text-sm text-slate-900 dark:text-white">{title}</h4>
        </div>
        <Badge variant="success" size="sm">Live Feed</Badge>
      </div>

      <div className="space-y-3 max-h-80 overflow-y-auto pr-1">
        {items.map((it) => (
          <div
            key={it.id}
            className="flex items-start justify-between p-3 rounded-lg bg-slate-50 dark:bg-obsidian-900/60 border border-slate-200 dark:border-obsidian-600/50 hover:border-indigo-500/30 transition-all text-xs"
          >
            <div className="flex items-start space-x-2.5">
              <div className={cn(
                "p-1.5 rounded-full mt-0.5",
                it.type === "security" ? "bg-rose-500/20 text-rose-400" :
                it.type === "ai" ? "bg-purple-500/20 text-purple-400" : "bg-indigo-500/20 text-indigo-400"
              )}>
                {it.type === "security" ? <ShieldAlert className="w-3.5 h-3.5" /> : <User className="w-3.5 h-3.5" />}
              </div>
              <div>
                <span className="font-semibold text-slate-900 dark:text-white">{it.user}</span>
                <p className="text-slate-600 dark:text-slate-300 mt-0.5 leading-snug">{it.action}</p>
              </div>
            </div>
            <span className="text-[10px] text-slate-500 font-mono flex items-center gap-1 shrink-0 ml-2">
              <Clock className="w-3 h-3" /> {it.timestamp}
            </span>
          </div>
        ))}
      </div>
    </Card>
  );
};
