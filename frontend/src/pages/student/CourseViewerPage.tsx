import React, { useState } from "react";
import { useParams, Link } from "react-router-dom";
import { Play, CheckCircle2, MessageSquare, BookOpen, ArrowLeft, Send, Sparkles } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Input } from "@/components/ui/Input";
import { AIResponseCard } from "@/components/widgets/AIResponseCard";
import { SafetyBadge } from "@/components/widgets/SafetyBadge";

export const CourseViewerPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [activeTab, setActiveTab] = useState<"video" | "notes" | "tutor">("tutor");
  const [question, setQuestion] = useState("");
  const [tutorReply, setTutorReply] = useState(
    "Welcome to Module 3! In this lesson, we will implement deterministic routing in intelligent advanced AI workflows. Feel free to ask me for code examples or syllabus clarifications."
  );

  const handleAskTutor = () => {
    if (!question.trim()) return;
    setTutorReply(`Analyzing query: "${question}"... Here is how you configure the routing schema in AI workflows:\n\n\`\`\`ts\nexport const router = createRouter({\n  tools: [vectorSearchTool, safetyValidateTool],\n  strategy: 'deterministic'\n});\n\`\`\`\n\nThis ensures 0% hallucination during agent execution.`);
    setQuestion("");
  };

  return (
    <div className="space-y-6 py-4">
      <div className="flex items-center justify-between border-b border-slate-200 dark:border-obsidian-600 pb-4">
        <div className="flex items-center space-x-4">
          <Link to="/student/my-courses" className="p-2 rounded-lg bg-white dark:bg-obsidian-800 border border-slate-200 dark:border-obsidian-600 hover:bg-slate-100 dark:bg-obsidian-700 transition-colors">
            <ArrowLeft className="w-4 h-4 text-slate-600 dark:text-slate-300" />
          </Link>
          <div>
            <div className="flex items-center space-x-2">
              <Badge variant="purple" size="sm">Module 3 of 12</Badge>
              <SafetyBadge status="VERIFIED" />
            </div>
            <h1 className="text-xl font-bold text-slate-900 dark:text-white mt-1">Deterministic Tool Execution in tutors</h1>
          </div>
        </div>
        <Button size="sm" variant="primary" rightIcon={<CheckCircle2 className="w-4 h-4" />}>
          Mark Module Complete
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left 2 Cols: Video / Interactive Viewer */}
        <div className="lg:col-span-2 space-y-6">
          <div className="aspect-video w-full rounded-2xl bg-white dark:bg-obsidian-900 border border-slate-200 dark:border-obsidian-600 relative overflow-hidden flex items-center justify-center shadow-2xl group">
            <div className="absolute inset-0 bg-gradient-to-tr from-indigo-950/40 via-obsidian-900 to-transparent" />
            <div className="text-center z-10 space-y-4">
              <div className="w-16 h-16 rounded-full bg-primary-600 text-slate-900 dark:text-white flex items-center justify-center mx-auto shadow-lg shadow-indigo-500/30 group-hover:scale-110 transition-transform cursor-pointer">
                <Play className="w-8 h-8 fill-current ml-1" />
              </div>
              <span className="text-sm font-semibold text-slate-600 dark:text-slate-300 block">Click to Start Interactive Video Lecture</span>
            </div>
          </div>

          <div className="flex border-b border-slate-200 dark:border-obsidian-600 space-x-4">
            {(["tutor", "notes", "video"] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`py-2 px-4 text-xs font-semibold capitalize border-b-2 transition-all ${
                  activeTab === tab
                    ? "border-primary-500 text-primary-400"
                    : "border-transparent text-slate-400 hover:text-slate-900 dark:text-white"
                }`}
              >
                {tab === "tutor" ? "🤖 Intelligent AI Tutor" : tab === "notes" ? "📝 My Notes" : "📺 Lecture Transcript"}
              </button>
            ))}
          </div>

          {activeTab === "tutor" && (
            <div className="space-y-4">
              <AIResponseCard
                title="Intelligent Interactive Tutor"
                content={tutorReply}
                confidenceScore={0.99}
              />
              <div className="flex items-center space-x-2">
                <Input
                  placeholder="Ask a question about deterministic routing..."
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleAskTutor()}
                />
                <Button size="md" onClick={handleAskTutor} className="shrink-0">
                  <Send className="w-4 h-4" />
                </Button>
              </div>
            </div>
          )}

          {activeTab === "notes" && (
            <Card variant="default" className="p-4 space-y-3">
              <h4 className="font-semibold text-sm text-slate-900 dark:text-white">Student Study Notes</h4>
              <textarea
                rows={6}
                placeholder="Type your lecture notes here... They will automatically sync with your Learning Profile."
                className="w-full rounded-lg bg-slate-50 dark:bg-obsidian-900 border border-slate-200 dark:border-obsidian-600 p-3 text-sm text-slate-700 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
              <Button size="sm" variant="outline">Save Note to Twin</Button>
            </Card>
          )}

          {activeTab === "video" && (
            <Card variant="default" className="p-4 space-y-2 text-xs text-slate-600 dark:text-slate-300 font-mono leading-relaxed">
              <p>[00:00] Welcome to Module 3 of Advanced Agentic Coding.</p>
              <p>[01:15] When coordinating multiple autonomous LLM agents, non-deterministic routing can cause infinite loops or tool execution failures.</p>
              <p>[03:40] To mitigate this, we introduce the AI Safety verification pattern...</p>
            </Card>
          )}
        </div>

        {/* Right 1 Col: Module Checklist */}
        <div className="space-y-6">
          <Card variant="default" className="p-5 space-y-4">
            <h3 className="font-bold text-sm text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-indigo-400" /> Course Modules
            </h3>
            <div className="space-y-2 text-xs">
              {[
                { id: 1, title: "Introduction to tutors", status: "completed" },
                { id: 2, title: "Tool Execution & Routing", status: "completed" },
                { id: 3, title: "Deterministic Tool Execution", status: "active" },
                { id: 4, title: "Learning Memory Integration", status: "locked" },
                { id: 5, title: "AI Safety Interception", status: "locked" },
              ].map((mod) => (
                <div
                  key={mod.id}
                  className={`p-3 rounded-xl border flex items-center justify-between ${
                    mod.status === "active"
                      ? "bg-primary-600/10 border-primary-500/40 text-slate-900 dark:text-white font-semibold"
                      : "bg-slate-50 dark:bg-obsidian-900/60 border-slate-200 dark:border-obsidian-600/50 text-slate-400"
                  }`}
                >
                  <span className="truncate">0{mod.id}. {mod.title}</span>
                  {mod.status === "completed" && <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />}
                  {mod.status === "active" && <span className="w-2 h-2 rounded-full bg-primary-500 animate-pulse shrink-0" />}
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
