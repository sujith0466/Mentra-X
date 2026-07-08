import React from "react";
import { useParams, Link } from "react-router-dom";
import { BookOpen, Clock, Award, ShieldCheck, CheckCircle2, Play, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { SafetyBadge } from "@/components/widgets/SafetyBadge";
import { AIResponseCard } from "@/components/widgets/AIResponseCard";

export const CourseDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  const courseTitle = id === "ai-101" ? "Introduction to Artificial Intelligence" :
                     id === "cs-202" ? "Cloud Computing & Distributed Systems" :
                     "Natural Language Processing";

  const syllabus = [
    { mod: 1, title: "Introduction to Neural Networks", desc: "Understanding network architectures and backpropagation.", status: "completed" },
    { mod: 2, title: "Deep Learning Fundamentals", desc: "Implementing convolutional and recurrent neural networks.", status: "completed" },
    { mod: 3, title: "Natural Language Processing", desc: "Building text classification and sentiment analysis models.", status: "in_progress" },
    { mod: 4, title: "AI Ethics and Safety", desc: "Understanding bias, fairness, and safety in AI models.", status: "locked" },
    { mod: 5, title: "Deploying AI Models", desc: "Scaling machine learning models in production environments.", status: "locked" },
  ];

  return (
    <div className="space-y-8 py-6">
      <Link to="/courses" className="inline-flex items-center space-x-2 text-xs text-slate-400 hover:text-slate-900 dark:text-white transition-colors">
        <ArrowLeft className="w-4 h-4" /> <span>Back to Course Catalog</span>
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <div className="space-y-3">
            <div className="flex items-center space-x-2">
              <Badge variant="purple">AI & Machine Learning</Badge>
              <Badge variant="danger">Advanced Level</Badge>
              <SafetyBadge status="VERIFIED" />
            </div>
            <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white leading-tight">{courseTitle}</h1>
            <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              This masterclass covers the complete theoretical and practical foundations required to design, test, and deploy enterprise-grade autonomous AI agents into high-concurrency production environments.
            </p>
          </div>

          {/* AI Tutoring Highlight */}
          <AIResponseCard
            title="Syllabus AI Tutor Insight"
            content="Based on your Learning Profile profile, you have already mastered 85% of Module 1 concepts from your previous coursework. I recommend jumping directly into Module 2's lab exercise on deterministic tool execution."
            confidenceScore={0.99}
          />

          {/* Syllabus Accordion / List */}
          <div className="space-y-4">
            <h2 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-indigo-400" /> Course Syllabus ({syllabus.length} Modules)
            </h2>
            <div className="space-y-3">
              {syllabus.map((item) => (
                <div
                  key={item.mod}
                  className="p-4 rounded-xl bg-white dark:bg-obsidian-800 border border-slate-200 dark:border-obsidian-600 flex items-center justify-between hover:border-indigo-500/40 transition-colors"
                >
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 rounded-lg bg-slate-50 dark:bg-obsidian-900 border border-slate-200 dark:border-obsidian-600 flex items-center justify-center text-xs font-bold text-indigo-400 shrink-0 mt-0.5">
                      0{item.mod}
                    </div>
                    <div>
                      <h4 className="text-sm font-bold text-slate-900 dark:text-white">{item.title}</h4>
                      <p className="text-xs text-slate-400 mt-0.5">{item.desc}</p>
                    </div>
                  </div>
                  <div className="shrink-0 ml-4">
                    {item.status === "completed" ? (
                      <span className="inline-flex items-center text-xs font-semibold text-emerald-400 gap-1">
                        <CheckCircle2 className="w-4 h-4" /> Completed
                      </span>
                    ) : item.status === "in_progress" ? (
                      <Link to={`/student/course/${id}`}>
                        <Button size="sm" leftIcon={<Play className="w-3.5 h-3.5 fill-current" />}>
                          Continue
                        </Button>
                      </Link>
                    ) : (
                      <span className="text-xs text-slate-500 font-mono">Locked</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Sidebar Enrollment Box */}
        <div className="space-y-6">
          <Card variant="glow" className="space-y-6 sticky top-24">
            <div className="space-y-2">
              <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Enterprise Enrollment</span>
              <div className="text-3xl font-extrabold text-slate-900 dark:text-white">Full Access Included</div>
              <p className="text-xs text-slate-400">Covered under your Mentra X Student AI license.</p>
            </div>

            <div className="space-y-3 text-xs text-slate-600 dark:text-slate-300 border-t border-b border-slate-200 dark:border-obsidian-600 py-4">
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-1.5"><Clock className="w-4 h-4 text-indigo-400" /> Duration</span>
                <span className="font-semibold text-slate-900 dark:text-white">24 Hours</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-1.5"><BookOpen className="w-4 h-4 text-ai-violet" /> Modules</span>
                <span className="font-semibold text-slate-900 dark:text-white">5 Dedicated Labs</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-1.5"><Award className="w-4 h-4 text-amber-400" /> Certificate</span>
                <span className="font-semibold text-slate-900 dark:text-white">Enterprise Certified</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="flex items-center gap-1.5"><ShieldCheck className="w-4 h-4 text-cyan-400" /> Safety Verification</span>
                <span className="font-semibold text-emerald-400">100% Validated</span>
              </div>
            </div>

            <Link to="/student/dashboard" className="block w-full">
              <Button size="lg" className="w-full">
                Go to Classroom
              </Button>
            </Link>
          </Card>
        </div>
      </div>
    </div>
  );
};
