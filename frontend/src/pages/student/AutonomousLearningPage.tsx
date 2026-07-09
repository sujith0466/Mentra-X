import React, { useState, useEffect } from "react";
import {
  Sparkles,
  CheckCircle2,
  Clock,
  Flame,
  Award,
  TrendingUp,
  BookOpen,
  Calendar,
  AlertCircle,
  RefreshCw,
  Zap,
  ArrowRight
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Link } from "react-router-dom";

interface MissionTask {
  task_id: string;
  title: string;
  category: string;
  concept: string;
  duration_mins: number;
  xp_reward: number;
  completed: boolean;
  action_url: string;
}

interface RevisionItem {
  concept: string;
  domain: string;
  days_since_last_review: number;
  recommended_interval_days: number;
  retention_estimate: number;
  urgency: "CRITICAL" | "OVERDUE" | "SCHEDULED" | "UPCOMING";
}

interface InterventionAlert {
  intervention_id: string;
  title: string;
  message: string;
  suggested_action: string;
  action_route: string;
  severity: "ACTION_REQUIRED" | "WARNING" | "NOTICE" | "INFO";
}

export const AutonomousLearningPage: React.FC = () => {
  const [tasks, setTasks] = useState<MissionTask[]>([
    {
      task_id: "m-101",
      title: "Remediate Weakness: Dynamic Programming Subproblems",
      category: "REMEDIATION",
      concept: "Dynamic Programming",
      duration_mins: 25,
      xp_reward: 100,
      completed: false,
      action_url: "/student/weakness-intelligence"
    },
    {
      task_id: "m-102",
      title: "Spaced Reinforcement: Graph Shortest Paths (Dijkstra)",
      category: "REVISION",
      concept: "Graph Algorithms",
      duration_mins: 20,
      xp_reward: 60,
      completed: false,
      action_url: "/student/notes"
    },
    {
      task_id: "m-103",
      title: "Active Challenge: Timed Interview Simulation #4",
      category: "PROBLEM_SOLVING",
      concept: "Algorithms & Complexity",
      duration_mins: 35,
      xp_reward: 100,
      completed: false,
      action_url: "/student/coding-arena"
    },
    {
      task_id: "m-104",
      title: "Syllabus Progression: Attention Mechanisms in ML",
      category: "NEW_CONCEPT",
      concept: "Deep Learning",
      duration_mins: 40,
      xp_reward: 60,
      completed: false,
      action_url: "/student/my-courses"
    }
  ]);

  const [revisions] = useState<RevisionItem[]>([
    {
      concept: "Recursion & Memoization Patterns",
      domain: "Computer Science",
      days_since_last_review: 4,
      recommended_interval_days: 3,
      retention_estimate: 0.54,
      urgency: "CRITICAL"
    },
    {
      concept: "SQL Index Optimization & Joins",
      domain: "Database Systems",
      days_since_last_review: 3,
      recommended_interval_days: 3,
      retention_estimate: 0.68,
      urgency: "OVERDUE"
    },
    {
      concept: "Transformer Self-Attention",
      domain: "Artificial Intelligence",
      days_since_last_review: 5,
      recommended_interval_days: 7,
      retention_estimate: 0.82,
      urgency: "SCHEDULED"
    }
  ]);

  const [interventions] = useState<InterventionAlert[]>([
    {
      intervention_id: "inv-1",
      title: "Proactive AI Guidance: Dynamic Programming Focus",
      message:
        "You're experiencing slight retention decay in Dynamic Programming subproblems. Let's spend 25 minutes today reinforcing state transitions before moving to graphs.",
      suggested_action: "Start AI Tutoring Remediation",
      action_route: "/student/weakness-intelligence",
      severity: "ACTION_REQUIRED"
    },
    {
      intervention_id: "inv-2",
      title: "Placement Readiness Milestone On Track",
      message:
        "Your technical problem-solving consistency is in the top 15% of your cohort. Keep your 7-day study streak active.",
      suggested_action: "Enter Challenge Arena",
      action_route: "/student/coding-arena",
      severity: "NOTICE"
    }
  ]);

  const [loading, setLoading] = useState(false);
  const [habitScore] = useState(88.5);
  const [streakDays] = useState(7);

  const toggleTaskComplete = (taskId: string) => {
    setTasks((prev) =>
      prev.map((t) => (t.task_id === taskId ? { ...t, completed: !t.completed } : t))
    );
  };

  const completedCount = tasks.filter((t) => t.completed).length;
  const progressPercent = Math.round((completedCount / tasks.length) * 100);

  useEffect(() => {
    // Attempt to fetch live autonomous overview if backend API is connected
    const fetchOverview = async () => {
      try {
        setLoading(true);
        const res = await fetch("/api/v1/autonomous/overview");
        if (res.ok) {
          const json = await res.json();
          if (json?.data?.daily_mission?.daily_tasks) {
            setTasks(json.data.daily_mission.daily_tasks);
          }
        }
      } catch {
        // Fallback silently to initial rich demo student state
      } finally {
        setLoading(false);
      }
    };
    fetchOverview();
  }, []);

  return (
    <div className="space-y-8 py-6">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 dark:border-obsidian-600 pb-6">
        <div>
          <div className="flex items-center space-x-2">
            <Badge variant="cyan" size="sm">
              <Sparkles className="w-3.5 h-3.5 mr-1 text-indigo-500 dark:text-indigo-400" />
              Proactive AI Companion
            </Badge>
            <Badge variant="success" size="sm">
              <Flame className="w-3.5 h-3.5 mr-1 text-amber-500" />
              {streakDays} Day Study Streak
            </Badge>
          </div>
          <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white mt-2">
            Autonomous Learning Companion
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1 max-w-2xl">
            Your personal AI mentor continuously analyzes your learning profile, schedules spaced
            revisions, and orchestrates optimal daily study missions.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center px-4 py-2 rounded-xl bg-indigo-500/10 border border-indigo-500/20">
            <Award className="w-5 h-5 text-indigo-600 dark:text-indigo-400 mr-2" />
            <div>
              <div className="text-[10px] font-semibold uppercase tracking-wider text-slate-400">
                Habit Index
              </div>
              <div className="text-sm font-bold text-slate-900 dark:text-white">
                {habitScore} / 100
              </div>
            </div>
          </div>

          <Button
            size="md"
            variant="outline"
            leftIcon={<RefreshCw className="w-4 h-4" />}
            onClick={() => window.location.reload()}
          >
            Rebalance Schedule
          </Button>
        </div>
      </div>

      {/* Top Section: Proactive AI Mentor Feed & Predictive Readiness */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Mentor Interventions Feed (2 cols) */}
        <Card className="lg:col-span-2 p-6 bg-gradient-to-br from-indigo-500/5 via-transparent to-purple-500/5 border-indigo-500/20">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 rounded-lg bg-indigo-500/20 flex items-center justify-center">
                <Sparkles className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
              </div>
              <h2 className="text-lg font-bold text-slate-900 dark:text-white">
                Proactive AI Mentor Feed
              </h2>
            </div>
            <Badge variant="purple" size="sm">
              Live Mentorship
            </Badge>
          </div>

          <div className="space-y-4">
            {interventions.map((item) => (
              <div
                key={item.intervention_id}
                className="p-4 rounded-xl bg-white dark:bg-obsidian-900/80 border border-slate-200 dark:border-obsidian-600 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4"
              >
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    <AlertCircle
                      className={`w-4 h-4 ${
                        item.severity === "ACTION_REQUIRED"
                          ? "text-rose-500"
                          : "text-amber-500"
                      }`}
                    />
                    <span className="font-semibold text-slate-900 dark:text-white text-sm">
                      {item.title}
                    </span>
                  </div>
                  <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                    {item.message}
                  </p>
                </div>

                <Link to={item.action_route} className="shrink-0">
                  <Button size="sm" rightIcon={<ArrowRight className="w-3.5 h-3.5" />}>
                    {item.suggested_action}
                  </Button>
                </Link>
              </div>
            ))}
          </div>
        </Card>

        {/* Predictive Success Radar Card */}
        <Card className="p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-slate-900 dark:text-white flex items-center">
                <TrendingUp className="w-5 h-5 text-emerald-500 mr-2" />
                Predicted Success
              </h3>
              <Badge variant="success" size="sm">
                AI Forecast
              </Badge>
            </div>

            <div className="space-y-4 my-4">
              <div>
                <div className="flex justify-between text-xs font-semibold mb-1">
                  <span className="text-slate-600 dark:text-slate-300">
                    Course Mastery Probability
                  </span>
                  <span className="text-emerald-600 dark:text-emerald-400">98.5%</span>
                </div>
                <div className="w-full bg-slate-200 dark:bg-obsidian-700 h-2 rounded-full overflow-hidden">
                  <div
                    className="bg-gradient-to-r from-emerald-500 to-teal-400 h-full rounded-full"
                    style={{ width: "98.5%" }}
                  />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs font-semibold mb-1">
                  <span className="text-slate-600 dark:text-slate-300">
                    Technical Placement Readiness
                  </span>
                  <span className="text-indigo-600 dark:text-indigo-400">94.0%</span>
                </div>
                <div className="w-full bg-slate-200 dark:bg-obsidian-700 h-2 rounded-full overflow-hidden">
                  <div
                    className="bg-gradient-to-r from-indigo-500 to-purple-400 h-full rounded-full"
                    style={{ width: "94%" }}
                  />
                </div>
              </div>

              <div>
                <div className="flex justify-between text-xs font-semibold mb-1">
                  <span className="text-slate-600 dark:text-slate-300">
                    Exam Confidence Index
                  </span>
                  <span className="text-cyan-600 dark:text-cyan-400">96.0%</span>
                </div>
                <div className="w-full bg-slate-200 dark:bg-obsidian-700 h-2 rounded-full overflow-hidden">
                  <div
                    className="bg-gradient-to-r from-cyan-500 to-blue-400 h-full rounded-full"
                    style={{ width: "96%" }}
                  />
                </div>
              </div>
            </div>
          </div>

          <p className="text-[11px] text-slate-400 dark:text-slate-500 pt-2 border-t border-slate-200 dark:border-obsidian-600">
            Based on your real-time quiz retention, coding arena speed, and spaced repetition metrics.
          </p>
        </Card>
      </div>

      {/* Middle Section: Daily AI Mission & Spaced Repetition Queue */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Today's AI Mission Checklist */}
        <Card className="p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-lg font-bold text-slate-900 dark:text-white flex items-center">
                <Zap className="w-5 h-5 text-amber-500 mr-2" />
                Today&apos;s Proactive Study Mission
              </h2>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                Targeted daily goals curated by your autonomous learning brain.
              </p>
            </div>
            <Badge variant="cyan" size="sm">
              {completedCount} / {tasks.length} Completed
            </Badge>
          </div>

          {/* Progress bar */}
          <div className="mb-6">
            <div className="w-full bg-slate-200 dark:bg-obsidian-700 h-2.5 rounded-full overflow-hidden">
              <div
                className="bg-gradient-to-r from-primary-500 to-indigo-500 h-full rounded-full transition-all duration-300"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </div>

          <div className="space-y-3">
            {tasks.map((task) => (
              <div
                key={task.task_id}
                className={`p-4 rounded-xl border transition-all flex items-center justify-between ${
                  task.completed
                    ? "bg-slate-50 dark:bg-obsidian-900/40 border-slate-200 dark:border-obsidian-600 opacity-75"
                    : "bg-white dark:bg-obsidian-800 border-slate-200 dark:border-obsidian-600 shadow-sm"
                }`}
              >
                <div className="flex items-center space-x-3.5">
                  <button
                    onClick={() => toggleTaskComplete(task.task_id)}
                    className={`w-6 h-6 rounded-full flex items-center justify-center border transition-colors ${
                      task.completed
                        ? "bg-emerald-500 border-emerald-500 text-white"
                        : "border-slate-300 dark:border-slate-600 hover:border-indigo-500"
                    }`}
                  >
                    {task.completed && <CheckCircle2 className="w-4 h-4" />}
                  </button>
                  <div>
                    <span
                      className={`text-sm font-semibold block ${
                        task.completed
                          ? "line-through text-slate-400 dark:text-slate-500"
                          : "text-slate-900 dark:text-white"
                      }`}
                    >
                      {task.title}
                    </span>
                    <div className="flex items-center space-x-3 text-xs text-slate-500 dark:text-slate-400 mt-1">
                      <span className="inline-flex items-center">
                        <Clock className="w-3 h-3 mr-1" />
                        {task.duration_mins} mins
                      </span>
                      <span>•</span>
                      <span className="text-amber-600 dark:text-amber-400 font-medium">
                        +{task.xp_reward} XP
                      </span>
                    </div>
                  </div>
                </div>

                <Link to={task.action_url}>
                  <Button size="sm" variant="outline">
                    Launch
                  </Button>
                </Link>
              </div>
            ))}
          </div>
        </Card>

        {/* Spaced Repetition Revision Queue */}
        <Card className="p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-lg font-bold text-slate-900 dark:text-white flex items-center">
                <BookOpen className="w-5 h-5 text-indigo-500 mr-2" />
                Spaced Repetition Revision Queue
              </h2>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                SM-2 memory retention intervals prioritized by decay risk.
              </p>
            </div>
            <Badge variant="purple" size="sm">
              Adaptive Recall
            </Badge>
          </div>

          <div className="space-y-3 mt-4">
            {revisions.map((item) => (
              <div
                key={item.concept}
                className="p-4 rounded-xl bg-white dark:bg-obsidian-800 border border-slate-200 dark:border-obsidian-600 flex items-center justify-between"
              >
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-bold text-slate-900 dark:text-white">
                      {item.concept}
                    </span>
                    <span
                      className={`px-2 py-0.5 text-[10px] font-bold rounded-full ${
                        item.urgency === "CRITICAL"
                          ? "bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20"
                          : item.urgency === "OVERDUE"
                          ? "bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20"
                          : "bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/20"
                      }`}
                    >
                      {item.urgency}
                    </span>
                  </div>
                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                    Reviewed {item.days_since_last_review} days ago • Recommended interval:{" "}
                    {item.recommended_interval_days} days
                  </p>
                </div>

                <Link to="/student/notes">
                  <Button size="sm" variant="secondary">
                    Review Now
                  </Button>
                </Link>
              </div>
            ))}
          </div>

          {/* Weekly / Monthly Focus Summary */}
          <div className="mt-6 p-4 rounded-xl bg-slate-50 dark:bg-obsidian-900/60 border border-slate-200 dark:border-obsidian-600">
            <div className="flex items-center space-x-2 text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              <Calendar className="w-3.5 h-3.5 text-indigo-500" />
              <span>Weekly Milestone Focus</span>
            </div>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Complete 15 Core AI &amp; Algorithms Missions with &gt;85% Quiz Retention.
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
};
