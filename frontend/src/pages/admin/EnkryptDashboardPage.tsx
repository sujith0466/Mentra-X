import React, { useState } from "react";
import { Shield, ShieldCheck, AlertTriangle, CheckCircle2, Lock, FileText, Download, Activity, Eye, Check, Zap } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { MetricCard } from "@/components/widgets/MetricCard";
import { Modal } from "@/components/ui/Modal";

interface SecurityLog {
  id: string;
  timestamp: string;
  user: string;
  event: string;
  layer: string;
  status: "APPROVE" | "INTERCEPT" | "REDACT";
  confidence: number;
}

export const EnkryptDashboardPage: React.FC = () => {
  const [logs, setLogs] = useState<SecurityLog[]>([
    { id: "log-1", timestamp: "02:14:02 UTC", user: "stu_010 (Alex)", event: "Socratic Tutor Query", layer: "Layer 6 (Hallucination Check)", status: "APPROVE", confidence: 0.99 },
    { id: "log-2", timestamp: "02:12:45 UTC", user: "stu_409 (Sarah)", event: "SQL Injection Probe in Code Sandbox", layer: "Layer 3 (Injection Defense)", status: "INTERCEPT", confidence: 0.98 },
    { id: "log-3", timestamp: "01:58:12 UTC", user: "stu_882 (David)", event: "API Key PII Inclusion in Chat", layer: "Layer 2 (PII Redactor)", status: "REDACT", confidence: 0.95 },
    { id: "log-4", timestamp: "01:45:00 UTC", user: "fac_001 (Prof. Thorne)", event: "Syllabus Embedding Batch Sync", layer: "Layer 6 (Integrity Verifier)", status: "APPROVE", confidence: 1.00 },
  ]);

  const [selectedLog, setSelectedLog] = useState<SecurityLog | null>(null);
  const [filter, setFilter] = useState<"ALL" | "APPROVE" | "INTERCEPT" | "REDACT">("ALL");

  const filteredLogs = filter === "ALL" ? logs : logs.filter((l) => l.status === filter);

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-6">
        <div>
          <Badge variant="cyan" className="mb-2">
            <Shield className="w-3.5 h-3.5 mr-1.5 inline text-emerald-400" />
            ESDLC Layer 6 Safety Governance
          </Badge>
          <h1 className="text-3xl font-extrabold text-white">Enkrypt Security & Privacy Dashboard</h1>
          <p className="text-sm text-slate-400">Real-time hallucination interception, prompt injection defense, and institutional compliance audit logs.</p>
        </div>

        <div className="flex items-center gap-3">
          <Badge variant="success" className="px-4 py-2 text-sm">
            <ShieldCheck className="w-4 h-4 mr-2 inline" />
            Layer 6 Active & Auditing
          </Badge>
          <Button variant="secondary" onClick={() => alert("Exporting encrypted audit archive (GDPR compliance)...")} className="text-xs py-2">
            <Download className="w-3.5 h-3.5 mr-1.5" />
            Export Compliance Archive
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard title="Safety Approval Rate" value="99.82%" trend={0.5} trendLabel="36/36 ESDLC checks passed" icon={<Check className="w-5 h-5 text-emerald-400" />} />
        <MetricCard title="Threat Interceptions" value="142" trend={-8.0} trendLabel="vs last week" icon={<Shield className="w-5 h-5 text-rose-400" />} />
        <MetricCard title="PII Redactions Executed" value="38" trend={0.0} trendLabel="Zero credential leaks" icon={<Lock className="w-5 h-5 text-amber-400" />} />
        <MetricCard title="Avg Intercept Latency" value="3.2 ms" trend={-1.2} trendLabel="In-memory evaluation" icon={<Zap className="w-5 h-5 text-cyan-400" />} />
      </div>

      {/* Architecture Overview Card */}
      <Card variant="glow" className="p-8 grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
        <div className="md:col-span-2 space-y-3">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Lock className="w-6 h-6 text-emerald-400" />
            How Enkrypt Layer 6 Safeguards Your Campus
          </h2>
          <p className="text-sm text-slate-300 leading-relaxed font-sans">
            Unlike standard AI wrappers, Mentra X embeds Enkrypt Layer 6 as a mandatory proxy between Mastra swarms and Qdrant memory. It enforces cosine similarity boundaries (&gt;0.85 required) to ensure zero hallucination variance and strips personal identifiers before external LLM dispatch.
          </p>
        </div>
        <div className="flex flex-col gap-2 justify-center">
          <div className="p-3 rounded-xl bg-obsidian-950/80 border border-white/10 text-xs text-center font-mono text-emerald-400">
            ✓ GDPR Article 17 Compliant
          </div>
          <div className="p-3 rounded-xl bg-obsidian-950/80 border border-white/10 text-xs text-center font-mono text-cyan-400">
            ✓ ISO 27001 AI Security Align
          </div>
        </div>
      </Card>

      {/* Real-Time Audit Logs Table */}
      <Card variant="default" className="p-6 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-indigo-400" />
            Real-Time Security & Interception Log
          </h3>

          <div className="flex bg-obsidian-900 rounded-lg p-1 border border-white/10 self-start sm:self-center">
            {(["ALL", "APPROVE", "INTERCEPT", "REDACT"] as const).map((st) => (
              <button
                key={st}
                onClick={() => setFilter(st)}
                className={`px-3 py-1 rounded-md text-xs font-bold transition-all ${
                  filter === st ? "bg-indigo-600 text-white shadow-sm" : "text-slate-400 hover:text-white"
                }`}
              >
                {st}
              </button>
            ))}
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-sm">
            <thead>
              <tr className="border-b border-white/10 text-xs font-semibold uppercase tracking-wider text-slate-400 bg-obsidian-900/50">
                <th className="py-3 px-4">Timestamp (UTC)</th>
                <th className="py-3 px-4">Student / Identity</th>
                <th className="py-3 px-4">Event Description</th>
                <th className="py-3 px-4">Enkrypt Layer Triggered</th>
                <th className="py-3 px-4">Action</th>
                <th className="py-3 px-4 text-right">Confidence</th>
                <th className="py-3 px-4 text-right">Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 text-slate-300 font-mono text-xs">
              {filteredLogs.map((log) => {
                const statusBadges = {
                  APPROVE: "success",
                  INTERCEPT: "danger",
                  REDACT: "cyan",
                } as const;
                return (
                  <tr key={log.id} className="hover:bg-white/5 font-sans">
                    <td className="py-3 px-4 font-mono text-slate-400">{log.timestamp}</td>
                    <td className="py-3 px-4 font-bold text-white">{log.user}</td>
                    <td className="py-3 px-4">{log.event}</td>
                    <td className="py-3 px-4 text-xs text-indigo-300">{log.layer}</td>
                    <td className="py-3 px-4">
                      <Badge variant={statusBadges[log.status]}>{log.status}</Badge>
                    </td>
                    <td className="py-3 px-4 text-right font-mono font-bold text-cyan-400">
                      {(log.confidence * 100).toFixed(0)}%
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => setSelectedLog(log)}
                        className="p-1.5 rounded-lg bg-obsidian-900 hover:bg-white/10 text-slate-400 hover:text-white transition-all"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Log Detail Modal */}
      <Modal isOpen={!!selectedLog} onClose={() => setSelectedLog(null)} title="Enkrypt Audit Log Inspection">
        {selectedLog && (
          <div className="space-y-4 text-slate-300 font-sans text-sm">
            <div className="grid grid-cols-2 gap-4 p-4 rounded-xl bg-obsidian-950 border border-white/10 font-mono text-xs">
              <div>
                <span className="text-slate-500 block">Event ID</span>
                <span className="text-white font-bold">{selectedLog.id}</span>
              </div>
              <div>
                <span className="text-slate-500 block">Timestamp</span>
                <span className="text-white font-bold">{selectedLog.timestamp}</span>
              </div>
              <div>
                <span className="text-slate-500 block">Identity / User</span>
                <span className="text-cyan-400 font-bold">{selectedLog.user}</span>
              </div>
              <div>
                <span className="text-slate-500 block">Status Decision</span>
                <Badge variant={selectedLog.status === "APPROVE" ? "success" : selectedLog.status === "INTERCEPT" ? "danger" : "cyan"}>
                  {selectedLog.status}
                </Badge>
              </div>
            </div>

            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">Telemetry Evaluation Note</h4>
              <p className="p-3 rounded-lg bg-obsidian-900 border border-white/5 text-xs text-slate-300 leading-relaxed">
                {selectedLog.status === "APPROVE" && "Cosine similarity against authoritative Qdrant syllabus embedding passed threshold (0.99 >= 0.85). No prompt injection heuristics triggered."}
                {selectedLog.status === "INTERCEPT" && "High-risk adversarial SQL syntax pattern detected in code sandbox input. Enkrypt Layer 3 terminated request before LLM execution."}
                {selectedLog.status === "REDACT" && "Regex and NER detected secret string resembling API Bearer Token. Token stripped and replaced with [REDACTED_SECRET] prior to swarm dispatch."}
              </p>
            </div>

            <div className="pt-4 flex justify-end">
              <Button variant="primary" onClick={() => setSelectedLog(null)}>
                Close Audit View
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};
