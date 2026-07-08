import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Brain, CheckCircle, ArrowRight, Shield, AlertCircle, Award, Sparkles, RefreshCw } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { useAuthStore } from "@/store/useAuthStore";
import { Link } from "react-router-dom";

export const AssessmentPage: React.FC = () => {
  const { user } = useAuthStore();
  const [step, setStep] = useState<"intro" | "questions" | "results">("intro");
  const [currentQIndex, setCurrentQIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, number>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const questions = [
    {
      id: 1,
      domain: "Computer Science & Algorithmic Foundations",
      question: "What is the worst-case time complexity of inserting a node into a balanced Binary Search Tree (AVL)?",
      options: ["O(1) constant time", "O(log n) logarithmic time", "O(n) linear time", "O(n log n) linearithmic time"],
      correct: 1,
      difficulty: "Intermediate",
    },
    {
      id: 2,
      domain: "Artificial Intelligence & Neural Networks",
      question: "In the Transformer architecture, what is the primary computational benefit of Self-Attention over Recurrent Neural Networks?",
      options: [
        "It eliminates mathematical floating-point operations.",
        "It allows parallel processing of sequential tokens across the context window.",
        "It requires zero gradient backpropagation during training.",
        "It reduces model parameter count to O(1).",
      ],
      correct: 1,
      difficulty: "Advanced",
    },
    {
      id: 3,
      domain: "Full-Stack Enterprise Systems",
      question: "Why would an enterprise architecture team choose a hybrid MySQL + Database storage model over a standalone vector DB?",
      options: [
        "Database cannot store string characters.",
        "MySQL provides ACID transactional integrity for relational users/courses, while Database specializes in high-dimensional semantic similarity search.",
        "MySQL runs faster than memory RAM.",
        "Database Systems do not support network HTTP protocols.",
      ],
      correct: 1,
      difficulty: "Advanced",
    },
    {
      id: 4,
      domain: "Cognitive AI Tutors & Tool Routing",
      question: "What is the primary function of deterministic tool calling inside an intelligent advanced AI system?",
      options: [
        "To randomly guess Python syntax errors.",
        "To allow specialized agents to invoke verifiable external APIs and database queries without hallucinating free-form text.",
        "To encrypt CSS stylesheets.",
        "To bypass AI Safety Verification governance.",
      ],
      correct: 1,
      difficulty: "Expert",
    },
  ];

  const handleSelectOption = (qIdx: number, optIdx: number) => {
    setSelectedAnswers((prev) => ({ ...prev, [qIdx]: optIdx }));
  };

  const handleNext = () => {
    if (currentQIndex < questions.length - 1) {
      setCurrentQIndex((prev) => prev + 1);
    } else {
      setIsSubmitting(true);
      setTimeout(() => {
        setIsSubmitting(false);
        setStep("results");
      }, 1500);
    }
  };

  const calculateScore = () => {
    let correctCount = 0;
    questions.forEach((q, idx) => {
      if (selectedAnswers[idx] === q.correct) correctCount++;
    });
    return Math.round((correctCount / questions.length) * 100);
  };

  return (
    <div className="max-w-4xl mx-auto py-12 px-4 sm:px-6 space-y-8">
      {/* Header */}
      <div className="text-center space-y-3">
        <Badge variant="info" className="px-3 py-1 text-xs">
          <Brain className="w-3.5 h-3.5 mr-1.5 inline text-indigo-400" />
          Adaptive DNA Seeding Engine
        </Badge>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight">
          Cognitive Skill <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">Assessment</span>
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-300 max-w-xl mx-auto">
          Our adaptive assessment calibrates your initial learning embeddings in your Personalized Learning Memory, enabling our AI tutors to personalize your learning trajectory.
        </p>
      </div>

      <AnimatePresence mode="wait">
        {step === "intro" && (
          <motion.div
            key="intro"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
          >
            <Card variant="glow" className="p-8 space-y-6 text-center">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-indigo-500/20 to-cyan-500/20 border border-indigo-500/30 flex items-center justify-center mx-auto">
                <Sparkles className="w-8 h-8 text-cyan-400" />
              </div>
              <div className="space-y-2">
                <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Ready to Seed Your Learning Profile?</h2>
                <p className="text-sm text-slate-600 dark:text-slate-300 max-w-md mx-auto">
                  This 4-question adaptive evaluation tests your foundations across Algorithms, Transformer Architectures, Hybrid Database Systems, and Cognitive tutors.
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-2xl mx-auto pt-2 text-left">
                <div className="p-4 rounded-xl bg-slate-50 dark:bg-obsidian-900/80 border border-slate-200 dark:border-white/10">
                  <Badge variant="default" className="mb-2">Time: ~5 mins</Badge>
                  <p className="text-xs text-slate-400">Untimed Socratic evaluation designed to measure depth over speed.</p>
                </div>
                <div className="p-4 rounded-xl bg-slate-50 dark:bg-obsidian-900/80 border border-slate-200 dark:border-white/10">
                  <Badge variant="info" className="mb-2">Memory Sync</Badge>
                  <p className="text-xs text-slate-400">Directly initializes your 1536-dimensional personalized learning memory state.</p>
                </div>
                <div className="p-4 rounded-xl bg-slate-50 dark:bg-obsidian-900/80 border border-slate-200 dark:border-white/10">
                  <Badge variant="success" className="mb-2">Verified DNA</Badge>
                  <p className="text-xs text-slate-400">Generates verifiable skill badges for your student profile.</p>
                </div>
              </div>

              <div className="pt-4">
                <Button variant="primary" onClick={() => setStep("questions")} className="px-8 py-3.5 text-base">
                  Begin Adaptive Assessment
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </div>
            </Card>
          </motion.div>
        )}

        {step === "questions" && (
          <motion.div
            key="questions"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="space-y-6"
          >
            {/* Progress Bar */}
            <div className="flex items-center justify-between text-xs font-semibold text-slate-400">
              <span>Question {currentQIndex + 1} of {questions.length}</span>
              <span className="text-indigo-400">{questions[currentQIndex].domain}</span>
            </div>
            <div className="w-full h-2 bg-slate-50 dark:bg-obsidian-900 rounded-full overflow-hidden border border-slate-200 dark:border-white/5">
              <div
                className="h-full bg-gradient-to-r from-indigo-500 to-cyan-400 transition-all duration-300"
                style={{ width: `${((currentQIndex + 1) / questions.length) * 100}%` }}
              />
            </div>

            {/* Question Card */}
            <Card variant="default" className="p-8 space-y-6">
              <div className="flex justify-between items-start gap-4">
                <h3 className="text-lg sm:text-xl font-bold text-slate-900 dark:text-white leading-relaxed">
                  {questions[currentQIndex].question}
                </h3>
                <Badge variant="info">{questions[currentQIndex].difficulty}</Badge>
              </div>

              <div className="space-y-3 pt-2">
                {questions[currentQIndex].options.map((option, idx) => {
                  const isSelected = selectedAnswers[currentQIndex] === idx;
                  return (
                    <button
                      key={option}
                      onClick={() => handleSelectOption(currentQIndex, idx)}
                      className={`w-full p-4 rounded-xl text-left border text-sm font-medium transition-all flex items-center justify-between ${
                        isSelected
                          ? "bg-gradient-to-r from-indigo-600/20 to-cyan-600/20 border-indigo-500 text-slate-900 dark:text-white shadow-md shadow-indigo-500/10"
                          : "bg-slate-50 dark:bg-obsidian-900/60 border-slate-200 dark:border-white/10 text-slate-600 dark:text-slate-300 hover:bg-white dark:bg-obsidian-800/80 hover:border-slate-300 dark:border-white/20"
                      }`}
                    >
                      <span className="flex items-center gap-3">
                        <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                          isSelected ? "bg-indigo-500 text-slate-900 dark:text-white" : "bg-white dark:bg-obsidian-800 text-slate-400 border border-slate-200 dark:border-white/10"
                        }`}>
                          {String.fromCharCode(65 + idx)}
                        </span>
                        {option}
                      </span>
                      {isSelected && <CheckCircle className="w-5 h-5 text-cyan-400 shrink-0" />}
                    </button>
                  );
                })}
              </div>

              <div className="pt-6 border-t border-slate-200 dark:border-white/10 flex justify-between items-center">
                <Button
                  variant="secondary"
                  disabled={currentQIndex === 0 || isSubmitting}
                  onClick={() => setCurrentQIndex((prev) => prev - 1)}
                  className="text-xs"
                >
                  Previous
                </Button>
                <Button
                  variant="primary"
                  disabled={selectedAnswers[currentQIndex] === undefined || isSubmitting}
                  onClick={handleNext}
                  className="px-6 py-2.5 text-sm"
                >
                  {isSubmitting ? (
                    <span className="inline-flex items-center gap-2">
                      <RefreshCw className="w-4 h-4 animate-spin" />
                      Seeding Learning Profile...
                    </span>
                  ) : currentQIndex === questions.length - 1 ? (
                    "Submit Assessment"
                  ) : (
                    "Next Question"
                  )}
                </Button>
              </div>
            </Card>
          </motion.div>
        )}

        {step === "results" && (
          <motion.div
            key="results"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="space-y-6"
          >
            <Card variant="gradient" className="p-8 text-center space-y-6">
              <div className="w-20 h-20 rounded-full bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center mx-auto">
                <Award className="w-10 h-10 text-emerald-400" />
              </div>
              <div className="space-y-2">
                <Badge variant="success" className="px-3 py-1">Learning Profile Seeded Successfully</Badge>
                <h2 className="text-3xl font-extrabold text-slate-900 dark:text-white">Assessment Mastery Score: {calculateScore()}%</h2>
                <p className="text-sm text-slate-600 dark:text-slate-300 max-w-lg mx-auto">
                  Your responses have been compiled into high-dimensional embeddings and synchronized with your Personalized Learning Memory.
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-xl mx-auto text-left pt-2">
                <div className="p-4 rounded-xl bg-white dark:bg-obsidian-900/80 border border-slate-200 dark:border-white/10 space-y-1">
                  <span className="text-xs text-slate-400 block">Assigned Competency Tier</span>
                  <span className="text-lg font-bold text-cyan-400">Enterprise Advanced (Level 8)</span>
                </div>
                <div className="p-4 rounded-xl bg-white dark:bg-obsidian-900/80 border border-slate-200 dark:border-white/10 space-y-1">
                  <span className="text-xs text-slate-400 block">Recommended Focus</span>
                  <span className="text-lg font-bold text-indigo-400">advanced AI Cognitive tutors</span>
                </div>
              </div>

              <div className="pt-6 flex flex-wrap justify-center gap-4">
                <Link to="/student/dashboard">
                  <Button variant="primary" className="px-8 py-3">
                    View Learning Profile Dashboard
                  </Button>
                </Link>
                <button onClick={() => { setSelectedAnswers({}); setCurrentQIndex(0); setStep("intro"); }}>
                  <Button variant="secondary" className="px-6 py-3">
                    Retake Assessment
                  </Button>
                </button>
              </div>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
