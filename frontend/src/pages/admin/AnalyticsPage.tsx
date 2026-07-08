import React, { useState } from "react";
import { BarChart3, Users, BookOpen, TrendingUp, DollarSign, ArrowUpRight, ArrowDownRight, Filter, Download } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { MetricCard } from "@/components/widgets/MetricCard";
import { ChartComponent } from "@/components/widgets/ChartComponent";

export const AnalyticsPage: React.FC = () => {
  const [timeRange, setTimeRange] = useState<"7d" | "30d" | "90d" | "1y">("30d");

  const enrollmentData = [
    { label: "Week 1", value: 1200 },
    { label: "Week 2", value: 1850 },
    { label: "Week 3", value: 2400 },
    { label: "Week 4", value: 3100 },
  ];

  const domainData = [
    { label: "AI & Neural Networks", value: 42 },
    { label: "Full-Stack Enterprise", value: 28 },
    { label: "Database Systems", value: 18 },
    { label: "Cybersecurity & AI Safety", value: 12 },
  ];

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-white/10 pb-6">
        <div>
          <Badge variant="cyan" className="mb-2">
            <BarChart3 className="w-3.5 h-3.5 mr-1.5 inline text-indigo-400" />
            Executive Intelligence Console
          </Badge>
          <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white">Platform Analytics & Telemetry</h1>
          <p className="text-sm text-slate-400">Real-time student retention, course completion velocity, and institutional growth metrics.</p>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex bg-slate-50 dark:bg-obsidian-900 rounded-lg p-1 border border-slate-200 dark:border-white/10">
            {(["7d", "30d", "90d", "1y"] as const).map((range) => (
              <button
                key={range}
                onClick={() => setTimeRange(range)}
                className={`px-3 py-1 rounded-md text-xs font-bold transition-all ${
                  timeRange === range ? "bg-indigo-600 text-slate-900 dark:text-white shadow-sm" : "text-slate-400 hover:text-slate-900 dark:text-white"
                }`}
              >
                {range.toUpperCase()}
              </button>
            ))}
          </div>
          <Button variant="secondary" onClick={() => alert("Exporting executive CSV report...")} className="text-xs py-2">
            <Download className="w-3.5 h-3.5 mr-1.5" />
            Export CSV
          </Button>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Total Campus Enrollments"
          value="14,892"
          trend={18.4}
          trendLabel="vs last month"
          icon="users"
        />
        <MetricCard
          title="Course Completion Rate"
          value="84.2%"
          trend={4.1}
          trendLabel="ESDLC benchmark"
          icon="activity"
        />
        <MetricCard
          title="Database Vector Syncs"
          value="1.42M"
          trend={0.5}
          trendLabel="12ms avg latency"
          icon="zap"
        />
        <MetricCard
          title="Institutional Retention"
          value="96.8%"
          trend={0.2}
          trendLabel="low churn rate"
          icon="shield"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-stretch">
        <div className="lg:col-span-2">
          <ChartComponent
            title="Student Enrollment Growth Velocity"
            data={enrollmentData}
            type="bar"
          />
        </div>
        <div>
          <ChartComponent
            title="Enrollment by Academic Domain (%)"
            data={domainData}
            type="progress"
          />
        </div>
      </div>

      {/* Detailed Domain Breakdown Table */}
      <Card variant="default" className="p-6 space-y-4">
        <h3 className="text-lg font-bold text-slate-900 dark:text-white">Top Performing Academic Modules</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-sm">
            <thead>
              <tr className="border-b border-slate-200 dark:border-white/10 text-xs font-semibold uppercase tracking-wider text-slate-400">
                <th className="py-3 px-4">Course Module Name</th>
                <th className="py-3 px-4">Enrolled Students</th>
                <th className="py-3 px-4">Avg Mastery Score</th>
                <th className="py-3 px-4">AI Tutor Assistance</th>
                <th className="py-3 px-4 text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 text-slate-600 dark:text-slate-300">
              <tr>
                <td className="py-3 px-4 font-bold text-slate-900 dark:text-white">CS-401: Advanced Neural Architectures</td>
                <td className="py-3 px-4">4,210</td>
                <td className="py-3 px-4 font-bold text-cyan-400">91.4%</td>
                <td className="py-3 px-4">14.2 queries / student</td>
                <td className="py-3 px-4 text-right"><Badge variant="success">Optimal</Badge></td>
              </tr>
              <tr>
                <td className="py-3 px-4 font-bold text-slate-900 dark:text-white">CS-305: Enterprise Database Systems</td>
                <td className="py-3 px-4">3,890</td>
                <td className="py-3 px-4 font-bold text-indigo-400">88.7%</td>
                <td className="py-3 px-4">18.5 queries / student</td>
                <td className="py-3 px-4 text-right"><Badge variant="success">Optimal</Badge></td>
              </tr>
              <tr>
                <td className="py-3 px-4 font-bold text-slate-900 dark:text-white">SEC-502: AI Safety & Governance</td>
                <td className="py-3 px-4">2,950</td>
                <td className="py-3 px-4 font-bold text-emerald-400">94.1%</td>
                <td className="py-3 px-4">8.1 queries / student</td>
                <td className="py-3 px-4 text-right"><Badge variant="info">High Retention</Badge></td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
