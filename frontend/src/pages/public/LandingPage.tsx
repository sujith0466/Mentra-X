import React, { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import { motion, useInView } from "framer-motion";
import {
  Sparkles, ArrowRight, BookOpen, CheckCircle2, TrendingUp, Award, Users,
  ChevronDown, ChevronRight, Target, Brain, Code2, MessageSquare, BarChart3,
  FileText, Mic, Trophy, GraduationCap, Lightbulb, Rocket, Star, Play,
  CheckCheck, Clock, Zap, Shield, Globe, Flame, Calendar,
} from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

/* ── Animation helpers ──────────────────────────────────── */
const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 20 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, margin: "-60px" },
  transition: { duration: 0.5, delay, ease: [0.22, 1, 0.36, 1] as const },
});

const stagger = (i: number) => fadeUp(i * 0.07);

/* ── Animated counter ───────────────────────────────────── */
function AnimatedCounter({ to, suffix = "" }: { to: number; suffix?: string }) {
  const [count, setCount] = useState(0);
  const ref = useRef<HTMLSpanElement>(null);
  const inView = useInView(ref, { once: true });

  useEffect(() => {
    if (!inView) return;
    const duration = 1200;
    const start = performance.now();
    const raf = requestAnimationFrame(function tick(now) {
      const pct = Math.min((now - start) / duration, 1);
      const ease = 1 - Math.pow(1 - pct, 3);
      setCount(Math.round(ease * to));
      if (pct < 1) requestAnimationFrame(tick);
    });
    return () => cancelAnimationFrame(raf);
  }, [inView, to]);

  return <span ref={ref}>{count}{suffix}</span>;
}

/* ── Data ────────────────────────────────────────────────── */
const stats = [
  { value: 50, suffix: "K+", label: "Learning Sessions", icon: BookOpen,   color: "text-indigo-600 dark:text-indigo-400", bg: "bg-indigo-50 dark:bg-indigo-500/10" },
  { value: 98, suffix: "%",  label: "Student Satisfaction", icon: Star,    color: "text-amber-500 dark:text-amber-400",  bg: "bg-amber-50 dark:bg-amber-500/10" },
  { value: 3,  suffix: ".4×", label: "Faster Skill Growth", icon: TrendingUp, color: "text-emerald-600 dark:text-emerald-400", bg: "bg-emerald-50 dark:bg-emerald-500/10" },
  { value: 24, suffix: "/7", label: "AI Tutor Available",  icon: Zap,      color: "text-purple-600 dark:text-purple-400", bg: "bg-purple-50 dark:bg-purple-500/10" },
];

const features = [
  { icon: Brain,    color: "indigo", title: "AI Tutor",           problem: "Stuck on a concept at 2 AM?",         solution: "Your personal AI tutor is available 24/7, adapts to your level, and gives instant, accurate explanations.", outcome: "Never feel lost in a course again." },
  { icon: Target,   color: "rose",   title: "Weakness Detection",  problem: "Don't know what you don't know?",      solution: "Mentra X automatically identifies your knowledge gaps and creates targeted practice drills to close them.", outcome: "Study smarter, not harder." },
  { icon: Code2,    color: "cyan",   title: "Coding Practice",     problem: "Theory without practice goes nowhere.", solution: "Solve real coding challenges with AI-assisted feedback. Get reviewed code, hints, and optimized solutions.", outcome: "Build a strong coding portfolio." },
  { icon: BarChart3,color: "emerald",title: "Progress Tracking",   problem: "Losing motivation without visible progress?", solution: "Visual dashboards show your learning velocity, completed modules, streaks, and skill growth over time.", outcome: "Stay motivated with clear milestones." },
  { icon: Rocket,   color: "purple", title: "Learning Roadmaps",   problem: "Overwhelmed by what to learn first?",  solution: "Upload your resume or pick a career goal and get a step-by-step learning path tailored just for you.", outcome: "Always know your next step." },
  { icon: Mic,      color: "amber",  title: "Mock Interviews",     problem: "Interview anxiety holding you back?",  solution: "Practice technical and behavioral interviews with AI feedback on your answers, confidence, and clarity.", outcome: "Walk into interviews fully prepared." },
  { icon: FileText, color: "teal",   title: "Smart Notes",         problem: "Scattered notes across a dozen apps?", solution: "Capture ideas, summaries, and key concepts in one organized space, searchable and linked to your courses.", outcome: "Build a second brain for learning." },
  { icon: Trophy,   color: "orange", title: "Leaderboards",        problem: "Studying alone can be isolating.",     solution: "Compete and collaborate with students globally. Earn XP, climb leaderboards, and celebrate achievements.", outcome: "Turn learning into a community sport." },
];

const colorMap: Record<string, { bg: string; text: string; border: string }> = {
  indigo: { bg: "bg-indigo-50 dark:bg-indigo-500/10",   text: "text-indigo-600 dark:text-indigo-400",   border: "border-indigo-100 dark:border-indigo-500/20" },
  rose:   { bg: "bg-rose-50 dark:bg-rose-500/10",       text: "text-rose-600 dark:text-rose-400",       border: "border-rose-100 dark:border-rose-500/20" },
  cyan:   { bg: "bg-cyan-50 dark:bg-cyan-500/10",       text: "text-cyan-600 dark:text-cyan-400",       border: "border-cyan-100 dark:border-cyan-500/20" },
  emerald:{ bg: "bg-emerald-50 dark:bg-emerald-500/10", text: "text-emerald-600 dark:text-emerald-400", border: "border-emerald-100 dark:border-emerald-500/20" },
  purple: { bg: "bg-purple-50 dark:bg-purple-500/10",   text: "text-purple-600 dark:text-purple-400",   border: "border-purple-100 dark:border-purple-500/20" },
  amber:  { bg: "bg-amber-50 dark:bg-amber-500/10",     text: "text-amber-600 dark:text-amber-400",     border: "border-amber-100 dark:border-amber-500/20" },
  teal:   { bg: "bg-teal-50 dark:bg-teal-500/10",       text: "text-teal-600 dark:text-teal-400",       border: "border-teal-100 dark:border-teal-500/20" },
  orange: { bg: "bg-orange-50 dark:bg-orange-500/10",   text: "text-orange-600 dark:text-orange-400",   border: "border-orange-100 dark:border-orange-500/20" },
};

const journey = [
  { step: "01", label: "Discover",     desc: "Browse AI-matched courses",         icon: Lightbulb,     color: "indigo" },
  { step: "02", label: "Enroll",       desc: "Start a structured path",           icon: BookOpen,      color: "purple" },
  { step: "03", label: "Study",        desc: "Learn with AI by your side",        icon: Brain,         color: "cyan" },
  { step: "04", label: "Practice",     desc: "Solve real coding challenges",      icon: Code2,         color: "emerald" },
  { step: "05", label: "Improve",      desc: "Close skill gaps automatically",    icon: TrendingUp,    color: "rose" },
  { step: "06", label: "Build",        desc: "Complete real-world projects",      icon: Rocket,        color: "amber" },
  { step: "07", label: "Interview",    desc: "Practice with AI mock interviews",  icon: Mic,           color: "orange" },
  { step: "08", label: "Career Ready", desc: "Land the job you've worked for",    icon: GraduationCap, color: "purple" },
];

const courses = [
  {
    id: "dsa-101", emoji: "🧠", title: "Data Structures & Algorithms",
    desc: "Master arrays, trees, graphs, dynamic programming, and ace technical interviews.",
    level: "Beginner–Advanced", duration: "12 weeks", rating: 4.9, enrolled: "12.4K",
    skills: ["Sorting", "Graph Traversal", "DP", "Recursion"],
    gradient: "from-indigo-500 to-indigo-600", gradientBg: "from-indigo-500/8 to-indigo-500/3",
    accent: "border-indigo-200 dark:border-indigo-500/25",
  },
  {
    id: "ml-202", emoji: "🤖", title: "Machine Learning & AI Foundations",
    desc: "Learn regression, neural networks, model training, and deploy production ML systems.",
    level: "Intermediate", duration: "10 weeks", rating: 4.8, enrolled: "9.2K",
    skills: ["Python", "PyTorch", "Scikit-learn", "NLP"],
    gradient: "from-purple-500 to-purple-600", gradientBg: "from-purple-500/8 to-purple-500/3",
    accent: "border-purple-200 dark:border-purple-500/25",
  },
  {
    id: "web-303", emoji: "🌐", title: "Full-Stack Web Development",
    desc: "Build beautiful, scalable web apps with React, Node.js, databases, and cloud deployment.",
    level: "Beginner", duration: "14 weeks", rating: 4.9, enrolled: "18.7K",
    skills: ["React", "Node.js", "PostgreSQL", "AWS"],
    gradient: "from-cyan-500 to-cyan-600", gradientBg: "from-cyan-500/8 to-cyan-500/3",
    accent: "border-cyan-200 dark:border-cyan-500/25",
  },
];

const faqs = [
  { q: "How does the AI personalize my learning?", a: "Mentra X continuously tracks your progress, identifies which concepts you struggle with, and automatically adjusts your study plan and practice exercises to fill your exact gaps — no manual effort needed." },
  { q: "Do I need any prior experience to start?", a: "Not at all! Whether you're a complete beginner or an experienced student, Mentra X meets you where you are. Every course has a built-in placement check so you start at the right level." },
  { q: "How is this different from YouTube or traditional courses?", a: "Unlike passive videos, Mentra X interacts with you — it quizzes, detects misconceptions, corrects mistakes in real-time, and builds a personalized path. It's like having a personal tutor, not a lecture recording." },
  { q: "Can I use Mentra X to prepare for placements and interviews?", a: "Absolutely. Upload your resume, pick your target companies, and Mentra X generates a custom study roadmap with coding practice, mock interviews, and skill tracking tailored for your placement goals." },
];

/* ── Hero UI Preview (pure CSS mockup) ──────────────────── */
function HeroPreview() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 32, scale: 0.97 }}
      whileInView={{ opacity: 1, y: 0, scale: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1], delay: 0.3 }}
      className="relative max-w-2xl mx-auto mt-12"
    >
      {/* Glow behind */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-b from-indigo-500/15 via-purple-500/10 to-transparent rounded-3xl blur-2xl" />

      {/* Browser chrome */}
      <div className="rounded-2xl border border-slate-200 dark:border-white/10 bg-white dark:bg-obsidian-800 shadow-2xl shadow-slate-900/10 dark:shadow-black/40 overflow-hidden">
        {/* Titlebar */}
        <div className="flex items-center gap-2 px-4 py-3 border-b border-slate-100 dark:border-white/8 bg-slate-50 dark:bg-obsidian-900/60">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-rose-400" />
            <div className="w-3 h-3 rounded-full bg-amber-400" />
            <div className="w-3 h-3 rounded-full bg-emerald-400" />
          </div>
          <div className="flex-1 mx-4 h-5 rounded-md bg-slate-200 dark:bg-obsidian-700 flex items-center px-2">
            <span className="text-[10px] text-slate-400 dark:text-slate-500">app.mentrax.io/student/dashboard</span>
          </div>
        </div>

        {/* Dashboard preview */}
        <div className="p-4 space-y-3">
          {/* Greeting */}
          <div className="flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-slate-900 dark:text-white">Good morning, Alex 👋</div>
              <div className="text-[10px] text-slate-500">Ready to continue your learning journey?</div>
            </div>
            <div className="text-xs font-black text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
              <Flame className="w-3 h-3" /> 14-day streak
            </div>
          </div>

          {/* Stats row */}
          <div className="grid grid-cols-3 gap-2">
            {[
              { label: "Mastery", value: "84%", color: "text-indigo-600 dark:text-indigo-400" },
              { label: "Courses", value: "3", color: "text-purple-600 dark:text-purple-400" },
              { label: "XP Today", value: "420", color: "text-amber-600 dark:text-amber-400" },
            ].map((s) => (
              <div key={s.label} className="bg-slate-50 dark:bg-obsidian-900/60 rounded-lg p-2 text-center border border-slate-100 dark:border-white/6">
                <div className={`text-sm font-black ${s.color}`}>{s.value}</div>
                <div className="text-[9px] text-slate-500 dark:text-slate-400">{s.label}</div>
              </div>
            ))}
          </div>

          {/* Course progress */}
          <div className="space-y-1.5">
            <div className="text-[10px] font-semibold text-slate-600 dark:text-slate-300 uppercase tracking-wider">In Progress</div>
            {[
              { name: "Data Structures & Algorithms", pct: 67, color: "bg-indigo-500" },
              { name: "Machine Learning Foundations", pct: 42, color: "bg-purple-500" },
            ].map((c) => (
              <div key={c.name} className="space-y-1">
                <div className="flex items-center justify-between text-[10px]">
                  <span className="text-slate-700 dark:text-slate-300 font-medium truncate">{c.name}</span>
                  <span className="text-slate-500 ml-2 shrink-0">{c.pct}%</span>
                </div>
                <div className="h-1.5 bg-slate-100 dark:bg-obsidian-700 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    whileInView={{ width: `${c.pct}%` }}
                    viewport={{ once: true }}
                    transition={{ duration: 1, ease: "easeOut", delay: 0.8 }}
                    className={`h-full ${c.color} rounded-full`}
                  />
                </div>
              </div>
            ))}
          </div>

          {/* AI message */}
          <div className="flex gap-2 p-2.5 bg-indigo-50 dark:bg-indigo-500/10 rounded-xl border border-indigo-100 dark:border-indigo-500/20">
            <div className="w-6 h-6 rounded-lg bg-indigo-600 flex items-center justify-center shrink-0">
              <Sparkles className="w-3 h-3 text-white" />
            </div>
            <div>
              <div className="text-[10px] font-semibold text-indigo-700 dark:text-indigo-300">AI Tutor</div>
              <div className="text-[10px] text-slate-600 dark:text-slate-400">You're 2 modules away from mastering Graphs! Let's review DFS today.</div>
            </div>
          </div>
        </div>
      </div>

      {/* Floating badges */}
      <motion.div
        animate={{ y: [0, -5, 0] }}
        transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
        className="absolute -top-3 -right-4 bg-white dark:bg-obsidian-800 border border-emerald-200 dark:border-emerald-500/30 rounded-xl px-3 py-1.5 shadow-lg flex items-center gap-1.5 text-[10px] font-semibold text-emerald-700 dark:text-emerald-300"
      >
        <CheckCircle2 className="w-3 h-3" /> Skill gap closed!
      </motion.div>
      <motion.div
        animate={{ y: [0, 5, 0] }}
        transition={{ duration: 3.5, repeat: Infinity, ease: "easeInOut", delay: 0.5 }}
        className="absolute -bottom-3 -left-4 bg-white dark:bg-obsidian-800 border border-indigo-200 dark:border-indigo-500/30 rounded-xl px-3 py-1.5 shadow-lg flex items-center gap-1.5 text-[10px] font-semibold text-indigo-700 dark:text-indigo-400"
      >
        <Zap className="w-3 h-3" /> 3.4× faster progress
      </motion.div>
    </motion.div>
  );
}

/* ── Main Component ─────────────────────────────────────── */
export const LandingPage: React.FC = () => {
  const [openFaq, setOpenFaq] = useState<number | null>(null);

  return (
    <div className="space-y-24 pb-8">

      {/* ── HERO ─────────────────────────────────────────── */}
      <section className="relative text-center space-y-6 max-w-5xl mx-auto pt-14 px-4 sm:px-6">
        {/* Ambient gradient */}
        <div className="absolute inset-0 -z-10 pointer-events-none overflow-hidden">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[700px] h-[400px] bg-gradient-to-b from-indigo-100/70 via-purple-50/40 to-transparent dark:from-indigo-500/10 dark:via-purple-500/5 dark:to-transparent rounded-full blur-3xl" />
        </div>

        {/* Pill badges */}
        <motion.div {...fadeUp(0)} className="flex flex-wrap items-center justify-center gap-2">
          <span className="inline-flex items-center gap-1.5 text-[11px] font-semibold text-indigo-700 dark:text-indigo-300 bg-indigo-50 dark:bg-indigo-500/10 border border-indigo-100 dark:border-indigo-500/20 px-3 py-1 rounded-full">
            <Sparkles className="w-3 h-3" /> AI-Powered Learning Platform
          </span>
          <span className="inline-flex items-center gap-1.5 text-[11px] font-semibold text-emerald-700 dark:text-emerald-300 bg-emerald-50 dark:bg-emerald-500/10 border border-emerald-100 dark:border-emerald-500/20 px-3 py-1 rounded-full">
            <Shield className="w-3 h-3" /> Safe &amp; Verified AI Responses
          </span>
        </motion.div>

        {/* Headline */}
        <motion.h1
          {...fadeUp(0.08)}
          className="text-4xl sm:text-6xl md:text-7xl font-black tracking-tight text-slate-900 dark:text-white leading-[1.06] text-balance"
        >
          Study Smarter.{" "}
          <span className="block sm:inline">Learn Faster.{" "}</span>
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 via-purple-500 to-pink-500 dark:from-indigo-400 dark:via-purple-400 dark:to-pink-400">
            Build Your Career.
          </span>
        </motion.h1>

        {/* Subheadline */}
        <motion.p
          {...fadeUp(0.14)}
          className="text-lg sm:text-xl text-slate-600 dark:text-slate-300 max-w-2xl mx-auto leading-relaxed"
        >
          Your personal AI learning companion that adapts to{" "}
          <strong className="font-semibold text-slate-800 dark:text-slate-100">your pace, your goals</strong>,
          and your weaknesses — so you grow every single day.
        </motion.p>

        {/* CTAs */}
        <motion.div {...fadeUp(0.2)} className="flex flex-wrap items-center justify-center gap-3 pt-2">
          <Link to="/register">
            <Button size="lg" variant="gradient" rightIcon={<ArrowRight className="w-4 h-4" />}>
              Start Learning Free
            </Button>
          </Link>
          <Link to="/courses">
            <Button size="lg" variant="outline" leftIcon={<Play className="w-4 h-4" />}>
              Explore Courses
            </Button>
          </Link>
        </motion.div>

        <motion.p {...fadeUp(0.26)} className="text-xs text-slate-400 dark:text-slate-500">
          No credit card required · Free account available · Instant access
        </motion.p>

        {/* Stats */}
        <motion.div
          {...fadeUp(0.32)}
          className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-8"
        >
          {stats.map((s) => {
            const Icon = s.icon;
            return (
              <div key={s.label} className="stat-card group">
                <div className={`w-8 h-8 rounded-xl flex items-center justify-center mx-auto mb-2 ${s.bg}`}>
                  <Icon className={`w-4 h-4 ${s.color}`} />
                </div>
                <div className={`text-2xl font-black ${s.color}`}>
                  <AnimatedCounter to={s.value} suffix={s.suffix} />
                </div>
                <div className="text-[11px] font-medium text-slate-500 dark:text-slate-400 mt-0.5">{s.label}</div>
              </div>
            );
          })}
        </motion.div>

        {/* Hero UI Preview */}
        <HeroPreview />
      </section>

      {/* ── VALUE PROPOSITION ─────────────────────────────── */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 space-y-12">
        <motion.div {...fadeUp()} className="text-center space-y-3">
          <Badge variant="indigo" size="sm">Why Mentra X?</Badge>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white">
            Everything you need to succeed
          </h2>
          <p className="text-base text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            One platform. Personalized just for you. Designed to take you from student to career-ready.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {[
            {
              icon: Brain, accent: "indigo", tag: "Personalized Learning",
              title: "AI that actually knows you",
              desc: "Unlike one-size-fits-all courses, Mentra X learns from your study patterns, identifies what you find difficult, and creates a custom study plan just for you.",
              points: ["Adapts to your skill level", "Fills your exact knowledge gaps", "Updates in real-time as you learn"],
            },
            {
              icon: Code2, accent: "cyan", tag: "Hands-On Practice",
              title: "Learn by doing, not just watching",
              desc: "Coding challenges, mock projects, and interactive exercises put your knowledge to work. Get instant AI feedback on every solution you write.",
              points: ["Real coding challenges", "Line-by-line AI feedback", "Build projects for your portfolio"],
            },
            {
              icon: GraduationCap, accent: "purple", tag: "Career Guidance",
              title: "From student to job-ready",
              desc: "Upload your resume and target role to get a personalized career roadmap with skill milestones, mock interviews, and placement preparation.",
              points: ["Custom career roadmap", "Interview preparation", "Resume review & improvement"],
            },
          ].map((item, i) => {
            const Icon = item.icon;
            const c = colorMap[item.accent];
            return (
              <motion.div key={i} {...stagger(i)}>
                <Card variant="default" className="h-full flex flex-col gap-4 hover:border-slate-300 dark:hover:border-white/15 hover:-translate-y-1 transition-all duration-200">
                  <div className={`w-11 h-11 rounded-xl flex items-center justify-center border ${c.bg} ${c.text} ${c.border}`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-1.5">{item.tag}</div>
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white leading-snug">{item.title}</h3>
                    <p className="text-sm text-slate-600 dark:text-slate-400 mt-2 leading-relaxed">{item.desc}</p>
                  </div>
                  <ul className="mt-auto space-y-1.5">
                    {item.points.map((p, pi) => (
                      <li key={pi} className="flex items-center gap-2 text-xs text-slate-700 dark:text-slate-300">
                        <CheckCheck className="w-3.5 h-3.5 text-emerald-500 shrink-0" />{p}
                      </li>
                    ))}
                  </ul>
                </Card>
              </motion.div>
            );
          })}
        </div>
      </section>

      {/* ── FEATURES GRID ─────────────────────────────────── */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 space-y-12">
        <motion.div {...fadeUp()} className="text-center space-y-3">
          <Badge variant="success" size="sm">Platform Features</Badge>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white">
            Every tool you need to learn better
          </h2>
          <p className="text-base text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            Eight powerful features, all working together to accelerate your growth.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {features.map((f, i) => {
            const Icon = f.icon;
            const c = colorMap[f.color];
            return (
              <motion.div key={i} {...stagger(i)}>
                <Card variant="default" className="h-full flex flex-col gap-3 hover:border-slate-300 dark:hover:border-white/15 hover:-translate-y-1 transition-all duration-200 cursor-default">
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center border ${c.bg} ${c.text} ${c.border}`}>
                    <Icon className="w-4.5 h-4.5" />
                  </div>
                  <h3 className="font-bold text-slate-900 dark:text-white text-sm">{f.title}</h3>
                  <div className="space-y-1.5 flex-1">
                    <p className="text-[11px] font-semibold text-slate-400 dark:text-slate-500 italic">{f.problem}</p>
                    <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">{f.solution}</p>
                  </div>
                  <div className="pt-2 border-t border-slate-100 dark:border-white/6">
                    <p className="text-[11px] font-semibold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />{f.outcome}
                    </p>
                  </div>
                </Card>
              </motion.div>
            );
          })}
        </div>
      </section>

      {/* ── STUDENT JOURNEY ───────────────────────────────── */}
      <section className="px-4 py-14 bg-gradient-to-b from-slate-50 to-white dark:from-obsidian-900/60 dark:to-transparent rounded-3xl max-w-6xl mx-auto border border-slate-100 dark:border-white/6">
        <motion.div {...fadeUp()} className="text-center space-y-3 mb-14">
          <Badge variant="purple" size="sm">Your Learning Journey</Badge>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white">
            From beginner to career-ready
          </h2>
          <p className="text-base text-slate-600 dark:text-slate-400 max-w-xl mx-auto">
            A clear, structured path from day one to job offer. You always know where you're going.
          </p>
        </motion.div>

        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3">
          {journey.map((j, i) => {
            const Icon = j.icon;
            const c = colorMap[j.color];
            return (
              <motion.div key={i} {...stagger(i)} className="relative flex flex-col items-center text-center gap-3 group">
                {i < journey.length - 1 && (
                  <div className="hidden lg:block absolute top-6 left-[60%] w-full h-px bg-gradient-to-r from-slate-200 to-slate-100 dark:from-white/8 dark:to-transparent z-0" />
                )}
                <div className={`relative z-10 w-12 h-12 rounded-2xl bg-white dark:bg-obsidian-800 border border-slate-200 dark:border-white/10 shadow-sm flex items-center justify-center group-hover:border-indigo-300 dark:group-hover:border-indigo-500/40 group-hover:shadow-md transition-all duration-200`}>
                  <Icon className={`w-5 h-5 text-slate-400 dark:text-slate-500 group-hover:${c.text} transition-colors`} />
                </div>
                <div>
                  <div className="text-[9px] font-black text-slate-300 dark:text-slate-600 tracking-widest">{j.step}</div>
                  <div className="text-xs font-bold text-slate-900 dark:text-white">{j.label}</div>
                  <div className="text-[10px] text-slate-500 dark:text-slate-400 leading-tight mt-0.5 hidden sm:block">{j.desc}</div>
                </div>
              </motion.div>
            );
          })}
        </div>

        <motion.div {...fadeUp(0.4)} className="text-center mt-12">
          <Link to="/register">
            <Button size="md" variant="gradient" rightIcon={<ArrowRight className="w-4 h-4" />}>
              Begin Your Journey
            </Button>
          </Link>
        </motion.div>
      </section>

      {/* ── COURSE PREVIEW ────────────────────────────────── */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 space-y-10">
        <motion.div {...fadeUp()} className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div className="space-y-2">
            <Badge variant="cyan" size="sm">Popular Courses</Badge>
            <h2 className="text-3xl font-extrabold text-slate-900 dark:text-white">Start with a top course</h2>
            <p className="text-sm text-slate-600 dark:text-slate-400">Structured, hands-on, and powered by AI tutoring from day one.</p>
          </div>
          <Link to="/courses" className="text-sm font-semibold text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 flex items-center gap-1 transition-colors shrink-0">
            View all courses <ChevronRight className="w-4 h-4" />
          </Link>
        </motion.div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-5">
          {courses.map((course, i) => (
            <motion.div key={course.id} {...stagger(i)}>
              <Card variant="interactive" className="flex flex-col gap-4 group h-full">
                {/* Thumbnail */}
                <div className={`w-full h-36 rounded-xl bg-gradient-to-br ${course.gradientBg} border ${course.accent} flex items-center justify-center text-5xl relative overflow-hidden`}>
                  <span className="relative z-10 select-none">{course.emoji}</span>
                  <div className={`absolute inset-0 bg-gradient-to-br ${course.gradient} opacity-5`} />
                </div>

                {/* Meta */}
                <div className="flex items-center justify-between text-[11px] text-slate-500 dark:text-slate-400">
                  <span className="flex items-center gap-1">
                    <Star className="w-3 h-3 text-amber-400 fill-amber-400" />
                    {course.rating} · {course.enrolled} enrolled
                  </span>
                  <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {course.duration}</span>
                </div>

                <div className="flex-1 space-y-2">
                  <h3 className="font-bold text-slate-900 dark:text-white leading-snug group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                    {course.title}
                  </h3>
                  <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">{course.desc}</p>

                  {/* Level badge */}
                  <span className="inline-block text-[10px] font-semibold px-2 py-0.5 rounded-full bg-slate-100 dark:bg-white/8 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-white/10">
                    {course.level}
                  </span>

                  {/* Skills */}
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {course.skills.map((s) => (
                      <span key={s} className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-indigo-50 dark:bg-indigo-500/10 text-indigo-700 dark:text-indigo-300 border border-indigo-100 dark:border-indigo-500/20">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="flex items-center justify-between pt-3 border-t border-slate-100 dark:border-white/6">
                  <span className="text-[11px] font-semibold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> AI Tutor Included
                  </span>
                  <Link to={`/course/${course.id}`}>
                    <Button size="sm" variant="outline" className="group-hover:border-indigo-400 dark:group-hover:border-indigo-500/60 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-all">
                      Enroll Free
                    </Button>
                  </Link>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ── AI SHOWCASE ───────────────────────────────────── */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 space-y-10">
        <motion.div {...fadeUp()} className="text-center space-y-3">
          <Badge variant="purple" size="sm">AI Learning Assistant</Badge>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white">
            Meet your personal AI tutor
          </h2>
          <p className="text-base text-slate-600 dark:text-slate-400 max-w-xl mx-auto">
            Not a chatbot. A genuine learning partner that understands your progress and helps you grow.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {[
            { icon: Brain,         title: "Instant Explanations",  tag: "Always Available",  tagC: "text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-500/10",  desc: "Ask anything about your course. Get clear, step-by-step answers tailored to your current level — never too advanced, never too basic." },
            { icon: Target,        title: "Weakness Detection",    tag: "Fully Automatic",   tagC: "text-rose-600 dark:text-rose-400 bg-rose-50 dark:bg-rose-500/10",          desc: "Mentra X automatically detects when you're struggling with a concept and prepares targeted exercises to strengthen exactly that area." },
            { icon: Globe,         title: "Smart Study Planner",   tag: "Adaptive",          tagC: "text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-500/10", desc: "Your study schedule adapts to your availability and performance. Miss a session? The plan reorganizes itself so you never fall behind." },
            { icon: GraduationCap, title: "Career Assistant",      tag: "Career Ready",      tagC: "text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-500/10",      desc: "From resume review to interview coaching, your AI career assistant prepares you for every step of the hiring process." },
          ].map((item, i) => {
            const Icon = item.icon;
            return (
              <motion.div key={i} {...stagger(i)}>
                <Card variant="glass" className="flex gap-4 items-start hover:border-slate-300 dark:hover:border-white/15 hover:-translate-y-0.5 transition-all duration-200">
                  <div className="p-2.5 rounded-xl bg-white dark:bg-obsidian-900/80 border border-slate-200 dark:border-white/10 shadow-sm shrink-0">
                    <Icon className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                  </div>
                  <div className="space-y-1.5 flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <h3 className="font-bold text-slate-900 dark:text-white text-sm">{item.title}</h3>
                      <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${item.tagC}`}>{item.tag}</span>
                    </div>
                    <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">{item.desc}</p>
                  </div>
                </Card>
              </motion.div>
            );
          })}
        </div>
      </section>

      {/* ── COMMUNITY ─────────────────────────────────────── */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 space-y-10">
        <motion.div {...fadeUp()} className="text-center space-y-3">
          <Badge variant="warning" size="sm">Community</Badge>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white">
            Learn together, grow faster
          </h2>
          <p className="text-base text-slate-600 dark:text-slate-400 max-w-xl mx-auto">
            Join a thriving community of students who motivate each other every day.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { icon: MessageSquare, title: "Discussion Forum",    desc: "Ask questions, share solutions, help others learn.", color: "indigo", link: "/community/discussions" },
            { icon: Trophy,        title: "Leaderboard",         desc: "Compete on weekly XP rankings and earn recognition.", color: "amber",  link: "/community/leaderboard" },
            { icon: Users,         title: "Study Groups",        desc: "Join topic-based study groups and solve problems together.", color: "emerald", link: "/community/groups" },
            { icon: Calendar,      title: "Events & Hackathons", desc: "Participate in coding events, webinars, and competitions.", color: "purple", link: "/community/events" },
          ].map((item, i) => {
            const Icon = item.icon;
            const c = colorMap[item.color];
            return (
              <motion.div key={i} {...stagger(i)}>
                <Link to={item.link}>
                  <Card variant="default" className="h-full text-center flex flex-col items-center gap-3 hover:border-slate-300 dark:hover:border-white/15 hover:-translate-y-1 transition-all duration-200 cursor-pointer">
                    <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${c.bg}`}>
                      <Icon className={`w-5 h-5 ${c.text}`} />
                    </div>
                    <h3 className="font-bold text-slate-900 dark:text-white text-sm">{item.title}</h3>
                    <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">{item.desc}</p>
                  </Card>
                </Link>
              </motion.div>
            );
          })}
        </div>
      </section>

      {/* ── WHY MENTRA X ─────────────────────────────────── */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6">
        <motion.div {...fadeUp()}>
          <div className="rounded-2xl bg-gradient-to-br from-slate-50 via-indigo-50/40 to-purple-50/30 dark:from-obsidian-800 dark:via-indigo-950/30 dark:to-obsidian-800 border border-slate-200 dark:border-white/8 p-8 sm:p-12 space-y-10">
            <div className="max-w-2xl mx-auto text-center space-y-3">
              <Badge variant="indigo" size="sm">Why Students Choose Us</Badge>
              <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white">
                Not just another course platform
              </h2>
              <p className="text-sm sm:text-base text-slate-600 dark:text-slate-400">
                Traditional platforms give you videos and quizzes. Mentra X gives you a thinking partner.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {[
                { icon: TrendingUp, color: "indigo", title: "Continuous Progress Tracking",  desc: "Visual dashboards map your mastery across every skill area, highlight what's improving, and what still needs work." },
                { icon: Award,      color: "emerald", title: "Verified Achievements",        desc: "Every skill you master is logged and verifiable. Show employers real evidence of your learning, not just a certificate." },
                { icon: Users,      color: "purple",  title: "Community & Collaboration",    desc: "Learn alongside thousands of ambitious students. Share progress, tackle challenges together, and motivate each other." },
              ].map((item, i) => {
                const Icon = item.icon;
                const c = colorMap[item.color];
                return (
                  <div key={i} className="p-5 rounded-xl bg-white dark:bg-obsidian-900/60 border border-slate-200 dark:border-white/8 space-y-3">
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${c.bg}`}>
                      <Icon className={`w-5 h-5 ${c.text}`} />
                    </div>
                    <h3 className="font-bold text-slate-900 dark:text-white">{item.title}</h3>
                    <p className="text-sm text-slate-600 dark:text-slate-400 leading-relaxed">{item.desc}</p>
                  </div>
                );
              })}
            </div>
          </div>
        </motion.div>
      </section>

      {/* ── FAQ ───────────────────────────────────────────── */}
      <section className="max-w-3xl mx-auto px-4 sm:px-6 space-y-8">
        <motion.div {...fadeUp()} className="text-center space-y-3">
          <Badge variant="cyan" size="sm">FAQ</Badge>
          <h2 className="text-3xl font-extrabold text-slate-900 dark:text-white">
            Questions? We've got answers.
          </h2>
        </motion.div>

        <motion.div initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true }} transition={{ duration: 0.4, delay: 0.1 }} className="space-y-2.5">
          {faqs.map((faq, i) => (
            <div
              key={i}
              className="rounded-xl border border-slate-200 dark:border-white/8 bg-white dark:bg-obsidian-800 overflow-hidden transition-all duration-200"
            >
              <button
                onClick={() => setOpenFaq(openFaq === i ? null : i)}
                className="w-full flex items-center justify-between p-5 text-left group"
                aria-expanded={openFaq === i}
              >
                <span className="font-semibold text-slate-900 dark:text-white text-sm pr-4 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">
                  {faq.q}
                </span>
                <ChevronDown
                  className={`w-4 h-4 text-slate-400 shrink-0 transition-transform duration-200 ${openFaq === i ? "rotate-180" : ""}`}
                />
              </button>
              {openFaq === i && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  className="px-5 pb-5 text-sm text-slate-600 dark:text-slate-400 leading-relaxed border-t border-slate-100 dark:border-white/6 pt-4"
                >
                  {faq.a}
                </motion.div>
              )}
            </div>
          ))}
        </motion.div>

        <motion.div {...fadeUp(0.2)} className="text-center">
          <Link to="/faq">
            <Button variant="ghost" size="sm" rightIcon={<ChevronRight className="w-4 h-4" />}>
              View all frequently asked questions
            </Button>
          </Link>
        </motion.div>
      </section>

      {/* ── FINAL CTA ─────────────────────────────────────── */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6">
        <motion.div {...fadeUp()}>
          <div className="rounded-3xl bg-gradient-to-br from-indigo-600 via-purple-600 to-indigo-700 p-10 sm:p-16 text-center relative overflow-hidden">
            <div className="absolute -top-20 -right-20 w-72 h-72 bg-white/6 rounded-full blur-3xl pointer-events-none" />
            <div className="absolute -bottom-20 -left-20 w-72 h-72 bg-purple-400/12 rounded-full blur-3xl pointer-events-none" />

            <div className="relative z-10 space-y-6 max-w-2xl mx-auto">
              <div className="inline-flex items-center gap-2 bg-white/15 text-white text-xs font-semibold px-3.5 py-1.5 rounded-full border border-white/20 backdrop-blur-sm">
                <Sparkles className="w-3.5 h-3.5" /> Free to get started · No credit card needed
              </div>

              <h2 className="text-3xl sm:text-5xl font-black text-white tracking-tight leading-tight">
                Start your learning journey today.
              </h2>

              <p className="text-base text-indigo-100 leading-relaxed">
                Join thousands of students who are already learning smarter, building faster, and landing better opportunities with Mentra X.
              </p>

              <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
                <Link to="/register">
                  <Button
                    size="lg"
                    className="bg-white text-indigo-700 hover:bg-slate-50 shadow-xl border-2 border-white font-bold hover:-translate-y-0.5 transition-all"
                    rightIcon={<ArrowRight className="w-4 h-4" />}
                  >
                    Create Free Account
                  </Button>
                </Link>
                <Link to="/courses">
                  <Button
                    size="lg"
                    className="bg-white/15 hover:bg-white/25 text-white border border-white/30 hover:-translate-y-0.5 transition-all font-semibold backdrop-blur-sm"
                  >
                    Browse Courses
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

    </div>
  );
};
