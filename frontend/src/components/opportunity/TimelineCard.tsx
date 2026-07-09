import React from "react";
import { Calendar, Clock, CheckCircle2, AlertCircle, RefreshCw } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

export interface TimelineEntry {
  entry_id: string;
  user_id: number;
  opportunity_id: string;
  opportunity_title: string;
  organization: string;
  status: string;
  updated_at: string;
  reminder_note: string;
}

interface TimelineCardProps {
  entries: TimelineEntry[];
  onStatusChange: (opportunityId: string, newStatus: string) => void;
}

const LIFECYCLE_STAGES = [
  "RECOMMENDED",
  "SAVED",
  "INTERESTED",
  "APPLIED",
  "INTERVIEW",
  "ACCEPTED",
  "REJECTED",
  "COMPLETED",
  "EXPIRED"
];

export const TimelineCard: React.FC<TimelineCardProps> = ({ entries, onStatusChange }) => {
  const getStatusBadgeVariant = (st: string) => {
    switch (st) {
      case "ACCEPTED":
      case "COMPLETED":
        return "success";
      case "INTERVIEW":
      case "APPLIED":
        return "indigo";
      case "SAVED":
      case "INTERESTED":
        return "cyan";
      case "REJECTED":
      case "EXPIRED":
        return "danger";
      default:
        return "default";
    }
  };

  return (
    <Card className="p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <Calendar className="w-5 h-5 text-indigo-500" />
          <h3 className="text-lg font-bold text-slate-900 dark:text-white">
            Opportunity Lifecycle Timeline
          </h3>
        </div>
        <Badge variant="purple" size="sm">
          9-Stage Pipeline
        </Badge>
      </div>

      {entries.length === 0 ? (
        <p className="text-xs text-slate-500 dark:text-slate-400 py-6 text-center">
          No active opportunities tracked in your timeline yet. Save or apply to start tracking!
        </p>
      ) : (
        <div className="space-y-4">
          {entries.map((item) => (
            <div
              key={item.entry_id}
              className="p-4 rounded-xl bg-white dark:bg-obsidian-800 border border-slate-200 dark:border-obsidian-700 flex flex-col md:flex-row md:items-center justify-between gap-4"
            >
              <div className="space-y-1">
                <div className="flex items-center space-x-2">
                  <span className="font-bold text-slate-900 dark:text-white text-sm">
                    {item.opportunity_title}
                  </span>
                  <Badge variant={getStatusBadgeVariant(item.status)} size="sm">
                    {item.status}
                  </Badge>
                </div>
                <div className="text-xs text-indigo-600 dark:text-indigo-400 font-semibold">
                  {item.organization}
                </div>
                {item.reminder_note && (
                  <p className="text-xs text-slate-500 dark:text-slate-400 flex items-center pt-1">
                    <Clock className="w-3.5 h-3.5 mr-1 text-slate-400" />
                    {item.reminder_note}
                  </p>
                )}
              </div>

              {/* Status Update Select */}
              <div className="flex items-center space-x-2 shrink-0">
                <span className="text-xs font-semibold text-slate-400">Move to:</span>
                <select
                  value={item.status}
                  onChange={(e) => onStatusChange(item.opportunity_id, e.target.value)}
                  className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-100 dark:bg-obsidian-700 border border-slate-300 dark:border-obsidian-600 text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  {LIFECYCLE_STAGES.map((st) => (
                    <option key={st} value={st}>
                      {st}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
};
