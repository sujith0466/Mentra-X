import React, { useState } from "react";
import { FileCheck2, Play, CheckCircle2, MessageSquare, Award, Sparkles } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { AIResponseCard } from "@/components/widgets/AIResponseCard";

export const InterviewPrepPage: React.FC = () => {
  const [selectedTopic, setSelectedTopic] = useState("System Design: AI Swarm Architectures");
  const [inSession, setInSession] = useState(false);
  const [questionIndex, setQuestionIndex] = useState(0);
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState<string | null>(null);

  const questions = [
    "How do you handle tool execution failures when an autonomous agent encounters rate limits?",
    "Explain how Qdrant HNSW indexing differs from standard inverted index keyword search.",
    "Describe the role of Enkrypt Layer 6 in preventing PII leakage during LLM inference.",
  ];

  const handleStart = (topic: string) => {
    setSelectedTopic(topic);
    setInSession(true);
    setQuestionIndex(0);
    setFeedback(null);
  };

  const handleSubmitAnswer = () => {
    if (!answer.trim()) return;
    setFeedback(`Strong response! Your emphasis on exponential backoff and circuit breaker patterns aligns with Tier-1 enterprise reliability guidelines. Score: 94/100.`);
  };

  return (
    <div className="space-y-8 py-6">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 border-b border-obsidian-600 pb-6">
        <div>
          <Badge variant="purple" size="sm">Mock Technical Interviewer</Badge>
          <h1 className="text-3xl font-extrabold text-white mt-1">AI Mock Interview Simulator</h1>
          <p className="text-sm text-slate-400 mt-1">Practice system design and agentic coding questions with real-time Enkrypt feedback.</p>
        </div>
      </div>

      {!inSession ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            { title: "System Design: AI Swarm Architectures", qCount: 15, level: "Advanced", desc: "Multi-agent orchestration, state machines, and failure domain separation." },
            { title: "Vector Memory & Retrieval Engineering", qCount: 12, level: "Advanced", desc: "Vector embeddings, HNSW tuning, cosine similarity, and RAG optimization." },
            { title: "Enterprise Frontend Architecture", qCount: 20, level: "Intermediate", desc: "React 18 SPA performance, server state caching, and design systems." },
          ].map((item, idx) => (
            <Card key={idx} variant="interactive" className="flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <Badge variant="primary">{item.level}</Badge>
                  <span className="text-xs text-slate-500">{item.qCount} Questions</span>
                </div>
                <h3 className="text-lg font-bold text-white">{item.title}</h3>
                <p className="text-xs text-slate-400 mt-2">{item.desc}</p>
              </div>
              <div className="pt-4 mt-4 border-t border-obsidian-600">
                <Button size="md" className="w-full" onClick={() => handleStart(item.title)} leftIcon={<Play className="w-4 h-4 fill-current" />}>
                  Start Mock Interview
                </Button>
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <div className="space-y-6 max-w-4xl mx-auto">
          <Card variant="glow" className="p-6 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-indigo-400 uppercase tracking-wider">{selectedTopic}</span>
              <Badge variant="cyan">Question {questionIndex + 1} of {questions.length}</Badge>
            </div>
            <h3 className="text-xl font-bold text-white leading-relaxed">{questions[questionIndex]}</h3>
          </Card>

          <Card variant="default" className="p-6 space-y-4">
            <h4 className="font-semibold text-sm text-white">Your Verbal / Written Explanation</h4>
            <textarea
              rows={6}
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="Type your structured explanation here (use STAR method or architecture diagrams)..."
              className="w-full rounded-lg bg-obsidian-900 border border-obsidian-600 p-4 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
            <div className="flex items-center justify-between">
              <Button size="sm" variant="outline" onClick={() => setInSession(false)}>Exit Session</Button>
              <Button size="md" onClick={handleSubmitAnswer}>Submit for AI Critique</Button>
            </div>
          </Card>

          {feedback && (
            <div className="space-y-4">
              <AIResponseCard
                title="Mastra Interview Evaluation Agent"
                content={feedback}
                confidenceScore={0.96}
                modelName="Gemini-2.5-Interview-Pro"
              />
              <div className="flex justify-end">
                <Button
                  size="md"
                  onClick={() => {
                    setFeedback(null);
                    setAnswer("");
                    if (questionIndex < questions.length - 1) setQuestionIndex(questionIndex + 1);
                    else setInSession(false);
                  }}
                >
                  {questionIndex < questions.length - 1 ? "Next Question" : "Complete Interview"}
                </Button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
