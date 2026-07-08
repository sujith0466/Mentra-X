import React from "react";
import { ShieldCheck, BrainCircuit, Zap, Server, Award, Users } from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { SafetyBadge } from "@/components/widgets/SafetyBadge";

export const AboutPage: React.FC = () => {
  return (
    <div className="space-y-16 py-8 max-w-5xl mx-auto">
      <div className="text-center space-y-4">
        <Badge variant="cyan">Our Vision</Badge>
        <h1 className="text-4xl font-extrabold text-slate-900 dark:text-white">The Future of Learning</h1>
        <p className="text-base text-slate-600 dark:text-slate-300 max-w-3xl mx-auto leading-relaxed">
          Mentra X is a next-generation AI learning platform designed to adapt to your unique learning style and help you achieve your goals.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card variant="glass" className="space-y-4">
          <div className="w-10 h-10 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center">
            <BrainCircuit className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-slate-900 dark:text-white">Personalized Learning Profile</h3>
          <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
            Our system learns how you study best, tracking your progress and adapting course materials to help you learn faster and remember longer.
          </p>
        </Card>

        <Card variant="glass" className="space-y-4">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-slate-900 dark:text-white">Safe & Verified Content</h3>
          <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
            All AI responses are cross-checked against authoritative course materials to ensure accuracy and prevent misinformation.
          </p>
        </Card>

        <Card variant="glass" className="space-y-4">
          <div className="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center">
            <Zap className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-slate-900 dark:text-white">Smart AI Tutors</h3>
          <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
            Get instant, accurate help with coding, architecture, and career prep from our specialized AI tutors.
          </p>
        </Card>

        <Card variant="glass" className="space-y-4">
          <div className="w-10 h-10 rounded-xl bg-purple-500/20 text-purple-400 flex items-center justify-center">
            <Server className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-slate-900 dark:text-white">Long-Term Learning Memory</h3>
          <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
            Our AI remembers what you've learned in the past, connecting new concepts to your existing knowledge for a deeper understanding.
          </p>
        </Card>
      </div>

      <Card variant="default" className="p-8 text-center space-y-4 bg-gradient-to-tr from-obsidian-900 via-obsidian-800 to-indigo-950/40">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Built for Student Success</h2>
        <p className="text-sm text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">
          Mentra X is trusted by thousands of students to deliver a safe, effective, and personalized learning experience.
        </p>
        <div className="flex justify-center gap-3 pt-2">
          <SafetyBadge status="APPROVE" score={1.0} />
          <Badge variant="success">Zero Functional Regression</Badge>
        </div>
      </Card>
    </div>
  );
};
