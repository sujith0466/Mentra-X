import React, { useState, useEffect } from "react";
import { Trophy, Medal, Award, Flame, GitPullRequest, Search } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Input } from "@/components/ui/Input";
import { useAuthStore } from "@/store/useAuthStore";
import { useCommunityStore, StudentRank } from "@/store/useCommunityStore";
import { motion } from "framer-motion";

export const LeaderboardPage: React.FC = () => {
  const { user } = useAuthStore();
  const { leaderboard, updateLeaderboardWithUser } = useCommunityStore();
  const [filter, setFilter] = useState<"global" | "campus" | "streak">("global");
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    if (user && user.role === "student") {
      updateLeaderboardWithUser(`${user.name} (You)`, "Enterprise University", 120, 1);
    }
  }, [user, updateLeaderboardWithUser]);

  const filtered = leaderboard.filter((item) =>
    item.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.campus.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.badge.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Podium medal config
  const podiumConfig = [
    {
      medal: Trophy,
      iconColor: "text-amber-400",
      ringColor: "ring-amber-400/40",
      bgGradient: "from-amber-500/10 via-yellow-400/5 to-transparent",
      label: "🥇 Gold",
    },
    {
      medal: Medal,
      iconColor: "text-slate-400 dark:text-slate-300",
      ringColor: "ring-slate-400/30",
      bgGradient: "from-slate-400/10 via-slate-300/5 to-transparent",
      label: "🥈 Silver",
    },
    {
      medal: Award,
      iconColor: "text-amber-600",
      ringColor: "ring-amber-700/30",
      bgGradient: "from-amber-700/10 via-orange-600/5 to-transparent",
      label: "🥉 Bronze",
    },
  ] as const;

  // Rank badge for table rows
  const rankBadge = (rank: number) => {
    if (rank === 1) return <span className="text-base">🥇</span>;
    if (rank === 2) return <span className="text-base">🥈</span>;
    if (rank === 3) return <span className="text-base">🥉</span>;
    return (
      <span className="text-xs font-bold text-slate-500 dark:text-slate-400 w-6 text-center">
        #{rank}
      </span>
    );
  };

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <motion.div
        className="border-b border-slate-200 dark:border-white/10 pb-6"
        initial={{ opacity: 0, y: -12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <Badge variant="warning" className="mb-3">
          <Trophy className="w-3.5 h-3.5 mr-1.5 inline text-amber-500" />
          Live Rankings
        </Badge>
        <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white">
          Academic XP Leaderboard
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
          Ranked by coding challenges, study streaks, and course completions.
        </p>
      </motion.div>

      {/* Top 3 Podium Cards */}
      {leaderboard.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
          {leaderboard.slice(0, 3).map((item, idx) => {
            const cfg = podiumConfig[idx];
            const MedalIcon = cfg.medal;
            return (
              <motion.div
                key={item.rank}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: idx * 0.08 }}
              >
                <Card
                  variant={idx === 0 ? "glow" : "default"}
                  className={`p-6 text-center space-y-4 relative overflow-hidden ring-1 ${cfg.ringColor} hover:-translate-y-0.5 hover:shadow-lg transition-all duration-200`}
                >
                  {/* Background gradient accent */}
                  <div className={`absolute inset-0 bg-gradient-to-b ${cfg.bgGradient} pointer-events-none`} />

                  <div className="relative flex justify-between items-center">
                    <Badge
                      variant={idx === 0 ? "warning" : "default"}
                      className="text-[10px] font-bold px-2 py-1"
                    >
                      {cfg.label}
                    </Badge>
                    <MedalIcon className={`w-6 h-6 ${cfg.iconColor}`} />
                  </div>

                  <div className="relative space-y-0.5">
                    <h3 className="text-base font-bold text-slate-900 dark:text-white leading-snug">
                      {item.name}
                    </h3>
                    <p className="text-xs text-indigo-500 dark:text-indigo-300 font-semibold">
                      {item.campus}
                    </p>
                    <p className="text-[10px] text-slate-400">{item.level}</p>
                  </div>

                  <div className="relative pt-3 border-t border-slate-200 dark:border-white/10 flex justify-around text-xs">
                    <div>
                      <span className="block font-extrabold text-slate-900 dark:text-white text-sm">
                        {item.xp.toLocaleString()}
                      </span>
                      <span className="text-[10px] text-slate-400">Total XP</span>
                    </div>
                    <div>
                      <span className="flex items-center justify-center gap-1 font-extrabold text-cyan-500 dark:text-cyan-400 text-sm">
                        <Flame className="w-3.5 h-3.5 text-orange-400" />
                        {item.streakDays}d
                      </span>
                      <span className="text-[10px] text-slate-400">Streak</span>
                    </div>
                  </div>
                </Card>
              </motion.div>
            );
          })}
        </div>
      )}

      {/* Filters & Search */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
          <Input
            placeholder="Search student or campus…"
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
              className={`px-4 py-2 rounded-lg text-xs font-bold transition-all duration-150 ${
                filter === tab.id
                  ? "bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-md shadow-indigo-500/20"
                  : "bg-white dark:bg-obsidian-800 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white border border-slate-200 dark:border-white/10 hover:border-slate-300 dark:hover:border-white/20"
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
              <tr className="border-b border-slate-200 dark:border-white/10 text-xs font-semibold uppercase tracking-wider text-slate-400 bg-slate-50 dark:bg-obsidian-900/60">
                <th className="py-3.5 px-6">Rank</th>
                <th className="py-3.5 px-6">Student &amp; Campus</th>
                <th className="py-3.5 px-6">Level</th>
                <th className="py-3.5 px-6">Streak</th>
                <th className="py-3.5 px-6">Code PRs</th>
                <th className="py-3.5 px-6 text-right">Total XP</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-white/5 text-sm">
              {filtered.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-14 px-6 text-center">
                    <div className="flex flex-col items-center gap-3">
                      <Trophy className="w-10 h-10 text-slate-300 dark:text-slate-600" />
                      <p className="text-slate-500 dark:text-slate-400 font-medium">
                        No results found. Complete lessons to appear on the leaderboard!
                      </p>
                    </div>
                  </td>
                </tr>
              ) : (
                filtered.map((item, index) => {
                  const isUser = item.name.includes("(You)");
                  return (
                    <motion.tr
                      key={item.rank}
                      initial={{ opacity: 0, x: -8 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.3, delay: index * 0.04 }}
                      className={`group transition-colors duration-150 ${
                        isUser
                          ? "bg-indigo-50 dark:bg-indigo-600/10 hover:bg-indigo-100 dark:hover:bg-indigo-600/20"
                          : "hover:bg-slate-50 dark:hover:bg-white/5"
                      }`}
                    >
                      <td className="py-4 px-6">
                        <div className="flex items-center gap-2">
                          {rankBadge(item.rank)}
                        </div>
                      </td>
                      <td className="py-4 px-6">
                        <div className="font-bold text-slate-900 dark:text-white flex items-center gap-2">
                          <span>{item.name}</span>
                          {isUser && (
                            <Badge variant="info" className="text-[10px] py-0">
                              You
                            </Badge>
                          )}
                        </div>
                        <span className="text-xs text-slate-400">
                          {item.campus} &bull; {item.badge}
                        </span>
                      </td>
                      <td className="py-4 px-6">
                        <span className="text-xs font-semibold text-indigo-500 dark:text-indigo-300 bg-indigo-50 dark:bg-indigo-500/10 px-2 py-0.5 rounded-full">
                          {item.level}
                        </span>
                      </td>
                      <td className="py-4 px-6">
                        <span className="inline-flex items-center gap-1.5 font-bold text-cyan-600 dark:text-cyan-400">
                          <Flame className="w-3.5 h-3.5 text-orange-400" />
                          {item.streakDays} days
                        </span>
                      </td>
                      <td className="py-4 px-6 text-xs text-slate-600 dark:text-slate-300 font-mono">
                        <span className="inline-flex items-center gap-1">
                          <GitPullRequest className="w-3.5 h-3.5 text-emerald-400" />
                          {item.prCount} PRs
                        </span>
                      </td>
                      <td className="py-4 px-6 text-right">
                        <span className="font-extrabold text-slate-900 dark:text-white text-base tabular-nums">
                          {item.xp.toLocaleString()}
                        </span>
                        <span className="text-xs text-slate-400 ml-1">XP</span>
                      </td>
                    </motion.tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};