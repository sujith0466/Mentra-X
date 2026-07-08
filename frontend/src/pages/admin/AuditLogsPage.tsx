import React from "react";
import { ShieldAlert, CheckCircle2, Clock, Filter, AlertTriangle } from "lucide-react";
import { DataTable, Column } from "@/components/ui/DataTable";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { SafetyBadge } from "@/components/widgets/SafetyBadge";

export interface AuditRow {
  id: string;
  timestamp: string;
  source: string;
  action: string;
  status: "APPROVE" | "REGENERATE" | "HARD_FAIL" | "VERIFIED";
  user: string;
  similarity: number;
}

export const AuditLogsPage: React.FC = () => {
  const logs: AuditRow[] = [
    { id: "LOG-9001", timestamp: "2026-07-06 06:35:12", source: "Safety System Layer 6 Gateway", action: "Intercepted off-topic query in Agentic Coding tutor", status: "HARD_FAIL", user: "STU-103", similarity: 0.42 },
    { id: "LOG-9002", timestamp: "2026-07-06 06:34:00", source: "Mentra tutor Router", action: "Routed student query to Database Learning Memory search tool", status: "VERIFIED", user: "STU-101", similarity: 0.99 },
    { id: "LOG-9003", timestamp: "2026-07-06 06:30:45", source: "Safety System Safety Interceptor", action: "Regenerating tutoring response due to low confidence threshold", status: "REGENERATE", user: "STU-104", similarity: 0.68 },
    { id: "LOG-9004", timestamp: "2026-07-06 06:25:10", source: "Learning Profile Sync Service", action: "Updated knowledge retention heuristics for 1,240 twins", status: "APPROVE", user: "SYSTEM_tutor", similarity: 1.0 },
  ];

  const columns: Column<AuditRow>[] = [
    { key: "id", title: "Event ID", sortable: true, render: (item) => <span className="font-mono text-xs text-slate-400">{item.id}</span> },
    { key: "timestamp", title: "Timestamp", sortable: true, render: (item) => <span className="font-mono text-xs text-slate-600 dark:text-slate-300">{item.timestamp}</span> },
    { key: "source", title: "Source Component", sortable: true, render: (item) => <span className="font-semibold text-slate-900 dark:text-white">{item.source}</span> },
    { key: "action", title: "Action Description", render: (item) => <span className="text-slate-600 dark:text-slate-300">{item.action}</span> },
    { key: "status", title: "Safety System Verdict", sortable: true, render: (item) => <SafetyBadge status={item.status} score={item.similarity} /> },
    { key: "user", title: "Actor ID", sortable: true, render: (item) => <Badge variant="default" size="sm">{item.user}</Badge> },
  ];

  return (
    <div className="space-y-8 py-6">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-slate-200 dark:border-obsidian-600 pb-6">
        <div>
          <div className="flex items-center space-x-2">
            <Badge variant="cyan" size="sm">Safety System Layer 6</Badge>
            <Badge variant="success" size="sm">Immutable Audit Trail</Badge>
          </div>
          <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white mt-1">Security Audit & Governance Logs</h1>
          <p className="text-sm text-slate-400 mt-1">Real-time inspection of safety interceptions, PII filtering, and vector similarity verifications.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card variant="glass" className="p-4 flex items-center justify-between">
          <div>
            <span className="text-xs text-slate-400 font-semibold block">Total Intercepts (24h)</span>
            <span className="text-2xl font-bold text-slate-900 dark:text-white mt-1 block">142 Events</span>
          </div>
          <ShieldAlert className="w-8 h-8 text-rose-400 opacity-80" />
        </Card>
        <Card variant="glass" className="p-4 flex items-center justify-between">
          <div>
            <span className="text-xs text-slate-400 font-semibold block">Average Similarity Score</span>
            <span className="text-2xl font-bold text-emerald-400 mt-1 block">0.964</span>
          </div>
          <CheckCircle2 className="w-8 h-8 text-emerald-400 opacity-80" />
        </Card>
        <Card variant="glass" className="p-4 flex items-center justify-between">
          <div>
            <span className="text-xs text-slate-400 font-semibold block">Hallucination Prevention Rate</span>
            <span className="text-2xl font-bold text-cyan-400 mt-1 block">100.0%</span>
          </div>
          <AlertTriangle className="w-8 h-8 text-cyan-400 opacity-80" />
        </Card>
      </div>

      <Card variant="default" className="p-6">
        <DataTable
          data={logs}
          columns={columns}
          searchKey="action"
          searchPlaceholder="Search logs by keyword or action..."
        />
      </Card>
    </div>
  );
};
