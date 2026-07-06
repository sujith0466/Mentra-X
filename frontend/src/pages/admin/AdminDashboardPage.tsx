import React from "react";
import { Link } from "react-router-dom";
import { Server, Activity, Users, BookOpen, ShieldAlert, Zap, Cpu, RefreshCw } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { MetricCard } from "@/components/widgets/MetricCard";
import { ChartComponent } from "@/components/widgets/ChartComponent";
import { ActivityFeed } from "@/components/widgets/ActivityFeed";
import { SafetyBadge } from "@/components/widgets/SafetyBadge";

export const AdminDashboardPage: React.FC = () => {
  const chartData = [
    { label: "Mastra Swarm Agent Queries", value: 4250, color: "from-primary-600 to-indigo-400" },
    { label: "Qdrant Vector Embeddings Indexed", value: 3890, color: "from-ai-violet to-purple-500" },
    { label: "Enkrypt Safety Intercepts", value: 142, color: "from-emerald-500 to-teal-400" },
    { label: "Active Student Digital Twins", value: 1240, color: "from-cyan-500 to-blue-400" },
  ];

  const liveActivities = [
    { id: 1, user: "Sujith Kumar", action: "Submitted solution for Challenge #4 (Qdrant Tool)", timestamp: "2m ago", type: "ai" as const },
    { id: 2, user: "Enkrypt Layer 6", action: "Intercepted out-of-scope prompt on Course #cs-202", timestamp: "5m ago", type: "security" as const },
    { id: 3, user: "Elena Rostova", action: "Enrolled in Advanced Agentic Coding & Orchestration", timestamp: "12m ago", type: "normal" as const },
    { id: 4, user: "Mastra Swarm #8", action: "Completed nightly graph compaction for 1,240 Digital Twins", timestamp: "1h ago", type: "ai" as const },
  ];

  return (
    <div className="space-y-8 py-4">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-obsidian-600 pb-6">
        <div>
          <div className="flex items-center space-x-2">
            <Badge variant="danger" size="sm">Admin Portal</Badge>
            <Badge variant="cyan" size="sm">Live Telemetry</Badge>
          </div>
          <h1 className="text-3xl font-extrabold text-white mt-1">AI Operations & Cluster Monitor</h1>
          <p className="text-sm text-slate-400 mt-0.5">Real-time enterprise metrics across Mastra swarms, Qdrant memory, and Enkrypt safety layers.</p>
        </div>
        <div className="flex items-center space-x-3">
          <Link to="/admin/audit-logs">
            <Button size="md" variant="outline" leftIcon={<ShieldAlert className="w-4 h-4 text-rose-400" />}>
              Security Audit Logs
            </Button>
          </Link>
          <Button size="md" leftIcon={<RefreshCw className="w-4 h-4" />}>
            Refresh Telemetry
          </Button>
        </div>
      </div>

      {/* KPI Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard title="Total Students" value="1,240" trend={8.4} icon={<Users className="w-5 h-5" />} subtitle="Active Digital Twins" />
        <MetricCard title="AI Swarm QPS" value="142.8" trend={15.2} icon={<Cpu className="w-5 h-5" />} subtitle="Queries per second" />
        <MetricCard title="Enkrypt Accuracy" value="99.98%" trend={0.01} icon={<ShieldAlert className="w-5 h-5" />} subtitle="Zero hallucination rate" />
        <MetricCard title="Qdrant Latency" value="12.4ms" trend={-4.5} trendLabel="faster" icon={<Server className="w-5 h-5" />} subtitle="P99 vector search" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <ChartComponent
            title="Daily AI System Workload Distribution"
            data={chartData}
            type="progress"
          />

          <Card variant="default" className="p-6 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-obsidian-600">
              <h3 className="font-bold text-base text-white flex items-center gap-2">
                <Server className="w-5 h-5 text-indigo-400" /> Infrastructure Node Status
              </h3>
              <Badge variant="success">All Systems Operational</Badge>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              <div className="p-3.5 rounded-xl bg-obsidian-900 border border-obsidian-600 space-y-1">
                <span className="text-slate-400 block font-semibold">Mastra Orchestrator Pods</span>
                <span className="text-base font-bold text-emerald-400">12 / 12 Ready</span>
                <span className="text-[10px] text-slate-500 block">CPU: 42% • RAM: 3.8GB</span>
              </div>
              <div className="p-3.5 rounded-xl bg-obsidian-900 border border-obsidian-600 space-y-1">
                <span className="text-slate-400 block font-semibold">Qdrant Vector Cluster</span>
                <span className="text-base font-bold text-emerald-400">3 Nodes Synced</span>
                <span className="text-[10px] text-slate-500 block">Storage: 48.2GB / 500GB</span>
              </div>
              <div className="p-3.5 rounded-xl bg-obsidian-900 border border-obsidian-600 space-y-1">
                <span className="text-slate-400 block font-semibold">Enkrypt Proxy Gateway</span>
                <span className="text-base font-bold text-cyan-400">Layer 6 Active</span>
                <span className="text-[10px] text-slate-500 block">Throughput: 1.2 GB/s</span>
              </div>
            </div>
          </Card>
        </div>

        <div className="space-y-6">
          <ActivityFeed items={liveActivities} title="Enterprise Live Feed" />
        </div>
      </div>
    </div>
  );
};
