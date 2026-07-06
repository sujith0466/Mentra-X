import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Sparkles, ArrowRight, BrainCircuit, ShieldCheck, Zap, BookOpen, CheckCircle2 } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { SafetyBadge } from "@/components/widgets/SafetyBadge";
import { ConfidenceMeter } from "@/components/widgets/ConfidenceMeter";

export const LandingPage: React.FC = () => {
  return (
    <div className="space-y-20 py-8">
      {/* Hero Section */}
      <section className="relative text-center space-y-6 max-w-4xl mx-auto pt-8">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[500px] h-[300px] bg-primary-600/15 rounded-full blur-3xl -z-10 pointer-events-none" />
        
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs font-semibold text-indigo-300"
        >
          <Sparkles className="w-3.5 h-3.5 text-primary-500 animate-pulse" />
          <span>Enterprise Certified Enkrypt Layer 6 Active</span>
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white leading-tight"
        >
          The Next-Generation AI LMS with <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-500 via-ai-violet to-indigo-300">Cognitive Digital Twins</span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="text-lg sm:text-xl text-slate-300 max-w-2xl mx-auto font-normal leading-relaxed"
        >
          Experience hyper-personalized AI tutoring powered by Qdrant vector memory swarms, adaptive career pathways, and real-time safety interception.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="flex flex-wrap items-center justify-center gap-4 pt-4"
        >
          <Link to="/courses">
            <Button size="lg" rightIcon={<ArrowRight className="w-4 h-4" />}>
              Explore Course Catalog
            </Button>
          </Link>
          <Link to="/student/dashboard">
            <Button size="lg" variant="outline">
              Enter Student Portal
            </Button>
          </Link>
        </motion.div>
      </section>

      {/* Live Enterprise Demo Widget Showcase */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card variant="glass" className="space-y-4">
          <div className="flex items-center justify-between">
            <Badge variant="purple" size="sm">Mastra Swarm</Badge>
            <SafetyBadge status="APPROVE" score={0.99} />
          </div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <BrainCircuit className="w-5 h-5 text-ai-violet" /> Real-Time Cognitive Sync
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Your Digital Twin continuously models your learning velocity, mastery gaps, and retrieval retention in real-time.
          </p>
          <ConfidenceMeter score={0.96} label="Twin Prediction Accuracy" size="sm" />
        </Card>

        <Card variant="glass" className="space-y-4">
          <div className="flex items-center justify-between">
            <Badge variant="cyan" size="sm">Enkrypt Layer 6</Badge>
            <Badge variant="success" size="sm">100% Secure</Badge>
          </div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-cyan-400" /> Zero Hallucination Guarantee
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            All AI tutoring outputs are intercepted and validated against authoritative course syllabus embeddings before rendering.
          </p>
          <div className="p-2.5 rounded bg-obsidian-900 border border-white/5 font-mono text-[11px] text-emerald-400">
            [ENKRYPT_VERIFIED]: Content matches syllabus embedding #4092 with 0.992 cosine similarity.
          </div>
        </Card>

        <Card variant="glass" className="space-y-4">
          <div className="flex items-center justify-between">
            <Badge variant="primary" size="sm">Adaptive LMS</Badge>
            <Badge variant="default" size="sm">Qdrant Memory</Badge>
          </div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Zap className="w-5 h-5 text-amber-400" /> Dynamic Career Roadmaps
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Upload your resume to instantly generate custom learning pathways tailored to target enterprise job descriptions.
          </p>
          <div className="flex items-center justify-between text-xs text-slate-300 pt-2">
            <span>Skill Gap Closure Rate</span>
            <span className="font-bold text-indigo-400">3.4x Faster</span>
          </div>
        </Card>
      </section>

      {/* Featured Courses Preview */}
      <section className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-white">Featured Enterprise Courses</h2>
            <p className="text-sm text-slate-400 mt-1">Curated syllabi with automated AI tutoring support.</p>
          </div>
          <Link to="/courses" className="text-xs font-semibold text-primary-500 hover:text-indigo-300 transition-colors flex items-center gap-1">
            View All Courses <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {[
            { id: "ai-101", title: "Advanced Agentic Coding & Orchestration", desc: "Master Mastra swarms, multi-agent workflows, and tool execution.", level: "Advanced", modules: 12 },
            { id: "cs-202", title: "Enterprise Cloud Architecture & Distributed Systems", desc: "Design fault-tolerant, high-concurrency microservices on AWS/GCP.", level: "Intermediate", modules: 8 },
            { id: "ml-303", title: "Vector Memory Systems & Qdrant Engineering", desc: "Build semantic search engines, hybrid search, and RAG pipelines.", level: "Advanced", modules: 10 },
          ].map((course) => (
            <Card key={course.id} variant="interactive" className="flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <Badge variant="primary">{course.level}</Badge>
                  <span className="text-xs text-slate-500 flex items-center gap-1"><BookOpen className="w-3.5 h-3.5" /> {course.modules} Modules</span>
                </div>
                <h3 className="text-lg font-bold text-white leading-snug">{course.title}</h3>
                <p className="text-xs text-slate-400 mt-2 leading-relaxed">{course.desc}</p>
              </div>
              <div className="pt-4 mt-4 border-t border-obsidian-600 flex items-center justify-between">
                <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1"><CheckCircle2 className="w-3.5 h-3.5" /> AI Tutor Ready</span>
                <Link to={`/course/${course.id}`}>
                  <Button size="sm" variant="outline">Enroll Now</Button>
                </Link>
              </div>
            </Card>
          ))}
        </div>
      </section>
    </div>
  );
};
