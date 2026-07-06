import React from "react";
import { Sparkles, Brain, ArrowRight, BookOpen, Target, Briefcase, Award, TrendingUp } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Link } from "react-router-dom";

export const RecommendationsPage: React.FC = () => {
  const recommendations = [
    {
      id: 1,
      type: "Course Reinforcement",
      title: "CS-402: Scalable Vector Search & HNSW Indexing",
      matchScore: "98% Match",
      reason: "Your Digital Twin detected high mastery in general data structures but recommended deeper exploration into HNSW graph parameters based on recent quiz velocity.",
      badge: "Priority DNA Match",
      variant: "glow" as const,
      link: "/courses/2",
      icon: BookOpen,
    },
    {
      id: 2,
      type: "Coding Challenge",
      title: "Challenge #14: Implement LRU Cache with O(1) Lookup",
      matchScore: "94% Match",
      reason: "Enhances your algorithmic time-complexity vector vector embedding before attempting Level 9 career technical evaluations.",
      badge: "Skill Acceleration",
      variant: "default" as const,
      link: "/student/coding",
      icon: Target,
    },
    {
      id: 3,
      type: "Career Milestone",
      title: "AI Security Systems Architect Roadmap",
      matchScore: "96% Match",
      reason: "Aligns with your top scores in Enkrypt Layer 6 safety protocols and full-stack enterprise systems development.",
      badge: "Career Track",
      variant: "gradient" as const,
      link: "/student/career/resume",
      icon: Briefcase,
    },
  ];

  return (
    <div className="max-w-6xl mx-auto py-10 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-6">
        <div>
          <Badge variant="info" className="mb-2">
            <Sparkles className="w-3.5 h-3.5 mr-1.5 inline text-indigo-400" />
            Mastra Swarm Intelligence
          </Badge>
          <h1 className="text-3xl font-extrabold text-white">Personalized Digital Twin Recommendations</h1>
          <p className="text-sm text-slate-400">Curated learning paths and career milestones generated in real-time from your Qdrant knowledge state.</p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" className="px-3 py-1.5 text-xs">
            <TrendingUp className="w-3.5 h-3.5 mr-1 inline" />
            2.8x Mastery Velocity
          </Badge>
        </div>
      </div>

      {/* Hero Banner */}
      <Card variant="glass" className="p-8 grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
        <div className="md:col-span-2 space-y-3">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Brain className="w-6 h-6 text-indigo-400" />
            How Your Recommendations are Generated
          </h2>
          <p className="text-sm text-slate-300 leading-relaxed">
            Every lesson video watched, quiz completed, and code compiled updates your 1536-dimensional vector profile in Qdrant. Our Mastra swarm agents continuously analyze this semantic memory against enterprise job requirements to recommend optimal next steps.
          </p>
        </div>
        <div className="flex justify-center md:justify-end">
          <Link to="/student/twin">
            <Button variant="secondary" className="px-6 py-3 text-xs">
              View Full Digital Twin Graph &rarr;
            </Button>
          </Link>
        </div>
      </Card>

      {/* Recommendations Cards */}
      <div className="space-y-6">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <Award className="w-5 h-5 text-cyan-400" />
          Recommended Actions for This Week
        </h3>

        <div className="grid grid-cols-1 gap-6">
          {recommendations.map((rec) => {
            const Icon = rec.icon;
            return (
              <Card key={rec.id} variant={rec.variant} className="p-6 sm:p-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 transition-all hover:border-white/20">
                <div className="flex items-start gap-5 flex-1">
                  <div className="w-14 h-14 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center shrink-0">
                    <Icon className="w-7 h-7 text-indigo-400" />
                  </div>
                  <div className="space-y-2">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">{rec.type}</span>
                      <Badge variant="success">{rec.matchScore}</Badge>
                      <Badge variant={rec.variant === "glow" ? "info" : "default"}>{rec.badge}</Badge>
                    </div>
                    <h4 className="text-xl font-bold text-white">{rec.title}</h4>
                    <p className="text-sm text-slate-300 leading-relaxed max-w-3xl">{rec.reason}</p>
                  </div>
                </div>

                <div className="shrink-0 w-full md:w-auto flex justify-end">
                  <Link to={rec.link}>
                    <Button variant={rec.variant === "glow" ? "primary" : "secondary"} className="w-full md:w-auto px-6 py-3">
                      Start Recommended Action
                      <ArrowRight className="w-4 h-4 ml-2" />
                    </Button>
                  </Link>
                </div>
              </Card>
            );
          })}
        </div>
      </div>
    </div>
  );
};
