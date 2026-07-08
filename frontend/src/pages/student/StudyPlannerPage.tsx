import React, { useState } from "react";
import { TrendingUp, Calendar, Sparkles, CheckCircle2, Clock, BookOpen } from "lucide-react";
import { motion } from "framer-motion";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { AIResponseCard } from "@/components/widgets/AIResponseCard";
import { RecommendationCard } from "@/components/widgets/RecommendationCard";

export const StudyPlannerPage: React.FC = () => {
  const [generating, setGenerating] = useState(false);

  const schedule = [
    {
      day: "Today (Monday)",
      tasks: [
        { title: "Complete Module 3 Video Lecture", time: "10:00 AM – 11:30 AM", course: "Agentic Coding", status: "done" },
        { title: "Practice Lab: Data Structures", time: "2:00 PM – 3:00 PM", course: "Algorithms", status: "pending" },
      ],
    },
    {
      day: "Tomorrow (Tuesday)",
      tasks: [
        { title: "Review AI Safety Concepts", time: "9:30 AM – 11:00 AM", course: "Security", status: "pending" },
        { title: "Mock Technical Interview Practice", time: "4:00 PM – 5:00 PM", course: "Career Prep", status: "pending" },
      ],
    },
    {
      day: "Wednesday",
      tasks: [
        { title: "Kubernetes Cluster Autoscaling Lab", time: "1:00 PM – 4:00 PM", course: "Cloud Architecture", status: "pending" },
      ],
    },
  ];

  const handleGenerate = () => {
    setGenerating(true);
    setTimeout(() => setGenerating(false), 1000);
  };

  return (
    <div className="space-y-8 py-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-slate-200 dark:border-obsidian-600 pb-6">
        <div>
          <Badge variant="purple">
            <Sparkles className="w-3 h-3 mr-1.5 inline" />
            AI-Powered Schedule
          </Badge>
          <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white mt-1">Study Planner</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            Your schedule is optimised by AI based on your retention patterns and upcoming exams.
          </p>
        </div>
        <Button
          size="md"
          onClick={handleGenerate}
          isLoading={generating}
          leftIcon={<Sparkles className="w-4 h-4 text-indigo-400" />}
        >
          Re-Optimise with AI
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Schedule */}
        <div className="lg:col-span-2 space-y-6">
          <AIResponseCard
            title="Your AI recommends"
            content="I moved your data structures lab to Monday afternoon — your retention is historically 22% higher during that time slot based on your recent quiz scores."
            confidenceScore={0.98}
          />

          <div className="space-y-5">
            {schedule.map((group, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.05 }}
              >
                <Card variant="default" className="p-5 space-y-4">
                  <div className="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-obsidian-600">
                    <h3 className="font-bold text-base text-slate-900 dark:text-white flex items-center gap-2">
                      <Calendar className="w-4 h-4 text-indigo-500" />
                      {group.day}
                    </h3>
                    <Badge variant="default">{group.tasks.length} {group.tasks.length === 1 ? "Session" : "Sessions"}</Badge>
                  </div>

                  <div className="space-y-3">
                    {group.tasks.map((task, tIdx) => (
                      <div
                        key={tIdx}
                        className={`p-4 rounded-xl border flex items-center justify-between gap-4 transition-all duration-200 group hover:-translate-y-0.5 hover:shadow-sm ${
                          task.status === "done"
                            ? "bg-emerald-500/5 border-emerald-500/20"
                            : "bg-slate-50 dark:bg-obsidian-900/60 border-slate-200 dark:border-obsidian-600 hover:border-indigo-300 dark:hover:border-indigo-500/40"
                        }`}
                      >
                        <div className="flex items-start gap-3">
                          <button className="mt-0.5 text-slate-300 hover:text-emerald-400 transition-colors">
                            <CheckCircle2
                              className={`w-5 h-5 transition-colors ${
                                task.status === "done"
                                  ? "text-emerald-400 fill-emerald-400/20"
                                  : "text-slate-300 dark:text-obsidian-500"
                              }`}
                            />
                          </button>
                          <div>
                            <h4
                              className={`text-sm font-semibold ${
                                task.status === "done"
                                  ? "line-through text-slate-400"
                                  : "text-slate-900 dark:text-white"
                              }`}
                            >
                              {task.title}
                            </h4>
                            <div className="flex items-center gap-3 mt-1.5 text-xs text-slate-400">
                              <span className="flex items-center gap-1">
                                <Clock className="w-3 h-3" />
                                {task.time}
                              </span>
                              <Badge variant="purple" size="sm">{task.course}</Badge>
                            </div>
                          </div>
                        </div>
                        <Badge variant={task.status === "done" ? "success" : "primary"}>
                          {task.status === "done" ? "Done" : "Upcoming"}
                        </Badge>
                      </div>
                    ))}
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          <RecommendationCard
            title="Focus Block: 45 Min Pomodoro"
            description="Your AI recommends a 45-minute focused study block before your afternoon lab to maximise deep-work retention."
            category="Optimal Timing"
            priority="high"
          />

          <Card variant="default" className="p-5 space-y-4">
            <div className="flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-cyan-400" />
              <h4 className="text-sm font-bold text-slate-900 dark:text-white">This Week's Progress</h4>
            </div>
            <div className="space-y-3">
              {[
                { label: "Sessions Completed", value: "4 / 7", pct: 57 },
                { label: "Study Hours Logged", value: "6.5 hrs", pct: 72 },
              ].map((stat) => (
                <div key={stat.label} className="space-y-1.5">
                  <div className="flex justify-between text-xs text-slate-500 dark:text-slate-400">
                    <span>{stat.label}</span>
                    <span className="font-semibold text-slate-700 dark:text-slate-300">{stat.value}</span>
                  </div>
                  <div className="h-1.5 bg-slate-100 dark:bg-obsidian-900 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-indigo-500 to-cyan-400 rounded-full transition-all duration-500"
                      style={{ width: `${stat.pct}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
