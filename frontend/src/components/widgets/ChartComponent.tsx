import React from "react";
import { BarChart3, TrendingUp } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { cn } from "@/utils/cn";

export interface DataPoint {
  label: string;
  value: number;
  color?: string;
}

export interface ChartComponentProps {
  title: string;
  data: DataPoint[];
  type?: "bar" | "progress";
  maxValue?: number;
  className?: string;
}

export const ChartComponent: React.FC<ChartComponentProps> = ({
  title,
  data,
  type = "bar",
  maxValue,
  className,
}) => {
  const max = maxValue || Math.max(...data.map((d) => d.value), 100);

  return (
    <Card variant="default" className={cn("p-5 space-y-4", className)}>
      <div className="flex items-center justify-between pb-2 border-b border-obsidian-600">
        <div className="flex items-center space-x-2">
          <BarChart3 className="w-4 h-4 text-indigo-400" />
          <h4 className="font-semibold text-sm text-white">{title}</h4>
        </div>
        <span className="text-xs font-mono text-slate-500 flex items-center gap-1">
          <TrendingUp className="w-3 h-3 text-emerald-400" /> Live Metrics
        </span>
      </div>

      <div className="space-y-3 pt-2">
        {data.map((item, idx) => {
          const pct = Math.min(Math.round((item.value / max) * 100), 100);
          const barColor = item.color || "from-primary-600 to-indigo-400";

          return (
            <div key={idx} className="space-y-1">
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-300 font-medium">{item.label}</span>
                <span className="font-mono text-slate-400 font-bold">{item.value} ({pct}%)</span>
              </div>
              <div className="w-full h-2.5 rounded-full bg-obsidian-900 border border-obsidian-600 overflow-hidden">
                <div
                  style={{ width: `${pct}%` }}
                  className={cn("h-full rounded-full bg-gradient-to-r transition-all duration-500", barColor)}
                />
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
};
