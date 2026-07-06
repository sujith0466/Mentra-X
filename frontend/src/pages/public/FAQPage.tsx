import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { HelpCircle, ChevronDown, Sparkles, ShieldCheck, Brain, Code, BookOpen } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Input } from "@/components/ui/Input";

export const FAQPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [openId, setOpenId] = useState<number | null>(1);
  const [activeCategory, setActiveCategory] = useState<string>("all");

  const faqItems = [
    {
      id: 1,
      category: "ai",
      question: "How does the Cognitive Digital Twin graph track my academic progress?",
      answer: "The Digital Twin graph is seeded with your initial skill profile during onboarding. As you complete video lectures, practice quizzes, and coding challenges, real-time telemetry updates your knowledge state vectors in Qdrant. This allows our Mastra swarm tutoring agents to precisely identify concepts requiring reinforcement without repeating already mastered material.",
    },
    {
      id: 2,
      category: "ai",
      question: "What is Mastra Cognitive Swarm tutoring and how is it different from standard ChatGPT?",
      answer: "Instead of a single monolithic LLM prompt, Mentra X utilizes Mastra to orchestrate specialized cognitive swarms (Career AI, Tutor AI, DevTools AI, and Community AI). Each agent has dedicated tool access, deterministic memory context, and is governed by Enkrypt Layer 6 safety monitors to eliminate hallucinations and ensure pedagogical accuracy.",
    },
    {
      id: 3,
      category: "security",
      question: "How does Enkrypt Layer 6 protect my student data and AI interactions?",
      answer: "Enkrypt Layer 6 acts as an immutable real-time interceptor between all user inputs and AI model executions. It performs continuous similarity scoring, PII redaction, and prompt injection filtering. Every response generated is accompanied by a verifiable safety badge and audit log entry.",
    },
    {
      id: 4,
      category: "coding",
      question: "Can I practice coding in multiple languages inside the platform?",
      answer: "Yes! The Mentra X Coding Arena supports sandboxed execution for Python, JavaScript, TypeScript, C++, and Java. You receive instant console output, automated test case validation, and real-time Socratic debugging hints from our integrated DevTools AI assistant.",
    },
    {
      id: 5,
      category: "academic",
      question: "How do course certificates and career roadmaps work?",
      answer: "Upon completing all required course modules and passing the adaptive skill assessments, your Digital Twin certifies your competency. The Career AI module then uses this verified DNA to generate customized career roadmaps, resume enhancements, and targeted mock interview simulations.",
    },
    {
      id: 6,
      category: "security",
      question: "Is Mentra X GDPR compliant and can I export my learning memory?",
      answer: "Absolutely. In compliance with enterprise governance standards, students have full sovereignty over their data. You can export your entire conversation history, coding logs, and Qdrant vector embeddings, or request permanent deletion directly from your account settings.",
    },
  ];

  const categories = [
    { id: "all", label: "All Questions", icon: HelpCircle },
    { id: "ai", label: "AI & Digital Twin", icon: Brain },
    { id: "coding", label: "Coding Arena", icon: Code },
    { id: "academic", label: "Courses & Career", icon: BookOpen },
    { id: "security", label: "Safety & GDPR", icon: ShieldCheck },
  ];

  const filteredFaqs = faqItems.filter((item) => {
    const matchesCategory = activeCategory === "all" || item.category === activeCategory;
    const matchesSearch = item.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          item.answer.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="min-h-screen py-16 px-4 sm:px-6 lg:px-8 space-y-12">
      {/* Header */}
      <div className="max-w-4xl mx-auto text-center space-y-6">
        <Badge variant="info" className="px-3 py-1 text-xs">
          <Sparkles className="w-3.5 h-3.5 mr-1.5 inline text-indigo-400" />
          Enterprise Knowledge Base
        </Badge>
        <h1 className="text-4xl sm:text-5xl font-extrabold text-white tracking-tight">
          Frequently Asked <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">Questions</span>
        </h1>
        <p className="text-lg text-slate-300 max-w-2xl mx-auto">
          Everything you need to know about our cognitive AI swarms, real-time Digital Twin tracking, and enterprise security governance.
        </p>

        {/* Search Bar */}
        <div className="max-w-xl mx-auto pt-4">
          <Input
            placeholder="Search questions, concepts, or security terms..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-obsidian-800/80 border-white/10 text-white placeholder-slate-500 py-3 px-4 rounded-xl shadow-lg focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        {/* Category Tabs */}
        <div className="flex flex-wrap justify-center gap-2 pt-4">
          {categories.map((cat) => {
            const Icon = cat.icon;
            const isActive = activeCategory === cat.id;
            return (
              <button
                key={cat.id}
                onClick={() => setActiveCategory(cat.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? "bg-gradient-to-r from-indigo-600 to-cyan-600 text-white shadow-md shadow-indigo-500/20"
                    : "bg-obsidian-800/60 text-slate-400 hover:text-white hover:bg-obsidian-700/60 border border-white/5"
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{cat.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* FAQ Accordion List */}
      <div className="max-w-3xl mx-auto space-y-4">
        {filteredFaqs.length === 0 ? (
          <Card variant="glass" className="p-8 text-center text-slate-400">
            No matching questions found for "{searchQuery}". Try adjusting your search or category filter.
          </Card>
        ) : (
          filteredFaqs.map((faq) => {
            const isOpen = openId === faq.id;
            return (
              <Card
                key={faq.id}
                variant={isOpen ? "glow" : "default"}
                className="overflow-hidden border border-white/10 transition-colors"
              >
                <button
                  onClick={() => setOpenId(isOpen ? null : faq.id)}
                  className="w-full p-6 text-left flex justify-between items-center gap-4 focus:outline-none"
                >
                  <span className="text-base font-bold text-white flex items-center gap-3">
                    <span className="w-2 h-2 rounded-full bg-indigo-400 shrink-0" />
                    {faq.question}
                  </span>
                  <div className={`p-1 rounded-full bg-white/5 transition-transform duration-200 ${isOpen ? "rotate-180 bg-indigo-500/20 text-indigo-400" : "text-slate-400"}`}>
                    <ChevronDown className="w-5 h-5" />
                  </div>
                </button>
                <AnimatePresence>
                  {isOpen && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.2 }}
                      className="px-6 pb-6 pt-2 text-sm text-slate-300 leading-relaxed border-t border-white/5"
                    >
                      <p className="pl-5 border-l-2 border-indigo-500/50">{faq.answer}</p>
                    </motion.div>
                  )}
                </AnimatePresence>
              </Card>
            );
          })
        )}
      </div>
    </div>
  );
};
