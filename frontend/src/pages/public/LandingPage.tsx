import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { 
  Sparkles, 
  ArrowRight, 
  BrainCircuit, 
  ShieldCheck, 
  Zap, 
  BookOpen, 
  CheckCircle2, 
  TrendingUp, 
  Award, 
  Users, 
  HelpCircle, 
  ChevronRight,
  Terminal,
  Cpu,
  Lock
} from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { SafetyBadge } from "@/components/widgets/SafetyBadge";
import { ConfidenceMeter } from "@/components/widgets/ConfidenceMeter";

export const LandingPage: React.FC = () => {
  const faqs = [
    {
      q: "How does the Cognitive Digital Twin personalize my learning?",
      a: "Your Digital Twin continuously models your learning velocity, knowledge retention, and skill gaps in real-time. It predicts when you might forget a concept and adjusts your study planner automatically using intelligent vector memory engines."
    },
    {
      q: "What is AI Safety Verification Interception?",
      a: "AI Safety Verification is our real-time operational safety interceptor. Before any AI tutor response is rendered to you, it is checked against authoritative course syllabus embeddings to guarantee zero hallucinations and 100% curriculum accuracy."
    },
    {
      q: "Can I use Mentra X for enterprise engineering team training?",
      a: "Yes. Mentra X includes enterprise admin dashboards, AI swarm monitoring, custom course authoring, and granular audit logs designed for technical teams mastering complex architectures."
    },
    {
      q: "How do I get started with adaptive learning?",
      a: "Simply browse the Course Catalog, enroll in any course, or upload your resume in the Career & Resume section to instantly generate a custom career roadmap."
    }
  ];

  return (
    <div className="space-y-24 py-8">
      {/* Hero Section */}
      <section className="relative text-center space-y-8 max-w-5xl mx-auto pt-10">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[350px] bg-primary-600/15 dark:bg-primary-600/20 rounded-full blur-3xl -z-10 pointer-events-none" />
        
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-slate-100 dark:bg-white/5 border border-slate-200 dark:border-white/10 text-xs font-semibold text-indigo-700 dark:text-indigo-300 shadow-sm"
        >
          <Sparkles className="w-3.5 h-3.5 text-primary-600 dark:text-primary-500 animate-pulse" />
          <span>Enterprise Certified AI Safety Active</span>
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping ml-1" />
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="text-4xl sm:text-6xl md:text-7xl font-extrabold tracking-tight text-slate-900 dark:text-white leading-tight sm:leading-none"
        >
          The Next-Generation AI LMS with <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-600 via-ai-violet to-indigo-500 dark:from-primary-500 dark:via-ai-violet dark:to-indigo-300">Cognitive Digital Twins</span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="text-lg sm:text-xl text-slate-600 dark:text-slate-300 max-w-3xl mx-auto font-normal leading-relaxed"
        >
          Experience hyper-personalized AI tutoring powered by intelligent vector memory engines, adaptive career pathways, and real-time safety interception. Built for modern enterprise engineering teams.
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
          <Link to="/documentation">
            <Button size="lg" variant="ghost">
              Architecture Docs
            </Button>
          </Link>
        </motion.div>

        {/* Hero Quick Stats Row */}
        <motion.div 
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-8 max-w-4xl mx-auto border-t border-slate-200 dark:border-obsidian-600/60"
        >
          <div className="p-4 rounded-xl bg-white/60 dark:bg-obsidian-800/40 border border-slate-200/60 dark:border-white/5 backdrop-blur-sm">
            <div className="text-2xl font-black text-slate-900 dark:text-white">50,000+</div>
            <div className="text-xs font-medium text-slate-500 dark:text-slate-400 mt-0.5">Vector Memory Embeddings</div>
          </div>
          <div className="p-4 rounded-xl bg-white/60 dark:bg-obsidian-800/40 border border-slate-200/60 dark:border-white/5 backdrop-blur-sm">
            <div className="text-2xl font-black text-emerald-600 dark:text-emerald-400">99.9%</div>
            <div className="text-xs font-medium text-slate-500 dark:text-slate-400 mt-0.5">Safety Intercept Rate</div>
          </div>
          <div className="p-4 rounded-xl bg-white/60 dark:bg-obsidian-800/40 border border-slate-200/60 dark:border-white/5 backdrop-blur-sm">
            <div className="text-2xl font-black text-indigo-600 dark:text-indigo-400">&lt; 50ms</div>
            <div className="text-xs font-medium text-slate-500 dark:text-slate-400 mt-0.5">Swarm Response Latency</div>
          </div>
          <div className="p-4 rounded-xl bg-white/60 dark:bg-obsidian-800/40 border border-slate-200/60 dark:border-white/5 backdrop-blur-sm">
            <div className="text-2xl font-black text-purple-600 dark:text-purple-400">100%</div>
            <div className="text-xs font-medium text-slate-500 dark:text-slate-400 mt-0.5">Syllabus Mapping Parity</div>
          </div>
        </motion.div>
      </section>

      {/* Live Enterprise Demo Widget Showcase */}
      <section className="space-y-6">
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-white">Powered by Autonomous AI Swarms</h2>
          <p className="text-sm text-slate-600 dark:text-slate-400">Our tri-layer intelligence engine continuously models, verifies, and optimizes your technical mastery.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
          <Card variant="glass" className="space-y-4 flex flex-col justify-between hover:border-purple-500/40">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <Badge variant="purple" size="sm">Intelligent AI Engine</Badge>
                <SafetyBadge status="APPROVE" score={0.99} />
              </div>
              <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <BrainCircuit className="w-5 h-5 text-ai-violet" /> Real-Time Cognitive Sync
              </h3>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                Your Digital Twin continuously models your learning velocity, mastery gaps, and retrieval retention in real-time, predicting optimal study interventions before decay occurs.
              </p>
            </div>
            <div className="pt-2">
              <ConfidenceMeter score={0.96} label="Twin Prediction Accuracy" size="sm" />
            </div>
          </Card>

          <Card variant="glass" className="space-y-4 flex flex-col justify-between hover:border-cyan-500/40">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <Badge variant="cyan" size="sm">AI Safety Verification</Badge>
                <Badge variant="success" size="sm">100% Secure</Badge>
              </div>
              <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-cyan-600 dark:text-cyan-400" /> Zero Hallucination Guarantee
              </h3>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                All AI tutoring outputs are intercepted and validated against authoritative course syllabus embeddings before rendering to protect technical learning integrity.
              </p>
            </div>
            <div className="p-2.5 rounded bg-slate-100 dark:bg-obsidian-900 border border-slate-200 dark:border-white/5 font-mono text-[11px] text-emerald-600 dark:text-emerald-400 mt-2">
              [SAFETY_VERIFIED]: Content matches syllabus embedding #4092 with 0.992 cosine similarity.
            </div>
          </Card>

          <Card variant="glass" className="space-y-4 flex flex-col justify-between hover:border-amber-500/40">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <Badge variant="primary" size="sm">Adaptive LMS</Badge>
                <Badge variant="default" size="sm">Personalized Memory</Badge>
              </div>
              <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <Zap className="w-5 h-5 text-amber-500 dark:text-amber-400" /> Dynamic Career Roadmaps
              </h3>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                Upload your technical resume to instantly generate custom learning pathways tailored to target enterprise job descriptions and industry competence benchmarks.
              </p>
            </div>
            <div className="flex items-center justify-between text-xs text-slate-700 dark:text-slate-300 pt-2 border-t border-slate-200 dark:border-white/5 mt-2">
              <span>Skill Gap Closure Rate</span>
              <span className="font-bold text-indigo-600 dark:text-indigo-400">3.4x Faster</span>
            </div>
          </Card>
        </div>
      </section>

      {/* Featured Courses Preview */}
      <section className="space-y-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Featured Enterprise Courses</h2>
            <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">Curated syllabi with automated AI tutoring support and interactive coding challenges.</p>
          </div>
          <Link to="/courses" className="text-xs font-semibold text-primary-600 dark:text-primary-500 hover:text-indigo-700 dark:hover:text-indigo-300 transition-colors flex items-center gap-1">
            View All Courses <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {[
            { id: "ai-101", title: "Advanced Agentic Coding & Orchestration", desc: "Master intelligent AI engines, multi-agent workflows, tool execution, and autonomous software development.", level: "Advanced", modules: 12, icon: Terminal },
            { id: "cs-202", title: "Enterprise Cloud Architecture & Distributed Systems", desc: "Design fault-tolerant, high-concurrency microservices and data pipelines on AWS/GCP.", level: "Intermediate", modules: 8, icon: Cpu },
            { id: "ml-303", title: "Vector Memory Systems & Similarity Engineering", desc: "Build semantic search engines, hybrid retrieval architectures, and production RAG pipelines.", level: "Advanced", modules: 10, icon: Lock },
          ].map((course) => {
            const CourseIcon = course.icon;
            return (
              <Card key={course.id} variant="interactive" className="flex flex-col justify-between group">
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <Badge variant="primary">{course.level}</Badge>
                    <span className="text-xs text-slate-500 dark:text-slate-400 flex items-center gap-1">
                      <BookOpen className="w-3.5 h-3.5" /> {course.modules} Modules
                    </span>
                  </div>
                  <div className="flex items-center gap-2 mb-2">
                    <div className="p-2 rounded-lg bg-primary-500/10 text-primary-600 dark:text-primary-400 group-hover:scale-105 transition-transform">
                      <CourseIcon className="w-5 h-5" />
                    </div>
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white leading-snug group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">{course.title}</h3>
                  </div>
                  <p className="text-xs text-slate-600 dark:text-slate-400 mt-2 leading-relaxed">{course.desc}</p>
                </div>
                <div className="pt-4 mt-6 border-t border-slate-200 dark:border-obsidian-600 flex items-center justify-between">
                  <span className="text-xs font-semibold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> AI Tutor Ready
                  </span>
                  <Link to={`/course/${course.id}`}>
                    <Button size="sm" variant="outline" className="group-hover:border-primary-500/50">Enroll Now</Button>
                  </Link>
                </div>
              </Card>
            );
          })}
        </div>
      </section>

      {/* Student Success & Why Mentra X Section */}
      <section className="rounded-2xl bg-gradient-to-tr from-slate-100 via-indigo-50/50 to-purple-50/30 dark:from-obsidian-800 dark:via-obsidian-800/80 dark:to-indigo-950/30 border border-slate-200 dark:border-indigo-500/20 p-8 sm:p-12 shadow-sm dark:shadow-glow space-y-8">
        <div className="max-w-3xl mx-auto text-center space-y-3">
          <Badge variant="purple" size="md">Enterprise Impact</Badge>
          <h2 className="text-2xl sm:text-4xl font-extrabold text-slate-900 dark:text-white tracking-tight">Why Leading Engineers Choose Mentra X</h2>
          <p className="text-sm sm:text-base text-slate-600 dark:text-slate-300">
            Traditional LMS platforms rely on static videos and generic multiple-choice quizzes. Mentra X transforms technical learning into an active, verified feedback loop.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
          <div className="p-6 rounded-xl bg-white dark:bg-obsidian-900/60 border border-slate-200 dark:border-white/10 space-y-3">
            <div className="w-10 h-10 rounded-lg bg-indigo-500/10 flex items-center justify-center text-indigo-600 dark:text-indigo-400">
              <TrendingUp className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-slate-900 dark:text-white">Continuous Velocity Tracking</h3>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              Your Digital Twin maps mastery against 500+ granular engineering competencies, eliminating redundant review and focusing 100% on active growth.
            </p>
          </div>

          <div className="p-6 rounded-xl bg-white dark:bg-obsidian-900/60 border border-slate-200 dark:border-white/10 space-y-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-500/10 flex items-center justify-center text-emerald-600 dark:text-emerald-400">
              <Award className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-slate-900 dark:text-white">Verifiable Certification</h3>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              Every completed module and coding challenge is validated by AI Safety Verification and permanently recorded in your student audit log for employer verification.
            </p>
          </div>

          <div className="p-6 rounded-xl bg-white dark:bg-obsidian-900/60 border border-slate-200 dark:border-white/10 space-y-3">
            <div className="w-10 h-10 rounded-lg bg-purple-500/10 flex items-center justify-center text-purple-600 dark:text-purple-400">
              <Users className="w-5 h-5" />
            </div>
            <h3 className="font-bold text-base text-slate-900 dark:text-white">Peer Guilds & Leaderboards</h3>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              Collaborate in study guilds, compete on real-time XP leaderboards, and solve community architectural challenges with top software engineers worldwide.
            </p>
          </div>
        </div>
      </section>

      {/* FAQ Section Preview */}
      <section className="space-y-8 max-w-4xl mx-auto">
        <div className="text-center space-y-2">
          <Badge variant="cyan">Got Questions?</Badge>
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-white">Frequently Asked Questions</h2>
          <p className="text-sm text-slate-600 dark:text-slate-400">Everything you need to know about the Mentra X enterprise architecture and AI tutoring.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {faqs.map((faq, index) => (
            <Card key={index} className="space-y-2 border-slate-200 dark:border-obsidian-600 bg-white dark:bg-obsidian-800">
              <h3 className="font-bold text-sm sm:text-base text-slate-900 dark:text-white flex items-start gap-2">
                <HelpCircle className="w-4 h-4 text-primary-500 shrink-0 mt-1" /> {faq.q}
              </h3>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed pl-6">
                {faq.a}
              </p>
            </Card>
          ))}
        </div>

        <div className="text-center pt-2">
          <Link to="/faq">
            <Button variant="ghost" size="sm" rightIcon={<ChevronRight className="w-4 h-4" />}>
              View All 15+ Enterprise FAQs
            </Button>
          </Link>
        </div>
      </section>

      {/* Final Call to Action Banner */}
      <section className="rounded-2xl bg-gradient-to-r from-primary-600 via-indigo-600 to-purple-600 p-8 sm:p-12 text-center text-white shadow-xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-80 h-80 bg-white/10 rounded-full blur-3xl -z-0 pointer-events-none" />
        <div className="relative z-10 max-w-2xl mx-auto space-y-6">
          <h2 className="text-3xl sm:text-4xl font-black tracking-tight leading-tight">Ready to Master Advanced Agentic AI?</h2>
          <p className="text-sm sm:text-base text-indigo-100 font-normal">
            Join thousands of engineering students and software architects learning with autonomous cognitive digital twins today.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-4 pt-2">
            <Link to="/register">
              <Button size="lg" className="bg-white text-slate-900 hover:bg-slate-100 shadow-xl border-0 font-bold">
                Get Started for Free
              </Button>
            </Link>
            <Link to="/courses">
              <Button size="lg" variant="outline" className="border-white/30 text-white hover:bg-white/10">
                Browse Course Syllabi
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};
