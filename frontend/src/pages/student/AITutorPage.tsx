import React, { useState } from "react";
import { MessageSquare, Sparkles, HelpCircle, Layers, Terminal, Send, RefreshCw, CheckCircle2, ShieldAlert } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Badge } from "@/components/ui/Badge";
import { useAuthStore } from "@/store/useAuthStore";

export const AITutorPage: React.FC = () => {
  const { user } = useAuthStore();
  const [activeTab, setActiveTab] = useState<"doubt" | "quiz" | "revision" | "debug">("doubt");
  const [query, setQuery] = useState("");
  const [chatLog, setChatLog] = useState([
    {
      sender: "ai",
      text: `Hello ${user?.name || "Student"}! I am your autonomous Mastra swarm tutoring agent. How can I assist with your computer science or AI coursework today?`,
      timestamp: "Just now",
      badge: "Enkrypt Verified",
    },
  ]);
  const [isThinking, setIsThinking] = useState(false);

  // Flashcard State
  const [cardIndex, setCardIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const flashcards = [
    { front: "What is the vanishing gradient problem in deep neural networks?", back: "When gradients become exponentially small as they propagate backward through many layers, preventing weights in early layers from updating effectively." },
    { front: "What is the primary difference between ACID and BASE database transactions?", back: "ACID guarantees immediate consistency and durability (MySQL), while BASE prioritizes high availability and eventual consistency in distributed systems." },
    { front: "How does Qdrant HNSW indexing achieve sub-millisecond similarity search?", back: "By constructing multi-layered skip lists where upper layers route queries across long vector distances and lower layers perform fine-grained neighbor search." },
  ];

  // Debug Assistant State
  const [codeSnippet, setCodeSnippet] = useState("def calculate_attention(Q, K, V):\n    # Bug: Forgot scaling factor\n    scores = np.dot(Q, K.T)\n    return softmax(scores) @ V");
  const [debugOutput, setDebugOutput] = useState<string | null>(null);
  const [debugging, setDebugging] = useState(false);

  const handleSendQuery = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isThinking) return;

    const userMsg = { sender: "user", text: query, timestamp: "Just now", badge: "" };
    setChatLog((prev) => [...prev, userMsg]);
    setQuery("");
    setIsThinking(true);

    setTimeout(() => {
      const aiReply = {
        sender: "ai",
        text: `Socratic Insight: To answer "${userMsg.text}", let's consider how this concept maps to your Qdrant mastery embedding. Have you considered analyzing the time complexity of the underlying matrix multiplication first?`,
        timestamp: "Just now",
        badge: "Enkrypt Layer 6 OK",
      };
      setChatLog((prev) => [...prev, aiReply]);
      setIsThinking(false);
    }, 1200);
  };

  const handleRunDebug = () => {
    setDebugging(true);
    setDebugOutput(null);
    setTimeout(() => {
      setDebugOutput("Enkrypt DevTools AI Diagnosis:\n\n[Line 3] Bug Detected: Unscaled dot-product attention.\nFix: Divide dot-product by np.sqrt(d_k) before passing into softmax to prevent exploding gradients under high dimensional embedding vectors.");
      setDebugging(false);
    }, 1500);
  };

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-6">
        <div>
          <Badge variant="info" className="mb-2">
            <Sparkles className="w-3.5 h-3.5 mr-1.5 inline text-indigo-400" />
            24/7 Cognitive Learning Assistant
          </Badge>
          <h1 className="text-3xl font-extrabold text-white">Mastra AI Tutoring Swarm</h1>
          <p className="text-sm text-slate-400">Interactive Socratic doubt solving, flashcard revision, and code debugging with real-time Enkrypt verification.</p>
        </div>
        <div className="flex gap-2">
          {["doubt", "quiz", "revision", "debug"].map((tab) => {
            const labels: Record<string, { name: string; icon: any }> = {
              doubt: { name: "Doubt Solver", icon: MessageSquare },
              quiz: { name: "Practice Quiz", icon: HelpCircle },
              revision: { name: "Flashcards", icon: Layers },
              debug: { name: "Debug Assistant", icon: Terminal },
            };
            const item = labels[tab];
            const Icon = item.icon;
            const isActive = activeTab === tab;
            return (
              <button
                key={tab}
                onClick={() => setActiveTab(tab as any)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold transition-all ${
                  isActive
                    ? "bg-gradient-to-r from-indigo-600 to-cyan-600 text-white shadow-md shadow-indigo-500/20"
                    : "bg-obsidian-800/60 text-slate-400 hover:text-white border border-white/5"
                }`}
              >
                <Icon className="w-4 h-4" />
                <span className="hidden md:inline">{item.name}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Tab Panels */}
      {activeTab === "doubt" && (
        <Card variant="default" className="p-6 sm:p-8 flex flex-col h-[650px] justify-between">
          <div className="space-y-4 flex-1 overflow-y-auto pr-2">
            {chatLog.map((msg, idx) => (
              <div
                key={idx}
                className={`flex flex-col ${msg.sender === "user" ? "items-end" : "items-start"} space-y-1`}
              >
                <div
                  className={`max-w-2xl p-4 rounded-2xl text-sm leading-relaxed ${
                    msg.sender === "user"
                      ? "bg-indigo-600 text-white rounded-br-none"
                      : "bg-obsidian-900 border border-white/10 text-slate-200 rounded-bl-none"
                  }`}
                >
                  <p className="whitespace-pre-line">{msg.text}</p>
                </div>
                <div className="flex items-center gap-2 text-[10px] text-slate-500 px-1">
                  <span>{msg.timestamp}</span>
                  {msg.badge && <span className="text-emerald-400 font-semibold">{msg.badge}</span>}
                </div>
              </div>
            ))}
            {isThinking && (
              <div className="flex items-center gap-2 text-xs text-indigo-400 animate-pulse pl-2 pt-2">
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>Mastra swarm agent querying syllabus embedding vectors...</span>
              </div>
            )}
          </div>

          <form onSubmit={handleSendQuery} className="pt-4 border-t border-white/10 flex gap-3 mt-4">
            <Input
              placeholder="Ask any concept doubt or request a Socratic hint..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              disabled={isThinking}
              className="flex-1"
            />
            <Button type="submit" variant="primary" disabled={isThinking || !query.trim()} className="px-6">
              <Send className="w-4 h-4" />
            </Button>
          </form>
        </Card>
      )}

      {activeTab === "revision" && (
        <div className="max-w-2xl mx-auto space-y-6 text-center">
          <div className="flex justify-between items-center text-xs font-semibold text-slate-400">
            <span>Card {cardIndex + 1} of {flashcards.length}</span>
            <span className="text-cyan-400">Click card to flip</span>
          </div>

          <Card
            variant="glow"
            onClick={() => setIsFlipped(!isFlipped)}
            className="p-12 min-h-[300px] flex items-center justify-center cursor-pointer transition-transform duration-300 transform active:scale-98 border border-indigo-500/30 select-none"
          >
            <div className="space-y-4">
              <Badge variant={isFlipped ? "success" : "info"} className="mb-2">
                {isFlipped ? "Answer / Synthesis" : "Question / Concept"}
              </Badge>
              <p className="text-lg sm:text-xl font-bold text-white leading-relaxed max-w-lg mx-auto">
                {isFlipped ? flashcards[cardIndex].back : flashcards[cardIndex].front}
              </p>
            </div>
          </Card>

          <div className="flex justify-center gap-4 pt-2">
            <Button
              variant="secondary"
              disabled={cardIndex === 0}
              onClick={() => { setCardIndex(cardIndex - 1); setIsFlipped(false); }}
              className="px-6 py-2.5"
            >
              Previous Card
            </Button>
            <Button
              variant="primary"
              disabled={cardIndex === flashcards.length - 1}
              onClick={() => { setCardIndex(cardIndex + 1); setIsFlipped(false); }}
              className="px-6 py-2.5"
            >
              Next Card
            </Button>
          </div>
        </div>
      )}

      {activeTab === "debug" && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">
          <Card variant="default" className="p-6 flex flex-col justify-between space-y-4">
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <Badge variant="info">Sandboxed Code Editor</Badge>
                <span className="text-xs font-mono text-slate-400">Python 3.11</span>
              </div>
              <textarea
                rows={12}
                value={codeSnippet}
                onChange={(e) => setCodeSnippet(e.target.value)}
                className="w-full bg-obsidian-950 border border-white/10 rounded-xl p-4 text-xs sm:text-sm font-mono text-cyan-300 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <Button variant="primary" onClick={handleRunDebug} disabled={debugging} className="w-full justify-center py-3">
              <Terminal className="w-4 h-4 mr-2" />
              {debugging ? "Running Swarm Diagnostics..." : "Diagnose Code & Explain Bug"}
            </Button>
          </Card>

          <Card variant="gradient" className="p-6 flex flex-col justify-between space-y-4">
            <div className="space-y-3">
              <Badge variant="success">Enkrypt DevTools AI Output</Badge>
              {debugOutput ? (
                <div className="p-4 rounded-xl bg-obsidian-950/90 border border-white/10 font-mono text-xs text-slate-300 whitespace-pre-line leading-relaxed">
                  {debugOutput}
                </div>
              ) : (
                <div className="h-64 flex items-center justify-center text-center text-slate-400 text-xs">
                  Click "Diagnose Code" to execute Mastra swarm analysis.
                </div>
              )}
            </div>
            <div className="text-[10px] text-slate-400 flex items-center justify-between border-t border-white/10 pt-3">
              <span>Zero Hallucination Guarantee</span>
              <span className="text-emerald-400 font-semibold">Enkrypt Layer 6 Active</span>
            </div>
          </Card>
        </div>
      )}

      {activeTab === "quiz" && (
        <Card variant="glass" className="p-12 text-center space-y-6 max-w-2xl mx-auto">
          <div className="w-16 h-16 rounded-full bg-indigo-500/20 border border-indigo-500/40 flex items-center justify-center mx-auto">
            <HelpCircle className="w-8 h-8 text-indigo-400" />
          </div>
          <div className="space-y-2">
            <h3 className="text-2xl font-bold text-white">Adaptive Practice Quiz Generator</h3>
            <p className="text-sm text-slate-300">
              Generate a custom 5-question evaluation tailored to your weakest Qdrant vector concepts.
            </p>
          </div>
          <Button variant="primary" onClick={() => alert("Practice Quiz generated! Transferring to Assessment engine...")} className="px-8 py-3.5">
            <Sparkles className="w-4 h-4 mr-2" />
            Generate Adaptive Quiz Now
          </Button>
        </Card>
      )}
    </div>
  );
};
