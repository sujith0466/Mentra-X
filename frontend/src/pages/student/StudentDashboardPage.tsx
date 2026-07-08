import React from "react";
import { Link } from "react-router-dom";
import { BrainCircuit, BookOpen, Clock, Flame, ArrowRight, CheckCircle2, Award, Zap, TrendingUp, Target } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { MetricCard } from "@/components/widgets/MetricCard";
import { DigitalTwinCard } from "@/components/widgets/DigitalTwinCard";
import { LearningProgress } from "@/components/widgets/LearningProgress";
import { RecommendationCard } from "@/components/widgets/RecommendationCard";
import { AIResponseCard } from "@/components/widgets/AIResponseCard";
import { useAuthStore } from "@/store/useAuthStore";

export const StudentDashboardPage: React.FC = () => {
  const { user } = useAuthStore();

  return (
    <div className="space-y-8 py-4">

      {/* ── Welcome Banner ─────────────────────────────── */}
      <div className="relative rounded-2xl overflow-hidden bg-gradient-to-br from-indigo-600 via-purple-600 to-indigo-700 p-6 sm:p-8">
        {/* Subtle orbs */}
        <div className="absolute -top-10 -right-10 w-48 h-48 bg-white/8 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-10 -left-10 w-48 h-48 bg-purple-400/15 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <Badge variant="success" size="sm">Free Plan Active</Badge>
              <span className="text-xs text-indigo-200">Student ID: #{user?.id || "—"}</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
              Welcome back, {user?.name?.split(" ")[0] || "Student"} 👋
            </h1>
            <p className="text-sm text-indigo-200 mt-1">
              Your AI tutor has identified 3 new practice exercises for you today.
            </p>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <Link to="/student/twin">
              <Button
                size="md"
                className="bg-white/15 hover:bg-white/25 text-white border border-white/25 backdrop-blur-sm"
                leftIcon={<BrainCircuit className="w-4 h-4" />}
              >
                Learning Profile
              </Button>
            </Link>
            <Link to="/student/coding">
              <Button
                size="md"
                className="bg-white text-indigo-700 hover:bg-slate-50 shadow-lg font-bold"
                leftIcon={<Zap className="w-4 h-4 text-amber-500" />}
              >
                Coding Arena
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* ── KPI Metrics ────────────────────────────────── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <MetricCard title="Overall Mastery"  value="84.2%" trend={4.5}  icon={<Award className="w-5 h-5" />}   subtitle="Top 5% of cohort" />
        <MetricCard title="Study Velocity"   value="2.8×"  trend={12.0} icon={<TrendingUp className="w-5 h-5" />} subtitle="vs. average learner" />
        <MetricCard title="Active Courses"   value="3"     trend={0}    icon={<BookOpen className="w-5 h-5" />} subtitle="Enrolled this term" />
        <MetricCard title="Learning Streak"  value="14 days" trend={20} icon={<Flame className="w-5 h-5" />}   subtitle="Personal best!" />
      </div>

      {/* ── Learning Profile Widget ─────────────────────── */}
      <DigitalTwinCard
        studentName={user?.name || "Student"}
        healthScore={92}
        knowledgeMastery={84}
        studyVelocity={2.8}
        streakDays={14}
        status="healthy"
      />

      {/* ── Main Grid ──────────────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

        {/* Left: Courses & Recommendations */}
        <div className="lg:col-span-2 space-y-6">

          {/* In-Progress Courses */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-indigo-500 dark:text-indigo-400" />
                In-Progress Courses
              </h2>
              <Link to="/student/my-courses" className="text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 transition-colors flex items-center gap-1">
                View All <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
            <div className="space-y-3">
              <LearningProgress courseTitle="Data Structures & Algorithms"      completedModules={8} totalModules={12} estimatedTimeLeft="3.5 hrs remaining" />
              <LearningProgress courseTitle="Cloud Computing & Distributed Systems" completedModules={5} totalModules={8}  estimatedTimeLeft="6 hrs remaining" />
              <LearningProgress courseTitle="Natural Language Processing"           completedModules={9} totalModules={10} estimatedTimeLeft="1 hr remaining" />
            </div>
          </div>

          {/* AI Recommendations */}
          <div>
            <h2 className="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2 mb-4">
              <Target className="w-5 h-5 text-rose-500 dark:text-rose-400" />
              AI Recommendations
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <RecommendationCard
                title="Review Search & Sorting Algorithms"
                description="Your practice results show a slight retention drop in binary search. A quick review will solidify your understanding."
                category="Retention Boost"
                priority="high"
              />
              <RecommendationCard
                title="Complete Cloud Architecture Autoscaling Lab"
                description="You are 1 lab away from unlocking your Cloud Architecture badge."
                category="Next Milestone"
                priority="medium"
              />
            </div>
          </div>
        </div>

        {/* Right: AI Feed & Deadlines */}
        <div className="space-y-5">

          {/* Daily AI Brief */}
          <Card variant="glass" className="space-y-4">
            <div className="flex items-center justify-between">
              <Badge variant="cyan" size="sm">AI Tutor</Badge>
              <span className="text-[10px] font-semibold text-emerald-600 dark:text-emerald-400">Live</span>
            </div>
            <h3 className="text-sm font-bold text-slate-900 dark:text-white">Today's Study Brief</h3>
            <AIResponseCard
              title="Study Tip"
              content="Great progress on Data Structures! You're 8 modules in. Today's focus: review DFS and BFS graph traversal — you scored 73% on those concepts in your last quiz. Let's push that to 90%!"
              confidenceScore={0.99}
              modelName="Mentra AI v2.5"
            />
          </Card>

          {/* Upcoming Deadlines */}
          <Card variant="default" className="space-y-4">
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-slate-400" />
              <h3 className="text-sm font-bold text-slate-900 dark:text-white">Upcoming Deadlines</h3>
            </div>
            <div className="space-y-2.5">
              {[
                { title: "Algorithms Quiz — Module 9",    course: "Data Structures",    badge: "In 2 Days", variant: "warning" as const },
                { title: "Cloud Architecture Lab Report", course: "Cloud Computing",     badge: "In 5 Days", variant: "primary" as const },
              ].map((d, i) => (
                <div key={i} className="flex items-center justify-between p-3 rounded-lg bg-slate-50 dark:bg-obsidian-900/60 border border-slate-100 dark:border-obsidian-600 text-xs">
                  <div>
                    <span className="font-semibold text-slate-900 dark:text-white block">{d.title}</span>
                    <span className="text-slate-500 dark:text-slate-400">{d.course}</span>
                  </div>
                  <Badge variant={d.variant} size="sm">{d.badge}</Badge>
                </div>
              ))}
            </div>
            <Link to="/student/planner">
              <Button variant="outline" size="sm" className="w-full" rightIcon={<ArrowRight className="w-3.5 h-3.5" />}>
                Open Planner
              </Button>
            </Link>
          </Card>

          {/* Quick Links */}
          <div className="grid grid-cols-2 gap-2.5">
            {[
              { to: "/student/ai-tutor",      label: "AI Tutor",       icon: BrainCircuit, color: "text-indigo-600 dark:text-indigo-400", bg: "bg-indigo-50 dark:bg-indigo-500/10" },
              { to: "/student/weakness",      label: "Weaknesses",     icon: Target,       color: "text-rose-600 dark:text-rose-400",     bg: "bg-rose-50 dark:bg-rose-500/10" },
              { to: "/student/career-resume", label: "Career",         icon: Award,        color: "text-amber-600 dark:text-amber-400",   bg: "bg-amber-50 dark:bg-amber-500/10" },
              { to: "/student/interview",     label: "Interview Prep", icon: CheckCircle2, color: "text-emerald-600 dark:text-emerald-400",bg: "bg-emerald-50 dark:bg-emerald-500/10" },
            ].map((q) => (
              <Link key={q.to} to={q.to}>
                <div className={`flex flex-col items-center gap-2 p-3 rounded-xl border border-slate-100 dark:border-obsidian-600 ${q.bg} hover:border-indigo-200 dark:hover:border-indigo-500/30 hover:-translate-y-0.5 transition-all duration-200 cursor-pointer`}>
                  <q.icon className={`w-5 h-5 ${q.color}`} />
                  <span className="text-[10px] font-semibold text-slate-700 dark:text-slate-300">{q.label}</span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
