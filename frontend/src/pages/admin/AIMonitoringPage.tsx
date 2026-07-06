import React, { useState } from "react";
import { Cpu, Activity, RefreshCw, AlertTriangle, CheckCircle2, ShieldAlert, Sparkles, Terminal } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { MetricCard } from "@/components/widgets/MetricCard";

export const AIMonitoringPage: React.FC = () => {
  const [isRefreshing, setIsRefreshing] = useState(false);

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => setIsRefreshing(false), 1000);
  };

  const swarmAgents = [
    { name: "Tutor AI Swarm (Socratic Core)", status: "Active", latency: "142ms", errorRate: "0.01%", requests24h: "45,210", model: "gpt-4o / mastra-v2" },
    { name: "DevTools AI (Sandbox Debugger)", status: "Active", latency: "210ms", errorRate: "0.04%", requests24h: "28,940", model: "claude-3.5-sonnet" },
    { name: "Career AI (Roadmap Engine)", status: "Active", latency: "185ms", errorRate: "0.00%", requests24h: "12,450", model: "gpt-4o-mini" },
    { name: "Qdrant Vector Retrieval Worker", status: "Active", latency: "14ms", errorRate: "0.00%", requests24h: "142,000", model: "hnsw-cosine-1536" },
  ];

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-6">
        <div>
          <Badge variant="info" className="mb-2">
            <Cpu className="w-3.5 h-3.5 mr-1.5 inline text-indigo-400" />
            Mastra Orchestration Telemetry
          </Badge>
          <h1 className="text-3xl font-extrabold text-white">AI Operations & Swarm Console</h1>
          <p className="text-sm text-slate-400">Monitor multi-agent swarm latency, token consumption, and Qdrant vector search heuristics.</p>
        </div>

        <Button variant="secondary" onClick={handleRefresh} disabled={isRefreshing} className="px-5 py-2.5 self-start sm:self-center">
          <RefreshCw className={`w-4 h-4 mr-2 ${isRefreshing ? "animate-spin text-cyan-400" : ""}`} />
          {isRefreshing ? "Syncing Telemetry..." : "Refresh Live Streams"}
        </Button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard title="Total AI Queries (24h)" value="228,600" change="+14.2% peak load" isPositive={true} icon="activity" />
        <MetricCard title="Avg Swarm Latency" value="138 ms" change="-12ms optimization" isPositive={true} icon="zap" />
        <MetricCard title="Vector Retrieval Accuracy" value="99.4%" change="0% hallucination variance" isPositive={true} icon="check" />
        <MetricCard title="Token Consumption Cost" value="$142.50" change="Within budget SLA" isPositive={true} icon="dollar" />
      </div>

      {/* Swarm Status Table */}
      <Card variant="default" className="p-6 space-y-4">
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-cyan-400" />
            Active Mastra Swarm Workers
          </h3>
          <Badge variant="success">All Systems Operational</Badge>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-sm">
            <thead>
              <tr className="border-b border-white/10 text-xs font-semibold uppercase tracking-wider text-slate-400 bg-obsidian-900/50">
                <th className="py-3 px-4">Swarm Worker Name</th>
                <th className="py-3 px-4">Underlying Model / Index</th>
                <th className="py-3 px-4">24h Requests</th>
                <th className="py-3 px-4">Avg Latency</th>
                <th className="py-3 px-4">Error Rate</th>
                <th className="py-3 px-4 text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 text-slate-300 font-mono">
              {swarmAgents.map((agent) => (
                <tr key={agent.name} className="hover:bg-white/5 font-sans">
                  <td className="py-3 px-4 font-bold text-white">{agent.name}</td>
                  <td className="py-3 px-4 text-xs font-mono text-indigo-300">{agent.model}</td>
                  <td className="py-3 px-4">{agent.requests24h}</td>
                  <td className="py-3 px-4 font-bold text-cyan-400">{agent.latency}</td>
                  <td className="py-3 px-4 text-emerald-400">{agent.errorRate}</td>
                  <td className="py-3 px-4 text-right"><Badge variant="success">{agent.status}</Badge></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Live Logs Terminal Preview */}
      <Card variant="glow" className="p-6 space-y-3">
        <div className="flex justify-between items-center">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Terminal className="w-4 h-4 text-indigo-400" />
            Live Swarm Execution Logs (Enkrypt Audited)
          </h3>
          <span className="text-xs text-emerald-400 font-mono animate-pulse">● Live Stream Active</span>
        </div>
        <div className="p-4 rounded-xl bg-obsidian-950 border border-white/10 font-mono text-xs text-slate-300 space-y-1.5 h-48 overflow-y-auto">
          <p className="text-slate-500">[2026-07-06 02:12:10 UTC] INFO: Mastra Router dispatching user query #8892 to Tutor AI Swarm.</p>
          <p className="text-emerald-400">[2026-07-06 02:12:11 UTC] OK: Enkrypt Layer 6 pre-execution safety check passed (Score: 1.00).</p>
          <p className="text-cyan-400">[2026-07-06 02:12:11 UTC] QDRANT: HNSW similarity search retrieved top-3 syllabus chunks in 12ms.</p>
          <p className="text-slate-300">[2026-07-06 02:12:12 UTC] SUCCESS: Socratic response generated. Token count: 184 prompt, 92 completion.</p>
          <p className="text-indigo-400">[2026-07-06 02:12:15 UTC] MUTATE: Student Digital Twin vector embedding #010 updated in Qdrant.</p>
        </div>
      </Card>
    </div>
  );
};
