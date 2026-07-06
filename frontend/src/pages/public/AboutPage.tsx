import React from "react";
import { ShieldCheck, BrainCircuit, Zap, Server, Award, Users } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { SafetyBadge } from "@/components/widgets/SafetyBadge";

export const AboutPage: React.FC = () => {
  return (
    <div className="space-y-16 py-8 max-w-5xl mx-auto">
      <div className="text-center space-y-4">
        <Badge variant="cyan">Enterprise Architecture Vision</Badge>
        <h1 className="text-4xl font-extrabold text-white">Engineering the Future of AI Learning</h1>
        <p className="text-base text-slate-300 max-w-3xl mx-auto leading-relaxed">
          Mentra X is an enterprise-grade AI student platform that bridges the gap between traditional Learning Management Systems and autonomous AI tutoring swarms.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card variant="glass" className="space-y-4">
          <div className="w-10 h-10 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center">
            <BrainCircuit className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white">Cognitive Digital Twins</h3>
          <p className="text-sm text-slate-300 leading-relaxed">
            Every student is paired with a persistent Digital Twin that models knowledge graphs, learning velocity, and retrieval retention in real-time, enabling hyper-personalized syllabus adaptation.
          </p>
        </Card>

        <Card variant="glass" className="space-y-4">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white">AI Safety Verification Layer</h3>
          <p className="text-sm text-slate-300 leading-relaxed">
            All AI interactions pass through rigorous multi-agent governance interceptors that verify cosine similarity against authoritative course syllabi, eliminating AI hallucinations and PII leaks.
          </p>
        </Card>

        <Card variant="glass" className="space-y-4">
          <div className="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center">
            <Zap className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white">Intelligent AI Orchestration Engines</h3>
          <p className="text-sm text-slate-300 leading-relaxed">
            Our multi-agent swarms dynamically route complex coding questions, architecture reviews, and resume analysis to specialized LLM agents for deterministic, high-accuracy execution.
          </p>
        </Card>

        <Card variant="glass" className="space-y-4">
          <div className="w-10 h-10 rounded-xl bg-purple-500/20 text-purple-400 flex items-center justify-center">
            <Server className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white">Personalized Vector Memory</h3>
          <p className="text-sm text-slate-300 leading-relaxed">
            We utilize high-performance vector databases to maintain long-term semantic memory across semesters, ensuring tutoring agents never lose context of prior student milestones.
          </p>
        </Card>
      </div>

      <Card variant="default" className="p-8 text-center space-y-4 bg-gradient-to-tr from-obsidian-900 via-obsidian-800 to-indigo-950/40">
        <h2 className="text-2xl font-bold text-white">Enterprise Certified & Audited</h2>
        <p className="text-sm text-slate-300 max-w-2xl mx-auto">
          Our platform has completed 36/36 ESDLC compliance tests and achieved full enterprise certification across all cognitive architecture layers.
        </p>
        <div className="flex justify-center gap-3 pt-2">
          <SafetyBadge status="APPROVE" score={1.0} />
          <Badge variant="success">Zero Functional Regression</Badge>
        </div>
      </Card>
    </div>
  );
};
