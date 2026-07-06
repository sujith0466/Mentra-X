import React from "react";
import { Link } from "react-router-dom";
import { BrainCircuit, BookOpen, Clock, Flame, ArrowRight, CheckCircle2, Award, Zap } from "lucide-react";
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
      {/* Welcome Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-obsidian-600 pb-6">
        <div>
          <div className="flex items-center space-x-2">
            <Badge variant="cyan" size="sm">Enterprise License Active</Badge>
            <span className="text-xs font-mono text-slate-500">Session ID: #MX-9942</span>
          </div>
          <h1 className="text-3xl font-extrabold text-white mt-1">
            Welcome back, {user?.name || "Student"} 👋
          </h1>
          <p className="text-sm text-slate-400 mt-0.5">
            Your Digital Twin has processed 14 new concept embeddings since your last login.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <Link to="/student/twin">
            <Button size="md" variant="outline" leftIcon={<BrainCircuit className="w-4 h-4 text-ai-violet" />}>
              Inspect Twin Graph
            </Button>
          </Link>
          <Link to="/student/coding">
            <Button size="md" leftIcon={<Zap className="w-4 h-4 text-amber-400" />}>
              Coding Arena
            </Button>
          </Link>
        </div>
      </div>

      {/* KPI Metric Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard title="Overall Mastery" value="84.2%" trend={4.5} icon={<Award className="w-5 h-5" />} subtitle="Top 5% of cohort" />
        <MetricCard title="Study Velocity" value="2.8x" trend={12.0} icon={<Zap className="w-5 h-5" />} subtitle="vs baseline average" />
        <MetricCard title="Active Courses" value="3" trend={0} icon={<BookOpen className="w-5 h-5" />} subtitle="Enrolled syllabus" />
        <MetricCard title="Learning Streak" value="14 Days" trend={20.0} icon={<Flame className="w-5 h-5" />} subtitle="Personal best streak!" />
      </div>

      {/* Digital Twin Widget */}
      <DigitalTwinCard
        studentName={user?.name || "Sujith"}
        healthScore={92}
        knowledgeMastery={84}
        studyVelocity={2.8}
        streakDays={14}
        status="healthy"
      />

      {/* Main Grid: Enrolled Courses & AI Tutoring Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-indigo-400" /> In-Progress Courses
            </h2>
            <Link to="/student/my-courses" className="text-xs text-primary-500 hover:text-indigo-300 transition-colors flex items-center gap-1">
              View All <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="space-y-4">
            <LearningProgress courseTitle="Advanced Agentic Coding & Orchestration" completedModules={8} totalModules={12} estimatedTimeLeft="3.5 hrs remaining" />
            <LearningProgress courseTitle="Enterprise Cloud Architecture & Distributed Systems" completedModules={5} totalModules={8} estimatedTimeLeft="6 hrs remaining" />
            <LearningProgress courseTitle="Vector Memory Systems & Qdrant Engineering" completedModules={9} totalModules={10} estimatedTimeLeft="1 hr remaining" />
          </div>

          <div className="space-y-4 pt-4">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <Zap className="w-5 h-5 text-amber-400" /> Adaptive AI Recommendations
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <RecommendationCard
                title="Review Qdrant HNSW Index Parameters"
                description="Your Digital Twin detected a slight retention drop in vector similarity search heuristics."
                category="Retention Boost"
                priority="high"
              />
              <RecommendationCard
                title="Complete Kubernetes Autoscaling Lab"
                description="You are 1 lab away from unlocking your Enterprise Cloud Architecture badge."
                category="Milestone Goal"
                priority="medium"
              />
            </div>
          </div>
        </div>

        {/* Right Column: AI Tutor & Live Feed */}
        <div className="space-y-6">
          <Card variant="glass" className="space-y-4">
            <div className="flex items-center justify-between">
              <Badge variant="cyan" size="sm">Mastra AI Swarm</Badge>
              <span className="text-xs font-mono text-emerald-400">Enkrypt Protected</span>
            </div>
            <h3 className="text-base font-bold text-white">Daily Cognitive Briefing</h3>
            <AIResponseCard
              title="Twin Diagnostic Note"
              content="Good morning! I reviewed your recent submissions in the Developer Arena. Your code structure is clean, but pay close attention to async error boundaries when delegating tools in Mastra swarms."
              confidenceScore={0.99}
              modelName="Gemini-2.5-Pro"
            />
          </Card>

          <Card variant="default" className="p-5 space-y-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider">Upcoming Deadlines</h3>
            <div className="space-y-3 text-xs">
              <div className="flex items-center justify-between p-2.5 rounded bg-obsidian-900 border border-obsidian-600">
                <div>
                  <span className="font-semibold text-white block">Multi-Agent Routing Quiz</span>
                  <span className="text-slate-400">Course: Agentic Coding</span>
                </div>
                <Badge variant="warning">In 2 Days</Badge>
              </div>
              <div className="flex items-center justify-between p-2.5 rounded bg-obsidian-900 border border-obsidian-600">
                <div>
                  <span className="font-semibold text-white block">Qdrant Vector Lab Submission</span>
                  <span className="text-slate-400">Course: Vector Systems</span>
                </div>
                <Badge variant="primary">In 5 Days</Badge>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
