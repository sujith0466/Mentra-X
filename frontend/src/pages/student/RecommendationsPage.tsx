import React from "react";
import { Sparkles, Brain, ArrowRight, BookOpen, Target, Briefcase, Award, TrendingUp, Lightbulb } from "lucide-react";
import { motion } from "framer-motion";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Link } from "react-router-dom";

export const RecommendationsPage: React.FC = () => {
  const recommendations = [
    {
      id: 1,
      type: "Course Recommendation",
      title: "CS-402: Advanced Search & Data Indexing",
      matchScore: "98% Match",
      reason: "Based on your strong performance in data structures, this course dives deeper into advanced indexing algorithms — a natural next step that aligns with your recent quiz results.",
      badge: "Top Pick",
      variant: "glow" as const,
      link: "/courses/2",
      icon: BookOpen,
    },
    {
      id: 2,
      type: "Coding Challenge",
      title: "Challenge #14: Implement LRU Cache with O(1) Lookup",
      matchScore: "94% Match",
      reason: "Strengthens your understanding of time-complexity trade-offs before you attempt Level 9 technical interview problems.",
      badge: "Skill Builder",
      variant: "default" as const,
      link: "/student/coding",
      icon: Target,
    },
    {
      id: 3,
      type: "Career Milestone",
      title: "AI Security Systems Architect Roadmap",
      matchScore: "96% Match",
      reason: "Your top scores in AI safety and full-stack development make this career track a great fit for your current skill level.",
      badge: "Career Track",
      variant: "gradient" as const,
      link: "/student/career/resume",
      icon: Briefcase,
    },
  ];

  return (
    <div className="max-w-6xl mx-auto py-10 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-white/10 pb-6">
        <div>
          <Badge variant="info" className="mb-2">
            <Sparkles className="w-3.5 h-3.5 mr-1.5 inline text-indigo-400" />
            Personalised for You
          </Badge>
          <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white">My Recommendations</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            Curated courses, challenges, and career milestones based on your learning progress.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" className="px-3 py-1.5 text-xs">
            <TrendingUp className="w-3.5 h-3.5 mr-1 inline" />
            On a Learning Streak
          </Badge>
        </div>
      </div>

      {/* How Recommendations Work Banner */}
      <Card variant="glass" className="p-8 grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
        <div className="md:col-span-2 space-y-3">
          <h2 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-indigo-400" />
            How your recommendations work
          </h2>
          <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
            Every lesson you watch, quiz you complete, and challenge you attempt updates your personal learning profile. Our AI analyses your progress and matches it against real-world skills to suggest the most impactful next steps for you.
          </p>
        </div>
        <div className="flex justify-center md:justify-end">
          <Link to="/student/twin">
            <Button variant="secondary" className="px-6 py-3 text-xs">
              View My Learning Profile →
            </Button>
          </Link>
        </div>
      </Card>

      {/* Recommendation Cards */}
      <div className="space-y-5">
        <h3 className="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <Award className="w-5 h-5 text-cyan-400" />
          Recommended This Week
        </h3>

        <div className="grid grid-cols-1 gap-5">
          {recommendations.map((rec, idx) => {
            const Icon = rec.icon;
            return (
              <motion.div
                key={rec.id}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.07 }}
              >
                <Card
                  variant={rec.variant}
                  className="p-6 sm:p-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 hover:-translate-y-0.5 hover:shadow-md transition-all duration-200"
                >
                  <div className="flex items-start gap-5 flex-1">
                    {/* Icon */}
                    <div className="w-14 h-14 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center shrink-0">
                      <Icon className="w-7 h-7 text-indigo-400" />
                    </div>

                    <div className="space-y-2.5">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">{rec.type}</span>
                        <Badge variant="success">{rec.matchScore}</Badge>
                        <Badge variant={rec.variant === "glow" ? "info" : "default"}>{rec.badge}</Badge>
                      </div>
                      <h4 className="text-xl font-bold text-slate-900 dark:text-white leading-snug">{rec.title}</h4>
                      <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed max-w-2xl">{rec.reason}</p>
                    </div>
                  </div>

                  <div className="shrink-0 w-full md:w-auto flex justify-end">
                    <Link to={rec.link}>
                      <Button
                        variant={rec.variant === "glow" ? "primary" : "secondary"}
                        className="w-full md:w-auto px-6 py-3"
                      >
                        Get Started
                        <ArrowRight className="w-4 h-4 ml-2" />
                      </Button>
                    </Link>
                  </div>
                </Card>
              </motion.div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
