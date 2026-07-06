import React, { useState } from "react";
import { Award, Trophy, Medal, Sparkles, Flame, GitPullRequest, Search, ShieldCheck } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Input } from "@/components/ui/Input";
import { useAuthStore } from "@/store/useAuthStore";

interface StudentRank {
  rank: number;
  name: name;
  campus: string;
  level: string;
  xp: number;
  streakDays: number;
  prCount: number;
  badge: string;
}

type name = string;

export const LeaderboardPage: React.FC = () => {
  const { user } = useAuthStore();
  const [filter, setFilter] = useState<"global" | "campus" | "streak">("global");
  const [searchQuery, setSearchQuery] = useState("");

  const leaderboard: StudentRank[] = [
    { rank: 1, name: "Marcus Vance", campus: "MIT AI Lab", level: "Level 10 Master", xp: 48500, streakDays: 142, prCount: 34, badge: "Grand Architect" },
    { rank: 2, name: "Elena Rostova", campus: "Stanford CS Campus", level: "Level 9 Architect", xp: 44200, streakDays: 98, prCount: 28, badge: "Vector Pioneer" },
    { rank: 3, name: "David Kim", campus: "UC Berkeley Tech", level: "Level 9 Architect", xp: 41150, streakDays: 115, prCount: 22, badge: "AI Specialist" },
    { rank: 4, name: `${user?.name || "Sujith Kumar"} (You)`, campus: "Campus Enterprise", level: "Level 8 Scholar", xp: 38900, streakDays: 64, prCount: 18, badge: "DNA Seeder" },
    { rank: 5, name: "Aria Montgomery", campus: "Oxford AI Institute", level: "Level 8 Scholar", xp: 35400, streakDays: 72, prCount: 15, badge: "Safety Audited" },
    { rank: 6, name: "Kenji Sato", campus: "Tokyo Tech AI", level: "Level 7 Scholar", xp: 31200, streakDays: 45, prCount: 12, badge: "Full-Stack Dev" },
    { rank: 7, name: "Sarah Jenkins", campus: "Georgia Tech", level: "Level 6 Student", xp: 27800, streakDays: 31, prCount: 9, badge: "Code Arena Pro" },
  ];

  const filtered = leaderboard.filter((item) =>
    item.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.campus.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.badge.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-6">
        <div>
          <Badge variant="info" className="mb-2">
            <Trophy className="w-3.5 h-3.5 mr-1.5 inline text-indigo-400" />
            Global Student Telemetry Rankings
          </Badge>
          <h1 className="text-3xl font-extrabold text-white">Academic XP Leaderboard</h1>
          <p className="text-sm text-slate-400">Ranked by vector memory mastery velocity, coding arena submissions, and study streaks.</p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" className="px-3 py-1.5">
            <ShieldCheck className="w-4 h-4 mr-1.5 inline" />
            Safety Verified Telemetry
          </Badge>
        </div>
      </div>

      {/* Top 3 Podium Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
        {leaderboard.slice(0, 3).map((item, idx) => {
          const variants = ["glow", "gradient", "default"] as const;
          const medals = [Trophy, Medal, Award];
          const MedalIcon = medals[idx];
          const colors = ["text-amber-400", "text-slate-300", "text-amber-600"];
          return (
            <Card key={item.rank} variant={variants[idx]} className="p-6 text-center space-y-4 relative overflow-hidden">
              <div className="flex justify-between items-center">
                <Badge variant="default" className="text-xs">Rank #{item.rank}</Badge>
                <MedalIcon className={`w-6 h-6 ${colors[idx]}`} />
              </div>
              <div className="space-y-1">
                <h3 className="text-lg font-bold text-white">{item.name}</h3>
                <p className="text-xs text-indigo-300 font-semibold">{item.campus}</p>
                <p className="text-[10px] text-slate-400">{item.level}</p>
              </div>
              <div className="pt-2 border-t border-white/10 flex justify-around text-xs">
                <div>
                  <span className="block font-extrabold text-white">{item.xp.toLocaleString()}</span>
                  <span className="text-[10px] text-slate-400">Total XP</span>
                </div>
                <div>
                  <span className="block font-extrabold text-cyan-400 flex items-center justify-center gap-1">
                    <Flame className="w-3 h-3 text-red-400" />
                    {item.streakDays}d
                  </span>
                  <span className="text-[10px] text-slate-400">Streak</span>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Filters & Search */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
          <Input
            placeholder="Search scholar or campus..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 w-full"
          />
        </div>

        <div className="flex gap-2 w-full sm:w-auto justify-end">
          {[
            { id: "global", label: "Global Campus" },
            { id: "campus", label: "My University" },
            { id: "streak", label: "Top Streaks" },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setFilter(tab.id as any)}
              className={`px-4 py-2 rounded-lg text-xs font-bold transition-all ${
                filter === tab.id
                  ? "bg-gradient-to-r from-indigo-600 to-cyan-600 text-white shadow-md shadow-indigo-500/20"
                  : "bg-obsidian-800/60 text-slate-400 hover:text-white border border-white/5"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Table Rankings */}
      <Card variant="default" className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-white/10 text-xs font-semibold uppercase tracking-wider text-slate-400 bg-obsidian-900/50">
                <th className="py-4 px-6">Rank</th>
                <th className="py-4 px-6">Student & Campus</th>
                <th className="py-4 px-6">Mastery Level</th>
                <th className="py-4 px-6">Study Streak</th>
                <th className="py-4 px-6">Code PRs</th>
                <th className="py-4 px-6 text-right">Total XP</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 text-sm">
              {filtered.map((item) => {
                const isUser = item.name.includes("(You)");
                return (
                  <tr
                    key={item.rank}
                    className={`transition-colors ${isUser ? "bg-indigo-600/10 hover:bg-indigo-600/20" : "hover:bg-white/5"}`}
                  >
                    <td className="py-4 px-6 font-bold text-white flex items-center gap-2">
                      <span>#{item.rank}</span>
                      {item.rank <= 3 && <Trophy className="w-3.5 h-3.5 text-amber-400" />}
                    </td>
                    <td className="py-4 px-6">
                      <div className="font-bold text-white flex items-center gap-2">
                        <span>{item.name}</span>
                        {isUser && <Badge variant="info" className="text-[10px]">You</Badge>}
                      </div>
                      <span className="text-xs text-slate-400">{item.campus} &bull; {item.badge}</span>
                    </td>
                    <td className="py-4 px-6 text-xs font-semibold text-indigo-300">{item.level}</td>
                    <td className="py-4 px-6 font-bold text-cyan-400 flex items-center gap-1.5 pt-5">
                      <Flame className="w-3.5 h-3.5 text-red-400" />
                      {item.streakDays} days
                    </td>
                    <td className="py-4 px-6 text-xs text-slate-300 font-mono">
                      <span className="inline-flex items-center gap-1">
                        <GitPullRequest className="w-3.5 h-3.5 text-emerald-400" />
                        {item.prCount} PRs
                      </span>
                    </td>
                    <td className="py-4 px-6 text-right font-extrabold text-white text-base">
                      {item.xp.toLocaleString()} XP
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
