import React, { useState, useRef, useEffect } from "react";
import { MessageSquare, Sparkles, HelpCircle, Layers, Terminal, Send, RefreshCw, CheckCircle2, Bot, User } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
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
      text: `Hello ${user?.name || "Student"}! I'm your personal AI tutor. Ask me anything about your coursework — concepts, problems, or code — and I'll guide you step by step.`,
      timestamp: "Just now",
      badge: "Verified",
    },
  ]);
  const [isThinking, setIsThinking] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  // Flashcard State
  const [cardIndex, setCardIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const flashcards = [
    { front: "What is the vanishing gradient problem in deep neural networks?", back: "When gradients become exponentially small as they propagate backward through many layers, preventing weights in early layers from updating effectively." },
    { front: "What is the primary difference between ACID and BASE database transactions?", back: "ACID guarantees immediate consistency and durability (MySQL), while BASE prioritizes high availability and eventual consistency in distributed systems." },
    { front: "How does high-dimensional indexing achieve fast similarity search?", back: "By constructing multi-layered skip lists where upper layers route queries across long distances and lower layers perform fine-grained neighbor search." },
  ];

  // Debug Assistant State
  const [codeSnippet, setCodeSnippet] = useState("def calculate_attention(Q, K, V):\n    # Bug: Forgot scaling factor\n    scores = np.dot(Q, K.T)\n    return softmax(scores) @ V");
  const [debugOutput, setDebugOutput] = useState<string | null>(null);
  const [debugging, setDebugging] = useState(false);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatLog, isThinking]);

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
        text: `Great question! To understand "${userMsg.text}", let's break it down step by step. Start by considering the time complexity of the core operation — what do you think happens when the input size doubles?`,
        timestamp: "Just now",
        badge: "Verified",
      };
      setChatLog((prev) => [...prev, aiReply]);
      setIsThinking(false);
    }, 1200);
  };

  const handleRunDebug = () => {
    setDebugging(true);
    setDebugOutput(null);
    setTimeout(() => {
      setDebugOutput("AI Code Diagnostic:\n\n[Line 3] Bug Detected: Unscaled dot-product attention.\nFix: Divide the dot-product by np.sqrt(d_k) before passing into softmax. This prevents values from growing too large, which would cause softmax gradients to vanish during training.");
      setDebugging(false);
    }, 1500);
  };

  const tabs = [
    { key: "doubt", name: "Ask a Question", icon: MessageSquare },
    { key: "quiz", name: "Practice Quiz", icon: HelpCircle },
    { key: "revision", name: "Flashcards", icon: Layers },
    { key: "debug", name: "Debug Helper", icon: Terminal },
  ];

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-white/10 pb-6">
        <div>
          <Badge variant="info" className="mb-2">
            <Sparkles className="w-3.5 h-3.5 mr-1.5 inline text-indigo-400" />
            Available 24/7
          </Badge>
          <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white">AI Tutor</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            Ask questions, practice with quizzes, review flashcards, or get help debugging your code.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.key;
            return (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key as any)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition-all duration-200 ${
                  isActive
                    ? "bg-gradient-to-r from-indigo-600 to-indigo-500 text-white shadow-md shadow-indigo-500/25"
                    : "bg-white dark:bg-obsidian-800 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white border border-slate-200 dark:border-obsidian-600 hover:border-indigo-300 dark:hover:border-indigo-500/40"
                }`}
              >
                <Icon className="w-4 h-4" />
                <span className="hidden md:inline">{tab.name}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Doubt Solver Chat */}
      <AnimatePresence mode="wait">
        {activeTab === "doubt" && (
          <motion.div
            key="doubt"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.2 }}
          >
            <Card variant="default" className="flex flex-col h-[650px]">
              {/* Chat Messages */}
              <div className="flex-1 overflow-y-auto p-6 space-y-5">
                {chatLog.map((msg, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.2 }}
                    className={`flex gap-3 ${msg.sender === "user" ? "flex-row-reverse" : "flex-row"}`}
                  >
                    {/* Avatar */}
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-1 ${
                      msg.sender === "user"
                        ? "bg-indigo-600"
                        : "bg-gradient-to-br from-cyan-500 to-indigo-600"
                    }`}>
                      {msg.sender === "user"
                        ? <User className="w-4 h-4 text-white" />
                        : <Bot className="w-4 h-4 text-white" />
                      }
                    </div>

                    {/* Bubble */}
                    <div className={`flex flex-col gap-1 max-w-[75%] ${msg.sender === "user" ? "items-end" : "items-start"}`}>
                      <div
                        className={`px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                          msg.sender === "user"
                            ? "bg-indigo-600 text-white rounded-tr-sm"
                            : "bg-slate-50 dark:bg-obsidian-900 border border-slate-200 dark:border-white/10 text-slate-700 dark:text-slate-200 rounded-tl-sm"
                        }`}
                      >
                        <p className="whitespace-pre-line">{msg.text}</p>
                      </div>
                      <div className="flex items-center gap-2 text-[10px] text-slate-400 px-1">
                        <span>{msg.timestamp}</span>
                        {msg.badge && (
                          <span className="inline-flex items-center gap-1 text-emerald-500 font-semibold">
                            <CheckCircle2 className="w-2.5 h-2.5" />
                            {msg.badge}
                          </span>
                        )}
                      </div>
                    </div>
                  </motion.div>
                ))}

                {isThinking && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="flex gap-3"
                  >
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-cyan-500 to-indigo-600 flex items-center justify-center shrink-0">
                      <Bot className="w-4 h-4 text-white" />
                    </div>
                    <div className="px-4 py-3 rounded-2xl rounded-tl-sm bg-slate-50 dark:bg-obsidian-900 border border-slate-200 dark:border-white/10 flex items-center gap-2">
                      <RefreshCw className="w-3.5 h-3.5 text-indigo-400 animate-spin" />
                      <span className="text-xs text-slate-400 animate-pulse">AI is thinking...</span>
                    </div>
                  </motion.div>
                )}
                <div ref={chatEndRef} />
              </div>

              {/* Input Area */}
              <div className="border-t border-slate-200 dark:border-white/10 p-4">
                <form onSubmit={handleSendQuery} className="flex gap-3 items-center">
                  <Input
                    placeholder="Ask anything about your coursework..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    disabled={isThinking}
                    className="flex-1"
                  />
                  <Button
                    type="submit"
                    variant="primary"
                    disabled={isThinking || !query.trim()}
                    className="px-5 py-2.5 shrink-0"
                  >
                    <Send className="w-4 h-4" />
                  </Button>
                </form>
                <p className="text-[10px] text-slate-400 mt-2 pl-1">Press Enter or click Send to ask your question.</p>
              </div>
            </Card>
          </motion.div>
        )}

        {/* Flashcard Revision */}
        {activeTab === "revision" && (
          <motion.div
            key="revision"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.2 }}
            className="max-w-2xl mx-auto space-y-6 text-center"
          >
            <div className="flex justify-between items-center text-xs font-semibold text-slate-400">
              <span>Card {cardIndex + 1} of {flashcards.length}</span>
              <span className="text-cyan-400">Click card to reveal answer</span>
            </div>

            <Card
              variant="glow"
              onClick={() => setIsFlipped(!isFlipped)}
              className="p-12 min-h-[300px] flex items-center justify-center cursor-pointer border border-indigo-500/30 select-none hover:border-indigo-400/50 hover:shadow-lg hover:shadow-indigo-500/10 transition-all duration-300"
            >
              <div className="space-y-4">
                <Badge variant={isFlipped ? "success" : "info"} className="mb-2">
                  {isFlipped ? "Answer" : "Question"}
                </Badge>
                <p className="text-lg sm:text-xl font-bold text-slate-900 dark:text-white leading-relaxed max-w-lg mx-auto">
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
                Previous
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
          </motion.div>
        )}

        {/* Debug Helper */}
        {activeTab === "debug" && (
          <motion.div
            key="debug"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.2 }}
            className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch"
          >
            <Card variant="default" className="p-6 flex flex-col gap-4">
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <Badge variant="info">Code Editor</Badge>
                  <span className="text-xs font-mono text-slate-400">Python 3.11</span>
                </div>
                <textarea
                  rows={12}
                  value={codeSnippet}
                  onChange={(e) => setCodeSnippet(e.target.value)}
                  className="w-full bg-slate-50 dark:bg-obsidian-900 border border-slate-200 dark:border-white/10 rounded-xl p-4 text-xs sm:text-sm font-mono text-cyan-400 dark:text-cyan-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
                />
              </div>
              <Button variant="primary" onClick={handleRunDebug} disabled={debugging} className="w-full justify-center py-3">
                <Terminal className="w-4 h-4 mr-2" />
                {debugging ? "Analysing Code..." : "Diagnose Code & Explain Bug"}
              </Button>
            </Card>

            <Card variant="gradient" className="p-6 flex flex-col gap-4">
              <Badge variant="success">AI Diagnostics</Badge>
              {debugOutput ? (
                <div className="flex-1 p-4 rounded-xl bg-white dark:bg-obsidian-900/90 border border-slate-200 dark:border-white/10 font-mono text-xs text-slate-600 dark:text-slate-300 whitespace-pre-line leading-relaxed">
                  {debugOutput}
                </div>
              ) : (
                <div className="flex-1 flex flex-col items-center justify-center text-center gap-3 text-slate-400 py-12">
                  <Terminal className="w-10 h-10 text-slate-300 dark:text-obsidian-600" />
                  <p className="text-sm font-medium">No diagnostics yet</p>
                  <p className="text-xs">Click "Diagnose Code" to run an AI-powered analysis of your code.</p>
                </div>
              )}
              <div className="text-[10px] text-slate-400 flex items-center justify-between border-t border-slate-200 dark:border-white/10 pt-3">
                <span>Sandboxed execution environment</span>
                <span className="text-emerald-500 font-semibold">AI Verified</span>
              </div>
            </Card>
          </motion.div>
        )}

        {/* Practice Quiz */}
        {activeTab === "quiz" && (
          <motion.div
            key="quiz"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.2 }}
          >
            <Card variant="glass" className="p-12 text-center space-y-6 max-w-2xl mx-auto">
              <div className="w-16 h-16 rounded-2xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center mx-auto">
                <HelpCircle className="w-8 h-8 text-indigo-400" />
              </div>
              <div className="space-y-2">
                <h3 className="text-2xl font-bold text-slate-900 dark:text-white">Adaptive Practice Quiz</h3>
                <p className="text-sm text-slate-600 dark:text-slate-300 max-w-md mx-auto">
                  Generate a personalized 5-question quiz tailored to your current weak areas and learning progress.
                </p>
              </div>
              <Button variant="primary" onClick={() => alert("Practice Quiz generated! Transferring to Assessment engine...")} className="px-8 py-3.5">
                <Sparkles className="w-4 h-4 mr-2" />
                Generate My Practice Quiz
              </Button>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
